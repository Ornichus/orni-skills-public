# Architecture v2 — Documentation Intelligente

> **Version**: 2.0.0 | **Date**: 2026-03-29

Analyse le projet courant, génère et maintient une documentation d'architecture vivante : carte technique, spécification produit et PRD. Quatre modes couvrent le cycle complet — de la cartographie initiale à la correction assistée.

**Principe fondamental :** Documentation ONLY. Ce skill ne modifie JAMAIS les fichiers source du projet. Il crée et met à jour uniquement des fichiers de documentation dans `docs/`.

---

## Vue d'ensemble

Le skill analyse le projet, génère et maintient 3 documents (`architecture.md`, `product-specification.md`, `prd.md`) via 4 modes complémentaires. Chaque mode a un périmètre précis et des livrables définis. L'ensemble forme un système documentaire cohérent où l'architecture technique, la vision produit et le contrat d'implémentation restent synchronisés.

---

## Modes

| Commande | Mode | Description | Livrable principal |
|----------|------|-------------|--------------------|
| `/architecture` | **Carte technique** | Scan du projet, génération de `docs/architecture.md` enrichi (composants, relations, ADRs, stack, data flow) | `docs/architecture.md` |
| `/architecture audit` | **Audit documentaire** | Scan profond de toute la base documentaire existante, rapport de gaps et incohérences entre les 3 documents | Rapport d'audit (gaps, sections manquantes, désynchronisations) |
| `/architecture sync` | **Synchronisation rapide** | Mise à jour du PS et PRD depuis les changements récents du code et de l'architecture | `docs/product-specification.md` et `docs/prd.md` mis à jour |
| `/architecture fix` | **Correction agentique** | Agents spécialisés corrigent les gaps détectés par l'audit, l'utilisateur valide chaque correction | Documents corrigés après validation utilisateur |

---

## Documents produits

| Fichier | Rôle | Contenu clé |
|---------|------|-------------|
| `docs/architecture.md` | Carte technique | Composants classifiés, relations, ADRs (Architecture Decision Records), stack technique, data flow, schéma DB |
| `docs/product-specification.md` | Bible du projet | Vision, personas, JTBD (Jobs To Be Done), features détaillées, roadmap, contraintes business |
| `docs/prd.md` | Contrat d'implémentation | FRs (Functional Requirements), NFRs (Non-Functional Requirements), success criteria, user journeys, dérivé du PS |

---

## PS et PRD — Coexistence

Les deux documents coexistent avec des rôles distincts et complémentaires :

| Aspect | Product Specification (PS) | PRD |
|--------|---------------------------|-----|
| **Rôle** | Bible exhaustive du projet | Vue focalisée pour l'implémentation |
| **Audience** | Tout le monde (stakeholders, design, dev, agents) | Dev + agents IA |
| **Taille typique** | ~500–1700 lignes (~25K tokens) | ~200–500 lignes (~5K tokens) |
| **Contenu** | Vision, personas, JTBD, features, roadmap, contraintes | FRs, NFRs, success criteria, user journeys |
| **Stabilité** | Évolue avec la vision produit | Dérivé et resynchronisé depuis le PS |

**Flux de dérivation :**

```
PS (bible) → PRD (extraction focalisée) → Epics → Stories
```

Quand le PS est mis à jour, le skill propose automatiquement de resynchroniser le PRD pour maintenir la cohérence. Le PRD ne contient jamais d'information qui contredit le PS — en cas de conflit, le PS fait autorité.

---

## Classification des composants

Chaque composant du projet est classé dans un des 5 niveaux :

| Niveau | Tag | Description | Exemple |
|--------|-----|-------------|---------|
| **Core** | `[CORE]` | Fondations du projet, tout en dépend | Auth, Database, Config, API Client |
| **Feature** | `[FEAT]` | Fonctionnalité principale visible utilisateur | Dashboard, Paiements, Notifications |
| **Sub** | `[SUB]` | Sous-fonctionnalité d'une feature | Filtres, Export CSV, Recherche |
| **Hook** | `[HOOK]` | Logique événementielle, réactive | onAuthChange, onPaymentSuccess |
| **Utility** | `[UTIL]` | Helpers partagés, sans logique métier | Formatters, Validators, Logger |

