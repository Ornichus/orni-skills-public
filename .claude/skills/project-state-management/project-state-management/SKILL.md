# Project-State Management - Guide Complet

> **Version**: 1.0.0 | **Dernière mise à jour**: 24 janvier 2026

Ce skill définit le pattern de gestion du fichier `project-state.xml` pour les projets Claude Code. L'objectif est de maintenir un fichier condensé pour les agents tout en préservant l'historique complet.

---

## Table des matières

1. [Principe fondamental](#1-principe-fondamental)
2. [Structure des dossiers](#2-structure-des-dossiers)
3. [Format condensé](#3-format-condensé)
4. [Convention de nommage](#4-convention-de-nommage)
5. [Règles de backup](#5-règles-de-backup)
6. [Intégration CLAUDE.md](#6-intégration-claudemd)
7. [Template](#7-template)

---

## 1. Principe fondamental

### Séparation État/Historique

| Fichier | Contenu | Taille cible |
|---------|---------|-------------|
| `project-state.xml` | État actuel UNIQUEMENT | ~150 lignes |
| `_backup/project-state/archive/*.xml` | Historique complet | Illimité |

### Pourquoi ?

- **Agents IA** : Chargement rapide, contexte pertinent
- **Historique** : Préservé mais accessible à la demande
- **Backups** : Protection contre les pertes de données

---

## 2. Structure des dossiers

```
project-root/
├── project-state.xml                    # État actuel (condensé)
└── _backup/
    └── project-state/
        ├── README.md                    # Documentation
        ├── current/
        │   └── project-state_latest.xml # Dernier backup
        └── archive/
            ├── project-state_2026-01-20_10-30-00.xml
            ├── project-state_2026-01-22_15-45-30.xml
            └── project-state-history_2026-01-24.xml
```

### Rôle de chaque dossier

| Dossier | Rôle |
|---------|------|
| `current/` | Dernier backup avant modification |
| `archive/` | Tous les backups historiques |

---

## 3. Format condensé

### Sections à GARDER (~150 lignes)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project-state>
  
  <!-- METADATA - Infos projet -->
  <metadata>
    <name>...</name>
    <version>...</version>
    <last-updated>...</last-updated>
    <description>...</description>
  </metadata>

  <!-- PREREQUISITES - Dépendances -->
  <prerequisites status="validated">
    <credential name="..." status="available"/>
    <service name="..." status="validated"/>
  </prerequisites>

  <!-- CURRENT STATE - État actuel -->
  <current-state>
    <phase>...</phase>
    <status>...</status>
    <progress-percent>...</progress-percent>
    <current-focus>...</current-focus>
    
    <!-- Résumé compact des waves -->
    <waves-summary>
      <wave number="1" status="done">Description courte</wave>
      <wave number="2" status="doing">Description courte</wave>
    </waves-summary>
    
    <last-milestone date="...">...</last-milestone>
  </current-state>

  <!-- TECHNICAL DECISIONS - Résumé -->
  <technical-decisions>
    <decision id="TD-001">Résumé en une ligne</decision>
  </technical-decisions>

  <!-- ARCHITECTURE SUMMARY - Condensé -->
  <architecture-summary>
    <stack>...</stack>
    <key-paths>...</key-paths>
  </architecture-summary>

  <!-- HISTORY REFERENCE -->
  <history-reference>
    <archive-path>_backup/project-state/archive/</archive-path>
    <last-archive>project-state-history_YYYY-MM-DD.xml</last-archive>
  </history-reference>

</project-state>
```

### Sections à ARCHIVER

| Section | Raison |
|---------|--------|
| `<session-log>` | Historique pur |
| `<completed-milestones>` détaillés | Verbeux |
| `<execution-plan>` | Documentation |
| `<user-journey>` | Documentation |
| `<target-architecture>` | Documentation |
| `<next-session-context>` détaillé | Obsolète après session |

---

## 4. Convention de nommage

### Format

```
project-state_{YYYY-MM-DD}_{HH-MM-SS}.xml
```

### Exemples

| Type | Exemple |
|------|--------|
| Backup régulier | `project-state_2026-01-24_10-30-00.xml` |
| Archive historique | `project-state-history_2026-01-24.xml` |
| Backup courant | `project-state_latest.xml` |

---

## 5. Règles de backup

### Déclencheurs

| Événement | Action |
|-----------|--------|
| Avant modification `project-state.xml` | Backup → `current/project-state_latest.xml` |
| Fin de grande étape `/iterate` | Backup → `archive/` + mise à jour latest |
| Auto-compact Claude | Backup via hook PRE-COMPACT |
| Migration/restructuration | Backup complet avant changement |

### Hook PRE-COMPACT (settings.json)

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -File .claude/hooks/pre-compact-backup.ps1"
          }
        ]
      }
    ]
  }
}
```

### Script de backup (PowerShell)

```powershell
# pre-compact-backup.ps1
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$source = "project-state.xml"
$dest = "_backup/project-state/archive/project-state_$timestamp.xml"

if (Test-Path $source) {
    Copy-Item $source $dest
    Copy-Item $source "_backup/project-state/current/project-state_latest.xml"
    Write-Host "[PRE-COMPACT] Backup: $dest"
}
```

---

## 6. Intégration CLAUDE.md

Ajouter cette section dans votre `CLAUDE.md` :

```markdown
## Gestion project-state.xml

### Principe fondamental
- `project-state.xml` = **état actuel UNIQUEMENT** (condensé, ~150 lignes max)
- **Historique** = archivé dans `_backup/project-state/archive/`
- Tout backup est fait AVANT modification du fichier

### Convention de nommage
- Format: `project-state_{YYYY-MM-DD}_{HH-MM-SS}.xml`

### Règles de déclenchement backup
| Événement | Action |
|-----------|--------|
| Avant modification project-state.xml | Backup dans current/ |
| Fin de grande étape /iterate | Backup dans archive/ |
| Auto-compact Claude | Backup via hook PRE-COMPACT |
```

---

## 7. Template

Un template complet est disponible dans `template/project-state-template.xml`.

Pour l'utiliser :

```bash
# Copier le template
cp skills/project-state-management/template/project-state-template.xml project-state.xml

# Créer la structure de backup
mkdir -p _backup/project-state/{current,archive}
```

---

## Changelog

| Date | Version | Changements |
|------|---------|-------------|
| 2026-01-24 | 1.0.0 | Version initiale |

---

## Ressources

- Orni-Skills (ce depot)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
