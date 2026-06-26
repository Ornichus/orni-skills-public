---
name: project-status-snapshot
description: Genere et maintient un snapshot condense du projet (JSON + rapport humain 4 sections). Utilise par /update et /orni-status.
user-invocable: false
---

# Project Status Snapshot

> **Version**: 1.0.0 | **Derniere mise a jour**: 24 mars 2026

Genere un rapport d'etat condense du projet en deux formats : JSON machine-readable (`project-status.json`) et rapport humain structuré (4 sections). Complementaire a project-state.xml (exhaustif, pour agents), le snapshot est leger et destine aux humains et scripts.

## 1. Schema JSON

Le fichier `project-status.json` se trouve a la racine du projet.

### Structure

```json
{
  "project": "<slug>",
  "current": {
    "snapshot_date": "<ISO 8601>",
    "session": "<session-id>",
    "phase": "<phase actuelle>",
    "question": "<question/objectif principal de la session>",
    "summary": "<resume en 1 phrase>",
    "decisions": [
      {
        "topic": "<sujet>",
        "analysis": "<axe d'analyse>",
        "result": "<verdict clair>",
        "status": "todo | done | deferred"
      }
    ],
    "next_actions": ["<action 1>", "<action 2>"],
    "blockers": ["<bloqueur>" ],
    "metrics": {
      "progress_percent": "<0-100, optionnel>",
      "tests_passing": "<bool, optionnel>",
      "deployed": "<bool, optionnel>"
    }
  },
  "history": [
    {
      "snapshot_date": "<ISO 8601>",
      "session": "<session-id>",
      "phase": "<phase>",
      "summary": "<resume 1 phrase>",
      "key_decisions": ["<decision 1>", "<decision 2>"]
    }
  ]
}
```

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `project` | string | Slug du projet (resolution standard section 2 du SKILL mailbox) |
| `current` | object | Snapshot actuel complet |
| `current.snapshot_date` | string | Date ISO 8601 de generation |
| `current.session` | string | Identifiant de session (depuis project-state.xml) |
| `current.phase` | string | Phase actuelle (brainstorming, development, testing, consolidation, etc.) |
| `current.question` | string | Question/objectif principal de la session, dans les mots de l'utilisateur |
| `current.summary` | string | Resume de la session en 1 phrase. Si impossible en 1 phrase, clarifier davantage |
| `current.decisions` | array | Decisions/choix significatifs de la session |
| `current.next_actions` | array | Prochaines actions (top 3-5, depuis les taches todo de project-state.xml) |
| `current.blockers` | array | Bloqueurs identifies (vide si aucun) |
| `current.metrics` | object | Metriques projet — cles bien-connues + libre par projet |
| `history` | array | Max 3 snapshots precedents (condenses) |

## 2. Regles de generation

Quand `/update` met a jour le snapshot :

### Rotation historique

1. Lire le fichier `project-status.json` existant
2. Si `current.snapshot_date` n'est PAS null (un snapshot precedent existe) :
   - Condenser `current` en objet historique : garder uniquement `snapshot_date`, `session`, `phase`, `summary`, et extraire `key_decisions` depuis `decisions[].topic + ": " + decisions[].result`
   - Inserer cet objet en position 0 de `history`
   - Si `history` depasse 3 entrees, supprimer la plus ancienne (derniere position)
3. Si `current.snapshot_date` EST null (premiere fois) : ne pas toucher `history`

### Remplissage de `current`

Remplir chaque champ depuis ces sources (par priorite) :

| Champ | Source |
|-------|--------|
| `snapshot_date` | Date/heure courante ISO 8601 |
| `session` | `<session-id>` de project-state.xml, ou "unknown" si absent |
| `phase` | `<phase>` ou `<current-state><status>` de project-state.xml, ou deduit du contexte |
| `question` | Synthetiser depuis `<current-objective>` de project-state.xml ou contexte conversation |
| `summary` | Synthese 1 phrase de ce qui a ete accompli (depuis resume utilisateur etape 2 de /update) |
| `decisions` | Decisions/choix significatifs identifies dans la session |
| `next_actions` | Taches de project-state.xml avec status=todo (top 3-5) |
| `blockers` | Depuis contexte conversation (vide si aucun) |
| `metrics.progress_percent` | Depuis `<progress-percent>` de project-state.xml si disponible |

## 3. Format humain (4 sections)

La commande `/orni-status` lit `project-status.json` et affiche :

### Mode complet (defaut)

```
## Status : {project}
**Session :** {session} | **Phase :** {phase} | **Date :** {snapshot_date}

### 1. Question de depart
{question}

### 2. Ce qui s'est passe
{narrative derivee des decisions — 1-2 phrases par decision significative}

### 3. Synthese
| Problematique | Axe d'analyse | Resultat | Status |
|---------------|---------------|----------|--------|
| {topic} | {analysis} | **{result}** | {status} |

Regles : 1 ligne par problematique, max 8-10 lignes, verdict en gras, pas de nuances.

### 4. Resume
> {summary}

### Prochaines actions
- {next_actions}

### Bloqueurs
- {blockers, ou "Aucun"}
```

### Mode rapide (`/status quick`)

```
## {project} — {phase}

> {summary}

**A faire :** {next_actions en ligne}
**Bloqueurs :** {blockers ou "Aucun"}
```

## 4. Cles metrics bien-connues

Ces cles sont documentees et utilisables pour du monitoring cross-projets. Toutes sont optionnelles.

| Cle | Type | Description |
|-----|------|-------------|
| `progress_percent` | number (0-100) | Pourcentage d'avancement global |
| `tests_passing` | boolean | Tests passent-ils ? |
| `deployed` | boolean | Deploye en production ? |
| `version` | string (semver) | Version actuelle |

L'objet `metrics` accepte toute cle additionnelle specifique au projet.

## 5. Relation avec project-state.xml

| | project-state.xml | project-status.json |
|---|---|---|
| Audience | Agents (rechargement contexte) | Humains + scripts |
| Contenu | Etat complet : taches, waves, architecture | Snapshot : question, decisions, resume |
| Taille | ~150 lignes | ~50 lignes |
| Historique | Dans `_backup/` archive | 3 entrees inline |
| Format | XML | JSON |

Les deux coexistent. `/update` alimente les deux.

## Changelog

- **1.0.0** (2026-03-24) : Version initiale — schema JSON, format humain 4 sections, mode quick, rotation historique