---

## Types de relations

4 types de connexions explicites entre composants :

| Relation | Symbole | Signification | Exemple |
|----------|---------|---------------|---------|
| `utilise` | `-->` | Appel direct / import | Dashboard `utilise` API Client |
| `déclenche` | `==>` | Trigger un événement / action | Auth `déclenche` Dashboard refresh |
| `dépend_de` | `<--` | Nécessite pour fonctionner | Dashboard `dépend_de` Auth |
| `persiste_dans` | `==>DB` | Stocke/lit des données | Notes `persiste_dans` Supabase |

---

## Sources

Le skill collecte les informations depuis plusieurs sources, activées selon le mode de scan.

### Scan léger (défaut)

Utilisé par `/architecture` en mode standard. Sources analysées :

| Source | Ce qu'on en tire |
|--------|-----------------|
| **Code source** | Composants, imports, dépendances directes, structure |
| **Structure des dossiers** | Organisation du projet, conventions de nommage |
| **Fichiers de configuration** | Stack technique, dépendances, scripts (package.json, tsconfig, docker-compose, etc.) |
| **`docs/`** | Documentation existante, architecture précédente |
| **`CLAUDE.md`** | Instructions projet, conventions, contexte agent |
| **`_bmad-output/`** | Artefacts BMAD existants (PRD, stories, epics) |

### Scan profond (`--deep` ou mode audit)

Activé par `/architecture audit` ou flag `--deep`. Ajoute aux sources légères :

| Source | Ce qu'on en tire |
|--------|-----------------|
| **Git history (2 passes)** | Passe 1 : commits récents (évolutions rapides). Passe 2 : commits fondateurs (décisions structurantes) |
| **claude-mem MCP** | Mémoire persistante cross-session (décisions passées, contexte historique) |
| **`project-state.xml`** | État courant du projet (epics, stories, blockers) |
| **Mailbox inter-projets** | Communications avec d'autres projets (dépendances externes, contrats d'API) |

> **Si claude-mem MCP est déconnecté / la recherche sémantique tombe** (fréquent sur Windows x64 — Chroma ne démarre pas) : voir la fiche de dépannage `docs/CLAUDE-MEM-CHROMA-WINDOWS-FIX.md` du repo Orni-Skills (correctif + ré-indexation).

### Auto-détection

Chaque source est auto-détectée : si elle est présente, elle est scannée. Si elle est absente, elle est ignorée silencieusement — pas d'erreur, pas d'avertissement. Le skill s'adapte au projet tel qu'il est.

---

## Changelog

- 2.0.0 (2026-03-29) : Réécriture complète — 4 modes, 3 documents, sources multiples
- 1.0.0 (2026-03-19) : Version initiale (cartographie simple)

---

## Templates de documents

### Template : `docs/architecture.md`

#### Frontmatter

```yaml
---
date: YYYY-MM-DD
project: "{nom du projet}"
version: "{version}"
bmad_detected: true|false
generated_by: architecture-skill-v2
audience: "Développeurs et agents IA"
source_hash: "{hash}"
coherence_with:
  - docs/product-specification.md: synced|stale|absent
  - docs/prd.md: synced|stale|absent
inputDocuments: []  # si BMAD
---
```

#### Structure du document

1. **`# Architecture — {Projet}`**
2. **`## Executive Summary`** — 2-3 phrases positionnant le projet et ses choix structurants.
3. **`## Architecture Decisions`** — ADRs (Architecture Decision Records). Chaque décision contient :
   - **Choix** — la décision prise
   - **Raison** — pourquoi ce choix
   - **Alternatives écartées** — ce qui a été considéré et rejeté
   - **Source** — d'où vient cette information (code, config, git history, CLAUDE.md, etc.)
4. **`## Technical Stack`** — Table avec colonnes : Couche | Technologie | Rôle
5. **`## Component Map`** — Arbre indenté utilisant la classification à 5 niveaux :
   ```
   [CORE] Auth
     [SUB] session-manager
     [HOOK] onAuthChange
   [FEAT] Dashboard
     [SUB] Filters
     [UTIL] formatters
   ```
