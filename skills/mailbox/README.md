# Mailbox Inter-Projets

Systeme de communication asynchrone entre agents Claude Code travaillant dans des projets differents.

## Concept

Les agents Claude Code operent dans des projets isoles. Quand un agent a une question pour un agent d'un autre projet, il peut deposer un message dans la boite aux lettres du destinataire. Le destinataire le lira lors de sa prochaine session.

## Architecture

```
~/.claude/mailbox/
├── orni-skills/
│   ├── inbox/          # Messages non lus
│   └── archive/        # Messages lus/archives
├── my-webapp/
│   ├── inbox/
│   └── archive/
└── ...
```

Chaque projet possede un **slug** unique derive de son nom.

## Commandes

### /mail-send

Envoie un message a un autre projet.

```
/mail-send my-webapp "Question about auth"
```

Mode interactif (liste les projets connus) :
```
/mail-send
```

### /mail-read

Lit les messages du projet courant.

```
/mail-read                        # Tous les messages
/mail-read --from my-webapp       # Filtrer par expediteur
/mail-read --thread thread_abc123 # Filtrer par conversation
```

## Lifecycle d'un message

```
1. Agent A execute /mail-send vers projet B
   → Fichier cree dans ~/.claude/mailbox/B/inbox/

2. Agent B execute /mail-read
   → Lit le message, choisit une action :
     - Repondre → nouveau fichier dans ~/.claude/mailbox/A/inbox/
     - Archiver → fichier deplace vers ~/.claude/mailbox/B/archive/
     - Passer   → fichier reste dans inbox

3. Agent A execute /mail-read
   → Voit la reponse de B dans son inbox
```

## Format des messages

Fichiers Markdown avec frontmatter YAML :

```yaml
---
id: msg_a1b2c3d4
from: orni-skills
to: my-webapp
subject: Question about auth strategy
date: 2026-02-15T14:30:00Z
reply-to: null
thread-id: thread_e5f6g7h8
---

Salut ! On travaille sur l'integration OAuth et on se demande
quelle strategie vous avez choisie pour les refresh tokens.
```

## Bonnes pratiques

1. **Sujets clairs** : le sujet doit etre comprehensible sans lire le corps
2. **Messages concis** : aller droit au but, le contexte peut se perdre entre sessions
3. **Un sujet par thread** : ne pas melanger les sujets dans un meme fil
4. **Archiver regulierement** : garder l'inbox propre pour reperer les nouveaux messages
5. **Verifier sa mailbox** : prendre l'habitude de lancer `/mail-read` en debut de session

## Installation

Installe avec les autres modules Orni-Skills :

```bash
/orni-init-ml     # Installation initiale du module Mailbox
/orni-update-ml   # Mise a jour du module
/orni-init-full   # Installation complete (inclut Mailbox)
```

## Details techniques

Voir `SKILL.md` pour :
- Algorithme de resolution du slug projet
- Format complet du frontmatter
- Convention de nommage des fichiers
- Generation des identifiants
