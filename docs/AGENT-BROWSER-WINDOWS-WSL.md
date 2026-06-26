# Agent-Browser sur Windows avec WSL

Guide de configuration pour utiliser [agent-browser](https://github.com/vercel-labs/agent-browser) (Vercel) depuis Windows via WSL Ubuntu.

## Probleme

Sur Windows, Ralphy avec `--browser` echoue car:
- `agent-browser` s'execute dans **WSL/Ubuntu**
- Ralphy s'execute dans **Windows/PowerShell**
- Les commandes ne sont pas trouvees depuis Windows

```
[WARN] --browser flag used but agent-browser CLI not found
[WARN] Install from: https://agent-browser.dev
```

## Solution

Creer un wrapper Windows qui redirige vers WSL.

### 1. Installer agent-browser dans WSL

```bash
wsl -d Ubuntu -- npm install -g agent-browser
wsl -d Ubuntu -- npx agent-browser install  # Telecharge Chromium
```

### 2. Verifier l'installation

```bash
wsl.exe -d Ubuntu -- npx agent-browser --version
# Devrait afficher: agent-browser 0.7.x
```

### 3. Creer les wrappers (IMPORTANT: 2 fichiers necessaires)

Ralphy utilise **Git Bash** (`/usr/bin/bash`), pas cmd.exe. Il faut donc **deux wrappers**.

> **CRITIQUE - Choix du dossier**: Ralphy (via Bun) utilise `where agent-browser` pour detecter
> l'outil. `where` ne cherche que dans le **PATH Windows natif**. Le dossier `~/bin` est visible
> par Git Bash mais souvent **absent du PATH Windows**. Utilisez un dossier deja dans le PATH
> Windows comme `C:\Users\<USERNAME>\.local\bin`.

#### Verifier quel dossier utiliser

```powershell
# Lister les dossiers "bin" deja dans le PATH Windows
[Environment]::GetEnvironmentVariable('PATH', 'User') -split ';' | Where-Object { $_ -match 'bin' }

# Resultat typique:
# C:\Users\<USERNAME>\.local\bin    ← PREFERE (deja dans PATH Windows)
# C:\Users\<USERNAME>\.cargo\bin
# C:\Users\<USERNAME>\.bun\bin
```

#### Wrapper Bash (pour Ralphy/Git Bash/Claude Code)

Creer `C:\Users\<USERNAME>\.local\bin\agent-browser` (sans extension):

```bash
#!/bin/bash
# Wrapper agent-browser pour Git Bash -> WSL
wsl.exe -d Ubuntu -- npx agent-browser "$@"
```

Rendre executable:
```bash
chmod +x "$HOME/.local/bin/agent-browser"
```

#### Wrapper CMD (pour PowerShell/cmd.exe)

Creer `C:\Users\<USERNAME>\.local\bin\agent-browser.cmd`:

```batch
@echo off
wsl.exe -d Ubuntu -- npx agent-browser %*
```

> **Important**: Utiliser `wsl.exe` (pas `wsl`) pour la compatibilite.

### 4. Verifier la detection par Ralphy

Ralphy utilise `where agent-browser` (via Bun/Node.js `execSync`) pour detecter l'outil.
Ce check doit reussir sinon le flag `--browser` est ignore silencieusement.

```powershell
# Ce test simule exactement ce que Ralphy fait
where.exe agent-browser
# Doit afficher le chemin vers le wrapper

# Si "not found", le dossier n'est pas dans le PATH Windows natif
# Verifier avec:
[Environment]::GetEnvironmentVariable('PATH', 'User') -split ';'
```

### 5. Tester

```powershell
# Nouveau terminal PowerShell
agent-browser --version
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser screenshot test.png
agent-browser close
```

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  Windows                                                       │
│                                                                │
│  ┌─────────────┐                                               │
│  │   Ralphy    │  ralphy --browser "task"                      │
│  │  --browser  │                                               │
│  └──────┬──────┘                                               │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Claude Code utilise /usr/bin/bash (Git Bash)           │  │
│  └──────┬──────────────────────────────────────────────────┘  │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  C:\Users\<USER>\bin\agent-browser  (script bash)       │  │
│  │  #!/bin/bash                                            │  │
│  │  wsl.exe -d Ubuntu -- npx agent-browser "$@"            │  │
│  └──────┬──────────────────────────────────────────────────┘  │
│         │                                                      │
├─────────┼──────────────────────────────────────────────────────┤
│  WSL Ubuntu                                                    │
│         ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  npx agent-browser 0.7.x                                │  │
│  │  └── Chromium headless                                  │  │
│  │      └── Screenshots, Interactions, Snapshots           │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

**Note**: Le wrapper `.cmd` est pour PowerShell/cmd.exe direct, le script bash (sans extension) est pour Ralphy qui utilise Git Bash.

## Commandes agent-browser

| Commande | Description |
|----------|-------------|
| `agent-browser open <url>` | Ouvre une page |
| `agent-browser snapshot -i` | Capture les elements avec refs (@e1, @e2...) |
| `agent-browser snapshot --json` | Snapshot en format JSON |
| `agent-browser click @e1` | Clique sur un element |
| `agent-browser type @e1 "text"` | Tape du texte |
| `agent-browser screenshot <file>` | Capture d'ecran |
| `agent-browser close` | Ferme le navigateur |

## Utilisation avec Ralphy

```powershell
# Le flag --browser fonctionne maintenant
ralphy --json tasks.json --parallel --max-par --browser

# Verification pre-flight
agent-browser --version  # Doit retourner la version
```

## Depannage

### "/usr/bin/bash: agent-browser: command not found" (Ralphy)

Cette erreur signifie que Ralphy utilise Git Bash mais ne trouve que le wrapper `.cmd`.

**Solution**: Creer le script bash (sans extension):
```bash
# Creer le fichier
cat > /c/Users/$USER/bin/agent-browser << 'EOF'
#!/bin/bash
wsl.exe -d Ubuntu -- npx agent-browser "$@"
EOF

# Rendre executable
chmod +x /c/Users/$USER/bin/agent-browser

# Tester
agent-browser --version
```

### "agent-browser not found" (PowerShell/cmd)

1. Verifier l'installation WSL:
   ```bash
   wsl.exe -d Ubuntu -- npx agent-browser --version
   ```

2. Verifier le wrapper .cmd:
   ```powershell
   Get-Content "$env:USERPROFILE\bin\agent-browser.cmd"
   ```

3. Verifier le PATH:
   ```powershell
   where.exe agent-browser.cmd
   ```

### Screenshots vides ou erreurs

1. S'assurer que Chromium est installe:
   ```bash
   wsl.exe -d Ubuntu -- npx agent-browser install
   ```

2. Tester en mode visible:
   ```bash
   wsl.exe -d Ubuntu -- npx agent-browser open https://example.com --headed
   ```

### Problemes de chemins Windows/WSL

Git Bash convertit automatiquement les chemins (`/c/Users/...` → `C:\Users\...`).
Cela peut casser les arguments passes a WSL. Utiliser `MSYS_NO_PATHCONV=1` si necessaire:

```bash
# Si les chemins sont mal convertis
MSYS_NO_PATHCONV=1 agent-browser screenshot ./capture.png
```

Pour les screenshots via WSL, utiliser des chemins WSL puis copier:

```bash
# Sauvegarder dans WSL
wsl.exe -d Ubuntu -- npx agent-browser screenshot /tmp/capture.png

# Copier vers Windows
wsl.exe -d Ubuntu -- bash -c "cp /tmp/capture.png /mnt/c/Users/<USERNAME>/Desktop/"
```

### Ralphy affiche WARNING malgre l'installation

```
[WARN] --browser flag used but agent-browser CLI not found
```

Cette erreur signifie que Ralphy (Bun) ne trouve pas `agent-browser` via `where`.

**Cause**: Le code source de Ralphy (`execution/browser.ts`) fait:
```typescript
const checkCommand = isWindows ? "where agent-browser" : "which agent-browser";
execSync(checkCommand, { stdio: "ignore" });
```

**Solution**: Les wrappers doivent etre dans un dossier present dans le **PATH Windows natif**
(pas seulement Git Bash). Verifier avec `where.exe agent-browser` dans PowerShell.

Le dossier recommande est `C:\Users\<USERNAME>\.local\bin` (generalement deja dans le PATH).

## Verification rapide

Tester les deux environnements:

```bash
# Test Git Bash (utilise par Ralphy)
which agent-browser
agent-browser --version

# Test PowerShell
powershell.exe -Command "agent-browser --version"

# Test Ralphy complet
ralphy --browser --dry-run "test task"
# Doit afficher: [INFO] Browser automation enabled (agent-browser)
```

## References

- [agent-browser GitHub](https://github.com/vercel-labs/agent-browser)
- [agent-browser npm](https://www.npmjs.com/package/agent-browser)
- [Ralphy GitHub](https://github.com/michaelshimeles/ralphy)
- [Guide complet agent-browser](https://help.apiyi.com/en/agent-browser-ai-browser-automation-cli-guide-en.html)
