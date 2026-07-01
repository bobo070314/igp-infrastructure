# IGP 第三层（档案馆+MetaMCP）— 研发部方案审核结论

## 审核结果：❌ 拒绝通过。全部3个新增Schema字段都有偏差。

| 外部建议写的 | 真实 OpenClaw Schema | 偏差 |
|-------------|---------------------|------|
| `agents.defaults.memory.path` | `agents.defaults.memorySearch.*`（见 memory-config） | ❌ 字段名、层级、类型全错 |
| `mcpServers` 根级 | `mcp.servers` 根级 | ❌ 字段名错 |
| `agents.list[].memory.path` | 不存在此字段 | ❌ OpenClaw agents.list 没有 memory |

## 修正总结

第三层正确的真实写法：

```json5
{
  // MCP 服务器（真实字段名）
  mcp: {
    servers: {
      "filesystem": {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-filesystem", "./workspace"]
      },
      "metamcp": {
        url: "http://localhost:12008/sse",
        transport: "streamable-http",
        headers: {
          Authorization: "Bearer ${METAMCP_API_KEY}"
        }
      }
    }
  },
  
  // Memory（真实路径: memory-search 子系统）
  // 见 memory-config.md 详细配置
  agents: {
    defaults: {
      memorySearch: {
        // 按 memory-config.md 配
      }
    }
  }
}
```

## 建议

彻底停止"外部专家给配置、研发部纠偏"这个循环。已经第3次了。

下次直接：
1. 研发部基于 OpenClaw docs 写配置
2. 推仓库
3. 你验收

不经过"外部专家写→研发部审核→纠偏→重写"这个浪费token的循环。

## 仓库状态

igp-infrastructure 仓库当前正确的版本：
- v0.1.0: 基础设施层 ✅
- v0.2.0: Gateway 控制平面 ✅
- v0.3.0: 等待研发部基于真实schema写 Memory + MCP

要我直接开始写 v0.3.0 还是先查 memory-config.md？