6. **`## Relations`** — Table avec colonnes : Source | Relation | Destination | Détail
7. **`## Data Flow`** — Pipeline textuel décrivant les flux de données principaux :
   ```
   Requête → API Gateway → Auth middleware → Controller → Service → DB
   DB → Service → Transformer → Response
   ```
8. **`## Constraints (NFRs)`** — Performance, Sécurité, Scalabilité, Disponibilité, etc.
9. **`## FR Coverage Map`** — *(BMAD Niveau 3 uniquement)* Table avec colonnes : Composant | FRs | Stories

> **Note :** Régénération complète du Component Map à chaque run (pas incrémental). Le skill compare le document entier avec l'existant et ne propose la mise à jour que si un diff significatif est détecté.

---

### Template : `docs/product-specification.md`

#### Frontmatter

```yaml
---
date: YYYY-MM-DD
project: "{nom du projet}"
version: "{version}"
generated_by: architecture-skill-v2
audience: "Fondateur, développeurs, agents IA"
spec_level: full|strategic|minimal
last_audit: YYYY-MM-DD
source_hash: "{hash}"
coherence_with:
  - docs/architecture.md: synced|stale|absent
  - docs/prd.md: synced|stale|absent
changelog:
  - "{version} ({date}): {description}"
---
```

#### Sections fixes (toujours présentes)

1. **Vision et problème** — Quel problème est résolu, pour qui, pourquoi maintenant
2. **Persona / Utilisateurs** — Profils types avec besoins et frustrations
3. **Jobs-to-be-Done** — Ce que l'utilisateur cherche à accomplir (pas les features)
4. **Architecture de la solution** — Vue haut niveau de la structure technique
5. **NOT-WHAT (exclusions explicites)** — Ce que le projet ne fait PAS et pourquoi
6. **Critères de succès** — Métriques mesurables de réussite
7. **Roadmap** — Phases et jalons
8. **Risques et blockers** — Obstacles identifiés avec mitigation
9. **Différenciateurs** — Ce qui distingue ce projet des alternatives
10. **Références** — Sources externes, inspirations, documentation liée

#### Sections dynamiques (générées si détectées dans le projet)

| Section | Condition de génération |
|---------|------------------------|
| Sections par domaine fonctionnel | Autant que nécessaire selon les features détectées |
| Schéma de base de données | Si DB détectée (Prisma, migrations SQL, schema.prisma, etc.) |
| API — Inventaire | Si routes détectées (Express, Next.js API, FastAPI, etc.) |
| Frontend — Pages et composants | Si frontend détecté (React, Vue, Svelte, etc.) |
| Pipeline de données | Si flux de données détectés (ETL, workers, queues, etc.) |
| Infrastructure et déploiement | Si Docker, docker-compose, ou config deploy détecté |
| MCP Tools | Si configuration MCP détectée (.mcp.json, mcp-servers, etc.) |
| Modèle de coût | Si infra payante détectée (cloud providers, SaaS, APIs facturées) |
| Système de sources | Si sources externes détectées (APIs tierces, webhooks, scraping) |

#### Géométrie variable

Le niveau de détail du PS s'adapte à la taille du projet :

| Profil projet | Critères | Niveau PS |
|---------------|----------|-----------|
| **Complexe** | >50 fichiers, BMAD, DB, API | PS complet — toutes les sections fixes + dynamiques pertinentes |
| **Moyen** | 10-50 fichiers | PS moyen — sections fixes + sections dynamiques pertinentes uniquement |
| **Léger** | <10 fichiers, script, lib | PS minimal — Vision + Architecture + NOT-WHAT |

#### Sourçage obligatoire

Chaque information factuelle du PS DOIT être sourcée inline :

```markdown
> Source: [package.json — dependencies]
> Source: [CLAUDE.md — section Conventions]
> Source: [git log — commit abc1234]
```

---

### Template : `docs/prd.md`

#### Frontmatter

```yaml
---
date: YYYY-MM-DD
project: "{nom du projet}"
version: "{version}"
derived_from: "product-specification.md v{ps_version}"
generated_by: architecture-skill-v2
audience: "Développeurs et agents implémentant"
source_hash: "{hash}"
coherence_with:
  - docs/product-specification.md: synced|stale
---
```

#### Sections du PRD

Le PRD est extrait automatiquement du PS — il ne contient que l'information nécessaire à l'implémentation :

