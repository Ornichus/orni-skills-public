---
description: 'Team Builder intelligent - compose et lance une equipe d agents'
---

# /ateam - Team Builder Intelligent

Compose une equipe d'agents optimale selon le contexte et les roles demandes, puis orchestre leur travail.

## Syntaxe

```
/ateam [mode] [roles...] [options]
```

**Modes:**
- `suggest` - Suggere une composition, attend validation (defaut si aucun role)
- `go` - Compose et lance directement

**Roles (combinables):**
- `test` - Testeur browser avec agent-browser + screenshots
- `test-front` - Alias de test (nom explicite pour equipes mixtes)
- `test-back` - Testeur backend/API (curl, validation schemas)
- `dev` - Developpeur general
- `dev-front` - Developpeur frontend
- `dev-back` - Developpeur backend
- `research` - Agent de recherche (codebase, web, docs)
- `research-council` - Recherche approfondie + debat BMAD Council sur les resultats

**Options:**
- `--url <url>` - URL cible pour tests browser
- `--scope <s>` - Perimetre: frontend / backend / integration / all
- `--iterate` - Active le mode iterate-test-fix
- `--name <nom>` - Nom de l'equipe (defaut: auto-genere)
- `--tasks` - Charger les taches depuis project-state.xml
- `--links <url...>` - URLs a explorer (pour research et research-council)
- `--council-mode <m>` - Mode du council: debate (defaut) / advisory / round-table / review
- `--council-agents <a...>` - Agents BMAD pour le council (defaut: auto-selection)

## Instructions d'execution

Tu es le **lead agent** de l'equipe. Suis ces etapes dans l'ordre.

---

### Phase 1: Parsing des parametres

1. **Parser les arguments** de l'utilisateur apres `/ateam`:
   - Identifier le mode: `suggest` ou `go` (defaut: `suggest` si aucun role specifie, `go` si roles presents)
   - Identifier les roles: `test`, `dev`, `dev-front`, `dev-back`, `test-front`, `test-back`, `research`, `research-council`
   - Identifier les options: `--url`, `--scope`, `--iterate`, `--name`, `--tasks`, `--links`, `--council-mode`, `--council-agents`
   - Si role = `research-council`: c'est un mode composite qui declenche Phase 4bis au lieu des Phases 4+5
   - **Extraction automatique des URLs:** Scanner tout le texte utilisateur pour detecter les URLs (pattern `https?://...`). Si des URLs sont trouvees et que `--links` n'est pas specifie, les utiliser automatiquement comme `--links`. Le reste du texte (hors URLs et options) = le sujet/contexte de la demande.

2. **Lire le contexte projet:**
   - Lire `CLAUDE.md` du projet courant -> extraire le Project ID si present
   - Lire `project-state.xml` si present -> objectif courant, taches
   - Lire `package.json` si present -> detecter le stack technique

3. **Si role `test` ou `test-front` est demande et `--url` absent:**
   - Detecter le port depuis `package.json` (scripts.dev) ou config Vite/Next
   - Detecter l'IP LAN:
     ```bash
     ipconfig | findstr "192.168"
     ```
   - Construire l'URL: `http://{IP}:{PORT}`
   - Informer l'utilisateur de l'URL detectee

4. **Si `--tasks` ou des taches presentes dans `project-state.xml`:**
   - Charger les taches depuis la section `<tasks>` de `project-state.xml`:
     - les taches avec status `todo`
     - les taches avec status `doing`

5. **Detecter le stack technique** (pour adapter les profils dev):
   - `package.json` -> dependencies: react, vue, next, express, fastapi...
   - Config files: `vite.config.*`, `next.config.*`, `tsconfig.json`, etc.
   - Backend: `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`

---

### Phase 2: Suggestion (si mode = suggest)

Si le mode est `suggest` (pas de roles specifies ou mode explicite):

1. **Analyser** le contexte et proposer une composition:
   - Quels roles sont pertinents vu le stack et les taches ?
   - Combien d'agents par role ?
   - Justification

2. **Afficher** la suggestion:

```
## ATEAM - Composition suggeree

**Contexte:** {projet} - {objectif courant}
**Stack:** {stack detecte}
**Taches:** {N} todo, {N} doing

### Equipe recommandee
| Role | Agent | Justification |
|------|-------|---------------|
| Lead (toi) | Coordination + dev | ... |
| Tester | tester-1 (browser) | ... |
| Dev | dev-1 | ... |

### Options detectees
- URL: {url detectee ou --url}
- Scope: {scope}

Confirmer? Repondre "go" pour lancer, ou modifier les roles.
```

3. **Attendre** la validation de l'utilisateur avant de continuer.

---

### Phase 3: Creation de l'equipe et des taches

1. **Creer l'equipe:**
   ```
   TeamCreate(
     team_name="{nom}",
     description="Equipe {roles} pour {objectif}"
   )
   ```
   - Nom auto si `--name` absent: `{projet}-{roles}` (ex: `myapp-dev-test`)

