# COUNCIL.md - BMAD Council Framework

Source de verite pour les templates et protocoles du BMAD Council.
Le lead lit ce fichier avant de spawner les agents du council.

---

## Section 1: Chargement des vrais agents BMAD

**Principe fondamental:** Chaque agent du council est incarné par son **vrai fichier agent .md officiel** de BMAD. On ne dilue PAS la persona dans un resume CSV.

### Processus du lead pour chaque agent selectionne

1. Lire le CSV `_bmad/_config/agent-manifest.csv` pour obtenir le `path` de l'agent (ex: `_bmad/bmm/agents/architect.md`)
2. Lire le fichier agent .md complet depuis `{project-root}/{path}`
3. **Extraire** le bloc `<persona>` verbatim (role, identity, communication_style, principles)
4. **Extraire** les attributs `<agent>` (name, title, icon)
5. **Extraire** les `<item>` du bloc `<menu>` comme reference de capacites (l'agent sait ce qu'il POURRAIT conseiller)
6. **Ignorer** le bloc `<activation>` (steps 1-8, menu-handlers, rules) - remplace par le wrapper council
7. Assembler le prompt de spawn avec le template ci-dessous

### Fallback: Agent absent du repo source

Si le fichier agent .md est introuvable (repo BMAD non clone dans le projet):
1. Utiliser les champs du CSV: role, identity, communicationStyle, principles
2. Construire un bloc `<persona>` synthetique depuis le CSV
3. Informer l'utilisateur: "Agent {name} charge depuis le CSV (fichier source non trouve: {path})"
4. Le council fonctionne quand meme, mais avec une persona moins riche

---

## Section 2: Template de spawn agent

```markdown
# BMAD Council - Agent Spawn

You must fully embody this agent's persona. NEVER break character.

## ACTIVATION COUNCIL (remplace l'activation BMAD standard)

Tu es invoque dans un **BMAD Council**, pas en mode interactif. Il n'y a PAS de menu,
PAS d'interaction directe avec l'utilisateur, PAS de config.yaml a charger.
Tu communiques UNIQUEMENT via SendMessage avec le lead ou ton superviseur.

---

## TA PERSONA BMAD OFFICIELLE

{PERSONA_XML_VERBATIM}

(Extrait tel quel du fichier agent officiel: {AGENT_PATH})

---

## TES CAPACITES DE REFERENCE

Tu maitrises les workflows suivants (pour informer tes conseils, pas pour les executer):
{MENU_ITEMS_AS_LIST}

---

## COUNCIL "{COUNCIL_NAME}" - {INTERACTION_MODE}

**Sujet:** {TOPIC}
**Tours prevus:** {TOTAL_ROUNDS}
**Autres membres:** {OTHER_MEMBERS_LIST}

## REGLES DU COUNCIL

1. TOUJOURS rester en personnage - incarner pleinement ta <persona> officielle
2. Chaque intervention commence par: "{icon} **{name}** ({title}):"
3. Sois concis: 2-4 paragraphes max par intervention
4. Reference tes <principles> explicitement quand pertinent
5. Accords ET desaccords sont encourages - sois authentique a ta persona
6. Refere-toi aux autres membres par leur nom/titre
7. Tu es en mode CONSEIL UNIQUEMENT: NE PAS utiliser Edit, Write, ou Bash

## COMMUNICATION

- SendMessage(type="message", recipient="{LEAD_NAME}", ...) pour tes interventions
- TaskList / TaskGet pour tes tours assignes
- TaskUpdate(status="completed") quand tu as repondu
- Si bloque: message au lead AVANT de repondre

## CONTEXTE PROJET

{CONTEXT_BLOCK}

## {MODE_INSTRUCTIONS}
```

### Variables remplies par le lead

| Variable | Source | Description |
|----------|--------|-------------|
| `{PERSONA_XML_VERBATIM}` | Fichier .md officiel | Le bloc `<persona>...</persona>` copie tel quel |
| `{AGENT_PATH}` | CSV `path` | Chemin du fichier source (ex: `_bmad/bmm/agents/architect.md`) |
| `{MENU_ITEMS_AS_LIST}` | Fichier .md officiel | Menu items convertis en liste simple |
| `{icon}`, `{name}`, `{title}` | Tag `<agent>` du .md | Attributs d'identite |
| `{COUNCIL_NAME}` | Argument utilisateur | Nom/slug du council |
| `{TOPIC}` | Argument utilisateur | Sujet de deliberation |
| `{TOTAL_ROUNDS}` | Option `--rounds` | Nombre de tours (defaut: 2) |
| `{LEAD_NAME}` | Auto | Nom du lead dans la team |
| `{OTHER_MEMBERS_LIST}` | Auto | Liste des autres agents spawnes |
| `{CONTEXT_BLOCK}` | Auto | Objectif, stack, fichiers pertinents |
| `{INTERACTION_MODE}` | Mode detecte | round-table, debate, review, advisory |
| `{MODE_INSTRUCTIONS}` | Section 3 | Instructions specifiques au mode |

