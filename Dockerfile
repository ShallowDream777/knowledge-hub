# syntax=docker/dockerfile:1
# 由 deploy-to-server 技能生成——按项目结构探测，请审阅后使用。
# ---------- Stage 1: build the frontend ----------
FROM node:24-alpine AS frontend-build
WORKDIR /app
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package.json
COPY backend/package.json backend/package.json
RUN npm ci --workspaces --include-workspace-root=false --no-audit --no-fund
COPY frontend frontend
RUN npm run build -w frontend
COPY backend backend
RUN npm prune --omit=dev --no-audit --no-fund
# ---------- Stage 2: production runtime ----------
FROM node:24-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app
COPY --from=frontend-build /app/backend ./backend
COPY --from=frontend-build /app/frontend/dist ./frontend/dist
COPY --from=frontend-build /app/node_modules ./node_modules
COPY knowledge-base ./knowledge-base
ENV DB_PATH=/data/app.db
ENV PORT=3000
EXPOSE 3000
CMD ["node", "backend/src/index.js"]
