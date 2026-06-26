---
description: 'Initialise le module Project Status Snapshot dans le projet courant'
---

# /orni-init-pss - Installer Project Status Snapshot

Installe le skill de rapport d'etat condense (JSON + format humain 4 sections) dans le projet courant.

## Instructions

### 1. Charger le skill source

Lire `~/.claude/orni-skills.json` pour trouver le chemin Orni-skills (`ORNI`).
Puis lire `{ORNI}/skills/project-status-snapshot/SKILL.md` pour recuperer la version source.

### 2. Pre-flight

- Verifier que `{ORNI}/skills/project-status-snapshot/SKILL.md` existe
- Si `.claude/skills/project-status-snapshot/SKILL.md` existe deja : signaler et proposer `/orni-update-pss`

### 3. Installer

```
Fichiers a copier :
  {ORNI}/skills/project-status-snapshot/SKILL.md  →  .claude/skills/project-status-snapshot/SKILL.md
  {ORNI}/commands/orni-status.md                    →  .claude/commands/orni-status.md
```

Si `project-status.json` n'existe PAS a la racine du projet :
```
  {ORNI}/skills/project-status-snapshot/template/project-status-template.json  →  project-status.json
```
Remplacer `PROJECT_SLUG` dans le fichier copie par le slug reel du projet (resolution standard : project-state.xml > CLAUDE.md H1 > basename).

Si `project-status.json` existe DEJA : ne pas ecraser (donnees utilisateur). Afficher : "project-status.json existant conserve."

Creer les dossiers si necessaire.

### 4. Mettre a jour le manifeste

Lire ou creer `.claude/orni-manifest.json` et ajouter :

```json
{
  "modules": {
    "PSS": {
      "version": "1.0.0",
      "installed_at": "[ISO 8601 UTC]",
      "updated_at": "[ISO 8601 UTC]",
      "source": "skills/project-status-snapshot/SKILL.md"
    }
  }
}
```

### 5. Verification

- [ ] `.claude/skills/project-status-snapshot/SKILL.md` existe et est lisible
- [ ] `.claude/commands/orni-status.md` existe
- [ ] `project-status.json` existe a la racine
- [ ] `.claude/orni-manifest.json` contient l'entree PSS

### 6. Rapport

```
/orni-init-pss termine

| Element | Status |
|---------|--------|
| SKILL.md | Installe |
| /status command | Installee |
| project-status.json | [Cree / Existant conserve] |
| Manifeste | Mis a jour (PSS v1.0.0) |

Utilisation :
- `/orni-status` pour afficher le rapport d'etat condense
- `/status quick` pour un resume rapide
- `/update` met a jour automatiquement project-status.json
```
