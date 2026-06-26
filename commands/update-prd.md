---
description: 'Audit conversation vs code + propagation docs (PS, PRD, architecture.md)'
---

# /update-prd - Audit et propagation documentaire

Audite la conversation courante, compare avec le code reel, et propage les changements dans les documents architecture (PS, PRD, architecture.md).

## Principe

La conversation est la source d'INTENT (ce qui devait etre fait).
Le code/git est la source de REALITE (ce qui a ete fait).
Le delta = les oublis, a capturer dans les docs.

## Pre-requis contexte

Ce skill est gourmand (~80-150K tokens). Il doit etre lance en debut de session ou avec un contexte frais. Ne PAS le lancer en fin de session — utiliser /update-all qui le differe automatiquement.

## Instructions

### Phase 1 : Orchestrateur — Audit de conversation

1. **Scanner la conversation complete :**
   - Remonter dans tout le transcript de la session courante
   - Identifier chaque item significatif :
     - Fonctionnalites discutees ou demandees
     - Decisions prises (et leur raisonnement)
     - Bugs identifies ou resolus
     - Changements d'architecture ou de stack
     - Contraintes ajoutees ou modifiees
     - Features explicitement retirees ou reportees

2. **Croiser chaque item avec la realite :**
   - Executer `git diff` et `git log` pour les commits de la session
   - Utiliser grep/glob pour verifier l'existence de fichiers/fonctions mentionnes
   - Ne PAS se fier uniquement au git — la conversation prime pour l'intent

3. **Tagger chaque item :**

   | Tag | Signification | Condition |
   |-----|---------------|-----------|
   | `[OK]` | Discute ET implemente | Preuve trouvee dans le code (grep/glob) |
   | `[NON IMPLEMENTE]` | Discute mais absent du code | Mentionne dans la conversation, pas dans le code |
   | `[PARTIEL]` | Partiellement implemente | Code present mais incomplet. En cas de doute, utiliser ce tag |
   | `[DECISION]` | Choix architectural | Pas de code attendu, c'est un choix documente |
   | `[DIFFERE]` | Explicitement reporte | L'utilisateur a dit "plus tard", "pas maintenant", etc. |
   | `[RETIRE]` | Feature supprimee | L'utilisateur a explicitement retire cette feature. Inclure raison + date |

4. **Documenter chaque item avec tracabilite :**

   Format pour chaque item du rapport :
   ```markdown
   ### [TAG] Nom de l'item

   - **Source:** Conversation (message user #N) | Documentation existante (fichier)
   - **Fiabilite:** HAUTE (user direct) | MOYENNE (agent/doc) | BASSE (externe)
   - **Verification:** grep "pattern" → fichier:ligne | Non trouve
   - **Detail:** Description de ce qui a ete discute/decide
   - **Raisonnement:** Pourquoi cette decision (si applicable)
   ```

   **Niveaux de fiabilite :**

   | Source | Fiabilite |
   |--------|-----------|
   | Conversation utilisateur | HAUTE — l'utilisateur fait autorite |
   | Conversation agent | MOYENNE — a verifier contre le code |
   | Documentation existante | MOYENNE — reflet presume fidele, peut etre desync |
   | Documentation externe | BASSE — reference utile, a valider |

5. **Garde-fous anti-hallucination :**
   - Regle 1 : Un item n'existe que s'il est mentionne dans la conversation. Ne pas inferer.
   - Regle 2 : Un item est `[OK]` UNIQUEMENT si preuve trouvee via grep/glob.
   - Regle 3 : En cas de doute → `[PARTIEL]` avec raison du doute.
   - Regle 4 : Chaque item cite sa source (index message dans la conversation).
   - Regle 5 : Ne jamais supprimer un element existant des docs sans decision explicite de l'utilisateur. Marquer `[RETIRE]` avec raison et date.

6. **Produire le rapport d'audit :**
   - Generer un rapport markdown structure
   - Le rapport est utilise en Phase 2 par les sous-agents

7. **Persister le rapport :**
   - Creer `docs/_backup/audit-reports/current/` et `docs/_backup/audit-reports/archive/` si absents
   - Sauvegarder dans `docs/_backup/audit-reports/archive/audit-report_{YYYY-MM-DD}_{HH-MM-SS}.md`
   - Copier dans `docs/_backup/audit-reports/current/audit-report_latest.md` (ecrase)
   - Nettoyage : les rapports de plus de 30 jours dans `archive/` peuvent etre supprimes

