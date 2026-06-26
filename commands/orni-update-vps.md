---
description: 'Met à jour le module VPS Management dans le projet courant'
---

# /orni-update-vps - Mettre à jour VPS Management

Met à jour le skill VPS et vérifie la configuration dans le projet courant.

## Instructions

1. **Résoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin à l'utilisateur et créer le fichier

2. **Pré-vol:**
   - Vérifier que `{ORNI}` existe
   - Vérifier que le module EST installé : `.claude/skills/vps/SKILL.md` dans le projet courant
   - Si PAS installé : AVERTIR et suggérer `/orni-init-vps` puis abandonner

3. **Mettre à jour le module VPS:**
   - Copier `{ORNI}/skills/vps/SKILL.md` en écrasement

4. **Vérifier la configuration globale:**
   - `~/.claude/vps-config.json` : vérifier que l'IP et la clé SSH sont toujours valides
   - `~/.claude/mcp.json` : vérifier que `hostinger-api` est configuré
   - `~/.claude/settings.json` : vérifier que `sshConfigs` contient `hostinger-vps`
   - Tester la connexion SSH : `ssh -i ~/.ssh/claude-vps -o ConnectTimeout=5 root@{IP} echo OK`

5. **Mettre à jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/vps/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Mettre à jour l'entrée VPS : `version` et `updated_at` (conserver `installed_at` d'origine)

6. **Vérifier le package MCP:**
   - Vérifier si `hostinger-api-mcp` a une mise à jour : `npm outdated -g hostinger-api-mcp`
   - Si mise à jour disponible : proposer `npm update -g hostinger-api-mcp`

7. **Rapport:**
   ```
   ## VPS Management - Mise à jour terminée

   | Composant | Statut |
   |-----------|--------|
   | Skill VPS | Mis à jour (v{ancienne} -> v{nouvelle}) |
   | Connexion SSH | {OK/Échec} |
   | MCP Hostinger | {À jour/Mise à jour dispo} |
   | npm hostinger-api-mcp | {version} |
   ```
