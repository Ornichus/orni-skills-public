---
description: 'Met à jour tous les composants Orni-Skills installés dans le projet courant (incl. Excal/Deploy optionnels)'
---

# /orni-update-full - Mise à jour complète Orni-Skills

Met à jour tous les composants Orni-Skills installés dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol - Détecter les modules installés:**
   - Vérifier chaque fichier marqueur:
     - BMAD: `_bmad/core/config.yaml`
     - UF: `.claude/commands/update.md`
     - AB: `.claude/commands/setup-agent-browser.md`
     - AT: `.claude/commands/ateam.md`
     - ML: `.claude/commands/mail-send.md`
     - VPS: `.claude/skills/vps/SKILL.md`
     - FAL: `.claude/skills/fal-image-gen/SKILL.md`
     - CF: `.claude/skills/cloudflare/SKILL.md`
     - EX: `.claude/skills/excal-diagram/SKILL.md`
     - DPL: `.claude/skills/deploy/SKILL.md`
     - AR: `.claude/skills/architecture/SKILL.md`
     - MP: `.claude/skills/marp-presentations/SKILL.md`
     - FS: `.claude/skills/frontend-slides/SKILL.md`
     - DS: `.claude/skills/design-system/SKILL.md`
     - WPC: `.claude/skills/web-pdf-compile/SKILL.md`
     - TO: `.claude/skills/task-orchestrator/SKILL.md`
   - Lister les modules détectés et ceux qui sont absents
   - Si AUCUN module installé : AVERTIR et suggérer `/orni-init-full`

