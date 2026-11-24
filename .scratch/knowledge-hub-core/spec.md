# Spec: Knowledge Hub — 多知识库实时 Markdown 渲染与交互刷题平台

**Status:** ready-for-agent

## Problem Statement

用户拥有一套经过深度精修的 Markdown 英语学习知识库（含 00–31 章线性语法正文、31 套强化练习题库、考试强化与语法字典，以及完整的设计规范文档 `README·设计理念与Agent迭代指南.md`）。目前该资料仅能在本地 Obsidian 与本地离线 HTML 中使用，无法直接通过远程浏览器在 PC 与手机端随时访问学习；且本地 HTML 的 `localStorage` 做题记录绑定在单台设备的单个浏览器中，跨设备无法同步，也无法支持未来扩展多个学科知识库的统一门户入口。同时，用户后续仍以直接修改底层 `.md` 文档的方式迭代知识库，不希望每次修改 `.md` 后还要手动复制或编译生成静态 HTML 页面。

## Solution

构建并部署 `knowledge-hub`（Vue 3 + Vite 前端、Express 后端、Node 内置 `node:sqlite` SQLite 数据库，对外端口 `1906`）：

1. **多知识库主入口门户（Portal）**：首页展示知识库卡片列表（当前提供“英语知识库”入口，含学习进度概览与三大子模块入口：`1.英语学习资料·完整线性版`、`2.同等学力申硕英语·考试强化`、`3.英语语法知识字典`；架构支持未来在 `knowledge-base/` 下新增其他学科知识库）。
2. **纯 Markdown 底层实时驱动**：后端直接实时读取 `knowledge-base/` 下的 `.md` 原文与目录结构（绝不预生成静态拷贝页面）；后续更新或微调任何 `.md` 文件后，刷新页面即可看到最新内容。
3. **Obsidian 级 Markdown 实时渲染引擎**：前端渲染引擎原生支持标准 GFM Markdown 以及本知识库核心减负特性：
   - `==重点高亮==` 渲染为醒目的荧光笔高亮样式；
   - `> [!important] 记笔记`、`> [!warning] 易错避坑`、`> [!tip] 小贴士`、`> [!note] 预告/说明` 渲染为带图标与色彩语义的提醒框；
   - `[[目标文档|显示文本]]` 与 `[[#章内锚点|目录项]]` 转换为站内路由跳转与平滑锚点滚动；
   - `<details><summary>...</summary>...</details>` 原生折叠交互与章末《本章核心记忆笔记》卡片高亮。
4. **数据库驱动的交互刷题中心与错题本**：后端实时解析 `强化题目/*.md` 中的结构化题目（A/B/D/C 分组、`必做/识读必做/选做` 标签、题干、折叠解析、C 组通关线），前端复刻用户高度认可的交互刷题体验（每题独立显隐答案、输入框回车看解析、默认 `⭐ 首轮必做` 减负筛选、`✅ 会了 / ⚠️ 不稳 / ❌ 错了` 三态自评、C 组独立验收实时计分、全局错题本、深浅色护眼主题），所有做题输入、自评状态与章节阅读勾选实时持久化到后端 SQLite 数据库。
5. **PC 与移动端全响应式体验**：支持桌面端双栏（左侧目录/进度树 + 右侧正文/刷题区）与移动端抽屉式目录、底部便捷翻章与触屏友好按钮。

## User Stories

1. 作为学习者，我希望打开主入口时看到清晰的多知识库门户页面（当前展示“英语知识库”卡片及总体学习/刷题进度），以便后续扩展其他学科时有统一的入口。
2. 作为学习者，我希望进入“英语知识库”后可以切换查看 `1.英语学习资料·完整线性版`（主线 32 章 + 交互题库）、`2.同等学力申硕英语·考试强化` 和 `3.英语语法知识字典`，以便在同一平台完成基础学习、查字典与真题强化。
3. 作为学习者，我希望在阅读章节时，页面直接实时渲染底层 `.md` 文件的 `==高亮==` 以及 `> [!important] 记笔记`、`> [!warning] 易错避坑`、`> [!tip] 小贴士`、`> [!note] 说明` 提醒框，以便零心智负担地区分“理解过程”与“必背重点”。
4. 作为学习者，我希望点击正文中的 `[[#锚点]]` 目录链接时平滑滚动到对应小节，点击跨章节 `[[02·名词基础...]]` 双链或底部“上一章 / 下一章”时直接无刷新切换到目标章节。
5. 作为学习者，我希望在每章末尾点击“进入本章交互刷题”时，直接打开该章的交互式刷题视图，无需再去翻看冗长的纯文本 MD 题目。
6. 作为学习者，我希望刷题界面默认只展示 `⭐ 首轮必做` 题目（自动隐藏选做题减轻压力），并支持随时切换 `全部题目`、`未自评`、`错题/不稳` 以及 `A / B / D / C` 分组标签。
7. 作为学习者，我希望每道题都有独立的输入框和 `👁 显示答案 / 🙈 隐藏答案` 按钮（支持在输入框按回车键直接展开答案），避免看一题答案时不小心扫到下一题答案。
8. 作为学习者，我希望每道题都可以点击 `✅ 会了`、`⚠️ 不稳`、`❌ 错了` 进行自评，系统自动按规则（会了 2 分、不稳 1 分、错了 0 分）计算 **C 组独立验收得分** 并提示是否达到本章建议通关分。
9. 作为学习者，我希望我的所有输入框作答内容、题目自评状态和章节“已读完”勾选都实时保存到服务端 SQLite 数据库，这样我无论在电脑浏览器还是手机浏览器远程访问，看到的进度和错题本都是完全一致的。
10. 作为学习者，我希望有一个“📕 全局错题本”视图，汇总所有章节里被标记为 `❌ 错了` 或 `⚠️ 不稳` 的题目，并在我重做标记为 `✅ 会了` 后自动移出错题本。
11. 作为学习者，我希望在手机或平板上访问时，左侧目录自动收起为顶部可呼出的抽屉菜单，字体大小、表格横向滚动与按钮点击区域都针对移动端做好适配，并支持深色/浅色护眼模式切换。
12. 作为知识库作者，我希望直接编辑项目 `knowledge-base/` 目录下的任何 `.md` 正文或题目文件并保存后，无需运行任何静态页面生成脚本，网页端即可实时读取并渲染最新内容。

