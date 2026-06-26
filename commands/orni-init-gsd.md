---
description: 'Initialise GSD (Get Shit Done) dans le projet courant'
---

# /orni-init-gsd - Initialiser GSD framework

Bootstrap le framework **GSD** (Get Shit Done) dans le projet courant. GSD est déjà installé globalement (`~/.claude/skills/gsd-*` + `~/.claude/get-shit-done/`). Cette commande **ne réinstalle pas** — elle :

1. Vérifie l'install global GSD
2. Documente le choix du framework dans `CLAUDE.md`
3. Suggère le mode d'exécution (`--dangerously-skip-permissions`)
4. Initialise `.planning/` via `/gsd-new-project` (greenfield) ou `/gsd-map-codebase` + `/gsd-new-project` (brownfield)
5. Met à jour le manifeste `.claude/orni-manifest.json`

**Pour qui** : projets MVP exploratoire / requirements qui peuvent shift. Pour BMAD voir `/orni-init-bmad`. Pour Superpowers TDD, c'est un plugin global déjà actif (pas d'init projet).

## Instructions

1. **Lire les skills nécessaires :**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Charger `~/.claude/skills/gsd/SKILL.md` (si présent dans le projet, sinon copier depuis `{ORNI}`)

2. **Résoudre `{ORNI}`** :
   - Lire `~/.claude/orni-skills.json` pour `source_path`
   - Si absent → demander à l'utilisateur et créer le fichier

3. **Pré-vol — vérifier install global GSD :**

   ```bash
   # Test SDK CLI
   gsd-sdk --version 2>&1 | head -3
   # Doit retourner un numéro de version, sinon GSD pas installé

   # Test skills globaux
   ls ~/.claude/skills/ | grep -c '^gsd-'
   # Doit retourner ~60-67 selon profile installé

   # Test workflows dir
   ls -d ~/.claude/get-shit-done/ 2>/dev/null
   ```

   Si GSD non installé :
   - Proposer install : `npx get-shit-done-cc@latest --claude --global --profile=full`
   - Demander confirmation utilisateur avant exécution
   - Sinon abandonner avec message d'info

4. **Détecter contexte projet :**

   ```bash
   # Est-ce un greenfield ou brownfield ?
   git log --oneline 2>/dev/null | wc -l
   ls -la 2>/dev/null | grep -cE '\.(ts|tsx|js|jsx|py|go|rs|java)$'
   ```

   - 0 commits + 0 fichiers code → **greenfield** : route direct `/gsd-new-project`
   - >0 commits OU >5 fichiers code → **brownfield** : recommander `/gsd-map-codebase` d'abord
   - Demander confirmation à l'utilisateur si ambigu

5. **Vérifier si `.planning/` existe déjà :**

   ```bash
   ls -d .planning/ 2>/dev/null
   ```

   - Si existe : AVERTIR `.planning/` déjà présent, demander si remplacer ou skip étape `/gsd-new-project`
   - Si absent : continuer

