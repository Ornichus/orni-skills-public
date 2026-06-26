# /setup-agent-browser - Configurer Agent-Browser sur Windows/WSL

## Contexte

`agent-browser` (Vercel) permet l'automatisation navigateur — directement via Claude Code, ou dans une **boucle autonome**. Sur Windows, il y a deux obstacles :

1. **agent-browser** s'execute dans **WSL Ubuntu**, pas Windows
2. **Claude Code** (et les lanceurs de boucle autonome cote Windows) detectent l'outil via `where agent-browser` (PATH Windows natif) et l'executent via **Git Bash** (`/usr/bin/bash`)

Il faut creer des wrappers dans un dossier present dans le PATH Windows **natif** (ex: `.local/bin`).

## Instructions

Execute les etapes suivantes dans l'ordre:

### 1. Verifier les prerequis

```bash
# Verifier WSL Ubuntu
wsl.exe -d Ubuntu -- echo "WSL OK"

# Verifier si agent-browser est installe dans WSL
wsl.exe -d Ubuntu -- npm list -g agent-browser 2>/dev/null || echo "Non installe"
```

### 2. Installer agent-browser dans WSL (si necessaire)

```bash
wsl.exe -d Ubuntu -- npm install -g agent-browser
wsl.exe -d Ubuntu -- npx agent-browser install
```

### 3. Trouver le dossier cible (dans le PATH Windows natif)

```powershell
# Lister les dossiers bin deja dans le PATH Windows
[Environment]::GetEnvironmentVariable('PATH', 'User') -split ';' | Where-Object { $_ -match 'bin' }
# Choisir un dossier existant, ex: C:\Users\<USERNAME>\.local\bin
```

```bash
# Creer le dossier si necessaire
mkdir -p "$HOME/.local/bin"
```

> **IMPORTANT**: Ne PAS utiliser `~/bin` seul. Ce dossier est visible par Git Bash
> mais souvent absent du PATH Windows natif. La detection via `where agent-browser`
> ne voit que le PATH Windows.

### 4. Creer le wrapper Bash (CRITIQUE pour Git Bash/Claude Code)

```bash
cat > "$HOME/.local/bin/agent-browser" << 'EOF'
#!/bin/bash
wsl.exe -d Ubuntu -- npx agent-browser "$@"
EOF
chmod +x "$HOME/.local/bin/agent-browser"
```

### 5. Creer le wrapper CMD (pour PowerShell)

```bash
cat > "$HOME/.local/bin/agent-browser.cmd" << 'EOF'
@echo off
wsl.exe -d Ubuntu -- npx agent-browser %*
EOF
```

### 6. Verifier la detection

```powershell
# Simuler exactement ce que fait un lanceur Windows natif
where.exe agent-browser
# DOIT afficher le chemin. Si "not found" → le dossier n'est pas dans le PATH Windows
```

### 7. Tests de validation

Executer tous ces tests et verifier qu'ils passent:

```bash
# Test 1: Version via bash
agent-browser --version
# Attendu: agent-browser 0.7.x

# Test 2: Version via PowerShell
powershell.exe -Command "agent-browser --version"
# Attendu: agent-browser 0.7.x

# Test 3: Test fonctionnel complet
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser screenshot /tmp/test-setup.png
agent-browser close
```

## Criteres de succes

- [ ] `agent-browser --version` fonctionne dans Git Bash
- [ ] `agent-browser --version` fonctionne dans PowerShell
- [ ] `where.exe agent-browser` affiche le chemin du wrapper (PATH Windows natif)
- [ ] Screenshot de test cree avec succes

## Depannage

### "/usr/bin/bash: agent-browser: command not found"
Le wrapper bash n'existe pas ou n'est pas executable.
Solution: Recreer le fichier sans extension et faire `chmod +x`

### "wsl.exe not found"
Utiliser le chemin complet `/mnt/c/Windows/System32/wsl.exe` dans le wrapper

### "npx agent-browser: command not found" dans WSL
Reinstaller: `wsl.exe -d Ubuntu -- npm install -g agent-browser`

### Screenshots vides
Installer Chromium: `wsl.exe -d Ubuntu -- npx agent-browser install`

## Architecture finale

```
Boucle autonome / Claude Code
    |
    v
Git Bash (/usr/bin/bash)
    |
    v
~/.local/bin/agent-browser (script bash)
    |
    v
wsl.exe -d Ubuntu -- npx agent-browser
    |
    v
WSL Ubuntu -> Chromium headless
```

## References

- Documentation complete: docs/AGENT-BROWSER-WINDOWS-WSL.md
- agent-browser GitHub: https://github.com/vercel-labs/agent-browser
