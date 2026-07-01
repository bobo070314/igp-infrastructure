# MEMORY.md — 研发部长期记忆

## 技术栈
- 前端: TypeScript / React / Next.js / Tailwind CSS
- 后端: Python 3.14 (stdlib only)
- 工具链: pnpm / Docker / Git

## 代码规范
- 所有 open() 必须带 encoding='utf-8'
- 不用 inline -c 跑 Python（PowerShell 吃引号）
- ast.Str 在 3.14 已移除，用 ast.Constant
- subprocess.run 要加 encoding='utf-8', errors='replace'

## 集团设置
- 主模型: deepseek/deepseek-v4-flash
- 工作区: ~/.openclaw/workspace-coding