6. **Ajouter section "Framework de dev" dans `CLAUDE.md` projet :**

   Lire `{PROJET}/CLAUDE.md` (créer si absent avec heading H1 = nom du projet).

   Ajouter section (avant la première section existante, après le bloc Project ID s'il existe) :

   ```markdown
   ## Framework de développement : GSD

   Ce projet utilise **GSD (Get Shit Done)** comme framework principal.
   Décisionnaire framework dans `~/.claude/skills/gsd/SKILL.md`.

   **Workflow type :**
   ```
   /gsd-new-project        # init
   /gsd-discuss-phase N    # capture décisions
   /gsd-plan-phase N       # plan adversarial
   /gsd-execute-phase N    # waves parallèles
   /gsd-verify-work N      # UAT manuel
   /gsd-ship N             # PR
   /gsd-complete-milestone # archive + tag
   ```

   **Lancer Claude Code** : `claude --dangerously-skip-permissions` (recommandé par GSD pour fluidité).

   **Artifacts GSD** : `.planning/` (peut être committé ou gitignored selon préférence).

   **Pas de mix avec BMAD ou Superpowers dans la même session** (saturation command space).
   ```

   Si la section existe déjà, ne pas la dupliquer.

7. **Décision `.planning/` : gitignored ou tracked ?**

   Demander à l'utilisateur :
   - **Tracked** (défaut GSD) : commit tous les artifacts planning. Avantage = historique décisions partagé équipe. Inconvénient = bruit dans diff + possible info sensible.
   - **Gitignored** : `.planning/` reste local. Plus propre git, mais perdu si dossier supprimé.

   Si gitignored choisi :
   ```bash
   echo '' >> .gitignore
   echo '# GSD planning artifacts' >> .gitignore
   echo '.planning/' >> .gitignore
   ```

8. **Lancer ou suggérer `/gsd-new-project` :**

   - Greenfield : suggérer à l'utilisateur de lancer maintenant `/gsd-new-project`
   - Brownfield : suggérer séquence `/gsd-map-codebase` puis `/gsd-new-project`
   - **Ne pas lancer automatiquement** — c'est un workflow long-form interactif qui nécessite l'attention utilisateur.

9. **Mettre à jour le manifeste de versioning :**

   Lire `.claude/orni-manifest.json` (créer si absent).
   Ajouter/mettre à jour l'entrée GSD :

   ```json
   {
     "modules": {
       "GSD": {
         "version": "<version retournée par gsd-sdk --version>",
         "installed_at": "<date ISO 8601 courante>",
         "updated_at": "<date ISO 8601 courante>",
         "source": "global (~/.claude/skills/gsd-*)",
         "profile": "full",
         "planning_dir": "tracked|gitignored",
         "framework_choice": "GSD"
       }
     }
   }
   ```

10. **Vérification finale :**
    - [ ] `gsd-sdk --version` retourne une version
    - [ ] `~/.claude/skills/gsd-*` contient >= 7 skills
    - [ ] `~/.claude/get-shit-done/` existe
    - [ ] `{PROJET}/CLAUDE.md` contient section "Framework de développement : GSD"
    - [ ] `.gitignore` mis à jour si choix gitignored
    - [ ] `.claude/orni-manifest.json` contient entrée GSD

11. **Rapport :**

    ```
    ## GSD - Initialisation projet terminée

    | Composant | Statut |
    |-----------|--------|
    | GSD global install | v{version} ({skills_count} skills) |
    | Type projet | {greenfield|brownfield} |
    | CLAUDE.md framework section | Ajoutée |
    | .planning/ policy | {tracked|gitignored} |
    | orni-manifest.json | Mis à jour entrée GSD |

    ### Prochaines étapes

    **{Greenfield}** :
    ```
    claude --dangerously-skip-permissions
    > /gsd-new-project
    ```

    **{Brownfield}** :
    ```
    claude --dangerously-skip-permissions
    > /gsd-map-codebase
    > /gsd-new-project
    ```

    ### Aide

    - `~/.claude/skills/gsd/SKILL.md` — décisionnaire framework + glossaire
    - `/gsd-help` — catalogue commandes GSD complet
    - `/gsd-surface --profile=core` — réduire bruit `/help` (7 skills boucle uniquement)
    ```

## Notes

- **Pas de copie de SKILL.md dans `.claude/skills/`** : le skill `gsd/` reste dans Orni-Skills source ; chaque projet lit via le path Orni si besoin. Évite duplication 200 lignes par projet.
- **GSD update** : `/gsd-update` ou re-run `npx get-shit-done-cc@latest --claude --global --profile=full`. Cette commande Orni ne gère pas l'update du framework upstream.
- **Désinstall** : `npx get-shit-done-cc@latest --uninstall`. Cette commande Orni ne désinstalle PAS — elle ne touche qu'au projet courant.
