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
   * 从模块根目录的索引 Markdown（如 `00·*.md`）动态解析“章节号 -> 阶段标题”映射。
   * 规则：扫描所有 `## ...` 或 `### ...` 标题，将其下方出现的 `[[01·...]]` 章节号归入该标题名下。
   * 这样任何知识库或模块的阶段划分都由 Markdown 文档自身决定，无需在代码中硬编码阶段名称。
   */
  _parseStagesFromIndexMd(modAbs, fallbackStage) {
    const stageMap = new Map(); // "01" -> "第一阶段：..."
    if (!fs.existsSync(modAbs)) return stageMap;

    const indexFile = fs
      .readdirSync(modAbs)
      .find(f => f.endsWith('.md') && (f.startsWith('00') || f.toLowerCase() === 'index.md'));
    if (!indexFile) return stageMap;

    const content = fs.readFileSync(path.join(modAbs, indexFile), 'utf-8');
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
          const chCode = mLink[1];
          stageMap.set(chCode, currentHeading);
        }
      }
    }
    return stageMap;
  }

  /**
   * 发现所有知识库。
   * 支持两种组织方式：
   * 1) 顶层目录含 `kb.json` 或独立学科目录；
   * 2) 按学科前缀/配置自动归组。
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
        id: meta.id || dirName.toLowerCase().replace(/[^a-z0-9_-]/g, '-'),
        title: meta.title || dirName,
        subtitle: meta.subtitle || `${dirName} 知识库`,
        icon: meta.icon || '📗',
        badge: meta.badge || '扩展知识库',
        modules: meta.modules || [dirName]
      });
    }

    return result;
  }

  getKbConfig(kbId) {
    const kbs = this.listKnowledgeBases();
    return kbs.find(k => k.id === kbId) || null;
  }

  /**
   * 扫描指定知识库下的所有模块、文档树、双链索引与练习集文件（支持任意模块下的 `强化题目/`）
   */
  scanKb(kbId) {
    const kb = this.getKbConfig(kbId);
    if (!kb) return null;

    const modules = [];
    const stemMap = new Map(); // stem -> relativePath
    const orderedDocs = [];
    const exerciseFiles = new Map(); // exerciseKey -> { absPath, stage, moduleName, moduleIdx }

    for (let modIdx = 0; modIdx < kb.modules.length; modIdx++) {
      const modName = kb.modules[modIdx];
      const modAbs = path.join(this.kbRoot, modName);
      if (!fs.existsSync(modAbs)) continue;

      const shortModName = modName.replace(/^\d+\./, '');
      const stageMap = this._parseStagesFromIndexMd(modAbs, shortModName);

      // 通用扫描任何模块下的 `强化题目` 目录
      const exDir = path.join(modAbs, '强化题目');
      const modExerciseCodes = new Set();
      if (fs.existsSync(exDir)) {
        for (const f of fs.readdirSync(exDir).sort()) {
          if (!f.endsWith('.md') || f.startsWith('00')) continue;
          const m = f.match(/^(\d{2})·(.+)\.md$/);
          if (m) {
            const rawCode = m[1];
            // 第一个模块保持 `01`~`31` 编码以兼容已有进度，其余模块带模块前缀如 `m2-01`
            const exKey = modIdx === 0 ? rawCode : `m${modIdx + 1}-${rawCode}`;
            modExerciseCodes.add(rawCode);
            exerciseFiles.set(exKey, {
              absPath: path.join(exDir, f),
              stage: stageMap.get(rawCode) || shortModName,
              moduleName: modName,
              moduleIdx: modIdx,
              rawCode
            });
          }
        }
      }

      const modNode = this._scanModuleDir(
        modAbs,
        modName,
        modIdx,
        modExerciseCodes,
        stemMap,
        orderedDocs
      );
      modules.push(modNode);
    }

    return { kb, modules, stemMap, orderedDocs, exerciseFiles };
  }

  _scanModuleDir(dirAbs, relPrefix, modIdx, modExerciseCodes, stemMap, orderedDocs) {
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
        const docItem = this._buildDocItem(entry.name, relPath, modIdx, modExerciseCodes);
        rootDocs.push(docItem);
        if (!relPath.includes('/强化题目/')) {
          orderedDocs.push(docItem);
        }
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
        const subDocs = this._collectMarkdownFiles(
          fullPath,
          relPath,
          modIdx,
          modExerciseCodes,
          stemMap,
          orderedDocs
        );
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
      hasExercises: modExerciseCodes.size > 0,
      rootDocs,
      groups
    };
  }

  _collectMarkdownFiles(dirAbs, relPrefix, modIdx, modExerciseCodes, stemMap, orderedDocs) {
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
        const item = this._buildDocItem(entry.name, relPath, modIdx, modExerciseCodes);
        docs.push(item);
        if (!relPath.includes('/强化题目/')) {
          orderedDocs.push(item);
        }
      }
    }
    return docs;
  }

  _buildDocItem(filename, relPath, modIdx, modExerciseCodes) {
    const stem = filename.replace(/\.md$/, '');
    const mChap = stem.match(/^(\d{2})·(.+)$/);
    const rawCode = mChap ? mChap[1] : null;
    const displayTitle = mChap ? `${mChap[1]} · ${mChap[2]}` : stem;

    let exerciseCode = null;
    if (rawCode && rawCode !== '00' && modExerciseCodes?.has(rawCode) && relPath.includes('/章节/')) {
      exerciseCode = modIdx === 0 ? rawCode : `m${modIdx + 1}-${rawCode}`;
    }

    return {
      name: filename,
      stem,
      code: rawCode,
      title: displayTitle,
      path: relPath,
      moduleIdx: modIdx,
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
      idx >= 0 ? scan.orderedDocs[idx] : this._buildDocItem(path.basename(abs), toPosix(targetRel), 0, new Set());
    const prevDoc = idx > 0 ? scan.orderedDocs[idx - 1] : null;
    const nextDoc = idx >= 0 && idx + 1 < scan.orderedDocs.length ? scan.orderedDocs[idx + 1] : null;

    return {
      ...currentItem,
      content,
      prevDoc,
      nextDoc
    };
  }

  _normalizeExerciseKey(scan, chapterCode) {
    const raw = String(chapterCode).trim();
    if (scan.exerciseFiles.has(raw)) return raw;
    const padded = raw.padStart(2, '0');
    if (scan.exerciseFiles.has(padded)) return padded;
    return null;
  }

  getExerciseChapter(kbId, chapterCode) {
    const scan = this.scanKb(kbId);
    if (!scan) return null;
    const key = this._normalizeExerciseKey(scan, chapterCode);
    if (!key) return null;
    const info = scan.exerciseFiles.get(key);
    if (!info || !fs.existsSync(info.absPath)) return null;
    const raw = fs.readFileSync(info.absPath, 'utf-8');
    const parsed = parseExerciseMarkdown(raw, path.basename(info.absPath), info.stage);
    return {
      ...parsed,
      code: key,
      rawCode: info.rawCode,
      moduleName: info.moduleName,
      moduleIdx: info.moduleIdx
    };
  }

  getAllExercises(kbId) {
    const scan = this.scanKb(kbId);
    if (!scan) return [];
    const list = [];
    for (const [key, info] of scan.exerciseFiles.entries()) {
      const raw = fs.readFileSync(info.absPath, 'utf-8');
      const parsed = parseExerciseMarkdown(raw, path.basename(info.absPath), info.stage);
      list.push({
        ...parsed,
        code: key,
        rawCode: info.rawCode,
        moduleName: info.moduleName,
        moduleIdx: info.moduleIdx
      });
    }
    return list.sort((a, b) => a.moduleIdx - b.moduleIdx || a.num - b.num);
  }
}
