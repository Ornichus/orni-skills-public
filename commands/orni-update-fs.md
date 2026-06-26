---
description: 'Met a jour le module Frontend Slides (HTML one-shot) dans le projet courant'
---

# /orni-update-fs - Mettre a jour Frontend Slides

Met a jour la commande `/frontend-slides` et le skill `frontend-slides` dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que le module EST installe : `.claude/commands/frontend-slides.md` dans le projet courant
   - Si PAS installe : AVERTIR et suggerer `/orni-init-fs` puis abandonner

4. **Mettre a jour le module FS:**
   - Copier la commande `{ORNI}/commands/frontend-slides.md` en ecrasement
   - Copier le skill `{ORNI}/skills/frontend-slides/` en ecrasement (recursif)
   - **NE PAS TOUCHER** aux presentations existantes dans `docs/presentations/`
   - **NE PAS TOUCHER** au dossier `.claude-design/` si present (cache de previews)

5. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/frontend-slides/SKILL.md` (pattern `**Version** : X.Y.Z`)
   - Mettre a jour l'entree FS : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Verification:**
   - Confirmer que `.claude/commands/frontend-slides.md` existe
   - Confirmer que `.claude/skills/frontend-slides/SKILL.md` existe
   - Confirmer que tous les fichiers du skill sont presents (STYLE_PRESETS.md, viewport-base.css, html-template.md, animation-patterns.md, README-ORNI.md, scripts/*)

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler la commande disponible :
     - Generer : `/frontend-slides "Titre"` ou `/frontend-slides` (interactif)
   - Preciser : "Les presentations existantes dans `docs/presentations/` n'ont pas ete modifiees."
