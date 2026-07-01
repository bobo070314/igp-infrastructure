# IGP 国际集团 — 多 Gateway + Profile 群控方案
#
# 对标 OpenClaw "多 Gateway + Profile 群控"
#
# 为什么需要多 Gateway？
#   1. 凭证隔离 — 不同部门的 API Key 各自独立
#   2. 资源隔离 — 研发部跑重模型，行政部跑轻模型
#   3. 物理隔离 — 可以分布在阿里云/公司服务器/Mac Mini
#   4. 故障容灾 — 主 Gateway 挂了，rescue Gateway 顶上
#
# 架构：
#   openclaw --profile main    → 主 Gateway :18789（或 18791）
#   openclaw --profile ops     → 运维 Gateway :19789
#   openclaw --profile rescue  → 救援 Gateway :20789（隔离状态）
#   openclaw --profile research → 研究 Gateway :21789（deep research）
#
# 部署位置建议：
#   本地台式机  → main + research（开发/研究用）
#   阿里云VPS   → ops + api（24小时在线服务）
#   公司服务器   → enterprise（内部业务）
#   树莓派/NAS  → rescue（低功耗备用）

# ====================================================================
# 方案 A：单机多 Gateway（最少配置）
# ====================================================================
# 一台机器上运行多个 Gateway，通过不同端口区分
#
# 1. 主 Gateway (国际版)
#    openclaw --profile main --port 18791 gateway
#
# 2. 运维 Gateway
#    openclaw --profile ops --port 19789 gateway
#
# 3. 救援 Gateway
#    openclaw --profile rescue --port 20789 gateway
#
# 每个 profile 有自己的：
#   ~/.openclaw/profiles/main/config.yaml
#   ~/.openclaw/profiles/ops/config.yaml
#   ~/.openclaw/profiles/rescue/config.yaml

# ====================================================================
# 方案 B：多机多 Gateway（生产级）
# ====================================================================
# 通过 SSH 隧道/ZeroTier/Tailscale 组成内网
#
# ┌─────────────────────────────────────────────────────────────┐
# │  本地 (Windows)                  阿里云 (Ubuntu)            │
# │  ┌─────────────────────┐         ┌──────────────────────┐  │
# │  │ main @ :18791       │ ◄─────►│ ops @ :19789         │  │
# │  │ research @ :21789   │         │ metamcp @ :12008     │  │
# │  │ Postgres (local)    │         │ postgres (production) │  │
# │  └─────────────────────┘         └──────────────────────┘  │
# │                                                             │
# │  公司服务器                     Mac Mini / 树莓派          │
# │  ┌─────────────────────┐         ┌──────────────────────┐  │
# │  │ enterprise @ :22789 │         │ rescue @ :20789      │  │
# │  │ 内部业务 Agent     │         │ 备用/保活 Agent     │  │
# │  └─────────────────────┘         └──────────────────────┘  │
# └─────────────────────────────────────────────────────────────┘

# ====================================================================
# 方案 C：Docker Compose 多 Gateway（推荐）
# ====================================================================
# 见 ../docker/docker-compose.yml
# 在 docker-compose.yml 中加多个 gateway 服务即可：
#
# services:
#   gateway-main:
#     image: openclaw/openclaw:latest
#     container_name: igp-gateway-main
#     ports: ["127.0.0.1:18791:18789"]
#     volumes: ["./data/main:/home/node/.openclaw"]
#
#   gateway-ops:
#     image: openclaw/openclaw:latest
#     container_name: igp-gateway-ops
#     ports: ["127.0.0.1:19789:18789"]
#     volumes: ["./data/ops:/home/node/.openclaw"]
#     profiles: ["full"]

# ====================================================================
# 启动脚本参考
# ====================================================================
#
# PowerShell:
#   openclaw --profile main --port 18791 gateway start
#   openclaw --profile ops --port 19789 gateway start &
#   openclaw --profile rescue --port 20789 gateway start &
#
# Linux:
#   nohup openclaw --profile main --port 18789 gateway > /var/log/igp/main.log 2>&1 &
#   nohup openclaw --profile ops --port 19789 gateway > /var/log/igp/ops.log 2>&1 &
#   nohup openclaw --profile rescue --port 20789 gateway > /var/log/igp/rescue.log 2>&1 &
#
# Docker Compose:
#   docker compose --profile full up -d gateway-main gateway-ops
