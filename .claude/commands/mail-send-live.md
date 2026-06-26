---
description: 'Envoie un message et entre en mode live-talk (conversation autonome agent-a-agent)'
---

# /mail-send-live - Conversation live inter-projets (expediteur)

Envoie un message initial puis entre en boucle de polling pour une conversation autonome avec un autre agent via la mailbox.

**Syntaxe:** `/mail-send-live --to <slug> --subject <sujet> [--context <contexte>] [--timeout <minutes>] [--poll <secondes>]`

## Instructions

1. **Charger le skill mailbox:**
   - Lire `~/.claude/skills/mailbox/SKILL.md`
   - Ce skill contient le protocole complet (format, slugs, nommage)

2. **Identifier le projet courant (slug):**
   - Appliquer l'algorithme de resolution du slug (SKILL.md section 2)
   - Afficher : "Live-talk depuis **{slug}** vers **{to}**"

3. **Parametres:**
   - `--to` (requis) : slug du projet destinataire
   - `--subject` (requis) : sujet de la conversation
   - `--context` (optionnel) : contexte additionnel pour guider les reponses automatiques
   - `--timeout` (defaut: 10) : minutes sans reponse avant abandon
   - `--poll` (defaut: 15) : secondes entre chaque verification de l'inbox

4. **Composer et envoyer le message initial:**
   - Demander le corps du message a l'utilisateur (une seule fois au debut)
   - Generer `msg_id` et `thread_id` selon le protocole mailbox
   - Deposer le message dans `~/.claude/mailbox/{to}/inbox/`
   - Afficher : "Message envoye. Entree en mode live-talk..."

5. **Boucle de polling:**

   ```
   REPETER:
     1. Attendre {poll} secondes (utiliser `sleep {poll}`)
     2. Scanner ~/.claude/mailbox/{slug}/inbox/*.md
     3. Filtrer : messages dont thread-id == thread courant
     4. Si message trouve :
        a. Lire le contenu complet
        b. Afficher : "--- Message de {from} ---" + contenu
        c. Verifier si le corps contient [RESOLVED] ou [TIMEOUT]
           → Si oui : archiver le message, aller a l'etape 6 (FIN)
        d. Construire le contexte de reponse (voir section 5b)
        e. Generer une reponse automatique
        f. Envoyer la reponse dans ~/.claude/mailbox/{to}/inbox/
        g. Archiver le message recu
        h. Afficher : "--- Reponse envoyee ---" + resume
        i. Remettre le compteur timeout a zero
     5. Si pas de message :
        a. Incrementer le temps ecoule
        b. Si temps ecoule >= timeout :
           → Envoyer un message avec [TIMEOUT] dans le corps
           → Aller a l'etape 6 (FIN)
        c. Afficher : "En attente... ({temps_ecoule}s / {timeout_total}s)"
   ```

   ### 5b. Construction du contexte de reponse

   Pour chaque reponse automatique, l'agent utilise :
   1. **Le message recu** (contenu integral)
   2. **L'historique du thread** : lire tous les messages archives du meme `thread-id` dans `~/.claude/mailbox/{slug}/archive/`, tries chronologiquement
   3. **Le contexte initial** : le parametre `--context` fourni au lancement
   4. **Le contexte projet** : `CLAUDE.md` et `project-state.xml` du repertoire courant
   5. **La consigne** : "Tu es l'agent du projet {slug}. Reponds de maniere utile et concise. Si le probleme est resolu, inclus [RESOLVED] dans ta reponse."

6. **Terminaison:**
   - Archiver TOUS les messages restants du thread dans l'inbox
   - Afficher le resume :
     ```
     ## Live-talk termine

     | Info | Valeur |
     |------|--------|
     | Thread | {thread_id} |
     | Avec | {to} |
     | Messages echanges | {count} |
     | Raison de fin | [RESOLVED] / [TIMEOUT] |
     | Duree | {duree} |
     ```

## Regles importantes

- **Ne jamais demander d'input utilisateur** apres le message initial — tout est autonome
- **Garder les reponses concises** — max 200 mots par message automatique
- **Respecter le format mailbox** pour chaque message (frontmatter YAML + corps markdown)
- **Toujours archiver** les messages traites (ne pas les laisser dans l'inbox)
- **Un seul thread** — ignorer les messages d'autres threads/expediteurs
