---
name: task-orchestrator
description: Meta-orchestrateur sur GSD/BMAD/Superpowers. Inventorie les tâches (Archon + state.xml + conversation + git), les organise en waves parallèles/séquentielles, route chaque tâche vers le bon framework selon décisionnaire Orni, visualise avec KPIs typés (validation/valeur/custom), exécute via subagents + worktrees, et peut générer un prompt /goal <4k chars pour boucle autonome.
---

# Task Orchestrator — Skill méta-orchestrateur Orni

**Version:** 1.0.0

## Overview

Skill **chef d'orchestre** qui sit au-dessus de GSD / BMAD / Superpowers. Sans lui, l'utilisateur décide frame-by-frame quel framework + quel outil. Avec lui, le skill décide selon le décisionnaire Orni intégré (`CLAUDE.md` projet DENSE v2.0 + `docs/GUIDE-UTILISATION.md` §4.5 + `skills/gsd/SKILL.md` §1).

**Synergie session 021** : zéro duplication. Le skill **lit** les sources canoniques + applique la logique. Cohérent avec philosophie DENSE-POINTEURS.

**Use cases** :
- "Inventorie tout ce qui reste à faire et organise"
- "Lance tout en parallèle, 0 conflit"
- "Génère un /goal pour finir cette session sans que je doive prompt chaque étape"
- "Visualise l'état d'avancement avec KPIs"

## When to Use

Invoquer ce skill quand :
- 3+ tâches identifiées (sinon overkill — `superpowers:dispatching-parallel-agents` direct)
- Mix de tâches de types différents (code + doc + audit + déploiement)
- Besoin de routage framework (GSD/BMAD/Superpowers/aucun) par tâche
- Avant de lancer une session de travail substantielle

**Skip** si :
- 1 tâche unique simple → faire direct
- Tâches toutes identiques → `dispatching-parallel-agents` suffit
- Pas de mémoire persistante voulue → faire en chat normal

## Entry Point

**Commande :** `/orchestrate [mode] [flags]`

| Mode | Effet |
|------|-------|
| `/orchestrate` (sans arg) | Équivalent `visualize` — vue état seule |
| `/orchestrate inventory` | Scan + merge dedup 5 sources |
| `/orchestrate organize` | Analyse dépendances + DAG waves |
| `/orchestrate route` | Match framework + tool per tâche |
| `/orchestrate visualize` | Compose tout en vue user (table + KPIs + Gantt) |
| `/orchestrate execute [flags]` | Lance les waves |
| `/orchestrate goal [flags]` | Génère + set `/goal` condition <4k chars |

**Flags execute + goal :**

| Flag | Effet |
|------|-------|
| `--auto` | Lance toutes les waves sans pause |
| `--confirm-wave` (default) | Pause entre waves, valide user |
| `--confirm-task` | Confirme chaque tâche (ultra-prudent) |
| `--dry-run` | Visualize seul, no execute |
| `--bound=20turns` ou `--bound=2h` | Injection dans `/goal` condition |
| `--framework=X` | Force framework dominant (résout conflits 1-par-session) |
| `--include-code-todos` | Inclut TODO/FIXME scan dans inventory (bruyant) |

---

## Sous-mode 1 — Inventory

Scanne et merge 5 sources avec déduplication intelligente.

### Sources

| Source | Méthode | Notes |
|--------|---------|-------|
| **Archon MCP** | `mcp__archon__find_tasks(filter_by=status, filter_value=todo)` + `doing` + `review` | Source de vérité tâches structurées |
| **project-state.xml** | Parse `<tasks status="todo">` + `<pending-followup>` | Tâches projet persistantes |
| **Conversation courante** | Heuristic — phrases user "à faire / TODO / il faut / ensuite", listes numérotées | Volatile, prio basse |
| **git status** | `git status --short` + `git diff --stat` | WIP signals (uncommitted) |
| **TODO/FIXME code** (opt-in `--include-code-todos`) | Grep `TODO\|FIXME\|XXX` | Bruyant, à filtrer manuellement |

### Algorithme dedup (Q2 user = C : merge intelligent)

```
1. Charger toutes les tâches de toutes les sources
2. Normaliser titres (lowercase, remove stopwords, strip ponctuation)
3. Pour chaque paire (A, B) :
   - Si A.archon_id == B.archon_id → merge (Archon source)
   - Si Levenshtein(A.title_normalized, B.title_normalized) ratio > 0.7 → merge candidate
4. Pour chaque merge candidate, résoudre :
   - Si A.source = archon, B.source = state-xml → garde A, ajoute "also in state-xml"
   - Si A.source = conversation, B.source = archon → garde B (Archon prime)
   - Statut : précédence Archon doing > Archon todo > state.xml todo > conv mention
5. Output : liste typée flat avec `sources: [...]` indiqué
```

