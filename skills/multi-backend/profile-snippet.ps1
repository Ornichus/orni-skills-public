# ─── Orni Multi-Backend Claude Code ─────────────────────────────────────────
# DO NOT EDIT THIS BLOCK MANUALLY — managed by /orni-init-mb and /orni-update-mb.
# Source: skills/multi-backend/profile-snippet.ps1 (Orni-Skills)
# Per OR docs: https://openrouter.ai/docs/guides/coding-agents/claude-code-integration
# Functions: cdsp / odsp / odsp-models / dsp-status / dsp-reset
# Block markers: # ORNI-MB-START / # ORNI-MB-END
# ORNI-MB-START v1.1.0

function _ccGetKey([string]$name) {
    $f = Join-Path $env:USERPROFILE ".claude\backend_keys.json"
    if (-not (Test-Path $f)) { return $null }
    $j = Get-Content $f -Raw | ConvertFrom-Json
    return $j.$name
}

# OR alias -> real model ID. Edit via /orni-update-mb to refresh from upstream.
$global:_OR_ALIASES = @{
    # Paid — DeepSeek
    "deepseek"        = "deepseek/deepseek-v4-pro"
    "deepseek-pro"    = "deepseek/deepseek-v4-pro"
    "deepseek-flash"  = "deepseek/deepseek-v4-flash"
    "deepseek-v3.2"   = "deepseek/deepseek-v3.2"
    # Paid — Mimo (Xiaomi)
    "mimo"            = "xiaomi/mimo-v2.5-pro"
    "mimo-pro"        = "xiaomi/mimo-v2.5-pro"
    "mimo-std"        = "xiaomi/mimo-v2.5"
    # Paid — GLM (Z.AI)
    "glm"             = "z-ai/glm-4.7"
    "glm-flash"       = "z-ai/glm-4.7-flash"
    "glm-5"           = "z-ai/glm-5"
    "glm-5-turbo"     = "z-ai/glm-5-turbo"
    # Free — handpicked best-for-coding (subject to OR rate limits)
    "free"            = "tencent/hy3-preview:free"
    "hy3"             = "tencent/hy3-preview:free"
    "qwen-coder"      = "qwen/qwen3-coder:free"
    "qwen"            = "qwen/qwen3-next-80b-a3b-instruct:free"
    "gpt-oss"         = "openai/gpt-oss-120b:free"
    "gpt-oss-20b"     = "openai/gpt-oss-20b:free"
    "llama"           = "meta-llama/llama-3.3-70b-instruct:free"
    "nemotron"        = "nvidia/nemotron-3-super-120b-a12b:free"
    "nemotron-reason" = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
    "minimax"         = "minimax/minimax-m2.5:free"
    "ling"            = "inclusionai/ling-2.6-1t:free"
    "glm-air-free"    = "z-ai/glm-4.5-air:free"
}

# Resolve user input -> full OR model ID. Accepts alias OR full provider/model[:tag].
function _orResolveModel([string]$idOrAlias) {
    if ([string]::IsNullOrWhiteSpace($idOrAlias)) { return $null }
    if ($global:_OR_ALIASES.ContainsKey($idOrAlias)) { return $global:_OR_ALIASES[$idOrAlias] }
    if ($idOrAlias -match "^[a-zA-Z0-9._-]+/[a-zA-Z0-9._:-]+$") { return $idOrAlias }
    return $null
}

# cdsp — Anthropic native. Use Max plan quota. Pick model with /model in session.
function cdsp {
    dsp-reset | Out-Null
    & claude --dangerously-skip-permissions @args
}

