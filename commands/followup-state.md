---
description: 'Etat projet depuis Archon MCP et project-state.xml'
---

# /followup-state - Etat projet (Archon + State)

Affiche l'état actuel du projet depuis Archon MCP et project-state.xml.

## Instructions

1. **Identifier le projet courant:**
   - Lire `CLAUDE.md` à la racine du projet pour trouver l'**Archon Project ID**
   - Pattern à chercher: `**Archon Project ID:** \`xxx-xxx-xxx\``
   - Si non trouvé, demander à l'utilisateur

2. **Lire Archon MCP:**
   - `find_projects(project_id="<ID trouvé>")` pour le projet
   - `find_tasks(project_id="<ID trouvé>", filter_by="status", filter_value="doing")` pour tâches en cours
   - `find_tasks(project_id="<ID trouvé>", filter_by="status", filter_value="review")` pour tâches en review
   - `find_tasks(project_id="<ID trouvé>", filter_by="status", filter_value="todo", per_page=10)` pour tâches à faire

3. **Lire project-state.xml:**
   - Fichier: `{project-root}/project-state.xml` (fichier local au projet)
   - Si le fichier n'existe pas, indiquer qu'il faut utiliser `/update` pour le créer
   - Extraire les informations clés: objectif, tâches, history, milestones

4. **Afficher un résumé structuré**

## Format de sortie

```
# État du Projet: [NOM_PROJET]

**Archon ID:** `xxx-xxx-xxx`

## Objectif Actuel (project-state.xml)
**[NOM_OBJECTIF]** - Status: [STATUS]
> [DESCRIPTION]

## Tâches en Cours (Archon)
| Tâche | Assignée à | Feature |
|-------|------------|---------|
| ... | ... | ... |

## Tâches en Review (Archon)
| Tâche | Assignée à | Feature |
|-------|------------|---------|
| ... | ... | ... |

## Prochaines Tâches (Archon)
| Tâche | Priorité | Feature |
|-------|----------|---------|
| ... | ... | ... |

## Derniers Événements (project-state.xml)
- [DATE] - Événement 1
- [DATE] - Événement 2

## Milestones Complétés
- [x] Milestone 1 (DATE)
- [x] Milestone 2 (DATE)

## Notes
- Note 1
- Note 2
```
