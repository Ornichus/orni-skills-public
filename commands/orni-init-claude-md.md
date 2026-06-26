---
description: 'Bootstrap CLAUDE.md projet standardisé Orni (template DENSE-POINTEURS) — scaffold nouveau OU augmenter existant'
---

# /orni-init-claude-md — Bootstrap CLAUDE.md projet standardisé Orni

Génère ou augmente le `CLAUDE.md` du projet courant avec un template **DENSE-POINTEURS** qui oriente l'agent vers les bons outils + framework selon le contexte projet — avec un minimum de tokens et un maximum de pointeurs vers les sources canoniques.

**Référence** : redesign v2.0 DENSE (session 021).

## Principe de design

**Objectif** : CLAUDE.md le plus **dense** possible (tokens minimum) tout en restant **exhaustif** par pointeurs vers les sources canoniques.

- **Pas de duplication** : le contenu détaillé vit dans `{ORNI_PATH}/skills/*/SKILL.md` + `docs/GUIDE-UTILISATION.md`. Le CLAUDE.md pointe.
- **Décisionnaire inline** : tables compressées (1 ligne par item) pour Framework + Outil-par-besoin + Réflexes.
- **Pas de framework fixé** : l'utilisateur peut **varier** entre GSD / BMAD / Superpowers selon le contexte projet → le template liste les 4 cas + le pivot, et reste neutre.
- **Style/communication** : pointeur vers `~/.claude/CLAUDE.md` global. Pas de duplication des règles caveman/vulgarisation/etc.

**v2.0 vs v1.0 (ADAPTATIF)** : le précédent design (sections framework conditionnelles + 4 framework-blocks séparés) a été remplacé par un template unique dense avec décisionnaire inline. Plus simple, plus dense, support natif du mix multi-framework cross-session.

## Instructions

### 1. Résoudre le chemin source Orni

- Lire `~/.claude/orni-skills.json` pour obtenir `source_path` → `{ORNI}`
- Si absent : demander à l'utilisateur et créer le fichier

### 2. Détecter le mode d'opération

- **MODE SCAFFOLD** : `CLAUDE.md` projet **absent** ou taille < 200 octets (placeholder vide)
- **MODE AUGMENT** : `CLAUDE.md` projet **présent** et non-vide → préserver contenu, ajouter sections manquantes via marqueurs `<!-- ORNI-CLAUDE-MD-START:* -->`

### 3. Détecter les frameworks présents (info-only, pas branchement conditionnel)

Lister (à des fins de rapport et notes éventuelles) les frameworks présents :

| Marqueur | Framework |
|----------|-----------|
| `.planning/PROJECT.md` OU `.planning/config.json` | **GSD** |
| `_bmad/core/config.yaml` | **BMAD** |
| `plans/` répertoire avec `.md` + utilisation skills `superpowers:*` mentionnée dans CLAUDE.md existant | **Superpowers** |

**v2.0** : la détection sert **uniquement** à enrichir le rapport final + à pré-renseigner les notes "framework actif détecté dans ce projet" si pertinent. Le template DENSE liste les 4 cas de toute façon (décisionnaire neutre), donc pas de branchement conditionnel sur le contenu.

### 4. Récupérer le Project ID

- Chercher dans `CLAUDE.md` existant pattern `**Project ID:** \`xxx-xxx-xxx\``
- Si absent ou MODE SCAFFOLD : demander à l'utilisateur OU générer un identifiant (stocké dans `project-state.xml`)

### 5. Récupérer info projet

- Nom : depuis dossier courant (`basename "$(pwd)"`)
- Modules installés : lire `.claude/orni-manifest.json` (clé `modules` → liste {code, version, installed_at, updated_at})
- Si pas de manifeste : noter "Aucun module Orni détecté" + suggérer `/orni-init-full`

### 6. Demander tech stack (5 questions interactives — SCAFFOLD uniquement)

> En MODE AUGMENT, **ne pas demander** si la section Tech Stack existe déjà. Sinon, demander.

| Question | Exemples de réponse |
|----------|---------------------|
| Q1 : Langage(s) primaire(s) | Python, TypeScript, Go, Rust, PowerShell |
| Q2 : Framework(s) applicatif(s) | FastAPI, Next.js, React, Vue, none |
| Q3 : Base(s) de données | PostgreSQL, SQLite, ChromaDB, Redis, aucune |
| Q4 : Infrastructure / Déploiement | Docker VPS, Cloudflare Pages, Vercel, local only |
| Q5 : Tests | pytest, vitest, playwright, manuel uniquement |

### 7. Composer CLAUDE.md final

**MODE SCAFFOLD** :

1. Lire template `{ORNI}/templates/CLAUDE-project-template.md`
2. (v2.0) Pas de framework block à charger — décisionnaire inline dans le template.
3. Composer table modules format DENSE depuis `.claude/orni-manifest.json` (step 7.5 ci-dessous) :
   ```
   | Code | Module | Version |
   |------|--------|---------|
   | UF | Update/Followup | 1.0.0 |
   | ML | Mailbox | 1.0.0 |
   | ... | ... | ... |
   ```
