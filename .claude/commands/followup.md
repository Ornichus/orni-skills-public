---
description: 'Menu de consultation etat projet — state, prd, ou full'
---

# /followup - Etat du projet

Point d'entree pour consulter l'etat du projet. Propose 3 modes.

## Instructions

1. **Si argument fourni** (ex: `/followup state`, `/followup prd`, `/followup full`) :
   - Executer directement le mode correspondant sans afficher le menu

2. **Sinon, afficher le menu :**

   ```
   ## /followup — Quel mode ?

   | # | Mode | Description |
   |---|------|-------------|
   | 1 | **State** | project-state.xml (taches, objectifs, historique) |
   | 2 | **PRD** | Etat de la documentation (PS, PRD, architecture.md, tags de statut) |
   | 3 | **Full** | State puis PRD |

   Choix (1/2/3) :
   ```

3. **Executer le mode choisi :**
   - **1 (State)** : Suivre les instructions de `/followup-state`
   - **2 (PRD)** : Suivre les instructions de `/followup-prd`
   - **3 (Full)** : Suivre les instructions de `/followup-full`