1. **Executive Summary** — Condensé depuis PS sections Vision (§1) + Architecture (§4)
2. **Success Criteria** — Depuis PS section Critères de succès (§6)
3. **User Journeys** — Depuis PS section Jobs-to-be-Done (§3), reformulés en parcours utilisateur
4. **Functional Requirements (FRs)** — Depuis les sections domaine fonctionnel du PS
5. **Non-Functional Requirements (NFRs)** — Depuis PS section Constraints + Risques

> **Traçabilité :** Chaque information du PRD est traçable à sa section source dans le PS. Le format de référence est `[PS §{numéro} — {nom section}]`.

---

## Workflows

### `/architecture` — Carte technique

Génère (ou régénère) `docs/architecture.md` à partir d'un scan du projet. Régénération complète à chaque run — le skill compare avec l'existant et ne propose la mise à jour que si un diff significatif est détecté.

**Étapes :**

1. **Scan léger** — Analyser le code source, configs, structure des dossiers, `docs/`, `CLAUDE.md`, `_bmad-output/` (si présent).

2. **Détection BMAD** — Vérifier si `_bmad-output/` existe :
   - **OUI → Mode Niveau 3** : traçabilité FR Coverage Map, liens vers Epics/Stories depuis `_bmad-output/planning-artifacts/` (PRD, epics-and-stories) et `implementation-artifacts/` (stories, sprint-status).
   - **NON → Mode Niveau 2** : standalone, ADRs détectées depuis git/code/conversations.

