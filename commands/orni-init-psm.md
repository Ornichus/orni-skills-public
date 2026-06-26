---
description: 'Initialise Project State Management (gestion de project-state.xml) dans le projet courant'
---

# /orni-init-psm - Initialiser Project State Management

Initialise le skill project-state-management (gestion de `project-state.xml`) dans le projet courant.

> Ce module est un **skill seul** : il n'a pas de commande dédiée. Il est consommé par `/update` et `/followup`. Cette commande n'installe que le skill.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Ce skill contient les manifestes, la logique et le format de rapport

2. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

3. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que `{ORNI}/skills/project-state-management/SKILL.md` existe
   - Vérifier si le module est déjà installé : `.claude/skills/project-state-management/SKILL.md` dans le projet courant
   - Si déjà installé : AVERTIR et demander confirmation avant de continuer

4. **Installer le module PSM:**
   - Suivre le manifeste "Module PSM" du SKILL.md
   - Copier UNIQUEMENT le skill complet (récursif) : `{ORNI}/skills/project-state-management/` -> `.claude/skills/project-state-management/`
     - SKILL.md
     - README.md
     - template/project-state-template.xml
   - Aucune commande à copier (ce module est un skill seul, utilisé par `/update` et `/followup`)

5. **Post-install:**
   - Vérifier si le module UF (Update/Followup) est installé : `.claude/commands/update.md`
   - Si UF absent : informer "Le skill Project State Management est consommé par `/update` et `/followup`. Installez le module UF avec `/orni-init-uf` pour disposer de ces commandes."

6. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le créer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/project-state-management/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre à jour l'entrée du module PSM :
     ```json
     {
       "modules": {
         "PSM": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/project-state-management/SKILL.md"
         }
       }
     }
     ```

7. **Vérification:**
   - Confirmer que `.claude/skills/project-state-management/SKILL.md` existe
   - Confirmer que `.claude/skills/project-state-management/README.md` existe
   - Confirmer que `.claude/skills/project-state-management/template/project-state-template.xml` existe

8. **Rapport:**
   - Utiliser le format de rapport du SKILL.md
   - Rappeler que ce skill est consommé par `/update` et `/followup` (module UF)
   - Préciser : "Aucune commande dédiée — le skill guide la gestion de `project-state.xml`."
