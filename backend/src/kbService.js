import fs from 'node:fs';
import path from 'node:path';
import { parseExerciseMarkdown } from './exerciseParser.js';

const IGNORED_DIRS = new Set(['编排记录', '编排维护', '原卷页', '章节入口', '__pycache__', '.git']);

function toPosix(p) {
  return p.split(path.sep).join('/');
}

export class KbService {
  constructor(kbRoot) {
    this.kbRoot = path.resolve(kbRoot);
  }

  /**
   * 从知识库根目录的索引 Markdown（如 `00·*.md`）动态解析“章节号 -> 阶段标题”映射。
   */
  _parseStagesFromIndexMd(kbAbs, fallbackStage) {
    const stageMap = new Map();
    if (!fs.existsSync(kbAbs)) return stageMap;

    const indexFile = fs
      .readdirSync(kbAbs)
      .find(f => f.endsWith('.md') && (f.startsWith('00') || f.toLowerCase() === 'index.md'));
    if (!indexFile) return stageMap;

    const content = fs.readFileSync(path.join(kbAbs, indexFile), 'utf-8');
    let currentHeading = fallbackStage;

    for (const rawLine of content.split(/\r?\n/)) {
      const line = rawLine.trim();
      const mH = line.match(/^#{2,3}\s+(.+)$/);
      if (mH) {
        currentHeading = mH[1].trim();
        continue;
      }
      if (line.startsWith('-')) {
        for (const mLink of line.matchAll(/\[\[(\d{2})·[^\]]+\]\]/g)) {
          stageMap.set(mLink[1], currentHeading);
        }
      }
    }
    return stageMap;
  }

  /**
   * 自动从知识库根目录下的 `00·*.md` 提取一句简短描述作为卡片副标题（零硬编码）
   */
  _extractSubtitleFromIndexMd(kbAbs, dirName) {
    if (!fs.existsSync(kbAbs)) return '';
    const indexFile = fs
      .readdirSync(kbAbs)
      .find(f => f.endsWith('.md') && (f.startsWith('00') || f.toLowerCase() === 'index.md'));
    if (!indexFile) return `底层 Markdown 实时渲染驱动 · ${dirName}`;

    const content = fs.readFileSync(path.join(kbAbs, indexFile), 'utf-8');
    for (const rawLine of content.split(/\r?\n/)) {
      const line = rawLine.trim();
      if (
        !line ||
        line.startsWith('#') ||
        line.startsWith('[[') ||
        line.startsWith('-') ||
        line.startsWith('|') ||
        line.startsWith('>')
      ) {
        continue;
      }
      return line.replace(/\*\*([^*]+)\*\*/g, '$1').slice(0, 72);
    }
    return `底层 Markdown 实时渲染驱动 · ${dirName}`;
  }

  /**
   * 直接扫描 `knowledge-base/` 下的一级文件夹作为独立知识库，零子知识库嵌套、零硬编码学科名。
   */
  listKnowledgeBases() {
    if (!fs.existsSync(this.kbRoot)) return [];
    const entries = fs
      .readdirSync(this.kbRoot, { withFileTypes: true })
      .filter(e => e.isDirectory() && !e.name.startsWith('.') && !IGNORED_DIRS.has(e.name))
      .sort((a, b) => a.name.localeCompare(b.name, 'zh-Hans-CN', { numeric: true }));

    return entries.map(entry => {
      const dirName = entry.name;
      const kbAbs = path.join(this.kbRoot, dirName);
      const hasExercises = fs.existsSync(path.join(kbAbs, '强化题目'));

      let meta = {};
      const metaPath = path.join(kbAbs, 'kb.json');
      if (fs.existsSync(metaPath)) {
        try {
          meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
        } catch {}
      }

      return {
        id: dirName,
        dirName,
        title: meta.title || dirName,
        subtitle: meta.subtitle || this._extractSubtitleFromIndexMd(kbAbs, dirName),
        icon: meta.icon || (hasExercises ? '📘' : '📗'),
        badge: meta.badge || (hasExercises ? '学习 + 刷题' : '知识查阅'),
        hasExercises
      };
    });
  }

