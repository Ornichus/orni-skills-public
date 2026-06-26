---
description: 'Initialise le module Deploy dans le projet courant'
---

# /orni-init-deploy - Initialiser Deploy

Configure le deploiement automatise (VPS + Cloudflare) pour le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que `{ORNI}/skills/deploy/SKILL.md` existe
   - Verifier si le module est deja installe : `.claude/skills/deploy/SKILL.md` dans le projet courant
   - Si deja installe : AVERTIR et demander confirmation

4. **Verifier les prerequis (BLOQUANTS) :**

   Chaque verification ci-dessous est **BLOQUANTE** : si l'une echoue, ARRETER l'installation et indiquer clairement l'erreur.

   **4a. Module VPS installe :**
   - Verifier que `~/.claude/skills/vps/SKILL.md` existe
   - Si absent : ERREUR BLOQUANTE — "Le module VPS doit etre installe globalement. Lancez `/orni-init-vps` d'abord."

   **4b. Module Cloudflare installe :**
   - Verifier que `~/.claude/skills/cloudflare/SKILL.md` existe
   - Si absent : ERREUR BLOQUANTE — "Le module Cloudflare doit etre installe globalement. Lancez `/orni-init-cf` d'abord."

   **4c. Configuration VPS :**
   - Verifier que `~/.claude/vps-config.json` existe
   - Si absent : ERREUR BLOQUANTE — "Fichier `~/.claude/vps-config.json` introuvable. Lancez `/orni-init-vps` d'abord."
   - Lire `ip` et `ssh_key_path` (ou `user` si present, sinon `root`) depuis le fichier

   **4d. Configuration Cloudflare :**
   - Verifier que `~/.claude/cloudflare.json` existe
   - Si absent : ERREUR BLOQUANTE — "Fichier `~/.claude/cloudflare.json` introuvable. Lancez `/orni-init-cf` d'abord."
   - Lire `api_token` depuis le fichier

   **4e. Test SSH :**
   - Lire `user` (defaut: `root`), `ip`, `ssh_key_path` depuis `~/.claude/vps-config.json`
   - Executer :
     ```bash
     ssh -i {ssh_key_path} -o ConnectTimeout=10 {user}@{ip} "echo OK"
     ```
   - Si echec : ERREUR BLOQUANTE — "Connexion SSH echouee vers {user}@{ip}. Verifiez votre configuration VPS."

   **4f. Test token Cloudflare :**
   - Executer :
     ```bash
     CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
     curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
       -H "Authorization: Bearer $CF_TOKEN" | jq '.success'
     ```
   - Si le resultat n'est pas `true` : ERREUR BLOQUANTE — "Token Cloudflare invalide ou expire. Mettez a jour `~/.claude/cloudflare.json`."

5. **Installer le module Deploy:**
   - Creer `.claude/skills/deploy/` dans le projet courant
   - Copier `{ORNI}/skills/deploy/SKILL.md`

6. **Afficher les domaines Cloudflare disponibles :**
   - Executer :
     ```bash
     CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
     curl -s "https://api.cloudflare.com/client/v4/zones?per_page=50" \
       -H "Authorization: Bearer $CF_TOKEN" \
       | jq -r '.result[] | "\(.name) (\(.id))"'
     ```
   - Presenter la liste des domaines disponibles

7. **Verifier que `.gitignore` protege les secrets:**
   - Si le projet a un `.gitignore`, verifier qu'il contient `vps-config.json` et `cloudflare.json`
   - Sinon : avertir l'utilisateur

8. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le creer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/deploy/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre a jour l'entree du module DPL :
     ```json
     {
       "modules": {
         "DPL": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/deploy/SKILL.md"
         }
       }
     }
     ```

9. **Verification:**
   - [ ] `.claude/skills/deploy/SKILL.md` existe dans le projet
   - [ ] `~/.claude/skills/vps/SKILL.md` existe
   - [ ] `~/.claude/skills/cloudflare/SKILL.md` existe
   - [ ] `~/.claude/vps-config.json` existe
   - [ ] `~/.claude/cloudflare.json` existe et token valide
   - [ ] Connexion SSH fonctionnelle
   - [ ] `.gitignore` protege les fichiers sensibles

10. **Rapport:**
    ```
    ## Deploy - Installation terminee

    | Composant | Statut |
    |-----------|--------|
    | Skill Deploy | Installe |
    | Module VPS | Present |
    | Module Cloudflare | Present |
    | Connexion SSH | OK |
    | Token Cloudflare | Valide |

    ### Domaines Cloudflare disponibles
    - {liste des domaines}

    ### Prochaines etapes
    - Consulter le SKILL.md pour les workflows de deploiement
    - Tester avec : "Deploie ce projet sur mon VPS"
    ```
