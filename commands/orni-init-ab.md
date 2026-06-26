---
description: 'Initialise Agent Browser dans le projet courant'
---

# /orni-init-ab - Initialiser Agent Browser

Initialise la commande `/setup-agent-browser` et le skill agent-browser dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que `{ORNI}/skills/agent-browser/SKILL.md` existe
   - Vérifier si le module est déjà installé : `.claude/skills/agent-browser/SKILL.md` dans le projet courant
   - Si déjà installé : AVERTIR et demander confirmation avant de continuer

4. **Installer le module AB:**
   - Suivre le manifeste "Module AB" du SKILL.md
   - Copier la commande : `setup-agent-browser.md`
   - Copier le skill complet (récursif) : `{ORNI}/skills/agent-browser/` -> `.claude/skills/agent-browser/`
     - SKILL.md
     - DOCUMENTATION.md

5. **Post-install:**
   - **Vérifier si le CLI est déjà configuré** : exécuter `agent-browser --version 2>/dev/null`
     - Si OK : noter "AB CLI déjà configuré (vX.Y.Z)"
     - Si échec : rappeler que la configuration Windows/WSL se fait via `/setup-agent-browser`

6. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le créer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/agent-browser/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre à jour l'entrée du module AB :
     ```json
     {
       "modules": {
         "AB": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/agent-browser/SKILL.md"
         }
       }
     }
     ```

7. **Vérification:**
   - Confirmer que `.claude/commands/setup-agent-browser.md` existe
   - Confirmer que `.claude/skills/agent-browser/SKILL.md` existe
   - Confirmer que `.claude/skills/agent-browser/DOCUMENTATION.md` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler que la configuration Windows/WSL se fait via `/setup-agent-browser`
   - Rappeler la commande disponible :
     - Configurer : `/setup-agent-browser`
