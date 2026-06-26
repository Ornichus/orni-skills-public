---
description: 'Met à jour le module Task Orchestrator dans le projet courant'
---

# /orni-update-to — Update Task Orchestrator

Met à jour le skill `task-orchestrator` + commande `/orchestrate` depuis la source Orni.

## Instructions

1. **Résoudre le chemin source Orni :**
   - Lire `~/.claude/orni-skills.json` → `source_path` → `{ORNI}`

2. **Vérifier installation :**
   - `.claude/skills/task-orchestrator/SKILL.md` existe
   - Si absent : avertir "Module TO non installé" + suggérer `/orni-init-to`

3. **Copier en écrasement :**
   - `cp {ORNI}/skills/task-orchestrator/SKILL.md .claude/skills/task-orchestrator/SKILL.md`
   - `cp {ORNI}/commands/orchestrate.md .claude/commands/orchestrate.md`

4. **NE PAS TOUCHER :**
   - `.orchestrate/state.json` (état runtime user)
   - `.orchestrate/kpis.yaml` (KPIs paramétrés user)

5. **Mettre à jour le manifeste :**
   - Lire version depuis `{ORNI}/skills/task-orchestrator/SKILL.md` (pattern `**Version:** X.Y.Z`)
   - Update `.claude/orni-manifest.json` entrée TO : `version` + `updated_at` (preserve `installed_at`)

6. **Vérification + rapport :**
   ```
   ## /orni-update-to terminé

   Module TO mis à jour : v<old> → v<new>

   Fichiers préservés : .orchestrate/state.json, .orchestrate/kpis.yaml
   ```

## Référence

Skill : `.claude/skills/task-orchestrator/SKILL.md`.
