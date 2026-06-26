---
description: 'Meta-orchestrateur tâches — inventory + organize + route + visualize + execute + goal. Sit au-dessus de GSD/BMAD/Superpowers.'
---

# /orchestrate — Task Orchestrator entry point

Charge le skill `task-orchestrator` et exécute le sous-mode demandé.

## Usage

```bash
/orchestrate [mode] [flags]
```

## Modes

| Mode | Effet |
|------|-------|
| (aucun) | `visualize` (vue état seule, read-only) |
| `inventory` | Scan + merge dedup tâches (Archon + state.xml + conv + git) |
| `organize` | DAG dépendances + waves parallèles/séquentielles |
| `route` | Recommande framework + skill/tool par tâche |
| `visualize` | Compose vue user (table + KPIs + Gantt ASCII) |
| `execute [flags]` | Lance les waves |
| `goal [flags]` | Génère + set `/goal <condition>` (<4k chars) |

## Flags

| Flag | Effet |
|------|-------|
| `--auto` | Sans confirm, blind execution |
| `--confirm-wave` (default execute) | Pause entre waves, valide user |
| `--confirm-task` | Confirm chaque tâche (prudent) |
| `--dry-run` | Visualize seul, no execute |
| `--bound=<N>turns` ou `--bound=<T>h` | Injection dans `/goal` condition |
| `--framework=GSD\|BMAD\|Superpowers\|aucun` | Force framework dominant (résout conflit 1-par-session) |
| `--include-code-todos` | Inclut TODO/FIXME scan dans inventory (bruyant) |
| `--split` | Split en 2+ goals si >4000 chars condition |

## Instructions

1. **Charger le skill :**
   - Lire `~/.claude/skills/task-orchestrator/SKILL.md` (ou source path Orni si projet sans skill installé)
   - Le skill décrit l'algorithme complet pour chaque sous-mode

2. **Identifier le mode demandé** depuis `$ARGUMENTS`. Si vide → `visualize`.

3. **Exécuter le sous-mode** en suivant l'algorithme du skill :
   - `inventory` : scan 5 sources + dedup → output JSON interne
   - `organize` : DAG + waves → output structure waves
   - `route` : pattern match framework + tool par tâche
   - `visualize` : compose vue user finale (markdown table + KPIs + Gantt)
   - `execute` : applique flags + dispatch via `superpowers:dispatching-parallel-agents` + worktrees via `superpowers:using-git-worktrees`
   - `goal` : compose prompt <4k chars via template + appelle `/goal "<composed>"`

4. **Persistance :**
   - Sauvegarder l'inventaire courant dans `.orchestrate/state.json` (gitignored)
   - KPIs custom paramétrés par user dans `.orchestrate/kpis.yaml`

5. **Rapport final :**
   - Format selon mode (table inventory, DAG organize, etc.)
   - Toujours inclure KPIs synthétiques (parallélisme %, framework distribution, ETA)
   - Si `execute` ou `goal` : confirmer lancement avant action irréversible

## Notes

- **Pré-requis** : ce projet doit avoir au moins Archon MCP configuré ET `project-state.xml` présent. Sinon `inventory` retombe sur conversation + git seulement.
- **Worktrees** : skill auto-crée `.worktrees/` (gitignored) pour wave parallèle code. Cleanup auto post-wave si KPIs OK.
- **Goal** : requiert Claude Code v2.1.139+. Si version inférieure, fallback message "use --auto execute instead".
- **Synergie** : skill lit `CLAUDE.md` projet pour décisionnaire local + `{ORNI}/docs/GUIDE-UTILISATION.md` §4.5 + `{ORNI}/skills/gsd/SKILL.md` §1. Zéro duplication.

## Exemple workflow type

```bash
# Vue état sans rien lancer
/orchestrate

# Si OK, lance avec confirm entre waves
/orchestrate execute --confirm-wave

# OU mode autonome via /goal
/orchestrate goal --bound=30turns
```

## Référence

Voir skill complet : `skills/task-orchestrator/SKILL.md`.
