// IGP 集团集团共享记忆 — 全局知识库
// 被 gateway 的 extraPaths 索引，供所有子 Agent 检索

## 集团基本信息
- 名称: IGP 国际集团
- 架构: OpenClaw Gateway (国际版 18791) + 4 个子 Agent
- 仓库: https://github.com/bobo070314/igp-infrastructure

## 技术栈
- AI: DeepSeek v4-flash / v3
- 前端: React / Next.js / Tailwind CSS
- 后端: Python 3.14 (stdlib only) / Node.js 20 / TypeScript
- 数据库: PostgreSQL + Prisma
- 包管理: pnpm
- 容器: Docker

## 编码约定
- 所有 Python open() 必须带 encoding='utf-8'
- 禁止 inline -c 执行 Python（PowerShell 引号问题）
- 禁止 rm -rf / sudo / 未审核的 Docker 操作
- Git 提交: Conventional Commits

## 环境变量
- TELEGRAM_BOT_TOKEN: Telegram Bot Token
- FEISHU_APP_ID: 飞书应用 ID
- FEISHU_APP_SECRET: 飞书应用密钥
- DEEPSEEK_API_KEY: DeepSeek API Key
- METAMCP_API_KEY: MetaMCP 聚合服务密钥
- GITHUB_TOKEN: GitHub Personal Access Token

## 端口
- 18791: OpenClaw 国际版 Gateway
- 18789: OpenClaw 国内版 Gateway
- 12008: MetaMCP 聚合服务
- 8080: IGP API 服务
