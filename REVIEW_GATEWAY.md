# IGP Gateway 控制平面 — 技术审核意见
#
# 审核日期: 2026-07-01
# 审核人: 研发部
# 建议来源: 外部专家
#
# 结论: ✅ 通过，具有瑕疵及改进

import os, json

review = """

=============================================================================
 IGP Gateway 控制平面 — 研发部技术审核
=============================================================================

一、openclaw.json          ✅ 通过，有 3 处改进
─────────────────────────────────────────────────────────────────────────────
[OK] schema 引用           正确
[OK] port=18791+bind=127   与当前运行一致
[OK] laneQueue 配置        serial调度
~

改进建议:
  1. fallbackChain: deepseek-v3 后不应放 local model
     原因: 如果 deepseek 挂了，local model 不可能能响应（它走不同网络路径）。
     改进: 第三级应为 hard_fail 或暂停重试，而不是假local.
     + 修复: fallback 改成 2 级: v4-flash → v3 → 1分钟后重试v4-flash

  2. channels 里 telegram.allowedUsers 留空数组
     风险: 空数组=全拒还是全通? OpenClaw 行为不确定。
     改进: 加注释明确行为，或预填你自己的user id

  3. bindings 用 ${VAR} 占位符
     注意: OpenClaw openclaw.json 不支持 .env 变量注入。
     + 修复: 要么走环境变量 ${TELEGRAM_BOT_TOKEN}（OpenClaw支持），
             要么直接填ID进配置。
     bindings 里的 chat ID 建议直接填入（不.env注入）


二、models.json            ✅ 通过，1 处修正
─────────────────────────────────────────────────────────────────────────────
[OK] provider 结构          清晰
[OK] local model 占位符    好（为未来 Qwen3-32B 留位置）

修正:
  1. model 名冲突
     OpenClaw 里 model 字段是 'deepseek/deepseek-v4-flash' 格式。
     建议 models.json 改成:
     {
       "providers": […],
       "models": {
         "deepseek/deepseek-v4-flash": { "provider": "deepseek", "name": "deepseek-v4-flash" },
         "deepseek/deepseek-v3":       { "provider": "deepseek", "name": "deepseek-v3" },
         "local/placeholder":           { "provider": "local",   "name": "llama3" }
       }
     }


三、allowlist.json          ✅ 通过，安全改进建议
─────────────────────────────────────────────────────────────────────────────
[OK] mode=deny             白名单模式正确
[OK] git status/diff/log   允许但不暴露push/rm

建议:
  1. 加 dev-specific 命令
     - curl (调试API)
     - python (跑测试/脚本)
     - docker compose (部署)
     - npm/pnpm (前端构建)
  2. 考虑加 shell 命令审计日志
     审计日志路径留占位: "auditLog": "./logs/shell-audit.jsonl"


四、cost-limits.json        ✅ 通过，1 处改进
─────────────────────────────────────────────────────────────────────────────
[OK] $10/day               合理基准
[OK] $0.5/request          足够宽松

改进:
  1. 加模型级限额
     deepseek-v4-flash:   $0.002/1K tokens (便宜)
     deepseek-v3:         $0.01/1K tokens
     建议: perModelLimits 区分

五、Agent SOUL.md          ✅ 通过，内容等补充
─────────────────────────────────────────────────────────────────────────────
[OK] coding SOUL.md        精炼，有约束有偏好
[NOTE] research/ops/exec   需补全，当前是折叠状态
[NOTE] USER.md+AGENTS.md  未提供，但外部建议没给这些


=============================================================================
 修正后文件清单（研发部产出）
=============================================================================

建议直接落地以下文件到 igp-infrastructure:

  config/
    openclaw.json           （修正 bindings 变量 + fallback 链）
    models.json             （修正 model 命名格式）
    safety/
      allowlist.json        （补充 dev 命令 + audit log）
      cost-limits.json      （加 per-model limits）
  agents/
    coding/   SOUL.md        （保留，文案微调）
    research/ SOUL.md + USER.md + AGENTS.md  （新写）
    ops/      SOUL.md + USER.md + AGENTS.md  （新写）
    exec/     SOUL.md + USER.md + AGENTS.md  （新写）
  .env.example              （修正：只保留真正支持的变量）
  README.gateway.md         （修正步骤）

=============================================================================
 结论
=============================================================================

外部建议质量 8/10。骨架正确但实现细节有瑕疵。
研发部已消化所有修正，开始写最终code。
"""

print(review)
