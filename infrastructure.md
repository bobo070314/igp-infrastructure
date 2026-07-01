# IGP 国际集团 — 基础设施层

> 对标 OpenClaw 标准架构：总部大楼 · 海外分部 · 园区围墙 · 电力机房

## 状态

| 模块 | 状态 | 文档 |
|------|------|------|
| 🏢 总部大楼 — Docker Compose | ✅ 生产级 + 安全加固 | [docker/](docker/) |
| 🌍 海外分部 — 多 Gateway 群控 | ✅ 3 种方案 + Profile 模板 | [multi-gateway/](multi-gateway/) |
| 🛡️ 园区围墙 — Cloudflare Tunnel | ✅ 手动/自动两种配置 | [cloudflare/](cloudflare/) |
| ⚡ 电力机房 — 跨平台部署 | ✅ Linux/Windows/Macmini/RPi 兼容 | 见下方 |

## 快速开始

```bash
# 1. 进入 docker 目录
cd infrastructure/docker

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Key

# 3. 启动集团总部
docker compose up -d

# 4. 首次配置
docker compose exec openclaw-gateway openclaw onboard
```

## 服务架构

```
┌─────────────────────────────────────────────────────────────┐
│                     IGP 国际集团                              │
├─────────────┬───────────────┬────────────────┬──────────────┤
│  总部大楼    │   海外分部     │   园区围墙      │   电力机房     │
│ Docker      │ Multi-Gateway │ Cloudflare     │ 跨平台        │
│ Compose     │ Profile 群控  │ Tunnel         │ 部署方案      │
│             │               │                │              │
│ Gateway     │ main @18791   │ 无公网端口     │ Ubuntu       │
│ IGP API     │ ops @19789    │ 全部走隧道     │ Windows      │
│ PostgreSQL  │ rescue @20789 │ Access 认证    │ Mac Mini     │
│ MetaMCP     │ enterprise    │ WAF 过滤       │ 树莓派/NAS   │
└─────────────┴───────────────┴────────────────┴──────────────┘
```

## 对标 OpenClaw 标准

| OpenClaw 建议 | IGP 实现 | 文件 |
|---------------|----------|------|
| 一台 Ubuntu + Docker 长期运行 | Windows/Linux Docker Compose 双支持 | [docker/docker-compose.yml](docker/docker-compose.yml) |
| 多 Gateway + Profile 群控 | 4 Profile 模板 + 3 部署方案 | [multi-gateway/](multi-gateway/) |
| Cloudflare Tunnel | 手动/自动双方案 + Access 配置 | [cloudflare/](cloudflare/) |
| 云服务器 / 树莓派 / NAS | 跨平台 Docker + 轻量架构 | 各部署方案 |
| 1GB 内存起步 | 最小配置 512MB（cloudflared 仅 128MB） | docker-compose.yml |

## 部署选项

### 方案 A：Docker Compose（推荐）

```bash
python scripts/infra_deploy.py init     # 环境检查
python scripts/infra_deploy.py docker   # 部署 Docker
python scripts/infra_deploy.py status   # 查看状态
python scripts/infra_deploy.py doctor   # 全链路诊断
```

### 方案 B：原生进程（无 Docker）

```bash
openclaw --profile main --port 18791 gateway start
openclaw --profile ops --port 19789 gateway start
openclaw --profile rescue --port 20789 gateway start
```

### 方案 C：混合部署

- 本地：主 Gateway (main @18791)
- 阿里云：运维 Gateway (ops @19789) + PostgreSQL
- Mac Mini：救援 Gateway (rescue @20789)

## 安全加固

1. **端口只绑 127.0.0.1**：不暴露公网
2. **Cloudflare Tunnel**：零开放端口
3. **容器非 root 运行**：user: node:node
4. **内存 + CPU 限制**：防止资源耗尽
5. **健康检查**：自动重启故障服务
6. **容丢弃所有能力**：cap_drop: ALL

## 与 IGP 集团的关系

```
IGP 国际集团（你的 OpenClaw 实例）
  │
  ├── infrastructure/    ← 你在这里
  │   ├── docker/         Docker Compose 总部
  │   ├── multi-gateway/  海外分部
  │   ├── cloudflare/     园区围墙
  │   └── profiles/       Profile 模板
  │
  ├── family-corp-teams/  ← IGP 核心（36 团队、19 染色体、硅胶体记忆）
  │
  └── (其他 OpenClaw 配置)
```

## 许可证

MIT — IGP 国际集团内部使用
