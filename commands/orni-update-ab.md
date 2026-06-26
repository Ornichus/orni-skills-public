---
description: 'Met à jour Agent Browser dans le projet courant'
---

# /orni-update-ab - Mettre à jour Agent Browser

Met à jour la commande `/setup-agent-browser` et le skill agent-browser dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que le module EST installé : `.claude/skills/agent-browser/SKILL.md` dans le projet courant
   - Si PAS installé : AVERTIR et suggérer `/orni-init-ab` puis abandonner

4. **Mettre à jour le module AB:**
   - Suivre le manifeste "Module AB" du SKILL.md (logique Update)
   - Copier la commande : `setup-agent-browser.md` en écrasement
   - Copier le skill `agent-browser/` (récursif) en écrasement (SKILL.md, DOCUMENTATION.md)

5. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/agent-browser/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Mettre à jour l'entrée AB : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Vérification:**
   - Confirmer que `.claude/commands/setup-agent-browser.md` existe
   - Confirmer que `.claude/skills/agent-browser/SKILL.md` existe
   - Confirmer que `.claude/skills/agent-browser/DOCUMENTATION.md` existe

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler que la configuration Windows/WSL se fait via `/setup-agent-browser`
   - Rappeler la commande disponible :
     - Configurer : `/setup-agent-browser`
