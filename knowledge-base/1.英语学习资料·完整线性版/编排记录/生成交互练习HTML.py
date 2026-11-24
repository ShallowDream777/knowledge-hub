#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 `强化题目/` 下 01–31 章的 Markdown 练习题解析并打包为单文件离线交互式刷题网页：
输出路径：1.英语学习资料·完整线性版/强化题目/交互刷题.html

设计原则：
- MD 文件仍是唯一数据源（Single Source of Truth）。
- 未来修改任意章节练习题 MD 后，重新运行本脚本即可 1 秒同步更新交互网页。
- 生成的 HTML 零外部依赖、支持 file:// 直接双击离线打开、自动保存进度与错题本到 localStorage。
"""

import glob
import html
import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EX_DIR = BASE_DIR / "强化题目"
OUT_HTML = EX_DIR / "交互刷题.html"

STAGES = [
    ("第一阶段：先把词与句子认清", 1, 8),
    ("第二阶段：句子骨架与动词时间", 9, 18),
    ("第三阶段：从简单句走向复杂句", 19, 24),
    ("第四阶段：整合与进阶", 25, 31),
]


def stage_for_chapter(num: int) -> str:
    for name, lo, hi in STAGES:
        if lo <= num <= hi:
            return name
    return "其他"


def md_inline_to_html(text: str) -> str:
    """将题干或解析中的轻度 Markdown 语法转为干净的 HTML。"""
    s = html.escape(text.strip())
    # Obsidian wiki links [[target|label]] or [[target]]
    s = re.sub(
        r"\[\[([^\]|]+)\|([^\]]+)\]\]",
        r'<span class="ref-chip">\2</span>',
        s,
    )
    s = re.sub(
        r"\[\[([^\]]+)\]\]",
        r'<span class="ref-chip">\1</span>',
        s,
    )
    # Inline code `...`
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    # Bold **...**
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # Highlight blanks ___
    s = re.sub(r"_{3,}", r'<span class="blank-slot">_____</span>', s)
    return s


def clean_answer_html(raw: str) -> str:
    """清理 <p><strong>A01</strong>　...</p> 中的题号前缀，保留干净解析。"""
    s = raw.strip()
    s = re.sub(r"^<p>\s*<strong>[ABCD]\d+</strong>\s*[　\s]*", "", s)
    s = re.sub(r"</p>\s*$", "", s)
    # Convert any stray markdown backticks/bold inside answer
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s.strip()


def parse_exercise_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fname = path.name
    m_num = re.match(r"^(\d{2})·强化练习·(.+)\.md$", fname)
    if not m_num:
        raise ValueError(f"Unexpected filename: {fname}")
    num = int(m_num.group(1))
    title = m_num.group(2)

    # Extract scope boundary
    m_scope = re.search(r"\*\*范围边界：\*\*(.+)", text)
    scope = m_scope.group(1).strip() if m_scope else ""

    # Extract target C score hint
    m_pass = re.search(r"满分(\d+)分[，、]?建议至少(\d+)分", text)
    c_full = int(m_pass.group(1)) if m_pass else 24
    c_pass = int(m_pass.group(2)) if m_pass else 20

    # Extract coverage table (练习范围与易错点)
    coverage = []
    m_cov = re.search(r"## 练习范围与易错点\s+([\s\S]+?)(?=\n## )", text)
    if m_cov:
        for line in m_cov.group(1).splitlines():
            line = line.strip()
            if line.startswith("|") and not re.match(r"^\|\s*---", line) and "核心情境" not in line:
                cols = [c.strip() for c in line.strip("|").split("|")]
                if len(cols) >= 3:
                    coverage.append({"scene": cols[0], "point": cols[1], "ids": cols[2]})

    # Extract answers map from all <p><strong>ID</strong>...</p>
    answers = {}
    for m in re.finditer(r"(<p><strong>([ABCD]\d+)</strong>[\s\S]*?</p>)", text):
        qid = m.group(2)
        answers[qid] = clean_answer_html(m.group(1))

    # Extract questions by section (A, B, D, C)
    section_defs = [
        ("A", "A 分项强化", r"## A 分项强化"),
        ("B", "B 串联应用", r"## B 已学知识综合练习"),
        ("D", "D 专项补练", r"## D 专项补练"),
        ("C", "C 独立验收", r"## C 独立验收"),
    ]

    # Split document by ## headings
    heading_matches = list(re.finditer(r"^## .+$", text, re.M))
    sections_text = {}
    for i, hm in enumerate(heading_matches):
        h_line = hm.group(0).strip()
        start = hm.end()
        end = heading_matches[i + 1].start() if i + 1 < len(heading_matches) else len(text)
        sections_text[h_line] = text[start:end]

    questions = []
    present_groups = []
    for g_key, g_label, h_pat in section_defs:
        matched_heading = next((h for h in sections_text if re.match(h_pat, h)), None)
        if not matched_heading:
            continue
        sec_body = sections_text[matched_heading]
        # Remove <details> blocks before extracting questions
        sec_no_details = re.sub(r"<details>[\s\S]*?</details>", "", sec_body)
        group_qs = []
        for qm in re.finditer(r"^\*\*([ABCD]\d+)｜([^*\n]+)\*\*[　\s]*(.+)$", sec_no_details, re.M):
            qid = qm.group(1).strip()
            meta = qm.group(2).strip()
            prompt_raw = qm.group(3).strip()

            m_tag = re.search(r"【([^】]+)】", meta)
            tag = m_tag.group(1) if m_tag else "必做"
            topic = re.sub(r"【[^】]+】", "", meta).strip()

            group_qs.append(
                {
                    "id": qid,
                    "group": g_key,
                    "tag": tag,
                    "required": tag != "选做",
                    "topic": topic,
                    "prompt": md_inline_to_html(prompt_raw),
                    "answer": answers.get(qid, "（暂无解析）"),
                }
            )
        if group_qs:
            present_groups.append({"key": g_key, "label": g_label, "count": len(group_qs)})
            questions.extend(group_qs)

    return {
        "num": num,
        "code": f"{num:02d}",
        "title": title,
        "stage": stage_for_chapter(num),
        "scope": scope,
        "cFull": c_full,
        "cPass": c_pass,
        "coverage": coverage,
        "groups": present_groups,
        "questions": questions,
    }


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>英语学习资料·完整线性版｜交互刷题中心</title>
<style>
  :root {
    --bg: #f6f5f0;
    --surface: #ffffff;
    --surface-soft: #faf9f5;
    --border: #e6e3da;
    --border-strong: #d4cfc2;
    --text: #22242a;
    --text-muted: #666a73;
    --accent: #2c6bed;
    --accent-soft: #eaf1ff;
    --ok: #1d8a4e;
    --ok-soft: #e8f7ee;
    --warn: #b86e00;
    --warn-soft: #fff5e0;
    --bad: #c93434;
    --bad-soft: #fdecec;
    --code-bg: #f0eee7;
    --shadow: 0 2px 10px rgba(25, 28, 36, 0.05);
    --radius: 12px;
  }
  [data-theme="dark"] {
    --bg: #14171d;
    --surface: #1d212a;
    --surface-soft: #232834;
    --border: #2e3442;
    --border-strong: #3f4759;
    --text: #e7eaf0;
    --text-muted: #9aa2b2;
    --accent: #6aa0ff;
    --accent-soft: #1e2c47;
    --ok: #4cd084;
    --ok-soft: #173324;
    --warn: #f2b44c;
    --warn-soft: #362a16;
    --bad: #f26d6d;
    --bad-soft: #3a1d21;
    --code-bg: #29303e;
    --shadow: 0 2px 12px rgba(0, 0, 0, 0.28);
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }
  .app {
    display: grid;
    grid-template-columns: 290px 1fr;
    min-height: 100vh;
  }
  /* Sidebar */
  .sidebar {
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow: hidden;
  }
  .sidebar-header {
    padding: 18px 16px 12px;
    border-bottom: 1px solid var(--border);
  }
  .brand {
    font-size: 16px; font-weight: 700; margin: 0 0 4px;
    display: flex; align-items: center; justify-content: space-between;
  }
  .brand-sub { font-size: 12px; color: var(--text-muted); margin: 0 0 10px; }
  .search-input {
    width: 100%; padding: 8px 10px; border-radius: 8px;
    border: 1px solid var(--border); background: var(--surface-soft);
    color: var(--text); font-size: 13px; outline: none;
  }
  .search-input:focus { border-color: var(--accent); }
  .sidebar-tools {
    display: flex; gap: 6px; padding: 10px 16px; border-bottom: 1px solid var(--border);
  }
  .tool-btn {
    flex: 1; padding: 7px 8px; font-size: 12px; font-weight: 600;
    border-radius: 8px; border: 1px solid var(--border);
    background: var(--surface-soft); color: var(--text); cursor: pointer;
    transition: all .15s;
  }
  .tool-btn:hover { border-color: var(--accent); color: var(--accent); }
  .tool-btn.active { background: var(--bad-soft); border-color: var(--bad); color: var(--bad); }
  .chapter-list {
    flex: 1; overflow-y: auto; padding: 8px 10px 24px;
  }
  .stage-label {
    font-size: 11px; font-weight: 700; color: var(--text-muted);
    padding: 12px 8px 4px; letter-spacing: .3px;
  }
  .ch-item {
    display: flex; flex-direction: column; gap: 4px;
    padding: 8px 10px; margin-bottom: 3px; border-radius: 9px;
    cursor: pointer; border: 1px solid transparent;
    transition: background .15s, border-color .15s;
  }
  .ch-item:hover { background: var(--surface-soft); }
  .ch-item.active { background: var(--accent-soft); border-color: var(--accent); }
  .ch-item-top { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
  .ch-code {
    font-size: 11px; font-weight: 700; color: var(--accent);
    background: var(--accent-soft); padding: 1px 6px; border-radius: 5px;
    flex-shrink: 0;
  }
  .ch-item.active .ch-code { background: var(--accent); color: #fff; }
  .ch-name {
    font-size: 13px; font-weight: 500; flex: 1;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .ch-stat { font-size: 11px; color: var(--text-muted); flex-shrink: 0; }
  .mini-bar { height: 3px; background: var(--border); border-radius: 99px; overflow: hidden; }
  .mini-bar-fill { height: 100%; background: var(--ok); transition: width .25s; }

  /* Main */
  .main {
    padding: 24px 32px 64px;
    max-width: 960px;
    width: 100%;
    margin: 0 auto;
  }
  .mobile-bar {
    display: none; align-items: center; justify-content: space-between;
    padding: 12px 16px; background: var(--surface); border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 20;
  }
  .header-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    box-shadow: var(--shadow);
    margin-bottom: 16px;
  }
  .header-top {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  }
  .ch-title { font-size: 22px; font-weight: 700; margin: 0 0 6px; }
  .ch-scope { font-size: 13.5px; color: var(--text-muted); margin: 0; }
  .summary-pills {
    display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px;
  }
  .stat-pill {
    font-size: 12.5px; padding: 4px 10px; border-radius: 99px;
    background: var(--surface-soft); border: 1px solid var(--border); color: var(--text);
  }
  .stat-pill.pass { background: var(--ok-soft); border-color: var(--ok); color: var(--ok); font-weight: 600; }
  .stat-pill.warn { background: var(--warn-soft); border-color: var(--warn); color: var(--warn); font-weight: 600; }

  details.drawer {
    margin-top: 14px; border-top: 1px dashed var(--border); padding-top: 10px;
  }
  details.drawer summary {
    cursor: pointer; font-size: 13px; font-weight: 600; color: var(--accent); user-select: none;
  }
  .cov-table {
    width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px;
  }
  .cov-table th, .cov-table td {
    text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--border);
  }
  .cov-table th { color: var(--text-muted); font-weight: 600; background: var(--surface-soft); }

  /* Controls */
  .controls {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 16px;
    margin-bottom: 16px;
    display: flex; flex-direction: column; gap: 10px;
    position: sticky; top: 10px; z-index: 10;
    box-shadow: var(--shadow);
  }
  .ctrl-row {
    display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap;
  }
  .pill-group { display: flex; gap: 6px; flex-wrap: wrap; }
  .pill {
    padding: 6px 12px; border-radius: 99px; font-size: 13px; font-weight: 500;
    border: 1px solid var(--border); background: var(--surface-soft); color: var(--text);
    cursor: pointer; transition: all .15s;
  }
  .pill:hover { border-color: var(--accent); }
  .pill.active { background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 600; }
  .ghost-btn {
    padding: 5px 10px; border-radius: 8px; font-size: 12.5px;
    border: 1px solid var(--border); background: transparent; color: var(--text-muted);
    cursor: pointer; transition: all .15s;
  }
  .ghost-btn:hover { color: var(--text); border-color: var(--border-strong); background: var(--surface-soft); }

  /* Question Cards */
  .q-list { display: flex; flex-direction: column; gap: 12px; }
  .q-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--border-strong);
    border-radius: var(--radius);
    padding: 16px 20px;
    box-shadow: var(--shadow);
    transition: border-color .15s;
  }
  .q-card.st-ok { border-left-color: var(--ok); }
  .q-card.st-warn { border-left-color: var(--warn); }
  .q-card.st-bad { border-left-color: var(--bad); }

  .q-meta {
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px;
  }
  .q-id { font-weight: 700; font-size: 14px; color: var(--accent); }
  .q-tag {
    font-size: 11.5px; font-weight: 600; padding: 2px 8px; border-radius: 6px;
  }
  .q-tag.req { background: var(--accent-soft); color: var(--accent); }
  .q-tag.read { background: var(--warn-soft); color: var(--warn); }
  .q-tag.opt { background: var(--surface-soft); color: var(--text-muted); border: 1px solid var(--border); }
  .q-topic { font-size: 12.5px; color: var(--text-muted); }
  .q-chapter-badge {
    font-size: 11.5px; padding: 2px 8px; border-radius: 6px;
    background: var(--code-bg); color: var(--text-muted); margin-left: auto;
  }

  .q-prompt { font-size: 15.5px; margin: 0 0 12px; line-height: 1.75; }
  .q-prompt code, .ans-body code {
    background: var(--code-bg); padding: 2px 6px; border-radius: 5px;
    font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 0.92em;
  }
  .blank-slot {
    display: inline-block; padding: 0 6px; border-bottom: 2px solid var(--accent);
    color: var(--accent); font-weight: 600; margin: 0 2px;
  }
  .ref-chip {
    font-size: 12px; padding: 1px 7px; border-radius: 5px;
    background: var(--surface-soft); border: 1px solid var(--border); color: var(--text-muted);
  }

  .q-input-row { margin-bottom: 12px; }
  .q-input {
    width: 100%; padding: 9px 12px; border-radius: 8px;
    border: 1px solid var(--border); background: var(--surface-soft);
    color: var(--text); font-size: 14px; outline: none;
    transition: border-color .15s, background .15s;
  }
  .q-input:focus { border-color: var(--accent); background: var(--surface); }

  .q-actions {
    display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap;
  }
  .ans-toggle {
    padding: 7px 14px; border-radius: 8px; font-size: 13px; font-weight: 600;
    border: 1px solid var(--accent); background: var(--accent-soft); color: var(--accent);
    cursor: pointer; transition: all .15s;
  }
  .ans-toggle:hover { background: var(--accent); color: #fff; }
  .ans-toggle.open { background: var(--surface-soft); border-color: var(--border-strong); color: var(--text-muted); }

  .grade-group { display: flex; gap: 6px; }
  .grade-btn {
    padding: 6px 10px; border-radius: 8px; font-size: 12.5px; font-weight: 500;
    border: 1px solid var(--border); background: var(--surface-soft); color: var(--text-muted);
    cursor: pointer; transition: all .15s;
  }
  .grade-btn:hover { border-color: var(--border-strong); color: var(--text); }
  .grade-btn.active-ok { background: var(--ok-soft); border-color: var(--ok); color: var(--ok); font-weight: 700; }
  .grade-btn.active-warn { background: var(--warn-soft); border-color: var(--warn); color: var(--warn); font-weight: 700; }
  .grade-btn.active-bad { background: var(--bad-soft); border-color: var(--bad); color: var(--bad); font-weight: 700; }

  .ans-box {
    display: none;
    margin-top: 12px;
    padding: 12px 14px;
    border-radius: 9px;
    background: var(--surface-soft);
    border: 1px solid var(--border);
  }
  .ans-box.show { display: block; animation: fadeIn .15s ease-out; }
  .ans-label { font-size: 11.5px; font-weight: 700; color: var(--ok); margin-bottom: 4px; letter-spacing: .3px; }
  .ans-body { font-size: 14.5px; line-height: 1.7; }

  .empty-state {
    text-align: center; padding: 48px 20px; color: var(--text-muted);
    background: var(--surface); border: 1px dashed var(--border-strong); border-radius: var(--radius);
  }

  .bottom-nav {
    display: flex; justify-content: space-between; margin-top: 24px; gap: 12px;
  }
  .nav-btn {
    padding: 10px 18px; border-radius: 10px; font-size: 14px; font-weight: 600;
    border: 1px solid var(--border); background: var(--surface); color: var(--text);
    cursor: pointer; transition: all .15s;
  }
  .nav-btn:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
  .nav-btn:disabled { opacity: .4; cursor: not-allowed; }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(-3px); } to { opacity: 1; transform: none; } }

  @media (max-width: 860px) {
    .app { grid-template-columns: 1fr; }
    .mobile-bar { display: flex; }
    .sidebar {
      position: fixed; left: -310px; top: 0; width: 290px; z-index: 40;
      transition: left .2s ease; box-shadow: 4px 0 24px rgba(0,0,0,.2);
    }
    .sidebar.open { left: 0; }
    .main { padding: 16px 14px 48px; }
    .controls { position: static; }
  }
</style>
</head>
<body>
<div class="mobile-bar">
  <button class="ghost-btn" id="menuBtn">☰ 章节目录</button>
  <strong style="font-size:14px;">英语交互刷题中心</strong>
  <button class="ghost-btn" id="themeBtnMobile">🌓</button>
</div>
<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <div class="brand">
        <span>📘 英语交互刷题中心</span>
        <button class="ghost-btn" id="themeBtn" title="切换深浅色">🌓</button>
      </div>
      <p class="brand-sub">31 章强化与验收 · 离线自动存进度</p>
      <input class="search-input" id="chSearch" type="text" placeholder="搜索章节号或关键词…" />
    </div>
    <div class="sidebar-tools">
      <button class="tool-btn" id="wrongBookBtn">📕 全局错题本 (<span id="wrongCount">0</span>)</button>
    </div>
    <div class="chapter-list" id="chapterList"></div>
  </aside>

  <main class="main">
    <div id="headerArea"></div>
    <div id="controlsArea"></div>
    <div class="q-list" id="questionList"></div>
    <div class="bottom-nav" id="bottomNav"></div>
  </main>
</div>

<script>
const DATA = __DATA_JSON__;

const STORAGE_KEY = "eng_linear_practice_v1";
const THEME_KEY = "eng_linear_theme_v1";

let state = loadState();
let viewMode = "chapter"; // "chapter" | "wrongbook"
let currentCh = 1;
let filterMode = "required"; // "required" | "all" | "todo" | "review"
let groupTab = "ALL"; // "ALL" | "A" | "B" | "D" | "C"
let openAnswers = new Set();

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  return { grades: {}, inputs: {} };
}
function saveState() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
}
function qKey(chCode, qid) { return `${chCode}:${qid}`; }

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === "dark") document.documentElement.setAttribute("data-theme", "dark");
}
function toggleTheme() {
  const cur = document.documentElement.getAttribute("data-theme");
  const next = cur === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem(THEME_KEY, next);
}

function getAllWrongItems() {
  const res = [];
  for (const ch of DATA) {
    for (const q of ch.questions) {
      const g = state.grades[qKey(ch.code, q.id)];
      if (g === "bad" || g === "warn") {
        res.push({ ch, q, grade: g });
      }
    }
  }
  return res;
}

function renderSidebar() {
  const list = document.getElementById("chapterList");
  const kw = document.getElementById("chSearch").value.trim().toLowerCase();
  const wrongItems = getAllWrongItems();
  document.getElementById("wrongCount").textContent = wrongItems.length;
  document.getElementById("wrongBookBtn").classList.toggle("active", viewMode === "wrongbook");

  let html = "";
  let lastStage = "";
  for (const ch of DATA) {
    if (kw && !ch.code.includes(kw) && !ch.title.toLowerCase().includes(kw)) continue;
    if (ch.stage !== lastStage) {
      html += `<div class="stage-label">${ch.stage}</div>`;
      lastStage = ch.stage;
    }
    const reqQs = ch.questions.filter(q => q.required);
    const doneOk = reqQs.filter(q => state.grades[qKey(ch.code, q.id)] === "ok").length;
    const pct = reqQs.length ? Math.round((doneOk / reqQs.length) * 100) : 0;
    const active = viewMode === "chapter" && currentCh === ch.num ? "active" : "";
    html += `
      <div class="ch-item ${active}" data-ch="${ch.num}">
        <div class="ch-item-top">
          <span class="ch-code">${ch.code}</span>
          <span class="ch-name" title="${ch.title}">${ch.title}</span>
          <span class="ch-stat">${doneOk}/${reqQs.length}</span>
        </div>
        <div class="mini-bar"><div class="mini-bar-fill" style="width:${pct}%"></div></div>
      </div>`;
  }
  list.innerHTML = html;
  list.querySelectorAll(".ch-item").forEach(el => {
    el.addEventListener("click", () => {
      currentCh = Number(el.dataset.ch);
      viewMode = "chapter";
      groupTab = "ALL";
      openAnswers.clear();
      location.hash = `ch=${String(currentCh).padStart(2, "0")}`;
      document.getElementById("sidebar").classList.remove("open");
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
}

function getFilteredQuestions(ch) {
  return ch.questions.filter(q => {
    if (groupTab !== "ALL" && q.group !== groupTab) return false;
    const g = state.grades[qKey(ch.code, q.id)];
    if (filterMode === "required" && !q.required) return false;
    if (filterMode === "todo" && g) return false;
    if (filterMode === "review" && g !== "bad" && g !== "warn") return false;
    return true;
  });
}

function renderCard(ch, q, showChapterBadge = false) {
  const key = qKey(ch.code, q.id);
  const grade = state.grades[key] || "";
  const savedInput = state.inputs[key] || "";
  const isOpen = openAnswers.has(key);
  const tagClass = q.tag === "选做" ? "opt" : (q.tag === "识读必做" ? "read" : "req");
  const cardState = grade ? `st-${grade}` : "";

  return `
    <article class="q-card ${cardState}" data-key="${key}">
      <div class="q-meta">
        <span class="q-id">${q.id}</span>
        <span class="q-tag ${tagClass}">${q.tag}</span>
        <span class="q-topic">${q.topic}</span>
        ${showChapterBadge ? `<span class="q-chapter-badge">第${ch.code}章 · ${ch.title}</span>` : ""}
      </div>
      <div class="q-prompt">${q.prompt}</div>
      <div class="q-input-row">
        <input class="q-input" type="text" data-key="${key}" value="${savedInput.replace(/"/g, "&quot;")}" placeholder="在此输入你的答案（按回车直接查看解析，也可直接心中作答）…" />
      </div>
      <div class="q-actions">
        <button class="ans-toggle ${isOpen ? "open" : ""}" data-toggle="${key}">
          ${isOpen ? "🙈 隐藏答案" : "👁 显示答案"}
        </button>
        <div class="grade-group">
          <button class="grade-btn ${grade === "ok" ? "active-ok" : ""}" data-grade="${key}" data-val="ok">✅ 会了</button>
          <button class="grade-btn ${grade === "warn" ? "active-warn" : ""}" data-grade="${key}" data-val="warn">⚠️ 不稳</button>
          <button class="grade-btn ${grade === "bad" ? "active-bad" : ""}" data-grade="${key}" data-val="bad">❌ 错了</button>
        </div>
      </div>
      <div class="ans-box ${isOpen ? "show" : ""}" id="ans-${key.replace(":", "-")}">
        <div class="ans-label">参考答案与解析</div>
        <div class="ans-body">${q.answer}</div>
      </div>
    </article>`;
}

function renderChapter() {
  const ch = DATA.find(c => c.num === currentCh) || DATA[0];
  const reqQs = ch.questions.filter(q => q.required);
  const doneReq = reqQs.filter(q => state.grades[qKey(ch.code, q.id)]).length;
  const okReq = reqQs.filter(q => state.grades[qKey(ch.code, q.id)] === "ok").length;
  const reviewCount = ch.questions.filter(q => {
    const g = state.grades[qKey(ch.code, q.id)];
    return g === "bad" || g === "warn";
  }).length;

  // C-group auto score (首轮必做 C 组：会了=2分，不稳=1分，错了=0分)
  const cReq = ch.questions.filter(q => q.group === "C" && q.required);
  let cScore = 0, cGraded = 0;
  for (const q of cReq) {
    const g = state.grades[qKey(ch.code, q.id)];
    if (g) {
      cGraded++;
      if (g === "ok") cScore += 2;
      else if (g === "warn") cScore += 1;
    }
  }
  const cMax = cReq.length * 2;
  const cPassed = cGraded === cReq.length && cScore >= ch.cPass;

  const covRows = ch.coverage.map(r => `<tr><td>${r.scene}</td><td>${r.point}</td><td>${r.ids}</td></tr>`).join("");

  document.getElementById("headerArea").innerHTML = `
    <section class="header-card">
      <div class="header-top">
        <div>
          <h1 class="ch-title">第 ${ch.code} 章　${ch.title}</h1>
          <p class="ch-scope">${ch.scope || "按首轮必做题完成练习与独立验收即可进入下一章。"}</p>
        </div>
      </div>
      <div class="summary-pills">
        <span class="stat-pill">首轮必做：${okReq} / ${reqQs.length} 会了（已自评 ${doneReq}）</span>
        <span class="stat-pill ${cPassed ? "pass" : (cGraded > 0 ? "warn" : "")}">
          C组独立验收：${cScore} / ${cMax} 分（建议 ≥ ${ch.cPass} 分${cPassed ? " · 已达标 🎉" : ""}）
        </span>
        <span class="stat-pill">本章错题/不稳：${reviewCount} 题</span>
      </div>
      ${ch.coverage.length ? `
      <details class="drawer">
        <summary>📋 展开本章练习范围与易错点（${ch.coverage.length} 个核心情境）</summary>
        <table class="cov-table">
          <thead><tr><th>核心情境</th><th>主要检查</th><th>关联题号</th></tr></thead>
          <tbody>${covRows}</tbody>
        </table>
      </details>` : ""}
    </section>`;

  const groupButtons = [
    `<button class="pill ${groupTab === "ALL" ? "active" : ""}" data-group="ALL">全部组 (${ch.questions.length})</button>`,
    ...ch.groups.map(g => `<button class="pill ${groupTab === g.key ? "active" : ""}" data-group="${g.key}">${g.label} (${g.count})</button>`)
  ].join("");

  document.getElementById("controlsArea").innerHTML = `
    <section class="controls">
      <div class="ctrl-row">
        <div class="pill-group">
          <button class="pill ${filterMode === "required" ? "active" : ""}" data-filter="required">⭐ 首轮必做</button>
          <button class="pill ${filterMode === "all" ? "active" : ""}" data-filter="all">全部题目</button>
          <button class="pill ${filterMode === "todo" ? "active" : ""}" data-filter="todo">未自评</button>
          <button class="pill ${filterMode === "review" ? "active" : ""}" data-filter="review">错题/不稳 (${reviewCount})</button>
        </div>
        <div class="pill-group">
          <button class="ghost-btn" id="expandAllBtn">全部展开答案</button>
          <button class="ghost-btn" id="collapseAllBtn">全部隐藏答案</button>
          <button class="ghost-btn" id="resetChBtn">重置本章</button>
        </div>
      </div>
      <div class="ctrl-row">
        <div class="pill-group">${groupButtons}</div>
      </div>
    </section>`;

  const filtered = getFilteredQuestions(ch);
  const qList = document.getElementById("questionList");
  if (!filtered.length) {
    qList.innerHTML = `<div class="empty-state">当前筛选条件下没有题目 🎉<br/><span style="font-size:13px;">可以切换“全部题目”或“全部组”查看其他题目。</span></div>`;
  } else {
    qList.innerHTML = filtered.map(q => renderCard(ch, q, false)).join("");
  }

  document.getElementById("bottomNav").innerHTML = `
    <button class="nav-btn" id="prevChBtn" ${ch.num <= 1 ? "disabled" : ""}>← 上一章</button>
    <button class="nav-btn" id="nextChBtn" ${ch.num >= DATA.length ? "disabled" : ""}>下一章 →</button>`;

  bindChapterControls(ch, filtered);
  bindCardEvents();
}

function renderWrongBook() {
  const items = getAllWrongItems();
  document.getElementById("headerArea").innerHTML = `
    <section class="header-card">
      <h1 class="ch-title">📕 全局错题与不稳题本</h1>
      <p class="ch-scope">集中复盘你在全书 31 章中标记为“❌ 错了”或“⚠️ 不稳”的题目；重新做对并点“✅ 会了”后会自动移出。</p>
      <div class="summary-pills">
        <span class="stat-pill warn">待修复题目：${items.length} 题</span>
      </div>
    </section>`;

  document.getElementById("controlsArea").innerHTML = `
    <section class="controls">
      <div class="ctrl-row">
        <span style="font-size:13px;color:var(--text-muted);">提示：每题独立点击“显示答案”核对，做稳后点“✅ 会了”。</span>
        <div class="pill-group">
          <button class="ghost-btn" id="expandAllBtn">全部展开答案</button>
          <button class="ghost-btn" id="collapseAllBtn">全部隐藏答案</button>
        </div>
      </div>
    </section>`;

  const qList = document.getElementById("questionList");
  if (!items.length) {
    qList.innerHTML = `<div class="empty-state">目前没有错题或不稳项，继续保持！ 🎉</div>`;
  } else {
    qList.innerHTML = items.map(it => renderCard(it.ch, it.q, true)).join("");
  }
  document.getElementById("bottomNav").innerHTML = "";

  document.getElementById("expandAllBtn")?.addEventListener("click", () => {
    items.forEach(it => openAnswers.add(qKey(it.ch.code, it.q.id)));
    render();
  });
  document.getElementById("collapseAllBtn")?.addEventListener("click", () => {
    openAnswers.clear();
    render();
  });
  bindCardEvents();
}

function bindChapterControls(ch, filtered) {
  document.querySelectorAll("[data-filter]").forEach(btn => {
    btn.addEventListener("click", () => {
      filterMode = btn.dataset.filter;
      render();
    });
  });
  document.querySelectorAll("[data-group]").forEach(btn => {
    btn.addEventListener("click", () => {
      groupTab = btn.dataset.group;
      render();
    });
  });
  document.getElementById("expandAllBtn")?.addEventListener("click", () => {
    filtered.forEach(q => openAnswers.add(qKey(ch.code, q.id)));
    render();
  });
  document.getElementById("collapseAllBtn")?.addEventListener("click", () => {
    filtered.forEach(q => openAnswers.delete(qKey(ch.code, q.id)));
    render();
  });
  document.getElementById("resetChBtn")?.addEventListener("click", () => {
    if (!confirm(`确定清空第 ${ch.code} 章的作答输入和自评记录吗？`)) return;
    for (const q of ch.questions) {
      const k = qKey(ch.code, q.id);
      delete state.grades[k];
      delete state.inputs[k];
      openAnswers.delete(k);
    }
    saveState();
    render();
  });
  document.getElementById("prevChBtn")?.addEventListener("click", () => {
    if (currentCh > 1) {
      currentCh--;
      groupTab = "ALL";
      openAnswers.clear();
      location.hash = `ch=${String(currentCh).padStart(2, "0")}`;
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });
  document.getElementById("nextChBtn")?.addEventListener("click", () => {
    if (currentCh < DATA.length) {
      currentCh++;
      groupTab = "ALL";
      openAnswers.clear();
      location.hash = `ch=${String(currentCh).padStart(2, "0")}`;
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });
}

function bindCardEvents() {
  document.querySelectorAll("[data-toggle]").forEach(btn => {
    btn.addEventListener("click", () => {
      const k = btn.dataset.toggle;
      if (openAnswers.has(k)) openAnswers.delete(k);
      else openAnswers.add(k);
      const box = document.getElementById(`ans-${k.replace(":", "-")}`);
      const nowOpen = openAnswers.has(k);
      box.classList.toggle("show", nowOpen);
      btn.classList.toggle("open", nowOpen);
      btn.textContent = nowOpen ? "🙈 隐藏答案" : "👁 显示答案";
    });
  });

  document.querySelectorAll("[data-grade]").forEach(btn => {
    btn.addEventListener("click", () => {
      const k = btn.dataset.grade;
      const val = btn.dataset.val;
      if (state.grades[k] === val) delete state.grades[k];
      else state.grades[k] = val;
      saveState();
      render();
    });
  });

  document.querySelectorAll(".q-input").forEach(inp => {
    inp.addEventListener("input", () => {
      state.inputs[inp.dataset.key] = inp.value;
      saveState();
    });
    inp.addEventListener("keydown", e => {
      if (e.key === "Enter") {
        const btn = document.querySelector(`[data-toggle="${inp.dataset.key}"]`);
        btn?.click();
      }
    });
  });
}

function render() {
  renderSidebar();
  if (viewMode === "wrongbook") renderWrongBook();
  else renderChapter();
}

function parseHash() {
  const m = location.hash.match(/ch=(\d+)/);
  if (m) {
    const n = Number(m[1]);
    if (n >= 1 && n <= DATA.length) {
      currentCh = n;
      viewMode = "chapter";
    }
  }
}

document.getElementById("themeBtn").addEventListener("click", toggleTheme);
document.getElementById("themeBtnMobile").addEventListener("click", toggleTheme);
document.getElementById("chSearch").addEventListener("input", renderSidebar);
document.getElementById("wrongBookBtn").addEventListener("click", () => {
  viewMode = viewMode === "wrongbook" ? "chapter" : "wrongbook";
  openAnswers.clear();
  document.getElementById("sidebar").classList.remove("open");
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
});
document.getElementById("menuBtn").addEventListener("click", () => {
  document.getElementById("sidebar").classList.toggle("open");
});
window.addEventListener("hashchange", () => {
  parseHash();
  render();
});

initTheme();
parseHash();
render();
</script>
</body>
</html>
"""


