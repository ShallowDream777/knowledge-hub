# 03 — 强化题库 MD 实时解析与 SQLite 刷题持久化闭环

**What to build:** 用户点击任意章节末尾的“进入本章交互刷题”或左侧刷题入口时，后端实时解析 `强化题目/` 下对应的 `.md` 文件，前端呈现完整的交互刷题界面（默认 `⭐ 首轮必做` 筛选、A/B/D/C 分组切换、每题独立输入框与回车看解析、每题独立 `👁 显示答案 / 🙈 隐藏答案`、`✅ 会了 / ⚠️ 不稳 / ❌ 错了` 三态自评、C 组独立验收实时计分与达标提示、📕 全局错题本），所有做题输入与自评实时持久化到后端 SQLite 数据库。

**Blocked by:** 01 — 多知识库门户与底层 Markdown 目录树及进度勾选

**Status:** resolved

- [x] `GET /api/kbs/:kbId/exercise/:chapterCode` 实时解析 `强化题目/<chapterCode>·强化练习*.md`（提取范围边界、C 组满分与建议达标分、练习范围与易错点表、A/B/D/C 题目与折叠答案），并合并 SQLite `practice_records` 中的 `user_input` 与 `grade`
- [x] `PUT /api/kbs/:kbId/practice` 幂等保存单题 `userInput` 与 `grade`（`ok` / `warn` / `bad` / `""`）至 SQLite
- [x] `DELETE /api/kbs/:kbId/practice/:chapterCode` 重置指定章节的所有刷题记录
- [x] `GET /api/kbs/:kbId/wrongbook` 聚合所有 `grade IN ('warn', 'bad')` 的题目并返回完整题面与解析，重评为 `ok` 后自动移出
- [x] 集成测试验证 31 章 1,278 道题解析无遗漏、SQLite 持久化与错题本聚合准确