  getKbConfig(kbId) {
    const kbs = this.listKnowledgeBases();
    return kbs.find(k => k.id === kbId) || null;
  }

  /**
   * 扫描单个一级知识库文件夹下的全部根文档、分类子目录、双链索引与练习题集
   */
  scanKb(kbId) {
    const kb = this.getKbConfig(kbId);
    if (!kb) return null;

    const kbAbs = path.join(this.kbRoot, kb.dirName);
    if (!fs.existsSync(kbAbs)) return null;

    const shortTitle = kb.title.replace(/^\d+\./, '');
    const stageMap = this._parseStagesFromIndexMd(kbAbs, shortTitle);

    const stemMap = new Map();
    const orderedDocs = [];
    const exerciseFiles = new Map(); // code ("01") -> { absPath, stage, rawCode }
    const exerciseCodes = new Set();

    // 扫描 `强化题目/`（若该知识库存在练习题目录）
    const exDir = path.join(kbAbs, '强化题目');
    if (fs.existsSync(exDir)) {
      for (const f of fs.readdirSync(exDir).sort((a, b) => a.localeCompare(b, 'zh-Hans-CN', { numeric: true }))) {
        if (!f.endsWith('.md') || f.startsWith('00')) continue;
        const m = f.match(/^(\d{2})·(.+)\.md$/);
        if (m) {
          const code = m[1];
          exerciseCodes.add(code);
          exerciseFiles.set(code, {
            absPath: path.join(exDir, f),
            stage: stageMap.get(code) || shortTitle,
            rawCode: code
          });
        }
      }
    }

    const entries = fs
      .readdirSync(kbAbs, { withFileTypes: true })
      .sort((a, b) => a.name.localeCompare(b.name, 'zh-Hans-CN', { numeric: true }));

    const rootDocs = [];
    const groups = [];

    for (const entry of entries) {
      if (entry.name.startsWith('.') || IGNORED_DIRS.has(entry.name) || entry.name.includes('快照')) {
        continue;
      }
      const fullPath = path.join(kbAbs, entry.name);
      const relPath = entry.name;

      if (entry.isFile() && entry.name.endsWith('.md')) {
        const stem = entry.name.replace(/\.md$/, '');
        if (!stemMap.has(stem)) stemMap.set(stem, relPath);
        const docItem = this._buildDocItem(entry.name, relPath, exerciseCodes);
        rootDocs.push(docItem);
        orderedDocs.push(docItem);
      } else if (entry.isDirectory()) {
        if (entry.name === '强化题目') {
          for (const f of fs.readdirSync(fullPath)) {
            if (f.endsWith('.md')) {
              const stem = f.replace(/\.md$/, '');
              stemMap.set(stem, toPosix(path.join(relPath, f)));
            }
          }
          continue;
        }
        const subDocs = this._collectMarkdownFiles(fullPath, relPath, exerciseCodes, stemMap, orderedDocs);
        if (subDocs.length > 0) {
          groups.push({
            name: entry.name,
            path: relPath,
            docs: subDocs
          });
        }
      }
    }

    return {
      kb,
      rootDocs,
      groups,
      stemMap,
      orderedDocs,
      exerciseFiles
    };
  }

