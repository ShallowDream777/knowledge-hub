# knowledge-hub

AI Agent 驱动的多知识库在线学习与交互刷题平台（以底层 Markdown 文档实时渲染驱动，支持 PC/移动端与做题数据 SQLite 持久化）。

> ⚠️ **本项目由 AI Agent 驱动。** 日常迭代（提需求、改 bug、更新知识库、部署）通过 agent 对话完成——
> agent 自动走「设计澄清 → spec → ticket → 实现 → 审查」流程（`auto-mattpocock` 技能），
> 部署由 `deploy-to-server` 技能一键完成。开发者不需要手动维护 spec/ticket/部署脚本——
> 正常描述需求即可。

## Agent 驱动的工作方式

- **正常对话即可**：说「加个 XX 功能」「这个 bug 修一下」「部署」等，agent 自动处理
  （`auto-mattpocock` 路由迭代流程，`deploy-to-server` 处理部署）。
- **修改请求**：agent 会先对照 spec/原型判断错在 spec / ticket / 代码哪一层，该同步的文档会同步。
- **知识库迭代规范**：修改 `knowledge-base/` 下的 Markdown 知识库内容时，必须遵守 `knowledge-base/1.英语学习资料·完整线性版/README·设计理念与Agent迭代指南.md`。
- **技术栈**：Vue 3 + Vite（前端）/ Express（后端）/ SQLite（数据库，`node:sqlite`）/ Node.js（运行时）；公开端口 1906。

## 开发

```bash
npm install        # 安装依赖（workspaces: frontend + backend）
npm run dev        # 并行启动 frontend (Vite) 与 backend (Express)
npm test           # 测试
```

## 一键部署（由 agent 完成）

对 agent 说「部署到服务器」→ agent 读 `deploy.config.json` → 打包上传 → 服务器构建启动 →
健康检查并报告访问地址。首次会问服务器 IP / SSH 用户名，之后复用配置。

## 目录速查

- 知识库源文档（MD 驱动）：`knowledge-base/`
- 英语知识库设计规范：`knowledge-base/1.英语学习资料·完整线性版/README·设计理念与Agent迭代指南.md`
- 领域词汇：`CONTEXT.md`
- 规格与 ticket：`.scratch/<feature>/`
- 部署配置：`deploy.config.json`
- Agent 约定：`AGENTS.md`、`docs/agents/`
