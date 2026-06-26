---
description: 'Met a jour le module Design System dans le projet courant'
---

# /orni-update-ds - Mettre a jour Design System

Met a jour la commande `/design-system` et le skill `design-system` dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que le module EST installe : `.claude/commands/design-system.md` dans le projet courant
   - Si PAS installe : AVERTIR et suggerer `/orni-init-ds` puis abandonner

4. **Mettre a jour le module DS:**
   - Copier la commande `{ORNI}/commands/design-system.md` en ecrasement
   - Copier le skill `{ORNI}/skills/design-system/` en ecrasement (recursif)
   - **NE PAS TOUCHER** aux artifacts existants dans `design/` (design-system.html / brand-book-a4.pdf precedents)

5. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/design-system/SKILL.md` (pattern `**Version** : X.Y.Z`)
   - Mettre a jour l'entree DS : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Verification:**
   - Confirmer que `.claude/commands/design-system.md` existe
   - Confirmer que `.claude/skills/design-system/SKILL.md` existe
   - Confirmer que `.claude/skills/design-system/examples/template.html` existe
   - Confirmer que `.claude/skills/design-system/README-ORNI.md` existe

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler la commande disponible :
     - Generer : `/design-system <URL ou description>` ou `/design-system` (interactif)
   - Preciser : "Les artifacts existants dans `design/` n'ont pas ete modifies."
