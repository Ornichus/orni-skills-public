# Council Scenarios - Configurations pre-definies

Scenarios pre-configures pour le BMAD Council. Chaque scenario definit une composition optimale pour un cas d'usage courant.

Usage: `/ateam-council --scenario <nom> [sujet/fichier]`

---

## prd-review

**Description:** Revue complete d'un PRD (Product Requirements Document)
**Mode:** review
**Rounds:** 2
**Agents:** pm, analyst, ux-designer, architect

**Justification:**
- `pm` (John) - Verifie la coherence produit, les user stories, le scope
- `analyst` (Mary) - Valide les requirements, l'analyse marche, les metriques
- `ux-designer` (Sally) - Evalue l'experience utilisateur, les parcours, l'accessibilite
- `architect` (Winston) - Verifie la faisabilite technique, les contraintes, l'integration

**Usage typique:**
```
/ateam-council --scenario prd-review _bmad-output/prd.md
```

---

## arch-decision

**Description:** Decision d'architecture technique (choix de stack, patterns, infra)
**Mode:** debate
**Rounds:** 3
**Agents:** architect, dev, tea, qa

**Justification:**
- `architect` (Winston) - Vision systeme, scalabilite, patterns
- `dev` (Amelia) - Faisabilite implementation, DX, productivite
- `tea` (Murat) - Testabilite, qualite, risques techniques
- `qa` (Quinn) - Couverture tests, regression, CI/CD impact

**Usage typique:**
```
/ateam-council --scenario arch-decision "monolith vs microservices pour notre API"
```

---

## sprint-planning

**Description:** Planification de sprint - priorisation et decoupage des stories
**Mode:** round-table
**Rounds:** 2
**Agents:** sm, dev, pm, qa

**Justification:**
- `sm` (Bob) - Facilitation agile, estimation, velocity
- `dev` (Amelia) - Estimation technique, complexite, dependencies
- `pm` (John) - Priorisation business, valeur utilisateur
- `qa` (Quinn) - Effort de test, criteres d'acceptance, risques

**Usage typique:**
```
/ateam-council --scenario sprint-planning "Sprint 4 - feature auth + dashboard"
```

---

## brainstorm

**Description:** Session de brainstorming creatif - generation d'idees et innovation
**Mode:** round-table
**Rounds:** 3
**Agents:** brainstorming-coach, creative-problem-solver, innovation-strategist

**Justification:**
- `brainstorming-coach` (Carson) - Facilitation creative, techniques de divergence
- `creative-problem-solver` (Dr. Quinn) - Resolution systematique, TRIZ, pensee laterale
- `innovation-strategist` (Victor) - Vision strategique, disruption, business models

**Usage typique:**
```
/ateam-council --scenario brainstorm "nouvelle feature de gamification pour l'onboarding"
```

---

## doc-review

**Description:** Revue de documentation technique (README, guides, specs API)
**Mode:** review
**Rounds:** 2
**Agents:** tech-writer, architect, pm

**Justification:**
- `tech-writer` (Paige) - Clarte, structure, standards documentation
- `architect` (Winston) - Exactitude technique, coherence avec l'architecture
- `pm` (John) - Pertinence produit, audience cible, completude

**Usage typique:**
```
/ateam-council --scenario doc-review docs/API-REFERENCE.md
```

---

## course-correction

**Description:** Correction de trajectoire - le projet derive, il faut recadrer
**Mode:** advisory
**Rounds:** 2
**Agents:** pm, architect, sm, dev

**Justification:**
- `pm` (John) - Realignement avec la vision produit et les objectifs
- `architect` (Winston) - Evaluation de la dette technique et des risques
- `sm` (Bob) - Process agile, velocity, blockers
- `dev` (Amelia) - Realite terrain, faisabilite des ajustements

**Usage typique:**
```
/ateam-council --scenario course-correction "on a 2 sprints de retard, que faire?"
```

---

## ux-review

**Description:** Revue UX/UI - evaluation de maquettes, parcours utilisateur, design
**Mode:** review
**Rounds:** 2
**Agents:** ux-designer, pm, analyst

**Justification:**
- `ux-designer` (Sally) - Evaluation UX, accessibilite, patterns d'interaction
- `pm` (John) - Alignement avec les besoins produit et les personas
- `analyst` (Mary) - Donnees utilisateur, metriques d'engagement, benchmarks

**Usage typique:**
```
/ateam-council --scenario ux-review _bmad-output/ux-spec.md
```

---

## test-strategy

**Description:** Definition de la strategie de test pour un projet ou une feature
**Mode:** advisory
**Rounds:** 2
**Agents:** tea, qa, architect, dev

**Justification:**
- `tea` (Murat) - Architecture de test, pyramide, risk-based testing
- `qa` (Quinn) - Coverage, automatisation, pragmatisme
- `architect` (Winston) - Testabilite de l'architecture, points d'integration
- `dev` (Amelia) - Unit tests, TDD, faisabilite des tests

**Usage typique:**
```
/ateam-council --scenario test-strategy "strategie de test pour le module de paiement"
```

---

## research-council

**Description:** Recherche approfondie puis debat BMAD Council sur les resultats
**Mode:** debate
**Rounds:** 2
**Agents:** auto-selection selon le sujet (matrice Section 7 de COUNCIL.md)
**Research agents:** 1-3 selon --links

**Quand l'utiliser:**
- Explorer un sujet complexe avec plusieurs sources web/docs
- Obtenir des recommandations argumentees par des experts BMAD
- Traiter des points bloquants identifies par la recherche
- Combiner exploration et deliberation en un seul workflow

**Usage typique:**
```
/ateam go research-council "optimiser la strategie de caching" --links https://doc1.com https://doc2.com
/ateam go research-council "choisir un framework frontend" --council-mode advisory
/ateam go research-council "ameliorer le comparateur" --council-agents architect,pm,analyst
```

**Pipeline:**
1. Research agents explorent les liens/sujet (WebSearch, WebFetch, codebase)
2. Lead compile un Research Brief structure
3. Shutdown research agents
4. Spawn BMAD Council avec le Research Brief en contexte
5. 2 tours de deliberation (debate par defaut)
6. Rapport final consolide (recherche + recommandations council)

---

## Reference rapide

| Scenario | Agents | Mode | Rounds | Cas d'usage |
|----------|--------|------|--------|-------------|
| `prd-review` | pm, analyst, ux-designer, architect | review | 2 | Revue de PRD |
| `arch-decision` | architect, dev, tea, qa | debate | 3 | Decision architecture |
| `sprint-planning` | sm, dev, pm, qa | round-table | 2 | Planification sprint |
| `brainstorm` | brainstorming-coach, creative-problem-solver, innovation-strategist | round-table | 3 | Brainstorming creatif |
| `doc-review` | tech-writer, architect, pm | review | 2 | Revue documentation |
| `course-correction` | pm, architect, sm, dev | advisory | 2 | Correction trajectoire |
| `ux-review` | ux-designer, pm, analyst | review | 2 | Revue UX/UI |
| `test-strategy` | tea, qa, architect, dev | advisory | 2 | Strategie de test |
| `research-council` | auto-selection | debate | 2 | Recherche + debat BMAD |
