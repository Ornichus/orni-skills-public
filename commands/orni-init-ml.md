---
description: 'Initialise le module Mailbox inter-projets dans le projet courant'
---

# /orni-init-ml - Initialiser Mailbox Inter-Projets

Initialise les commandes `/mail-send` et `/mail-read` et le skill mailbox dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier si le module est déjà installé : `.claude/commands/mail-send.md` dans le projet courant
   - Si déjà installé : AVERTIR et demander confirmation avant de continuer

4. **Installer le module ML:**
   - Suivre le manifeste "Module ML" du SKILL.md
   - Copier les commandes : `mail-send.md` et `mail-read.md`
   - Copier le skill `mailbox/` (SKILL.md, README.md)

5. **Post-install:**
   - Résoudre le slug du projet courant (algorithme de résolution du skill mailbox/SKILL.md)
   - Créer la mailbox globale du projet :
     ```bash
     mkdir -p ~/.claude/mailbox/{slug}/inbox
     mkdir -p ~/.claude/mailbox/{slug}/archive
     ```
   - Informer : "Mailbox créée pour **{slug}** dans `~/.claude/mailbox/{slug}/`"
   - Vérifier si le module UF (Update/Followup) est installé : `.claude/commands/update.md`
   - Si UF absent : informer "Le module UF est recommandé pour `project-state.xml` (améliore la détection du slug). Installez-le avec `/orni-init-uf`."

6. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le créer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/mailbox/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre à jour l'entrée du module ML :
     ```json
     {
       "modules": {
         "ML": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/mailbox/SKILL.md"
         }
       }
     }
     ```

7. **Vérification:**
   - Confirmer que `.claude/commands/mail-send.md` existe
   - Confirmer que `.claude/commands/mail-read.md` existe
   - Confirmer que `.claude/skills/mailbox/SKILL.md` existe
   - Confirmer que `.claude/skills/mailbox/README.md` existe
   - Confirmer que `~/.claude/mailbox/{slug}/inbox/` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler les commandes disponibles :
     - Envoyer : `/mail-send <destinataire> "Sujet"`
     - Lire : `/mail-read`
     - Interactif : `/mail-send` (liste les projets connus)
