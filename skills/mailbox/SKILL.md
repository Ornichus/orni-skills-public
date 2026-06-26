# Mailbox Inter-Projets - Skill partagé

> **Version**: 1.0.0 | Logique commune pour `/mail-send` et `/mail-read`

Ce skill définit le protocole de communication inter-projets via un système de boîtes aux lettres dans `~/.claude/mailbox/`.

---

## 1. Architecture

```
~/.claude/mailbox/
├── {slug-projet-A}/
│   ├── inbox/          # Messages non lus
│   └── archive/        # Messages lus/archivés
├── {slug-projet-B}/
│   ├── inbox/
│   └── archive/
└── ...
```

Chaque projet a sa propre boîte aux lettres identifiée par un **slug unique**.

---

## 2. Résolution du slug projet

### Priorité (première valeur trouvée gagne)

1. **project-state.xml** : `<project-name>` dans `<metadata>`
2. **CLAUDE.md** : première ligne `# Titre du projet` (heading H1)
3. **Nom du dossier** : basename du répertoire courant

### Algorithme de sanitization

Appliquer dans l'ordre :
1. Convertir en minuscules
2. Remplacer espaces et underscores par des tirets (`-`)
3. Supprimer tous les caractères non `[a-z0-9-]`
4. Réduire les tirets multiples en un seul
5. Supprimer les tirets en début/fin
6. Tronquer à 50 caractères max

### Exemples

| Source | Slug résultant |
|--------|----------------|
| `BMAD Skills` | `bmad-skills` |
| `My_WebApp (v2)` | `my-webapp-v2` |
| `Orni-Skills` | `orni-skills` |

---

## 3. Format des messages

### Frontmatter YAML

```yaml
---
id: msg_<8-chars-hex>
from: <slug-expediteur>
to: <slug-destinataire>
subject: <sujet en texte libre>
date: <ISO 8601 avec timezone Z>
reply-to: null
thread-id: thread_<8-chars-hex>
---
```

### Champs

| Champ | Description | Exemple |
|-------|-------------|---------|
| `id` | Identifiant unique du message | `msg_a1b2c3d4` |
| `from` | Slug du projet expéditeur | `orni-skills` |
| `to` | Slug du projet destinataire | `my-webapp` |
| `subject` | Sujet du message | `Question about auth strategy` |
| `date` | Date/heure ISO 8601 UTC | `2026-02-15T14:30:00Z` |
| `reply-to` | ID du message auquel on répond | `null` ou `msg_x1y2z3w4` |
| `thread-id` | ID du fil de conversation | `thread_e5f6g7h8` |

### Corps du message

Texte libre en Markdown après le frontmatter. Pas de limite de taille imposée mais rester concis.

---

## 4. Génération des identifiants

### msg_id

```bash
msg_$(cat /dev/urandom | tr -dc 'a-f0-9' | head -c 8)
```

Format : `msg_` + 8 caractères hexadécimaux aléatoires.

### thread_id

```bash
thread_$(cat /dev/urandom | tr -dc 'a-f0-9' | head -c 8)
```

Format : `thread_` + 8 caractères hexadécimaux aléatoires.

**Règle thread :** Un nouveau message crée un nouveau `thread_id`. Une réponse (reply) réutilise le `thread-id` du message original.

---

## 5. Convention de nommage des fichiers

### Format

```
{YYYY-MM-DD}_{HHMM}_{from}_{subject-slug}.md
```

### Sanitization du sujet

Même algorithme que le slug projet (section 2), appliqué au champ `subject`, tronqué à 40 caractères.

### Exemples

| Date | From | Subject | Nom fichier |
|------|------|---------|-------------|
| 2026-02-15 14:30 | orni-skills | Question about auth | `2026-02-15_1430_orni-skills_question-about-auth.md` |
| 2026-02-15 16:00 | my-webapp | RE: Auth strategy | `2026-02-15_1600_my-webapp_re-auth-strategy.md` |

---

## 6. Opérations mailbox

### Créer une mailbox

```bash
mkdir -p ~/.claude/mailbox/{slug}/inbox
mkdir -p ~/.claude/mailbox/{slug}/archive
```

Toujours utiliser `mkdir -p` pour créer la structure si elle n'existe pas encore.

### Lister les messages inbox

```bash
ls ~/.claude/mailbox/{slug}/inbox/*.md 2>/dev/null
```

Trier par nom de fichier (le préfixe date assure l'ordre chronologique).

### Compter les messages

```bash
ls ~/.claude/mailbox/{slug}/inbox/*.md 2>/dev/null | wc -l
```

### Archiver un message

```bash
mv ~/.claude/mailbox/{slug}/inbox/{fichier}.md ~/.claude/mailbox/{slug}/archive/
```

### Lister les destinataires connus

```bash
ls -d ~/.claude/mailbox/*/ 2>/dev/null | xargs -I{} basename {}
```

---

## 7. Réponse à un message

Quand on répond à un message :
1. Le champ `reply-to` prend la valeur de l'`id` du message original
2. Le champ `thread-id` reprend le `thread-id` du message original
3. Le message est déposé dans la `inbox/` du projet **expéditeur original** (`from` du message auquel on répond)
4. Le sujet est préfixé par "RE: " si ce n'est pas déjà le cas
