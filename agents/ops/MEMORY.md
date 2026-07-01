# IGP 集团运维笔记 — 长期记忆

## 生产环境
- Gateway: OpenClaw 国际版 (端口 18791)
- 所有配置在 igp-infrastructure GitHub 仓库
- Docker Compose 在 infrastructure/docker/

## 安全管理
- 飞书 dmPolicy: allowlist, 需添加用户 ID
- Telegram dmPolicy: pairing, 陌生人需配对
- Shell 白名单: 禁止 rm -rf / sudo / raw ssh
- 成本上限: $10/天, $0.5/次

## 故障处理
- Gateway 拒绝启动 → `openclaw doctor --fix`
- MCP server 超时 → `openclaw mcp status`
- Memory index 损坏 → `openclaw memory index --force --agent <id>`
