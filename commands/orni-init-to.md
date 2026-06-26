---
description: 'Initialise le module Task Orchestrator (méta-orchestrateur GSD/BMAD/Superpowers) dans le projet courant'
---

# /orni-init-to — Init Task Orchestrator

Installe le skill `task-orchestrator` + commande `/orchestrate` dans le projet courant.

## Pré-requis

- Projet a déjà `/orni-init-full` exécuté (au minimum UF + Archon configuré)
- `project-state.xml` présent
- Archon Project ID configuré dans CLAUDE.md projet

## Instructions

1. **Résoudre le chemin source Orni :**
   - Lire `~/.claude/orni-skills.json` → `source_path` → `{ORNI}`

2. **Vérifier pré-requis :**
   - `.claude/commands/update.md` existe (UF installé)
   - `project-state.xml` existe à la racine
   - Si l'un manque : avertir et suggérer `/orni-init-full` ou `/orni-init-uf` d'abord

3. **Copier le skill :**
   - `cp -r {ORNI}/skills/task-orchestrator/ .claude/skills/task-orchestrator/`

4. **Copier la commande :**
   - `cp {ORNI}/commands/orchestrate.md .claude/commands/orchestrate.md`

5. **Préparer dir runtime :**
   - Créer `.orchestrate/` (gitignored auto, contiendra state.json + kpis.yaml runtime)
   - Vérifier que `.orchestrate/` est dans `.gitignore` projet (ajouter sinon)

6. **Vérifier que `.worktrees/` est gitignored :**
   - Le skill `task-orchestrator` utilise `superpowers:using-git-worktrees` pour wave parallèle code
   - Ajouter `.worktrees/` à `.gitignore` si pas déjà présent

7. **Mettre à jour `.claude/orni-manifest.json` :**
   ```json
   "TO": {
     "version": "1.0.0",
     "installed_at": "{ISO now}",
     "updated_at": "{ISO now}"
   }
   ```

8. **Vérification finale :**
   - [ ] `.claude/skills/task-orchestrator/SKILL.md` présent
   - [ ] `.claude/commands/orchestrate.md` présent
   - [ ] `.orchestrate/` créé + gitignored
   - [ ] `.worktrees/` gitignored
   - [ ] Manifeste TO enregistré

9. **Rapport :**
   ```
   ## /orni-init-to terminé

   Module Task Orchestrator v1.0.0 installé.

   Commande disponible : /orchestrate
   Modes : (vide) | inventory | organize | route | visualize | execute | goal

   Prochaine étape :
   - /orchestrate    → vue état projet (read-only)
   - /orchestrate execute --confirm-wave   → lance avec confirm
   - /orchestrate goal --bound=20turns    → mode autonome via /goal
   ```

## Référence

Skill détaillé : `.claude/skills/task-orchestrator/SKILL.md` ou `{ORNI}/skills/task-orchestrator/SKILL.md`.
