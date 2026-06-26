---
description: 'Met a jour le module fal-image-gen dans le projet courant'
---

# /orni-update-fal - Mise a jour du module Fal Image Gen

Met a jour le MCP server fal-image-gen et le SKILL.md du projet.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` -> `{ORNI}`

3. **Pre-vol:**
   - Definir `{MCP_FAL}` = `<VOTRE_DOSSIER_MCP>/fal-image-gen`
   - Verifier que le module est installe :
     - `.claude/skills/fal-image-gen/SKILL.md` OU config MCP dans settings.json
   - Si NON installe : avertir et suggerer `/orni-init-fal`

4. **Rebuild du MCP server:**
   ```bash
   cd "{MCP_FAL}"
   npm install
   npm run build
   ```

5. **Mettre a jour le SKILL.md:**
   ```bash
   cp "{ORNI}/skills/fal-image-gen/SKILL.md" "{PROJET}/.claude/skills/fal-image-gen/SKILL.md"
   ```

6. **Verifier la config MCP:**
   - Lire `~/.claude/settings.json`
   - Si la config `fal-image-gen` est presente : verifier que le chemin pointe bien vers `{MCP_FAL}/dist/index.js`
   - Si absente : la recreer (comme dans init)

7. **Mettre a jour le manifeste:**
   - Lire `.claude/orni-manifest.json`
   - Mettre a jour `version` et `updated_at` pour le module FAL
   - Conserver `installed_at` d'origine

8. **Rapport:**
   - MCP server rebuild
   - SKILL.md mis a jour
   - Rappeler : "Redemarrez Claude Code si le MCP etait deja actif"
