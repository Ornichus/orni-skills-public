---
description: 'Lit les messages de la mailbox du projet courant'
---

# /mail-read - Lire les messages inter-projets

Lit les messages dans la boîte aux lettres du projet courant et propose des actions (répondre, archiver, passer).

**Syntaxe:** `/mail-read` ou `/mail-read --from <slug>` ou `/mail-read --thread <thread_id>`

## Instructions

1. **Charger le skill mailbox:**
   - Lire `~/.claude/skills/mailbox/SKILL.md`
   - Ce skill contient le protocole complet (format, slugs, nommage)

2. **Identifier le projet courant (slug):**
   - Appliquer l'algorithme de résolution du slug (SKILL.md section 2):
     1. Chercher `<project-name>` dans `project-state.xml` du répertoire courant
     2. Sinon, chercher le heading H1 (`# ...`) dans `CLAUDE.md`
     3. Sinon, utiliser le basename du répertoire courant
   - Appliquer la sanitization (lowercase, hyphens, max 50 chars)
   - Afficher : "Mailbox de **{slug}**"

2b. **Auto-enregistrement dans le registre:**
   - Lire `~/.claude/mailbox/registry.json` (créer si absent avec structure par défaut)
   - Si le slug courant n'est pas dans le registre :
     - Ajouter l'entrée avec path = répertoire courant, aliases = [slug], description extraite de CLAUDE.md
   - Si le slug existe mais le path a changé :
     - Mettre à jour le path
   - Écrire le registre

3. **Créer la mailbox si nécessaire:**
   ```bash
   mkdir -p ~/.claude/mailbox/{slug}/inbox
   mkdir -p ~/.claude/mailbox/{slug}/archive
   ```

4. **Scanner l'inbox:**
   - Lister les fichiers dans `~/.claude/mailbox/{slug}/inbox/*.md`
   - Si `--from <slug>` : filtrer les messages dont le frontmatter `from:` correspond
   - Si `--thread <thread_id>` : filtrer les messages dont le frontmatter `thread-id:` correspond
   - Trier par nom de fichier (chronologique)

5. **Afficher le résumé:**

   Si aucun message :
   ```
   ## Inbox vide
   Aucun message pour **{slug}**. Votre mailbox est à jour.
   ```

   Si messages trouvés :
   ```
   ## Inbox de {slug} — {N} message(s)

   | # | Date | De | Sujet | Thread |
   |---|------|----|-------|--------|
   | 1 | 2026-02-15 14:30 | my-webapp | Question about auth | thread_abc12345 |
   | 2 | 2026-02-15 16:00 | api-server | Deploy schedule | thread_def67890 |
   ```

6. **Traiter chaque message (interactif):**

   Pour chaque message, lire le contenu complet et l'afficher, puis proposer :

   **Actions disponibles :**
   - **Répondre** : composer une réponse
   - **Archiver** : marquer comme lu et déplacer
   - **Passer** : message suivant sans action

   ### Action : Répondre

   1. Demander le corps de la réponse à l'utilisateur
   2. Générer le message de réponse :
      - `id` : nouveau `msg_` + 8 hex
      - `from` : slug du projet courant
      - `to` : `from` du message original
      - `subject` : "RE: " + sujet original (sauf si déjà préfixé RE:)
      - `reply-to` : `id` du message original
      - `thread-id` : reprendre le `thread-id` du message original
   3. Créer la mailbox du destinataire si nécessaire
   4. Écrire dans `~/.claude/mailbox/{to-original}/inbox/`
   5. Archiver le message original : déplacer vers `archive/`
   6. Confirmer : "Réponse envoyée à **{to}**, message original archivé."

   ### Action : Archiver

   1. Déplacer le fichier de `inbox/` vers `archive/` :
      ```bash
      mv ~/.claude/mailbox/{slug}/inbox/{fichier} ~/.claude/mailbox/{slug}/archive/
      ```
   2. Confirmer : "Message archivé."

   ### Action : Passer

   1. Ne rien faire, passer au message suivant.

7. **Résumé final:**

   Après traitement de tous les messages :
   ```
   ## Résumé

   | Action | Nombre |
   |--------|--------|
   | Réponses envoyées | X |
   | Messages archivés | X |
   | Messages passés (restent dans inbox) | X |

   Messages restants dans l'inbox : **Y**
   ```