### Output (format JSON interne, présenté en table par `visualize`)

```yaml
tasks:
  - id: "fix-tva-arrondi"
    title: "Fix bug TVA arrondi multi-lignes"
    status: "todo"
    sources: ["archon:9ae3f0db", "conv:msg-5"]
    priority: "high"
```

---

## Sous-mode 2 — Organize

Analyse dépendances + détecte conflits + compose waves.

### Détection dépendances

| Type | Détection | Effet |
|------|-----------|-------|
| **Hard dependency** | Tâche A mentionne explicitement B dans description | A bloque B (sequential) |
| **File conflict** | A et B modifient même fichier (depuis `files_touched` ou heuristic du titre) | Split en sequential dans même wave |
| **Resource conflict** | A et B utilisent même port / DB / VPS / branche | Sequential |
| **Framework conflict** | A demande GSD + B demande Superpowers dans **même session** | Bloquant ou split en 2 sessions |
| **State.xml conflict** | A et B modifient state.xml | Force sequential (1 seul peut écrire) |

### Algorithme DAG

```
1. Construire graphe orienté : tâches = nodes, dépendances = edges
2. Topological sort
3. Identifier waves : nodes au même "level" topologique sans conflit fichier/ressource
4. Pour chaque wave parallèle, vérifier worktree nécessaire (voir §Worktrees)
5. Pour chaque dépendance, marquer comme sequential post-wave
```

### Output

```yaml
waves:
  - id: "W1"
    type: "parallel"
    tasks: ["fix-tva", "update-readme", "compile-dossier"]
    estimated_min: 12
    worktrees_needed: ["fix-tva"]  # touche code; les 2 autres non
    files_touched_union: ["src/tva.py", "tests/", "README.md", "docs/dossiers/"]
  - id: "W2"
    type: "sequential"
    tasks: ["update-state", "commit", "push"]
    blocking_prior: ["W1"]
    estimated_min: 5
```

---

## Sous-mode 3 — Route

Pour chaque tâche, recommande framework + tool.

### Sources de vérité décisionnaire (consultées dans cet ordre)

1. **`CLAUDE.md` projet courant** (si présent) — table framework + tooling DENSE v2.0
2. **`{ORNI}/docs/GUIDE-UTILISATION.md` §4.5** — décisionnaire par cas d'usage
3. **`{ORNI}/skills/gsd/SKILL.md` §1** — décisionnaire framework détaillé

Où `{ORNI}` = `source_path` depuis `~/.claude/orni-skills.json`.

### Algorithme routing

```
Pour chaque tâche T :
  1. Match titre + description T contre patterns :
     - "MVP / exploratoire / requirements shift / hackathon" → GSD
     - "CRM / SaaS / community / migration legacy" → BMAD
     - "paiement / IA agentique / critique / refactor financier / pipeline data" → Superpowers
     - "script / page statique / fix trivial" → aucun (direct)
  2. Match besoin contre tooling table (présentation → /frontend-slides, etc.)
  3. Si ambigu, default au framework de la session courante OU demander user
  4. Détection conflit "1 par session" : si plusieurs frameworks détectés, raise warning
```

### Output

```yaml
routing:
  - task: "fix-tva-arrondi"
    framework: "Superpowers"
    primary_skill: "superpowers:test-driven-development"
    secondary_skills: ["superpowers:brainstorming", "superpowers:verification-before-completion"]
    rationale: "comptabilité = critique financièrement, TDD obligatoire"
  - task: "compile-dossier-presse"
    framework: "aucun"
    primary_tool: "/web-pdf-compile"
    rationale: "use-case direct compile articles → PDF, pas de framework requis"
```

---

## Sous-mode 4 — Visualize

Compose inventory + organize + route en vue claire user. **Mode par défaut quand `/orchestrate` invoqué sans arg.**

### Format output

