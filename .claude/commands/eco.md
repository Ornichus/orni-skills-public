---
description: 'Active/change le Mode Economie Token (off|eco|max), scope global ou local'
---

# /eco — Mode Économie Token

Argument reçu : `$ARGUMENTS` (ex : `max`, `eco --local`, `off --global`, ou vide pour afficher l'état).

Cette commande règle la **molette d'économie de tokens du principal** (toi tant que crédit Claude).

## Logique d'exécution

1. **Parser le niveau** = premier mot de `$ARGUMENTS` ∈ `{off, eco, max, ultra}`.
   - Si vide ou invalide → lire les fichiers `eco-mode` (local puis global), afficher le niveau effectif courant + scope, puis **stop** (ne rien écrire).
2. **Parser le scope** : `--local` → fichier projet ; `--global` ou absent → fichier global. **Défaut = global** (le quota Claude est partagé sur tout l'environnement).
3. **Écrire l'état** (un seul mot, le niveau, sans rien d'autre) :
   - global → `C:/Users/<USER>/.claude/eco-mode`
   - local → `<racine projet>/.claude/eco-mode` (créer `.claude/` si absent)
4. **Résolution** (rappel) : niveau effectif = fichier **local** s'il existe, sinon **global**, sinon `off`. Donc un `off` global est masqué par un fichier local non-off. Si tu poses un niveau global mais qu'un `eco-mode` local non-off traîne dans le projet courant, **le signaler**.
5. **Confirmer** : `ECO → <niveau> (scope: <global|local>)` + rappel 1 ligne du comportement :
   - `off` : aucune contrainte d'économie.
   - `eco` : réflexion/décisions/review chez le principal, tours courts ; lecture/recherche/doc/refacto → délégués à des sous-agents.
   - `max` : seule la réflexion irréductible reste ; tout le reste délégué ; handoff tenu frais.
   - `ultra` : comme `max`, **mais APPLIQUÉ par un hook** — `eco-guard` (PreToolUse) **bloque** Workflow / Agent / Task (les agents Claude consomment le plan).

## Appliquer immédiatement

Le hook SessionStart applique le niveau à la session **suivante** et la statusline le montre au prochain refresh. Pour la session **courante**, applique le comportement du niveau **dès maintenant** dans la conversation (ne pas attendre un restart).

## Règle dure (ne jamais l'enfreindre)

L'économie ne **rétrograde jamais** un gate **Critique** (sécurité / irréversible / cœur logique). L'importance gagne toujours sur l'économie.
