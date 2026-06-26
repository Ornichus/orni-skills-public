---
description: 'Met a jour le module Architecture Relationnelle v2.0.0 dans le projet courant'
---

# /orni-update-archi - Mettre a jour Architecture Relationnelle

Met a jour le skill de cartographie d'architecture relationnelle dans le projet courant.

## Instructions

### 1. Charger le skill source

Lire `~/.claude/orni-skills.json` pour trouver le chemin Orni-skills (`ORNI`).
Puis lire `{ORNI}/skills/architecture/SKILL.md` pour recuperer la version source.

### 2. Pre-flight

- Verifier que `.claude/skills/architecture/SKILL.md` existe (sinon : proposer `/orni-init-archi`)
- Lire la version actuellement installee
- Comparer avec la version source

### 3. Mettre a jour

Copier en ecrasant :

```
{ORNI}/skills/architecture/SKILL.md  →  .claude/skills/architecture/SKILL.md
{ORNI}/commands/architecture.md      →  .claude/commands/architecture.md
```

### 4. Mettre a jour le manifeste

Dans `.claude/orni-manifest.json`, mettre a jour l'entree AR :
- `version` : nouvelle version
- `updated_at` : date courante ISO 8601 UTC
- **Preserver** `installed_at`

### 5. Rapport

```
/orni-update-archi termine

| Element | Avant | Apres |
|---------|-------|-------|
| Version | [old] | [new] |
| SKILL.md | Mis a jour | ✓ |
| Commande | Mis a jour | ✓ |
| Manifeste | updated_at | [date] |
```
