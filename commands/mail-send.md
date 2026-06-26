---
description: 'Envoie un message à un autre projet via la mailbox inter-projets'
---

# /mail-send - Envoyer un message inter-projets

Envoie un message depuis le projet courant vers la boîte aux lettres d'un autre projet.
**L'agent compose le message** d'après le contexte de la conversation. L'utilisateur ne rédige pas le message.

**Syntaxe:** `/mail-send <destinataire>`

## Instructions

1. **Charger le skill mailbox:**
   - Lire `~/.claude/skills/mailbox/SKILL.md`
   - Ce skill contient le protocole complet (format, slugs, nommage)

2. **Identifier le projet courant (slug expéditeur):**
   - Appliquer l'algorithme de résolution du slug (SKILL.md section 2):
     1. Chercher `<project-name>` dans `project-state.xml` du répertoire courant
     2. Sinon, chercher le heading H1 (`# ...`) dans `CLAUDE.md`
     3. Sinon, utiliser le basename du répertoire courant
   - Appliquer la sanitization (lowercase, hyphens, max 50 chars)
   - Afficher : "Projet identifié : **{slug}**"

2b. **Auto-enregistrement dans le registre:**
   - Lire `~/.claude/mailbox/registry.json` (créer si absent avec structure par défaut)
   - Si le slug courant n'est pas dans le registre :
     - Ajouter l'entrée avec path = répertoire courant, aliases = [slug], description extraite de CLAUDE.md
   - Si le slug existe mais le path a changé :
     - Mettre à jour le path
   - Écrire le registre

3. **Résoudre le destinataire:**
   - Si `<destinataire>` fourni en argument : sanitizer le slug
   - Sinon (mode interactif) :
     - Lister les mailboxes existantes : `ls -d ~/.claude/mailbox/*/ 2>/dev/null`
     - Afficher la liste des projets connus (exclure le projet courant)
     - Demander à l'utilisateur de choisir ou saisir un nouveau slug
   - Vérifier que le destinataire n'est pas le même que l'expéditeur

4. **Composer le message (l'AGENT rédige, PAS l'utilisateur):**
   - Analyser le contexte de la conversation en cours
   - Identifier la raison/besoin qui motive l'envoi du message
   - Rédiger un **sujet** clair et concis
   - Rédiger un **corps de message** structuré qui :
     - Se présente (quel projet, quel contexte)
     - Explique clairement la demande ou l'information
     - Pose des questions précises si nécessaire
     - Reste concis et actionnable
   - **Afficher le brouillon** à l'utilisateur pour validation AVANT envoi
   - L'utilisateur peut valider, modifier ou annuler

5. **Générer les métadonnées:**
   - `id` : `msg_` + 8 hex aléatoires
   - `thread-id` : `thread_` + 8 hex aléatoires
   - `date` : date/heure courante en ISO 8601 UTC
   - `reply-to` : `null` (message initial)

6. **Créer la mailbox destinataire si nécessaire:**
   ```bash
   mkdir -p ~/.claude/mailbox/{to}/inbox
   mkdir -p ~/.claude/mailbox/{to}/archive
   ```

7. **Créer la mailbox expéditeur si nécessaire:**
   ```bash
   mkdir -p ~/.claude/mailbox/{from}/inbox
   mkdir -p ~/.claude/mailbox/{from}/archive
   ```

8. **Écrire le message:**
   - Générer le nom du fichier selon la convention : `{YYYY-MM-DD}_{HHMM}_{from}_{subject-slug}.md`
   - Écrire le fichier dans `~/.claude/mailbox/{to}/inbox/` avec le frontmatter YAML + corps

   Format du fichier :
   ```markdown
   ---
   id: msg_xxxxxxxx
   from: {slug-expediteur}
   to: {slug-destinataire}
   subject: {sujet}
   date: {ISO 8601}
   reply-to: null
   thread-id: thread_xxxxxxxx
   ---

   {corps du message}
   ```

9. **Confirmation:**
   Afficher un résumé :
   ```
   ## Message envoyé

   | Champ | Valeur |
   |-------|--------|
   | De | {from} |
   | À | {to} |
   | Sujet | {subject} |
   | ID | {msg_id} |
   | Thread | {thread_id} |
   | Fichier | {nom_fichier} |

   Le destinataire pourra le lire avec `/mail-read` depuis son projet.
   ```
