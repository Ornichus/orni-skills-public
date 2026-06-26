---
description: 'Initialise le module Frontend Slides (HTML one-shot) dans le projet courant'
---

# /orni-init-fs - Initialiser Frontend Slides

Initialise la commande `/frontend-slides` et le skill `frontend-slides` dans le projet courant. Skill HTML one-shot pour pitch decks premium, brand mockups, decks one-off.

**Cohabite avec `marp-presentations`** : les deux skills sont complementaires (cf. `skills/frontend-slides/README-ORNI.md`).

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que `{ORNI}/skills/frontend-slides/SKILL.md` existe
   - Verifier si le module est deja installe : `.claude/commands/frontend-slides.md` dans le projet courant
   - Si deja installe : AVERTIR et demander confirmation avant de continuer

4. **Installer le module FS:**
   - Copier la commande : `{ORNI}/commands/frontend-slides.md` -> `.claude/commands/frontend-slides.md`
   - Copier le skill complet (recursif) : `{ORNI}/skills/frontend-slides/` -> `.claude/skills/frontend-slides/`
     - SKILL.md
     - README-ORNI.md
     - STYLE_PRESETS.md
     - viewport-base.css
     - html-template.md
     - animation-patterns.md
     - LICENSE
     - scripts/extract-pptx.py
     - scripts/deploy.sh
     - scripts/export-pdf.sh

5. **Post-install:**
   - Creer le repertoire de presentations si absent :
     ```bash
     mkdir -p docs/presentations
     ```
   - Verifier les dependances optionnelles :
     - `python -c "import pptx" 2>/dev/null` (pour PPT conversion). Sinon : informer `pip install python-pptx`
     - `node --version 2>/dev/null` (pour Vercel deploy + Playwright PDF). Sinon : informer install via https://nodejs.org

6. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le creer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/frontend-slides/SKILL.md` (pattern `**Version** : X.Y.Z`)
   - Ajouter/mettre a jour l'entree du module FS :
     ```json
     {
       "modules": {
         "FS": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/frontend-slides/SKILL.md"
         }
       }
     }
     ```

7. **Verification:**
   - Confirmer que `.claude/commands/frontend-slides.md` existe
   - Confirmer que `.claude/skills/frontend-slides/SKILL.md` existe
   - Confirmer que `.claude/skills/frontend-slides/scripts/extract-pptx.py` existe
   - Confirmer que `docs/presentations/` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler la commande disponible :
     - Generer : `/frontend-slides "Titre"` ou `/frontend-slides` (interactif)
     - Convertir PPT : `/frontend-slides convert fichier.pptx`
     - Enhancer existant : `/frontend-slides enhance fichier.html`
   - Mentionner la complementarite avec `/marp-slides` (renvoyer vers `README-ORNI.md`)
   - Si dependances optionnelles absentes : rappeler les instructions d'installation
