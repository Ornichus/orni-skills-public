---
description: 'Vérifie si les composants Orni installés sont à jour et propose les mises à jour'
---

# /orni-checkup - Vérification des mises à jour Orni-Skills

Scanne les composants Orni installés dans le projet courant, compare avec la source, et propose les mises à jour.

## Instructions

1. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

2. **Lire le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` dans le projet courant (s'il existe)
   - Ce fichier contient les versions installées et les dates d'init/update :
     ```json
     {
       "modules": {
         "ML": {
           "version": "1.0.0",
           "installed_at": "2026-02-21T12:00:00Z",
           "updated_at": "2026-02-21T15:30:00Z",
           "source": "skills/mailbox/SKILL.md"
         }
       }
     }
     ```
   - Si le manifeste n'existe pas : le signaler et se baser uniquement sur la détection de fichiers

3. **Scanner les modules installés:**

   Pour chaque module ci-dessous, vérifier si installé dans le **projet courant** ET/OU **globalement** (`~/.claude/`).

   ### Registre des modules

   | Module | Code | Fichier indicateur (projet) | Fichier indicateur (global) | Source version (dans `{ORNI}`) |
   |--------|------|----------------------------|----------------------------|-------------------------------|
   | Mailbox | ML | `.claude/commands/mail-send.md` | `~/.claude/commands/mail-send.md` | `skills/mailbox/SKILL.md` |
   | ATeam | AT | `.claude/commands/ateam.md` | `~/.claude/commands/ateam.md` | `skills/ateam/SKILL.md` |
   | ATeam Council | ATC | `.claude/commands/ateam-council.md` | `~/.claude/commands/ateam-council.md` | `skills/ateam/COUNCIL.md` |
   | Agent Browser | AB | `.claude/skills/agent-browser/SKILL.md` | `~/.claude/skills/agent-browser/SKILL.md` | `skills/agent-browser/SKILL.md` |
   | Update/Followup | UF | `.claude/commands/update.md` | `~/.claude/commands/update.md` | `commands/update.md` |
   | Followup | UF | `.claude/commands/followup.md` | `~/.claude/commands/followup.md` | `commands/followup.md` |
   | Followup Doctor | UF | `.claude/commands/followup-doctor.md` | `~/.claude/commands/followup-doctor.md` | `commands/followup-doctor.md` |
   | Structure | STR | `.claude/commands/structure.md` | `~/.claude/commands/structure.md` | `commands/structure.md` |
   | Project State Mgmt | PSM | `.claude/skills/project-state-management/SKILL.md` | `~/.claude/skills/project-state-management/SKILL.md` | `skills/project-state-management/SKILL.md` |
   | VPS Management | VPS | `.claude/skills/vps/SKILL.md` | `~/.claude/skills/vps/SKILL.md` | `skills/vps/SKILL.md` |
   | Fal Image Gen | FAL | `.claude/skills/fal-image-gen/SKILL.md` | config `fal-image-gen` dans `~/.claude/settings.json` | `skills/fal-image-gen/SKILL.md` |
   | Cloudflare | CF | `.claude/skills/cloudflare/SKILL.md` | `~/.claude/cloudflare.json` | `skills/cloudflare/SKILL.md` |
   | Excalidraw Diagram | EX | `.claude/skills/excal-diagram/SKILL.md` | `~/.claude/skills/excal-diagram/SKILL.md` | `skills/excal/SKILL.md` |
   | Deploy | DPL | `.claude/skills/deploy/SKILL.md` | `~/.claude/skills/deploy/SKILL.md` | `skills/deploy/SKILL.md` |
   | Architecture | AR | `.claude/skills/architecture/SKILL.md` | `~/.claude/skills/architecture/SKILL.md` | `skills/architecture/SKILL.md` |
   | Project Status Snapshot | PSS | `.claude/skills/project-status-snapshot/SKILL.md` | `~/.claude/skills/project-status-snapshot/SKILL.md` | `skills/project-status-snapshot/SKILL.md` |
   | Marp Presentations | MP | `.claude/skills/marp-presentations/SKILL.md` | `~/.claude/skills/marp-presentations/SKILL.md` | `skills/marp-presentations/SKILL.md` |
   | Frontend Slides | FS | `.claude/skills/frontend-slides/SKILL.md` | `~/.claude/skills/frontend-slides/SKILL.md` | `skills/frontend-slides/SKILL.md` |
   | Design System | DS | `.claude/skills/design-system/SKILL.md` | `~/.claude/skills/design-system/SKILL.md` | `skills/design-system/SKILL.md` |

4. **Pour chaque module trouvé (installé) :**
   - **Version du manifeste** : lire la version et les dates depuis `.claude/orni-manifest.json` (si présent)
   - **Version du fichier installé** : lire le fichier installé et chercher le pattern `**Version**: X.Y.Z` ou `**Version:** X.Y.Z` (première occurrence)
   - **Version source** : lire le fichier correspondant dans `{ORNI}` et chercher le même pattern
   - **Comparer** :
     - Si même version ET même contenu (comparer les fichiers) → `A jour`
     - Si même version MAIS contenu différent → `Modifié en source`
     - Si version différente → `Mise à jour disponible`
     - Si pas de version trouvée dans l'un ou l'autre → comparer uniquement le contenu des fichiers
   - **Détecter les modifications locales** : si le fichier installé diffère du source ET de la dernière version connue, noter `Modifié localement`

5. **Afficher le rapport :**

   ```
   ## Orni-Skills Checkup

   **Projet :** {nom du projet courant}
   **Source :** {ORNI}
   **Manifeste :** {trouvé / absent}

   ### Composants installés

   | Module | Code | Scope | Version | Source | Statut | Installé le | Mis à jour le |
   |--------|------|-------|---------|--------|--------|-------------|---------------|
   | Mailbox | ML | Projet | 1.0.0 | 1.0.0 | A jour | 2026-02-15 | 2026-02-21 |
   | VPS | VPS | Projet | 1.1.0 | 1.1.0 | A jour | 2026-02-21 | 2026-02-21 |
   | ATeam | AT | Global | 1.0.0 | 1.1.0 | MAJ dispo | 2026-02-10 | - |
   | Agent Browser | AB | - | - | 0.7.6 | Non installé | - | - |
   | ... | ... | ... | ... | ... | ... | ... | ... |

   ### Actions disponibles
   - {liste des updates disponibles avec la commande correspondante}
   ```

   Statuts possibles et leur signification :
   - `A jour` — Même version, même contenu
   - `MAJ dispo` — Version source plus récente
   - `Modifié en source` — Même version mais contenu modifié dans le repo
   - `Non installé` — Module disponible mais pas installé ici
   - `Modifié localement` — Le fichier installé a été modifié par rapport à la source
   - `Sans manifeste` — Module installé mais pas tracké dans orni-manifest.json (dates inconnues)

6. **Proposer les actions :**
   - Si des mises à jour sont disponibles ou des fichiers modifiés en source :
     - Lister chaque module concerné avec la commande `/orni-update-*` correspondante
     - Demander : "Voulez-vous mettre à jour ? (tous / sélection / aucun)"
   - Si "tous" : exécuter chaque `/orni-update-*` séquentiellement
   - Si "sélection" : demander lesquels, puis exécuter
   - Si aucune commande `/orni-update-*` n'existe pour un module, proposer une copie manuelle :
     - "Pas de commande update pour {module}. Copie directe depuis `{ORNI}/{source}` ?"

7. **Pour les modules sans `/orni-update-*` :**
   - Copier le(s) fichier(s) source vers la destination (projet ou global selon où il est installé)
   - Mettre à jour le manifeste `.claude/orni-manifest.json` avec la nouvelle version et date
   - Confirmer la copie

8. **Résumé final :**
   ```
   ## Résultat
   - {N} modules à jour
   - {N} modules mis à jour
   - {N} modules non installés (disponibles)
   - Manifeste : {créé / mis à jour / déjà à jour}
   ```
