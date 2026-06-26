---
description: 'Initialise le module Cloudflare Management dans le projet courant'
---

# /orni-init-cf - Initialiser Cloudflare Management

Configure l'acces a l'API Cloudflare pour le projet courant.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que `{ORNI}/skills/cloudflare/SKILL.md` existe
   - Verifier si le module est deja installe : `.claude/skills/cloudflare/SKILL.md` dans le projet courant
   - Si deja installe : AVERTIR et demander confirmation

4. **Verifier les prerequis globaux:**
   - `~/.claude/cloudflare.json` existe ? Si non : guider la creation interactive
   - Le fichier doit contenir : `api_token`, `account_id`, `default_zone`
   - Guide utilisateur : "Dashboard → My Profile → API Tokens → Create Token avec permission 'Edit zone DNS'"
   - Tester l'API :
     ```bash
     CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
     curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
       -H "Authorization: Bearer $CF_TOKEN" | jq '.success'
     ```
   - Si echec : indiquer que le token est invalide ou expire et guider le renouvellement

5. **Installer le module Cloudflare:**
   - Creer `.claude/skills/cloudflare/` dans le projet courant
   - Copier `{ORNI}/skills/cloudflare/SKILL.md`

6. **Verifier que `.gitignore` protege les secrets:**
   - Si le projet a un `.gitignore`, verifier qu'il contient `cloudflare.json`
   - Sinon : avertir l'utilisateur

7. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (le creer s'il n'existe pas)
   - Extraire la version depuis `{ORNI}/skills/cloudflare/SKILL.md` (pattern `**Version**: X.Y.Z`)
   - Ajouter/mettre a jour l'entree du module CF :
     ```json
     {
       "modules": {
         "CF": {
           "version": "<version extraite>",
           "installed_at": "<date ISO 8601 courante>",
           "updated_at": "<date ISO 8601 courante>",
           "source": "skills/cloudflare/SKILL.md"
         }
       }
     }
     ```

8. **Verification:**
   - [ ] `.claude/skills/cloudflare/SKILL.md` existe dans le projet
   - [ ] `~/.claude/cloudflare.json` existe et contient les 3 champs requis
   - [ ] Token API valide (test curl reussi)
   - [ ] `.gitignore` protege `cloudflare.json`

9. **Rapport:**
   ```
   ## Cloudflare Management - Installation terminee

   | Composant | Statut |
   |-----------|--------|
   | Skill Cloudflare | Installe |
   | Config globale | ~/.claude/cloudflare.json |
   | Token API | {Valide/Invalide} |
   | .gitignore | {Protege/Non protege} |

   ### Acces disponibles
   - **API** : Gestion DNS, Zones, Cache via curl
   - **Zone par defaut** : {default_zone}

   ### Prochaines etapes
   - Tester avec : "Liste les records DNS de mon domaine"
   - Consulter le SKILL.md pour les commandes disponibles
   ```
