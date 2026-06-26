---
description: 'Initialise ATeam (Team Builder + Council) dans le projet courant'
---

# /orni-init-at - Initialiser ATeam (Team Builder + Council)

Initialise les commandes `/ateam` et `/ateam-council` et le skill ateam dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que `{ORNI}/skills/ateam/SKILL.md` existe
   - Vérifier si le module est déjà installé : `.claude/commands/ateam.md` dans le projet courant
   - Si déjà installé : AVERTIR et demander confirmation avant de continuer

4. **Installer le module AT:**
   - Suivre le manifeste "Module AT" du SKILL.md
   - Copier les commandes : `ateam.md` et `ateam-council.md`
   - Copier le skill complet (récursif) : `{ORNI}/skills/ateam/` -> `.claude/skills/ateam/`
     - SKILL.md
     - README.md
     - COUNCIL.md
     - council-scenarios.md
     - council-workflow.png
     - council-interaction.png

5. **Post-install:**
   - Le profil de test du Team Builder s'appuie sur Agent Browser : vérifier si le module AB est installé (`.claude/skills/agent-browser/SKILL.md`)
   - Si AB absent : informer "Le module Agent Browser est recommandé pour le profil de test. Installez-le avec `/orni-init-ab`."

6. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le créer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/ateam/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre à jour l'entrée du module AT :
     ```json
     {
       "modules": {
         "AT": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/ateam/SKILL.md"
         }
       }
     }
     ```

7. **Vérification:**
   - Confirmer que `.claude/commands/ateam.md` existe
   - Confirmer que `.claude/commands/ateam-council.md` existe
   - Confirmer que `.claude/skills/ateam/SKILL.md` existe
   - Confirmer que `.claude/skills/ateam/COUNCIL.md` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler les commandes disponibles :
     - Composer une équipe : `/ateam suggest` ou `/ateam` (interactif)
     - Délibération collaborative : `/ateam-council`
