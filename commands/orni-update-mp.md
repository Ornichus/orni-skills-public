---
description: 'Met à jour le module Marp Presentations dans le projet courant'
---

# /orni-update-mp - Mettre à jour Marp Presentations

Met à jour la commande `/marp-slides` et le skill marp-presentations dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que le module EST installé : `.claude/commands/marp-slides.md` dans le projet courant
   - Si PAS installé : AVERTIR et suggérer `/orni-init-mp` puis abandonner

4. **Mettre à jour le module MP:**
   - Suivre le manifeste "Module MP" du SKILL.md (logique Update)
   - Copier la commande `marp-slides.md` en écrasement
   - Copier le skill `marp-presentations/` en écrasement
   - NE PAS TOUCHER aux présentations existantes dans `docs/slides/`

5. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/marp-presentations/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Mettre à jour l'entrée MP : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Vérification:**
   - Confirmer que `.claude/commands/marp-slides.md` existe
   - Confirmer que `.claude/skills/marp-presentations/SKILL.md` existe

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler la commande disponible :
     - Générer : `/marp-slides "Titre"` ou `/marp-slides` (interactif)
   - Préciser : "Les présentations existantes dans `docs/slides/` n'ont pas été modifiées."
