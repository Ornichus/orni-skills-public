---
description: 'Initialise le module Excalidraw Diagram dans le projet courant'
---

# /orni-init-excal - Initialisation du module Excalidraw Diagram

Installe le skill de generation de diagrammes Excalidraw avec validation visuelle.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin

3. **Pre-vol:**
   - Verifier que `{ORNI}` existe
   - Verifier que `{ORNI}/skills/excal/SKILL.md` existe
   - Verifier que `uv` est disponible (`uv --version` ou `python -m uv --version`)
     - Si absent : **auto-installer** via `pip install uv`
     - Si pip absent aussi : ERREUR "Python + pip requis"
     - Apres install, verifier que `uv` fonctionne (tester `uv --version` puis fallback `python -m uv --version`)
     - Si `uv` n'est pas dans le PATH mais `python -m uv` fonctionne : utiliser `python -m uv` comme prefixe pour les commandes uv dans les etapes suivantes
   - Verifier si le module est deja installe :
     - Marqueur : `.claude/skills/excal-diagram/SKILL.md`
   - Si deja installe : avertir et demander confirmation

4. **Installer le skill dans le projet:**
   ```bash
   mkdir -p ".claude/skills/excal-diagram/references"
   cp "{ORNI}/skills/excal/SKILL.md" ".claude/skills/excal-diagram/SKILL.md"
   cp "{ORNI}/skills/excal/references/color-palette.md" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/element-templates.md" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/json-schema.md" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/pyproject.toml" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/render_excalidraw.py" ".claude/skills/excal-diagram/references/"
   cp "{ORNI}/skills/excal/references/render_template.html" ".claude/skills/excal-diagram/references/"
   ```

5. **Setup Python (rendering pipeline):**
   ```bash
   cd ".claude/skills/excal-diagram/references"
   # Utiliser uv ou python -m uv selon ce qui est disponible
   uv sync        # ou: python -m uv sync
   uv run playwright install chromium  # ou: python -m uv run playwright install chromium
   ```

6. **Creer le dossier de sortie:**
   ```bash
   mkdir -p "docs/diagrams"
   ```

7. **Mettre a jour le manifeste de versioning:**
   - Lire/creer `.claude/orni-manifest.json`
   - Ajouter l'entree :
     ```json
     "EX": {
       "version": "1.0.0",
       "installed_at": "<ISO 8601>",
       "updated_at": "<ISO 8601>",
       "source": "skills/excal/SKILL.md"
     }
     ```

8. **Verification:**
   - [ ] `.claude/skills/excal-diagram/SKILL.md` existe
   - [ ] `.claude/skills/excal-diagram/references/render_excalidraw.py` existe
   - [ ] `.claude/skills/excal-diagram/references/render_template.html` existe
   - [ ] `.claude/skills/excal-diagram/references/pyproject.toml` existe
   - [ ] `docs/diagrams/` existe
   - [ ] `uv sync` a reussi (`.claude/skills/excal-diagram/references/.venv/` existe)
   - [ ] Playwright chromium installe

9. **Rapport:**
   - Module installe avec succes
   - Rappeler : "Utilisez 'cree un diagramme pour expliquer X' pour generer un diagramme"
   - Output : `docs/diagrams/`
   - Viewer : Obsidian + plugin Excalidraw ou excalidraw.com
