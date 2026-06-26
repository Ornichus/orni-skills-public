---
description: 'Initialise le module Design System (extract brand -> design-system.html + brand-book-a4.pdf) dans le projet courant'
---

# /orni-init-ds - Initialiser Design System

Initialise la commande `/design-system` et le skill `design-system` dans le projet courant. Skill pour generation d'artifacts publics partageables (HTML scrollable + PDF A4 print-ready) depuis une reference brand.

**Complementaire de `frontend-slides`** : design-system produit les artifacts publics, frontend-slides consomme la palette/typo extraite pour generer des decks brandes (cf. `skills/design-system/README-ORNI.md`).

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que `{ORNI}/skills/design-system/SKILL.md` existe
   - Verifier si le module est deja installe : `.claude/commands/design-system.md` dans le projet courant
   - Si deja installe : AVERTIR et demander confirmation avant de continuer

4. **Installer le module DS:**
   - Copier la commande : `{ORNI}/commands/design-system.md` -> `.claude/commands/design-system.md`
   - Copier le skill complet (recursif) : `{ORNI}/skills/design-system/` -> `.claude/skills/design-system/`
     - SKILL.md
     - README-ORNI.md
     - LICENSE
     - examples/template.html

5. **Post-install:**
   - Creer le repertoire de sortie si absent :
     ```bash
     mkdir -p design
     ```
   - Verifier les dependances obligatoires (rendering PDF) :
     - Windows : verifier presence `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
     - macOS : verifier `/Applications/Google Chrome.app`
     - Linux : verifier `which chromium` ou `which chrome`
     - Si absent : avertir l'utilisateur que le rendering PDF necessite Edge/Chrome/Chromium

6. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le creer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/design-system/SKILL.md` (pattern `**Version** : X.Y.Z`)
   - Ajouter/mettre a jour l'entree du module DS :
     ```json
     {
       "modules": {
         "DS": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/design-system/SKILL.md"
         }
       }
     }
     ```

7. **Verification:**
   - Confirmer que `.claude/commands/design-system.md` existe
   - Confirmer que `.claude/skills/design-system/SKILL.md` existe
   - Confirmer que `.claude/skills/design-system/examples/template.html` existe
   - Confirmer que `design/` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler la commande disponible :
     - Generer : `/design-system <URL ou description>` ou `/design-system` (interactif)
   - Mentionner la complementarite avec `/frontend-slides --new-style` (renvoyer vers `README-ORNI.md`)
   - Si Edge/Chrome absent : rappeler les instructions d'installation
