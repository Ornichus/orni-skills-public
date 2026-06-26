# GSD (Get Shit Done) - Skill partagé

> **Version**: 1.0.0 | Wrapper Orni-skills pour GSD framework par TÂCHES (62k★ MIT)

Wrapper de sélection et bootstrap pour le framework **GSD** (`get-shit-done-cc` npm) intégré dans l'écosystème Orni-Skills. Ce skill ne réimplémente PAS GSD — il documente le décisionnaire (GSD vs BMAD vs Superpowers) et formalise l'install per-projet.

**Upstream :** https://github.com/gsd-build/get-shit-done (MIT)
**Package npm :** `get-shit-done-cc`
**Référence vidéos analyse :**
- AI LABS — *GSD Is the Missing Piece For Claude Code* (sélection critères)
- Eric Tech — *Superpowers vs. GSD: The Results Shocked Me* (benchmark brownfield E2E test)

---

## 1. Quand utiliser GSD vs BMAD vs Superpowers

L'écosystème Orni-Skills supporte **3 frameworks spec-driven** complémentaires. Ils ne se remplacent pas — chacun a son use case.

### Décisionnaire

| Type de projet | Framework recommandé |
|----------------|----------------------|
| **MVP expérimental, vision floue, requirements peuvent shift** | **GSD** |
| **CRM / SaaS / community classique, specs connues à l'avance** | **BMAD** |
| **Système critique, edge cases coûteux, actions irréversibles, agentic** | **Superpowers** |
| **Hybride** : MVP rapide puis refactor critique | **GSD core → Superpowers parties critiques** |

### Caractéristiques

| Critère | GSD | BMAD | Superpowers |
|---------|-----|------|-------------|
| **Planning** | Phase-par-phase incrémental | Exhaustif pré-code, sharded tasks | Feature-by-feature TDD-first |
| **Tests** | Playwright en fin de phase | Post-spec, sharded tâches | TDD tests-first systématique |
| **Adversarial planning** | Oui (verifier agent) | Spec interlins | Code review post-impl |
| **Subagents** | Oui (fresh 200k chacun) | Oui | Oui (dispatching-parallel) |
| **Robuste si requirements shift** | Oui | Casse | OK feature-by-feature |
| **Token consumption** | Baseline | n/a | 5-7× plus efficient |
| **Code quality gates** | Excellent (security audit + UAT + learnings) | Specs interlins | Bons (verification-before-completion) |
| **Maintainability git** | Plus de commits noise (16 vs 8) | n/a | Plus propre |

### Benchmark Eric Tech (brownfield E2E testing, 2026-04-15)

Sur le même brownfield (food ordering app) avec spec identique :

| Métrique | Superpowers | GSD |
|----------|-------------|-----|
| Test accuracy | **9/10** | 8/10 |
| Token efficiency | **5-7× mieux** | baseline |
| Code quality gates | OK | **Meilleur** |
| Maintainability | **Meilleur** | OK |
| Bugs trouvés | 10 | 4 |
| Test coverage | 46% | **53%** |
| Verdict global | **Vainqueur sur ce cas** | 2ème |

**Lecture critique** : benchmark = 1 projet brownfield E2E test. Pour MVP greenfield exploratoire, GSD reste plus adapté (sa niche).

---

## 2. Architecture GSD

### Loop core (6 commandes)

```
/gsd-new-project        # Questions → research → requirements → roadmap
   ↓
/gsd-discuss-phase [N]  # Capture décisions implémentation avant planning
   ↓
/gsd-plan-phase [N]     # Research + plan + verify en boucle adversariale
   ↓
/gsd-execute-phase <N>  # Plans exécutés en waves parallèles (subagents)
   ↓
/gsd-verify-work [N]    # UAT manuel + fix plans auto
   ↓
/gsd-ship [N]           # PR depuis phase verified
   ↓
/gsd-complete-milestone # Archive + tag release
   ↓
/gsd-new-milestone      # Start version suivante
```

### Artifacts persistants

Tout dans `.planning/` à la racine du projet :

| Fichier | Rôle |
|---------|------|
| `PROJECT.md` | Vision globale, scope, contraintes, décisions-clés |
| `REQUIREMENTS.md` | Scope MVP, features essentielles V1 |
| `ROADMAP.md` | Phases du projet, ordre, dépendances |
| `STATE.md` | Position courante, décisions live |
| `CONTEXT.md` (par phase) | Décisions implémentation phase courante |
| `phases/<N>/` | Plans, research.md, FALLOW.json, REVIEW.md, etc. |
| `config.json` | Réglages workflow (mode interactive/yolo, model profiles, quality gates) |

