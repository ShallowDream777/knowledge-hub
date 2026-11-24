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
   * 发现所有知识库。
   * 默认将当前 `1.英语...`、`2.同等学力...`、`3.英语语法...` 聚合为 `english`（英语知识库）。
   * 若未来在 `knowledge-base/` 下新建其他顶层学科文件夹（如 `math/` 或带 `kb.json` 的目录），自动作为新知识库卡片展示。
   */
  listKnowledgeBases() {
    if (!fs.existsSync(this.kbRoot)) return [];
    const entries = fs.readdirSync(this.kbRoot, { withFileTypes: true }).filter(e => e.isDirectory());

    const englishModules = [];
    const customKbs = [];

    for (const entry of entries) {
      if (IGNORED_DIRS.has(entry.name) || entry.name.startsWith('.')) continue;
      if (/^[123]\..*英语/.test(entry.name) || entry.name.includes('英语')) {
        englishModules.push(entry.name);
      } else {
        customKbs.push(entry.name);
      }
    }

    const result = [];
    if (englishModules.length > 0) {
      result.push({
        id: 'english',
        title: '英语知识库',
        subtitle: '零基础完整线性语法 · 语法知识字典 · 同等学力申硕考试强化',
        icon: '📘',
        badge: '核心主线',
        modules: englishModules.sort()
      });
    }

    for (const dirName of customKbs.sort()) {
      const metaPath = path.join(this.kbRoot, dirName, 'kb.json');
      let meta = {};
      if (fs.existsSync(metaPath)) {
        try {
          meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
        } catch {}
      }
      result.push({
        id: dirName.toLowerCase().replace(/[^a-z0-9_-]/g, '-'),
        title: meta.title || dirName,
        subtitle: meta.subtitle || `${dirName} 知识库`,
        icon: meta.icon || '📗',
        badge: meta.badge || '扩展知识库',
        modules: [dirName]
      });
    }

    return result;
  }

  getKbConfig(kbId) {
    const kbs = this.listKnowledgeBases();
    return kbs.find(k => k.id === kbId) || null;
  }

  /**
   * 扫描指定知识库下的所有模块、文档树、双链索引与练习集文件
   */
  scanKb(kbId) {
    const kb = this.getKbConfig(kbId);
    if (!kb) return null;

    const modules = [];
    const stemMap = new Map(); // stem -> relativePath
    const orderedDocs = [];
    const exerciseFiles = new Map(); // chapterCode ("01") -> absPath

    for (const modName of kb.modules) {
      const modAbs = path.join(this.kbRoot, modName);
      if (!fs.existsSync(modAbs)) continue;

      // Scan exercises in `1.英语学习资料·完整线性版/强化题目`
      const exDir = path.join(modAbs, '强化题目');
      if (fs.existsSync(exDir) && modName.startsWith('1.')) {
        for (const f of fs.readdirSync(exDir).sort()) {
          const m = f.match(/^(\d{2})·强化练习·(.+)\.md$/);
          if (m) {
            exerciseFiles.set(m[1], path.join(exDir, f));
          }
        }
      }

      const modNode = this._scanModuleDir(modAbs, modName, stemMap, orderedDocs);
      modules.push(modNode);
    }

    return { kb, modules, stemMap, orderedDocs, exerciseFiles };
  }

  _scanModuleDir(dirAbs, relPrefix, stemMap, orderedDocs) {
    const entries = fs.readdirSync(dirAbs, { withFileTypes: true }).sort((a, b) =>
      a.name.localeCompare(b.name, 'zh-Hans-CN', { numeric: true })
    );

    const rootDocs = [];
    const groups = [];

    for (const entry of entries) {
      if (entry.name.startsWith('.') || IGNORED_DIRS.has(entry.name) || entry.name.includes('快照')) {
        continue;
      }
      const fullPath = path.join(dirAbs, entry.name);
      const relPath = toPosix(path.join(relPrefix, entry.name));

      if (entry.isFile() && entry.name.endsWith('.md')) {
        const stem = entry.name.replace(/\.md$/, '');
        if (!stemMap.has(stem)) stemMap.set(stem, relPath);
        const docItem = this._buildDocItem(entry.name, relPath);
        rootDocs.push(docItem);
        if (!relPath.includes('/强化题目/')) {
          orderedDocs.push(docItem);
        }
      } else if (entry.isDirectory()) {
        // Skip raw exercise markdown folder in main reading tree for Module 1 (since interactive practice has its own tab)
        if (entry.name === '强化题目' && relPrefix.startsWith('1.')) {
          // Still register stems so wiki-links to [[01·强化练习·...]] can be resolved
          for (const f of fs.readdirSync(fullPath)) {
            if (f.endsWith('.md')) {
              const stem = f.replace(/\.md$/, '');
              stemMap.set(stem, toPosix(path.join(relPath, f)));
            }
          }
          continue;
        }
        const subDocs = this._collectMarkdownFiles(fullPath, relPath, stemMap, orderedDocs);
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
      name: relPrefix,
      shortName: relPrefix.replace(/^\d+\./, ''),
      rootDocs,
      groups
    };
  }

  _collectMarkdownFiles(dirAbs, relPrefix, stemMap, orderedDocs) {
    const entries = fs.readdirSync(dirAbs, { withFileTypes: true }).sort((a, b) =>
      a.name.localeCompare(b.name, 'zh-Hans-CN', { numeric: true })
    );
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
        const item = this._buildDocItem(entry.name, relPath);
        docs.push(item);
        if (!relPath.includes('/强化题目/')) {
          orderedDocs.push(item);
        }
      }
    }
    return docs;
  }

  _buildDocItem(filename, relPath) {
    const stem = filename.replace(/\.md$/, '');
    const mChap = stem.match(/^(\d{2})·(.+)$/);
    const code = mChap ? mChap[1] : null;
    const displayTitle = mChap ? `${mChap[1]} · ${mChap[2]}` : stem;
    const exerciseCode =
      relPath.startsWith('1.') && relPath.includes('/章节/') && code && code !== '00' ? code : null;
    return {
      name: filename,
      stem,
      code,
      title: displayTitle,
      path: relPath,
      exerciseCode
    };
  }

  resolveSafePath(relPath) {
    const normalized = path.normalize(relPath);
    const abs = path.resolve(this.kbRoot, normalized);
    if (!abs.startsWith(this.kbRoot)) {
      throw new Error('Invalid path outside knowledge base');
    }
    return abs;
  }

  readDocument(kbId, relPath) {
    const scan = this.scanKb(kbId);
    if (!scan) return null;

    // Allow resolving by exact relative path OR by wiki-link stem
    let targetRel = relPath;
    if (!targetRel.endsWith('.md') && scan.stemMap.has(targetRel)) {
      targetRel = scan.stemMap.get(targetRel);
    } else if (targetRel.endsWith('.md') && !fs.existsSync(this.resolveSafePath(targetRel))) {
      const stem = path.basename(targetRel, '.md');
      if (scan.stemMap.has(stem)) targetRel = scan.stemMap.get(stem);
    }

    const abs = this.resolveSafePath(targetRel);
    if (!fs.existsSync(abs) || !fs.statSync(abs).isFile()) {
      return null;
    }

    const content = fs.readFileSync(abs, 'utf-8');
    const idx = scan.orderedDocs.findIndex(d => d.path === toPosix(targetRel));
    const currentItem =
      idx >= 0 ? scan.orderedDocs[idx] : this._buildDocItem(path.basename(abs), toPosix(targetRel));
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
    const padded = String(chapterCode).padStart(2, '0');
    const exPath = scan.exerciseFiles.get(padded);
    if (!exPath || !fs.existsSync(exPath)) return null;
    const raw = fs.readFileSync(exPath, 'utf-8');
    return parseExerciseMarkdown(raw, path.basename(exPath));
  }

  getAllExercises(kbId) {
    const scan = this.scanKb(kbId);
    if (!scan) return [];
    const list = [];
    for (const [code, exPath] of scan.exerciseFiles.entries()) {
      const raw = fs.readFileSync(exPath, 'utf-8');
      list.push(parseExerciseMarkdown(raw, path.basename(exPath)));
    }
    return list.sort((a, b) => a.num - b.num);
  }
}
