---
description: 'Met a jour le module Web PDF Compile dans le projet courant'
---

# /orni-update-wpc - Mettre a jour Web PDF Compile

Met a jour la commande `/web-pdf-compile` et le skill `web-pdf-compile` dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que le module EST installe : `.claude/commands/web-pdf-compile.md` dans le projet courant
   - Si PAS installe : AVERTIR et suggerer `/orni-init-wpc` puis abandonner

4. **Mettre a jour le module WPC:**
   - Copier la commande `{ORNI}/commands/web-pdf-compile.md` en ecrasement
   - Copier le skill `{ORNI}/skills/web-pdf-compile/` en ecrasement (recursif)
     - SKILL.md, README.md, PROTOCOLE.md, package.json
     - scripts/* (capture.js, compile-pdf.js, probe-dom.js)
     - examples/* (sources.example.json, random-test.json)
   - **NE PAS TOUCHER** au dossier `node_modules/` du skill (preserve les deps installees)
   - **NE PAS TOUCHER** aux dossiers de sortie `docs/dossiers/` ou `output/` du projet

5. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/web-pdf-compile/SKILL.md` (pattern `version: X.Y.Z` dans frontmatter)
   - Mettre a jour l'entree WPC : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Post-update:**
   - Si `package.json` a change (nouvelle deps) : suggerer `cd .claude/skills/web-pdf-compile && npm install` pour synchroniser
   - Comparer ancien et nouveau `package.json` deps si possible

7. **Verification:**
   - Confirmer que `.claude/commands/web-pdf-compile.md` existe
   - Confirmer que tous les fichiers du skill sont presents (SKILL.md, scripts/*, examples/*)

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler la commande disponible : `/web-pdf-compile`
   - Preciser : "Les dossiers de sortie existants n'ont pas ete modifies."