### Subagents (66 skills disponibles avec --profile=full)

GSD ne pollue PAS le main context. Tout le heavy lifting se passe dans des subagents :

- **Researchers** (`gsd-advisor-researcher`, `gsd-ai-researcher`) : exploration parallèle
- **Planners** (`gsd-plan-phase`, `gsd-mvp-phase`, `gsd-ai-integration-phase`, `gsd-ui-phase`) : plans phases
- **Executors** : implémentent les plans en waves parallèles
- **Reviewers** (`gsd-code-reviewer`, `gsd-code-fixer`, `gsd-debugger`) : audit + fix
- **Verifiers** (`gsd-verify-work`, `gsd-audit-uat`, `gsd-secure-phase`) : UAT + sécurité
- **Meta** (`gsd-extract-learnings`, `gsd-forensics`, `gsd-stats`) : capitalisation

---

## 3. Configuration

### Install global (déjà fait)

```bash
npx get-shit-done-cc@latest --claude --global --profile=full
```

Footprint global :
- `~/.claude/skills/gsd-*` : 67 skills
- `~/.claude/agents/gsd-*` : 14+ agents
- `~/.claude/get-shit-done/` : workflows, contexts, templates, bin
- `gsd-sdk` CLI dans `%APPDATA%/npm/`
- 9 hooks GSD configurés dans `~/.claude/settings.json` (update check, context monitor, prompt injection guard, etc.)

### Vérifier l'install

```bash
gsd-sdk --version 2>&1
ls ~/.claude/skills/ | grep -c '^gsd-'   # doit retourner ~67
```

### Mise à jour

```bash
/gsd-update
# ou
npx get-shit-done-cc@latest --claude --global
```

### Profile runtime (sans réinstall)

```bash
/gsd-surface --profile=core      # 7 skills boucle uniquement
/gsd-surface --profile=standard  # 13 skills core + phase mgmt
/gsd-surface --profile=full      # 66 skills
```

Permet de réduire bruit `/help` selon contexte projet sans réinstaller.

### Config par projet

`.planning/config.json` configuré pendant `/gsd-new-project` ou via `/gsd-config` :

| Setting | Valeur |
|---------|--------|
| `mode` | `interactive` (confirm chaque step) ou `yolo` (auto-approve) |
| `model_profile` | `quality` / `balanced` / `budget` |
| `workflow.research` | bool (active gsd-advisor-researcher) |
| `workflow.plan_check` | bool (adversarial planning) |
| `workflow.verifier` | bool (UAT post-execute) |
| `parallelization.enabled` | bool (waves parallèles) |
| `code_quality.fallow.enabled` | bool (structural review opt-in) |

---

## 4. Bootstrap projet

### Option A — Greenfield (nouveau projet)

```bash
cd <project-root>
claude --dangerously-skip-permissions
> /gsd-new-project
# → Questions audience, scope, contraintes
# → Research parallèle multi-agents
# → Synthesis + REQUIREMENTS.md + ROADMAP.md
# → Approval → .planning/ initialisé
```

### Option B — Brownfield (codebase existant)

```bash
cd <project-root>
claude --dangerously-skip-permissions
> /gsd-map-codebase     # Analyse stack + archi + conventions existantes
> /gsd-new-project      # Pose questions adaptées au codebase mapped
```

### Option C — Migration depuis BMAD ou Superpowers

```bash
> /gsd-ingest-docs   # Lit ADRs, PRDs, SPECs existants → fusion .planning/
```

Pas de conflit fichiers — `.planning/` ne touche pas `_bmad/` ni les artifacts Superpowers.

---

## 5. Cohabitation avec BMAD + Superpowers

Aucun conflit namespace :

| Framework | Commandes | Skills | Artifacts |
|-----------|-----------|--------|-----------|
| **GSD** | `/gsd-*` (60+) | `gsd-*` (67) | `.planning/` |
| **BMAD** | `/bmad-*` | `bmad-*` | `_bmad/` + `_bmad-output/` |
| **Superpowers** | (skills only) | `superpowers:*` | git worktrees, plans/ |
| **Orni** | `/orni-*` `/update*` `/followup*` `/mail-*` | divers | `project-state.xml`, `_backup/`, mailbox |

### Règle pratique

**1 framework par session** pour pas saturer command space et éviter la confusion. Mélanger dans la même session = LLM picks wrong skill.

**Mix possible sur projet long** :
- Phase MVP exploration → GSD
- Phase refactor critique paiement → switch session, Superpowers TDD
- Phase setup module conventional auth → switch session, BMAD

