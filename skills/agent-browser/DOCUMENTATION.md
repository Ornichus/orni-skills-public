# Vercel Agent Browser CLI - Documentation Complète

> **Version**: 0.7.6 | **Dernière mise à jour**: 24 janvier 2026 | **Statut**: Validé (22/22 tests)

## Table des Matières

1. [Introduction](#introduction)
2. [Architecture et Fonctionnement](#architecture-et-fonctionnement)
3. [Pourquoi Agent Browser est Plus Fiable](#pourquoi-agent-browser-est-plus-fiable)
4. [Installation sur Windows via WSL](#installation-sur-windows-via-wsl)
5. [Commandes Principales](#commandes-principales)
6. [Workflow Optimal pour Agents IA](#workflow-optimal-pour-agents-ia)
7. [Intégration avec Claude Code](#integration-avec-claude-code)
8. [Sessions et Mode Multi-Browser](#sessions-et-mode-multi-browser)
9. [Dépannage](#depannage)
10. [Références](#references)

---

## Introduction

**Vercel Agent Browser CLI** est un outil d'automatisation de navigateur headless conçu spécifiquement pour les agents IA. Il utilise Playwright sous le capot mais avec une approche innovante basée sur des "références condensées" qui le rend significativement plus fiable que les alternatives traditionnelles.

### Statistiques de Fiabilité (Source: Cole Medin)

| Outil | Taux de Réussite Premier Essai |
|-------|-------------------------------|
| Vercel Agent Browser CLI | **95%** |
| Playwright MCP | 80% |
| Chrome DevTools MCP | 75% |

### Caractéristiques Clés

- **Gratuit et Open Source** (Licence Apache-2.0)
- **CLI Rust rapide** avec fallback Node.js
- **Système de références** (`e1`, `e2`) pour interactions déterministes
- **Optimisé pour les LLMs** - sortie condensée et token-efficient
- **Sessions isolées** pour tests parallèles

---

## Architecture et Fonctionnement

### Architecture Client-Daemon

```
┌─────────────────────────────────────────────────────────────────┐
│                         Windows Host                            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   Frontend   │    │   Backend    │    │  Firewall Rules  │  │
│  │  :5173       │    │   :8003      │    │  (ports ouverts) │  │
│  └──────────────┘    └──────────────┘    └──────────────────┘  │
│         ▲                   ▲                     │             │
│         │    IP LAN (192.168.x.x)                 │             │
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

1. **CLI Rust** (binaire natif rapide) - Parse les commandes, communique avec le daemon
2. **Node.js Daemon** - Gère l'instance Playwright/Chromium
3. **Fallback** - Si le binaire natif n'est pas disponible, utilise Node.js directement

Le daemon démarre automatiquement à la première commande et persiste ~30 secondes entre les commandes pour des opérations rapides.

### Philosophie "Less is More"

Contrairement aux approches traditionnelles qui utilisent des sélecteurs et des recherches (matching non-déterministe), Agent Browser:

1. **Visite le site** et prend un **snapshot**
2. **Condense** la structure en références pointant vers les éléments interactifs
3. **Retourne** une version consolidée au LLM
4. L'agent utilise les **refs** (`e1`, `e2`) pour interagir de manière déterministe

Cette approche réduit les erreurs car on ne dépend pas de recherches/matching qui peuvent échouer.

---

## Pourquoi Agent Browser est Plus Fiable

### Approche Traditionnelle (Playwright MCP)

```
Agent -> Recherche sélecteur -> Match elements -> Retry si échec -> Action
         (non-déterministe)     (peut échouer)
```

### Approche Agent Browser

```
Agent -> Snapshot -> Références déterminées -> Action directe avec ref
         (structure complète)  (e1, e2, e3)      (pas de recherche)
```

### Avantages

1. **Déterministe** - La référence pointe vers l'élément exact du snapshot
2. **Rapide** - Pas de re-query du DOM nécessaire
3. **Token-efficient** - Structure condensée envoyée au LLM
4. **Fiable** - Pas de dépendance aux recherches qui peuvent échouer

---

## Installation sur Windows via WSL

> **IMPORTANT**: Agent Browser ne fonctionne PAS correctement sur Windows natif.
> Il FAUT utiliser WSL (Windows Subsystem for Linux) avec Ubuntu.

### Prérequis

- Windows 10/11 avec WSL2
- Ubuntu installé dans WSL
- Node.js 18+ installé dans Ubuntu

### Étape 1: Vérifier/Installer WSL

```powershell
# Dans PowerShell (Admin)
wsl --install -d Ubuntu
```

### Étape 2: Installer Node.js dans WSL

```bash
# Dans WSL Ubuntu
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Étape 3: Installer Agent Browser

```bash
# Dans WSL Ubuntu
npm install -g agent-browser
```

### Étape 4: Installer Chromium

```bash
# Installer les navigateurs Playwright
npx playwright install chromium

# Installer les dépendances système (OBLIGATOIRE)
npx playwright install-deps chromium
```

### Étape 5: Configurer le Firewall Windows

**Exécuter en tant qu'Administrateur** dans PowerShell:

```powershell
# Règle pour les ports de développement
netsh advfirewall firewall add rule name="WSL Dev Ports" dir=in action=allow protocol=TCP localport=8000-8010,3000,5173 enable=yes

# Règle permissive pour WSL (IMPORTANTE)
netsh advfirewall firewall add rule name="Allow Any to Local Dev Ports" dir=in action=allow protocol=TCP localport=5173,8003 remoteip=any enable=yes profile=any
```

### Étape 6: Identifier l'IP à utiliser

```powershell
# Dans PowerShell Windows
ipconfig | findstr "IPv4"

# Chercher l'IP de la carte Ethernet principale (ex: 192.168.1.x)
# NE PAS utiliser l'IP vEthernet (WSL) qui est en 172.x.x.x
```

### Étape 7: Vérifier l'Installation

```bash
# Tester que tout fonctionne
wsl -d Ubuntu -- bash -c "npx agent-browser open 'https://example.com'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
wsl -d Ubuntu -- bash -c "npx agent-browser close"
```

---

## Commandes Principales

### Pattern Obligatoire pour Claude Code

```bash
# OBLIGATOIRE: Utiliser bash -c pour éviter l'erreur EAGAIN
wsl -d Ubuntu -- bash -c "npx agent-browser <commande>"
```

### Workflow de Base

```bash
# 1. Ouvrir une URL
npx agent-browser open <url>

# 2. Prendre un snapshot (éléments interactifs)
npx agent-browser snapshot -i

# 3. Interagir avec les références
npx agent-browser click e1
npx agent-browser fill e2 "texte"

# 4. Fermer
npx agent-browser close
```

### Navigation

```bash
npx agent-browser open <url>      # Naviguer vers URL
npx agent-browser back            # Page précédente
npx agent-browser forward         # Page suivante
npx agent-browser reload          # Recharger
npx agent-browser close           # Fermer le navigateur
```

### Snapshot (Analyse de Page)

```bash
npx agent-browser snapshot            # Arbre d'accessibilité complet
npx agent-browser snapshot -i         # Éléments interactifs seulement (RECOMMANDÉ)
npx agent-browser snapshot -c         # Sortie compacte
npx agent-browser snapshot -d 3       # Limiter profondeur à 3
npx agent-browser snapshot -s "#main" # Limiter à un sélecteur CSS
npx agent-browser snapshot -i --json  # Format JSON pour parsing
```

### Interactions (avec refs du snapshot)

```bash
npx agent-browser click e1           # Clic
npx agent-browser dblclick e1        # Double-clic
npx agent-browser fill e2 "texte"    # Effacer et taper
npx agent-browser type e2 "texte"    # Taper sans effacer
npx agent-browser press Enter        # Appuyer sur touche
npx agent-browser press Control+a    # Combinaison de touches
npx agent-browser hover e1           # Survol (voir note spéciale)
npx agent-browser check e1           # Cocher checkbox
npx agent-browser uncheck e1         # Décocher checkbox
npx agent-browser select e1 "value"  # Sélectionner dropdown
npx agent-browser scroll down 500    # Défiler page
npx agent-browser scrollintoview e1  # Amener élément en vue
npx agent-browser drag e1 e2         # Glisser-déposer
npx agent-browser upload e1 file.pdf # Télécharger fichier
```

### Commande hover (cas spécial)

La commande `hover` nécessite `nohup` pour fonctionner dans Claude Code:

```bash
wsl -d Ubuntu -- bash -c "nohup npx agent-browser hover e1 > /tmp/hover.log 2>&1 & sleep 2"
```

### Obtenir des Informations

```bash
npx agent-browser get text e1        # Texte de l'élément
npx agent-browser get html e1        # innerHTML
npx agent-browser get value e1       # Valeur input
npx agent-browser get attr e1 href   # Attribut spécifique
npx agent-browser get title          # Titre de la page
npx agent-browser get url            # URL actuelle
npx agent-browser get count ".item"  # Compter éléments
npx agent-browser get box e1         # Bounding box
```

### Vérifications d'état

```bash
npx agent-browser is visible e1      # Élément visible?
npx agent-browser is enabled e1      # Élément activé?
npx agent-browser is checked e1      # Checkbox cochée?
```

### Screenshots et PDF

```bash
npx agent-browser screenshot              # Screenshot vers stdout
npx agent-browser screenshot page.png     # Sauvegarder fichier
npx agent-browser screenshot --full       # Page complète
npx agent-browser pdf output.pdf          # Sauvegarder en PDF
```

### Debug

```bash
npx agent-browser highlight e1       # Surligner un élément
npx agent-browser console            # Afficher les logs console
npx agent-browser errors             # Afficher les erreurs JS
```

### Attente

```bash
npx agent-browser wait e1                     # Attendre élément
npx agent-browser wait 2000                   # Attendre millisecondes
npx agent-browser wait --text "Success"       # Attendre texte
npx agent-browser wait --url "**/dashboard"   # Attendre pattern URL
npx agent-browser wait --load networkidle     # Attendre fin réseau
npx agent-browser wait --fn "window.ready"    # Attendre condition JS
```

---

## Workflow Optimal pour Agents IA

### Workflow Recommandé

```bash
# 1. Naviguer et obtenir snapshot
wsl -d Ubuntu -- bash -c "npx agent-browser open 'https://example.com'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"

# 2. L'IA identifie les refs cibles depuis le snapshot
# 3. Exécuter les actions avec les refs
wsl -d Ubuntu -- bash -c "npx agent-browser click e2"
wsl -d Ubuntu -- bash -c "npx agent-browser fill e3 'texte input'"

# 4. Nouveau snapshot si la page a changé
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"

# 5. Fermer
wsl -d Ubuntu -- bash -c "npx agent-browser close"
```

### Exemple Complet: Soumission de Formulaire

```bash
# Ouvrir la page du formulaire
wsl -d Ubuntu -- bash -c "npx agent-browser open 'https://example.com/form'"

# Obtenir les éléments interactifs
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
# Sortie:
# - textbox "Email" [ref=e1]
# - textbox "Password" [ref=e2]
# - button "Submit" [ref=e3]

# Remplir le formulaire
wsl -d Ubuntu -- bash -c "npx agent-browser fill e1 'user@example.com'"
wsl -d Ubuntu -- bash -c "npx agent-browser fill e2 'password123'"
wsl -d Ubuntu -- bash -c "npx agent-browser click e3"

# Attendre et vérifier
wsl -d Ubuntu -- bash -c "npx agent-browser wait --load networkidle"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
```

---

## Intégration avec Claude Code

> **IMPORTANT pour Windows**: Toutes les commandes doivent utiliser le pattern `bash -c` pour éviter l'erreur EAGAIN.

### Méthode 1: Skill pour un Projet Spécifique

Copiez le dossier `skills/agent-browser/` dans votre projet:

```powershell
# PowerShell - copier vers un projet
xcopy /E /I "skills\agent-browser" "C:\chemin\vers\ton-projet\.claude\skills\agent-browser"
```

### Méthode 2: Skill Global (Tous les Projets)

Pour que le skill soit disponible dans TOUS vos projets Claude Code:

```powershell
# PowerShell - installer globalement
xcopy /E /I "skills\agent-browser" "%USERPROFILE%\.claude\skills\agent-browser"
```

### Méthode 3: Instructions dans CLAUDE.md

Ajoutez à votre fichier `CLAUDE.md`:

```markdown
## Browser Automation (Windows/WSL)

Use agent-browser via WSL for web automation:

Core workflow:
1. `wsl -d Ubuntu -- bash -c "npx agent-browser open '<url>'"` - Navigate to page
2. `wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"` - Get interactive elements with refs (e1, e2)
3. `wsl -d Ubuntu -- bash -c "npx agent-browser click e1"` - Interact using refs
4. `wsl -d Ubuntu -- bash -c "npx agent-browser close"` - Close browser

Note: Pour accéder à localhost Windows depuis WSL, utiliser l'IP LAN (192.168.x.x)
```

### Accès à Localhost Windows depuis WSL

Si votre serveur de dev tourne sur Windows (ex: `npm run dev` sur port 5173):

```bash
# Vérifier l'IP LAN Windows
ipconfig | findstr "192.168"

# Depuis WSL, utiliser l'IP LAN (PAS 172.x.x.x)
wsl -d Ubuntu -- bash -c "npx agent-browser open 'http://192.168.1.50:5173'"
```

---

## Sessions et Mode Multi-Browser

### Sessions Isolées

Exécutez plusieurs instances de navigateur isolées:

```bash
# Sessions différentes
npx agent-browser --session agent1 open site-a.com
npx agent-browser --session agent2 open site-b.com

# Lister les sessions actives
npx agent-browser session list
```

Chaque session a ses propres:
- Instance de navigateur
- Cookies et stockage
- Historique de navigation
- État d'authentification

### Mode Headed (Debug)

Afficher la fenêtre du navigateur pour le debug:

```bash
npx agent-browser open example.com --headed
```

---

## Dépannage

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
1. Mauvaise IP utilisée (172.x.x.x au lieu de 192.168.x.x)
2. Firewall bloque la connexion
3. Serveur non démarré

**Solutions**:
```powershell
# 1. Vérifier l'IP LAN (pas vEthernet!)
ipconfig | findstr "IPv4"
# Utiliser 192.168.x.x, PAS 172.x.x.x

# 2. Vérifier que le serveur écoute
netstat -ano | findstr "5173"

# 3. Vérifier les règles firewall
netsh advfirewall firewall show rule name="Allow Any to Local Dev Ports"
```

### Erreur: "command not found: agent-browser"

```bash
# Option 1: Utiliser npx
npx agent-browser <commande>

# Option 2: Ajouter au PATH
export PATH="$PATH:$(npm config get prefix)/bin"
```

### Erreur: "Executable doesn't exist at /home/.../.cache/ms-playwright/..."

Les navigateurs Playwright manquent:

```bash
# Installer les navigateurs
wsl -d Ubuntu -- npx playwright install chromium

# Si erreur de dépendances:
wsl -d Ubuntu -- npx playwright install-deps chromium
```

### Erreur: "libnspr4.so: cannot open shared object file"

Les dépendances système manquent:

```bash
sudo apt-get update
sudo apt-get install -y libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2

# Ou utilisez la commande Playwright
sudo npx playwright install-deps chromium
```

---

## Références

### Liens Officiels

- **GitHub Repository**: https://github.com/vercel-labs/agent-browser
- **Video Explicative**: https://www.youtube.com/watch?v=7aEQnTsI6zs
- **Blog Vercel (Philosophie)**: https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools

### Version Actuelle

- **Package**: `agent-browser@0.7.6`
- **Playwright**: `^1.57.0`
- **Licence**: Apache-2.0

---

## Résumé des Commandes Essentielles

```bash
# Installation (WSL Ubuntu)
npm install -g agent-browser
npx playwright install chromium
npx playwright install-deps chromium

# Workflow de base (depuis Windows avec Claude Code)
wsl -d Ubuntu -- bash -c "npx agent-browser open '<url>'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
wsl -d Ubuntu -- bash -c "npx agent-browser click e1"
wsl -d Ubuntu -- bash -c "npx agent-browser fill e2 'text'"
wsl -d Ubuntu -- bash -c "npx agent-browser close"
```

---

## Changelog

| Date | Version | Changements |
|------|---------|-------------|
| 2026-01-24 | 0.7.6 | Mise à jour complète, résolution EAGAIN, 22/22 tests validés |
| 2026-01-20 | 0.6.0 | Documentation initiale |

---

*Documentation mise à jour le 24/01/2026 - Basée sur agent-browser v0.7.6*
