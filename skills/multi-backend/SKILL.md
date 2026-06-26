---
name: multi-backend
description: Multi-backend Claude Code routing — cdsp (Anthropic native, Max plan quota) + odsp (OpenRouter, any model paid or free). PowerShell helpers cdsp / odsp / odsp-models / dsp-status / dsp-reset. Supports single-tier and multi-tier modes for richer in-session /model picker. Reference for /orni-init-mb and /orni-update-mb.
version: 1.1.0
---

# Multi-Backend Claude Code

Routes Claude Code via two interchangeable backends depending on per-launch needs :
- **`cdsp`** — Anthropic native (Max plan quota, Sonnet/Opus/Haiku)
- **`odsp`** — OpenRouter unified gateway (any model, paid or free)

Designed for **autonomous /loop sessions** that would otherwise burn the Anthropic Max plan quota in hours. Switch to `odsp` for mechanical refactors / scraping / boilerplate generation, keep `cdsp` for high-quality work.

---

## 1. Architecture

Claude Code resolves model selection through **tier env vars** (NOT `ANTHROPIC_MODEL` alone). The skill sets all four tier vars to the same OpenRouter model so Claude Code's internal opus/sonnet/haiku/subagent logic always lands on the chosen target.

| Env var | Purpose |
|---|---|
| `ANTHROPIC_BASE_URL` | API endpoint. `https://openrouter.ai/api` for OR (NOT `/api/v1` — Anthropic SDK appends `/v1/messages` itself). |
| `ANTHROPIC_AUTH_TOKEN` | Bearer token. OR API key for odsp. |
| `ANTHROPIC_API_KEY` | Must be **empty string** (not unset) to prevent CC from prompting Anthropic login. PS `$env:X = ""` actually unsets — use `[Environment]::SetEnvironmentVariable(...,'',('Process'))`. |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Tier override (opus). |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Tier override (sonnet). |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Tier override (haiku). |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Tier override (subagents). |

Reference : https://openrouter.ai/docs/guides/coding-agents/claude-code-integration

---

## 2. Files installed

| Path | Type | Purpose |
|---|---|---|
| `$PROFILE` (PowerShell profile) | Block injected | cdsp / odsp / odsp-models / dsp-status / dsp-reset functions |
| `~/.claude/backend_keys.json` | Created from template | Stores `openrouter_key` (NEVER commit) |
| `~/.claude/backend_keys.json.template` | Reference | Template with placeholders |

The PowerShell profile path varies per host :
- pwsh 7 (default Documents) : `~/Documents/PowerShell/Microsoft.PowerShell_profile.ps1`
- pwsh 7 (OneDrive Documents redirection) : `~/OneDrive/Documents/PowerShell/Microsoft.PowerShell_profile.ps1`
- Windows PowerShell 5.1 : `~/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1` (or OneDrive variant)

**Always inspect `$PROFILE` in the user's actual shell** — installing to the wrong path is the #1 failure mode. See `INSTALL.md` for path-detection logic.

---

## 3. Usage

### cdsp — Anthropic native

```powershell
cdsp                              # Launch CC with Max plan / Sonnet default
cdsp <claude-args>                # Pass any args through
```

Clears all backend env vars first, so it always reverts to native Anthropic.

### odsp — OpenRouter

**Single-tier mode** (one model on all CC tiers — `/model` picker shows 1 choice) :

```powershell
odsp                              # default model (deepseek-pro)
odsp <alias>                      # alias model (see odsp-models)
odsp provider/model[:tag]         # full OR model ID (any catalog model)
odsp <model> -p "prompt" --output-format json   # non-interactive print mode
```

**Multi-tier mode** (different models per tier — `/model` picker shows 3-4 choices, switchable mid-session) :

```powershell
odsp <opus>,<sonnet>,<haiku>           # 3 tiers, subagent = sonnet
odsp <opus>,<sonnet>,<haiku>,<sub>     # 4 tiers explicit
```

Examples :
```powershell
odsp deepseek,deepseek-flash,free                # quality / fast / free fallback
odsp deepseek-pro,glm-flash,qwen-coder           # premium / mid / coding
odsp deepseek,deepseek-flash,free,deepseek-flash # same plus explicit subagent
```

In session : `/model` opens the picker, switch between opus / sonnet / haiku without relaunching.

**Inline override** : type `/model provider/model:tag` in-session to use ANY OR model (not just configured tiers). Bypasses the picker entirely — works because CC accepts arbitrary model strings when `ANTHROPIC_BASE_URL` points to a compatible API.

### odsp-models — alias catalogue

```powershell
odsp-models                       # Print all known aliases
```

### dsp-status / dsp-reset — inspection

```powershell
dsp-status                        # Print current backend env vars
dsp-reset                         # Clear all backend env vars (cdsp clean state)
```

