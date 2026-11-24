const STAGES = [
  ['第一阶段：先把词与句子认清', 1, 8],
  ['第二阶段：句子骨架与动词时间', 9, 18],
  ['第三阶段：从简单句走向复杂句', 19, 24],
  ['第四阶段：整合与进阶', 25, 31]
];

export function stageForChapter(num) {
  for (const [name, lo, hi] of STAGES) {
    if (num >= lo && num <= hi) return name;
  }
  return '综合强化';
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function mdInlineToHtml(text) {
  let s = escapeHtml(text.trim());
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

function cleanAnswerHtml(raw) {
  let s = raw.trim();
  s = s.replace(/^<p>\s*<strong>[ABCD]\d+<\/strong>\s*[　\s]*/, '');
  s = s.replace(/<\/p>\s*$/, '');
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  return s.trim();
}

export function parseExerciseMarkdown(text, filename) {
  const mNum = filename.match(/^(\d{2})·强化练习·(.+)\.md$/);
  const num = mNum ? Number(mNum[1]) : 0;
  const code = mNum ? mNum[1] : '00';
  const title = mNum ? mNum[2] : filename.replace(/\.md$/, '');

  const mScope = text.match(/\*\*范围边界：\*\*(.+)/);
  const scope = mScope ? mScope[1].trim() : '';

  const mPass = text.match(/满分(\d+)分[，、]?建议至少(\d+)分/);
  const cFull = mPass ? Number(mPass[1]) : 24;
  const cPass = mPass ? Number(mPass[2]) : 20;

  const coverage = [];
  const mCov = text.match(/## 练习范围与易错点\s+([\s\S]+?)(?=\n## )/);
  if (mCov) {
    for (const rawLine of mCov[1].split(/\r?\n/)) {
      const line = rawLine.trim();
      if (line.startsWith('|') && !/^\|\s*---/.test(line) && !line.includes('核心情境')) {
        const cols = line
          .replace(/^\|/, '')
          .replace(/\|$/, '')
          .split('|')
          .map(c => c.trim());
        if (cols.length >= 3) {
          coverage.push({ scene: cols[0], point: cols[1], ids: cols[2] });
        }
      }
    }
  }

  const answers = {};
  const ansRegex = /(<p><strong>([ABCD]\d+)<\/strong>[\s\S]*?<\/p>)/g;
  let am;
  while ((am = ansRegex.exec(text)) !== null) {
    answers[am[2]] = cleanAnswerHtml(am[1]);
  }

  const sectionDefs = [
    ['A', 'A 分项强化', /^## A 分项强化/],
    ['B', 'B 串联应用', /^## B 已学知识综合练习/],
    ['D', 'D 专项补练', /^## D 专项补练/],
    ['C', 'C 独立验收', /^## C 独立验收/]
  ];

  const headingMatches = [...text.matchAll(/^## .+$/gm)];
  const sectionsText = {};
  for (let i = 0; i < headingMatches.length; i++) {
    const hLine = headingMatches[i][0].trim();
    const start = headingMatches[i].index + headingMatches[i][0].length;
    const end = i + 1 < headingMatches.length ? headingMatches[i + 1].index : text.length;
    sectionsText[hLine] = text.slice(start, end);
  }

  const questions = [];
  const presentGroups = [];

  for (const [gKey, gLabel, hPat] of sectionDefs) {
    const matchedHeading = Object.keys(sectionsText).find(h => hPat.test(h));
    if (!matchedHeading) continue;
    const secBody = sectionsText[matchedHeading].replace(/<details>[\s\S]*?<\/details>/g, '');
    const groupQs = [];
    const qRegex = /^\*\*([ABCD]\d+)｜([^*\n]+)\*\*[　\s]*(.+)$/gm;
    let qm;
    while ((qm = qRegex.exec(secBody)) !== null) {
      const qid = qm[1].trim();
      const meta = qm[2].trim();
      const promptRaw = qm[3].trim();
      const mTag = meta.match(/【([^】]+)】/);
      const tag = mTag ? mTag[1] : '必做';
      const topic = meta.replace(/【[^】]+】/, '').trim();

      groupQs.push({
        id: qid,
        group: gKey,
        tag,
        required: tag !== '选做',
        topic,
        prompt: mdInlineToHtml(promptRaw),
        promptRaw,
        answer: answers[qid] || '（暂无解析）'
      });
    }
    if (groupQs.length > 0) {
      presentGroups.push({ key: gKey, label: gLabel, count: groupQs.length });
      questions.push(...groupQs);
    }
  }

  return {
    num,
    code,
    title,
    stage: stageForChapter(num),
    scope,
    cFull,
    cPass,
    coverage,
    groups: presentGroups,
    questions
  };
}
