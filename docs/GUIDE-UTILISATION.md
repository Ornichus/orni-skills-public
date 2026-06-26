# Guide d'utilisation quotidien — Orni-Skills

> Ce guide explique comment utiliser Orni-Skills au quotidien, du plus important au moins important. Si tu n'as que 2 minutes, lis juste le [TL;DR](#tldr) et la section [Commandes du quotidien](#1-les-commandes-du-quotidien).

---

## TL;DR

> **Tu nettoies avec `/update-all` quand tu finis, tu redémarres avec `/followup` quand tu reprends. Pour choisir un outil, tu consultes le décisionnaire section 4.5. Pour choisir un framework (GSD / BMAD / Superpowers), tu consultes `skills/gsd/SKILL.md` section 1. Le reste, c'est du bonus.**

L'environnement Orni est un **écosystème modulaire** : ~22 modules + 3 frameworks spec-driven + hooks TTS/statusline/precompact + mémoire persistante cross-session (project-state.xml + MEMORY.md + mailbox). Les modules s'installent à la demande par projet via `/orni-init-<code>`. Le CLAUDE.md projet (généré par `/orni-init-claude-md`) oriente l'agent vers les bons outils selon le contexte.

---

## Sommaire

1. [Les commandes du quotidien](#1-les-commandes-du-quotidien)
2. [La reprise après pause](#2-la-reprise-après-pause)
3. [Workflow type d'une journée](#3-workflow-type-dune-journée)
4. [Les modules spécialisés](#4-les-modules-spécialisés)
5. [Bonnes pratiques](#5-bonnes-pratiques)
6. [Commandes avancées](#6-commandes-avancées)
7. [FAQ & dépannage](#7-faq--dépannage)

---

## 1. Les commandes du quotidien

Le cœur du système tourne autour de **trois commandes** qui synchronisent ton contexte entre les sessions Claude Code. Elles forment le protocole de base.

### `/update-state` — fin de session de travail

À lancer quand tu as fini un bout de travail significatif. Effets :

- Met à jour **Archon MCP** (les tâches du projet)
- Met à jour `project-state.xml` (état local du projet)
- Sauvegarde les 3 derniers messages de la conversation
- Backup automatique avant écrasement

**Quand l'utiliser ?** À chaque fois que tu finis une feature, un fix, ou avant un `/compact`.

### `/update-prd` — audit et propagation documentaire

Scanne la conversation complète, compare avec le code réel (git), tag chaque item, puis propage les changements dans la documentation d'architecture.

| Tag | Signification |
|-----|---------------|
| `[OK]` | Discuté et implémenté |
| `[NON IMPLEMENTE]` | Discuté mais absent du code |
| `[PARTIEL]` | Implémentation incomplète |
| `[DECISION]` | Choix architectural documenté |
| `[DIFFERE]` | Reporté explicitement |
| `[RETIRE]` | Feature supprimée |

Les items sont propagés dans :

- `docs/product-specification.md`
- `docs/prd.md`
- `docs/architecture.md`

**Quand l'utiliser ?** En fin de session où tu as pris des décisions d'architecture, ajouté des features, ou modifié des contraintes.

### `/update-all` — le combo

Exécute `/update-state` puis `/update-prd` en séquence. **C'est la commande à privilégier** avant un `/compact` ou en fin de grosse session.

```bash
/update-all
```

> **Règle d'or** : toujours `/update-all` avant un `/compact`. Sinon tu perds le contexte après compactage.

---

## 2. La reprise après pause

### `/followup` — rechargement du contexte

Après un `/compact` ou au début d'une nouvelle session, `/followup` lit `project-state.xml` et te ramène dans le contexte. Il rappelle :

- L'objectif en cours
- Les tâches en attente
- Les 3 derniers messages échangés
- Les milestones atteints

**Variantes** :

| Commande | Usage |
|----------|-------|
| `/followup` | État complet (défaut) |
| `/followup-state` | Juste l'état projet |
| `/followup-prd` | Juste la doc |
| `/followup-full` | Tout + détails |

### `/followup-doctor` — diagnostic de cohérence

Vérifie la cohérence entre Archon MCP et `project-state.xml`. À lancer si tu soupçonnes une désynchronisation (ex : tâches qui disparaissent, statut incohérent).

---

## 3. Workflow type d'une journée

```
┌─────────────────────────────────────────┐
│  Matin      →  /followup                │  Reprise du contexte
│  Travail    →  Tu itères avec Claude    │  Production
│  Pause      →  /update-all              │  Sauvegarde avant compact
│  Reprise    →  /followup                │  Rechargement
│  Fin journée → /update-all              │  Sync finale
└─────────────────────────────────────────┘
```

### Exemple concret

```bash
# Matin, nouvelle session Claude Code
/followup
# → "Tu étais sur la feature X, étape 3/5, dernière décision Y..."

# Tu bosses 2 heures, tu finis la feature
/update-all
# → Archon task marquée done, project-state.xml à jour, doc propagée

# Tu lances /compact pour libérer du contexte
/compact

# Tu continues sur une autre feature
/followup
# → Contexte restauré depuis project-state.xml
```

---

## 4. Les modules spécialisés

Orni-Skills est modulaire. Chaque projet installe uniquement les modules dont il a besoin via `/orni-init-<code>`.

### Installation complète (recommandée)

```bash
/orni-init-full   # bootstrap BMAD + UF + AB + AT + ML + Ralph + opt-in (VPS/FAL/CF/EX/DPL/FS/DS/WPC) + MP/AR/PSS par défaut
```

### Catalogue modules — par catégorie

#### Tracking, mémoire & meta (installés par défaut)

| Code | Commande | Module | Usage |
|------|----------|--------|-------|
| **UF** | `/orni-init-uf` | Update / Followup | Sync Archon MCP + project-state.xml + 3 derniers messages. **Cœur du protocole de session**. |
| **PSS** | `/orni-init-pss` | Project Status Snapshot | Rapport JSON + humain 4 sections, regen via `/orni-status`. |
| **AR** | `/orni-init-archi` | Architecture Relationnelle | Cartographie composants + relations + ADRs. |
| **ML** | `/orni-init-ml` | Mailbox inter-projets | Messagerie asynchrone entre projets via `~/.claude/mailbox/`. |
| **CLA** | `/orni-init-claude-md` | CLAUDE.md template Orni | Bootstrap CLAUDE.md projet DENSE-POINTEURS (framework + modules + tech stack). |
| **TO** | `/orni-init-to` | Task Orchestrator | Méta-orchestrateur sur GSD/BMAD/Superpowers — inventory + DAG waves + routing framework + KPIs typés + `/goal` autonome. |

#### Frameworks spec-driven (1 par session, mutuellement exclusifs)

| Code | Commande | Framework | Quand l'utiliser |
|------|----------|-----------|------------------|
| **BMAD** | (inclus dans `/orni-init-full`) | BMAD Method | Specs locked-in / CRM / SaaS B2B / community / migration legacy / e-commerce classique. |
| **GSD** | `/orni-init-gsd` | Get Shit Done | MVP exploratoire / requirements shift / outil interne / hackathon / side-project. |
| (global) | (plugin global) | Superpowers | TDD edge cases / actions irréversibles / paiement / IA agentique / pipeline data critique / API publique. |

> **Décisionnaire complet** : `skills/gsd/SKILL.md` section 1. Règle d'or : 1 framework par session.

#### Présentation & Design

| Code | Commande | Module | Usage |
|------|----------|--------|-------|
| **MP** | `/orni-init-mp` | Marp Presentations | Decks HTML reproductibles avec thème HSL paramétrique (slides versionnés). |
| **FS** | `/orni-init-fs` | Frontend Slides | Decks one-shot premium (pitch, brand mockups, animations CSS riches). Complémentaire à MP. |
| **DS** | `/orni-init-ds` | Design System | Extract brand depuis URL/screenshot → `design-system.html` scrollable + `brand-book-a4.pdf` print-ready. |
| **EX** | `/orni-init-excal` | Excalidraw Diagram | Diagrammes visuels Excalidraw stylisés. |

#### Médias & contenu

| Code | Commande | Module | Usage |
|------|----------|--------|-------|
| **FAL** | `/orni-init-fal` | Fal Image Gen | Génération d'images via fal.ai (MCP). |
| **WPC** | `/orni-init-wpc` | Web PDF Compile | Capture articles web → PDF dossier groupé par pays/catégorie (revue de presse, bibliographie). |

#### Infrastructure & Déploiement

| Code | Commande | Module | Usage |
|------|----------|--------|-------|
| **VPS** | `/orni-init-vps` | VPS Management | SSH + MCP Hostinger pour gestion serveurs distants. |
| **CF** | `/orni-init-cf` | Cloudflare Management | DNS + Workers + Pages via API Cloudflare. |
| **DPL** | `/orni-init-deploy` | Deploy & Publish | Déploiement automatisé VPS + Cloudflare + HTTPS Let's Encrypt. **Requiert VPS + CF**. |

#### Agents & orchestration

| Code | Commande | Module | Usage |
|------|----------|--------|-------|
| **AT** | `/orni-init-at` | ATeam (Team Builder + Council) | Composition d'équipes d'agents pour délibération (BMAD Council). |
| **AB** | `/orni-init-ab` | Agent Browser | Automation web Chrome via extension Native Messaging Host. |

#### Standalone-only (hors pipeline `/orni-init-full`)

> Ces modules ne sont **pas installés** par `/orni-init-full` — par choix design, pas par oversight.

| Code | Commande | Module | Raison standalone |
|------|----------|--------|-------------------|
| **MB** | `/orni-init-mb` | Multi-Backend | Helper PowerShell global (`cdsp`/`odsp` pour Anthropic native / OpenRouter). Setup machine. |

### Vérifier l'état des modules

```bash
/orni-checkup       # versions installées vs source Orni-Skills
/orni-help          # catalogue complet commandes + skills
/orni-status        # snapshot projet (JSON + rapport humain)
```

### Mettre à jour

```bash
/orni-update-full           # tous les modules installés
/orni-update-<code>         # ciblé (e.g. /orni-update-fs, /orni-update-mp)
```

---

## 4.5 Décisionnaire par cas d'usage quotidien

> Cherche ton cas, lis la solution. Si rien ne matche : `/orni-help` pour le catalogue complet.

### Documents & présentations

| Besoin | Solution recommandée |
|--------|----------------------|
| Présentation client/partenaire stylée, one-shot, brand mockups premium | `/frontend-slides` (avec `--style {nom}` si brand existant) |
| Deck reproductible, versionné, multi-thèmes HSL (rapport, formation) | `/marp-slides` |
| Brand book A4 print-ready + design system page scrollable | `/design-system` (extract brand depuis URL/screenshot) |
| Compiler 5-15 articles web → PDF dossier (revue de presse, dossier d'enquête) | `/web-pdf-compile` |
| Diagrammes Excalidraw stylisés | `/excal-diagram` |
| Diagrammes Mermaid intégrés (flowchart/sequence/gantt/etc.) | section Mermaid dans `/marp-slides` ou `/frontend-slides` v1.4.0+ |

### Code & développement

| Besoin | Solution recommandée |
|--------|----------------------|
| Démarrer nouveau projet exploratoire (MVP, side-project, POC) | `/orni-init-full` + `/orni-init-gsd` + `/gsd-new-project` |
| Démarrer nouveau projet conventionnel (CRM, SaaS, community) | `/orni-init-full` (BMAD inclus) + `/bmad-help` pour workflow |
| Refactor module critique (paiement, IA agentique, pipeline data) | Superpowers (plugin global) : `brainstorming` → `writing-plans` → `test-driven-development` |
| Reprendre projet existant après pause | `/followup` (recharge contexte depuis project-state.xml) |
| Finir une feature, avant `/compact` | `/update-all` (Archon + state + audit + propagation doc) |
| Audit conversation vs code | `/update-prd` (38+ items typés OK/PARTIEL/NON IMPLEMENTE/DECISION/DIFFERE/RETIRE) |
| Diagnostic incohérence Archon ↔ state.xml | `/followup-doctor` |

### Infrastructure & ops

| Besoin | Solution recommandée |
|--------|----------------------|
| Déployer une app web (FastAPI/Next.js) sur VPS | `/orni-init-deploy` (requiert VPS + CF déjà installés) puis `/deploy` |
| Gérer DNS Cloudflare (créer record, route Worker) | `/orni-init-cf` puis `/cloudflare` |
| Setup helper PowerShell `cdsp`/`odsp` pour backend choice (Anthropic vs OpenRouter) | `/orni-init-mb` |

### Communication & orchestration

| Besoin | Solution recommandée |
|--------|----------------------|
| Envoyer un message vers un autre projet Orni | `/mail-send {projet} {sujet}` |
| Conversation autonome agent-à-agent entre 2 projets | `/mail-send-live` ou `/mail-read-live` |
| Composer équipe d'agents pour décision complexe | `/ateam suggest` puis `/ateam-council` |
| Brainstorming structuré avant code | skill `superpowers:brainstorming` (plugin global) |
| Génération image illustrative | `/orni-init-fal` puis `mcp__fal-image-gen__generate_image` |

### Maintenance & meta

| Besoin | Solution recommandée |
|--------|----------------------|
| Bootstrap CLAUDE.md projet selon framework/modules | `/orni-init-claude-md` |
| Orchestrer tâches en waves parallèles + routing framework + KPIs + `/goal` autonome | `/orchestrate` (skill `task-orchestrator`, install via `/orni-init-to`) |
| Update tous les modules au plus récent | `/orni-update-full` |
| Vérifier versions installées vs source | `/orni-checkup` |
| Enregistrer projet dans dashboard systray (orni-dashboard) | `/register-launcher` |
| Statusline barre de statut + pace calculator | `/orni-init-statusline` |

---

## 5. Bonnes pratiques

### À faire

✅ **`/update-all` avant tout `/compact`** — sinon perte de contexte  
✅ **Laisser Archon MCP gérer les tâches** — pas de fichiers TODO manuels  
✅ **Faire confiance au système de backup** — `_backup/` est créé automatiquement  
✅ **Lire `CLAUDE.md` du projet au démarrage** — contient les règles spécifiques  
✅ **Surveiller le statusline** — le pace calculator alerte si tu consommes trop de contexte  
✅ **Installer les modules à la demande** — pas besoin de `/orni-init-full` systématiquement

### À éviter

❌ **Éditer `project-state.xml` à la main** — passer par `/update-state`  
❌ **Compacter sans update préalable** — le contexte se perd  
❌ **Ignorer les alertes du statusline** — pace trop rapide = contexte qui se remplit  
❌ **Modifier les fichiers `_backup/`** — ils sont écrasés à chaque update  
❌ **Mélanger les workflows** — si tu utilises BMAD, utilise BMAD ; sinon, reste sur le protocole Orni

---

## 6. Commandes avancées

### Frameworks spec-driven (BMAD / GSD / Superpowers)

Orni-Skills permet la cohabitation de **3 frameworks spec-driven** dans son écosystème — mais 1 seul par session (mutuellement exclusifs).

**BMAD** — embarqué dans `/orni-init-full`, adapté aux projets conventionnels (CRM, SaaS B2B, community, migration legacy, e-commerce classique) :
- `/bmad-agent-*` — invoquer des agents spécialisés
- `/bmad-bmm-*` — workflows de développement (PRD, stories, sprints)
- `/bmad-cis-*` — brainstorming, storytelling, design thinking
- `/bmad-tea-*` — architecture de tests

**GSD (Get Shit Done)** — install global `npx get-shit-done-cc@latest --claude --global`, adapté aux MVP exploratoires / requirements shift / outil interne / side-project :
- Loop 6 commandes : `/gsd-new-project` → `/gsd-discuss-phase` → `/gsd-plan-phase` → `/gsd-execute-phase` → `/gsd-verify-work` → `/gsd-ship`
- Artifacts `.planning/` (PROJECT/REQUIREMENTS/ROADMAP/STATE + phases/<N>/)
- Bootstrap projet : `/orni-init-gsd`

**Superpowers** — plugin Claude Code global, adapté aux actions irréversibles / paiement / IA agentique / pipeline critique / refactor financier :
- Skills à invoquer : `superpowers:brainstorming`, `superpowers:writing-plans`, `superpowers:test-driven-development`, `superpowers:systematic-debugging`, `superpowers:executing-plans`, `superpowers:dispatching-parallel-agents`
- Artifacts : git worktrees + `plans/` markdown

> **Décisionnaire complet** : `skills/gsd/SKILL.md` section 1. Règle d'or : 1 framework par session. Mix possible entre sessions (MVP GSD → refactor critique Superpowers nouvelle session).
> **Quand n'utiliser AUCUN framework ?** Scripts utilitaires, pages statiques, features triviales → direct Claude Code, pas de framework.

### Agent Browser

Si tu développes du front et que tu veux des screenshots réels (vrai navigateur, vraie résolution) :

```bash
/setup-agent-browser
```

### Structure de prompt

Pour transformer un prompt flou en prompt structuré (format CO-STAR+) :

```bash
/structure
```

---

## 7. FAQ & dépannage

### "Mon contexte Claude Code se remplit trop vite"

→ Lance `/update-all` puis `/compact`. Le statusline indique quand tu approches de la limite.

### "Archon MCP échoue avec 'Failed to reconnect'"

→ Voir `~/.claude/docs/archon-mcp-troubleshooting.md` (laptop) ou redémarrer Docker Desktop.

### "project-state.xml a disparu"

→ Vérifier `_backup/project-state/current/project-state_latest.xml` (backup automatique).

### "Je ne sais plus quelle commande utiliser"

→ `/orni-help` affiche le catalogue complet.

### "Comment désinstaller un module ?"

→ Pas de commande dédiée. Supprimer manuellement les fichiers du module dans le projet (les modules sont copiés, pas liés).

### "Le statusline ne s'affiche pas"

→ `/orni-init-statusline` pour l'installer, puis redémarrer Claude Code.

### "Je veux contribuer / ajouter un skill"

→ Voir `CLAUDE.md` à la racine du repo. Les skills vivent dans `skills/`, les commandes dans `commands/`.

---

## Aller plus loin

- **Catalogue complet** : `/orni-help` ou [README.md](../README.md)
- **Index des skills** : [SKILLS-INDEX.md](../SKILLS-INDEX.md)
- **Configuration avancée** : [settings-template.json](../settings-template.json)
- **Architecture du repo** : section "Structure du repo" du [README.md](../README.md)

---

## Architecture de l'environnement Orni

Pour les agents qui veulent comprendre l'écosystème complet (pas juste les commandes) :

### Couches de l'écosystème

```
┌─────────────────────────────────────────────────────────────┐
│ Frameworks spec-driven : GSD / BMAD / Superpowers           │  ← 1 par session
├─────────────────────────────────────────────────────────────┤
│ Modules Orni-Skills (skills + commandes) : ~22 modules      │  ← installables /orni-init-*
├─────────────────────────────────────────────────────────────┤
│ Mémoire persistante : project-state.xml + MEMORY.md +       │  ← per-projet + global
│   ~/.claude/mailbox/ + Archon MCP                           │
├─────────────────────────────────────────────────────────────┤
│ Meta-commandes : orni-help / orni-checkup /                 │  ← maintenance
│   orni-init-full / orni-update-full / register-launcher     │
├─────────────────────────────────────────────────────────────┤
│ Hooks (TTS Stop / PreCompact / Statusline / SessionStart)   │  ← background
├─────────────────────────────────────────────────────────────┤
│ CLAUDE.md (global ~/.claude/CLAUDE.md + projet)             │  ← instructions agent
├─────────────────────────────────────────────────────────────┤
│ Claude Code CLI / Desktop / Web / IDE extensions            │  ← interface
└─────────────────────────────────────────────────────────────┘
```

### Anatomie d'un projet Orni

```
mon-projet/
├── .claude/
│   ├── commands/              # Commandes /orni-* + /bmad-* copiées
│   ├── skills/                # Skills installés (FS, DS, MP, etc.)
│   ├── orni-manifest.json     # Versions modules installés
│   └── settings.local.json    # Settings machine (gitignored)
├── _bmad/                     # BMAD core + modules (si BMAD)
├── _bmad-output/              # BMAD outputs (si BMAD)
├── .planning/                 # GSD artifacts (si GSD)
├── _backup/                   # Backup auto project-state.xml (gitignored)
├── docs/
│   ├── _backup/audit-reports/ # Rapports /update-prd
│   └── ...                    # Doc projet (prd.md, architecture.md, etc.)
├── CLAUDE.md                  # Instructions agent projet (généré /orni-init-claude-md)
├── project-state.xml          # État projet persistant
├── MEMORY.md                  # Mémoire utilisateur cross-session (optionnel, géré par auto-memory)
└── ...                        # Code projet
```

### Sources de vérité

| Sujet | Source |
|-------|--------|
| Style communication, vulgarisation, caveman policy, browser policy | `~/.claude/CLAUDE.md` global |
| Framework choisi pour ce projet + modules installés | `CLAUDE.md` projet (généré `/orni-init-claude-md`) |
| Tâches en cours + état projet | Archon MCP + `project-state.xml` |
| Décisions / lessons learned cross-session | `MEMORY.md` (auto-memory) + `~/.claude/memory/` |
| Décisionnaire framework (GSD/BMAD/Superpowers) | `skills/gsd/SKILL.md` section 1 |
| Catalogue commandes Orni complet | `/orni-help` ou `commands/orni-help.md` |
| Versions installées par projet | `.claude/orni-manifest.json` |
| Communication inter-projets | `~/.claude/mailbox/{projet}/` |

---

*Dernière mise à jour : 2026-05-17 (session 021 — ajout FS/DS/WPC/MB/GSD/CLA + décisionnaire par cas d'usage + architecture environnement)*
