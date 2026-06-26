---
description: 'Initialise le module Web PDF Compile (capture articles -> PDF dossier groupe par pays) dans le projet courant'
---

# /orni-init-wpc - Initialiser Web PDF Compile

Initialise la commande `/web-pdf-compile` et le skill `web-pdf-compile` dans le projet courant. Skill Node.js pour transformer une liste d'URLs articles en PDF dossier organise par pays/categorie (article-only, adblock, layout adaptive).

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que `{ORNI}/skills/web-pdf-compile/SKILL.md` existe
   - Verifier si le module est deja installe : `.claude/commands/web-pdf-compile.md` dans le projet courant
   - Si deja installe : AVERTIR et demander confirmation avant de continuer

4. **Installer le module WPC:**
   - Copier la commande : `{ORNI}/commands/web-pdf-compile.md` -> `.claude/commands/web-pdf-compile.md`
   - Copier le skill complet (recursif) : `{ORNI}/skills/web-pdf-compile/` -> `.claude/skills/web-pdf-compile/`
     - SKILL.md
     - README.md
     - PROTOCOLE.md
     - package.json
     - scripts/capture.js
     - scripts/compile-pdf.js
     - scripts/probe-dom.js
     - examples/sources.example.json
     - examples/random-test.json

5. **Post-install:**
   - Creer le repertoire de sortie si absent :
     ```bash
     mkdir -p docs/dossiers
     ```
   - Verifier les dependances :
     - `node --version` (>= 18). Sinon : informer install via https://nodejs.org
     - Suggerer `cd .claude/skills/web-pdf-compile && npm install` (telecharge ~150MB de deps Puppeteer/Sharp)
     - Verifier presence de Chrome systeme (Puppeteer-core depend du Chrome systeme, pas Chromium bundle) :
       ```bash
       ls "C:\Program Files\Google\Chrome\Application\chrome.exe" 2>/dev/null || \
       ls "/Applications/Google Chrome.app" 2>/dev/null || \
       which google-chrome || which chromium
       ```
     - Si Chrome absent : informer install via https://www.google.com/chrome/

6. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le creer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/web-pdf-compile/SKILL.md` (pattern `version: X.Y.Z` dans frontmatter)
   - Ajouter/mettre a jour l'entree du module WPC :
     ```json
     {
       "modules": {
         "WPC": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/web-pdf-compile/SKILL.md"
         }
       }
     }
     ```

7. **Verification:**
   - Confirmer que `.claude/commands/web-pdf-compile.md` existe
   - Confirmer que `.claude/skills/web-pdf-compile/SKILL.md` existe
   - Confirmer que `.claude/skills/web-pdf-compile/scripts/capture.js` existe
   - Confirmer que `.claude/skills/web-pdf-compile/scripts/compile-pdf.js` existe
   - Confirmer que `.claude/skills/web-pdf-compile/examples/random-test.json` existe
   - Confirmer que `docs/dossiers/` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler les commandes disponibles :
     - Compiler : `/web-pdf-compile <sources.json>` ou `/web-pdf-compile` (interactif)
     - Probe selectors : `/web-pdf-compile probe <url>`
     - Test rapide : `/web-pdf-compile examples/sources.example.json` (apres `npm install`)
   - Si dependances manquantes : rappeler `cd .claude/skills/web-pdf-compile && npm install`
   - Mentionner la categorie : "Recherche & Documentation"
