#!/usr/bin/env python3
"""
IGP 国际集团 — 基础设施一键部署脚本
对标 OpenClaw 标准架构：Docker + Multi-Gateway + Tunnel + Monitoring

用法：
  python infra_deploy.py init          # 初始化环境检查
  python infra_deploy.py docker        # 部署 Docker Compose
  python infra_deploy.py gateway       # 部署多 Gateway
  python infra_deploy.py tunnel        # 配置 Cloudflare Tunnel
  python infra_deploy.py status        # 查看所有服务状态
  python infra_deploy.py doctor        # 全链路诊断
"""

import os
import sys
import subprocess
import json
from datetime import datetime

INFRA_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKER_DIR = os.path.join(INFRA_DIR, 'docker')
MULTI_GW_DIR = os.path.join(INFRA_DIR, 'multi-gateway')
CF_DIR = os.path.join(INFRA_DIR, 'cloudflare')

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def log_info(msg):
    print(f'{BLUE}[INFO]{RESET} {msg}')

def log_ok(msg):
    print(f'{GREEN}[OK]{RESET} {msg}')

def log_warn(msg):
    print(f'{YELLOW}[WARN]{RESET} {msg}')

def log_err(msg):
    print(f'{RED}[ERR]{RESET} {msg}')

def run_cmd(cmd, check=True, timeout=30):
    """运行命令并返回输出"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          timeout=timeout, encoding='utf-8', errors='replace')
        if r.returncode != 0 and check:
            log_err(f'命令失败: {cmd}')
            log_err(r.stderr.strip())
            return None
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        log_err(f'命令超时: {cmd}')
        return None
    except Exception as e:
        log_err(f'命令异常: {e}')
        return None

def check_prerequisites():
    """检查所有前置条件"""
    print(f'\n{"="*60}')
    print(f' IGP Infrastructure — 环境检查')
    print(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'{"="*60}\n')
    
    checks = []
    
    # 1. 检查 Python
    py = run_cmd('python --version', check=False)
    checks.append(('Python', py and '3' in py, py or '未安装'))
    
    # 2. 检查 Docker
    docker = run_cmd('docker --version', check=False)
    checks.append(('Docker', docker and 'Docker' in docker, docker or '未安装'))
    
    # 3. 检查 Docker Compose
    dc = run_cmd('docker compose version', check=False)
    checks.append(('Docker Compose', dc and 'v2' in dc, dc or '未安装'))
    
    # 4. 检查 OpenClaw
    oc = run_cmd('openclaw --version', check=False)
    checks.append(('OpenClaw', oc and 'openclaw' in oc.lower(), oc or '未安装'))
    
    # 5. 检查 .env
    dotenv = os.path.join(DOCKER_DIR, '.env')
    env_exists = os.path.isfile(dotenv)
    checks.append(('.env 配置', env_exists, '存在' if env_exists else '不存在(从 .env.example 复制)'))
    
    # 6. 检查 Cloudflare
    cf_token = os.environ.get('CF_TUNNEL_TOKEN', '')
    checks.append(('Cloudflare Token', bool(cf_token), '已配置' if cf_token else '未配置'))
    
    # 7. 检查 Gateway Token
    gw_token = os.environ.get('OPENCLAW_GATEWAY_TOKEN', '')
    gw_ok = bool(gw_token) and gw_token != 'change-me-to-a-random-secure-token'
    checks.append(('Gateway Token', gw_ok, 'OK' if gw_ok else '请配置'))
    
    # 打印结果
    for name, ok, detail in checks:
        icon = GREEN + '[OK]' + RESET if ok else RED + '[ERR]' + RESET
        print(f'  {icon} {name:<25} {detail}')
    
    pass_count = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    print(f'\n 通过: {pass_count}/{total}')
    return pass_count == total

def deploy_docker():
    """部署 Docker Compose"""
    print(f'\n{"="*60}')
    print(f' IGP Infrastructure — Docker Compose 部署')
    print(f'{"="*60}\n')
    
    os.chdir(DOCKER_DIR)
    
    # 1. 检查 .env
    dotenv = os.path.join(DOCKER_DIR, '.env')
    if not os.path.isfile(dotenv):
        log_err('.env 不存在，请从 .env.example 复制')
        log_info(f'cp {DOCKER_DIR}\\.env.example {dotenv}')
        return False
    
    # 2. 创建必要目录
    for d in ['data/gateway', 'data/igp', 'config', 'workspace']:
        os.makedirs(os.path.join(DOCKER_DIR, d), exist_ok=True)
    log_ok('数据目录已创建')
    
    # 3. 拉取镜像
    log_info('拉取 Docker 镜像...')
    run_cmd('docker compose pull', timeout=120)
    
    # 4. 启动服务
    log_info('启动服务...')
    result = run_cmd('docker compose up -d', timeout=60)
    if result is None:
        log_err('Docker Compose 启动失败')
        return False
    
    # 5. 检查服务状态
    log_info('检查服务状态...')
    status = run_cmd('docker compose ps', timeout=10)
    if status:
        print(status)
    
    log_ok('Docker Compose 部署完成')
    log_info(f'Gateway: http://localhost:18791')
    log_info(f'IGP API: http://localhost:8080')
    return True

def deploy_gateway():
    """部署多 Gateway"""
    print(f'\n{"="*60}')
    print(f' IGP Infrastructure — 多 Gateway 部署')
    print(f'{"="*60}\n')
    
    log_info('方案 A: Docker Compose（推荐）')
    log_info('  见 docker-compose.yml 中多 gateway 服务')
    log_info('  启动: docker compose --profile full up -d')
    
    log_info('\n方案 B: 原生进程')
    log_info('  启动命令:')
    print(f'    openclaw --profile main --port 18791 gateway start')
    print(f'    openclaw --profile ops --port 19789 gateway start')
    print(f'    openclaw --profile rescue --port 20789 gateway start')
    
    log_info('\n方案 C: 远程部署')
    for gw, port, loc in [
        ('ops', 19789, '阿里云'),
        ('enterprise', 22789, '公司服务器'),
        ('rescue', 20789, 'Mac Mini/树莓派'),
    ]:
        print(f'    {loc} → openclaw --profile {gw} --port {port} gateway')
    
    return True

def deploy_tunnel():
    """配置 Cloudflare Tunnel"""
    print(f'\n{"="*60}')
    print(f' IGP Infrastructure — Cloudflare Tunnel')
    print(f'{"="*60}\n')
    
    log_info('步骤:')
    print('\n  1. 登录 Cloudflare Dashboard:')
    print('     https://one.dash.cloudflare.com/ → Zero Trust → Networks → Tunnels')
    print('\n  2. 创建 Tunnel')
    print('     Name: igp-tunnel')
    print('\n  3. 复制 Token (eyJ...), 写入 .env:')
    print('     CF_TUNNEL_TOKEN=eyJhIjoi...')
    print('\n  4. 启动 cloudflared:')
    print('     docker compose up -d cloudflared')
    print('\n  5. 配置路由 (先配 Access, 再连域名):')
    print('     Subdomain: igp')
    print('     Domain: yourdomain.com')
    print('     Service: http://localhost:18791')
    print('\n  6. 配置 Access:')
    print('     Zero Trust → Access → Applications → Add')
    print('     Domain: igp.yourdomain.com')
    print('     Policy: Allow → Email OTP')
    
    return True

def show_status():
    """查看所有服务状态"""
    print(f'\n{"="*60}')
    print(f' IGP Infrastructure — 服务状态')
    print(f'{"="*60}\n')
    
    os.chdir(DOCKER_DIR)
    status = run_cmd('docker compose ps', check=False, timeout=10)
    if status:
        print(' Docker 服务:')
        print(status)
    else:
        log_warn('Docker 未运行或 docker-compose.yml 不存在')
    
    # 检查端口
    log_info('\n端口检查:')
    for port, name in [('18791', 'Gateway'), ('8080', 'IGP API'), ('19789', 'Ops GW'), ('20789', 'Rescue GW')]:
        r = run_cmd(f'netstat -an | findstr ":{port}"', check=False, timeout=5)
        if r:
            log_ok(f'{name} (:{port}) 运行中')
        else:
            log_warn(f'{name} (:{port}) 未检测到')

def doctor():
    """全链路诊断"""
    print(f'\n{"="*60}')
    print(f' IGP Infrastructure — 全链路诊断')
    print(f'{"="*60}\n')
    
    # 1. 环境检查
    all_ok = check_prerequisites()
    
    # 2. API 健康检查
    print(f'\n API 健康检查:')
    r = run_cmd('python -c "import urllib.request; print(urllib.request.urlopen(\'http://localhost:8080/health\', timeout=5).read().decode())"',
                check=False, timeout=10)
    if r:
        log_ok(f'IGP API: {r[:100]}')
    else:
        log_warn('IGP API 不可达')
    
    # 3. Gateway 检查
    print(f'\n Gateway 检查:')
    r = run_cmd('python -c "import urllib.request; print(urllib.request.urlopen(\'http://localhost:18791/health\', timeout=5).read().decode())"',
                check=False, timeout=10)
    if r:
        log_ok(f'Gateway: {r[:100]}')
    else:
        log_warn('Gateway 不可达（可能是端口18791的HTTP模式）')
    
    print()
    if all_ok:
        log_ok('全链路诊断通过')
    else:
        log_warn('部分检查未通过，请查看上方详情')

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    commands = {
        'init': check_prerequisites,
        'docker': deploy_docker,
        'gateway': deploy_gateway,
        'tunnel': deploy_tunnel,
        'status': show_status,
        'doctor': doctor,
    }
    
    fn = commands.get(cmd)
    if not fn:
        log_err(f'未知命令: {cmd}')
        print(f'可用命令: init, docker, gateway, tunnel, status, doctor')
        return
    
    success = fn()
    sys.exit(0 if success is not False else 1)

if __name__ == '__main__':
    main()