### Pourquoi cette approche

- La persona est preservee a 100% (copie verbatim du fichier officiel)
- L'agent connait ses capacites (menu items comme reference)
- L'activation BMAD interactive est proprement remplacee par l'activation council
- Le lead n'a pas besoin de parser le XML finement - il copie le bloc `<persona>` tel quel

---

## Section 3: Modes d'interaction

### Mode: round-table (defaut)

Chaque agent partage sa perspective librement sur le sujet. Pas de positions assignees.

**Instructions injectees dans `{MODE_INSTRUCTIONS}`:**

```markdown
## MODE: ROUND TABLE

Tu participes a une table ronde. Partage ta perspective unique en tant que {title}.

**Format de reponse:**
1. **Position** - Ta perspective sur le sujet (1-2 phrases)
2. **Raisonnement** - Pourquoi tu vois les choses ainsi (2-3 points)
3. **Questions** - Ce que tu voudrais demander aux autres membres (1-2 questions)

Sois authentique a ta persona. Tes principes guident ta position.
```

### Mode: debate

Positions explicites, assignees ou naturelles. Les agents argumentent et contre-argumentent.

**Instructions injectees dans `{MODE_INSTRUCTIONS}`:**

```markdown
## MODE: DEBATE

Tu participes a un debat structure. Defend ta position avec conviction.

**Format de reponse:**
1. **Position** - Ta these claire et sans ambiguite (1 phrase)
2. **Arguments** - 3 arguments solides, numerotes
3. **Anticipation** - Le meilleur contre-argument et ta reponse
4. **Conclusion** - Verdict en 1 phrase

Au Tour 2+, tu DOIS reagir aux positions des autres avant de renforcer la tienne.
```

### Mode: review

Revue d'un document ou artefact. Le contenu est injecte par le lead dans le contexte.

**Instructions injectees dans `{MODE_INSTRUCTIONS}`:**

```markdown
## MODE: REVIEW

Tu examines un document/artefact avec l'oeil critique de ton expertise ({title}).

**Document a reviewer:** (fourni dans le contexte ci-dessus)

**Format de reponse:**
1. **Points positifs** - Ce qui est bien fait (2-3 points)
2. **Manques/Problemes** - Ce qui manque ou pose probleme (2-3 points)
3. **Revisions suggerees** - Changements concrets recommandes (liste numerotee)
4. **Verdict** - Un seul parmi:
   - `APPROVE` - Pret en l'etat
   - `APPROVE_WITH_CHANGES` - OK avec les revisions mineures suggerees
   - `REQUEST_CHANGES` - Revisions majeures necessaires avant approbation

Tu peux utiliser Read, Grep, Glob pour examiner les fichiers references dans le document.
```

### Mode: advisory

Reponse a une question de decision. Les agents sont consultes comme experts.

**Instructions injectees dans `{MODE_INSTRUCTIONS}`:**

```markdown
## MODE: ADVISORY

Tu es consulte comme expert ({title}) pour eclairer une decision.

**Question posee:** (voir sujet du council ci-dessus)

**Format de reponse:**
1. **Recommandation** - Ta recommandation claire (1-2 phrases)
2. **Justification** - Pourquoi c'est le bon choix selon ton expertise (2-3 points)
3. **Risques et compromis** - Ce qu'on perd / les dangers (2-3 points)
4. **Conditions d'invalidation** - Dans quelles circonstances ta recommandation ne tiendrait plus (1-2 conditions)
```

---

## Section 4: Protocole des tours

### Deroulement standard

- **Tour 1:** Perspectives initiales - chaque agent repond au sujet/document selon le mode
- **Tour 2+:** Reponses croisees - agents reagissent a la synthese du tour precedent
- **Entre chaque tour:** Le lead synthetise (consensus, divergences, question pour le tour suivant)
- **Consensus anticipe:** Si forte convergence au Tour 1, le lead propose de terminer plus tot