2. **Creer les taches:**
   - Si des taches existent dans project-state.xml: les reprendre comme taches de la team
   - Sinon, creer des taches basees sur le contexte:
     - Taches de dev (pour agents dev)
     - Taches de test (pour agents test)
     - Taches de recherche (pour agents research)

   ```
   TaskCreate(
     subject="...",
     description="...",
     activeForm="..."
   )
   ```

3. **Etablir les dependencies** si pertinent:
   - Les taches de test sont bloquees par les taches de dev correspondantes
   - Les taches de dev peuvent etre bloquees par les taches de recherche
   ```
   TaskUpdate(taskId="X", addBlockedBy=["Y"])
   ```

4. **Assigner les taches:**
   ```
   TaskUpdate(taskId="X", owner="{role}-{N}")
   ```

---

### Phase 4: Spawn des agents

Pour chaque role demande, lire le profil correspondant et spawner l'agent.

**IMPORTANT:** Avant de spawner, lire le fichier `~/.claude/skills/ateam/SKILL.md` pour obtenir les profils d'agents complets.

Pour chaque agent:

1. **Lire** la section du profil dans SKILL.md
2. **Construire** le prompt en remplacant les variables:
   - `{N}` -> numero de l'agent
   - `{TEAM}` -> nom de l'equipe
   - `{URL}` -> URL cible (--url ou detectee)
   - `{IP}` -> IP LAN detectee
   - `{SCOPE}` -> scope demande
3. **Spawner** l'agent:

```
Task(
  subagent_type="general-purpose",
  team_name="{nom-equipe}",
  name="{role}-{N}",
  prompt="<prompt construit avec profil + taches assignees>"
)
```

**Mapping role -> subagent_type:**

| Role | subagent_type | Notes |
|------|---------------|-------|
| test | general-purpose | Besoin de Bash pour wsl agent-browser |
| test-front | general-purpose | Alias de test |
| test-back | general-purpose | Besoin de Bash pour curl |
| dev | general-purpose | Besoin de tous les outils |
| dev-front | general-purpose | Besoin de tous les outils |
| dev-back | general-purpose | Besoin de tous les outils |
| research | general-purpose | Lecture seule dans le profil |
| research-council | general-purpose | Mode composite: voir Phase 4bis |

**Structure du prompt de spawn:**

```markdown
# Tu es {role}-{N} dans l'equipe {TEAM}

{Contenu du profil depuis SKILL.md}

## Contexte du projet
{Stack detecte, objectif courant}

## Tes taches assignees
{Liste des taches avec IDs}

## Communication
- Envoie tes rapports au lead via SendMessage(type="message", recipient="lead", ...)
- Consulte TaskList regulierement pour voir si de nouvelles taches sont disponibles
- Si tu es bloque, previens le lead immediatement
- Quand une tache est terminee: TaskUpdate(taskId="X", status="completed") puis previens le lead
```

---

### Phase 4bis: Research-Council Workflow

**Declenchement:** Cette phase remplace les Phases 4 et 5 quand le role est `research-council`.

Le lead orchestre un pipeline en 6 sous-phases: recherche -> synthese -> transition -> council -> deliberation -> rapport.

**IMPORTANT:** Avant de commencer, lire:
- `~/.claude/skills/ateam/SKILL.md` pour les profils research et research-council
- `~/.claude/skills/ateam/COUNCIL.md` pour les templates council (Sections 2, 3, 5, 6, 7)

#### Sous-phase R1: Spawn recherche

1. **Determiner le nombre d'agents recherche:**
   - Si liens fournis: 1 agent par groupe de 3-4 liens (max 5 agents)
   - Repartir les liens equilibrement entre agents
   - Sinon (pas de liens): 1-2 agents selon l'ampleur du sujet

2. **Creer l'equipe:**
   ```
   TeamCreate(
     team_name="rc-{slug}",
     description="Research-Council: {sujet}"
   )
   ```

3. **Pour chaque research agent:**
   - Lire le profil `research` dans SKILL.md
   - Construire le prompt en injectant:
     - Le sujet de recherche
     - Les liens assignes (si `--links`)
     - Le format de rapport research (depuis SKILL.md)
   - Spawner:
     ```
     Task(
       subagent_type="general-purpose",
       team_name="rc-{slug}",
       name="researcher-{N}",
       prompt="{prompt research construit}"
     )
     ```

4. **Creer les taches de recherche:**
   ```
   TaskCreate(
     subject="Recherche: {sous-sujet ou liens assignes}",
     description="Explorer {liens/sujet} et produire un rapport structure",
     activeForm="researcher-{N} explore les sources"
   )
   TaskUpdate(taskId="{id}", owner="researcher-{N}")
   ```

#### Sous-phase R2: Collecte et Research Brief

1. **Attendre** que tous les rapports de recherche arrivent (monitor via TaskList + SendMessage)
2. **Collecter** les rapports de chaque agent
3. **Compiler le Research Brief:**

```markdown
## Research Brief: {sujet}

### Sources explorees
{liste des sources avec resumes - compilees depuis les rapports}

### Constats principaux
{points cles, regroupes par theme}

### Points bloquants identifies
{problemes sans solution claire}

### Pistes de solution
{solutions evoquees dans les recherches}
```

