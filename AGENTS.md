# AGENTS.md

## General conventions（通用约定）

- **Language**: 本项目 AI agent 对话默认使用中文（Chinese）。
- **Iteration workflow（迭代流程）**: 需求、变更、bug 一律先走 `auto-mattpocock` 技能——它负责判断阶段并执行对应工程流程（产出 spec + tickets）。
- **Deployment（部署）**: 部署/升级由 `deploy-to-server` 技能一键完成（配置见 `deploy.config.json`）；直接对 agent 说"部署"即可。
- **Knowledge-base first（Markdown 底层驱动约定）**: `knowledge-base/` 下的 `.md` 文档是所有知识与练习题的唯一真实数据源（Single Source of Truth）。前端页面通过渲染引擎动态渲染 MD 内容，严禁将 MD 静态复制生成硬编码页面。迭代英语知识库内容时必须严格遵守 `knowledge-base/1.英语学习资料·完整线性版/README·设计理念与Agent迭代指南.md`（分段拆块、`==高亮==`、`> [!important/warning/tip/note]` 提醒框、章末《本章核心记忆笔记》）。
- **Issue tracker**: Issues are tracked as local markdown files under `.scratch/<feature>/`（见 `docs/agents/issue-tracker.md`）。
- **Domain docs**: Single-context layout — one `CONTEXT.md` + `docs/adr/` at the repo root（见 `docs/agents/domain.md`）。
- **Correction-handling rule（修正处理规则）**: 收到与 spec/原型相关的修正请求时，先对照 spec（`.scratch/<feature>/spec.md`）与原型判定错在哪层：
  - **spec 错/不完整** → 先向用户指出并提议更新 spec（走 auto-mattpocock 的 to-spec 流程），由用户决定；spec 变更后同步受影响的 ticket。
  - **spec 与原型冲突** → 停下请用户裁决，绝不自己选边。
  - **实现偏离清晰 spec/原型** → 直接修代码，改完对照 spec/原型验证。

## Agent skills

### Issue tracker

本仓库 issue / spec / ticket 以本地 markdown 文件存放于 `.scratch/<feature>/`。详见 `docs/agents/issue-tracker.md`。

### Triage labels

使用五套默认 triage 标签：`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`。详见 `docs/agents/triage-labels.md`。

### Domain docs

Single-context 布局 — 仓库根目录一个 `CONTEXT.md` + `docs/adr/`。详见 `docs/agents/domain.md`。