4. Substituer les placeholders dans le template DENSE :
   - `{{PROJECT_NAME}}` → nom projet (depuis dossier courant)
   - `{{PROJECT_SLUG}}` → slug projet (lowercase, kebab-case)
   - `{{PROJECT_ID}}` → Project ID (depuis `project-state.xml`, ou `non configuré`)
   - `{{LAST_SYNC_DATE}}` → ISO 8601 maintenant
   - `{{ORNI_PATH}}` → `source_path` Orni-Skills résolu (e.g. `<VOTRE_DOSSIER>/orni-skills`)
   - `{{MODULES_TABLE_DENSE}}` → table modules format dense (voir step 7.5)
   - `{{LANGUAGES}}` / `{{APP_FRAMEWORKS}}` / `{{DATABASES}}` / `{{INFRA}}` / `{{TESTS}}` → réponses Q1-Q5 (séparés par ` · `)
   - `{{USER_NOTES_PRESERVED}}` → vide (placeholder utilisateur)
5. Écrire `CLAUDE.md`

**MODE AUGMENT** :

1. Backup : copier `CLAUDE.md` actuel vers `.claude/CLAUDE.md.backup-orni-{timestamp}.md`
2. Détecter sections présentes (chercher `## Framework`, `## Modules Orni`, `## Tech Stack`, etc.)
3. Pour chaque section MANQUANTE :
   - Si pas de marqueurs ORNI-CLAUDE-MD-START/END : ajouter section complète depuis template avec marqueurs
   - Si section existe SANS marqueurs : laisser intacte (respecter choix user), juste **ajouter** les marqueurs autour pour éviter écraser au prochain refresh
4. Si section Framework existe mais le framework détecté diffère : avertir et demander confirmation (override ou skip)
5. Réécrire `CLAUDE.md` avec ajouts seulement (préserver l'ordre des sections existantes + le contenu hors marqueurs)

### 8. Mettre à jour le manifeste

Ajouter/mettre à jour entrée `CLA` dans `.claude/orni-manifest.json` :
```json
{
  "modules": {
    "CLA": {
      "version": "1.0.0",
      "installed_at": "{ISO date now}",
      "updated_at": "{ISO date now}",
      "template": "ADAPTATIF",
      "framework_detected": "{GSD|BMAD|Superpowers|none}",
      "mode": "{SCAFFOLD|AUGMENT}"
    }
  }
}
```

### 9. Vérification finale

- [ ] `CLAUDE.md` existe et taille > 500 octets
- [ ] Section `## Framework de développement` présente avec contenu non-vide
- [ ] Section `## Modules Orni installés` présente avec table (ou "aucun module")
- [ ] Section `## Tech Stack` présente avec valeurs ou placeholders
- [ ] Mention `~/.claude/CLAUDE.md global` pour style/communication
- [ ] Manifeste CLA mis à jour
- [ ] Backup créé (si MODE AUGMENT)

### 10. Rapport

```
## /orni-init-claude-md terminé

**Mode** : {SCAFFOLD|AUGMENT}
**Framework détecté** : {FRAMEWORK}
**Project ID** : {ID ou "non configuré"}
**Modules listés** : {N} ({liste codes})

**Fichiers** :
- CLAUDE.md : {créé|augmenté} ({lignes})
{si AUGMENT:}
- Backup : .claude/CLAUDE.md.backup-orni-{ts}.md

**Sections ajoutées** :
- ## Framework (si manquante)
- ## Modules Orni (si manquante)
- ## Tech Stack (si manquante + Q1-Q5 répondues)
- ## Conventions projet (placeholder)
- ## Anti-patterns projet (placeholder)
- ## Style & Communication (pointeur global)
- ## Notes projet (vide ou préservé)

**Prochaines étapes** :
- Compléter sections placeholder (Conventions, Anti-patterns) avec valeurs projet
- Si framework changé : adapter workflow
- Régénérer modules : `/orni-init-claude-md --refresh-modules`
- Régénérer framework : `/orni-init-claude-md --refresh-framework`
```

## Arguments optionnels

| Arg | Effet |
|-----|-------|
| `--refresh-modules` | Régénère uniquement la section Modules depuis `orni-manifest.json`. Préserve le reste. |
| `--refresh-tooling` | Re-synchronise la table Outils-par-besoin avec la version du template source (utile si le template upstream a évolué). |
| `--force-scaffold` | Force MODE SCAFFOLD même si CLAUDE.md existe (backup obligatoire). |

> **v2.0 — supprimé** : `--framework=X` et `--refresh-framework` (le template DENSE liste les 4 frameworks dans une table inline, pas de branchement conditionnel — donc aucun framework à "choisir" à l'install).

## Notes

- Le template Orni cohabite avec **n'importe quel** framework — un CLAUDE.md projet **doit** exister pour orienter l'agent même sans framework spec-driven.
- Les marqueurs `<!-- ORNI-CLAUDE-MD-START:* -->` délimitent les sections gérées par cette commande (regen safe). Tout en dehors est préservé.
- Le global `~/.claude/CLAUDE.md` reste source de vérité pour style/vulgarisation/caveman policy/etc. Le projet override uniquement si nécessaire.
- Multi-framework cross-session : pour un projet où on utilise tantôt GSD tantôt Superpowers (e.g. MVP exploratoire puis refactor critique), le décisionnaire inline du template guide la décision **par session**. Pas besoin de regénérer le CLAUDE.md.
- Migration framework runtime (e.g. ajouter `.planning/` à un projet existant) : lancer `/orni-init-gsd` (installe framework) — le CLAUDE.md projet n'a pas besoin d'être modifié, son décisionnaire couvre déjà GSD.
