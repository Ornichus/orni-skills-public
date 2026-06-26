---
description: 'Met a jour le module Project Status Snapshot dans le projet courant'
---

# /orni-update-pss - Mettre a jour Project Status Snapshot

Met a jour le skill et la commande /orni-status sans toucher aux donnees (project-status.json).

## Instructions

### 1. Charger le skill source

Lire `~/.claude/orni-skills.json` pour trouver le chemin Orni-skills (`ORNI`).
Lire `{ORNI}/skills/project-status-snapshot/SKILL.md` pour recuperer la version source.

### 2. Pre-flight

- Verifier que `.claude/skills/project-status-snapshot/SKILL.md` existe (sinon proposer `/orni-init-pss`)
- Comparer la version installee avec la version source
- Si versions identiques : informer et demander confirmation pour reinstaller

### 3. Mettre a jour

```
Fichiers a copier (ecrasement) :
  {ORNI}/skills/project-status-snapshot/SKILL.md  →  .claude/skills/project-status-snapshot/SKILL.md
  {ORNI}/commands/orni-status.md                    →  .claude/commands/orni-status.md
```

**Ne PAS toucher** `project-status.json` (donnees utilisateur).

### 4. Mettre a jour le manifeste

Mettre a jour dans `.claude/orni-manifest.json` :
- `version` : nouvelle version
- `updated_at` : date courante ISO 8601
- Conserver `installed_at` (ne pas modifier)

### 5. Rapport

```
/orni-update-pss termine

| Element | Avant | Apres |
|---------|-------|-------|
| SKILL.md | v{old} | v{new} |
| /orni-status command | Mise a jour | |
| project-status.json | Non touche | |
| Manifeste | Mis a jour | |
```