### Hooks superposés

GSD ajoute 9 hooks dans `~/.claude/settings.json`. Coexistent avec :
- Hooks Orni (say-project, daily-log-writer, precompact-handler)
- Hooks Superpowers (workflow guards)
- Hook Caveman

À surveiller si tu vois ralentissements PreToolUse — possible saturation hooks.

---

## 6. Workflow type pour un nouveau projet GSD

```bash
# 1. Setup projet
cd new-project
git init
claude --dangerously-skip-permissions

# 2. Init GSD
> /gsd-new-project
# → Réponds aux questions
# → Approuve ROADMAP

# 3. Pour chaque phase :
> /gsd-discuss-phase 1     # Capture tes décisions UI/API/data
> /gsd-plan-phase 1        # Recherche + plan + verify (parallèle)
> /gsd-execute-phase 1     # Waves parallèles, atomic commits
> /gsd-verify-work 1       # UAT manuel, fix plans auto
> /gsd-ship 1              # PR ready

# 4. Quand toutes phases done :
> /gsd-complete-milestone  # Archive + tag
> /gsd-new-milestone       # V2 fresh
```

### Mode autonome (yolo)

```bash
> /gsd-autonomous
# → Tourne discuss → plan → execute pour toutes phases sans intervention
# → Tu reviens, c'est buildé. Verify manuellement à la fin.
```

À utiliser quand tu fais confiance au planning initial et que tu veux walk-away.

---

## 7. Hooks GSD installés globalement

Tous opt-in via `~/.claude/settings.json` après install :

| Hook | Rôle |
|------|------|
| **update check** | Notifie quand nouvelle version GSD dispo |
| **context window monitor** | Alerte si context approche 80% |
| **prompt injection guard** | Détecte injections dans contenus lus |
| **read-before-edit guard** | Force `Read` avant `Edit` (safety) |
| **read injection scanner** | Scan contenu lu pour patterns suspects |
| **workflow guard** (opt-in) | Empêche skip étapes loop core |
| **commit validation** (opt-in) | Vérifie commit messages convention |
| **session state orientation** (opt-in) | Affiche état GSD au start session |
| **phase boundary detection** (opt-in) | Trigger actions auto à fin phase |

---

## 8. Glossaire spécifique GSD

| Terme | Sens |
|-------|------|
| **Phase** | Unité de travail dans `ROADMAP.md`, contient discuss/plan/execute/verify/ship |
| **Wave** | Groupe de plans qu'on peut exécuter en parallèle dans une phase |
| **Milestone** | Ensemble de phases qui livrent une version. `complete-milestone` = release |
| **Plan** | `.planning/phases/<N>/plans/<plan-id>.md` — unité d'exécution atomique |
| **Verifier agent** | Agent dédié qui critique le plan d'un autre agent (adversarial) |
| **YOLO mode** | Auto-approve tout. Combiné à `claude --dangerously-skip-permissions` = full automation |
| **Context rot** | Dégradation qualité agent quand son context grossit. GSD lutte via subagents fresh |

---

## 9. Que NE PAS faire

- **Ne pas mixer 2 frameworks dans même session** — saturation command space, confusion LLM.
- **Ne pas commit `.planning/` aveuglément si secrets dedans** — possible que `REQUIREMENTS.md` contienne décisions privées. Vérifier avant push public.
- **Ne pas skip `/gsd-discuss-phase`** sauf si tu sais exactement ce que tu veux — sinon plan généré sera générique.
- **Ne pas désactiver les hooks read-before-edit / injection guard** — safety nets utiles, surtout en YOLO mode.
- **Ne pas utiliser GSD pour projets où specs sont 100% connues** — overkill, prends BMAD.
- **Ne pas utiliser GSD si TDD non-négociable** — pas son design, prends Superpowers.

---

## 10. Pointeurs

- Repo : https://github.com/gsd-build/get-shit-done
- Doc complète : `~/.claude/get-shit-done/` (workflows, contexts, references, templates)
- Discord : https://discord.gg/mYgfVNfA2r
- Vidéo AI LABS sélection : https://www.youtube.com/watch?v=uEit1oOJK0w
- Vidéo Eric Tech benchmark : https://www.youtube.com/watch?v=GJmlik1C4Tg
- ADR profile model : `~/.claude/get-shit-done/docs/adr/0011-skill-surface-budget-module.md`

**Pour démarrer un projet GSD :** voir commande `/orni-init-gsd` (wrapper Orni qui setup le projet + ajoute le décisionnaire framework dans CLAUDE.md).
