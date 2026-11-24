# 01 — 多知识库门户与底层 Markdown 目录树及进度勾选

**What to build:** 用户打开主入口时看到多知识库门户（当前展示“英语知识库”卡片及下属三个子模块 `1.英语学习资料·完整线性版`、`2.同等学力申硕英语·考试强化`、`3.英语语法知识字典` 的章节与刷题进度统计）；点击进入知识库后，左侧展示由底层文件系统实时扫描生成的模块与 Markdown 文档树，并支持将任意章节勾选为“已学完”（持久化到 SQLite `chapter_progress` 表）。

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] `GET /api/kbs` 返回知识库门户列表（含 `english` 英语知识库、子模块数、总章节数、已完成章节数、已掌握题数）
- [x] `GET /api/kbs/:kbId/tree` 实时扫描 `knowledge-base/` 目录结构（自动过滤 `编排记录`、`精修前快照`、`章节入口` 等非阅读辅助目录），合并 SQLite 中的章节完成状态与各章刷题进度
- [x] `PUT /api/kbs/:kbId/chapter-progress` 将章节勾选状态持久化到 SQLite `chapter_progress` 表
- [x] 前端门户视图展示知识库入口卡片，点击进入知识库阅读/刷题主工作台