3. **Rapport-proposition** — Afficher au terminal le document proposé (PAS d'écriture). Le format suit le template `architecture.md` défini dans la section Templates.

4. **Validation utilisateur** — L'utilisateur valide, modifie, ou rejette. Ne JAMAIS écrire sans validation.

5. **Écriture** — Si validé : backup de l'existant dans `docs/_backup/architecture/`, puis écriture de `docs/architecture.md`. Mettre à jour le frontmatter (`date`, `version`, `source_hash`, `coherence_with`).

6. **Boucle interactive** — Après l'écriture, afficher le health-check documentaire et proposer la suite logique :
   ```
   Architecture générée. ⚠️ PS absent.
   Étape suivante recommandée : /architecture sync pour créer le PS.
   Lancer ?
   ```

---

### `/architecture audit` — Scan profond

Audit complet de TOUTE la base documentaire : `docs/architecture.md`, `docs/product-specification.md`, `docs/prd.md`, et `_bmad-output/` (épics, stories, sprint-status — si BMAD détecté).

**Étapes :**

1. **Health-check initial** — Lister tous les documents existants et absents :
   ```
   [HEALTH CHECK] État documentaire complet :

     DOCUMENTS ORNI :
     ✅ architecture.md — à jour (2026-03-25)
     ⚠️ product-specification.md — 3 features non documentées
     ⚠️ prd.md — désynchronisé du PS (PS v1.3, PRD basé sur v1.1)

     DOCUMENTS BMAD (si _bmad-output/ détecté) :
     ✅ epics-and-stories.md — 5 épics, 18 stories
     ⚠️ story-2-3-webhook-handler.md — status obsolète
     ⚠️ sprint-status.yaml — story 2-3 marquée "ready-for-dev" au lieu de "done"

     RÉSUMÉ : 2 ✅ à jour, 4 ⚠️ désynchronisés, 0 ❌ absents
   ```

2. **Scan profond des 8 sources** — Avec `--preview` optionnel pour estimer la taille avant de lancer. Approche 2 passes pour sources lourdes (git history, claude-mem) : index léger d'abord, deep dive sélectif ensuite. Budget estimé : ~60-80K tokens.

3. **Comparaison** — Comparer les informations trouvées dans les sources avec TOUS les documents existants.

4. **Classification des gaps** :
   - 🔴 **CRITIQUE** — Composant/décision majeure absente, incohérence bloquante
   - 🟡 **IMPORTANT** — Info partielle, obsolète, ou désynchronisée
   - 🔵 **MINEUR** — Détail manquant, amélioration possible

5. **Rapport synthétique** — Afficher un tableau récapitulatif :
   ```
   # Audit Documentation — {Projet}
   **Date :** YYYY-MM-DD
   **Sources analysées :** N/8 (liste des sources skippées avec raison)

   **Résumé :** X 🔴 critiques, Y 🟡 importants, Z 🔵 mineurs

   | # | Niveau | Document | Section | Gap | Source |
   |---|--------|----------|---------|-----|--------|
   | 1 | 🔴 | architecture.md | Component Map | WebhookHandler absent | code + git a1b2c3 |
   | 2 | 🟡 | prd.md | FRs | 2 FRs manquantes vs PS | PS v1.3 |
   ```

6. **Drill-down** — L'utilisateur peut demander le détail d'un gap spécifique (par numéro), de tous, ou ignorer. Chaque détail inclut : ce qui manque, où l'info a été trouvée (source exacte), suggestion concrète de modification.

7. **Validation et application** — L'utilisateur valide gap par gap (accepter / ignorer / modifier). Application dans le document concerné + backup.

8. **Boucle interactive** — Proposer `/architecture fix` si gaps nombreux, ou les prochaines étapes pertinentes.

---

### `/architecture sync` — Mise à jour rapide

Met à jour le PS et le PRD depuis les changements récents du code et de l'architecture.

**Étapes :**

1. **Lecture des documents actuels** — Lire PS et PRD. Si absents, proposer de les créer (rediriger vers le workflow de génération avec intelligence proactive).

2. **Scan léger des sources récentes** — Depuis `last_updated` du PS :
   - git log (commits depuis la date)
   - claude-mem observations récentes (via MCP si disponible)
   - Changements détectés dans le code (nouveaux fichiers, modifications structurelles)

3. **Détection des deltas** — Identifier : nouvelles features, décisions techniques, changements de scope, nouvelles contraintes, éléments supprimés/dépréciés.

4. **Proposition des modifications** — Afficher un rapport synthétique par section du PS :
   ```
   # Sync PS — {Projet}
   **Dernière mise à jour PS :** YYYY-MM-DD
   **Période analysée :** {last_updated} → {now}

   | # | Section PS | Type | Description | Source |
   |---|-----------|------|-------------|--------|
   | 1 | Architecture | Ajout | Nouveau module Webhooks | git commit a1b2c3 |
   | 2 | NOT-WHAT | Dépréciation | Feature X retirée | conversation claude-mem #4210 |
   ```

5. **Validation utilisateur** — Section par section (accepter / ignorer / modifier).

6. **Application** — Backup + écriture + incrémenter version + mettre à jour changelog.

7. **Resync PRD** — Si le PS a changé :
   ```
   Le PS a été mis à jour (v1.2 → v1.3). Le PRD devrait être resynchronisé.
   Lancer la resync ?
   ```
   Si oui : extraire les sections mises à jour du PS vers le PRD, montrer le diff, valider, appliquer.

8. **Boucle interactive** — Proposer la suite (audit si beaucoup de deltas, ou rien si tout est à jour).

---

### `/architecture fix` — Correction agentique

Agents spécialisés corrigent les gaps détectés par l'audit, avec validation utilisateur à chaque étape.

**Prérequis :** Un rapport d'audit existe (sinon proposer `/architecture audit` d'abord).

**Étapes :**

1. **Charger le rapport d'audit** — Reprendre les gaps identifiés par le dernier audit.

2. **Présenter le plan de correction par phases** :
   ```
   Plan de correction — {N} gaps à traiter :

   Phase 1 : Product Specification — {X} modifications (Agent PM)
   Phase 2 : PRD — resync avec PS (Agent PM)
   Phase 3 : Architecture — {Y} modifications (Agent Architect)
   Phase 4 : Epics & Stories & Sprint — {Z} corrections (Agent SM/Dev)

   Lancer ? (tout / phase par phase / ignorer)
   ```

3. **Choix utilisateur** — tout (séquentiel), phase par phase, une phase spécifique (`--phase N`), ou parallèle (`--parallel`).

4. **Spawner les agents spécialisés** pour les phases choisies :

   | Phase | Agent BMAD | Rôle |
   |-------|-----------|------|
   | 1 — PS | PM (John) | Enrichir sections, ajouter features, corriger infos |
   | 2 — PRD | PM (John) | Resynchroniser avec PS, ajouter FRs/NFRs manquantes |
   | 3 — Architecture | Architect (Winston) | Mettre à jour Component Map, ADRs, Stack, Relations |
   | 4 — Epics/Stories/Sprint | SM (Bob) + Dev (Amelia) | Corrections simples directes + réécriture complexe |

