---
description: 'Execute /update-state puis marque /update-prd comme en attente (contexte-safe)'
---

# /update-all - Mise a jour complete

Execute /update-state immediatement et differe /update-prd a la prochaine session (debut de session, contexte frais).

## Pourquoi ce decoupage

/update-prd est gourmand en tokens (~80-150K) : audit conversation, cross-ref git, 3 sous-agents paralleles. Appele en fin de session (quand /update est generalement invoque), il echoue silencieusement par manque de contexte. Ce design garantit que state est toujours sauvegarde et que prd tourne dans des conditions optimales.

## Instructions

### Etape 1 : Executer /update-state

- Suivre toutes les instructions de `/update-state`
- Attendre la completion (confirmation affichee)

### Etape 2 : Marquer /update-prd comme en attente

Creer le fichier marqueur `_backup/prd-pending.marker` a la racine du projet :

```
PRD_PENDING=true
DEFERRED_AT={ISO 8601 datetime}
DEFERRED_REASON=context-budget
SESSION_ID={session-id depuis project-state.xml}
```

- Creer `_backup/` si absent (mkdir -p)
- Ce marqueur est detecte par `/followup-prd` et `/followup-full`

### Etape 3 : Rapport et consigne

```
## /update-all termine

### State
- Archon MCP : [resume]
- project-state.xml : [resume]

### PRD (differe)
- /update-prd est marque comme en attente
- **Action requise :** lancer `/update-prd` en debut de session suivante (contexte frais)
- Le `/followup` de la prochaine session vous le rappellera automatiquement
```

## Exception : contexte frais

Si tu es certain d'avoir un budget contexte large (debut de session, conversation courte), tu PEUX enchainer /update-prd immediatement apres /update-state. Dans ce cas :
1. Suivre les instructions de `/update-prd`
2. Supprimer le marqueur `_backup/prd-pending.marker` si il existe
3. Fusionner les rapports state et prd dans un rapport consolide unique
