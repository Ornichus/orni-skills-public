---
description: 'Met à jour Project State Management (gestion de project-state.xml) dans le projet courant'
---

# /orni-update-psm - Mettre à jour Project State Management

Met à jour le skill project-state-management (gestion de `project-state.xml`) dans le projet courant.

> Ce module est un **skill seul** : il n'a pas de commande dédiée. Il est consommé par `/update` et `/followup`. Cette commande ne met à jour que le skill.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que le module EST installé : `.claude/skills/project-state-management/SKILL.md` dans le projet courant
   - Si PAS installé : AVERTIR et suggérer `/orni-init-psm` puis abandonner

4. **Mettre à jour le module PSM:**
   - Suivre le manifeste "Module PSM" du SKILL.md (logique Update)
   - Copier le skill `project-state-management/` (récursif) en écrasement (SKILL.md, README.md, template/project-state-template.xml)
   - NE PAS TOUCHER au `project-state.xml` existant à la racine du projet (uniquement le template du skill)

5. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/project-state-management/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Mettre à jour l'entrée PSM : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Vérification:**
   - Confirmer que `.claude/skills/project-state-management/SKILL.md` existe
   - Confirmer que `.claude/skills/project-state-management/README.md` existe
   - Confirmer que `.claude/skills/project-state-management/template/project-state-template.xml` existe

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Préciser : "Le `project-state.xml` du projet n'a pas été modifié — seul le skill a été mis à jour."
