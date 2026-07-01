# IGP 集团编码规范 — 长期记忆

## 架构决策
- 后端：TypeScript + Node.js 20
- 包管理：pnpm（禁用 npm/yarn）
- 数据库：PostgreSQL + Prisma ORM
- 部署：Docker + 阿里云 ECS
- 缓存：Redis (upstash)

## 编码偏好
- 禁止用 `any` 类型，优先用泛型
- 函数式编程优先，避免 class 副作用
- Git 提交遵循 Conventional Commits
- 代码格式化用 Prettier + ESLint

## 历史坑
- 2026-06-15: Docker 镜像构建失败因 pnpm lockfile 未同步
- 2026-06-20: GitHub Action 超时因 DeepSeek API 限流
- 2026-06-25: open() 必须加 encoding='utf-8'，Windows GBK 崩溃
- 2026-06-30: 永远不用 inline Python -c，PowerShell 吃引号
