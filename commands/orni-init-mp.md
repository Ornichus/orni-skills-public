---
description: 'Initialise le module Marp Presentations dans le projet courant'
---

# /orni-init-mp - Initialiser Marp Presentations

Initialise la commande `/marp-slides` et le skill marp-presentations dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier si le module est déjà installé : `.claude/commands/marp-slides.md` dans le projet courant
   - Si déjà installé : AVERTIR et demander confirmation avant de continuer

4. **Installer le module MP:**
   - Suivre le manifeste "Module MP" du SKILL.md
   - Copier la commande : `marp-slides.md`
   - Copier le skill `marp-presentations/` (SKILL.md)

5. **Post-install:**
   - Créer le répertoire de slides si absent :
     ```bash
     mkdir -p docs/slides
     ```
   - Vérifier si Marp CLI est installé :
     ```bash
     marp --version 2>/dev/null || npx @marp-team/marp-cli --version 2>/dev/null
     ```
   - Si Marp CLI absent : informer l'utilisateur des options d'installation :
     - `scoop install marp` (Windows)
     - `npm install -g @marp-team/marp-cli`
     - `npx @marp-team/marp-cli` (usage ponctuel, sans installation)
   - Vérifier si l'extension VS Code `marp-team.marp-vscode` est recommandée :
     - Si `.vscode/extensions.json` existe : ajouter `marp-team.marp-vscode` aux recommendations
     - Sinon : informer "Extension VS Code recommandée : `marp-team.marp-vscode`"

6. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le créer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/marp-presentations/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre à jour l'entrée du module MP :
     ```json
     {
       "modules": {
         "MP": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/marp-presentations/SKILL.md"
         }
       }
     }
     ```

7. **Vérification:**
   - Confirmer que `.claude/commands/marp-slides.md` existe
   - Confirmer que `.claude/skills/marp-presentations/SKILL.md` existe
   - Confirmer que `docs/slides/` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler la commande disponible :
     - Générer : `/marp-slides "Titre"` ou `/marp-slides` (interactif)
   - Mentionner les options d'export : `marp fichier.md --pdf` / `--pptx` / `--html`
   - Si Marp CLI absent : rappeler les instructions d'installation
