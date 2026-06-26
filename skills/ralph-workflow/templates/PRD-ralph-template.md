# PRD Ralph: [PROJECT_NAME]

**Version:** 1.0
**Created:** [DATE]
**Exit Condition:** ALL features must have `passes: true`

---

## Overview

- **Goal:** [Objectif principal du projet]
- **Tech Stack:** [Frontend] + [Backend] + [Database]
- **Estimated Features:** [N] features across [M] epics

---

## Features Checklist

### Epic 1: [EPIC_NAME]

> *[Description de l'epic]*

| # | Feature ID | Description | Priority | Validation Steps | Passes |
|---|------------|-------------|----------|------------------|--------|
| 1 | US-1.1 | [Description courte] | MUST | 1. [action] 2. [verify] | false |
| 2 | US-1.2 | [Description courte] | MUST | 1. [action] 2. [verify] | false |
| 3 | US-1.3 | [Description courte] | SHOULD | 1. [action] 2. [verify] | false |

### Epic 2: [EPIC_NAME]

> *[Description de l'epic]*

| # | Feature ID | Description | Priority | Validation Steps | Passes |
|---|------------|-------------|----------|------------------|--------|
| 4 | US-2.1 | [Description courte] | MUST | 1. [action] 2. [verify] | false |
| 5 | US-2.2 | [Description courte] | MUST | 1. [action] 2. [verify] | false |

---

## Validation Protocol

Pour chaque feature:

1. **Implement** - Écrire le code nécessaire
2. **Test** - Exécuter les validation steps avec agent-browser
3. **Verify** - Confirmer que le résultat est correct
4. **Update** - Mettre `passes: true` si validé
5. **Log** - Mettre à jour activity.md

## Agent-Browser Validation Commands

```bash
wsl -d Ubuntu -- bash -c "npx agent-browser open 'http://[IP]:[PORT]'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
wsl -d Ubuntu -- bash -c "npx agent-browser click e1"
wsl -d Ubuntu -- bash -c "npx agent-browser close"
```

---

## Exit Condition

**CRITICAL:** Ne jamais output "promise complete" tant que TOUTES les features n'ont pas `passes: true`.

---

## Progress Summary

| Epic | Total | Completed | Remaining |
|------|-------|-----------|----------|
| Epic 1 | 3 | 0 | 3 |
| Epic 2 | 2 | 0 | 2 |
| **TOTAL** | **5** | **0** | **5** |

---

*PRD Ralph généré le [DATE]*