## Implementation Decisions

- **目录与数据源架构**：
  - `knowledge-base/` 存放完整拷贝进项目的三大英语知识模块与 `README·设计理念与Agent迭代指南.md`。
  - 后端通过文件系统实时扫描 `knowledge-base/`，对外提供知识库列表、目录树、原始 Markdown 内容读取与动态解析后的章节练习题 JSON。
- **后端 API 契约（Express，端口 `1906`）**：
  - `GET /api/health`：健康检查 `{ status: "ok" }`。
  - `GET /api/kbs`：返回知识库门户列表（当前包含 `english` 英语知识库及其子模块、章节总数、已完成章节数、已掌握题数统计）。
  - `GET /api/kbs/:kbId/tree`：返回指定知识库下的模块与文档/练习目录树，合并数据库中的章节勾选完成状态与各章刷题统计。
  - `GET /api/kbs/:kbId/doc?path=<relativeMdPath>`：实时读取并返回指定 `.md` 文档的原文、标题、前后章导航信息及关联的强化练习题路径。
  - `GET /api/kbs/:kbId/exercise/:chapterCode`：实时解析 `强化题目/<chapterCode>·强化练习*.md`，返回结构化题目数据（`scope`, `cFull`, `cPass`, `coverage`, `groups`, `questions`）及数据库中该章各题的已保存 `input` 与 `grade`。
  - `GET /api/kbs/:kbId/wrongbook`：关联查询数据库中所有 `grade IN ('warn', 'bad')` 的题目并结合实时解析的 `.md` 题目内容返回全局错题本列表。
  - `PUT /api/kbs/:kbId/practice`：保存单题作答输入或自评状态 `{ chapterCode, questionId, userInput, grade }` 到 SQLite（幂等 `INSERT ... ON CONFLICT DO UPDATE`）。
  - `DELETE /api/kbs/:kbId/practice/:chapterCode`：重置某章的全部作答与自评记录。
  - `PUT /api/kbs/:kbId/chapter-progress`：切换某篇章节文档的已学完勾选状态 `{ docPath, completed }`。
- **SQLite 数据库 Schema（`backend/data/knowledge-hub.db`，使用 Node 内置 `node:sqlite`）**：
  - `practice_records` 表：`(kb_id TEXT, chapter_code TEXT, question_id TEXT, user_input TEXT DEFAULT '', grade TEXT DEFAULT '', updated_at TEXT, PRIMARY KEY (kb_id, chapter_code, question_id))`
  - `chapter_progress` 表：`(kb_id TEXT, doc_path TEXT, completed INTEGER DEFAULT 0, updated_at TEXT, PRIMARY KEY (kb_id, doc_path))`
- **前端架构与实时渲染引擎（Vue 3 + Vite + `marked` 自定义扩展）**：
  - 扩展 `marked`（或前后置转换管道）：
    1. 将 `==文本==` 转换为 `<mark class="md-highlight">文本</mark>`；
    2. 将块级引用中以 `[!(important|warning|tip|note)]\s*(.*)` 开头的段落转换为结构化 Obsidian Callout 组件 `<div class="callout callout-<type>">...</div>`；
    3. 将 `[[目标|别名]]` 与 `[[目标]]` 转换为带 `data-wikilink` 属性的可点击内链，由前端事件代理拦截并执行章内平滑滚动、跨章文档切换或直达对应章节交互刷题页。
- **生产部署与单端口服务**：
  - 生产环境下由 Express 统一托管 `frontend/dist` 静态资源与 `/api/*` 接口，统一通过 `1906` 端口对外提供服务，完美兼容 `deploy-to-server` 技能的一键 Docker 部署。

## Testing Decisions

- **测试接缝（Testing Seams）**：
  - 以**后端 HTTP API + SQLite 数据库 + 真实/临时 Markdown 文件系统**作为核心集成测试接缝（只测外部可观测的 HTTP 响应与持久化行为，不测内部私有函数细节）；
  - 以**前端 Markdown 渲染引擎纯函数转换结果**（输入包含 `==高亮==`、`> [!important] 记笔记`、`[[双链]]` 的 Markdown 字符串，断言输出的 HTML 结构）作为前端核心单元接缝。
- **将测试的模块**：
  1. 知识库目录树与 `.md` 文档实时读取接口（验证修改 `.md` 后接口立即返回新内容）；
  2. 强化练习 `.md` 实时解析接口（验证 31 章题目、A/B/D/C 分组、必做标签、答案解析 100% 准确提取）；
  3. SQLite 做题记录保存、章节重置、C 组计分数据与全局错题本聚合接口；
  4. Obsidian 扩展 Markdown 渲染引擎（高亮、四类 Callout 提醒框、Wiki 双链转换）。

## Out of Scope

- 多用户注册登录与权限隔离（当前为个人专属远程知识库，单用户全局共享 SQLite 进度）。
- 在网页端直接提供 Markdown 在线富文本编辑器（知识库内容更新仍通过本地/Agent 编辑 `.md` 文件驱动）。

## Further Notes

- 严格遵守 `knowledge-base/1.英语学习资料·完整线性版/README·设计理念与Agent迭代指南.md` 中的所有教学与视觉规范。