def main():
    files = sorted(EX_DIR.glob("[0-3][0-9]·强化练习*.md"))
    chapters = [parse_exercise_file(p) for p in files]
    total_q = sum(len(c["questions"]) for c in chapters)
    data_json = json.dumps(chapters, ensure_ascii=False)
    # Prevent </script> injection inside JSON
    data_json = data_json.replace("</script>", "<\\/script>")
    final_html = HTML_TEMPLATE.replace("__DATA_JSON__", data_json)
    OUT_HTML.write_text(final_html, encoding="utf-8")

    # 生成 31 个极轻量的单章跳转入口 HTML，方便 Obsidian 用相对路径一键直达对应章节
    entry_dir = EX_DIR / "章节入口"
    entry_dir.mkdir(exist_ok=True)
    for ch in chapters:
        code = ch["code"]
        target = f"../交互刷题.html#ch={code}"
        stub = (
            "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'>"
            f"<meta http-equiv='refresh' content='0;url={target}'>"
            f"<title>第 {code} 章交互刷题</title>"
            f"<script>location.replace('{target}');</script>"
            f"</head><body>正在跳转至第 {code} 章交互刷题… <a href='{target}'>点击这里</a></body></html>"
        )
        (entry_dir / f"第{code}章.html").write_text(stub, encoding="utf-8")

    print(f"Generated {OUT_HTML} ({len(chapters)} chapters, {total_q} questions, {len(final_html):,} bytes) + {len(chapters)} chapter entry stubs")


if __name__ == "__main__":
    main()
