# Fal Image Gen - MCP Server

> **Version**: 1.0.0 | Serveur MCP pour la generation d'images via fal.ai

Serveur MCP standalone qui expose 3 tools aux agents Claude Code pour generer des images via l'API fal.ai.

---

## 1. Tools exposes

### generate_image
Genere une image avec les parametres suivants :
- `prompt` (string, requis) — Description de l'image
- `model` (enum, opt) — `flux` (defaut), `seedream`, `nano-banana`
- `aspect_ratio` (string, opt) — Ex: "16:9", "1:1" (defaut: "1:1")
- `quality` (enum, opt) — `fast`, `standard` (defaut), `high` (Flux uniquement)
- `num_images` (int 1-6, opt) — Nombre d'images (defaut: 1, max selon modele)
- `seed` (int, opt) — Seed pour reproductibilite
- `output_format` (enum, opt) — `png` (defaut), `jpeg`, `webp`

Retourne les chemins locaux des images generees.

### list_models
Liste les modeles disponibles avec capacites, ratios supportes et couts.

### list_ratios
Liste les aspect ratios supportes par un modele donne avec dimensions pixels.

---

## 2. Modeles supportes

| Modele | Endpoint fal.ai | Max images | Particularites | Cout |
|--------|----------------|------------|----------------|------|
| `flux` (defaut) | `fal-ai/flux/dev` | 1 | Quality levels, guidance scale | $0.05/megapixel |
| `seedream` | `fal-ai/seedream-v4/text-to-image` | 6 | Rapide, multi-variations | $0.03/image |
| `nano-banana` | `fal-ai/nano-banana-pro` | 4 | 11 aspect ratios, resolution tiers | $0.15-0.30/image |

---

## 3. Aspect ratios

| Ratio | Pixels |
|-------|--------|
| 1:1 | 1024x1024 |
| 16:9 | 1344x768 |
| 9:16 | 768x1344 |
| 4:3 | 1152x864 |
| 3:4 | 864x1152 |
| 3:2 | 1216x832 |
| 2:3 | 832x1216 |
| 21:9 | 1536x640 (nano-banana only) |
| 9:21 | 640x1536 (nano-banana only) |
| 4:5 | 896x1088 (nano-banana only) |
| 5:4 | 1088x896 (nano-banana only) |

---

## 4. Configuration

### Emplacement du serveur
`<VOTRE_DOSSIER_MCP>/fal-image-gen/`

### Config MCP (dans ~/.claude/settings.json)
```json
{
  "mcpServers": {
    "fal-image-gen": {
      "command": "node",
      "args": ["<VOTRE_DOSSIER_MCP>/fal-image-gen/dist/index.js"],
      "env": {
        "FAL_KEY": "<cle-api-fal.ai>",
        "FAL_OUTPUT_DIR": "<VOTRE_DOSSIER_MCP>/fal-image-gen/generated-images"
      }
    }
  }
}
```

### Dependances
- Node.js (pour executer le serveur)
- `@fal-ai/client`, `@modelcontextprotocol/sdk`, `zod` (installees via npm)

### Cle API
- Obtenir sur https://fal.ai/dashboard/keys
- Stockee dans `FAL_KEY` dans la config MCP

---

## 5. Maintenance

### Build
```bash
cd <VOTRE_DOSSIER_MCP>/fal-image-gen
npm install
npm run build
```

### Dossier de sortie
Les images sont sauvegardees dans `FAL_OUTPUT_DIR` (defaut: `./generated-images`).
