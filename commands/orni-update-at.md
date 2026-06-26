---
description: 'Met à jour ATeam (Team Builder + Council) dans le projet courant'
---

# /orni-update-at - Mettre à jour ATeam (Team Builder + Council)

Met à jour les commandes `/ateam` et `/ateam-council` et le skill ateam dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que le module EST installé : `.claude/commands/ateam.md` dans le projet courant
   - Si PAS installé : AVERTIR et suggérer `/orni-init-at` puis abandonner

4. **Mettre à jour le module AT:**
   - Suivre le manifeste "Module AT" du SKILL.md (logique Update)
   - Copier les commandes : `ateam.md` et `ateam-council.md` en écrasement
   - Copier le skill `ateam/` (récursif) en écrasement (SKILL.md, README.md, COUNCIL.md, council-scenarios.md, council-workflow.png, council-interaction.png)

5. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/ateam/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Mettre à jour l'entrée AT : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Vérification:**
   - Confirmer que `.claude/commands/ateam.md` existe
   - Confirmer que `.claude/commands/ateam-council.md` existe
   - Confirmer que `.claude/skills/ateam/SKILL.md` existe
   - Confirmer que `.claude/skills/ateam/COUNCIL.md` existe

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler les commandes disponibles :
     - Composer une équipe : `/ateam suggest` ou `/ateam` (interactif)
     - Délibération collaborative : `/ateam-council`
