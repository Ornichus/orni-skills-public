---
description: 'Initialise le module VPS Management dans le projet courant'
---

# /orni-init-vps - Initialiser VPS Management

Configure l'accès au VPS Hostinger (SSH + MCP) pour le projet courant.

## Instructions

1. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

2. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que `{ORNI}/skills/vps/SKILL.md` existe
   - Vérifier si le module est déjà installé : `.claude/skills/vps/SKILL.md` dans le projet courant
   - Si déjà installé : AVERTIR et demander confirmation

3. **Vérifier les prérequis globaux:**
   - `~/.claude/vps-config.json` existe ? Si non : guider la création
   - `~/.ssh/claude-vps` (clé SSH) existe ? Si non : générer avec `ssh-keygen -t ed25519 -C "claude-vps-access" -f ~/.ssh/claude-vps -N ""`
   - `~/.claude/mcp.json` contient `hostinger-api` ? Si non : demander l'API token et l'ajouter
   - `~/.claude/settings.json` contient `sshConfigs` avec `hostinger-vps` ? Si non : l'ajouter
   - Tester la connexion SSH : `ssh -i ~/.ssh/claude-vps -o ConnectTimeout=5 root@{IP} echo OK`
   - Si échec SSH : indiquer qu'il faut déployer la clé publique manuellement

4. **Installer le module VPS:**
   - Créer `.claude/skills/vps/` dans le projet courant
   - Copier `{ORNI}/skills/vps/SKILL.md`

5. **Vérifier que `.gitignore` protège les secrets:**
   - Si le projet a un `.gitignore`, vérifier qu'il contient `vps-config.json`
   - Sinon : avertir l'utilisateur

6. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le créer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/vps/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre à jour l'entrée du module VPS :
     ```json
     {
       "modules": {
         "VPS": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/vps/SKILL.md"
         }
       }
     }
     ```

7. **Vérification:**
   - Confirmer que `.claude/skills/vps/SKILL.md` existe
   - Confirmer que la connexion SSH fonctionne
   - Confirmer que le MCP `hostinger-api` est configuré

8. **Rapport:**
   ```
   ## VPS Management - Installation terminée

   | Composant | Statut |
   |-----------|--------|
   | Skill VPS | Installé |
   | Clé SSH | {path} |
   | MCP Hostinger | Configuré |
   | Connexion SSH | {OK/Échec} |

   ### Accès disponibles
   - **SSH** : `ssh -i ~/.ssh/claude-vps root@{IP}`
   - **MCP** : Outils hostinger-api disponibles automatiquement

   ### Prochaines étapes
   - Relancer Claude Code pour activer le MCP Hostinger
   - Tester avec : "Montre-moi les DNS de mon domaine"
   ```
