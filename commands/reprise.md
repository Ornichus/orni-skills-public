---
description: 'Gere la TRANSITION (hand-off / reprise a travers un /clear). Args: present|absent, arm [mode], ou un mode (follow-up|ultracode|workflow|iterate).'
---

# /reprise — Gestion de la transition (hand-off & reprise)

> **Périmètre STRICT : la transition uniquement** — passer le relais à travers un `/clear` et reprendre exactement. Cette commande **ne décide rien** du workflow qui suit ; elle ne fait que le relais. L'arbre de décision ci-dessous concerne les problèmes **de la transition**, pas les tâches.

Argument : `$ARGUMENTS` (vide · `present` · `absent` · `arm [mode]` · ou un mode `follow-up|ultracode|workflow|iterate|plain`).

## 1. Présence (drapeau GLOBAL, visible dans la statusline)

- `/reprise present` → écrit `present` dans `C:/Users/<USER>/.claude/reprise-presence`. Tu es là : en cas de souci de transition, l'agent te sollicite plus volontiers.
- `/reprise absent` → écrit `absent`. Tu es parti : l'agent pousse la transition au maximum, seul.
- **Réflexe (sans commande)** : si l'utilisateur signale qu'il part (« bonne nuit », « je reviens », « je m'absente », « continue sans moi ») → passe en `absent`. S'il revient (« je suis là », « re ») → `present`.
- Écris le mot seul (`present`/`absent`), puis confirme : `REPRISE présence → <present|absent>` (statusline à jour au prochain refresh).

## 2. Logique principale

1. **Parser l'argument.**
2. `present` / `absent` → écrire le drapeau présence (section 1) et **stop**.
3. **ARMER le relais** (préparer le hand-off) — si arg = `arm`, OU si tu es en train de finir / de passer la main et qu'aucun relais frais n'existe :
   - Capture l'état : `objective`, `done_so_far`, `next_step`, et `mode` = **la logique préétablie à reprendre** (`follow-up|ultracode|workflow|iterate|plain` ; déduis-la du contexte si non fournie).
   - Écris `<projet>/.claude/reprise-relais.json` :
     ```json
     { "created": "<ISO8601>", "session_id": "<id ou ->", "project": "<slug>",
       "mode": "<...>", "objective": "...", "done_so_far": "...", "next_step": "...", "consumed": false }
     ```
   - Confirme : « Relais armé (mode: X). Fais `/clear` — la nouvelle session reprendra seule. »
4. **REPRENDRE** — sinon (un relais existe, ou un mode est passé) :
   - Lis `<projet>/.claude/reprise-relais.json` s'il existe, sinon `project-state.xml`.
   - Reprends **exactement la logique préétablie** (`mode`). Si un mode est donné en argument :
     - `follow-up` → exécute `/followup` **puis** continue la tâche.
     - `ultracode` / `workflow` → réactive l'orchestration sur l'objectif capturé.
     - `iterate` → reprends la boucle test-fix.
     - `plain` → reprends simplement la tâche.
   - Marque le relais `consumed: true` (ou supprime-le).
   - Annonce en une ligne ce que tu reprends, puis enchaîne.

## 3. Arbre de décision — TRANSITION uniquement

Pendant le hand-off / la reprise (écrire le relais, lire l'état, basculer), si un problème survient :
- **Anodin / réversible** → continue la transition.
- **Rattrapable** (un backup couvre le risque) → **sauvegarde puis continue** ; si le backup est trop lourd/disproportionné → traite comme bloquant.
- **Bloquant** (info manquante, état corrompu) → arrête proprement, écris le souci dans le relais, signale-le.
- **Critique / irréversible / externe** → **jamais seul** : pause et attends.
- Modulé par la **présence** : `present` → sollicite plus volontiers ; `absent` → pousse au maximum, n'arrête que sur critique. Marge de manœuvre = **bon sens + contexte**.

> Rappel : tout ceci ne concerne **que la transition**. Le présent/absent ne change rien aux workflows ni à ce que l'agent fait ensuite (cette partie sera gérée plus tard).
