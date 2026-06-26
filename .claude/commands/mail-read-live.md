---
description: 'Ecoute la mailbox et repond automatiquement (conversation autonome agent-a-agent)'
---

# /mail-read-live - Conversation live inter-projets (recepteur)

Ecoute l'inbox en attente de messages et repond automatiquement pour une conversation autonome avec un autre agent.

**Syntaxe:** `/mail-read-live [--thread <thread_id>] [--context <contexte>] [--timeout <minutes>] [--poll <secondes>]`

## Instructions

1. **Charger le skill mailbox:**
   - Lire `~/.claude/skills/mailbox/SKILL.md`
   - Ce skill contient le protocole complet (format, slugs, nommage)

2. **Identifier le projet courant (slug):**
   - Appliquer l'algorithme de resolution du slug (SKILL.md section 2)
   - Afficher : "Live-talk en ecoute pour **{slug}**"

3. **Parametres:**
   - `--thread` (optionnel) : filtrer sur un thread specifique. Si absent, accepte le premier message entrant.
   - `--context` (optionnel) : contexte additionnel pour guider les reponses automatiques
   - `--timeout` (defaut: 10) : minutes sans message avant abandon
   - `--poll` (defaut: 15) : secondes entre chaque verification de l'inbox

4. **Boucle de polling (attente du premier message):**

   ```
   REPETER:
     1. Attendre {poll} secondes (utiliser `sleep {poll}`)
     2. Scanner ~/.claude/mailbox/{slug}/inbox/*.md
     3. Filtrer :
        - Si --thread fourni : messages dont thread-id == thread specifie
        - Sinon : tout message dans l'inbox
     4. Si message trouve :
        a. Lire le contenu complet
        b. Extraire le thread-id (verrouiller dessus pour la suite)
        c. Extraire le from (c'est l'interlocuteur)
        d. Afficher : "--- Message de {from} ---" + contenu
        e. Verifier si le corps contient [RESOLVED] ou [TIMEOUT]
           → Si oui : archiver le message, aller a l'etape 5 (FIN)
        f. Construire le contexte de reponse (voir section 4b)
        g. Generer une reponse automatique
        h. Envoyer la reponse dans ~/.claude/mailbox/{from}/inbox/
        i. Archiver le message recu
        j. Afficher : "--- Reponse envoyee ---" + resume
        k. Remettre le compteur timeout a zero
     5. Si pas de message :
        a. Incrementer le temps ecoule
        b. Si temps ecoule >= timeout :
           → Si un interlocuteur est connu : envoyer [TIMEOUT]
           → Aller a l'etape 5 (FIN)
        c. Afficher : "En attente... ({temps_ecoule}s / {timeout_total}s)"
   ```

   ### 4b. Construction du contexte de reponse

   Pour chaque reponse automatique, l'agent utilise :
   1. **Le message recu** (contenu integral)
   2. **L'historique du thread** : lire tous les messages archives du meme `thread-id` dans `~/.claude/mailbox/{slug}/archive/`, tries chronologiquement
   3. **Le contexte initial** : le parametre `--context` fourni au lancement
   4. **Le contexte projet** : `CLAUDE.md` et `project-state.xml` du repertoire courant
   5. **La consigne** : "Tu es l'agent du projet {slug}. Reponds de maniere utile et concise. Si le probleme est resolu, inclus [RESOLVED] dans ta reponse."

5. **Terminaison:**
   - Archiver TOUS les messages restants du thread dans l'inbox
   - Afficher le resume :
     ```
     ## Live-talk termine

     | Info | Valeur |
     |------|--------|
     | Thread | {thread_id} |
     | Avec | {interlocuteur} |
     | Messages echanges | {count} |
     | Raison de fin | [RESOLVED] / [TIMEOUT] / Aucun message recu |
     | Duree | {duree} |
     ```

## Regles importantes

- **Ne jamais demander d'input utilisateur** — tout est autonome des le lancement
- **Garder les reponses concises** — max 200 mots par message automatique
- **Respecter le format mailbox** pour chaque message (frontmatter YAML + corps markdown)
- **Toujours archiver** les messages traites (ne pas les laisser dans l'inbox)
- **Verrouiller sur le thread** — une fois le premier message recu, ignorer les messages d'autres threads
- **Si plusieurs messages en attente** du meme thread : les lire tous chronologiquement avant de repondre au dernier
