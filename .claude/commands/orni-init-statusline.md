---
description: 'Installe ccstatusline avec pace calculator et hooks globaux'
---

# /orni-init-statusline - Setup Status Line complet

Installe et configure ccstatusline avec le pace calculator (ratio consommation/temps) et les hooks globaux (daily-log-writer).

## Instructions

### 1. Verifier les prerequis

```bash
npx -y ccstatusline@latest --version
```

Si ccstatusline n'est pas disponible, informer l'utilisateur d'installer Node.js.

### 2. Installer les hooks globaux

Copier les scripts depuis le repo Orni-skills vers `~/.claude/hooks/` :

| Source (repo) | Destination |
|---------------|-------------|
| `Worktable/claude-code-skills/hooks/pace-calculator.ps1` | `~/.claude/hooks/pace-calculator.ps1` |
| `Worktable/claude-code-skills/hooks/daily-log-writer.ps1` | `~/.claude/hooks/daily-log-writer.ps1` |
| `Worktable/claude-code-skills/hooks/eco-status.ps1` | `~/.claude/hooks/eco-status.ps1` |
| `Worktable/claude-code-skills/hooks/eco-session-start.ps1` | `~/.claude/hooks/eco-session-start.ps1` |

```bash
cp "ORNI_SKILLS_DIR/Worktable/claude-code-skills/hooks/pace-calculator.ps1" "$HOME/.claude/hooks/"
cp "ORNI_SKILLS_DIR/Worktable/claude-code-skills/hooks/daily-log-writer.ps1" "$HOME/.claude/hooks/"
cp "ORNI_SKILLS_DIR/Worktable/claude-code-skills/hooks/eco-status.ps1" "$HOME/.claude/hooks/"
cp "ORNI_SKILLS_DIR/Worktable/claude-code-skills/hooks/eco-session-start.ps1" "$HOME/.claude/hooks/"
```

Remplacer `ORNI_SKILLS_DIR` par le chemin reel du repo Orni-skills (chercher dans `CLAUDE.md` ou utiliser le cwd si on est dans le repo).

### 3. Creer les repertoires necessaires

```bash
mkdir -p "$HOME/.claude/daily-logs"
```

### 4. Configurer settings.json (hooks)

Lire `~/.claude/settings.json`. Ajouter ou mettre a jour les hooks suivants :

**PreCompact** — ajouter daily-log-writer (ne pas ecraser les hooks existants) :
```json
{
  "type": "command",
  "command": "powershell -ExecutionPolicy Bypass -File C:/Users/USERNAME/.claude/hooks/daily-log-writer.ps1",
  "timeout": 60
}
```

**SessionEnd** — ajouter daily-log-writer :
```json
{
  "type": "command",
  "command": "powershell -ExecutionPolicy Bypass -File C:/Users/USERNAME/.claude/hooks/daily-log-writer.ps1",
  "timeout": 60
}
```

**statusLine** — configurer ccstatusline :
```json
{
  "type": "command",
  "command": "npx -y ccstatusline@latest",
  "padding": 0
}
```

**SessionStart** — ajouter le hook Mode Economie Token (ne pas ecraser les hooks existants) :
```json
{
  "type": "command",
  "command": "powershell -ExecutionPolicy Bypass -File C:/Users/USERNAME/.claude/hooks/eco-session-start.ps1",
  "timeout": 10
}
```

Remplacer `USERNAME` par le nom d'utilisateur reel (`$env:USERNAME` ou `whoami`).

### 5. Configurer ccstatusline

Lire le template `Worktable/claude-code-skills/config/ccstatusline-settings.json`.

Remplacer `__HOOKS_DIR__` par le chemin reel vers `~/.claude/hooks` (format: `C:/Users/USERNAME/.claude/hooks`).

Ecrire dans `~/.config/ccstatusline/settings.json` :
- Si le fichier existe deja, demander confirmation avant d'ecraser
- Creer le dossier `~/.config/ccstatusline/` si absent

```bash
mkdir -p "$HOME/.config/ccstatusline"
```

### 6. Installer le skill daily-log-promoter

Copier si absent :

```bash
mkdir -p "$HOME/.claude/skills/daily-log-promoter"
cp "ORNI_SKILLS_DIR/skills/daily-log-promoter/SKILL.md" "$HOME/.claude/skills/daily-log-promoter/" 2>/dev/null
```

Note : le fichier source peut etre dans `~/.claude/skills/daily-log-promoter/SKILL.md` (deja installe globalement).

### 6b. Mode Economie Token (commande /eco + etat)

Installer la commande globale `/eco` (regle la molette d'economie de tokens) et l'etat par defaut :

```bash
mkdir -p "$HOME/.claude/commands"
cp "ORNI_SKILLS_DIR/.claude/commands/eco.md" "$HOME/.claude/commands/eco.md"

# Etat par defaut (off) si absent — un seul mot dans le fichier
[ -f "$HOME/.claude/eco-mode" ] || printf 'off' > "$HOME/.claude/eco-mode"
```

La ligne dediee dans la statusline est deja portee par le template ccstatusline (widget `eco-status.ps1`, etape 5). Le hook `eco-session-start.ps1` (enregistre en SessionStart, etape 4) applique le niveau persistant a chaque session.

### 7. Verification

```bash
# Hooks presents
ls -la "$HOME/.claude/hooks/pace-calculator.ps1"
ls -la "$HOME/.claude/hooks/daily-log-writer.ps1"

# ccstatusline configure
cat "$HOME/.config/ccstatusline/settings.json" | head -5

# Daily logs dir
ls -d "$HOME/.claude/daily-logs"

# Test pace calculator
powershell -ExecutionPolicy Bypass -File "$HOME/.claude/hooks/pace-calculator.ps1"
```

### 8. Rapport

```
## /orni-init-statusline termine

| Composant | Status |
|-----------|--------|
| pace-calculator.ps1 | [Installe/Deja present] |
| daily-log-writer.ps1 | [Installe/Deja present] |
| eco-status.ps1 (widget) | [Installe/Deja present] |
| eco-session-start.ps1 (hook) | [Installe/Deja present] |
| /eco command + eco-mode | [Installe/Deja present] |
| daily-log-promoter skill | [Installe/Deja present] |
| ccstatusline config | [Configure/Deja present] |
| settings.json hooks | [Mis a jour] |
| daily-logs directory | [Cree/Deja present] |

Relancez Claude Code pour appliquer la nouvelle status line.
```
