---
description: 'Affiche l etat de la documentation projet (PS, PRD, architecture.md)'
---

# /followup-prd - Etat de la documentation

Affiche un resume de l'etat des documents architecture et des tags de statut poses par /update-prd.

## Instructions

### 0. Verifier le marqueur prd-pending

Chercher `_backup/prd-pending.marker` a la racine du projet.

Si le fichier existe :
- Lire son contenu (date, session, raison)
- Afficher une alerte visible :
  ```
  ⚠ /update-prd en attente depuis {DEFERRED_AT} (session {SESSION_ID})
  → Contexte frais disponible. Recommandation : lancer /update-prd maintenant.
  ```

### 1. Detecter les documents existants

Chercher dans `docs/` :
- `docs/architecture.md`
- `docs/product-specification.md`
- `docs/specs/*.md` (modules PS si structure modulaire)
- `docs/prd.md`
- `docs/_backup/audit-reports/current/audit-report_latest.md`

Pour chaque document trouve, noter sa date de derniere modification.
Pour chaque document absent, le signaler.

### 2. Scanner les tags de statut

Pour chaque document trouve, scanner les tags suivants :
- `[NON IMPLEMENTE]`
- `[PARTIEL]`
- `[RETIRE]`
- `[DIFFERE]`
- `[DECISION]`

Compter les occurrences de chaque tag par document.

### 3. Lire le dernier rapport d'audit

Si `docs/_backup/audit-reports/current/audit-report_latest.md` existe :
- Lire le rapport
- Extraire le resume (nombre d'items par tag)
- Extraire la date du rapport

### 4. Afficher le resume

```
## Etat Documentation — [NOM_PROJET]

### Documents

| Document | Derniere modif | Status |
|----------|---------------|--------|
| architecture.md | YYYY-MM-DD | Present / Absent |
| product-specification.md | YYYY-MM-DD | Present / Absent |
| specs/*.md | YYYY-MM-DD | N modules / Absent |
| prd.md | YYYY-MM-DD | Present / Absent |

### Tags de statut

| Tag | architecture.md | PS | PRD | Total |
|-----|----------------|-----|-----|-------|
| [NON IMPLEMENTE] | N | N | N | N |
| [PARTIEL] | N | N | N | N |
| [RETIRE] | N | N | N | N |
| [DIFFERE] | N | N | N | N |
| [DECISION] | N | N | N | N |

### Dernier audit

- **Date :** YYYY-MM-DD HH:MM (ou "Aucun audit")
- **Items :** N total
- **Resume :** [OK]: N, [NON IMPLEMENTE]: N, [PARTIEL]: N, ...

### Recommandations

- Si beaucoup de [NON IMPLEMENTE] : "Lancer /update-prd pour propager les changements recents"
- Si aucun audit : "Lancer /update-prd pour un premier audit"
- Si docs absents : "Lancer /architecture pour generer la documentation initiale"
- Si docs anciens (> 7 jours) : "Documentation potentiellement desynchronisee"
```
