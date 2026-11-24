# CONTEXT.md — Domain Glossary

本项目核心领域词汇表（遵循 `docs/agents/domain.md`）：

- **Knowledge Base（知识库）**：位于 `knowledge-base/` 下的一套学科学习资料集合。主入口门户按知识库维度展示卡片（当前已接入“英语知识库” `english`，底层对应 `knowledge-base/1.英语学习资料·完整线性版` 等目录；未来可平级扩展其他学科知识库）。
- **Course / Module（课程模块）**：同一知识库下的子模块，如英语知识库下的 `1.英语学习资料·完整线性版`（主线 0 基础课程）、`2.同等学力申硕英语·考试强化`、`3.英语语法知识字典`。
- **Chapter（章节）**：由底层 `.md` 文件驱动的单章学习内容（如 `00·语音与拼读起步.md`、`01·文字、句子和必备术语.md` ~ `31·...md`）。
- **Markdown Rendering Engine（MD 实时渲染引擎）**：后端读取实时 `.md` 原文，前端在浏览器端动态解析并渲染标准 Markdown 及 Obsidian 扩展语法（`==高亮==`、`> [!important/warning/tip/note]` Callout 提醒框、`[[Wiki双链]]`、`<details>` 折叠块、表格与锚点目录），不在构建期把 MD 复制转存为静态 HTML 页面。
- **Exercise Set（强化题集）**：位于 `强化题目/` 下的配套 `.md` 练习文件（如 `01·强化练习·*.md`），由后端实时解析为结构化题目（含题号 `A01/B01/C01/D01`、分层标签 `必做/识读必做/选做`、主题、题干、参考答案与解析、C 组通关线）。
- **Practice Record（做题持久化记录）**：存储在后端 SQLite 数据库中的用户学习与刷题状态，包括每道题的作答输入（`user_input`）、三态自评（`grade`: `ok` 会了 / `warn` 不稳 / `bad` 错了）、章节阅读勾选进度（`chapter_progress`），并据此动态聚合出**全局错题本**与 **C 组独立验收得分**。
