# Project-State Management

Pattern de gestion du fichier `project-state.xml` pour les projets Claude Code.

## Objectif

Maintenir un fichier `project-state.xml` condensé (~150 lignes) pour les agents IA tout en préservant l'historique complet dans des archives.

## Fichiers

- `SKILL.md` - Documentation complète du pattern
- `template/project-state-template.xml` - Template vide à copier

## Installation rapide

```bash
# 1. Copier le template
cp skills/project-state-management/template/project-state-template.xml project-state.xml

# 2. Créer la structure de backup
mkdir -p _backup/project-state/{current,archive}

# 3. Ajouter à CLAUDE.md (voir SKILL.md section 6)
```

## Résumé

| Fichier | Contenu | Taille |
|---------|---------|--------|
| `project-state.xml` | État actuel | ~150 lignes |
| `_backup/project-state/archive/*.xml` | Historique | Illimité |

## Convention de nommage

```
project-state_{YYYY-MM-DD}_{HH-MM-SS}.xml
```
