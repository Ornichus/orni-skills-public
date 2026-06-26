---
description: 'BMAD Council - deliberation collaborative avec les vrais agents BMAD'
---

# /ateam-council - BMAD Council

Invoque un council de vrais agents BMAD pour deliberer, reviewer ou debattre avant l'implementation.

**Pipeline complet:** `/ateam-council` (deliberation) -> Plan Mode (planification) -> `/ateam go` (implementation)

## Syntaxe

```
/ateam-council [mode] [sujet/fichier] [options]
```

**Modes:**
- `suggest` - Suggere une composition (defaut si pas de mode explicite)
- `go` - Lance directement le council avec les agents selectionnes
- `review <fichier>` - Revue d'un document/artefact
- `debate <question>` - Debat structure sur une question
- `advisory <question>` - Consultation experte sur une decision
- `round-table <sujet>` - Table ronde libre (defaut si mode omis avec sujet)

**Options:**
- `--agents <liste>` - Forcer des agents specifiques (noms CSV: architect,pm,analyst)
- `--rounds <n>` - Nombre de tours (defaut: 2, max: 5)
- `--size <n>` - Taille du council (defaut: 3, max: 7)
- `--supervisor` - Activer la couche superviseur (auto si size >= 5)
- `--scenario <nom>` - Charger un scenario pre-configure
- `--output <fichier>` - Sauvegarder le rapport final
- `--plan` - Enchainer vers Plan Mode apres le council
- `--tasks` - Charger les taches de project-state.xml comme contexte

## Instructions d'execution

Tu es le **lead agent** du BMAD Council. Suis ces phases dans l'ordre strict.

---

### Phase 1: Parsing

1. **Parser les arguments** de l'utilisateur apres `/ateam-council`:
   - Identifier le mode: `suggest`, `go`, `review`, `debate`, `advisory`, `round-table`
   - Si aucun mode explicite: `suggest` si pas de sujet, `round-table` si sujet present
   - Identifier le sujet ou fichier cible
   - Identifier les options: `--agents`, `--rounds`, `--size`, `--supervisor`, `--scenario`, `--output`, `--plan`, `--tasks`

2. **Lire le contexte projet:**
   - Lire `CLAUDE.md` du projet courant -> extraire le Project ID si present
   - Lire `project-state.xml` si present -> objectif courant, phase, taches
   - Si `--tasks` ou des taches presentes dans `project-state.xml`:
     - Charger depuis la section `<tasks>` de `project-state.xml` les taches avec status `doing` puis `todo`

3. **Lire le roster BMAD:**
   - Lire `_bmad/_config/agent-manifest.csv` depuis le projet courant
   - Si absent: lire depuis le repo Orni-skills (`~/.claude/skills/` ou path connu)
   - Parser les 21+ agents: name, displayName, title, icon, role, identity, module, path

4. **Si `--scenario` specifie:**
   - Lire `~/.claude/skills/ateam/council-scenarios.md`
   - Trouver le scenario par nom
   - Appliquer: agents, mode, rounds, description (les options CLI overrident le scenario)

5. **Si mode = review:**
   - Lire le fichier cible integralement
   - Le stocker pour injection dans le contexte des agents

6. **Detecter la phase BMAD** (pour la selection automatique):
   - Analyser les keywords dans le sujet
   - Verifier les artefacts existants (PRD, architecture, stories...)
   - Mapper vers la matrice de selection (COUNCIL.md Section 7)

---

### Phase 2: Selection des agents

1. **Si `--agents` specifie:**
   - Lookup direct des noms dans le CSV
   - Valider que chaque agent existe
   - Avertir si un agent est dans la liste d'exclusion (bmad-master, quick-flow-solo-dev, presentation-master)

2. **Sinon: selection automatique:**
   - Lire `~/.claude/skills/ateam/COUNCIL.md` Section 7 (Matrice de selection)
   - Appliquer l'algorithme de scoring:
     - Keyword match dans role (x3), identity (x2), principles (x1)
     - Bonus phase: Primaire (+10), Secondaire (+5)
     - Module alignment (x2)
   - Appliquer contraintes de diversite (max 2/module, min 1 exterieur)
   - Selectionner les top N (N = `--size`, defaut 3)

