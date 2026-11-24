# 05 — 可选登录与“数据库优先 + 浏览器缓存双写”的刷题/阅读记录

**What to build:** 提供非强制的登录/注册功能：未登录时正常使用，刷题记录与阅读记录读写浏览器 `localStorage`；登录后刷题记录与阅读记录同时写入后端 SQLite 数据库与本地 `localStorage`，读取时**优先使用数据库数据**（若数据库中尚无记录则可用本地缓存兜底并回写数据库）。门户卡片将“已学完文档”改为“上次阅读章节”，主按钮在初次进入时显示“📖 进入阅读学习”，已有阅读记录时变为“📖 继续上次阅读”并一键直达上次读到的章节。

**Blocked by:** 04 — PC/移动端响应式布局、深浅色护眼主题与单端口生产托管

**Status:** resolved

- [x] 后端新增用户认证接口（`POST /api/auth/register`、`POST /api/auth/login`、`GET /api/auth/me`、`POST /api/auth/logout`），使用 Node 内置 `node:crypto` 安全哈希密码与生成 Token
- [x] 后端 SQLite 支持按登录用户持久化刷题记录（`user_practice_records`）、章节完成状态（`user_chapter_progress`）与上次阅读章节（`user_reading_state`，`PUT /api/kbs/:kbId/reading-state`）
- [x] 未登录时所有读取接口（`/api/kbs`、`/api/kbs/:kbId/tree`、`/api/kbs/:kbId/exercise/:code`）无需鉴权即可访问知识库与题目结构，前端自动从 `localStorage` 读取/计算刷题记录、错题本与上次阅读章节
- [x] 登录后前端从数据库加载并优先采用数据库中的刷题记录与上次阅读章节（若数据库为空而本地有缓存，支持自动合并上云），每次阅读切章或刷题操作同时写入数据库与 `localStorage`
- [x] 门户卡片“已学完文档”改为“上次阅读章节”；主按钮根据是否有阅读记录动态切换“📖 进入阅读学习”与“📖 继续上次阅读”
