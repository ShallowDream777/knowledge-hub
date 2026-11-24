function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function mdInlineToHtml(text) {
  let s = escapeHtml(String(text).trim());
  // Obsidian wiki links [[target|label]] or [[target]]
  s = s.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '<span class="ref-chip" data-wikilink="$1">$2</span>');
  s = s.replace(/\[\[([^\]]+)\]\]/g, '<span class="ref-chip" data-wikilink="$1">$1</span>');
  // Inline code `...`
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Bold **...**
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // Blank slot ___
  s = s.replace(/_{3,}/g, '<span class="blank-slot">_____</span>');
  return s;
}

function cleanSingleParagraphAnswer(raw) {
  let s = raw.trim();
  s = s.replace(/^<p>\s*<strong>[A-Za-z]+\d+<\/strong>\s*[　\s]*/, '');
  s = s.replace(/<\/p>\s*$/, '');
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  return s.trim();
}

/**
 * 从 <details> 块中通用提取所有题号的答案（支持单行 `<p><strong>A01</strong>...</p>` 与多段 `<p><strong>Q01　答案</strong></p><p>...</p>`）
 */
function extractAnswersMap(text) {
  const answers = {};

  // 模式 1：多段式 <p><strong>Q01　答案</strong></p> 后面紧跟若干 <p>...</p>
  const multiRegex =
    /<p><strong>([A-Za-z]+\d+)[　\s]*答案<\/strong><\/p>([\s\S]*?)(?=<p><strong>[A-Za-z]+\d+[　\s]*答案<\/strong><\/p>|<\/details>|$)/g;
  let mm;
  while ((mm = multiRegex.exec(text)) !== null) {
    const qid = mm[1].trim();
    const body = mm[2]
      .trim()
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    answers[qid] = body;
  }

  // 模式 2：单段式 <p><strong>A01</strong>　参考答案...</p>
  const singleRegex = /(<p><strong>([A-Za-z]+\d+)<\/strong>[\s\S]*?<\/p>)/g;
  let sm;
  while ((sm = singleRegex.exec(text)) !== null) {
    const qid = sm[2].trim();
    if (!answers[qid]) {
      answers[qid] = cleanSingleParagraphAnswer(sm[1]);
    }
  }

  return answers;
}

/**
 * 通用 Markdown 练习题解析器（无任何硬编码阶段名或固定题组标题）
 * @param {string} text - 练习题 Markdown 原文
 * @param {string} filename - 文件名（如 `01·强化练习·文字、句子和必备术语.md` 或 `01·考强练习·*.md`）
 * @param {string} [stageName] - 由上层目录索引文件（如 `00·*.md`）动态解析传入的阶段名
 */
