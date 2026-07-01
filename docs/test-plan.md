# 🧪 IGP 集团 · 全链路实战测试计划（v0.4.1）

> 基于真实 OpenClaw Schema 验证
> 拆分多轮避免 Agent 卡壳

---

## 📋 前置检查（必做）

启动 Gateway 和所有依赖后，运行以下命令确认：

```bash
# Gateway
curl http://127.0.0.1:18791/health

# MetaMCP（如有）
curl http://localhost:12008/mcp

# OTEL Collector
curl http://localhost:4318/v1/metrics
```

---

## 🔄 第1轮：档案馆 + Shell执行（核心链路）

### 测试目标
验证 **Channel路由** → **Memory检索** → **Shell执行** 三层联动。

### Prompt（发 Telegram Coding 群）

```
@coding 我记得你的编码规范里，关于TypeScript类型有一条铁律。
请告诉我具体是什么，然后用这个规范写一个 src/utils/greet.ts。
```

### 预期响应

先返回编码规范（从 `MEMORY.md` 检索）：
> 我们的规范禁止使用 `any` 类型，优先用泛型或具体类型。

然后写文件并展示内容：
```typescript
export function greet(name: string): string {
  return `Hello ${name}`;
}
```

### 验证点

| 层级 | 触发模块 | 成功标志 |
|------|----------|----------|
| 第二层 | Channel bindings | Telegram 消息自动路由到 `coding` Agent |
| 第三层 | Memory Search | 返回 "禁止 `any` 类型" |
| 第二层 | Shell exec | 生成 `src/utils/greet.ts`，内容无 `any` 类型 |

---

## 🔄 第2轮：MCP调用 + Model Fallback

### 测试目标
验证 **MCP Server** 调用 + **Model Fallback** 自动切换。

### Prompt（发 Telegram Coding 群）

```
@coding 通过 filesystem 工具，列出当前工作目录的所有文件。
如果第一个模型响应太慢，试试备用模型。
```

### 预期响应

代理先尝试 `deepseek-v4-flash`，超时/失败后自动切 `deepseek-v3`，然后通过 MCP filesystem server 列出文件。

### 验证点

| 层级 | 触发模块 | 成功标志 |
|------|----------|----------|
| 第三层 | MCP (filesystem) | 返回文件列表（含 `src/utils/greet.ts`） |
| 第二层 | Model Fallback | v4-flash 超时后自动切 v3，不中断响应 |

---

## 🔄 第3轮：OTEL监控上报（手动）

### 测试目标
验证 OTEL 指标推送到 Collector / Prometheus。

### 验证命令

```bash
# OTEL Collector 直接看
curl http://localhost:4318/v1/metrics 2>&1 | Select-String "openclaw_"

# Prometheus（如果配了）
curl http://localhost:9090/api/v1/query?query=openclaw_request_total
```

### 成功标志

存在以下指标：
- `openclaw_request_total`
- `openclaw_request_cost_usd`  
- `openclaw_agent_up{agent_id="coding"}`

---

## ❌ 故障排查表

| 问题 | 原因 | 解决 |
|------|------|------|
| Agent 未响应 | Bindings 不匹配 | 确认 Telegram Chat ID 与 `bindings[].match.chat` 一致 |
| Memory 未召回 | memorySearch 路径不对 | 检查 `agents.defaults.memorySearch.extraPaths` 指向 `./agents/shared/memory` |
| MCP 调用失败 | metamcp 未运行 | `docker logs metamcp` 查看错误；确认端口 12008 已监听 |
| 模型未 fallback | fallbacks 数组为空 | 确认 `fallbacks: ["deepseek/deepseek-v3"]` 存在 |
| 监控无数据 | OTEL Collector 未启动 | `docker restart otel-collector`；确认 4318 端口可达 |
| Shell 被拒绝 | 命令不在白名单 | 检查 `tools.exec.allow` 是否包含该命令 |

---

## 🏁 版本标签

本测试计划对应仓库标签 **v0.4.1**，不包含代码变更，仅为测试文档增量。
