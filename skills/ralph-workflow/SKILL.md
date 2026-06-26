# Ralph Workflow - PRD Validation & Autonomous Loop

**Version:** 0.1.0-beta
**Status:** Beta
**Author:** Ornichus
**Last Updated:** 2026-01-24

---

## Overview

Ce skill implémente le workflow **Ralph Loop** pour la validation PRD et l'exécution autonome de features. Basé sur la philosophie de Geoffrey Huntley et adapté pour Claude Code.

### Concept Clé

```
PRD Structuré → Test Manuel → Analyse Écarts → PRD Révisé → Ralph Loop Autonome
```

**Ralph Loop** = Boucle bash qui exécute Claude Code répétitivement. Chaque itération:
1. Lit le PRD (features avec `passes: true/false`)
2. Implémente la prochaine feature non-passée
3. Valide avec agent-browser
4. Met à jour `activity.md` (mémoire inter-loops)
5. Exit condition: TOUTES les features ont `passes: true`

---

## Workflow Complet

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RALPH WORKFLOW COMPLET                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 0: SETUP                                                              │
│  ══════════════                                                              │
│      │                                                                       │
│      ├── Créer/Vérifier PRD existant (format BMAD ou autre)                 │
│      ├── Installer agent-browser (WSL Ubuntu)                               │
│      └── Configurer firewall Windows                                        │
│                                                                              │
│  PHASE 1: TEST MANUEL (Human + Agent)                                       │
│  ═════════════════════════════════════                                       │
│      │                                                                       │
│      ├── Démarrer application (backend + frontend)                          │
│      ├── Tester chaque Epic/User Story du PRD                               │
│      ├── Agent-browser pour screenshots/validation                          │
│      └── Utilisateur note les écarts/problèmes                              │
│                                                                              │
│  PHASE 2: ANALYSE COMPARÉE                                                  │
│  ══════════════════════════                                                  │
│      │                                                                       │
│      ├── Feedback utilisateur vs PRD                                        │
│      ├── Classification: Manquant / Partiel / Différent / Bug              │
│      └── Création checklist de suivi                                        │
│                                                                              │
│  PHASE 3: RÉVISION PRD                                                      │
│  ══════════════════════                                                      │
│      │                                                                       │
│      ├── Correction des incohérences                                        │
│      ├── Ajout fonctionnalités manquantes                                   │
│      ├── Mise à jour User Stories                                           │
│      └── Validation utilisateur                                             │
│                                                                              │
│  PHASE 4: CONVERSION RALPH FORMAT                                           │
│  ═════════════════════════════════                                           │
│      │                                                                       │
│      ├── PRD → PRD-ralph.md (features + validation + passes)                │
│      ├── Création prompt.md (contexte par loop)                             │
│      ├── Création activity.md (mémoire)                                     │
│      ├── Création settings.json (sécurité)                                  │
│      └── Création ralph.sh (script boucle)                                  │
│                                                                              │
│  PHASE 5: RALPH LOOP AUTONOME                                               │
│  ══════════════════════════════                                              │
│      │                                                                       │
│      ├── ./ralph.sh 50 (max 50 itérations)                                  │
│      ├── Agent implémente feature par feature                               │
│      ├── Agent-browser valide chaque feature                                │
│      └── Exit: ALL passes=true → "promise complete"                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Fichiers Ralph

### Structure Requise

```
project-root/
├── .ralph/
│   ├── PRD-ralph.md        # PRD format Ralph (features + passes)
│   ├── prompt.md           # Contexte envoyé à chaque loop
│   ├── activity.md         # Mémoire long-terme entre loops
│   ├── settings.json       # Sécurité (commandes autorisées)
│   └── ralph.sh            # Script boucle bash
├── test/
│   ├── prd-validation-checklist.md
│   └── agent-browser/
│       └── test-results/
└── docs/
    └── PRD.md              # PRD original (BMAD ou autre)
```

---

## Agent-Browser Setup (Windows + WSL)

### Installation

```bash
# Dans WSL Ubuntu
npm install -g agent-browser
npx playwright install chromium
npx playwright install-deps chromium
```

### Configuration Firewall (PowerShell Admin)

```powershell
# Autoriser les ports dev
netsh advfirewall firewall add rule name="WSL Dev Ports" dir=in action=allow protocol=TCP localport=8000-8010,3000,5173 enable=yes
```

### Pattern de Commande OBLIGATOIRE

```bash
# TOUJOURS utiliser bash -c pour éviter EAGAIN
wsl -d Ubuntu -- bash -c "npx agent-browser <command>"

# Exemples
wsl -d Ubuntu -- bash -c "npx agent-browser open 'http://192.168.1.50:5173'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
wsl -d Ubuntu -- bash -c "npx agent-browser click e1"
wsl -d Ubuntu -- bash -c "npx agent-browser close"
```

### Points Clés

- **IP**: Utiliser IP LAN (192.168.x.x), PAS vEthernet (172.x.x.x)
- **Syntaxe refs**: `e1`, `e2` (sans @)
- **Pattern bash -c**: OBLIGATOIRE pour éviter EAGAIN

---

## Référence Vidéo

Concept basé sur:
- **Cole Medin**: "I Was Wrong About Ralph Wiggum" (2026-01-22)
- **Geoffrey Huntley**: Créateur original de la philosophie Ralph Wiggum
- Template: https://github.com/coleam00/ralph-loop-quickstart

---

*Skill créé le 2026-01-24 - Version Beta*