5. **Corrections hybrides dans Phase 4** :
   - Status, dates, frontmatter → correction directe (pas d'agent nécessaire)
   - Contenu existant à réécrire → Agent SM ou Dev
   - Nouveau document à créer (nouvelle épic/story) → Agent SM

6. **Préparation AVANT/APRÈS** — Chaque agent prépare ses modifications SANS écrire :
   ```
   ## Phase {N} : {Document} — {X} modifications proposées

   ### Modification 1/{X} — Section "{nom}"
   **Gap :** {description} ({niveau})

   **AVANT :**
   > {contenu actuel}

   **APRÈS :**
   > {contenu proposé}

   **Source :** {origine de l'information}
   ```

7. **Validation par phase** — L'utilisateur valide chaque phase : accepter / rejeter / modifier. Ne jamais appliquer sans validation explicite.

8. **Application** — Pour chaque phase validée : backup du document → écriture → incrémenter version → mettre à jour changelog → recalculer `source_hash` et `coherence_with`.

9. **Boucle interactive** — Proposer les phases restantes, ou confirmer que tout est à jour :
   ```
   Phase 1 (PS) appliquée. ✅
   Reste : Phase 2 (PRD, 2 FRs), Phase 4 (1 status story)
   On continue avec la Phase 2 ?
   ```

---

## Règles strictes

1. **JAMAIS** modifier de fichier source (`.ts`, `.js`, `.py`, `.css`, etc.)
2. **JAMAIS** inclure de secrets (clés API, tokens, URLs webhook)
3. **JAMAIS** écrire sans validation humaine — toujours rapport d'abord
4. **JAMAIS** inventer d'information — chaque info traçable à une source
5. **JAMAIS** supprimer de contenu — déprécier avec raison dans NOT-WHAT
6. **TOUJOURS** backup avant modification
7. **TOUJOURS** incrémenter version + changelog à chaque modification
8. **Idempotent :** relancer ne réécrit pas si rien n'a changé
9. **TOUJOURS** proposer la suite logique après chaque mode (boucle interactive)

---

## Versioning et archivage

### Structure de backup

```
docs/
├── product-specification.md
├── prd.md
├── architecture.md
└── _backup/
    ├── product-specification/
    │   ├── current/
    │   │   └── ps_latest.md
    │   └── archive/
    │       └── ps_{YYYY-MM-DD}_{HH-MM-SS}.md
    ├── prd/
    │   ├── current/
    │   │   └── prd_latest.md
    │   └── archive/
    │       └── prd_{YYYY-MM-DD}_{HH-MM-SS}.md
    └── architecture/
        ├── current/
        │   └── arch_latest.md
        └── archive/
            └── arch_{YYYY-MM-DD}_{HH-MM-SS}.md
```

### Déclencheurs

- **Avant chaque modification** par le skill — aucune exception
- **Nommage :** `{type}_{YYYY-MM-DD}_{HH-MM-SS}.md`
- `current/` contient toujours la dernière version connue (écrasée à chaque backup)
- `archive/` accumule l'historique complet

---

## Contrôle d'intégrité

Checklist vérifiée à chaque modification de document :

- [ ] Aucune section existante n'a disparu
- [ ] Changelog mis à jour
- [ ] Backup effectué
- [ ] Version incrémentée
- [ ] `source_hash` recalculé
- [ ] `coherence_with` vérifié :
  - [ ] `architecture.md` ↔ PS
  - [ ] PS ↔ PRD
  - [ ] PRD ↔ Epics (si BMAD)

Le skill REFUSE d'écrire si un point de cette checklist n'est pas satisfait. L'utilisateur est informé du point bloquant et de l'action corrective.

---

## Intelligence proactive

### Health-check documentaire

Affiché **au démarrage de chaque mode**, le health-check couvre les documents Orni et BMAD :

```
[HEALTH CHECK] État documentaire complet :

  DOCUMENTS ORNI :
  ✅ architecture.md — à jour (2026-03-25)
  ⚠️ product-specification.md — 3 features non documentées
  ❌ prd.md — absent

  DOCUMENTS BMAD (si _bmad-output/ détecté) :
  ✅ epics-and-stories.md — 5 épics, 18 stories
  ⚠️ story-2-3-webhook-handler.md — status obsolète
  ⚠️ sprint-status.yaml — story 2-3 marquée "ready-for-dev" au lieu de "done"

  RÉSUMÉ : 1 ✅ à jour, 3 ⚠️ désynchronisés, 1 ❌ absent
```

### Proposition de phases si documents manquants

```
Documents manquants détectés. Je propose :

  Phase 1 : Product Specification (bible du projet)
  Phase 2 : PRD (dérivé du PS, contrat d'implémentation)
  Phase 3 : Epics (regroupements fonctionnels)
  Phase 4 : Stories (unités de travail)

  Lancer la Phase 1 ? (oui / tout / ignorer)
```

Chaque phase est **optionnelle et indépendante**. Le skill propose mais ne force jamais un pipeline séquentiel. Les projets sans BMAD sont des citoyens de première classe — les phases 3 et 4 ne sont proposées que si BMAD est détecté.

### Boucle interactive

Après chaque mode, l'agent :

1. **Évalue** ce qui reste à faire
2. **Présente** clairement l'état (nombre de gaps restants, quelles phases, estimation d'effort)
3. **Propose** la prochaine étape logique
4. **L'utilisateur ne doit jamais deviner** quoi faire ensuite — le skill guide

