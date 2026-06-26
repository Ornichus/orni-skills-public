# Multi-Backend — Installation Guide for Agents

This is the step-by-step procedure an agent must follow when running `/orni-init-mb` or `/orni-update-mb`. It encodes the lessons learned from the v1.0.0 install (notably the OneDrive Documents redirection trap).

---

## 1. Pre-flight

1. Confirm OS = Windows. The skill is PowerShell-only (Windows). Reject macOS/Linux with a message :
   *"Multi-backend currently supports only PowerShell on Windows. Bash equivalents are not yet shipped."*
2. Confirm `claude` CLI is on PATH : `Get-Command claude -ErrorAction SilentlyContinue`. If not found : abort with install instructions.
3. Confirm the source repo `{ORNI}` exists and contains `skills/multi-backend/profile-snippet.ps1`.

---

## 2. Detect the **real** PowerShell profile path

**This is the #1 install failure mode.** When OneDrive Documents sync is enabled (very common on Windows 10/11), `~/Documents` is redirected to `~/OneDrive/Documents`. Both paths may exist as physically distinct directories — only one is what `$PROFILE` actually resolves to.

**You MUST query `$PROFILE` from inside the user's pwsh, not infer from filesystem layout.**

Use the following PowerShell snippet (executed via the Bash tool calling `pwsh -NoProfile -Command ...` to keep the user's loaded profile from masking the test):

```powershell
pwsh -NoProfile -Command "@{
  pwsh7_current_user_current_host = \$PROFILE
  pwsh7_all_users_current_host    = \$PROFILE.AllUsersCurrentHost
} | ConvertTo-Json"
```

Pick `pwsh7_current_user_current_host` as the canonical install target. Record it as `$PROFILE_PATH`.

If pwsh 7 is absent (only `powershell.exe` 5.1 available), fall back to :

```powershell
powershell -NoProfile -Command "\$PROFILE"
```

That returns `~/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1` (or OneDrive variant).

**Optional — also install for Win PS 5.1** : if the user uses both pwsh 7 and Windows PowerShell 5.1, ask whether to install for both. Default : pwsh 7 only.

---

## 3. Install / Update logic

### 3a. Idempotent block injection

The profile snippet is wrapped in marker comments :

```powershell
# ORNI-MB-START v1.0.0
... functions ...
# ORNI-MB-END
```

Procedure :

1. **Read** `$PROFILE_PATH`. If absent, create empty file and parent directory : `New-Item -ItemType File -Path $PROFILE_PATH -Force`.
2. **Search** for `# ORNI-MB-START` in the existing content.
3. **If marker found** (update path) :
   - Find matching `# ORNI-MB-END`. If absent, abort with error : *"corrupted profile — manual cleanup required"*.
   - Replace the entire block (from `# ORNI-MB-START` through `# ORNI-MB-END` inclusive) with the new snippet from `{ORNI}/skills/multi-backend/profile-snippet.ps1`.
4. **If marker absent** (init path) :
   - Append a blank line + the full snippet to the end of `$PROFILE_PATH`.
5. **Verify** the resulting file parses without errors :

```powershell
$tokens = $null; $errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PROFILE_PATH, [ref]$tokens, [ref]$errors) | Out-Null
if ($errors.Count -gt 0) { throw "Profile parse errors: $($errors | ConvertTo-Json)" }
```

### 3b. Backend keys file

1. **Source template** : `{ORNI}/skills/multi-backend/backend_keys.json.template`
2. **Target** : `~/.claude/backend_keys.json`
3. **Logic** :
   - If target absent : copy template.
   - If target present : leave untouched (preserves the real key the user already pasted).
4. **Always copy the template itself** to `~/.claude/backend_keys.json.template` for reference.

Print a clear next-step message :

> Edit `~/.claude/backend_keys.json` and replace `sk-or-v1-REPLACE_WITH_YOUR_OPENROUTER_API_KEY` with your OpenRouter key. Get one at https://openrouter.ai/keys.

---

## 4. Post-install verification

Run the following and ensure all checks pass (output to user only on failure for noise reduction) :

```powershell
pwsh -NoProfile -Command @'
  . "<PROFILE_PATH>"
  $functions = @('cdsp','odsp','odsp-models','dsp-status','dsp-reset','_orResolveModel','_ccGetKey')
  $missing = @()
  foreach ($f in $functions) {
    if (-not (Get-Command $f -ErrorAction SilentlyContinue)) { $missing += $f }
  }
  if ($missing.Count -gt 0) {
    Write-Error "Missing functions after install: $($missing -join ', ')"
    exit 1
  }
  if (-not (Test-Path "$env:USERPROFILE\.claude\backend_keys.json")) {
    Write-Error "backend_keys.json missing"
    exit 1
  }
  Write-Host "OK"
'@
```

Substitute `<PROFILE_PATH>` with the actual path detected in §2.

---

## 5. Common pitfalls (must check)

| Pitfall | Detection | Mitigation |
|---|---|---|
| OneDrive Documents redirection | `$PROFILE` resolves under `~/OneDrive/Documents/...` while `~/Documents/PowerShell/...` ALSO exists with stale content | Always trust `$PROFILE` from the user's shell. Optionally clean up the orphan path. |
| Stale shell session after install | Functions defined on disk but not in user's running pwsh | Tell user explicitly : "Close current pwsh and open a new one, OR run `. $PROFILE`." |
| `$env:ANTHROPIC_API_KEY = ""` unsets variable | PowerShell quirk : empty string assignment via `$env:` deletes the variable | Snippet uses `[Environment]::SetEnvironmentVariable(...,'',('Process'))` already. Do not edit by hand. |
| Old broken aliases with date suffix | Pre-1.0.0 profiles had IDs like `deepseek/deepseek-v4-pro-20260423` | Update path replaces the entire block, eliminating drift. |
| Both pwsh 7 and PS 5.1 in use | User runs one but install only touched the other | Ask user. If both, install to both `$PROFILE` paths. |

---

## 6. Update path specifics

- `/orni-update-mb` MUST replace the entire `# ORNI-MB-START` ... `# ORNI-MB-END` block, not patch in place. This guarantees alias / function refresh.
- Alias dictionary updates (new free models, deprecated paid IDs) ship via `profile-snippet.ps1` only. The user's `backend_keys.json` is never touched.
- Version bump in the START marker (`v1.0.0` → `v1.1.0` etc.) lets future updates detect outdated installs.

---

## 7. Report format

Use the report skeleton in `SKILL.md` §8. Always end with explicit next steps :
1. Reload : `. $PROFILE` or open new pwsh.
2. (If keys file new) edit `~/.claude/backend_keys.json` with OR key.
3. Verify : `odsp-models` lists aliases, `odsp deepseek -p "hi"` succeeds.
