# Coding Department — 子 Agent 协作规则

## 工作流

当你收到开发任务时，按以下顺序处理：

1. **规划** — 拆解任务为子步骤
2. **查询记忆** — 检查 MEMORY.md 和 shared/memory/ 了解历史决策
3. **实现** — 写代码（遵守 MEMORY.md 编码规范）
4. **自查** — 跑 linter + 测试
5. **部署** — 使用 `@ops` 通知运维部

## 调用其他部门

- 需要部署 → `@ops 部署 xxx`
- 需要研究新技术 → `@research 研究 xxx`
- 需要行政支持 → `@exec 发送周报`

## Git 提交规范

```
<type>(<scope>): <subject>

feat: 新功能
fix: 修复
refactor: 重构
docs: 文档
chore: 工具/构建
```

注意：提交前先 `git status` 确认变动。
