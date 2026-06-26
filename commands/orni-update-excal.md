---
description: 'Met a jour le module Excalidraw Diagram dans le projet courant'
---

# /orni-update-excal - Mise a jour du module Excalidraw Diagram

Met a jour le skill Excalidraw et le pipeline de rendering.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` -> `{ORNI}`

3. **Pre-vol:**
   - Verifier que le module est installe :
     - `.claude/skills/excal-diagram/SKILL.md`
   - Si NON installe : avertir et suggerer `/orni-init-excal`

4. **Mettre a jour les fichiers du skill:**
   ```bash
   cp "{ORNI}/skills/excal/SKILL.md" ".claude/skills/excal-diagram/SKILL.md"
   cp "{ORNI}/skills/excal/references/element-templates.md" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/json-schema.md" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/pyproject.toml" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/render_excalidraw.py" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/render_template.html" ".claude/skills/excal-diagram/references/"
   ```
   - **color-palette.md** : NE PAS ecraser automatiquement
     - Comparer `references/color-palette.md` local vs source
     - Si different : DEMANDER "Votre palette a ete personnalisee. Ecraser avec la source ?"
     - Si identique : copier silencieusement

5. **Mettre a jour le pipeline Python:**
   ```bash
   cd ".claude/skills/excal-diagram/references"
   uv sync
   ```

6. **Mettre a jour le manifeste:**
   - Lire `.claude/orni-manifest.json`
   - Mettre a jour `version` et `updated_at` pour le module EX
   - Conserver `installed_at` d'origine

7. **Rapport:**
   - SKILL.md mis a jour
   - References mises a jour (palette: ecrasee / conservee)
   - Pipeline Python synchronise