3. **Gestion des superviseurs:**
   - Si `--supervisor` explicite OU `--size >= 5`:
     - Grouper les agents par domaine
     - Identifier le plus senior de chaque groupe (>= 2 agents)
     - Marquer comme superviseur
   - Sinon: pas de superviseurs

---

### Phase 3: Suggestion (si mode = suggest)

Afficher la composition proposee et attendre validation:

```
## BMAD Council - Composition proposee

**Sujet:** {topic}
**Mode:** {mode d'interaction} | **Tours:** {rounds} | **Taille:** {size}
**Phase BMAD detectee:** {phase}

### Membres proposes

| # | Agent | Titre | Module | Justification |
|---|-------|-------|--------|---------------|
| 1 | {icon} {displayName} ({name}) | {title} | {module} | {raison de selection} |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |

### Superviseurs (si applicable)

| Domaine | Superviseur | Agents supervises |
|---------|-------------|-------------------|
| {domaine} | {icon} {name} | {agents} |

### Contexte charge
- **Objectif courant:** {objectif depuis project-state.xml}
- **Taches:** {N} doing, {M} todo
- **Fichier review:** {fichier si mode review}

---

Repondre:
- **"go"** pour lancer avec cette composition
- **"go --agents architect,dev,tea"** pour modifier les agents
- **"go --rounds 3"** pour changer les tours
- Ou tout autre ajustement
```

Attendre la validation de l'utilisateur avant de continuer.

---

### Phase 4: Formation du Council

1. **Creer l'equipe:**
   ```
   TeamCreate(
     team_name="council-{slug}",
     description="BMAD Council ({mode}): {topic}"
   )
   ```
   - Slug genere depuis le sujet (lowercase, tirets, max 30 chars)

2. **Creer les taches par tour:**

   Pour chaque tour prevu:
   ```
   TaskCreate(
     subject="Tour {N}: {description_tour}",
     description="Tour {N} du council. Mode: {mode}. Sujet: {topic}.",
     activeForm="Council Tour {N} en cours"
   )
   ```

   Si tours > 1: le Tour 2+ est bloque par le tour precedent:
   ```
   TaskUpdate(taskId="{tour_N}", addBlockedBy=["{tour_N-1}"])
   ```

3. **Si superviseurs:** Creer des taches de synthese superviseur entre les tours d'agents:
   ```
   TaskCreate(
     subject="Synthese superviseur {name} - Tour {N}",
     description="Synthetiser les reponses du sous-groupe et envoyer au lead",
     activeForm="{name} synthetise son sous-groupe"
   )
   ```

---

### Phase 5: Spawn des agents (vrais agents BMAD)

**IMPORTANT:** Avant de spawner, lire `~/.claude/skills/ateam/COUNCIL.md` pour le template de spawn (Section 2) et les instructions de mode (Section 3).

Pour chaque agent selectionne:

1. **Lire le CSV** pour obtenir le `path` de l'agent

2. **Lire le fichier agent .md officiel** depuis `{project-root}/{path}`
   - Si le fichier est introuvable: utiliser le fallback CSV (COUNCIL.md Section 1)

3. **Extraire du fichier .md:**
   - Le bloc `<persona>...</persona>` verbatim (copier tel quel entre les balises)
   - Les attributs du tag `<agent name="..." title="..." icon="...">`
   - Les `<item>` du bloc `<menu>` (convertir en liste de capacites: `- {texte de l'item}`)

4. **Assembler le prompt:**
   - Prendre le template de spawn (COUNCIL.md Section 2)
   - Injecter la `{PERSONA_XML_VERBATIM}` extraite
   - Injecter les `{MENU_ITEMS_AS_LIST}` extraits
   - Injecter les `{MODE_INSTRUCTIONS}` selon le mode (COUNCIL.md Section 3)
   - Remplir toutes les autres variables: `{COUNCIL_NAME}`, `{TOPIC}`, `{TOTAL_ROUNDS}`, etc.

5. **Si l'agent est superviseur:** Ajouter le prompt superviseur (COUNCIL.md Section 8)