4. **Mettre à jour chaque module installé:**

   Pour chaque module détecté, suivre la logique Update du SKILL.md:

   **4a. BMAD (si installé):**
   - Copier les commandes `bmad-*.md` et le dossier `_bmad/`
   - NE PAS toucher `_bmad-output/`

   **4b. UF (si installé):**
   - Copier les 3 commandes + skill project-state-management/
   - NE PAS toucher `project-state.xml`, CLAUDE.md, `_backup/`

   **4c. AB (si installé):**
   - Copier commande + skill + documentation

   **4c.5. AT (si installé):**
   - Copier commande ateam.md + skill ateam/

   **4c.6. ML (si installé):**
   - Copier commandes : `mail-send.md`, `mail-read.md` en écrasement
   - Copier skill `mailbox/` en écrasement (SKILL.md, README.md)
   - NE PAS TOUCHER aux messages dans `~/.claude/mailbox/`

   **4d. Extras (settings + meta-commandes orni):**
   - Copier settings-template.json
   - Copier/mettre à jour toutes les meta-commandes `{ORNI}/commands/orni-*.md` vers `.claude/commands/` (toujours)

   **4e. VPS (si installé):**
   - Copier le skill `vps/` en écrasement (SKILL.md)
   - Vérifier la connexion SSH
   - Vérifier si `hostinger-api-mcp` a une mise à jour npm

   **4f. FAL (si installe):**
   - Rebuild MCP server : `npm install` + `npm run build` dans `<VOTRE_DOSSIER_MCP>/fal-image-gen`
   - Copier `skills/fal-image-gen/SKILL.md` en ecrasement
   - Verifier la config MCP dans `~/.claude/settings.json`
   - NE PAS TOUCHER a `FAL_KEY` existante

   **4g. CF (si installé):**
   - Copier le skill `cloudflare/` en écrasement (SKILL.md)
   - Vérifier la connexion API Cloudflare
   - NE PAS TOUCHER à `~/.claude/cloudflare.json`

   **4h. EX (si installé):**
   - Copier skill `excal/` en écrasement (SKILL.md + references/)
   - Protéger la palette personnalisée (comparer avant écraser color-palette.md)
   - `uv sync` dans references/
   - NE PAS TOUCHER à `docs/diagrams/`

   **4i. DPL (si installé):**
   - Copier le skill `deploy/` en écrasement (SKILL.md)
   - Vérifier la connexion SSH et le token Cloudflare
   - NE PAS TOUCHER à `~/.claude/vps-config.json` ni `~/.claude/cloudflare.json`

   **4j. AR (si installé):**
   - Copier `skills/architecture/SKILL.md` en écrasement
   - Copier `commands/architecture.md` en écrasement
   - NE PAS TOUCHER à `docs/architecture.md` ni aux autres docs générés

   **4k. MP (si installé) :**
   - Copier `commands/marp-slides.md` en écrasement
   - Copier `skills/marp-presentations/` (récursif) en écrasement (SKILL.md + themes/standard/ + scripts/ + charte-graphique-template.md)
   - NE PAS TOUCHER aux decks générés sous `docs/presentations/` ni aux assets utilisateur dans `docs/slides/images/`
   - Si une charte personnalisée a été dérivée (`themes/custom/`) : la préserver

   **4l. FS (Frontend Slides — si installé) :**
   - Copier `commands/frontend-slides.md` en écrasement
   - Copier `skills/frontend-slides/` (récursif) en écrasement (SKILL.md, README-ORNI.md, STYLE_PRESETS.md, viewport-base.css, html-template.md, animation-patterns.md, LICENSE, scripts/)
   - NE PAS TOUCHER aux decks générés sous `docs/presentations/`
   - NE PAS TOUCHER au cache `.claude-design/` éventuel
   - NE PAS TOUCHER aux styles brandés custom dans `skills/frontend-slides/styles/{nom}/` du projet (uniquement écraser les styles upstream officiels)

   **4m. DS (Design System — si installé) :**
   - Copier `commands/design-system.md` en écrasement
   - Copier `skills/design-system/` (récursif) en écrasement (SKILL.md, README-ORNI.md, LICENSE, examples/template.html)
   - NE PAS TOUCHER aux artifacts existants dans `design/` (design-system.html, brand-book-a4.html, brand-book-a4.pdf)

   **4n. WPC (Web PDF Compile — si installé) :**
   - Copier `commands/web-pdf-compile.md` en écrasement
   - Copier `skills/web-pdf-compile/` (récursif) en écrasement (SKILL.md, README.md, PROTOCOLE.md, package.json, scripts/, examples/)
   - NE PAS TOUCHER au dossier `node_modules/` du skill (preserve les deps installees)
   - NE PAS TOUCHER aux dossiers de sortie `docs/dossiers/` ou `output/` du projet
   - Si `package.json` a change : suggerer `cd .claude/skills/web-pdf-compile && npm install`

   **4o. TO (Task Orchestrator — si installé) :**
   - Copier `commands/orchestrate.md` en écrasement
   - Copier `skills/task-orchestrator/SKILL.md` en écrasement
   - NE PAS TOUCHER au dir runtime `.orchestrate/` (state.json + kpis.yaml user)
   - NE PAS TOUCHER au dir `.worktrees/` (worktrees actifs éventuels)

5. **Mettre à jour le manifeste de versioning:**
   - Lire/créer `.claude/orni-manifest.json`
   - Pour chaque module mis à jour, extraire la version depuis le SKILL.md source
   - Mettre à jour `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Vérification:**
   - Exécuter la checklist de la section 5 du SKILL.md pour chaque module mis à jour

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Indiquer clairement quels modules ont été mis à jour et lesquels étaient absents
   - Rappeler les fichiers protégés (non modifiés)

---

## Modules disponibles standalone (hors pipeline /orni-update-full)

Les modules suivants ne sont **pas mis à jour** par `/orni-update-full` car installables uniquement standalone :

| Module | Commande update | Raison |
|--------|-----------------|--------|
| **GSD** | `/orni-update-gsd` (ou `npx get-shit-done-cc@latest --claude --global`) | Framework global installé par `npx`, pas un skill copié projet par projet. Update via le CLI officiel ou via `/gsd-update`. |
| **MB** | `/orni-update-mb` | Update profile shell PowerShell global, hors pipeline projet. |

Voir `/orni-help` pour les commandes update standalone correspondantes.
