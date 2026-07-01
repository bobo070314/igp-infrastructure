# IGP International Group — Enterprise Infrastructure

> **Production-grade Infrastructure-as-Code for OpenClaw Enterprise Deployment**
>
> Transform OpenClaw from single-machine CLI to multi-node enterprise AI agent platform.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/Powered_by-OpenClaw-FF6B35)](https://github.com/openclaw/openclaw)

---

## Architecture at a Glance

```
┌──────────────────────────────────────────────────────────────┐
│                    IGP International Group                     │
├─────────────────┬─────────────────┬────────────────┬─────────┤
│   HQ Building   │  Branch Offices  │  Perimiter      │ Power   │
│   Docker        │  Multi-Gateway   │  Cloudflare     │ Cross-  │
│   Compose       │  Profile Group   │  Tunnel         │ platform│
│                 │                  │                 │         │
│   Gateway       │  main @18791     │  Zero open port │ Ubuntu  │
│   IGP API       │  ops @19789      │  All via tunnel │ Windows │
│   PostgreSQL    │  rescue @20789   │  Access auth    │ Mac Mini│
│   MetaMCP       │  enterprise      │  WAF filtering  │ RPi/NAS │
└─────────────────┴─────────────────┴─────────────────┴─────────┘
```

## What's Inside

| Module | Status | Description |
|--------|--------|-------------|
| 🏢 **Headquarters** | ✅ Production-ready | Docker Compose for Gateway + API + DB |
| 🌍 **Branch Offices** | ✅ Multi-Profile | 4 profile templates + 3 deployment strategies |
| 🛡️ **Zero Trust Network** | ✅ Cloudflare Tunnel | Manual/auto setup + Access + WAF |
| ⚡ **Cross-Platform** | ✅ Any machine | Linux / Windows / macOS / ARM64 |

## Quick Start (5 min)

```bash
# Clone
git clone https://github.com/bobo070314/igp-infrastructure.git
cd igp-infrastructure

# Configure
cp docker/.env.example docker/.env
# Edit .env: add your API keys

# Launch HQ
docker compose -f docker/docker-compose.yml up -d

# Verify
curl http://127.0.0.1:18791/health

# Deploy branch offices
bash scripts/start-branches.sh
# Or on Windows:
python scripts/infra_deploy.py gateway
```

## Security (enabled by default)

- ✅ Non-root container user
- ✅ `127.0.0.1` only binding — no public ports
- ✅ Cloudflare Zero Trust authentication
- ✅ Memory & CPU limits per container
- ✅ Healthcheck with auto-restart
- ✅ All capabilities dropped (`cap_drop: ALL`)

## Infrastructure Layers (coming next)

After this foundation, the following layers build on top:

1. 🏢 **Infrastructure** ← You are here
2. 🧠 **Gateway Control Plane** — Channel adapters, Bindings routing, Model failover
3. 🏭 **Agent Departments** — Multi-agent six-piece isolation
4. 🛠️ **Shared Service Center** — MetaMCP + 500+ Skills
5. 📚 **Archive** — Memory four-layer stack
6. 🛡️ **Compliance** — Sandbox + Allowlist + HITL + Cost Cap

## License

MIT © bobo070314

---

> Built for the OpenClaw ecosystem. [OpenClaw](https://github.com/openclaw/openclaw) is MIT-licensed.
