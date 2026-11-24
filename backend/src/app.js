import express from 'express';
import { DatabaseSync } from 'node:sqlite';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { KbService } from './kbService.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export function createApp(options = {}) {
  const dbPath = options.dbPath || path.resolve(__dirname, '../data/knowledge-hub.db');
  const kbRoot = options.kbRoot || path.resolve(__dirname, '../../knowledge-base');
  const distDir = options.distDir || path.resolve(__dirname, '../../frontend/dist');

  fs.mkdirSync(path.dirname(dbPath), { recursive: true });
  const db = new DatabaseSync(dbPath);

  db.exec(`
    CREATE TABLE IF NOT EXISTS practice_records (
      kb_id TEXT NOT NULL,
      chapter_code TEXT NOT NULL,
      question_id TEXT NOT NULL,
      user_input TEXT NOT NULL DEFAULT '',
      grade TEXT NOT NULL DEFAULT '',
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      PRIMARY KEY (kb_id, chapter_code, question_id)
    );
    CREATE TABLE IF NOT EXISTS chapter_progress (
      kb_id TEXT NOT NULL,
      doc_path TEXT NOT NULL,
      completed INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      PRIMARY KEY (kb_id, doc_path)
    );
  `);

  const kbService = new KbService(kbRoot);
  const app = express();
  app.use(express.json());

  app.get('/api/health', (_req, res) => {
    res.json({ status: 'ok' });
  });

  // 1. 多知识库门户列表
  app.get('/api/kbs', (_req, res) => {
    const kbs = kbService.listKnowledgeBases();
    const enriched = kbs.map(kb => {
      const scan = kbService.scanKb(kb.id);
      const totalDocs = scan ? scan.orderedDocs.length : 0;
      const completedDocs = db
        .prepare('SELECT COUNT(*) AS cnt FROM chapter_progress WHERE kb_id = ? AND completed = 1')
        .get(kb.id).cnt;
      const masteredQuestions = db
        .prepare("SELECT COUNT(*) AS cnt FROM practice_records WHERE kb_id = ? AND grade = 'ok'")
        .get(kb.id).cnt;
      const wrongQuestions = db
        .prepare("SELECT COUNT(*) AS cnt FROM practice_records WHERE kb_id = ? AND grade IN ('bad', 'warn')")
        .get(kb.id).cnt;

      return {
        ...kb,
        stats: {
          moduleCount: kb.modules.length,
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

  // 2. 知识库目录树 + 章节完成度 + 各章刷题统计
  app.get('/api/kbs/:kbId/tree', (req, res) => {
    const { kbId } = req.params;
    const scan = kbService.scanKb(kbId);
    if (!scan) return res.status(404).json({ error: 'Knowledge base not found' });

    const progressRows = db
      .prepare('SELECT doc_path, completed FROM chapter_progress WHERE kb_id = ?')
      .all(kbId);
    const completedSet = new Set(progressRows.filter(r => r.completed === 1).map(r => r.doc_path));

    const gradeRows = db
      .prepare('SELECT chapter_code, question_id, grade FROM practice_records WHERE kb_id = ?')
      .all(kbId);
    const gradesByChapter = {};
    for (const r of gradeRows) {
      if (!gradesByChapter[r.chapter_code]) gradesByChapter[r.chapter_code] = {};
      gradesByChapter[r.chapter_code][r.question_id] = r.grade;
    }

    const decorateDoc = doc => ({
      ...doc,
      completed: completedSet.has(doc.path)
    });

    const modules = scan.modules.map(m => ({
      ...m,
      rootDocs: m.rootDocs.map(decorateDoc),
      groups: m.groups.map(g => ({
        ...g,
        docs: g.docs.map(decorateDoc)
      }))
    }));

    // Build exercise chapters summary
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
    const wrongTotal = gradeRows.filter(r => r.grade === 'bad' || r.grade === 'warn').length;

    res.json({
      kb: scan.kb,
      modules,
      exercises: exerciseSummaries,
      stemIndex,
      wrongTotal
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
      const row = db
        .prepare('SELECT completed FROM chapter_progress WHERE kb_id = ? AND doc_path = ?')
        .get(kbId, doc.path);
      res.json({
        ...doc,
        completed: row ? row.completed === 1 : false
      });
    } catch (err) {
      res.status(400).json({ error: err.message });
    }
  });

  // 4. 更新章节“已学完”勾选状态
  app.put('/api/kbs/:kbId/chapter-progress', (req, res) => {
    const { kbId } = req.params;
    const { docPath, completed } = req.body ?? {};
    if (!docPath) return res.status(400).json({ error: 'docPath is required' });
    const val = completed ? 1 : 0;
    db.prepare(`
      INSERT INTO chapter_progress (kb_id, doc_path, completed, updated_at)
      VALUES (?, ?, ?, datetime('now'))
      ON CONFLICT(kb_id, doc_path) DO UPDATE SET
        completed = excluded.completed,
        updated_at = datetime('now')
    `).run(kbId, docPath, val);
    res.json({ kbId, docPath, completed: Boolean(val) });
  });

  // 5. 实时解析单章强化练习题 + 合并 SQLite 做题记录
  app.get('/api/kbs/:kbId/exercise/:chapterCode', (req, res) => {
    const { kbId, chapterCode } = req.params;
    const ex = kbService.getExerciseChapter(kbId, chapterCode);
    if (!ex) return res.status(404).json({ error: 'Exercise chapter not found' });

    const records = db
      .prepare('SELECT question_id, user_input, grade FROM practice_records WHERE kb_id = ? AND chapter_code = ?')
      .all(kbId, ex.code);
    const recMap = {};
    for (const r of records) {
      recMap[r.question_id] = { userInput: r.user_input, grade: r.grade };
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

  // 6. 保存单题作答输入或自评状态到 SQLite
  app.put('/api/kbs/:kbId/practice', (req, res) => {
    const { kbId } = req.params;
    const { chapterCode, questionId, userInput, grade } = req.body ?? {};
    if (!chapterCode || !questionId) {
      return res.status(400).json({ error: 'chapterCode and questionId are required' });
    }
    const code = String(chapterCode).padStart(2, '0');
    const existing = db
      .prepare('SELECT user_input, grade FROM practice_records WHERE kb_id = ? AND chapter_code = ? AND question_id = ?')
      .get(kbId, code, questionId);

    const nextInput = userInput !== undefined ? String(userInput) : (existing?.user_input ?? '');
    const nextGrade = grade !== undefined ? String(grade) : (existing?.grade ?? '');

    db.prepare(`
      INSERT INTO practice_records (kb_id, chapter_code, question_id, user_input, grade, updated_at)
      VALUES (?, ?, ?, ?, ?, datetime('now'))
      ON CONFLICT(kb_id, chapter_code, question_id) DO UPDATE SET
        user_input = excluded.user_input,
        grade = excluded.grade,
        updated_at = datetime('now')
    `).run(kbId, code, questionId, nextInput, nextGrade);

    res.json({
      kbId,
      chapterCode: code,
      questionId,
      userInput: nextInput,
      grade: nextGrade
    });
  });

  // 7. 重置某章全部刷题记录
  app.delete('/api/kbs/:kbId/practice/:chapterCode', (req, res) => {
    const { kbId, chapterCode } = req.params;
    const code = String(chapterCode).padStart(2, '0');
    const info = db
      .prepare('DELETE FROM practice_records WHERE kb_id = ? AND chapter_code = ?')
      .run(kbId, code);
    res.json({ deletedCount: info.changes });
  });

  // 8. 全局错题与不稳题本
  app.get('/api/kbs/:kbId/wrongbook', (req, res) => {
    const { kbId } = req.params;
    const rows = db
      .prepare(`
        SELECT chapter_code, question_id, user_input, grade, updated_at
        FROM practice_records
        WHERE kb_id = ? AND grade IN ('bad', 'warn')
        ORDER BY chapter_code ASC, question_id ASC
      `)
      .all(kbId);

    const byChapter = {};
    for (const r of rows) {
      if (!byChapter[r.chapter_code]) {
        byChapter[r.chapter_code] = kbService.getExerciseChapter(kbId, r.chapter_code);
      }
    }

    const items = [];
    for (const r of rows) {
      const ex = byChapter[r.chapter_code];
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
