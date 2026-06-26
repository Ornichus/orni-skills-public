# ATeam - Team Builder Intelligent

Commande `/ateam` pour composer et lancer des equipes d'agents Claude Code.

## Usage rapide

```bash
# Dev + testeur browser (le plus courant)
/ateam go test dev

# Suggestion automatique basee sur le contexte
/ateam suggest

# Recherche pure
/ateam go research

# Equipe frontend complete
/ateam go dev-front test-front --url http://192.168.1.50:5173

# Full stack avec iteration
/ateam go dev-front dev-back test --iterate
```

## Roles disponibles

| Role | Description | Outils principaux |
|------|-------------|-------------------|
| `test` | Testeur browser (agent-browser + screenshots) | Bash (wsl), Read |
| `test-front` | Alias de test | idem |
| `test-back` | Testeur API (curl, validation) | Bash (curl, jq) |
| `dev` | Developpeur general | Tous |
| `dev-front` | Developpeur frontend | Tous |
| `dev-back` | Developpeur backend | Tous |
| `research` | Recherche (codebase, web, docs) | Read, Grep, WebSearch |

## Options

| Option | Description |
|--------|-------------|
| `--url <url>` | URL cible pour tests browser |
| `--scope <s>` | Perimetre: frontend/backend/integration/all |
| `--iterate` | Mode iterate-test-fix en boucle |
| `--name <nom>` | Nom de l'equipe (defaut: auto) |
| `--tasks` | Charger les taches depuis project-state.xml |

## Prerequis

- **Module AB** (Agent Browser) requis pour le role `test`/`test-front`
- WSL + agent-browser configures (`/setup-agent-browser`)

## Council - Deliberation collaborative

Commande `/ateam-council` pour invoquer un council de vrais agents BMAD qui deliberent, reviewent et debattent.

**Pipeline:** `/ateam-council` (deliberation) -> Plan Mode (planification) -> `/ateam go` (implementation)

### Usage rapide

```bash
# Suggestion automatique (analyse le sujet, propose les agents)
/ateam-council "faut-il migrer vers TypeScript?"

# Review d'un PRD avec scenario pre-configure
/ateam-council --scenario prd-review _bmad-output/prd.md

# Debat architecture avec agents forces
/ateam-council debate "monolith vs microservices" --agents architect,dev,tea

# Brainstorm creatif (3 tours)
/ateam-council --scenario brainstorm "gamification de l'onboarding"

# Pipeline complet: council -> rapport -> plan mode
/ateam-council debate "auth strategy" --plan --output council-auth.md
```

### Modes d'interaction

| Mode | Description | Format de reponse |
|------|-------------|-------------------|
| `round-table` | Table ronde libre (defaut) | Position + raisonnement + questions |
| `debate` | Debat structure avec arguments | These + 3 arguments + anticipation |
| `review` | Revue d'un document | Points + / - / revisions + verdict |
| `advisory` | Consultation experte | Recommandation + justification + risques |

### Scenarios pre-configures

| Scenario | Agents | Mode | Rounds |
|----------|--------|------|--------|
| `prd-review` | pm, analyst, ux-designer, architect | review | 2 |
| `arch-decision` | architect, dev, tea, qa | debate | 3 |
| `sprint-planning` | sm, dev, pm, qa | round-table | 2 |
| `brainstorm` | brainstorming-coach, creative-problem-solver, innovation-strategist | round-table | 3 |
| `doc-review` | tech-writer, architect, pm | review | 2 |
| `course-correction` | pm, architect, sm, dev | advisory | 2 |
| `ux-review` | ux-designer, pm, analyst | review | 2 |
| `test-strategy` | tea, qa, architect, dev | advisory | 2 |

### Options

| Option | Description |
|--------|-------------|
| `--agents <liste>` | Forcer des agents (noms CSV: architect,pm,analyst) |
| `--rounds <n>` | Nombre de tours (defaut: 2, max: 5) |
| `--size <n>` | Taille du council (defaut: 3, max: 7) |
| `--supervisor` | Activer superviseurs (auto si size >= 5) |
| `--scenario <nom>` | Charger un scenario pre-configure |
| `--output <fichier>` | Sauvegarder le rapport final |
| `--plan` | Enchainer vers Plan Mode apres le council |
| `--tasks` | Charger les taches de project-state.xml comme contexte |

### Superviseurs

Pour les councils de 5+ agents, des superviseurs synthetisent les reponses de sous-groupes avant d'envoyer au lead. Structure:

```
Lead (orchestrateur)
├── Superviseur Technique (ex: architect)
│   ├── dev, tea, qa
└── Superviseur Produit (ex: pm)
    ├── analyst, ux-designer
```

---

## Fichiers

| Fichier | Description |
|---------|-------------|
| `commands/ateam.md` | Commande Team Builder (prompt du lead) |
| `commands/ateam-council.md` | Commande Council (prompt du lead) |
| `skills/ateam/SKILL.md` | Profils d'agents composables (Team Builder) |
| `skills/ateam/COUNCIL.md` | Templates et protocoles (Council) |
| `skills/ateam/council-scenarios.md` | Scenarios pre-configures (Council) |
| `skills/ateam/README.md` | Ce fichier |

## Installation

```bash
/orni-init-at    # Premiere installation
/orni-update-at  # Mise a jour
```