8. **Afficher un resume a l'utilisateur :**
   ```
   ## Rapport d'audit — N items extraits

   | Tag | Nombre | Items |
   |-----|--------|-------|
   | [OK] | N | item1, item2 |
   | [NON IMPLEMENTE] | N | item3 |
   | [PARTIEL] | N | item4 |
   | [DECISION] | N | item5 |
   | [DIFFERE] | N | item6 |
   | [RETIRE] | N | item7 |

   Lancer la propagation docs ? (oui/non)
   ```

### Phase 2 : Sous-agents — Propagation documentaire

Si l'utilisateur confirme, lancer les sous-agents pertinents en parallele via l'outil Agent.

**Detection des documents existants :**
AVANT de lancer les sous-agents, verifier quels documents existent :
- `docs/product-specification.md` OU `docs/specs/*.md` → PS Agent
- `docs/prd.md` → PRD Agent
- `docs/architecture.md` → Archi Agent

**Si `docs/prd.md` n'existe PAS :** ne PAS lancer le PRD Agent. Le PS modulaire (si present) fait office de PRD — les items PRD sont integres par le PS Agent.

**Lancer UNIQUEMENT les agents dont le document cible existe.** Informer l'utilisateur des agents skippés et pourquoi.

**Chaque sous-agent recoit :**
- Le rapport d'audit complet (texte integral)
- Son document cible actuel (a lire au lancement)
- Ses regles specifiques (ci-dessous)

**Regles communes aux sous-agents :**
- Lire le document cible en entier AVANT de proposer des modifications
- Backup du document avant toute ecriture (pattern `docs/_backup/`)
- Ne JAMAIS supprimer de contenu existant sans tag `[RETIRE]` dans le rapport
- Preserver les tags `[NON IMPLEMENTE]`, `[PARTIEL]`, `[RETIRE]`, `[DIFFERE]` tels quels dans le document
- Preparer le diff (avant/apres) mais NE PAS ecrire — retourner le diff a l'orchestrateur

#### Sous-agent 1 : PS Agent

**Document cible :** `docs/product-specification.md` + `docs/specs/*.md` (si structure modulaire)

**Regles specifiques :**
- Detecter si PS monolithique ou modulaire (presence de `docs/specs/`)
- Si modulaire : identifier quel(s) module(s) sont affectes par chaque item
- Ajouter les items `[OK]` dans le module concerne (enrichir la spec existante)
- Ajouter les items `[NON IMPLEMENTE]` avec mention explicite : `> **Status : NON IMPLEMENTE** — [description]`
- Ajouter les items `[DECISION]` dans la section appropriee avec le raisonnement
- Ajouter les items `[PARTIEL]` avec mention : `> **Status : PARTIEL** — [ce qui manque]`
- Mettre a jour la date du module dans l'index si modifie
- Les items `[DIFFERE]` vont dans la roadmap avec mention "differe"
- Les items `[RETIRE]` sont marques dans le module avec raison et date

**Prompt pour le sous-agent :**
```
Tu es le PS Agent. Tu recois un rapport d'audit de conversation et tu dois mettre a jour le Product Specification.

RAPPORT D'AUDIT :
{rapport_audit}

REGLES :
1. Lis d'abord le PS complet (index + modules si modulaire)
2. Pour chaque item du rapport, identifie ou il doit aller
3. Enrichis le contenu existant — ne supprime jamais sans [RETIRE]
4. Preserve tous les tags de statut dans le document
5. Backup avant modification
6. Retourne le diff complet (avant/apres) pour chaque fichier modifie
```

#### Sous-agent 2 : PRD Agent

**Document cible :** `docs/prd.md`

**Regles specifiques :**
- Les items `[OK]` enrichissent les FRs/NFRs existants ou en creent de nouveaux
- Les items `[NON IMPLEMENTE]` deviennent des FRs marques `status: pending`
- Les items `[DECISION]` vont dans la section "Architectural Decisions" ou "Constraints"
- Les items `[PARTIEL]` deviennent des FRs marques `status: partial — [ce qui manque]`
- Mettre a jour les success criteria si impactes
- Les user journeys sont mis a jour si le flux utilisateur change