  _collectMarkdownFiles(dirAbs, relPrefix, exerciseCodes, stemMap, orderedDocs) {
    const entries = fs
      .readdirSync(dirAbs, { withFileTypes: true })
      .sort((a, b) => a.name.localeCompare(b.name, 'zh-Hans-CN', { numeric: true }));
    const docs = [];
    for (const entry of entries) {
      if (entry.name.startsWith('.') || IGNORED_DIRS.has(entry.name) || entry.name.includes('快照')) {
        continue;
      }
      const fullPath = path.join(dirAbs, entry.name);
      const relPath = toPosix(path.join(relPrefix, entry.name));
      if (entry.isFile() && entry.name.endsWith('.md')) {
        const stem = entry.name.replace(/\.md$/, '');
        if (!stemMap.has(stem)) stemMap.set(stem, relPath);
        const item = this._buildDocItem(entry.name, relPath, exerciseCodes);
        docs.push(item);
        orderedDocs.push(item);
      } else if (entry.isDirectory()) {
        const nested = this._collectMarkdownFiles(fullPath, relPath, exerciseCodes, stemMap, orderedDocs);
        docs.push(...nested);
      }
    }
    return docs;
  }

  _buildDocItem(filename, relPath, exerciseCodes) {
    const stem = filename.replace(/\.md$/, '');
    const mChap = stem.match(/^(\d{2})·(.+)$/);
    const code = mChap ? mChap[1] : null;
    const displayTitle = mChap ? `${mChap[1]} · ${mChap[2]}` : stem;
    const exerciseCode = code && code !== '00' && exerciseCodes?.has(code) ? code : null;

    return {
      name: filename,
      stem,
      code,
      title: displayTitle,
      path: relPath,
      exerciseCode
    };
  }

  resolveSafeKbPath(kb, relPath) {
    const kbAbs = path.resolve(this.kbRoot, kb.dirName);
    const abs = path.resolve(kbAbs, path.normalize(relPath));
    if (!abs.startsWith(kbAbs)) {
      throw new Error('Invalid path outside knowledge base');
    }
    return abs;
  }

  readDocument(kbId, relPath) {
    const scan = this.scanKb(kbId);
    if (!scan) return null;

    let targetRel = relPath;
    if (!targetRel.endsWith('.md') && scan.stemMap.has(targetRel)) {
      targetRel = scan.stemMap.get(targetRel);
    } else if (targetRel.endsWith('.md') && !fs.existsSync(this.resolveSafeKbPath(scan.kb, targetRel))) {
      const stem = path.basename(targetRel, '.md');
      if (scan.stemMap.has(stem)) targetRel = scan.stemMap.get(stem);
    }

    const abs = this.resolveSafeKbPath(scan.kb, targetRel);
    if (!fs.existsSync(abs) || !fs.statSync(abs).isFile()) {
      return null;
    }

    const content = fs.readFileSync(abs, 'utf-8');
    const idx = scan.orderedDocs.findIndex(d => d.path === toPosix(targetRel));
    const currentItem =
      idx >= 0 ? scan.orderedDocs[idx] : this._buildDocItem(path.basename(abs), toPosix(targetRel), new Set());
    const prevDoc = idx > 0 ? scan.orderedDocs[idx - 1] : null;
    const nextDoc = idx >= 0 && idx + 1 < scan.orderedDocs.length ? scan.orderedDocs[idx + 1] : null;

    return {
      ...currentItem,
      content,
      prevDoc,
      nextDoc
    };
  }

  getExerciseChapter(kbId, chapterCode) {
    const scan = this.scanKb(kbId);
    if (!scan) return null;
    const code = String(chapterCode).trim().padStart(2, '0');
    const info = scan.exerciseFiles.get(code);
    if (!info || !fs.existsSync(info.absPath)) return null;
    const raw = fs.readFileSync(info.absPath, 'utf-8');
    return parseExerciseMarkdown(raw, path.basename(info.absPath), info.stage);
  }

  getAllExercises(kbId) {
    const scan = this.scanKb(kbId);
    if (!scan) return [];
    const list = [];
    for (const [, info] of scan.exerciseFiles.entries()) {
      const raw = fs.readFileSync(info.absPath, 'utf-8');
      list.push(parseExerciseMarkdown(raw, path.basename(info.absPath), info.stage));
    }
    return list.sort((a, b) => a.num - b.num);
  }
}
