# Agent-Browser - Guide Complet pour Windows + WSL

> **Version**: 0.7.6 | **Dernière mise à jour**: 24 janvier 2026 | **Statut**: Validé (22/22 tests)

Agent-browser est un CLI de Vercel pour l'automatisation de navigateur, optimisé pour les agents IA. Ce guide couvre l'installation et l'utilisation sur Windows avec WSL Ubuntu.

---

## Table des matières

1. [Fonctionnement](#1-fonctionnement)
2. [Installation sur Windows](#2-installation-sur-windows)
3. [Configuration](#3-configuration)
4. [Commandes disponibles](#4-commandes-disponibles)
5. [Erreurs et dépannage](#5-erreurs-et-dépannage)
6. [Résultat attendu](#6-résultat-attendu)
7. [Checklist de validation](#7-checklist-de-validation)
8. [Intégration Claude Code](#8-intégration-claude-code)

---

## 1. Fonctionnement

### Principe

Agent-browser est un wrapper CLI autour de Playwright qui permet d'automatiser un navigateur Chromium en mode headless. Il expose des commandes simples pour naviguer, interagir et capturer des pages web.

### Architecture sur Windows

```
┌─────────────────────────────────────────────────────────────────┐
│                         Windows Host                            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   Frontend   │    │   Backend    │    │  Firewall Rules  │  │
│  │  :5173       │    │   :8003      │    │  (ports ouverts) │  │
│  │  (Vite)      │    │  (FastAPI)   │    │                  │  │
│  └──────────────┘    └──────────────┘    └──────────────────┘  │
│         ▲                   ▲                     │             │
│         │                   │                     │             │
│         │    IP LAN (192.168.x.x)                 │             │
│         │                   │                     │             │
│  ┌──────┴───────────────────┴─────────────────────┴──────────┐ │
│  │                      WSL Ubuntu                            │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │              agent-browser daemon                    │  │ │
│  │  │  ┌─────────────┐    ┌─────────────────────────────┐ │  │ │
│  │  │  │  Chromium   │◄───│  npx agent-browser <cmd>    │ │  │ │
│  │  │  │  (headless) │    │  (CLI commands)             │ │  │ │
│  │  │  └─────────────┘    └─────────────────────────────┘ │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Étapes clés du fonctionnement

1. **Démarrage**: `open <url>` lance le daemon et ouvre Chromium headless
2. **Session persistante**: Le daemon reste actif ~30 secondes après chaque commande
3. **Interaction**: Les commandes suivantes réutilisent le même daemon (rapide)
4. **Accessibilité**: `snapshot -i` retourne les éléments interactifs avec des refs (e1, e2...)
5. **Actions**: Utiliser les refs pour click, type, fill, etc.
6. **Fermeture**: `close` ferme explicitement le navigateur et le daemon

### Prérequis système

| Composant | Version minimum | Vérification |
|-----------|-----------------|--------------|
| Windows | 10 (build 19041+) | `winver` |
| WSL | 2.0+ | `wsl --version` |
| Ubuntu (WSL) | 20.04+ | `lsb_release -a` |
| Node.js | 18+ | `node --version` |
| agent-browser | 0.7.6+ | `npx agent-browser --version` |

---

## 2. Installation sur Windows

### Étape 1: Vérifier WSL

```powershell
# Vérifier que WSL2 est installé
wsl --version

# Si WSL n'est pas installé:
wsl --install -d Ubuntu
```

### Étape 2: Installer agent-browser dans WSL

```bash
# Ouvrir WSL Ubuntu
wsl -d Ubuntu

# Installer agent-browser globalement
npm install -g agent-browser

# Vérifier l'installation
npx agent-browser --version
# Attendu: agent-browser 0.7.6 (ou supérieur)
```

### Étape 3: Installer les navigateurs Playwright

```bash
# Dans WSL Ubuntu
npx playwright install chromium

# Si des dépendances manquent:
npx playwright install-deps chromium
```

### Étape 4: Configurer le firewall Windows

**Exécuter en tant qu'Administrateur** dans PowerShell:

```powershell
# Règle pour les ports de développement
netsh advfirewall firewall add rule name="WSL Dev Ports" dir=in action=allow protocol=TCP localport=8000-8010,3000,5173 enable=yes

# Règle permissive pour WSL (IMPORTANTE)
netsh advfirewall firewall add rule name="Allow Any to Local Dev Ports" dir=in action=allow protocol=TCP localport=5173,8003 remoteip=any enable=yes profile=any
```

### Étape 5: Identifier l'IP à utiliser

```powershell
# Dans PowerShell Windows
ipconfig | findstr "IPv4"

# Chercher l'IP de la carte Ethernet principale (ex: 192.168.1.x)
# NE PAS utiliser l'IP vEthernet (WSL) qui est en 172.x.x.x
```

**IMPORTANT**: L'IP LAN peut changer (DHCP). Vérifiez-la avant chaque session de test.

---

## 3. Configuration

### Configuration Vite (Frontend)

Le frontend doit écouter sur toutes les interfaces:

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    host: '0.0.0.0',  // OBLIGATOIRE
    port: 5173,
    allowedHosts: ['localhost', '192.168.1.50', 'host.docker.internal'],
  }
})
```

### Configuration Backend

```python
# main.py (FastAPI/Uvicorn)
uvicorn.run(app, host="0.0.0.0", port=8003)
```

### Variable d'environnement (optionnel)

```bash
# Dans WSL, ajouter à ~/.bashrc
export WIN_IP="192.168.1.50"  # Ajuster selon votre IP
```

---

## 4. Commandes disponibles

### Pattern de base (OBLIGATOIRE pour Claude Code)

```bash
wsl -d Ubuntu -- bash -c "npx agent-browser <commande>"
```

Le wrapper `bash -c` est **obligatoire** pour éviter l'erreur EAGAIN dans Claude Code.

### Navigation

| Commande | Description | Exemple |
|----------|-------------|---------|
| `open <url>` | Ouvrir une URL | `npx agent-browser open 'http://192.168.1.50:5173'` |
| `back` | Page précédente | `npx agent-browser back` |
| `forward` | Page suivante | `npx agent-browser forward` |
| `reload` | Recharger | `npx agent-browser reload` |
| `close` | Fermer le navigateur | `npx agent-browser close` |

### Capture

| Commande | Description | Exemple |
|----------|-------------|---------|
| `screenshot [path]` | Capture d'écran | `npx agent-browser screenshot /tmp/screen.png` |
| `screenshot --full` | Capture pleine page | `npx agent-browser screenshot /tmp/full.png --full` |
| `pdf <path>` | Export PDF | `npx agent-browser pdf /tmp/page.pdf` |
| `snapshot` | Arbre d'accessibilité complet | `npx agent-browser snapshot` |
| `snapshot -i` | Éléments interactifs uniquement | `npx agent-browser snapshot -i` |

### Interaction

| Commande | Description | Exemple |
|----------|-------------|---------|
| `click <ref>` | Cliquer | `npx agent-browser click e1` |
| `dblclick <ref>` | Double-clic | `npx agent-browser dblclick e1` |
| `type <ref> <text>` | Taper du texte | `npx agent-browser type e2 'Hello'` |
| `fill <ref> <text>` | Effacer et remplir | `npx agent-browser fill e2 'New text'` |
| `press <key>` | Appuyer touche | `npx agent-browser press Enter` |
| `hover <ref>` | Survoler (nécessite nohup*) | Voir section spéciale |
| `scroll <dir> [px]` | Défiler | `npx agent-browser scroll down 200` |
| `check <ref>` | Cocher checkbox | `npx agent-browser check e5` |
| `uncheck <ref>` | Décocher | `npx agent-browser uncheck e5` |
| `select <ref> <val>` | Sélectionner dropdown | `npx agent-browser select e3 option1` |

### Getters

| Commande | Description | Exemple |
|----------|-------------|---------|
| `get url` | URL actuelle | `npx agent-browser get url` |
| `get title` | Titre de la page | `npx agent-browser get title` |
| `get text <ref>` | Texte d'un élément | `npx agent-browser get text e1` |
| `get html <ref>` | HTML d'un élément | `npx agent-browser get html e1` |
| `get value <ref>` | Valeur d'un input | `npx agent-browser get value e2` |

### Vérifications d'état

| Commande | Description | Retour |
|----------|-------------|--------|
| `is visible <ref>` | Élément visible? | `true` / `false` |
| `is enabled <ref>` | Élément activé? | `true` / `false` |
| `is checked <ref>` | Checkbox cochée? | `true` / `false` |

### Debug

| Commande | Description |
|----------|-------------|
| `highlight <ref>` | Surligner un élément |
| `console` | Afficher les logs console |
| `errors` | Afficher les erreurs JS |

### Commande hover (cas spécial)

La commande `hover` nécessite `nohup` pour fonctionner dans Claude Code:

```bash
wsl -d Ubuntu -- bash -c "nohup npx agent-browser hover e1 > /tmp/hover.log 2>&1 & sleep 2"
```

---

## 5. Erreurs et dépannage

### Erreur: "Resource temporarily unavailable (os error 11)" / EAGAIN

**Cause**: Conflit entre le daemon agent-browser et la capture stdout de Claude Code.

**Solution**:
```bash
# MAUVAIS (provoque EAGAIN):
wsl -d Ubuntu -- npx agent-browser snapshot -i

# BON (avec bash -c):
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"

# Pour hover, utiliser nohup:
wsl -d Ubuntu -- bash -c "nohup npx agent-browser hover e1 > /tmp/out.log 2>&1 & sleep 2"
```

### Erreur: "net::ERR_ADDRESS_UNREACHABLE" ou timeout

**Causes possibles**:
1. Mauvaise IP utilisée
2. Firewall bloque la connexion
3. Serveur non démarré

**Solutions**:

```powershell
# 1. Vérifier l'IP LAN (pas vEthernet!)
ipconfig | findstr "IPv4"
# Utiliser 192.168.x.x, PAS 172.x.x.x

# 2. Vérifier que le serveur écoute
netstat -ano | findstr "5173"
# Doit montrer LISTENING sur 0.0.0.0:5173

# 3. Vérifier les règles firewall
netsh advfirewall firewall show rule name="Allow Any to Local Dev Ports"

# 4. Tester la connectivité depuis WSL
wsl -d Ubuntu -- bash -c "timeout 3 bash -c '</dev/tcp/192.168.1.50/5173' && echo OK || echo FAIL"
```

### Erreur: "Executable doesn't exist at /home/.../.cache/ms-playwright/..."

**Cause**: Navigateurs Playwright non installés ou version incompatible.

**Solution**:
```bash
# Installer les navigateurs
wsl -d Ubuntu -- npx playwright install chromium

# Si erreur de dépendances:
wsl -d Ubuntu -- npx playwright install-deps chromium
```

### Erreur: "Connection refused" (différent de timeout)

**Cause**: Le serveur ne tourne pas ou refuse les connexions.

**Solutions**:
```powershell
# Vérifier que le frontend tourne
netstat -ano | findstr "5173"

# Redémarrer le frontend si nécessaire
cd frontend && npm run dev
```

### Page blanche dans le screenshot

**Cause**: Le frontend n'a pas fini de charger ou erreur JS.

**Solutions**:
```bash
# Ajouter un délai après open
wsl -d Ubuntu -- bash -c "npx agent-browser open 'http://IP:5173' && sleep 3 && npx agent-browser screenshot /tmp/test.png"

# Vérifier les erreurs JS
wsl -d Ubuntu -- bash -c "npx agent-browser errors"
```

### L'IP a changé

**Cause**: DHCP a assigné une nouvelle IP.

**Solution**:
```powershell
# Vérifier la nouvelle IP
ipconfig | findstr "192.168"

# Mettre à jour les commandes avec la nouvelle IP
```

---

## 6. Résultat attendu

### Indicateurs de bon fonctionnement

| Test | Résultat attendu |
|------|------------------|
| `npx agent-browser --version` | `agent-browser 0.7.6` (ou supérieur) |
| `npx agent-browser open 'https://example.com'` | `✓ Example Domain` + URL |
| `npx agent-browser snapshot -i` | Liste d'éléments avec refs (e1, e2...) |
| `npx agent-browser screenshot /tmp/test.png` | `✓ Screenshot saved to /tmp/test.png` |
| `npx agent-browser get title` | Titre de la page |
| `npx agent-browser close` | `✓ Browser closed` |

### Comportement normal

1. **Première commande** (`open`): ~2-3 secondes (démarrage daemon + Chromium)
2. **Commandes suivantes**: ~100-500ms (daemon réutilisé)
3. **Timeout daemon**: ~30 secondes d'inactivité
4. **Screenshots**: Fichiers PNG de 10-500 KB selon la page

### Fichiers générés types

```
/tmp/
├── screenshot.png      # Screenshot standard
├── full.png           # Screenshot pleine page
├── page.pdf           # Export PDF
└── *.log              # Logs temporaires
```

---

## 7. Checklist de validation

### Test rapide (5 commandes)

```bash
# 1. Vérifier la version
wsl -d Ubuntu -- bash -c "npx agent-browser --version"
# Attendu: agent-browser 0.7.6+

# 2. Ouvrir un site externe
wsl -d Ubuntu -- bash -c "npx agent-browser open 'https://example.com'"
# Attendu: ✓ Example Domain

# 3. Snapshot interactif
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
# Attendu: - link "Learn more" [ref=e1]

# 4. Screenshot
wsl -d Ubuntu -- bash -c "npx agent-browser screenshot /tmp/test.png"
# Attendu: ✓ Screenshot saved

# 5. Fermer
wsl -d Ubuntu -- bash -c "npx agent-browser close"
# Attendu: ✓ Browser closed
```

### Test complet (22 commandes)

| # | Catégorie | Commande | Critère de réussite |
|---|-----------|----------|---------------------|
| 1 | Navigation | `open <url>` | Titre affiché |
| 2 | Navigation | `back` | URL change |
| 3 | Navigation | `forward` | URL revient |
| 4 | Navigation | `reload` | Page rechargée |
| 5 | Capture | `screenshot` | Fichier PNG créé |
| 6 | Capture | `screenshot --full` | PNG pleine page |
| 7 | Capture | `pdf` | Fichier PDF créé |
| 8 | Capture | `snapshot` | Arbre complet |
| 9 | Capture | `snapshot -i` | Refs listées (e1, e2...) |
| 10 | Interaction | `click` | Action déclenchée |
| 11 | Interaction | `type` | Texte visible |
| 12 | Interaction | `fill` | Texte remplacé |
| 13 | Interaction | `press` | Touche envoyée |
| 14 | Interaction | `hover` | Pas d'erreur (nohup) |
| 15 | Interaction | `scroll` | Position changée |
| 16 | Getter | `get url` | URL retournée |
| 17 | Getter | `get title` | Titre retourné |
| 18 | Getter | `get text` | Texte retourné |
| 19 | State | `is visible` | `true` ou `false` |
| 20 | State | `is enabled` | `true` ou `false` |
| 21 | Debug | `highlight` | Pas d'erreur |
| 22 | Debug | `console` | Logs affichés |

### Script de validation automatique

```bash
#!/bin/bash
# test-agent-browser.sh - À exécuter dans WSL

WIN_IP="192.168.1.50"  # AJUSTER SELON VOTRE IP
PASSED=0
FAILED=0

test_cmd() {
    echo -n "Testing: $1... "
    if eval "$2" > /dev/null 2>&1; then
        echo "PASS"
        ((PASSED++))
    else
        echo "FAIL"
        ((FAILED++))
    fi
}

# Tests
test_cmd "version" "npx agent-browser --version"
test_cmd "open" "npx agent-browser open 'https://example.com'"
test_cmd "snapshot" "npx agent-browser snapshot -i"
test_cmd "screenshot" "npx agent-browser screenshot /tmp/test.png"
test_cmd "get url" "npx agent-browser get url"
test_cmd "get title" "npx agent-browser get title"
test_cmd "close" "npx agent-browser close"

echo ""
echo "Results: $PASSED passed, $FAILED failed"
```

---

## 8. Intégration Claude Code

### Emplacement du skill

```
.claude/
└── skills/
    └── agent-browser/
        └── SKILL.md  ← Ce fichier
```

### Type de ressource

- **Type**: Skill (documentation de référence)
- **Invocation**: Référence dans les commandes/prompts
- **Pas de slash command**: Ce n'est pas une commande invocable directement

### Conformité Claude Code

| Aspect | Statut | Notes |
|--------|--------|-------|
| Structure `.claude/skills/` | ✅ Conforme | Emplacement standard |
| Format Markdown | ✅ Conforme | SKILL.md |
| Pattern bash -c | ✅ Requis | Évite EAGAIN |
| Documentation | ✅ Complète | Guide exhaustif |

### Utilisation dans d'autres skills/commandes

```markdown
# Dans .claude/commands/test.md
# Référencer agent-browser:

## Frontend Testing
Utiliser agent-browser pour les tests E2E:
\`\`\`bash
WIN_IP="192.168.1.50"
wsl -d Ubuntu -- bash -c "npx agent-browser open 'http://${WIN_IP}:5173'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
# ... tests ...
wsl -d Ubuntu -- bash -c "npx agent-browser close"
\`\`\`
```

### Bonnes pratiques

1. **Toujours** utiliser `bash -c` pour wrapper les commandes
2. **Vérifier** l'IP LAN avant chaque session
3. **Fermer** le navigateur après les tests (`close`)
4. **Utiliser nohup** pour la commande `hover`
5. **Copier** les screenshots vers Windows pour les visualiser:
   ```bash
   cp /tmp/screenshot.png /mnt/c/Users/.../output/
   ```

---

## Changelog

| Date | Version | Changements |
|------|---------|-------------|
| 2026-01-24 | 1.0.0 | Guide complet revalidé avec 22/22 tests |
| 2026-01-24 | 0.7.6 | Mise à jour agent-browser, résolution EAGAIN |

---

## Ressources

- [agent-browser GitHub](https://github.com/vercel-labs/agent-browser)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