---

## 4. Alias catalogue

### Paid

| Alias | Model |
|---|---|
| `deepseek` / `deepseek-pro` | `deepseek/deepseek-v4-pro` |
| `deepseek-flash` | `deepseek/deepseek-v4-flash` |
| `deepseek-v3.2` | `deepseek/deepseek-v3.2` |
| `mimo` / `mimo-pro` | `xiaomi/mimo-v2.5-pro` |
| `mimo-std` | `xiaomi/mimo-v2.5` |
| `glm` | `z-ai/glm-4.7` |
| `glm-flash` | `z-ai/glm-4.7-flash` |
| `glm-5` | `z-ai/glm-5` |
| `glm-5-turbo` | `z-ai/glm-5-turbo` |

### Free (rate-limited)

| Alias | Model |
|---|---|
| `free` / `hy3` | `tencent/hy3-preview:free` |
| `qwen-coder` | `qwen/qwen3-coder:free` |
| `qwen` | `qwen/qwen3-next-80b-a3b-instruct:free` |
| `gpt-oss` | `openai/gpt-oss-120b:free` |
| `gpt-oss-20b` | `openai/gpt-oss-20b:free` |
| `llama` | `meta-llama/llama-3.3-70b-instruct:free` |
| `nemotron` | `nvidia/nemotron-3-super-120b-a12b:free` |
| `nemotron-reason` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` |
| `minimax` | `minimax/minimax-m2.5:free` |
| `ling` | `inclusionai/ling-2.6-1t:free` |
| `glm-air-free` | `z-ai/glm-4.5-air:free` |

### Custom

```powershell
odsp provider/model[:tag]         # Any OR catalog model
```

Live catalogue : https://openrouter.ai/models

---

## 5. Verification (post-install)

```powershell
. $PROFILE
Get-Command odsp-models           # Must return a Function
dsp-status                        # Must print empty env vars + Keys file exists : True
odsp deepseek-flash -p "say hi" --output-format json  # Must succeed, modelUsage=deepseek/deepseek-v4-flash
```

---

## 6. Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `odsp-models : not recognized` after `. $PROFILE` | OneDrive Documents redirection — `$PROFILE` points to `~/OneDrive/Documents/PowerShell/...` but install touched `~/Documents/PowerShell/...` | Detect actual `$PROFILE` path **inside** user's shell, write there. See INSTALL.md §2. |
| `odsp <alias>` → 400 "alias is not a valid model ID" | Stale function in shell memory. Profile on disk is fine, but the running pwsh has the old version cached. | User must `. $PROFILE` again, or close + reopen shell. |
| `Routing CC tiers -> OR model: <alias-not-mapped>` | Old profile version (pre-1.0.0) without `_orResolveModel`. | Re-run `/orni-update-mb`. |
| 400 with "deepseek is not a valid model ID" while using full ID | Only `ANTHROPIC_MODEL` is set, not the tier vars. CC strips to first segment. | Verify tier vars set : `dsp-status`. |
| 401 "Invalid API key" | `openrouter_key` empty / wrong / not in `~/.claude/backend_keys.json`. | Edit keys file, key must start with `sk-or-`. |
| 429 on free models | OR rate limits free tier per minute and per day. | Wait 60s or switch alias. |
| `cdsp` still asks for Anthropic login | `ANTHROPIC_API_KEY` got unset (instead of empty string). | Run `dsp-reset` then `cdsp` (the reset is safe). For diagnosis, `dsp-status` shows `<unset>` vs `'' (len=0)`. |

---

## 7. Why shell profile (not settings.json env)

`~/.claude/settings.json` supports an `env` block that propagates env vars into Claude Code's process. That approach is simpler for **single-backend** setups but locks the entire system to one backend at a time.

Shell profile retains **per-launch switching** : `cdsp` for Max plan quota, `odsp <alias>` for OR. Both cohabit. Switching = type a different command, no file edit.

If a user only ever wants OR, the settings.json approach is acceptable — but this skill does not configure it. See https://openrouter.ai/docs/guides/coding-agents/claude-code-integration for that path.

---

## 8. Report format (for /orni-init-mb and /orni-update-mb)

```
## Multi-Backend Claude Code — install/update

| Component | Status |
|---|---|
| PowerShell profile | <path> ({injected | already present}) |
| backend_keys.json | <created from template | already present | needs OR key> |
| Functions loaded | cdsp ✓ odsp ✓ odsp-models ✓ dsp-status ✓ dsp-reset ✓ |

**Next steps:**
- Open a NEW pwsh window (or `. $PROFILE` in current).
- If `~/.claude/backend_keys.json` was just created : edit it and paste your OR key (https://openrouter.ai/keys).
- Test : `odsp-models` → must list aliases. `odsp deepseek -p "hi"` → must succeed.
```