**Prompt pour le sous-agent :**
```
Tu es le PRD Agent. Tu recois un rapport d'audit de conversation et tu dois mettre a jour le PRD.

RAPPORT D'AUDIT :
{rapport_audit}

REGLES :
1. Lis d'abord le PRD complet
2. Les [NON IMPLEMENTE] sont des FRs "pending" — ils DOIVENT apparaitre
3. Les [DECISION] vont dans Architectural Decisions
4. Ne supprime jamais un FR existant sans [RETIRE]
5. Backup avant modification
6. Retourne le diff complet (avant/apres)
```

#### Sous-agent 3 : Archi Agent

**Document cible :** `docs/architecture.md`

**Regles specifiques :**
- Les items `[OK]` enrichissent les composants/relations existants
- Les items `[DECISION]` deviennent des ADRs (Architecture Decision Records) avec format :
  ```markdown
  ### ADR-NNN : [Titre de la decision]
  - **Date :** YYYY-MM-DD
  - **Status :** Accepte
  - **Contexte :** [pourquoi cette decision]
  - **Decision :** [ce qui a ete choisi]
  - **Alternatives :** [ce qui a ete rejete et pourquoi]
  - **Source :** Conversation (message #N)
  ```
- Les nouveaux composants sont classes selon la taxonomie existante (`[CORE]`, `[FEAT]`, `[SUB]`, `[HOOK]`, `[UTIL]`)
- Les nouvelles relations utilisent les types existants (`-->`, `==>`, `<--`, `==>DB`)
- Mettre a jour le data flow si impacte

**Prompt pour le sous-agent :**
```
Tu es l'Archi Agent. Tu recois un rapport d'audit de conversation et tu dois mettre a jour architecture.md.

RAPPORT D'AUDIT :
{rapport_audit}

REGLES :
1. Lis d'abord architecture.md complet
2. Les [DECISION] deviennent des ADRs — format standardise
3. Classe les nouveaux composants selon [CORE/FEAT/SUB/HOOK/UTIL]
4. Les relations utilisent -->, ==>, <--, ==>DB
5. Ne supprime jamais un composant/relation sans [RETIRE]
6. Backup avant modification
7. Retourne le diff complet (avant/apres)
```

### Phase 3 : Validation et rapport final

1. **Collecter les diffs des 3 sous-agents**

2. **Presenter un rapport consolide a l'utilisateur :**
   ```
   ## Propagation documentaire — Validation

   ### Product Specification
   Fichiers modifies : [liste]
   Ajouts : +N lignes
   [Diff resume ou complet selon taille]

   ### PRD
   Fichiers modifies : prd.md
   Ajouts : +N lignes
   [Diff resume ou complet selon taille]

   ### Architecture
   Fichiers modifies : architecture.md
   Ajouts : +N lignes, N nouveaux ADRs
   [Diff resume ou complet selon taille]

   Valider et appliquer ? (oui / non / par doc)
   ```

3. **Appliquer selon la reponse :**
   - **oui** : ecrire tous les fichiers, backup avant chaque ecriture
   - **non** : annuler, rien n'est ecrit
   - **par doc** : l'utilisateur valide chaque doc individuellement

4. **Nettoyer le marqueur prd-pending :**
   - Si `_backup/prd-pending.marker` existe a la racine du projet, le supprimer (le prd a ete execute avec succes)

5. **Rapport final :**
   ```
   ## /update-prd termine

   Audit : X items extraits
     - [OK] : N
     - [NON IMPLEMENTE] : N
     - [PARTIEL] : N
     - [DECISION] : N
     - [DIFFERE] : N
     - [RETIRE] : N

   Sous-agents lances : [PS, PRD, Archi] (ou sous-ensemble)
   Sous-agents skippés : [PRD — pas de prd.md, PS modulaire fait office de PRD] (si applicable)

   Documents mis a jour :
     - product-specification.md : +X lignes (lister uniquement les docs modifies)
     - specs/module-a.md : +X lignes
     - prd.md : +X lignes
     - architecture.md : +X lignes, +N ADRs

   Rapport d'audit sauvegarde :
     - docs/_backup/audit-reports/current/audit-report_latest.md
   ```
