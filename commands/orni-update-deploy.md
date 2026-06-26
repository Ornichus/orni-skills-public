---
description: 'Met a jour le module Deploy dans le projet courant'
---

# /orni-update-deploy - Mettre a jour Deploy

Met a jour le skill Deploy et verifie la configuration dans le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que le module EST installe : `.claude/skills/deploy/SKILL.md` dans le projet courant
   - Si PAS installe : AVERTIR et suggerer `/orni-init-deploy` puis abandonner

4. **Mettre a jour le module Deploy:**
   - Copier `{ORNI}/skills/deploy/SKILL.md` en ecrasement

5. **Verifier la configuration globale:**
   - `~/.claude/vps-config.json` : verifier que le fichier existe et contient ip + ssh_key_path
   - `~/.claude/cloudflare.json` : verifier que les champs sont presents (`api_token`, `account_id`, `default_zone`)
   - Tester la connexion SSH :
     ```bash
     ssh -i {ssh_key_path} -o ConnectTimeout=10 {user}@{ip} "echo OK"
     ```
   - Tester l'API Cloudflare :
     ```bash
     CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
     curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
       -H "Authorization: Bearer $CF_TOKEN" | jq '.success'
     ```
   - Si echec d'un test : avertir mais NE PAS bloquer la mise a jour

6. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json`
   - Extraire la nouvelle version depuis `{ORNI}/skills/deploy/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Mettre a jour l'entree DPL : `version` et `updated_at` (conserver `installed_at` d'origine)

7. **Rapport:**
   ```
   ## Deploy - Mise a jour terminee

   | Composant | Statut |
   |-----------|--------|
   | Skill Deploy | Mis a jour (v{ancienne} -> v{nouvelle}) |
   | Connexion SSH | {OK/Echec} |
   | Token Cloudflare | {Valide/Invalide} |
   | Config VPS | {OK/Champs manquants} |
   | Config Cloudflare | {OK/Champs manquants} |
   ```
