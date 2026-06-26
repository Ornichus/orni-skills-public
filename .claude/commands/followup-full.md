---
description: 'Affiche etat complet du projet (state + documentation)'
---

# /followup-full - Etat complet du projet

Affiche l'etat du projet puis l'etat de la documentation en sequence.

## Instructions

1. **Executer /followup-state :**
   - Suivre toutes les instructions de `/followup-state`

2. **Verifier le marqueur prd-pending :**
   - Chercher `_backup/prd-pending.marker` a la racine du projet
   - Si present : afficher une alerte visible (voir /followup-prd etape 0) et recommander de lancer /update-prd

3. **Enchainer /followup-prd :**
   - Suivre toutes les instructions de `/followup-prd`

3. **Synthese finale :**
   ```
   ## Sante globale du projet

   - **Taches Archon :** N en cours, N en review, N todo
   - **Documentation :** N tags non-resolus ([NON IMPLEMENTE] + [PARTIEL])
   - **Dernier audit :** YYYY-MM-DD (ou "jamais")
   - **Recommandation :** [action prioritaire si applicable]
   ```
