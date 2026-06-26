# Contribuer à Orni-Skills

## Remontées automatiques des agents (`agent-suggestion`)

Les agents (Claude Code, OpenCode…) qui **utilisent** un skill/module Orni peuvent remonter ici tout **manque**, **incohérence** ou **bug** rencontré — sous forme d'**issue** labellisée `agent-suggestion`.

- **Comment** : ouvrir une issue GitHub (par exemple via `gh issue create`) en suivant le modèle `.github/ISSUE_TEMPLATE/agent-suggestion.md`.
- **Format** : titre `[auto][<skill>] …`, corps structuré (Type, Skill, Constat, Élément proposé, Origine).
- **Issue uniquement** : se limiter à ouvrir une issue — pas de PR ni de push de code via cette remontée. Dédoublonner avant de créer (commenter un doublon existant plutôt que d'en rouvrir un).

## Labels

- `agent-suggestion` — remontée automatique par un agent (à trier).
- `bug` / `enhancement` — ajoutés selon le type de la remontée.

## Contributions humaines

Issues et PR manuelles bienvenues selon le workflow GitHub standard. Pour un nouveau composant/skill, suivre la structure décrite dans `skills/<nom>/` et `styles/README.md`.
