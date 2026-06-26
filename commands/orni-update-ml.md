---
description: 'Met à jour le module Mailbox inter-projets dans le projet courant'
---

# /orni-update-ml - Mettre à jour Mailbox Inter-Projets

Met à jour les commandes `/mail-send` et `/mail-read` et le skill mailbox dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que le module EST installé : `.claude/commands/mail-send.md` dans le projet courant
   - Si PAS installé : AVERTIR et suggérer `/orni-init-ml` puis abandonner

4. **Mettre à jour le module ML:**
   - Suivre le manifeste "Module ML" du SKILL.md (logique Update)
   - Copier les commandes : `mail-send.md` et `mail-read.md` en écrasement
   - Copier le skill `mailbox/` en écrasement (SKILL.md, README.md)
   - NE PAS TOUCHER aux messages existants dans `~/.claude/mailbox/`

5. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/mailbox/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Mettre à jour l'entrée ML : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Vérification:**
   - Confirmer que `.claude/commands/mail-send.md` existe
   - Confirmer que `.claude/commands/mail-read.md` existe
   - Confirmer que `.claude/skills/mailbox/SKILL.md` existe
   - Confirmer que `.claude/skills/mailbox/README.md` existe

7. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler les commandes disponibles :
     - Envoyer : `/mail-send <destinataire> "Sujet"`
     - Lire : `/mail-read`
   - Préciser : "Les messages existants dans `~/.claude/mailbox/` n'ont pas été modifiés."
