---
description: 'Etat projet depuis project-state.xml'
---

# /followup-state - Etat projet (State)

Affiche l'état actuel du projet depuis project-state.xml.

## Instructions

1. **Lire project-state.xml:**
   - Fichier: `{project-root}/project-state.xml` (le répertoire courant = le projet, project-state.xml à sa racine)
   - Si le fichier n'existe pas, indiquer qu'il faut utiliser `/update` pour le créer
   - Extraire les informations clés: objectif, tâches, history, milestones

2. **Lire les tâches dans la section `<tasks>`:**
   - Les tâches se lisent dans la section `<tasks>` du project-state.xml
   - Statuts: `todo` / `doing` / `review` / `done`
   - Regrouper par statut: en cours (`doing`), en review (`review`), à faire (`todo`)

3. **Afficher un résumé structuré**

## Format de sortie

```
# État du Projet: [NOM_PROJET]

## Objectif Actuel (project-state.xml)
**[NOM_OBJECTIF]** - Status: [STATUS]
> [DESCRIPTION]

## Tâches en Cours (project-state.xml)
| Tâche | Assignée à | Feature |
|-------|------------|---------|
| ... | ... | ... |

## Tâches en Review (project-state.xml)
| Tâche | Assignée à | Feature |
|-------|------------|---------|
| ... | ... | ... |

## Prochaines Tâches (project-state.xml)
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
