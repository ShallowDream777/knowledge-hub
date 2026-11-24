# 02 — 底层 Markdown 实时读取与 Obsidian 级前端渲染引擎

**What to build:** 用户在知识库中点击任意 `.md` 章节时，后端实时读取磁盘上的 `.md` 原文（不生成静态拷贝文件），前端渲染引擎将其动态渲染为排版清爽、分段清晰的教学页面，原生支持 `==荧光笔高亮==`、四类 Obsidian Callout 提醒框（`> [!important] 记笔记`、`> [!warning] 易错避坑`、`> [!tip] 小贴士`、`> [!note] 预告/说明`）、`[[Wiki双链]]`（章内锚点平滑跳转、跨章无刷新切换、跳练习页）、`<details>` 折叠块以及前后章导航。

**Blocked by:** 01 — 多知识库门户与底层 Markdown 目录树及进度勾选

**Status:** resolved

- [x] `GET /api/kbs/:kbId/doc?path=<relativeMdPath>` 实时读取磁盘 `.md` 原文，校验路径防越权，并返回前后章路径及关联的强化练习章节号（若有）
- [x] 前端 Markdown 渲染引擎纯函数支持 `==高亮==` → `<mark class="md-highlight">`
- [x] 前端 Markdown 渲染引擎支持 `> [!(important|warning|tip|note)] 标题` 转换为带语义图标与样式的提醒框
- [x] 前端 Markdown 渲染引擎将 `[[目标|显示名]]` 与 `[[#锚点|显示名]]` 及指向 `强化题目` 的相对链接转换为站内路由跳转（直接进入对应章节或交互刷题视图）
- [x] 修改磁盘 `.md` 文件后刷新接口即可看到最新内容，单元测试覆盖渲染引擎核心语法
