---
description: 'Affiche le status condense du projet (auto-genere si necessaire)'
---

# /orni-status - Rapport d'etat condense

Affiche un rapport d'etat structure en 4 sections (ou mode rapide). Lit `project-status.json` s'il existe, sinon le genere a la volee depuis le contexte disponible.

**Syntaxe:** `/orni-status` (complet) ou `/orni-status quick` (rapide)

## Instructions

1. **Charger le skill PSS:**
   - Lire `~/.claude/skills/project-status-snapshot/SKILL.md`
   - Ce skill contient le schema JSON, les regles de generation et les formats de sortie

2. **Resoudre les donnees source:**

   **Cas A — `project-status.json` existe ET `current.snapshot_date` n'est pas null :**
   - Utiliser les donnees du JSON comme source principale
   - Passer a l'etape 3

   **Cas B — `project-status.json` n'existe pas OU `current.snapshot_date` est null :**
   - Generer le snapshot a la volee depuis les sources disponibles (par priorite) :
     1. **Contexte de la conversation en cours** (objectif, decisions, ce qui a ete fait)
     2. **project-state.xml** si present (session-id, phase, current-objective, tasks)
     3. **CLAUDE.md** (description du projet, documentation referencee)
     4. **Archon MCP** si disponible (taches todo/doing/done)
   - Remplir les champs `current` selon les regles de generation du SKILL.md (section 2)
   - Resoudre le slug du projet (project-state.xml > CLAUDE.md H1 > basename)
   - **Creer/mettre a jour `project-status.json`** avec les donnees generees :
     - Si le fichier n'existe pas : le creer avec le template du SKILL.md
     - Si le fichier existe mais vide : remplir `current`
     - Appliquer la rotation historique si applicable
   - Afficher : "*Snapshot genere a la volee et sauvegarde dans project-status.json.*"
   - Passer a l'etape 3

3. **Detecter le mode:**
   - Si l'argument contient "quick" ou "rapide" : mode rapide
   - Sinon : mode complet (defaut)

4. **Mode complet — Afficher le format 4 sections:**

   ```
   ## Status : {project}
   **Session :** {session} | **Phase :** {phase} | **Date :** {snapshot_date}

   ### 1. Question de depart
   {current.question}

   ### 2. Ce qui s'est passe
   {Generer un paragraphe narratif a partir de current.decisions — 1-2 phrases par decision significative, en ordre chronologique logique}

   ### 3. Synthese
   | Problematique | Axe d'analyse | Resultat | Status |
   |---------------|---------------|----------|--------|
   | {decisions[].topic} | {decisions[].analysis} | **{decisions[].result}** | {decisions[].status} |

   ### 4. Resume
   > {current.summary}

   ### Prochaines actions
   - {current.next_actions[] — liste a puces}

   ### Bloqueurs
   - {current.blockers[] — liste a puces, ou "Aucun"}
   ```

   Si `current.metrics` contient des donnees, ajouter :
   ```
   ### Metriques
   | Cle | Valeur |
   |-----|--------|
   | {key} | {value} |
   ```

5. **Mode rapide — Afficher le format condense:**

   ```
   ## {project} — {phase}

   > {current.summary}

   **A faire :** {current.next_actions jointes par ", "}
   **Bloqueurs :** {current.blockers jointes par ", ", ou "Aucun"}
   ```

6. **Historique (optionnel, mode complet seulement):**

   Si `history` contient des entrees, ajouter a la fin :
   ```
   ---

   ### Snapshots precedents
   | Date | Session | Phase | Resume |
   |------|---------|-------|--------|
   | {history[].snapshot_date} | {history[].session} | {history[].phase} | {history[].summary} |
   ```