```
Architecture générée. ⚠️ PS absent, PRD absent.
Gaps restants : 2 documents à créer (~20 min estimées).
Étape suivante recommandée : /architecture sync pour créer le PS.
Lancer ?
```

---

## Maintenance automatisée — CLAUDE.md

Le skill injecte la règle suivante dans le `CLAUDE.md` de chaque projet qui l'utilise :

```markdown
## Documentation — Règle de maintenance

Quand une discussion aboutit à une décision sur :
- une nouvelle feature, un changement de feature, ou une suppression
- un choix technique (stack, pattern, outil)
- un changement de scope (NOT-WHAT, roadmap)
- une contrainte (NFR, sécurité, performance)

→ AVANT d'implémenter, proposer :
"Cette décision devrait être ajoutée au PS (docs/product-specification.md).
Section concernée : [section]. Voulez-vous que je mette à jour le PS d'abord ?"

→ Si le PS est modifié, proposer ensuite :
"Le PS a changé. Le PRD (docs/prd.md) devrait être resynchronisé.
Voulez-vous lancer /architecture sync ?"
```

Cette injection est proposée (pas forcée) lors de la première utilisation du skill sur un projet. Si le `CLAUDE.md` contient déjà cette section, le skill ne la modifie pas.

---

## Résumé des mécanismes de maintenance

Trois couches complémentaires assurent que la documentation reste vivante :

```
PASSIF (permanent)
└── CLAUDE.md → l'agent propose la mise à jour PS + PRD à chaque décision

ACTIF (on-demand)
├── /architecture sync  → delta rapide depuis les changements récents
├── /architecture audit → scan profond de toute la base documentaire
└── /architecture fix   → correction agentique avec validation phase par phase

AUTOMATIQUE (garde-fous)
├── Backup avant chaque modification
├── Changelog + versioning dans frontmatter
├── Jamais de suppression, seulement dépréciations
├── Contrôle d'intégrité à chaque écriture (PS ↔ PRD ↔ architecture)
└── Boucle interactive : chaque mode propose la suite
```

---

## Récapitulatif des 4 modes

| Mode | Usage | Fréquence | Coût estimé |
|------|-------|-----------|-------------|
| `/architecture` | Générer/régénérer la carte technique | À chaque changement structurel | Léger (~10K tokens) |
| `/architecture audit` | Scan profond, détecter TOUS les gaps | Occasionnel (hebdo, milestone) | Lourd (~60-80K tokens) |
| `/architecture sync` | Mise à jour rapide PS + PRD | Fréquent (après discussions) | Moyen (~20-30K tokens) |
| `/architecture fix` | Correction agentique par phase | Après un audit | Variable (agents spécialisés) |
