# Orni-Skills

Bibliothèque modulaire de **skills, commandes et workflows pour Claude Code**.
Chaque module s'installe dans un projet via une commande `/orni-init-*` et se met à jour via `/orni-update-*`.

## ▶ Démarrage rapide

**Nouveau ici ?** Lis le **[Guide d'utilisation](docs/GUIDE-UTILISATION.md)** — il explique en 5 minutes comment utiliser Orni-Skills au quotidien (installer un module, le protocole `/update` + `/followup`, le workflow type).

## Modules disponibles

| Module | Code | Description |
|--------|------|-------------|
| **Architecture** | AR | Cartographie relationnelle des dépendances d'un projet |
| **ATeam** | AT | Composition d'équipes d'agents + Council délibératif |
| **Mailbox** | ML | Messagerie inter-projets (sync, live-talk, conférence multi-agents) |
| **Agent Browser** | AB | Automatisation navigateur via `agent-browser` (Windows/WSL) |
| **Update / Followup** | UF | Synchronisation Archon MCP + état projet + diagnostic |
| **Project State** | PSM | Gestion de `project-state.xml` |
| **Project Status Snapshot** | PSS | Rapport d'état condensé (JSON + format humain 4 sections) |
| **Structure** | STR | Restructureur de prompt professionnel |
| **VPS** | VPS | Gestion d'un serveur distant via SSH (config externalisée) |
| **Deploy** | DPL | Déploiement automatisé VPS + Cloudflare |
| **Cloudflare** | CF | Gestion DNS et Workers via l'API Cloudflare |
| **Excalidraw** | EX | Génération de diagrammes visuels |
| **Fal Image Gen** | FAL | Génération d'images via le MCP fal.ai |
| **Marp Presentations** | MP | Decks HTML reproductibles, thème HSL paramétrique, export multi-format |
| **Frontend Slides** | FS | Decks one-shot premium (pitch, mockups, animations CSS) — style « Nimbe » |
| **Design System** | DS | Extraction de marque → design-system.html + brand-book A4 PDF |
| **Web PDF Compile** | WPC | Capture d'articles web → PDF dossier groupé par thème |
| **Multi-Backend** | MB | Helper PowerShell de routage de modèles (Anthropic natif + OpenRouter) |
| **GSD** | GSD | Framework spec-driven MVP exploratoire (wrapper Orni) |
| **Task Orchestrator** | TO | Méta-orchestrateur au-dessus de GSD/BMAD/Superpowers (waves + routing + KPIs) |
| **CLAUDE.md Template** | CLA | Bootstrap d'un `CLAUDE.md` projet standardisé |

Le dossier `_bmad/` embarque par ailleurs le framework **BMAD** (Module Builder, Method, Creative & Innovation Skills, Testing) accessible via les commandes `/bmad-*`.

## Installation

```bash
# Installer tous les modules dans un projet
/orni-init-full

# Installer un module spécifique
/orni-init-archi    # Architecture
/orni-init-at       # ATeam
/orni-init-ab       # Agent Browser
/orni-init-psm      # Project State Management
/orni-init-ml       # Mailbox
/orni-init-deploy   # Deploy
/orni-init-vps      # VPS
/orni-init-cf       # Cloudflare
/orni-init-excal    # Excalidraw
/orni-init-fal      # Fal Image Gen
/orni-init-mp       # Marp Presentations
/orni-init-fs       # Frontend Slides
/orni-init-ds       # Design System
/orni-init-wpc      # Web PDF Compile
/orni-init-mb       # Multi-Backend
/orni-init-gsd      # GSD
/orni-init-to       # Task Orchestrator
/orni-init-claude-md  # Bootstrap CLAUDE.md projet
```

## Commandes principales

| Commande | Description |
|----------|-------------|
| `/orni-help` | Catalogue complet de toutes les commandes |
| `/orni-checkup` | Vérifie si les modules installés sont à jour |
| `/orni-init-full` | Installe tous les modules |
| `/orni-update-full` | Met à jour tous les modules installés |
| `/architecture` | Génère la doc d'architecture relationnelle |
| `/ateam suggest` | Compose une équipe d'agents adaptée au contexte |
| `/mail-send` · `/mail-read` | Messagerie inter-projets |
| `/update` · `/followup` | Sync Archon MCP + état projet |
| `/orni-status` | Rapport d'état condensé |
| `/structure` | Restructure un prompt en format professionnel |
| `/setup-agent-browser` | Configure agent-browser sur Windows/WSL |

## Structure du dépôt

```
orni-skills/
├── commands/        # Slash commands Orni (orni-init-*, orni-update-*, mail-*, ...)
├── skills/          # Modules (un dossier par skill, avec SKILL.md)
├── _bmad/           # Framework BMAD (bmb, bmm, cis, tea, core)
├── .claude/         # Commandes + skills installés côté projet
├── docs/            # Guides d'utilisation
├── templates/       # Templates (CLAUDE.md projet, ...)
└── settings-template.json
```

## Configuration requise

- **Claude Code** récent
- **Archon MCP** (optionnel — gestion de tâches/projets)
- **Docker Desktop** (optionnel — pour le MCP Toolkit)

Certains modules (Deploy, Cloudflare, VPS, Fal Image Gen) nécessitent que tu fournisses **ta propre configuration** (domaine, serveur, clés d'API) dans des fichiers locaux non versionnés — voir le `SKILL.md` de chaque module. Aucune clé ni aucun secret n'est inclus dans ce dépôt.

## Licence

MIT