```
=== ORCHESTRATION — Session 2026-XX-XX HH:MM ===

📋 Inventory (10 tâches après dedup)
  Sources: Archon 3 · state.xml 2 · conversation 5 · git 0 · code-todos 0
  Statuts: todo 7 · doing 2 · review 1

🔀 Routing
  Superpowers: 3  · GSD: 1  · BMAD: 0  · aucun: 6
  ⚠ Conflit "1 framework par session": NON (Superpowers seul session courante)

📊 Waves
  ┌─ W1 (parallèle, 0 conflit, ~12 min, 3 worktrees nécessaires) ───────┐
  │ #1 Fix bug TVA              [Superpowers TDD]       wt:.worktrees/fix-tva
  │ #2 Augment README           [aucun]                  in-place
  │ #3 Compile dossier presse   [aucun]                  in-place
  └───────────────────────────────────────────────────────────────────────┘
  ┌─ W2 (sequential — state.xml + git, ~5 min) ─────────────────────────┐
  │ #4 /update-state            blocking #5, #6
  │ #5 Commit atomique          blocking #6
  │ #6 Push origin/main         final
  └───────────────────────────────────────────────────────────────────────┘
  ┌─ W3 (long async via /goal, ~45 min) ────────────────────────────────┐
  │ #7 Refactor module paiement [Superpowers] /goal "..." bound=30turns
  └───────────────────────────────────────────────────────────────────────┘

📈 KPIs synthétiques
  Total: 10 tâches · Parallélisables: 6 (60%) · Séquentielles: 4
  Token budget estimé: ~150K (3 subagents 50K + main 30K + evaluator 5K)
  ETA: 17 min interactif + 45 min async
  Worktrees: 3 (auto-cleanup post-wave)

🎯 KPIs par tâche (échantillon)
  #1 Fix bug TVA
     Validation: test_tva_facture_5_lignes passes (binaire)
     Valeur:     tests_passing_ratio >=247/247  ·  écart facture == 0 cent
     Custom:     "pas de Float, Decimal partout dans calcul" (paramétré user)

[user] valider ? [y/n/edit/dry-run]
```

---

## Sous-mode 5 — Execute

Lance les waves en utilisant subagents (parallèle) + chaîne séquentielle + worktrees.

### Patterns utilisés (réutilisation skills existants)

| Pattern | Skill réutilisé |
|---------|-----------------|
| Worktree par tâche code | `superpowers:using-git-worktrees` |
| Subagent par tâche parallèle | `superpowers:dispatching-parallel-agents` |
| Verification end-of-task | `superpowers:verification-before-completion` |
| Code review interne | `superpowers:requesting-code-review` |
| Plan détaillé tâche | `superpowers:writing-plans` |
| TDD pour tâches code critiques | `superpowers:test-driven-development` |

**Le task-orchestrator ne RÉ-INVENTE PAS — il chaîne les skills existants.**

### Algorithme execution

```
Pour chaque wave W dans order(waves) :
  1. Si W.type == "parallel" :
     a. Pour chaque tâche T dans W :
        - Si T.worktree_needed : créer worktree via using-git-worktrees skill
        - Préparer prompt subagent spécifique (scope T, contraintes, KPIs)
     b. Dispatch parallèle via dispatching-parallel-agents skill
     c. Attendre tous subagents finis
     d. Verify : KPIs tâche par tâche (validation binaire + valeur metrics)
     e. Si --confirm-wave : pause + valide user
     f. Cleanup worktrees (merge OU drop selon choix user)
  2. Si W.type == "sequential" :
     a. Pour chaque tâche T dans W :
        - Si --confirm-task : pause + valide
        - Execute T (skill primary + secondary)
        - Verify KPIs
        - Commit atomique si applicable
  3. Sync intermédiaire : /update-state après chaque wave
```

### Gestion erreurs

| Erreur | Action |
|--------|--------|
| Subagent timeout | Retry 1× avec timeout doublé, sinon escalade user |
| KPI validation fail | Pause wave, demande user (continue / retry / skip / abort) |
| File conflict détecté à runtime | Stop wave, basculer sequential rest |
| Worktree creation fail | Fallback in-place + warning |
| /update-state fail | Stop tout, escalade user (state critique) |

---

## Sous-mode 6 — Goal

Génère un prompt `/goal` condition **<4000 chars** depuis l'état orchestré.

### Référence `/goal` Anthropic (v2.1.139+)

- Session-scoped, pas background
- Évaluateur (Haiku) lit conversation après chaque turn → décide si condition met
- Si non met → auto re-itère
- Si met → clear auto
- Condition doit décrire ce que Claude **prouve dans le transcript**
- 4000 chars max

### Template composer

```text
GOAL: <one measurable end state>

PROOF (must appear in conversation):
  Validation KPIs (binary pass/fail):
  - <kpi 1>
  - <kpi 2>
  Value KPIs (quantitative):
  - <metric> = <target>
  - <metric> = <target>
  Custom KPIs:
  - <description + proof>

CONSTRAINTS:
- 1 framework per session: <Framework> only
- No edit to <protected resources> outside <command>
- Atomic commits, conventional format
- <other constraints>

WORKFLOW (waves from /orchestrate organize):
W1 parallel (~Xmin): <task list>
  → for each: <skill chain>
W2 sequential after W1: <task list>
W3 (manual user, not in goal): <task list>

BOUND: stop after <N> turns OR <T> elapsed, whichever first.
COMMIT EACH: <wave-end | task-end>
SYNC: /update-state after each wave.
```