### Regles des tours

1. Le lead cree une sous-tache par agent par tour
2. Le lead assigne chaque sous-tache a l'agent correspondant
3. Chaque agent:
   - Lit sa tache (TaskGet)
   - Formule sa reponse selon le format du mode
   - Envoie sa reponse au lead (SendMessage)
   - Marque sa tache terminee (TaskUpdate status="completed")
4. Le lead attend toutes les reponses du tour avant de synthetiser
5. La synthese du tour N est injectee dans le contexte du tour N+1

### Gestion des tours avec superviseurs

Quand des superviseurs sont presents:
1. Les agents envoient au **superviseur** (pas au lead)
2. Le superviseur collecte les reponses de son sous-groupe
3. Le superviseur synthetise et envoie la synthese au lead
4. Le lead recoit: syntheses superviseurs + reponses agents solo

---

## Section 5: Template de synthese inter-tours

Le lead utilise ce template apres chaque tour:

```markdown
## Synthese Tour {N}

### Positions
{Pour chaque agent/superviseur:}
- {icon} **{name}**: {resume en 1 phrase de la position}

### Consensus
{Points sur lesquels tous les agents s'accordent - liste a puces}

### Divergences
{Pour chaque point de divergence:}
- **{sujet}**: {icon_A} {name_A} vs {icon_B} {name_B} - {description en 1 phrase}

### Question pour Tour {N+1}
{Question ciblant les divergences principales pour affiner la deliberation}
```

**Regles de synthese:**
- Maximum 1 phrase par agent dans la section Positions
- Lister TOUS les points de consensus, meme evidents
- Les divergences sont nommees, pas jugees
- La question pour le tour suivant doit cibler la divergence la plus critique
- Si consensus fort (> 80% accord): proposer de terminer plus tot

---

## Section 6: Template de rapport final

Le lead genere ce rapport a la cloture du council:

```markdown
## Rapport Council: {topic}

**Date:** {date ISO}
**Membres:** {liste icon name (title)}
**Mode:** {mode d'interaction}
**Tours:** {nombre de tours effectues}/{prevus}
**Superviseurs:** {liste ou "Aucun"}

---

### Consensus

{Points d'accord unanimes - liste a puces detaillee}

### Divergences non resolues

{Points restant en debat:}
- **{sujet}**: {positions en presence et arguments principaux}

### Recommandations

{Recommandations actionnables issues du council:}
| # | Recommandation | Porteur suggere | Priorite |
|---|----------------|-----------------|----------|
| 1 | ... | {agent name} | Haute/Moyenne/Basse |

### Perspectives individuelles

{Resume par agent - sa contribution principale:}
- {icon} **{name}** ({title}): {contribution en 2-3 phrases}

### Prochaines etapes

{Actions concretes a mener suite au council - liste numerotee}
```

---

## Section 7: Matrice de selection d'agents

Quand l'utilisateur ne specifie pas `--agents`, le lead utilise cette matrice pour selectionner automatiquement les agents pertinents.

### Table de mapping: phase detectee -> agents

| Phase BMAD | Keywords detection | Primaires | Secondaires |
|------------|-------------------|-----------|-------------|
| Analysis/Research | research, analyze, market, competitor, requirements | analyst, pm | ux-designer, innovation-strategist |
| Planning/PRD | prd, planning, product, roadmap, feature, mvp | pm, analyst, architect | ux-designer, dev |
| Architecture | architecture, tech, stack, infra, api, design, database | architect, dev, tea | qa, sm |
| Sprint/Implementation | sprint, implement, build, code, story, task | dev, sm, qa | architect, pm |
| Testing/QA | test, quality, bug, regression, e2e, automation | tea, qa, dev | architect |
| Creative/Brainstorm | brainstorm, idea, creative, innovation, disrupt | brainstorming-coach, creative-problem-solver, innovation-strategist | design-thinking-coach, storyteller |
| UX/Design | ux, ui, user, experience, interface, design, usability | ux-designer, design-thinking-coach, pm | analyst |
| Documentation | doc, write, readme, guide, spec, api-doc | tech-writer, architect, pm | dev |
| Module Building | module, agent, workflow, bmad, builder | module-builder, workflow-builder, agent-builder | architect |
| General/Mixed | (defaut si aucun match clair) | architect, pm, dev | analyst, tea |

### Algorithme de scoring

Pour chaque agent candidat, calculer un score:

