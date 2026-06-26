---
description: 'Diagnostic de cohérence entre Archon MCP, project-state.xml et fichiers réels'
---

# /followup-doctor - Diagnostic de cohérence du projet

Vérifie la cohérence entre Archon MCP, project-state.xml et l'état réel du projet courant.

## Instructions

### 1. Identifier le projet courant

- Lire `CLAUDE.md` à la racine du projet pour trouver l'**Archon Project ID**
- Pattern à chercher: `**Archon Project ID:** \`xxx-xxx-xxx\``
- Si non trouvé, demander à l'utilisateur

### 2. Collecter les données

**Archon MCP:**
- `find_projects(project_id="<ID trouvé>")` pour les infos projet
- `find_tasks(project_id="<ID trouvé>", per_page=50)` pour toutes les tâches

**project-state.xml:**
- Fichier: `{project-root}/project-state.xml` (fichier local au projet)
- Si le fichier n'existe pas, signaler qu'il faut utiliser `/update` pour le créer

**État réel du projet:**
- Vérifier existence des fichiers clés mentionnés dans project-state.xml
- Vérifier les dossiers de documentation

### 3. Vérifications de cohérence

| Vérification | Description |
|--------------|-------------|
| **SYNC-01** | Les tâches "done" dans Archon sont-elles dans `<tasks status="completed">` du XML ? |
| **SYNC-02** | L'objectif actuel XML correspond-il aux tâches "doing" Archon ? |
| **FILE-01** | Les fichiers clés listés dans `<resources>` existent-ils ? |
| **DATE-01** | La date `<last-updated>` est-elle récente (< 7 jours) ? |
| **TASK-01** | Y a-t-il des tâches "doing" depuis trop longtemps (> 3 jours) ? |
| **ID-01** | Le project-id dans le XML correspond-il à l'Archon ID dans CLAUDE.md ? |
| **MILE-01** | Les milestones correspondent-ils à l'avancement réel ? |

### 4. Générer le rapport

## Format de sortie

```
# Diagnostic de Cohérence - [DATE]

## Projet Détecté
- **Nom:** [NOM]
- **Archon ID:** `xxx-xxx-xxx`
- **XML project-id:** `xxx-xxx-xxx`

## Résumé
| Catégorie | Status | Issues |
|-----------|--------|--------|
| Synchronisation Archon/XML | ✅/⚠️/❌ | X issues |
| Fichiers projet | ✅/⚠️/❌ | X issues |
| Dates et fraîcheur | ✅/⚠️/❌ | X issues |
| Cohérence IDs | ✅/⚠️/❌ | X issues |

## Détails des vérifications

### ✅ Vérifications OK
- [SYNC-01] Tâches synchronisées
- [ID-01] IDs cohérents

### ⚠️ Avertissements
- [DATE-01] Dernière mise à jour il y a X jours

### ❌ Problèmes détectés
- [FILE-01] Fichier X manquant

## Actions recommandées
1. [PRIORITÉ HAUTE] ...
2. [PRIORITÉ MOYENNE] ...
3. [PRIORITÉ BASSE] ...

## Commande de correction
Si des problèmes sont détectés, exécuter `/update` pour resynchroniser.
```
