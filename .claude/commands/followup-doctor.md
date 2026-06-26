---
description: 'Diagnostic de cohérence entre project-state.xml et fichiers réels'
---

# /followup-doctor - Diagnostic de cohérence du projet

Vérifie la cohérence entre project-state.xml et l'état réel du projet courant.

## Instructions

### 1. Identifier le projet courant

- Le projet courant = le répertoire courant ; `project-state.xml` se trouve à sa racine

### 2. Collecter les données

**project-state.xml:**
- Fichier: `{project-root}/project-state.xml` (fichier local au projet)
- Si le fichier n'existe pas, signaler qu'il faut utiliser `/update` pour le créer

**État réel du projet:**
- Vérifier existence des fichiers clés mentionnés dans project-state.xml
- Vérifier les dossiers de documentation

### 3. Vérifications de cohérence

| Vérification | Description |
|--------------|-------------|
| **FILE-01** | Les fichiers clés listés dans `<resources>` existent-ils réellement ? |
| **SYNC-01** | L'objectif actuel du XML correspond-il à une tâche `doing` de la section `<tasks>` ? |
| **SYNC-02** | Les tâches `<tasks status="done">` correspondent-elles aux livrables réellement présents ? |
| **DATE-01** | La date `<last-updated>` est-elle récente (< 7 jours) ? |
| **TASK-01** | Y a-t-il des tâches `doing` depuis trop longtemps (> 3 jours) ? |
| **MILE-01** | Les milestones correspondent-ils à l'avancement réel ? |

### 4. Générer le rapport

## Format de sortie

```
# Diagnostic de Cohérence - [DATE]

## Projet Détecté
- **Nom:** [NOM]
- **XML project-id:** `xxx-xxx-xxx`

## Résumé
| Catégorie | Status | Issues |
|-----------|--------|--------|
| Cohérence project-state.xml | ✅/⚠️/❌ | X issues |
| Fichiers projet | ✅/⚠️/❌ | X issues |
| Dates et fraîcheur | ✅/⚠️/❌ | X issues |

## Détails des vérifications

### ✅ Vérifications OK
- [SYNC-01] Objectif aligné avec les tâches en cours
- [FILE-01] Fichiers clés présents

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