6. **Construire le contexte projet:**
   ```
   ## CONTEXTE PROJET
   **Objectif courant:** {objectif depuis project-state.xml}
   **Stack:** {stack detecte}
   **Phase BMAD:** {phase detectee}
   {Si mode review: "## DOCUMENT A REVIEWER\n{contenu du fichier}"}
   {Si taches presentes: "## TACHES EN COURS\n{liste des taches}"}
   ```

7. **Spawner:**
   ```
   Task(
     subagent_type="general-purpose",
     team_name="council-{slug}",
     name="{csv-name}-{csv-displayName}",
     prompt="{prompt assemble complet}"
   )
   ```

**Ordre de spawn:** Spawner tous les agents en parallele (pas de dependance entre eux au spawn).

---

### Phase 6: Orchestration des tours

Le lead orchestre chaque tour selon ce protocole:

```
pour tour in 1..total_rounds:

  # 1. Construire le contexte du tour
  si tour == 1:
    contexte_tour = sujet + document (si review) + taches (si --tasks)
  sinon:
    contexte_tour = synthese_tour_precedent + question_tour

  # 2. Creer et assigner sous-taches par agent
  pour agent in council_members:
    tache = TaskCreate(
      subject="Tour {tour}: {agent.displayName} repond",
      description="{contexte_tour}",
      activeForm="{agent.icon} {agent.displayName} formule sa reponse"
    )
    TaskUpdate(taskId=tache.id, owner="{agent.spawn_name}")
    # Notifier l'agent de sa tache
    SendMessage(
      type="message",
      recipient="{agent.spawn_name}",
      content="Tour {tour} - Voici ta tache: {contexte_tour}. Reponds selon le mode {mode}.",
      summary="Tour {tour} assigne"
    )

  # 3. Attendre toutes les reponses
  # - Monitor via TaskList (toutes les sous-taches du tour completed?)
  # - Recevoir les reponses via SendMessage automatique
  # - Si superviseurs: attendre les syntheses superviseur (pas les reponses brutes)

  # 4. Collecter les reponses
  reponses = {} # agent -> reponse

  # 5. Synthetiser le tour (template COUNCIL.md Section 5)
  synthese = generer_synthese(tour, reponses)

  # 6. Afficher la synthese a l'utilisateur
  afficher(synthese)

  # 7. Detection de consensus anticipe
  si consensus_fort(reponses) ET tours_restants > 0:
    afficher("Consensus fort detecte. Terminer plus tot? (oui/non)")
    si utilisateur_confirme("oui"):
      break
```

**Regles d'orchestration:**
- Seules les syntheses passent au tour suivant (pas les transcripts bruts)
- Le lead ne modifie PAS les reponses des agents
- Si un agent ne repond pas dans un delai raisonnable: relancer une fois, puis noter "Pas de reponse"
- Le lead peut intervenir entre les tours si l'utilisateur le demande

---

### Phase 7: Cloture OBLIGATOIRE

1. **Generer le rapport final:**
   - Utiliser le template de rapport (COUNCIL.md Section 6)
   - Compiler: consensus, divergences, recommandations, perspectives, prochaines etapes
   - Afficher le rapport complet a l'utilisateur

2. **Shutdown de tous les agents:**
   ```
   pour agent in council_members:
     SendMessage(type="shutdown_request", recipient="{agent.spawn_name}", content="Council termine, merci")
   ```
   - Attendre la confirmation de shutdown de chaque agent

3. **Nettoyage:**
   ```
   TeamDelete()
   ```

4. **Si `--output` specifie:**
   - Ecrire le rapport final dans le fichier indique
   - Confirmer: "Rapport sauvegarde dans {fichier}"

5. **Executer /update:**
   - C'est la DERNIERE action OBLIGATOIRE avant de rendre la main
   - Synchronise project-state.xml
   - NE PAS demander a l'utilisateur, l'executer directement
   ```
   /update
   ```

6. **Si `--plan` specifie:**
   - Injecter le rapport comme contexte
   - Activer Plan Mode:
     ```
     EnterPlanMode()
     ```
   - Le plan sera base sur les recommandations du council

7. **STOP** - Attendre l'input utilisateur.