export function parseExerciseMarkdown(text, filename, stageName = '') {
  // 通用提取章节编号与标题：匹配 `01·强化练习·标题.md`、`01·考强练习·标题.md`、`01·标题.md` 等任意格式
  const mFile = filename.match(/^(\d+)[\s·._-]*(?:[^·._-]*练习[\s·._-]*)?(.+)\.md$/);
  const num = mFile ? Number(mFile[1]) : 0;
  const code = mFile ? mFile[1].padStart(2, '0') : '00';
  let title = mFile ? mFile[2].trim() : filename.replace(/\.md$/, '');

  // 若正文有一级标题 `# ...`，优先从一级标题提取可读名称
  const mH1 = text.match(/^#\s+(.+)$/m);
  if (!mFile && mH1) {
    title = mH1[1].trim();
  }

  // 提取说明/范围边界（兼容 `**范围边界：**...` 或开头说明段落）
  const mScope = text.match(/\*\*范围边界：\*\*(.+)/);
  let scope = mScope ? mScope[1].trim() : '';
  if (!scope) {
    const mIntro = text.match(/^本卷共.+$/m);
    if (mIntro) scope = mIntro[0].trim();
  }

  // 动态提取满分与建议达标分（若该卷未设统一通关分，则 hasPassScore = false）
  const mPass = text.match(/满分(\d+)分[，、]?建议至少(\d+)分/);
  const cFull = mPass ? Number(mPass[1]) : 0;
  const cPass = mPass ? Number(mPass[2]) : 0;

  // 动态提取任意包含三列及以上的“范围/易错点”Markdown 表格（若有）
  const coverage = [];
  const mCov = text.match(/## [^\n]*(?:范围|易错点)[^\n]*\s+([\s\S]+?)(?=\n## )/);
  if (mCov) {
    for (const rawLine of mCov[1].split(/\r?\n/)) {
      const line = rawLine.trim();
      if (line.startsWith('|') && !/^\|\s*---/.test(line) && !line.includes('核心情境')) {
        const cols = line
          .replace(/^\|/, '')
          .replace(/\|$/, '')
          .split('|')
          .map(c => c.trim());
        if (cols.length >= 3 && cols[0]) {
          coverage.push({ scene: cols[0], point: cols[1], ids: cols[2] });
        }
      }
    }
  }

  const answers = extractAnswersMap(text);

  // 按所有二级标题 `## ...` 切分文档，自动发现包含题目的题组（无需硬编码 A/B/C/D 标题）
  const headingMatches = [...text.matchAll(/^##\s+(.+)$/gm)];
  const questions = [];
  const presentGroups = [];

  for (let i = 0; i < headingMatches.length; i++) {
    const rawHeading = headingMatches[i][1].trim();
    const start = headingMatches[i].index + headingMatches[i][0].length;
    const end = i + 1 < headingMatches.length ? headingMatches[i + 1].index : text.length;
    const secBody = text.slice(start, end).replace(/<details>[\s\S]*?<\/details>/g, '');

    // 在该小节内查找所有题目块：支持 `**A01｜【必做】主题**　题干` 或 `**Q01**　题干`（含下方多行选项）
    const qMatches = [...secBody.matchAll(/^\*\*([A-Za-z]+\d+)(?:｜([^*\n]+))?\*\*[　\s]*(.+)$/gm)];
    if (qMatches.length === 0) continue;

    // 自动推导该题组的 key 与 label
    const mLetter = rawHeading.match(/^([A-Za-z])\s+(.+)$/);
    const isAssessment = rawHeading.includes('独立验收');
    const gKey = mLetter ? mLetter[1].toUpperCase() : (isAssessment ? 'C' : `G${presentGroups.length + 1}`);
    const gLabel = rawHeading;

    // 提取本节第一道题之前的阅读材料或题组导语（如阅读理解短文）
    const introRaw = secBody.slice(0, qMatches[0].index).trim();
    const introHtml = introRaw
      ? introRaw
          .split(/\n{2,}/)
          .map(p => `<p>${mdInlineToHtml(p.replace(/\n/g, ' '))}</p>`)
          .join('')
      : '';

    const groupQs = [];
    for (let qi = 0; qi < qMatches.length; qi++) {
      const qm = qMatches[qi];
      const qid = qm[1].trim();
      const meta = (qm[2] || '').trim();
      const firstLinePrompt = qm[3].trim();

      // 检查当前题与下一题之间是否有多行附加内容（如 `- A. ...` 选择题选项）
      const qStartEnd = qm.index + qm[0].length;
      const qNextStart = qi + 1 < qMatches.length ? qMatches[qi + 1].index : secBody.length;
      const extraLines = secBody
        .slice(qStartEnd, qNextStart)
        .split(/\r?\n/)
        .map(l => l.trim())
        .filter(Boolean);

      let promptHtml = mdInlineToHtml(firstLinePrompt);
      if (extraLines.length > 0) {
        const optsHtml = extraLines
          .map(l => `<div class="q-option-line">${mdInlineToHtml(l)}</div>`)
          .join('');
        promptHtml += `<div class="q-options-block">${optsHtml}</div>`;
      }

      const mTag = meta.match(/【([^】]+)】/);
      const tag = mTag ? mTag[1] : (isAssessment ? '验收必做' : '必做');
      const topic = meta.replace(/【[^】]+】/, '').trim() || (isAssessment ? '独立验收' : gLabel);

      groupQs.push({
        id: qid,
        group: gKey,
        groupLabel: gLabel,
        tag,
        required: tag !== '选做',
        topic,
        introHtml: qi === 0 ? introHtml : '',
        prompt: promptHtml,
        promptRaw: firstLinePrompt,
        answer: answers[qid] || '（暂无解析）'
      });
    }

    presentGroups.push({
      key: gKey,
      label: gLabel,
      count: groupQs.length,
      hasIntro: Boolean(introHtml)
    });
    questions.push(...groupQs);
  }

  return {
    num,
    code,
    title,
    stage: stageName || '核心训练',
    scope,
    cFull,
    cPass,
    coverage,
    groups: presentGroups,
    questions
  };
}
