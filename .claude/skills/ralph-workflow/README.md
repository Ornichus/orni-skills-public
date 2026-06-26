# Ralph Workflow Skill

Workflow complet pour la validation PRD et l'exécution autonome de features avec Ralph Loop.

## Quick Start

1. Copier le dossier `.ralph/` template dans votre projet
2. Adapter `PRD-ralph.md` à votre projet
3. Configurer agent-browser (voir SKILL.md)
4. Lancer `./.ralph/ralph.sh 50`

## Fichiers

| Fichier | Description |
|---------|-------------|
| SKILL.md | Guide complet du workflow |
| LAUNCH-PROMPT.md | Prompt pour lancer le workflow sur un nouveau projet |
| templates/ | Templates des fichiers Ralph |

## Phases

1. **Setup** - PRD + agent-browser
2. **Test Manuel** - Human + Agent testent ensemble
3. **Analyse Écarts** - Comparaison PRD vs réalité
4. **Révision PRD** - Correction et mise à jour
5. **Ralph Loop** - Exécution autonome

## Prérequis

- Claude Code CLI
- WSL Ubuntu avec agent-browser
- PRD existant (BMAD ou autre format)

## Installation Agent-Browser

```bash
# WSL Ubuntu
npm install -g agent-browser
npx playwright install chromium
```

## Liens

- [SKILL.md](SKILL.md) - Documentation complète
- [LAUNCH-PROMPT.md](LAUNCH-PROMPT.md) - Prompt de lancement

---

*Version 0.1.0-beta*
