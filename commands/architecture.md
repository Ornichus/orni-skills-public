---
description: 'Génère et maintient la documentation d architecture, le Product Specification et le PRD du projet'
---

# /architecture — Documentation Intelligente v2

Analyse, génère et maintient la documentation complète du projet via 4 modes.

## Syntaxe

/architecture [mode] [options]

**Modes :**
- (aucun) → Génération de la carte technique (docs/architecture.md)
- audit → Scan profond de toute la base documentaire, rapport de gaps
- sync → Mise à jour rapide du PS et PRD depuis les changements récents
- fix → Mode agentique : agents spécialisés corrigent, user valide

**Options :**
- --deep → Force le scan profond (8 sources) même en mode génération
- --preview → Estime les sources et la taille avant de lancer l'audit
- --phase N → (mode fix) Exécuter seulement la phase N (1=PS, 2=PRD, 3=Archi, 4=Stories)
- --parallel → (mode fix) Lancer tous les agents en parallèle
- --sources → Générer le dossier docs/.sources/ avec les copies des sources (opt-in)

## Instructions

### Étape 1 : Charger le skill

Lire le fichier SKILL.md du module architecture :
- Projet : .claude/skills/architecture/SKILL.md
- Global : ~/.claude/skills/architecture/SKILL.md
- Source Orni : chercher via ~/.claude/orni-skills.json → skills/architecture/SKILL.md

### Étape 2 : Parser les arguments

1. Identifier le mode : aucun argument → génération, "audit" → audit, "sync" → sync, "fix" → fix
2. Identifier les options : --deep, --preview, --phase, --parallel, --sources
3. Valider les combinaisons (--phase et --parallel ne s'appliquent qu'au mode fix)

### Étape 3 : Exécuter le workflow correspondant

Suivre le workflow du mode sélectionné tel que défini dans le SKILL.md :
- Mode génération → Section "Workflow : /architecture"
- Mode audit → Section "Workflow : /architecture audit"
- Mode sync → Section "Workflow : /architecture sync"
- Mode fix → Section "Workflow : /architecture fix"

**IMPORTANT :** Chaque mode commence par le health-check documentaire (intelligence proactive) et se termine par la boucle interactive (proposition de la suite).

### Étape 4 : Garde-fous

- ZERO modification de fichier source — uniquement docs/ et CLAUDE.md
- ZERO secret dans la documentation
- ZERO écriture sans validation humaine explicite
- Analyse COMPLETE obligatoire — ne jamais se fier à une doc existante comme seule source
- Backup OBLIGATOIRE avant toute modification

## Exemples d'utilisation

/architecture                    → Génère docs/architecture.md
/architecture audit              → Scan profond + rapport de gaps
/architecture audit --preview    → Estime avant de lancer
/architecture sync               → Met à jour PS et PRD
/architecture fix                → Corrige tout (phase par phase)
/architecture fix --phase 1      → Corrige seulement le PS
/architecture fix --parallel     → Tous les agents en parallèle
/architecture --deep             → Génération avec scan profond