### Algorithme

```
1. inventory + organize + route (si pas déjà fait)
2. Pour chaque tâche, extraire :
   - Validation KPIs (binary) → "PROOF Validation"
   - Value KPIs (quantitative) → "PROOF Value"
   - Custom KPIs paramétrés → "PROOF Custom"
3. Composer prompt avec template + injection KPIs
4. Vérifier char count < 4000
5. Si > 4000 :
   - Compresser : drop W3 si trop verbose, agréger constraints
   - Sinon : warning user (trop de tâches pour 1 goal, split en 2)
6. Si --bound spécifié, injecter clause "stop after N turns OR T elapsed"
7. Set /goal "<condition générée>"
```

### Estimation char budget typique

| Section | Chars typique |
|---------|---------------|
| GOAL header | ~150 |
| PROOF (5 tâches × 3 KPIs) | ~1200 |
| CONSTRAINTS (5 items) | ~400 |
| WORKFLOW (3 waves) | ~800 |
| BOUND + COMMIT + SYNC | ~150 |
| **Total typique** | **~2700** (marge 1300 sous 4000) |

Si >4000, message d'erreur "trop de tâches pour /goal unique, --split"

---

## KPIs typés (schema)

Chaque tâche peut avoir des KPIs des 3 types ci-dessous (mix possible).

### Type 1 — KPI Validation (binaire pass/fail)

Vérification que la tâche a été correctement exécutée et testée.

```yaml
validation:
  - condition: "test_tva_facture_5_lignes passes"
    proof: "pytest output shows 'test_tva_facture_5_lignes PASSED'"
    binary: true
  - condition: "lint clean"
    proof: "ruff check . exits 0"
    binary: true
```

### Type 2 — KPI Valeur (quantitative)

Métrique chiffrée avec target.

```yaml
value:
  - metric: "tests_passing_ratio"
    target: ">=247/247"
    proof: "pytest summary line"
    current: null
  - metric: "scrape_success_rate"
    target: ">=90%"
    proof: "log output 'X/Y sources captured'"
    current: null
  - metric: "build_time_seconds"
    target: "<60"
    proof: "time output"
    current: null
```

### Type 3 — KPI Custom (paramétrable user)

Critère métier spécifique au cas, paramétré manuellement.

```yaml
custom:
  - description: "écart facture multi-lignes == 0 cent"
    proof: "manual diff vs ground truth dataset"
  - description: "PDF dossier final contient les 13 sources sans doublon"
    proof: "compile-pdf output 'X sections compiled, 0 duplicates'"
```

### Paramétrage par user

Lors de l'inventory ou organize, l'utilisateur peut **paramétrer des KPIs spécifiques** à des tâches sensibles :

```
/orchestrate inventory
[output: liste tâches]

[user] Pour la tâche #1 fix-tva, ajoute KPI valeur :
"écart facture == 0 cent sur dataset 100 factures de test"

/orchestrate organize
[skill enregistre KPI custom pour tâche #1]
```

Stockage : `.orchestrate/kpis.yaml` (dir gitignored, regen-friendly).

---

## Worktrees integration

### Décision : worktree par tâche, oui ou non ?

| Situation | Décision |
|-----------|----------|
| Wave parallel + tâches modifient code différents fichiers | **1 worktree par tâche** (isolation pure) |
| Wave parallel + 2 tâches même fichier | **Sequential dans la wave** (pas de worktree pour ces 2, séquence) |
| Wave parallel + tâches read-only (audit, scan, doc lookup) | **Pas de worktree** (lecture safe) |
| Wave sequential | **1 worktree global** (optionnel — branche dédiée suffit souvent) |
| Tâche unique non parallèle | **Pas de worktree** (sauf si critique, user décide) |

### Workflow worktree par wave parallèle

```
1. Pour chaque tâche code dans wave :
   - Skill superpowers:using-git-worktrees → setup .worktrees/<task-id>
2. Subagent travaille dans son worktree
3. Verify KPIs dans worktree
4. Si KPIs OK :
   - Merge changes vers branche principale (ou cherry-pick commits)
   - Cleanup : git worktree remove .worktrees/<task-id>
5. Si KPIs KO :
   - Worktree préservé pour inspection user
   - Cleanup manuel après résolution
```

