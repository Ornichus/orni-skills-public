---
description: 'Initialise BMAD + Update/Followup + Agent Browser + ATeam + VPS/FAL/CF/Excal/Deploy (optionnels) dans le projet courant'
---

# /orni-init-full - Initialisation complète Orni-Skills

Initialise tous les composants Orni-Skills dans le projet courant: BMAD, Update/Followup, Agent Browser, ATeam, Mailbox et VPS/FAL/CF/EX/Deploy (optionnels).

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que `node` et `npx` sont disponibles (pour BMAD)
   - Pour chaque module, vérifier le fichier marqueur:
     - BMAD: `_bmad/core/`
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
     - PSS: `.claude/skills/project-status-snapshot/SKILL.md`
     - MP: `.claude/skills/marp-presentations/SKILL.md`
     - FS: `.claude/skills/frontend-slides/SKILL.md`
     - DS: `.claude/skills/design-system/SKILL.md`
     - WPC: `.claude/skills/web-pdf-compile/SKILL.md`
   - Si un ou plusieurs modules sont déjà installés : LISTER lesquels et demander confirmation
   - **Demander si le module VPS est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module VPS Management (accès SSH + MCP Hostinger) ?"
   - **Demander si le module FAL Image Gen est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module FAL Image Gen (génération d'images via fal.ai) ?"
   - **Demander si le module Cloudflare est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module Cloudflare Management (gestion DNS via API Cloudflare) ?"
   - **Demander si le module Excalidraw Diagram est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module Excalidraw Diagram (génération de diagrammes visuels) ?"
   - **Demander si le module Deploy est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module Deploy (déploiement automatisé VPS + Cloudflare) ? Requiert VPS et CF installés."
   - **Demander si le module Frontend Slides est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module Frontend Slides (decks HTML one-shot premium, brand mockups) ? Complémentaire de Marp Presentations (`/marp-slides`)."
   - **Demander si le module Design System est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module Design System (extract brand depuis URL/screenshot -> design-system.html scrollable + brand-book-a4.pdf print-ready) ? Complémentaire de Frontend Slides (workflow méthode RoboNuggets complète)."
   - **Demander si le module Web PDF Compile est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module Web PDF Compile (capture articles web -> PDF dossier groupe par pays/categorie, pour revue de presse / dossier d'enquete / bibliographie) ? Requiert Node.js 18+ et Chrome systeme. ~150MB de deps a installer (puppeteer-core, sharp, etc)."
   - **Demander si le module Task Orchestrator est souhaité** (optionnel, pas installé par défaut) :
     - "Souhaitez-vous inclure le module Task Orchestrator (méta-orchestrateur sur GSD/BMAD/Superpowers : inventory tâches + DAG waves parallèles/séquentielles + routing framework + KPIs typés + génération `/goal <4k chars` autonome) ?"

4. **Demander les préférences BMAD à l'utilisateur:**

   **Modules BMAD:**
   | Module | Description |
   |--------|-------------|
   | `bmm` | BMAD Method - Workflows de développement (PRD, stories, sprints) |
   | `bmb` | BMAD Module Builder - Créer/éditer agents et modules |
   | `cis` | Creative & Innovation Skills - Brainstorming, design thinking |
   | `tea` | Test Architecture Enterprise - Tests, Playwright |

   Suggestion par défaut: tous les modules.

   **Si TEA sélectionné - config browser:**
   | Mode | Description |
   |------|-------------|
   | `auto` | TEA choisit CLI ou MCP selon disponibilité (recommandé) |
   | `cli` | Playwright CLI uniquement |
   | `mcp` | Playwright MCP Server uniquement |
   | `none` | Pas d'interaction browser |

5. **Installer dans l'ordre:** BMAD -> UF -> AB -> AT -> ML -> extras -> VPS/FAL (optionnels)

   **5a. Module BMAD (via CLI officiel):**
   ```bash
   npx bmad-method install --directory "." --modules <choix> --yes
   ```
   Créer `_bmad-output/` si absent.
   Si npx échoue: fallback copie locale depuis `{ORNI}` (voir SKILL.md).

   **5b. Module UF (Update/Followup):**
   - Copier les 3 commandes + skill project-state-management/
   - Créer project-state.xml depuis template
   - Configurer CLAUDE.md avec le Project ID (depuis project-state.xml)
   - Créer la structure _backup/

   **5c. Module AB (Agent Browser):**
   - Copier commande + skill + documentation
   - **Vérifier si le CLI est déjà configuré** : exécuter `agent-browser --version 2>/dev/null`
     - Si OK : noter "AB CLI déjà configuré (vX.Y.Z)" — NE PAS proposer `/setup-agent-browser` dans les prochaines étapes
     - Si échec : noter "AB CLI non configuré" — proposer `/setup-agent-browser` dans les prochaines étapes

   **5c.5. Module AT (ATeam):**
   - Copier commande ateam.md + skill ateam/
   - Vérifier que AB est installé (requis pour profil test)

   **5c.6. Module ML (Mailbox):**
   - Copier commandes : `mail-send.md`, `mail-read.md`
   - Copier skill `mailbox/` (SKILL.md, README.md)
   - Résoudre le slug projet et créer la mailbox : `mkdir -p ~/.claude/mailbox/{slug}/inbox` + `archive/`

   **5d. Extras (settings + meta-commandes orni):**
   - Copier settings-template.json
   - Copier toutes les meta-commandes `{ORNI}/commands/orni-*.md` vers `.claude/commands/` (orni-help, orni-checkup, orni-init-*, orni-update-*)

   **5e. Module VPS (si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-vps` :
     - Vérifier les prérequis globaux (vps-config.json, clé SSH, MCP hostinger-api)
     - Copier le skill `vps/` (SKILL.md)
     - Tester la connexion SSH

   **5f. Module FAL (si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-fal` :
     - Vérifier Node.js et le dossier MCP source
     - `npm install` + `npm run build` si nécessaire
     - Configurer le MCP dans `~/.claude/settings.json`
     - Demander `FAL_KEY`
     - Copier `SKILL.md` dans `.claude/skills/fal-image-gen/`

   **5g. Module CF (si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-cf` :
     - Vérifier/créer `~/.claude/cloudflare.json` (api_token, account_id, default_zone)
     - Tester la connexion API
     - Copier `SKILL.md` dans `.claude/skills/cloudflare/`

   **5h. Module EX (si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-excal` :
     - Vérifier `uv` disponible
     - Copier skill + references dans `.claude/skills/excal-diagram/`
     - `uv sync` + `playwright install chromium`
     - Créer `docs/diagrams/`

   **5i. Module DPL (si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-deploy` :
     - Vérifier que VPS et CF sont installés (prérequis bloquants)
     - Vérifier `~/.claude/vps-config.json` et `~/.claude/cloudflare.json`
     - Tester la connexion SSH et le token Cloudflare
     - Copier `SKILL.md` dans `.claude/skills/deploy/`
     - Afficher les domaines Cloudflare disponibles

   **5j. Module AR (Architecture Relationnelle — installé par défaut) :**
   - Copier `skills/architecture/SKILL.md` dans `.claude/skills/architecture/`
   - Copier `commands/architecture.md` dans `.claude/commands/`

   **5k. Module PSS (Project Status Snapshot — installe par defaut) :**
   - Copier `skills/project-status-snapshot/SKILL.md` dans `.claude/skills/project-status-snapshot/`
   - Copier `commands/orni-status.md` dans `.claude/commands/orni-status.md`
   - Si `project-status.json` n'existe PAS a la racine : copier le template depuis `skills/project-status-snapshot/template/project-status-template.json` et remplacer `PROJECT_SLUG` par le slug du projet
   - Si `project-status.json` existe deja : ne pas ecraser

   **5l. Module MP (Marp Presentations — installé par défaut) :**
   - Suivre les instructions du Module MP dans `~/.claude/skills/orni-installer/SKILL.md`
   - Copier `commands/marp-slides.md` dans `.claude/commands/marp-slides.md`
   - Copier `skills/marp-presentations/` (récursif) dans `.claude/skills/marp-presentations/` (inclut `themes/standard/`, `scripts/`, `charte-graphique-template.md`)
   - Vérifier que `marp` CLI est disponible (`marp --version`) — sinon informer des options d'install (scoop/npm/npx)
   - Vérifier que Playwright Python est disponible — sinon informer `pip install playwright && playwright install chromium`
   - Source de vérité visuelle : `themes/standard/charte-graphique.md` (deck showcase)

   **5m. Module FS (Frontend Slides — si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-fs` :
     - Copier `commands/frontend-slides.md` dans `.claude/commands/frontend-slides.md`
     - Copier `skills/frontend-slides/` (récursif) dans `.claude/skills/frontend-slides/` (inclut SKILL.md, README-ORNI.md, STYLE_PRESETS.md, viewport-base.css, html-template.md, animation-patterns.md, LICENSE, scripts/)
     - Créer `docs/presentations/` si absent
     - Vérifier `python-pptx` (optionnel pour PPT conversion) et Node.js (optionnel pour Vercel deploy + Playwright PDF)
   - **Coexiste avec MP** : `/marp-slides` pour decks reproductibles versionnes, `/frontend-slides` pour pitch one-shot ultra-stylisés (cf. `README-ORNI.md`)

   **5n. Module DS (Design System — si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-ds` :
     - Copier `commands/design-system.md` dans `.claude/commands/design-system.md`
     - Copier `skills/design-system/` (récursif) dans `.claude/skills/design-system/` (inclut SKILL.md, README-ORNI.md, LICENSE, examples/template.html)
     - Créer `design/` si absent
     - Vérifier presence Edge/Chrome/Chromium (rendering PDF obligatoire)
   - **Complémentaire de FS** : `/design-system` produit artifacts publics (HTML scrollable + PDF A4) pour clients/partenaires, `/frontend-slides --new-style` consume la palette extraite pour modules deck internes (cf. `README-ORNI.md` workflow RoboNuggets complet)

   **5o. Module WPC (Web PDF Compile — si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-wpc` :
     - Copier `commands/web-pdf-compile.md` dans `.claude/commands/web-pdf-compile.md`
     - Copier `skills/web-pdf-compile/` (récursif) dans `.claude/skills/web-pdf-compile/` (inclut SKILL.md, README.md, PROTOCOLE.md, package.json, scripts/, examples/)
     - Créer `docs/dossiers/` si absent
     - Vérifier Node.js 18+ et Chrome systeme
     - Suggerer `cd .claude/skills/web-pdf-compile && npm install` (~150MB)

   **5p. Module TO (Task Orchestrator — si l'utilisateur a accepté) :**
   - Suivre les instructions de `/orni-init-to` :
     - Copier `commands/orchestrate.md` dans `.claude/commands/orchestrate.md`
     - Copier `skills/task-orchestrator/SKILL.md` dans `.claude/skills/task-orchestrator/`
     - Créer `.orchestrate/` (runtime state.json + kpis.yaml)
     - Ajouter `.orchestrate/` + `.worktrees/` à `.gitignore` si absents
   - **Pré-requis** : UF installé + project-state.xml présent

6. **Mettre à jour le manifeste de versioning:**
   - Créer/mettre à jour `.claude/orni-manifest.json` avec une entrée pour chaque module installé
   - Pour chaque module, extraire la version depuis le SKILL.md source (pattern `**Version**: X.Y.Z`)
   - Enregistrer `installed_at` et `updated_at` avec la date ISO 8601 courante

7. **Vérification globale:**
   - Exécuter la checklist de la section 5 du SKILL.md

7. **Rapport:**
   - Résumer tous les modules installés avec les options choisies
   - Mentionner le Project ID configuré (project-state.xml)
   - Rappeler les prochaines étapes:
     - `/setup-agent-browser` pour configurer WSL **SEULEMENT si le CLI n'est pas déjà configuré** (vérifié à l'étape 5c)
     - `/ateam suggest` pour composer une première équipe
     - `/update` pour la première synchronisation de l'état projet
     - `/bmad-help` pour découvrir les commandes BMAD

---

## Modules disponibles standalone (hors pipeline /orni-init-full)

Les modules suivants sont installables **uniquement** via leur commande dédiée — pas inclus dans `/orni-init-full` par choix design (pas un oversight) :

| Module | Commande | Raison standalone |
|--------|----------|-------------------|
| **GSD** (Get Shit Done) | `/orni-init-gsd` | Framework spec-driven mutuellement exclusif avec BMAD (règle "1 framework par session"). Choix conscient par projet : MVP exploratoire (GSD) vs specs locked-in (BMAD) vs TDD critique (Superpowers). |
| **MB** (Multi-Backend) | `/orni-init-mb` | Helper PowerShell global (profile shell `cdsp`/`odsp` pour Anthropic native / OpenRouter routing). Setup machine, pas projet. |

Voir `/orni-help` pour la documentation complète de chaque module standalone.
