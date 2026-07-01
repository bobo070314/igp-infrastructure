# IGP 国际集团 — Cloudflare Tunnel 部署方案
#
# 对标 OpenClaw "Cloudflare Tunnel: 不开放公网端口"
#
# 为什么用 Tunnel 而不是直接暴露端口：
#   ❌ 直接暴露 18791 → 三天内被扫描 21000+ 次（安全报告）
#   ✅ Cloudflare Tunnel → 零开放端口，DDoS 防护，WAF 过滤
#
# 架构：
#   用户 → Cloudflare Edge → Access 认证 → Tunnel → localhost:18791
#
# 前提条件：
#   1. Cloudflare 账号（free tier 即可）
#   2. 一个域名（DNS 在 Cloudflare 管理）
#   3. 服务器能出站访问互联网（不需要入站端口）

# ====================================================================
# 方案 A：手动创建 Tunnel（推荐）
# ====================================================================
# Step 1: 登录 Cloudflare Dashboard
#   https://one.dash.cloudflare.com/ → Zero Trust → Networks → Tunnels
#
# Step 2: 创建 Tunnel
#   - Click "Create a tunnel"
#   - Name: igp-tunnel
#   - 复制 token（以 eyJ 开头的 base64 字符串）
#
# Step 3: 配置 Docker Compose
#   编辑 ../docker/.env，填入：
#   CF_TUNNEL_TOKEN=eyJhIjoiYWJj...
#
# Step 4: 启动
#   docker compose up -d cloudflared
#
# Step 5: 配置路由
#   Cloudflare Dashboard → Tunnel → igp-tunnel → Public Hostname
#   Subdomain: igp
#   Domain: yourdomain.com
#   Service: http://localhost:18791
#
# Step 6: 配置 Access（先配再连域名，保证从不暴露）
#   Zero Trust → Access → Applications → Add application
#   Application name: IGP Gateway
#   Session duration: 24h
#   Domain: igp.yourdomain.com
#   Policy: Allow → Email OTP（或 SSO）

# ====================================================================
# 方案 B：自动创建 Tunnel（高级）
# ====================================================================
# 需要 CF_API_TOKEN 权限：
#   Account: Account Settings (Read)
#   Account: Cloudflare Tunnel (Edit)
#   Zone: DNS (Edit)
#
# .env 配置：
#   CF_API_TOKEN=your-api-token
#   CF_TUNNEL_DOMAIN=igp.yourdomain.com
#
# 自动完成：
#   1. 创建 Tunnel
#   2. 配置 DNS 记录
#   3. 配置路由
#   4. 写入 CF_TUNNEL_TOKEN

# ====================================================================
# nginx 反向代理备选方案
# ====================================================================
# 如果没有 Cloudflare，或用的是 frp/ngrok：
#
# server {
#     listen 443 ssl;
#     server_name igp.yourdomain.com;
#
#     ssl_certificate /etc/nginx/ssl/cert.pem;
#     ssl_certificate_key /etc/nginx/ssl/key.pem;
#
#     location / {
#         proxy_pass http://127.0.0.1:18791;
#         proxy_http_version 1.1;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection "upgrade";
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#     }
# }

# ====================================================================
# 安全建议
# ====================================================================
# 1. 在 Cloudflare Access 启用前不要配置 DNS 记录
# 2. 只用 token-based tunnel（不用 cert.pem）
# 3. TUNNEL_TRANSPORT_PROTOCOL: quic（默认 h2）
# 4. 开启 WAF 规则：rate limiting + bot fight mode
# 5. 考虑 WARP Connector for subnet-level access