# odsp — OpenRouter. Routes Claude Code tiers to OR models.
# Usage:
#   odsp                              -> default (deepseek-pro on all tiers)
#   odsp <alias>                      -> all tiers on one model
#   odsp <opus>,<sonnet>,<haiku>      -> 3 tiers / 3 models (visible in /model picker)
#   odsp <opus>,<sonnet>,<haiku>,<subagent>   -> 4 tiers / 4 models
#   odsp provider/model[:tag]         -> any OR catalog model on all tiers
function odsp {
    # No [CmdletBinding] — would intercept -p / -v as common params.
    $key = _ccGetKey "openrouter_key"
    if (-not $key) { Write-Error "Missing openrouter_key in ~/.claude/backend_keys.json"; return }

    if ($args.Count -gt 0) {
        $first = [string]$args[0]
        if ($first.StartsWith("-")) {
            $ModelArg = "deepseek"
            $Rest = $args
        } else {
            $ModelArg = $first
            $Rest = if ($args.Count -gt 1) { $args[1..($args.Count-1)] } else { @() }
        }
    } else {
        $ModelArg = "deepseek"
        $Rest = @()
    }

    # Multi-tier mode: comma-separated aliases (opus,sonnet,haiku[,subagent])
    if ($ModelArg.Contains(',')) {
        $parts = $ModelArg.Split(',') | ForEach-Object { $_.Trim() }
        if ($parts.Count -lt 2 -or $parts.Count -gt 4) {
            Write-Error "Multi-tier mode needs 2-4 comma-separated aliases. Got: $ModelArg"
            return
        }
        $opusModel    = _orResolveModel $parts[0]
        $sonnetModel  = _orResolveModel $parts[1]
        $haikuModel   = if ($parts.Count -ge 3) { _orResolveModel $parts[2] } else { $sonnetModel }
        $subagentModel = if ($parts.Count -eq 4) { _orResolveModel $parts[3] } else { $sonnetModel }

        $unresolved = @()
        if (-not $opusModel)    { $unresolved += "opus=$($parts[0])" }
        if (-not $sonnetModel)  { $unresolved += "sonnet=$($parts[1])" }
        if ($parts.Count -ge 3 -and -not $haikuModel)    { $unresolved += "haiku=$($parts[2])" }
        if ($parts.Count -eq 4 -and -not $subagentModel) { $unresolved += "subagent=$($parts[3])" }
        if ($unresolved.Count -gt 0) {
            Write-Error "Unresolved alias(es): $($unresolved -join ', '). Run odsp-models for catalogue."
            return
        }

        [Environment]::SetEnvironmentVariable('ANTHROPIC_BASE_URL',  'https://openrouter.ai/api', 'Process')
        [Environment]::SetEnvironmentVariable('ANTHROPIC_AUTH_TOKEN', $key, 'Process')
        [Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY',   '',   'Process')
        [Environment]::SetEnvironmentVariable('ANTHROPIC_MODEL',     $null, 'Process')
        [Environment]::SetEnvironmentVariable('ANTHROPIC_DEFAULT_OPUS_MODEL',   $opusModel,    'Process')
        [Environment]::SetEnvironmentVariable('ANTHROPIC_DEFAULT_SONNET_MODEL', $sonnetModel,  'Process')
        [Environment]::SetEnvironmentVariable('ANTHROPIC_DEFAULT_HAIKU_MODEL',  $haikuModel,   'Process')
        [Environment]::SetEnvironmentVariable('CLAUDE_CODE_SUBAGENT_MODEL',     $subagentModel,'Process')

        Write-Host "Routing CC tiers -> OR multi-tier:" -ForegroundColor Cyan
        Write-Host "  opus     : $opusModel"     -ForegroundColor Cyan
        Write-Host "  sonnet   : $sonnetModel"   -ForegroundColor Cyan
        Write-Host "  haiku    : $haikuModel"    -ForegroundColor Cyan
        Write-Host "  subagent : $subagentModel" -ForegroundColor Cyan
        Write-Host "Use /model in session to switch between opus/sonnet/haiku." -ForegroundColor Yellow
        & claude --dangerously-skip-permissions @Rest
        return
    }

    # Single-tier mode: same model for all 4 tiers
    $model = _orResolveModel $ModelArg
    if (-not $model) {
        Write-Error "Unknown alias and not a valid model ID: '$ModelArg'. Run odsp-models for catalogue."
        return
    }

    [Environment]::SetEnvironmentVariable('ANTHROPIC_BASE_URL',  'https://openrouter.ai/api', 'Process')
    [Environment]::SetEnvironmentVariable('ANTHROPIC_AUTH_TOKEN', $key, 'Process')
    [Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY',   '',   'Process')
    [Environment]::SetEnvironmentVariable('ANTHROPIC_MODEL',     $null, 'Process')
    [Environment]::SetEnvironmentVariable('ANTHROPIC_DEFAULT_OPUS_MODEL',   $model, 'Process')
    [Environment]::SetEnvironmentVariable('ANTHROPIC_DEFAULT_SONNET_MODEL', $model, 'Process')
    [Environment]::SetEnvironmentVariable('ANTHROPIC_DEFAULT_HAIKU_MODEL',  $model, 'Process')
    [Environment]::SetEnvironmentVariable('CLAUDE_CODE_SUBAGENT_MODEL',     $model, 'Process')

    Write-Host "Routing CC tiers -> OR model: $model" -ForegroundColor Cyan
    & claude --dangerously-skip-permissions @Rest
}

function odsp-models {
    Write-Host "PAID — DeepSeek:"
    Write-Host "  deepseek / deepseek-pro    -> deepseek/deepseek-v4-pro"
    Write-Host "  deepseek-flash             -> deepseek/deepseek-v4-flash"
    Write-Host "  deepseek-v3.2              -> deepseek/deepseek-v3.2"
    Write-Host "PAID — Mimo (Xiaomi):"
    Write-Host "  mimo / mimo-pro            -> xiaomi/mimo-v2.5-pro"
    Write-Host "  mimo-std                   -> xiaomi/mimo-v2.5"
    Write-Host "PAID — GLM (Z.AI):"
    Write-Host "  glm                        -> z-ai/glm-4.7"
    Write-Host "  glm-flash                  -> z-ai/glm-4.7-flash"
    Write-Host "  glm-5 / glm-5-turbo        -> z-ai/glm-5(-turbo)"
    Write-Host "FREE (rate-limited):"
    Write-Host "  free / hy3                 -> tencent/hy3-preview:free"
    Write-Host "  qwen-coder                 -> qwen/qwen3-coder:free"
    Write-Host "  qwen                       -> qwen/qwen3-next-80b-a3b-instruct:free"
    Write-Host "  gpt-oss / gpt-oss-20b      -> openai/gpt-oss-120b(-20b):free"
    Write-Host "  llama                      -> meta-llama/llama-3.3-70b-instruct:free"
    Write-Host "  nemotron / nemotron-reason -> nvidia/nemotron-3-super-120b / nano-omni-reasoning:free"
    Write-Host "  minimax                    -> minimax/minimax-m2.5:free"
    Write-Host "  ling                       -> inclusionai/ling-2.6-1t:free"
    Write-Host "  glm-air-free               -> z-ai/glm-4.5-air:free"
    Write-Host ""
    Write-Host "USAGE:"
    Write-Host "  odsp <alias>               -> single-tier (all CC tiers on one model)"
    Write-Host "  odsp provider/model:tag    -> single-tier, any OR model ID"
    Write-Host "  odsp                       -> single-tier, default deepseek-pro"
    Write-Host "  odsp <a>,<b>,<c>           -> multi-tier (opus,sonnet,haiku) — /model picker shows 3 choices"
    Write-Host "  odsp <a>,<b>,<c>,<d>       -> multi-tier with subagent override"
    Write-Host ""
    Write-Host "Multi-tier examples:"
    Write-Host "  odsp deepseek,deepseek-flash,free   # quality / fast / free fallback"
    Write-Host "  odsp deepseek-pro,glm-flash,qwen-coder   # premium / mid / coding"
    Write-Host ""
    Write-Host "Full OR catalogue: https://openrouter.ai/models"
    Write-Host "Tip: in session, type '/model provider/model:tag' to use ANY OR model on the fly."
}

function dsp-status {
    $apiKey = [Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY','Process')
    Write-Host "ANTHROPIC_BASE_URL         : $($env:ANTHROPIC_BASE_URL)"
    Write-Host "ANTHROPIC_AUTH_TOKEN       : $(if ($env:ANTHROPIC_AUTH_TOKEN) { '<set>' } else { '<unset>' })"
    Write-Host "ANTHROPIC_API_KEY          : $(if ($null -eq $apiKey) { '<unset>' } else { "'$apiKey' (len=$($apiKey.Length))" })"
    Write-Host "ANTHROPIC_MODEL            : $($env:ANTHROPIC_MODEL)"
    Write-Host "ANTHROPIC_DEFAULT_OPUS     : $($env:ANTHROPIC_DEFAULT_OPUS_MODEL)"
    Write-Host "ANTHROPIC_DEFAULT_SONNET   : $($env:ANTHROPIC_DEFAULT_SONNET_MODEL)"
    Write-Host "ANTHROPIC_DEFAULT_HAIKU    : $($env:ANTHROPIC_DEFAULT_HAIKU_MODEL)"
    Write-Host "CLAUDE_CODE_SUBAGENT_MODEL : $($env:CLAUDE_CODE_SUBAGENT_MODEL)"
    $f = Join-Path $env:USERPROFILE ".claude\backend_keys.json"
    Write-Host "Keys file exists           : $(Test-Path $f)"
}

function dsp-reset {
    Remove-Item Env:ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_DEFAULT_OPUS_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_DEFAULT_SONNET_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_DEFAULT_HAIKU_MODEL -ErrorAction SilentlyContinue
    Remove-Item Env:CLAUDE_CODE_SUBAGENT_MODEL -ErrorAction SilentlyContinue
    Write-Host "Backend env vars cleared. cdsp will use Anthropic native."
}

# ORNI-MB-END
