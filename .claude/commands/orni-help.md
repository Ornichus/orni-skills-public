# /orni-help — Catalogue complet Orni-Skills

Affiche toutes les commandes et skills de l'ecosysteme Orni avec leur statut d'installation sur le projet courant.

## Instructions

### 1. Scanner les installations

Verifier la presence de chaque element :
- **Commandes** : chercher le fichier dans `.claude/commands/` du projet courant
- **Skills** : chercher le dossier dans `~/.claude/skills/`

Utiliser ces commandes pour scanner :
```bash
# Commandes installees sur le projet
ls .claude/commands/*.md 2>/dev/null | xargs -I{} basename {} .md

# Skills installes globalement
ls -d ~/.claude/skills/*/ 2>/dev/null | xargs -I{} basename {}
```

### 2. Afficher le catalogue

Afficher le catalogue ci-dessous en remplacant chaque `{status}` par :
- `OK` si le fichier/dossier correspondant existe
- `-` si absent

---

## Catalogue Orni-Skills

### Commandes projet (installees dans `.claude/commands/`)

#### Gestion de projet
| Status | Commande | Description |
|--------|----------|-------------|
| {status} | `/update` | Met a jour Archon MCP et project-state.xml |
| {status} | `/followup` | Affiche etat du projet (Archon + XML) |
| {status} | `/followup-doctor` | Diagnostic coherence Archon / XML / fichiers |
| {status} | `/structure` | Restructureur de prompt professionnel |
| {status} | `/register-launcher` | Enregistre le projet dans orni-dashboard (systray) |

#### Communication inter-agents
| Status | Commande | Description |
|--------|----------|-------------|
| {status} | `/mail-send` | Envoie un message a un autre projet |
| {status} | `/mail-send-live` | Envoie et entre en conversation autonome |
| {status} | `/mail-read` | Lit les messages de la mailbox du projet |
| {status} | `/mail-read-live` | Ecoute et repond automatiquement |

#### ATeam (equipes d'agents)
| Status | Commande | Description |
|--------|----------|-------------|
| {status} | `/ateam` | Team Builder - compose et lance une equipe |
| {status} | `/ateam-council` | BMAD Council - deliberation collaborative |

#### Agent Browser
| Status | Commande | Description |
|--------|----------|-------------|
| {status} | `/setup-agent-browser` | Configure Agent-Browser sur Windows/WSL |

### Skills (installes dans `~/.claude/skills/`)

| Status | Skill | Description |
|--------|-------|-------------|
| {status} | `deploy` | Deploy & Publish — deploiement VPS + HTTPS Cloudflare |
| {status} | `vps` | VPS Management — acces SSH au serveur Hostinger |
| {status} | `cloudflare` | Cloudflare Management — DNS via API v4 |
| {status} | `excal-diagram` | Excalidraw Diagram — generation de diagrammes |
| {status} | `fal-image-gen` | Fal Image Gen — generation d'images via MCP |
| {status} | `mailbox` | Mailbox Inter-Projets — protocole de communication |
| {status} | `ateam` | ATeam — profils d'agents composables |
| {status} | `agent-browser` | Agent Browser — navigation web automatisee |
| {status} | `project-state-management` | Project State — gestion du contexte projet |
| {status} | `orni-installer` | Orni Installer — logique d'installation partagee |

### Commandes systeme Orni

Ces commandes sont toujours disponibles depuis le repo Orni-Skills :

| Commande | Description |
|----------|-------------|
| `/orni-help` | Affiche ce catalogue |
| `/orni-checkup` | Verifie si les modules installes sont a jour |
| `/orni-init-full` | Installe tous les modules (BMAD + options) |
| `/orni-update-full` | Met a jour tous les modules installes |

#### Modules individuels (init / update)

| Module | Init | Update |
|--------|------|--------|
| BMAD | `/orni-init-bmad` | `/orni-update-bmad` |
| Update/Followup | `/orni-init-uf` | `/orni-update-uf` |
| Agent Browser | `/orni-init-ab` | `/orni-update-ab` |
| ATeam | `/orni-init-at` | `/orni-update-at` |
| Project State Mgmt | `/orni-init-psm` | `/orni-update-psm` |
| VPS | `/orni-init-vps` | `/orni-update-vps` |
| Cloudflare | `/orni-init-cf` | `/orni-update-cf` |
| Deploy & Publish | `/orni-init-deploy` | `/orni-update-deploy` |
| fal-image-gen | `/orni-init-fal` | `/orni-update-fal` |
| Excalidraw | `/orni-init-excal` | `/orni-update-excal` |
| Mailbox | `/orni-init-ml` | `/orni-update-ml` |
