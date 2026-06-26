---
description: 'Initialise le module Architecture Relationnelle v2.0.0 (4 modes) dans le projet courant'
---

# /orni-init-archi - Installer Architecture Relationnelle

Installe le skill de cartographie d'architecture relationnelle dans le projet courant.

## Instructions

### 1. Charger le skill source

Lire `~/.claude/orni-skills.json` pour trouver le chemin Orni-skills (`ORNI`).
Puis lire `{ORNI}/skills/architecture/SKILL.md` pour recuperer la version source.

### 2. Pre-flight

- Verifier que `{ORNI}/skills/architecture/SKILL.md` existe
- Verifier que `{ORNI}/commands/architecture.md` existe
- Si `.claude/skills/architecture/SKILL.md` existe deja : signaler et proposer `/orni-update-archi`

### 3. Installer

```
Fichiers a copier :
  {ORNI}/skills/architecture/SKILL.md  →  .claude/skills/architecture/SKILL.md
  {ORNI}/commands/architecture.md      →  .claude/commands/architecture.md
```

Creer les dossiers si necessaire.

### 4. Mettre a jour le manifeste

Lire ou creer `.claude/orni-manifest.json` et ajouter :

```json
{
  "modules": {
    "AR": {
      "version": "[version lue depuis SKILL.md]",
      "installed_at": "[ISO 8601 UTC]",
      "updated_at": "[ISO 8601 UTC]",
      "source": "skills/architecture/SKILL.md"
    }
  }
}
```

### 5. Verification

- [ ] `.claude/skills/architecture/SKILL.md` existe et est lisible
- [ ] `.claude/commands/architecture.md` existe et est lisible
- [ ] `.claude/orni-manifest.json` contient l'entree AR

### 6. Rapport

```
/orni-init-archi termine

| Element | Status |
|---------|--------|
| SKILL.md | Installe |
| architecture.md (commande) | Installe |
| Manifeste | Mis a jour (AR v[X.Y.Z]) |

Utilisation : /architecture [audit|sync|fix] [--deep|--preview|--phase N|--parallel]
```
