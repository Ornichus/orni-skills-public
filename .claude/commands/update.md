---
description: 'Menu de mise a jour projet — state, prd, ou all'
---

# /update - Mise a jour projet

Point d'entree pour les mises a jour projet. Propose 3 modes.

## Instructions

1. **Si argument fourni** (ex: `/update state`, `/update prd`, `/update all`) :
   - Executer directement le mode correspondant sans afficher le menu

2. **Sinon, afficher le menu :**

   ```
   ## /update — Quel mode ?

   | # | Mode | Description | Quand l'utiliser |
   |---|------|-------------|-----------------|
   | 1 | **State** | Archon MCP + project-state.xml + synthese conversation | Fin de session (leger, ~30-50K tokens) |
   | 2 | **PRD** | Audit conversation vs code + propagation docs (PS, PRD, architecture.md) | Debut de session suivante (lourd, ~80-150K tokens) |
   | 3 | **All** | State maintenant + PRD marque en attente | Fin de session (lance state, differe prd) |

   > **Note contexte :** /update-prd necessite un budget contexte large. En fin de session, privilegier State (1) ou All (3) qui differe automatiquement le PRD.

   Choix (1/2/3) :
   ```

3. **Executer le mode choisi :**
   - **1 (State)** : Suivre les instructions de `/update-state`
   - **2 (PRD)** : Suivre les instructions de `/update-prd`
   - **3 (All)** : Suivre les instructions de `/update-all`