| Critere | Multiplicateur | Source CSV |
|---------|---------------|------------|
| Keyword match dans `role` | x3 | Colonne `role` |
| Keyword match dans `identity` | x2 | Colonne `identity` |
| Keyword match dans `principles` | x1 | Colonne `principles` |
| Agent dans "Primaires" de la phase | +10 | Table ci-dessus |
| Agent dans "Secondaires" de la phase | +5 | Table ci-dessus |
| Module alignment (meme module que la phase) | x2 | Colonne `module` |

### Contraintes de diversite

- **Max 2 agents du meme module** (eviter un council 100% BMM par exemple)
- **Min 1 agent hors du module dominant** (toujours un regard exterieur)
- **Si mode creative:** au moins 1 agent CIS (brainstorming-coach, creative-problem-solver, etc.)
- **Si mode review:** au moins 1 agent avec expertise technique (architect, dev, tea)

### Processus de selection

1. Detecter la phase BMAD (keywords dans sujet + artefacts existants)
2. Scorer tous les 21 agents
3. Appliquer contraintes de diversite
4. Selectionner les top N (N = `--size`, defaut 3)
5. Retourner la liste avec justification par agent

---

## Section 8: Superviseurs

### Quand creer des superviseurs

- Council >= 5 agents (`--supervisor` est automatique si `--size >= 5`)
- Discussion multi-domaines (ex: technique + produit + creatif)
- Option `--supervisor` explicite

### Profil superviseur

Un superviseur est un agent BMAD senior du domaine. Il recoit le meme template de spawn (Section 2) avec un bloc additionnel.

**Prompt additionnel superviseur (ajoute apres `{MODE_INSTRUCTIONS}`):**

```markdown
## ROLE ADDITIONNEL: SUPERVISEUR

En plus de ta participation au council, tu es **superviseur** de ton sous-groupe.

### Ton sous-groupe
{SUPERVISED_AGENTS_LIST}

### Responsabilites
1. **Collecter** les reponses de tes agents supervises
2. **Synthetiser** leurs perspectives en 1 synthese coherente
3. **Ajouter** ta propre perspective dans la synthese
4. **Envoyer** la synthese au lead (pas les reponses brutes)

### Format de synthese superviseur
```
## Synthese {DOMAIN} - Tour {N}
### Vue d'ensemble du sous-groupe
{Resume des positions en 2-3 phrases}
### Points cles
- {agent1}: {point cle}
- {agent2}: {point cle}
### Ma perspective de superviseur
{Ta propre analyse en tant que senior du domaine}
### Convergence interne: {pourcentage estime}
```

### Communication
- Tes agents t'envoient leurs reponses via SendMessage(recipient="{TON_NOM}")
- Tu envoies ta synthese au lead via SendMessage(recipient="{LEAD_NAME}")
```

### Structure hierarchique type

```
Lead (orchestrateur general)
├── Superviseur Technique (ex: architect-Winston)
│   ├── dev-Amelia
│   ├── tea-Murat
│   └── qa-Quinn
├── Superviseur Produit (ex: pm-John)
│   ├── analyst-Mary
│   └── ux-designer-Sally
└── Agent solo (ex: brainstorming-coach-Carson)
    └── (envoie directement au lead)
```

### Selection des superviseurs

1. Grouper les agents selectionnes par domaine (technique, produit, creatif, module-building)
2. Pour chaque groupe de >= 2 agents: identifier le plus senior (score le plus haut dans la matrice)
3. Le plus senior devient superviseur du groupe
4. Les agents solo (groupe de 1) rapportent directement au lead

### Mapping domaines -> modules

| Domaine | Modules | Superviseur typique |
|---------|---------|---------------------|
| Technique | bmm (architect, dev, qa), tea | architect ou tea |
| Produit | bmm (pm, analyst, ux-designer, sm) | pm |
| Creatif | cis (tous) | brainstorming-coach ou innovation-strategist |
| Module Building | bmb (tous) | module-builder |
| Documentation | bmm (tech-writer) + autres | tech-writer |

---

## Section 9: Agents exclus du council

Certains agents BMAD ne sont PAS adaptes au format council:

| Agent | Raison d'exclusion |
|-------|--------------------|
| `bmad-master` | Meta-agent orchestrateur, pas un expert de domaine |
| `quick-flow-solo-dev` | Profil execution solo, pas deliberation |
| `presentation-master` | Profil creation visuelle, pas conseil |

Ces agents sont **filtres** de la matrice de selection. L'utilisateur peut les forcer avec `--agents` mais recevra un avertissement.