### `.gitignore` automatique

Ajout auto de `.worktrees/` si pas déjà présent (via skill `using-git-worktrees` Step 1b).

---

## Workflow type complet

```
1. /orchestrate                      # vue état (visualize par défaut)
2. [user lit, paramètre KPIs custom si besoin]
3. /orchestrate organize             # raffine si user a édité
4. /orchestrate execute --confirm-wave    # OU
   /orchestrate goal --bound=30turns      # set /goal pour auto-loop
5. [Claude orchestre + boucle jusqu'à fin OU goal condition met]
6. /update-state                     # final sync
```

---

## Cohérence "1 framework par session"

Si `route` détecte 2+ frameworks différents :

```
⚠ CONFLIT DÉTECTÉ
  Tâches #2, #5 → GSD
  Tâches #1, #3 → Superpowers
  Tâche #4 → BMAD

Options :
  (A) --framework=Superpowers : tâches GSD/BMAD downgradées vers Superpowers (TDD partout)
  (B) --framework=GSD : tâches Superpowers downgradées vers GSD (skip TDD obligatoire — risqué)
  (C) Split session : exécuter cette session avec framework X, créer task list pour session future framework Y
  (D) Édite tâches : reformule pour résoudre conflit

Choix ?
```

Bloquant — pas de fallback silencieux.

---

## Synergie session 021 (sources canoniques utilisées)

| Composant Orni | Comment task-orchestrator l'utilise |
|----|----|
| CLAUDE.md DENSE v2.0 | Lookup framework table + tooling table |
| `docs/GUIDE-UTILISATION.md` §4.5 | Match besoin → outil |
| `skills/gsd/SKILL.md` §1 | Décisionnaire framework détaillé |
| `project-state.xml` + Archon MCP | Inventory sources |
| `superpowers:dispatching-parallel-agents` | Backend wave parallèle |
| `superpowers:using-git-worktrees` | Backend isolation worktree |
| `superpowers:executing-plans` | Backend wave séquentielle |
| `/update-state` + `/update-prd` | Hooks post-wave |
| Exemple de référence (brownfield review section-par-section) | Pattern de référence |

Zéro duplication.

---

## Quick Reference

| Action | Commande |
|--------|----------|
| Vue état | `/orchestrate` |
| Inventaire seul | `/orchestrate inventory` |
| Vue waves | `/orchestrate organize` |
| Routing per tâche | `/orchestrate route` |
| Lancer avec confirm | `/orchestrate execute --confirm-wave` |
| Lancer autonome | `/orchestrate execute --auto` |
| Goal autonome | `/orchestrate goal --bound=20turns` |
| Force framework | `/orchestrate route --framework=Superpowers` |
| Dry-run | `/orchestrate execute --dry-run` |

---

## Common mistakes

### Oublier les KPIs

❌ Lancer execute sans définir KPIs typés → impossible de valider qu'une tâche est "done"
✅ Toujours définir au minimum 1 KPI validation par tâche

### Forcer parallèle malgré conflit fichier

❌ 2 tâches modifient `state.xml` en parallèle → corruption
✅ Skill détecte conflits + bascule sequential auto

### Goal condition trop large

❌ "Finir toutes les tâches du projet" → évaluateur ne peut pas vérifier
✅ "10 bugs identifiés review fixés (status=done dans Archon), tests pass, branch ready merge"

### Skip worktrees pour code parallèle

❌ 3 subagents touchent même repo en parallèle sans worktree → corrupted state
✅ 1 worktree par tâche code dans wave parallèle (auto par skill)

### Mélanger frameworks dans même session

❌ /orchestrate execute avec tâches GSD + Superpowers dans même session
✅ Warning bloquant + `--framework=X` ou split sessions

---

## Red Flags

**Never:**
- Lancer execute sans visualize préalable (user n'a pas validé)
- Set `/goal` avec >4000 chars condition
- Ignorer conflit "1 framework par session"
- Forcer parallèle avec file conflict détecté
- Skip worktree pour code parallèle multi-fichiers

**Always:**
- Inventory + organize + route avant execute
- Définir KPIs typés par tâche (au minimum validation)
- Auto-confirm seulement avec `--auto` explicite
- Cleanup worktrees post-wave
- Sync state.xml + Archon post-wave

---

## Versioning

- **1.0.0** (2026-05-23, session 022) : impl initiale Phase 1+2 complète. 6 sous-modes. Worktrees + parallel agents + KPIs typés (validation/valeur/custom) + Goal composer <4k chars. Synergie session 021.