4. **Afficher** le Research Brief a l'utilisateur pour visibilite

#### Sous-phase R3: Transition

1. **Shutdown des research agents:**
   ```
   pour agent in research_agents:
     SendMessage(type="shutdown_request", recipient="researcher-{N}", content="Recherche terminee, merci")
   ```
   - Attendre les confirmations

2. **Selectionner les agents BMAD Council:**
   - Si `--council-agents` specifie: utiliser ces agents
   - Sinon: auto-selection via la matrice Section 7 de COUNCIL.md (basee sur le sujet)
   - Appliquer l'algorithme de scoring standard

3. **Determiner le mode council:**
   - Si `--council-mode` specifie: utiliser ce mode
   - Sinon: `debate` par defaut

#### Sous-phase C1: Spawn Council

1. **Lire** COUNCIL.md Section 2 (template de spawn) et Section 3 (mode instructions)

2. **Pour chaque agent BMAD selectionne:**
   - Charger la persona (processus Section 1 de COUNCIL.md: CSV -> fichier .md -> extraction persona)
   - Assembler le prompt de spawn avec:
     - `{PERSONA_XML_VERBATIM}` depuis le fichier agent
     - `{MENU_ITEMS_AS_LIST}` depuis le fichier agent
     - `{MODE_INSTRUCTIONS}` selon le mode council
     - `{CONTEXT_BLOCK}` = le Research Brief compile en R2
     - `{TOPIC}` = le sujet original
     - `{COUNCIL_NAME}` = "rc-{slug}"
     - `{TOTAL_ROUNDS}` = 2 (defaut)

3. **Spawner les agents en parallele:**
   ```
   Task(
     subagent_type="general-purpose",
     team_name="rc-{slug}",
     name="{csv-name}-{csv-displayName}",
     prompt="{prompt council assemble}"
   )
   ```

#### Sous-phase C2: Deliberation

1. **Suivre le protocole des tours** (Section 4 de COUNCIL.md):
   - Tour 1: perspectives initiales sur le Research Brief
   - Tour 2: reponses croisees sur la synthese Tour 1
   - Syntheses inter-tours (Section 5 de COUNCIL.md)

2. **Nombre de tours:** 2 par defaut (pas configurable ici, cohérent avec le scenario)

3. **Detection consensus anticipe:** si accord fort au Tour 1, proposer de terminer

#### Sous-phase C3: Rapport final

Generer un rapport consolide combinant recherche et council:

```markdown
## Rapport Research-Council: {sujet}

### Phase Recherche
**Sources:** {N} sources explorees par {N} agents
{Research Brief resume}

### Phase Council
**Membres:** {liste agents BMAD avec icones}
**Mode:** {mode}
**Tours:** {N effectues}/{N prevus}

### Solutions identifiees
| # | Solution | Porteur | Priorite | Consensus |
|---|----------|---------|----------|-----------|
| 1 | ... | {agent} | Haute/Moyenne/Basse | Fort/Partiel/Divise |

### Points bloquants
| # | Blocage | Cause | Piste de resolution |
|---|---------|-------|---------------------|
| 1 | ... | ... | ... |

### Recommandations finales
1. {action concrete avec responsable suggere}
2. ...
```

Puis passer a la **Phase 6 (Cloture)** normalement.

---

### Phase 5: Coordination (workflow continu du lead)

En tant que lead, tu:

1. **Travailles** sur tes propres taches de dev (si applicable)
2. **Coordonnes** les agents:
   - Quand une feature est prete -> previens le testeur
   - Quand un test echoue -> corrige ou assigne la correction
   - Quand une recherche est terminee -> integre les resultats
3. **Si mode `--iterate`:**
   - Boucle: dev -> test -> fix -> re-test jusqu'a PASS
   - Le lead corrige les FAIL et re-notifie le testeur
4. **Quand toutes les taches sont terminees:**
   - Passe a la Phase 6 (cloture)

---

### Phase 6: Cloture OBLIGATOIRE

Quand tout le travail est termine:

1. **Shutdown** de tous les agents:
   ```
   SendMessage(type="shutdown_request", recipient="{agent}", content="Travail termine, merci")
   ```
   - Attendre la confirmation de shutdown de chaque agent

2. **Nettoyage:**
   ```
   TeamDelete()
   ```

3. **Rapport final:**
   ```
   ## Rapport ATEAM - {nom-equipe}

   **Duree:** {debut} -> {fin}
   **Equipe:** {liste des agents}

   ### Taches completees
   | # | Tache | Agent | Status |
   |---|-------|-------|--------|
   | 1 | ... | ... | DONE |

   ### Resultats des tests (si applicable)
   {Resume des rapports de test}

   ### Fichiers modifies
   {Liste des fichiers touches}
   ```

4. **Executer /update:**
   - C'est la DERNIERE action OBLIGATOIRE avant de rendre la main
   - Synchronise project-state.xml
   - NE PAS demander a l'utilisateur, l'executer directement

   ```
   /update
   ```

5. **STOP** - Attendre l'input utilisateur.
