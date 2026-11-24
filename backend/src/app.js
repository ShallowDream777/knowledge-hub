import express from 'express';
import { DatabaseSync } from 'node:sqlite';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { KbService } from './kbService.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function hashPassword(password, salt = crypto.randomBytes(16).toString('hex')) {
  const hash = crypto.scryptSync(String(password), salt, 64).toString('hex');
  return `${salt}:${hash}`;
}

function verifyPassword(password, stored) {
  const [salt, key] = String(stored).split(':');
  if (!salt || !key) return false;
  const hashBuffer = crypto.scryptSync(String(password), salt, 64);
  const keyBuffer = Buffer.from(key, 'hex');
  if (hashBuffer.length !== keyBuffer.length) return false;
  return crypto.timingSafeEqual(hashBuffer, keyBuffer);
}

export function createApp(options = {}) {
  const dbPath = options.dbPath || path.resolve(__dirname, '../data/knowledge-hub.db');
  const kbRoot = options.kbRoot || path.resolve(__dirname, '../../knowledge-base');
  const distDir = options.distDir || path.resolve(__dirname, '../../frontend/dist');

  fs.mkdirSync(path.dirname(dbPath), { recursive: true });
  const db = new DatabaseSync(dbPath);

  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      token TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS user_practice_records (
      user_id INTEGER NOT NULL,
      kb_id TEXT NOT NULL,
      chapter_code TEXT NOT NULL,
      question_id TEXT NOT NULL,
      user_input TEXT NOT NULL DEFAULT '',
      grade TEXT NOT NULL DEFAULT '',
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      PRIMARY KEY (user_id, kb_id, chapter_code, question_id)
    );
    CREATE TABLE IF NOT EXISTS user_chapter_progress (
      user_id INTEGER NOT NULL,
      kb_id TEXT NOT NULL,
      doc_path TEXT NOT NULL,
      completed INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      PRIMARY KEY (user_id, kb_id, doc_path)
    );
    CREATE TABLE IF NOT EXISTS user_reading_state (
      user_id INTEGER NOT NULL,
      kb_id TEXT NOT NULL,
      last_doc_path TEXT NOT NULL,
      last_doc_title TEXT NOT NULL,
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      PRIMARY KEY (user_id, kb_id)
    );
  `);

  const kbService = new KbService(kbRoot);
  const app = express();
  app.use(express.json({ limit: '2mb' }));

  // Optional auth middleware: attaches req.user if valid Bearer token is present
  app.use((req, _res, next) => {
    const auth = req.headers.authorization || '';
    if (auth.startsWith('Bearer ')) {
      const token = auth.slice(7).trim();
      if (token) {
        const user = db
          .prepare('SELECT id, username FROM users WHERE token = ?')
          .get(token);
        if (user) {
          req.user = { id: user.id, username: user.username };
        }
      }
    }
    next();
  });

  app.get('/api/health', (_req, res) => {
    res.json({ status: 'ok' });
  });

  // ==================== Auth Endpoints ====================
  app.post('/api/auth/register', (req, res) => {
    const { username, password } = req.body ?? {};
    const cleanUser = String(username || '').trim();
    const cleanPass = String(password || '');
    if (!cleanUser || cleanUser.length < 2) {
      return res.status(400).json({ error: '用户名至少需要 2 个字符' });
    }
    if (!cleanPass || cleanPass.length < 4) {
      return res.status(400).json({ error: '密码至少需要 4 个字符' });
    }
    const existing = db.prepare('SELECT id FROM users WHERE username = ?').get(cleanUser);
    if (existing) {
      return res.status(409).json({ error: '该用户名已存在，请直接登录' });
    }
    const token = crypto.randomBytes(24).toString('hex');
    const pwHash = hashPassword(cleanPass);
    const info = db
      .prepare('INSERT INTO users (username, password_hash, token) VALUES (?, ?, ?)')
      .run(cleanUser, pwHash, token);

    res.status(201).json({
      token,
      user: { id: Number(info.lastInsertRowid), username: cleanUser }
    });
  });

  app.post('/api/auth/login', (req, res) => {
    const { username, password } = req.body ?? {};
    const cleanUser = String(username || '').trim();
    const cleanPass = String(password || '');
    const row = db
      .prepare('SELECT id, username, password_hash FROM users WHERE username = ?')
      .get(cleanUser);
    if (!row || !verifyPassword(cleanPass, row.password_hash)) {
      return res.status(401).json({ error: '用户名或密码错误' });
    }
    const token = crypto.randomBytes(24).toString('hex');
    db.prepare('UPDATE users SET token = ? WHERE id = ?').run(token, row.id);
    res.json({
      token,
      user: { id: row.id, username: row.username }
    });
  });

  app.get('/api/auth/me', (req, res) => {
    res.json({ user: req.user || null });
  });

  app.post('/api/auth/logout', (req, res) => {
    if (req.user) {
      db.prepare('UPDATE users SET token = NULL WHERE id = ?').run(req.user.id);
    }
    res.json({ ok: true });
  });

  // ==================== Knowledge Base Endpoints ====================
  // 1. 多知识库门户列表（已登录返回数据库统计与上次阅读章节，未登录返回基础结构供前端叠加本地缓存）
  app.get('/api/kbs', (req, res) => {
    const kbs = kbService.listKnowledgeBases();
    const userId = req.user?.id || null;

    const enriched = kbs.map(kb => {
      const scan = kbService.scanKb(kb.id);
      const totalDocs = scan ? scan.orderedDocs.length : 0;

      let completedDocs = 0;
      let masteredQuestions = 0;
      let wrongQuestions = 0;
      let lastRead = null;

      if (userId) {
        completedDocs = db
          .prepare('SELECT COUNT(*) AS cnt FROM user_chapter_progress WHERE user_id = ? AND kb_id = ? AND completed = 1')
          .get(userId, kb.id).cnt;
        masteredQuestions = db
          .prepare("SELECT COUNT(*) AS cnt FROM user_practice_records WHERE user_id = ? AND kb_id = ? AND grade = 'ok'")
          .get(userId, kb.id).cnt;
        wrongQuestions = db
          .prepare("SELECT COUNT(*) AS cnt FROM user_practice_records WHERE user_id = ? AND kb_id = ? AND grade IN ('bad', 'warn')")
          .get(userId, kb.id).cnt;
        const lr = db
          .prepare('SELECT last_doc_path, last_doc_title, updated_at FROM user_reading_state WHERE user_id = ? AND kb_id = ?')
          .get(userId, kb.id);
        if (lr) {
          lastRead = {
            docPath: lr.last_doc_path,
            docTitle: lr.last_doc_title,
            updatedAt: lr.updated_at
          };
        }
      }

      return {
        ...kb,
        lastRead,
        stats: {
          totalDocs,
          completedDocs,
          masteredQuestions,
          wrongQuestions,
          totalExercises: scan ? scan.exerciseFiles.size : 0
        }
      };
    });
    res.json(enriched);
  });

  // 2. 知识库目录树 + 章节完成度 + 各章刷题统计 + 数据库全量用户记录（已登录时下发以便与本地缓存融合）
  app.get('/api/kbs/:kbId/tree', (req, res) => {
    const { kbId } = req.params;
    const scan = kbService.scanKb(kbId);
    if (!scan) return res.status(404).json({ error: 'Knowledge base not found' });

    const userId = req.user?.id || null;
    const completedSet = new Set();
    const gradesByChapter = {};
    const dbPracticeMap = {}; // "01:A01" -> { userInput, grade }
    let lastRead = null;

    if (userId) {
      const progressRows = db
        .prepare('SELECT doc_path, completed FROM user_chapter_progress WHERE user_id = ? AND kb_id = ?')
        .all(userId, kbId);
      for (const r of progressRows) {
        if (r.completed === 1) completedSet.add(r.doc_path);
      }

      const gradeRows = db
        .prepare('SELECT chapter_code, question_id, user_input, grade FROM user_practice_records WHERE user_id = ? AND kb_id = ?')
        .all(userId, kbId);
      for (const r of gradeRows) {
        if (!gradesByChapter[r.chapter_code]) gradesByChapter[r.chapter_code] = {};
        gradesByChapter[r.chapter_code][r.question_id] = r.grade;
        dbPracticeMap[`${r.chapter_code}:${r.question_id}`] = {
          userInput: r.user_input,
          grade: r.grade
        };
      }

      const lr = db
        .prepare('SELECT last_doc_path, last_doc_title, updated_at FROM user_reading_state WHERE user_id = ? AND kb_id = ?')
        .get(userId, kbId);
      if (lr) {
        lastRead = {
          docPath: lr.last_doc_path,
          docTitle: lr.last_doc_title,
          updatedAt: lr.updated_at
        };
      }
    }

    const decorateDoc = doc => ({
      ...doc,
      completed: completedSet.has(doc.path)
    });

    const rootDocs = scan.rootDocs.map(decorateDoc);
    const groups = scan.groups.map(g => ({
      ...g,
      docs: g.docs.map(decorateDoc)
    }));

    const allExercises = kbService.getAllExercises(kbId);
    const exerciseSummaries = allExercises.map(ex => {
      const chGrades = gradesByChapter[ex.code] || {};
      const reqQs = ex.questions.filter(q => q.required);
      const okReq = reqQs.filter(q => chGrades[q.id] === 'ok').length;
      const gradedReq = reqQs.filter(q => chGrades[q.id]).length;
      const wrongCount = ex.questions.filter(q => chGrades[q.id] === 'bad' || chGrades[q.id] === 'warn').length;
      return {
        num: ex.num,
        code: ex.code,
        title: ex.title,
        stage: ex.stage,
        totalQuestions: ex.questions.length,
        requiredCount: reqQs.length,
        okRequiredCount: okReq,
        gradedRequiredCount: gradedReq,
        wrongCount
      };
    });

    const stemIndex = Object.fromEntries(scan.stemMap.entries());
    const wrongTotal = Object.values(dbPracticeMap).filter(
      r => r.grade === 'bad' || r.grade === 'warn'
    ).length;

    res.json({
      kb: scan.kb,
      rootDocs,
      groups,
      exercises: exerciseSummaries,
      stemIndex,
      wrongTotal,
      lastRead,
      dbState: userId
        ? {
            practice: dbPracticeMap,
            completedDocs: [...completedSet],
            lastRead
          }
        : null
    });
  });

  // 3. 实时读取底层 Markdown 文档内容
  app.get('/api/kbs/:kbId/doc', (req, res) => {
    const { kbId } = req.params;
    const relPath = req.query.path;
    if (!relPath || typeof relPath !== 'string') {
      return res.status(400).json({ error: 'Missing path query parameter' });
    }
    try {
      const doc = kbService.readDocument(kbId, relPath);
      if (!doc) return res.status(404).json({ error: 'Document not found' });
      let completed = false;
      if (req.user) {
        const row = db
          .prepare('SELECT completed FROM user_chapter_progress WHERE user_id = ? AND kb_id = ? AND doc_path = ?')
          .get(req.user.id, kbId, doc.path);
        completed = row ? row.completed === 1 : false;
      }
      res.json({
        ...doc,
        completed
      });
    } catch (err) {
      res.status(400).json({ error: err.message });
    }
  });

  // 4. 保存上次阅读章节记录（已登录时写入 SQLite）
  app.put('/api/kbs/:kbId/reading-state', (req, res) => {
    const { kbId } = req.params;
    const { docPath, docTitle } = req.body ?? {};
    if (!docPath || !docTitle) {
      return res.status(400).json({ error: 'docPath and docTitle are required' });
    }
    if (!req.user) {
      return res.json({ savedToDb: false, docPath, docTitle });
    }
    db.prepare(`
      INSERT INTO user_reading_state (user_id, kb_id, last_doc_path, last_doc_title, updated_at)
      VALUES (?, ?, ?, ?, datetime('now'))
      ON CONFLICT(user_id, kb_id) DO UPDATE SET
        last_doc_path = excluded.last_doc_path,
        last_doc_title = excluded.last_doc_title,
        updated_at = datetime('now')
    `).run(req.user.id, kbId, docPath, docTitle);

    res.json({ savedToDb: true, docPath, docTitle });
  });

  // 5. 更新章节“已学完”勾选状态（已登录时写入 SQLite）
  app.put('/api/kbs/:kbId/chapter-progress', (req, res) => {
    const { kbId } = req.params;
    const { docPath, completed } = req.body ?? {};
    if (!docPath) return res.status(400).json({ error: 'docPath is required' });
    const val = completed ? 1 : 0;
    if (req.user) {
      db.prepare(`
        INSERT INTO user_chapter_progress (user_id, kb_id, doc_path, completed, updated_at)
        VALUES (?, ?, ?, ?, datetime('now'))
        ON CONFLICT(user_id, kb_id, doc_path) DO UPDATE SET
          completed = excluded.completed,
          updated_at = datetime('now')
      `).run(req.user.id, kbId, docPath, val);
    }
    res.json({ kbId, docPath, completed: Boolean(val), savedToDb: Boolean(req.user) });
  });

  // 6. 实时解析单章强化练习题 + 合并当前登录用户 SQLite 做题记录
  app.get('/api/kbs/:kbId/exercise/:chapterCode', (req, res) => {
    const { kbId, chapterCode } = req.params;
    const ex = kbService.getExerciseChapter(kbId, chapterCode);
    if (!ex) return res.status(404).json({ error: 'Exercise chapter not found' });

    const recMap = {};
    if (req.user) {
      const records = db
        .prepare('SELECT question_id, user_input, grade FROM user_practice_records WHERE user_id = ? AND kb_id = ? AND chapter_code = ?')
        .all(req.user.id, kbId, ex.code);
      for (const r of records) {
        recMap[r.question_id] = { userInput: r.user_input, grade: r.grade };
      }
    }

    const questions = ex.questions.map(q => ({
      ...q,
      userInput: recMap[q.id]?.userInput || '',
      grade: recMap[q.id]?.grade || ''
    }));

    res.json({
      ...ex,
      questions
    });
  });

  // 7. 保存单题作答输入或自评状态到 SQLite（已登录时写入）
  app.put('/api/kbs/:kbId/practice', (req, res) => {
    const { kbId } = req.params;
    const { chapterCode, questionId, userInput, grade } = req.body ?? {};
    if (!chapterCode || !questionId) {
      return res.status(400).json({ error: 'chapterCode and questionId are required' });
    }
    const raw = String(chapterCode).trim();
    const code = raw.includes('-') ? raw : raw.padStart(2, '0');
    if (!req.user) {
      return res.json({
        savedToDb: false,
        kbId,
        chapterCode: code,
        questionId,
        userInput: userInput ?? '',
        grade: grade ?? ''
      });
    }

    const existing = db
      .prepare('SELECT user_input, grade FROM user_practice_records WHERE user_id = ? AND kb_id = ? AND chapter_code = ? AND question_id = ?')
      .get(req.user.id, kbId, code, questionId);

    const nextInput = userInput !== undefined ? String(userInput) : (existing?.user_input ?? '');
    const nextGrade = grade !== undefined ? String(grade) : (existing?.grade ?? '');

    db.prepare(`
      INSERT INTO user_practice_records (user_id, kb_id, chapter_code, question_id, user_input, grade, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
      ON CONFLICT(user_id, kb_id, chapter_code, question_id) DO UPDATE SET
        user_input = excluded.user_input,
        grade = excluded.grade,
        updated_at = datetime('now')
    `).run(req.user.id, kbId, code, questionId, nextInput, nextGrade);

    res.json({
      savedToDb: true,
      kbId,
      chapterCode: code,
      questionId,
      userInput: nextInput,
      grade: nextGrade
    });
  });

  // 8. 登录后将浏览器本地缓存补齐到数据库（仅填补数据库尚未记录的项，确保“优先读数据库、同时不丢未登录时的缓存”）
  app.post('/api/kbs/:kbId/sync-local', (req, res) => {
    if (!req.user) return res.status(401).json({ error: 'Not logged in' });
    const { kbId } = req.params;
    const { practice = {}, completedDocs = [], lastRead = null } = req.body ?? {};
    const userId = req.user.id;

    // 1) reading state: only insert if DB has no record yet
    if (lastRead?.docPath && lastRead?.docTitle) {
      db.prepare(`
        INSERT OR IGNORE INTO user_reading_state (user_id, kb_id, last_doc_path, last_doc_title, updated_at)
        VALUES (?, ?, ?, ?, datetime('now'))
      `).run(userId, kbId, lastRead.docPath, lastRead.docTitle);
    }

    // 2) completed docs: only insert if DB has no record yet
    const insDoc = db.prepare(`
      INSERT OR IGNORE INTO user_chapter_progress (user_id, kb_id, doc_path, completed, updated_at)
      VALUES (?, ?, ?, 1, datetime('now'))
    `);
    for (const docPath of completedDocs) {
      if (docPath) insDoc.run(userId, kbId, docPath);
    }

    // 3) practice records: only insert or fill empty fields if DB has no record yet
    const insPrac = db.prepare(`
      INSERT OR IGNORE INTO user_practice_records (user_id, kb_id, chapter_code, question_id, user_input, grade, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
    `);
    for (const [key, val] of Object.entries(practice)) {
      const [chCode, qid] = key.split(':');
      if (chCode && qid && (val.userInput || val.grade)) {
        insPrac.run(userId, kbId, chCode, qid, String(val.userInput || ''), String(val.grade || ''));
      }
    }

    res.json({ synced: true });
  });

  // 9. 重置某章全部刷题记录
  app.delete('/api/kbs/:kbId/practice/:chapterCode', (req, res) => {
    const { kbId, chapterCode } = req.params;
    const raw = String(chapterCode).trim();
    const code = raw.includes('-') ? raw : raw.padStart(2, '0');
    if (!req.user) return res.json({ deletedCount: 0, savedToDb: false });
    const info = db
      .prepare('DELETE FROM user_practice_records WHERE user_id = ? AND kb_id = ? AND chapter_code = ?')
      .run(req.user.id, kbId, code);
    res.json({ deletedCount: info.changes, savedToDb: true });
  });

  // 10. 全局错题本（支持已登录从 DB 聚合，或未登录由前端传入 keys / 前端本地聚合；这里同时提供全量题库字典接口供前端本地缓存模式秒级聚合）
  app.get('/api/kbs/:kbId/wrongbook', (req, res) => {
    const { kbId } = req.params;
    const allExercises = kbService.getAllExercises(kbId);
    const exMap = Object.fromEntries(allExercises.map(ex => [ex.code, ex]));

    if (req.user) {
      const rows = db
        .prepare(`
          SELECT chapter_code, question_id, user_input, grade, updated_at
          FROM user_practice_records
          WHERE user_id = ? AND kb_id = ? AND grade IN ('bad', 'warn')
          ORDER BY chapter_code ASC, question_id ASC
        `)
        .all(req.user.id, kbId);

      const items = [];
      for (const r of rows) {
        const ex = exMap[r.chapter_code];
        if (!ex) continue;
        const q = ex.questions.find(item => item.id === r.question_id);
        if (!q) continue;
        items.push({
          chapterCode: ex.code,
          chapterTitle: ex.title,
          ...q,
          userInput: r.user_input,
          grade: r.grade,
          updatedAt: r.updated_at
        });
      }
      return res.json({ total: items.length, items });
    }

    // Guest mode: allow passing ?keys=01:A01,02:B01 to resolve full question details
    const rawKeys = String(req.query.keys || '').trim();
    if (!rawKeys) return res.json({ total: 0, items: [] });

    const items = [];
    for (const pair of rawKeys.split(',')) {
      const [chCode, qid] = pair.split(':');
      const ex = exMap[chCode];
      if (!ex) continue;
      const q = ex.questions.find(item => item.id === qid);
      if (!q) continue;
      items.push({
        chapterCode: ex.code,
        chapterTitle: ex.title,
        ...q
      });
    }
    res.json({ total: items.length, items });
  });

  // 生产环境静态托管 frontend/dist
  if (fs.existsSync(distDir)) {
    app.use(express.static(distDir));
    app.get('*', (req, res, next) => {
      if (req.path.startsWith('/api/')) return next();
      res.sendFile(path.join(distDir, 'index.html'));
    });
  }

  return { app, db, kbService };
}
