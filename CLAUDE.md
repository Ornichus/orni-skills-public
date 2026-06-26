# Orni-Skills — instructions projet

Ce dépôt est une **bibliothèque de skills, commandes et workflows pour Claude Code**.
Il sert de référence centrale : chaque module est installable dans un projet cible via une commande `/orni-init-*`.

## Organisation

- `commands/` — slash commands (méta-commandes `/orni-init-*`, `/orni-update-*`, plus les commandes de chaque module).
- `skills/` — un dossier par module, chacun avec un `SKILL.md` qui décrit son comportement.
- `_bmad/` — framework BMAD (Module Builder `bmb`, Method `bmm`, Creative & Innovation `cis`, Testing `tea`, `core`).
- `.claude/commands` et `.claude/skills` — versions installées côté projet.
- `docs/` — guides d'utilisation.
- `templates/` — gabarits (dont un `CLAUDE.md` projet standardisé).

## Conventions

- Chaque module doit avoir sa commande d'installation `/orni-init-<code>` et de mise à jour `/orni-update-<code>`.
- Les secrets, clés d'API et configurations spécifiques à une machine **ne sont jamais versionnés** : ils vivent dans des fichiers locaux (`~/.claude/*.json`) référencés par les skills, jamais en dur dans le dépôt.
- Pour ajouter ou modifier un module, suivre la structure d'un module existant (`SKILL.md` + commande init/update).

## Pour démarrer

Lire `README.md` pour le catalogue des modules, puis `docs/GUIDE-UTILISATION.md` pour le workflow quotidien.
