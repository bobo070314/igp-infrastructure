# 🛡️ 第四层：监控与可观测性（v0.4.0）

## 核心变更

1. **监控**: 使用 `diagnostics.otel.metricsEndpoint` 推送指标到 OTEL Collector
2. **成本**: 沿用 `agents.defaults.costLimit`（每日 $10/单次 $0.5），不做多余改动
3. **自愈**: OpenClaw 配置层不支持 `autoRestart`，改为 Docker `restart: unless-stopped`
4. **配置合并**: 将 v0.2.0/v0.3.0/v0.4.0 的配置字段统一写入 `config/openclaw.json5`

## 真实 Schema 说明

| 外部建议的假字段 | 真实 OpenClaw 字段 | 说明 |
|-----------------|-------------------|------|
| `metrics.*` 根级 | `diagnostics.otel.metricsEndpoint` | OpenClaw 不暴露 HTTP metrics endpoint |
| `costLimits.*` 根级 | `agents.defaults.costLimit` | 成本在 agent 级别控制 |
| `autoRestart` | 不存在 | 自愈交给 Docker 编排 |
| `tools.exec.retry` | 不存在 | 无此字段 |

## 部署步骤

### 1. 启动 OTEL Collector

```bash
docker run -d \
  --name otel-collector \
  -p 4318:4318 -p 9090:9090 \
  -v ./monitoring/otel-collector.yaml:/etc/otel-collector.yaml \
  otel/opentelemetry-collector:latest
```

### 2. 重载 Gateway

```bash
openclaw gateway reload
```

### 3. 容器自愈（Docker Compose）

在 `docker-compose.yml` 中添加：

```yaml
services:
  openclaw-main:
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:18791/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 验证

- OTEL Collector: `http://localhost:9090` (Prometheus)
- Gateway 指标: `openclaw diagnostics status`
- 健康检查: `docker ps` 看容器状态

## 四层最终结构

```
igp-infrastructure/
├── config/
│   └── openclaw.json5          ← 四层合并版（所有真实字段）
├── agents/                     ← 4子Agent + 共享
│   ├── coding/{SOUL,USER,MEMORY,AGENTS}.md
│   ├── research/{SOUL,MEMORY}.md
│   ├── ops/{SOUL,MEMORY}.md
│   ├── exec/{SOUL,MEMORY}.md
│   └── shared/memory/global-knowledge.md
├── mcp/metamcp.json            ← MetaMCP 聚合
├── monitoring/
│   └── otel-collector.yaml     ← OTEL Collector 配置
├── docker/                     ← v0.1.0
├── profiles/                   ← v0.1.0
├── scripts/                    ← v0.1.0
└── README.md                   ← 总览
```

## 版本标签

| Tag | 层级 | 内容 |
|-----|------|------|
| v0.1.0 | 一、基础设施 | Docker / Multi-Gateway / Tunnel |
| v0.2.0 | 二、控制平面 | Agent / Bindings / Fallback / Safety |
| v0.3.0 | 三、档案馆+MCP | Memory Search + MCP Hub |
| v0.4.0 | 四、监控 | OTEL + Cost + Docker自愈 |
