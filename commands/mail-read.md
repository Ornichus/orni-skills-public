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

6. **Traiter chaque message (autonome, pas de menu d'actions):**

   Pour chaque message, lire le contenu complet, l'afficher, puis **classer l'intention** sans demander à l'utilisateur :

   **Classification d'intention** (l'agent décide en lisant le contenu) :

   | Intention détectée | Indices | Action automatique |
   |--------------------|---------|---------------------|
   | **INFO** | "FYI", "pour info", "j'ai constaté", "rapport", pas de question/demande explicite | Afficher contenu + résumé court → **archiver auto** + signaler à l'utilisateur les points actionnables s'il y en a (bugs, suggestions à intégrer dans le projet) |
   | **REQUEST_INFO** | Questions concrètes (`?`, "peux-tu", "quel est", "comment") | Si la réponse est dans le contexte/code/state du projet courant → **répondre auto** avec la réponse factuelle + archiver. Sinon → présenter la question à l'utilisateur et attendre instruction. |
   | **HANDOFF** | "passe le relais", "ownership", "à toi de jouer", "tu prends" | **Pas de réponse auto**. Présenter à l'utilisateur le contexte + checklist de décision (accepter/refuser/déléguer). Attendre instruction. |
   | **TASK_ORDER** | "fais X", "implémente Y", "ajoute Z" venant d'un projet ami | Si tâche claire et alignée projet courant → exécuter directement (créer todo, faire le travail) puis répondre avec rapport + archiver. Sinon → présenter à l'utilisateur. |
   | **AMBIGUOUS** | Doute, mix d'intentions, message long et flou | Présenter à l'utilisateur avec ta lecture du message + recommandation. |

   **Règle d'or** : ne jamais demander "veux-tu archiver ou répondre ?". L'agent agit. Il consulte l'utilisateur **uniquement** quand l'action requiert une décision humaine (HANDOFF, AMBIGUOUS, ou réponse hors-projet).

   **Override utilisateur** : si l'utilisateur, dans son prompt initial, donne une instruction explicite par message (ex : "réponds au msg 1, archive le 2"), respecter à la lettre et ignorer la classification auto.

   ### Génération d'une réponse (auto ou demandée)

   1. Composer le corps :
      - **Réponse auto** : factuelle, courte, basée sur l'état réel du projet courant
      - **Réponse demandée** : utiliser le texte fourni par l'utilisateur
   2. Frontmatter de la réponse :
      - `id` : nouveau `msg_` + 8 hex
      - `from` : slug du projet courant
      - `to` : `from` du message original
      - `subject` : "RE: " + sujet original (sauf si déjà préfixé RE:)
      - `reply-to` : `id` du message original
      - `thread-id` : reprendre le `thread-id` du message original
   3. Créer la mailbox du destinataire si nécessaire (`mkdir -p`)
   4. Écrire dans `~/.claude/mailbox/{to-original}/inbox/` (nommage section 5 du SKILL)
   5. Archiver le message original : déplacer vers `archive/`
   6. Confirmer : "Réponse envoyée à **{to}**, message original archivé."

   ### Archivage

   ```bash
   mv ~/.claude/mailbox/{slug}/inbox/{fichier} ~/.claude/mailbox/{slug}/archive/
   ```

7. **Résumé final:**

   Après traitement de tous les messages :
   ```
   ## Résumé

   | Action | Nombre |
   |--------|--------|
   | Réponses auto envoyées | X |
   | Messages archivés (INFO) | X |
   | Messages remontés à l'utilisateur (HANDOFF/AMBIGUOUS) | X |
   | Tâches exécutées (TASK_ORDER) | X |

   Messages restants dans l'inbox : **Y**
   ```

   Pour les messages remontés à l'utilisateur, lister explicitement la décision attendue.
