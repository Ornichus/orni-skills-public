---
description: 'Initialise le module fal-image-gen (MCP generation d images) dans le projet courant'
---

# /orni-init-fal - Initialisation du module Fal Image Gen

Installe et configure le MCP server fal-image-gen pour la generation d'images via fal.ai.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que `node` est disponible (`node --version`)
   - Definir `{MCP_FAL}` = `<VOTRE_DOSSIER_MCP>/fal-image-gen`
   - Verifier que `{MCP_FAL}` existe
   - Verifier si le module est deja installe :
     - Marqueur projet : `.claude/skills/fal-image-gen/SKILL.md`
     - Marqueur global : config `fal-image-gen` dans `~/.claude/settings.json`
   - Si deja installe : avertir et demander confirmation

4. **Build du MCP server:**
   - Si `{MCP_FAL}/node_modules/` absent : `npm install` dans `{MCP_FAL}`
   - Si `{MCP_FAL}/dist/index.js` absent : `npm run build` dans `{MCP_FAL}`

5. **Configurer le MCP dans Claude Code:**
   - Lire `~/.claude/settings.json`
   - Ajouter (ou mettre a jour) dans `mcpServers` :
     ```json
     "fal-image-gen": {
       "command": "node",
       "args": ["<VOTRE_DOSSIER_MCP>/fal-image-gen/dist/index.js"],
       "env": {
         "FAL_KEY": "<cle>",
         "FAL_OUTPUT_DIR": "<VOTRE_DOSSIER_MCP>/fal-image-gen/generated-images"
       }
     }
     ```
   - **Cle API FAL_KEY :**
     - Verifier si `FAL_KEY` est deja dans la config existante
     - Si absent : demander la cle a l'utilisateur
     - Indiquer : "Obtenez votre cle sur https://fal.ai/dashboard/keys"
   - Sauvegarder `~/.claude/settings.json`

6. **Copier le SKILL.md dans le projet:**
   ```bash
   mkdir -p "{PROJET}/.claude/skills/fal-image-gen"
   cp "{ORNI}/skills/fal-image-gen/SKILL.md" "{PROJET}/.claude/skills/fal-image-gen/SKILL.md"
   ```

7. **Mettre a jour le manifeste de versioning:**
   - Lire/creer `.claude/orni-manifest.json`
   - Ajouter l'entree :
     ```json
     "FAL": {
       "version": "1.0.0",
       "installed_at": "<ISO 8601>",
       "updated_at": "<ISO 8601>",
       "source": "skills/fal-image-gen/SKILL.md"
     }
     ```

8. **Verification:**
   - [ ] `{MCP_FAL}/dist/index.js` existe
   - [ ] `fal-image-gen` present dans `~/.claude/settings.json` mcpServers
   - [ ] `FAL_KEY` configure (non vide)
   - [ ] `.claude/skills/fal-image-gen/SKILL.md` existe dans le projet

9. **Rapport:**
   - Module installe avec succes
   - Rappeler : "Redemarrez Claude Code pour activer le MCP server"
   - Tools disponibles : `generate_image`, `list_models`, `list_ratios`
