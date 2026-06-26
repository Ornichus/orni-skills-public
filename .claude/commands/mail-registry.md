---
description: 'Gere le registre des projets (scan, liste, edit)'
---

# /mail-registry - Gestion du registre des projets

Gere le fichier `~/.claude/mailbox/registry.json` qui mappe les slugs vers les chemins des repos.

**Syntaxe:**
- `/mail-registry` ou `/mail-registry list` — affiche le registre
- `/mail-registry scan` — scanne les dossiers et met a jour le registre
- `/mail-registry edit` — permet l'edition manuelle (ajouter/modifier aliases, descriptions)

## Instructions

### Action : list (defaut)

1. Lire `~/.claude/mailbox/registry.json`
2. Afficher un tableau :

   | Slug | Aliases | Path | Description |
   |------|---------|------|-------------|
   | ... | ... | ... | ... |

3. Afficher : "{N} projets enregistres. Dernier scan : {date}"

### Action : scan

1. Lire les `scan_paths` du registre (ou utiliser le defaut `<VOTRE_DOSSIER_PROJETS>`)
2. Pour chaque dossier dans les scan_paths :
   - Chercher `CLAUDE.md` (max depth 2)
   - Resoudre le slug (project-state.xml > CLAUDE.md H1 > basename)
   - Extraire la description (premiere phrase apres H1 dans CLAUDE.md)
3. Merger avec le registre existant :
   - Nouveaux projets : ajouter avec slug comme seul alias
   - Projets existants : mettre a jour le path si change, garder les aliases manuels
4. Mettre a jour `last_scan`
5. Ecrire le registre
6. Afficher : "{N} projets trouves, {M} nouveaux, {P} mis a jour"

### Action : edit

1. Afficher le registre actuel
2. Demander a l'utilisateur ce qu'il veut modifier :
   - Ajouter un alias a un projet
   - Modifier la description
   - Supprimer un projet orphelin
   - Ajouter un scan_path
3. Appliquer les modifications et ecrire le registre
