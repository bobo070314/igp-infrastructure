# IGn 国际集团 — Gateway 控制平面部署手册

## 修正说明（相对外部建议版本）

| 外部建议 | 外部建议的写法 | OpenClaw 实际写法 | 为什么改 |
|----------|---------------|-------------------|----------|
| models 根级别 | models.json | agents.defaults.models | OpenClaw schema 不允许根级别 models |
| fallback 对象 | strategy/delayMs/chain | agents.defaults.model.fallbacks 数组 | OpenClaw 用数组 key 做 fallback |
| safety 根级别 | safety/allowlist.json | agents.defaults.tools.exec.allow | 安全配置在 agent 内部 |
| Bindings 格式 | {channel, chat, agent} | {agentId, match: {channel}} | OpenClaw 真实格式 |

## 部署步骤

### 1. 配置注入

```bash
# 复制到 OpenClaw 配置路径
cp config/openclaw.json5 ~/.openclaw/openclaw.json

# 创建子 Agent 工作区
mkdir -p ~/.openclaw/workspace-{coding,research,ops,exec}
```

### 2. 配置子 Agent 上下文

```bash
cp -r agents/coding ~/.openclaw/
cp -r agents/research ~/.openclaw/
cp -r agents/ops ~/.openclaw/
cp -r agents/exec ~/.openclaw/
```

### 3. 设置环境变量

```bash
# Telegram Bot Token（必须）
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."

# 飞书（如启用）
export FEISHU_APP_ID="cli_xxxxxx"
export FEISHU_APP_SECRET="xxxxxx"
```

### 4. 启动 Gateway

```bash
openclaw gateway start
# 或指定端口
openclaw --port 18791 gateway start
```

### 5. 验证

```bash
# 检查 Gateway 状态
openclaw status

# 查看路由是否生效
openclaw config get bindings
```

## 验证路由

在 Telegram 研发群发消息:

```
帮我写一个 hello world in TypeScript
```

预期: 由 coding Agent 处理，deepseek/deepseek-v4-flash 响应

## 故障排查

Gateway 拒绝启动:
```bash
openclaw doctor
openclaw doctor --fix
```

查看活动 Agent:
```bash
openclaw config get agents.list
```
