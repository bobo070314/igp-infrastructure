# 🧠 第三层：档案馆 + 共享服务中心（v0.3.0）

## 概述

为 IGP 国际集团各子 Agent 赋予**长期记忆**和**统一工具集**。

## 架构

```
┌────────────────────────────────────────────────┐
│                Gateway (18791)                  │
│                                                 │
│  ┌──────────────┐  ┌──────────────────────┐    │
│  │ Memory Search │  │    MCP Servers       │    │
│  │ (FTS5+sqlite) │  │                      │    │
│  │               │  │ filesystem (stdio)   │    │
│  │ extraPaths:   │  │ metamcp (http)       │    │
│  │ shared/memory │  │ github (stdio)       │    │
│  └──────────────┘  └──────────────────────┘    │
└────────────────────────────────────────────────┘
```

## 文件结构

```
config/
├── openclaw.json5           ← (现有，v0.2.0)
└── memory-mcp-increment.json5  ← 第三层增量配置

agents/
├── coding/
│   ├── SOUL.md              ← (现有)
│   ├── USER.md              ← (现有)
│   ├── AGENTS.md            ★ 协作规则（新增）
│   └── MEMORY.md            ★ 长期记忆（新增）
├── research/
│   ├── SOUL.md              ← (现有)
│   └── MEMORY.md            ★ 研究记忆（新增）
├── ops/
│   ├── SOUL.md              ← (现有)
│   └── MEMORY.md            ★ 运维记忆（新增）
├── exec/
│   ├── SOUL.md              ← (现有)
│   └── MEMORY.md            ★ 行政记忆（新增）
└── shared/
    └── memory/
        └── global-knowledge.md  ★ 集团共享知识库

mcp/
└── metamcp.json             ★ MetaMCP 聚合配置
```

## 部署步骤

### Step 1: 合并配置

将 `config/memory-mcp-increment.json5` 的内容追加到 `config/openclaw.json5` 中。
注意：`memory` 和 `mcp` 是根级别字段，放在现有 `bindings` / `channels` 同级。

### Step 2: 设置环境变量

```bash
# MCP GitHub
export GITHUB_TOKEN="ghp_xxx"

# MetaMCP
export METAMCP_API_KEY="xxx"
```

### Step 3: 启动 MetaMCP（可选）

```bash
docker run -d \
  --name metamcp \
  -p 12008:12008 \
  -v ./mcp/metamcp.json:/config.json \
  metamcp/metamcp:latest
```

### Step 4: 重载 Gateway

```bash
openclaw gateway reload
```

## 验证

### Memory Search 验证

```
在 Telegram Coding 群发: 我们的数据库用什么？
预期: 返回 PostgreSQL + Prisma（来自 coding/MEMORY.md）
```

### MCP 验证

```
在 Telegram 发: 列出工作区的文件
预期: 通过 filesystem MCP server 执行
```

## 真实 Schema 说明

| 外部建议的假字段 | 真实 OpenClaw 字段 | 在 Docs 中的位置 |
|-----------------|-------------------|-----------------|
| `memorySearch.path` | `extraPaths: string[]` | memory-config.md |
| `memorySearch.vectorStore` | 不存在 | — |
| `mcpServers` | `mcp.servers` | configuration-reference.md |
| `agents.list[].memorySearch.path` | 不存在 | — |
