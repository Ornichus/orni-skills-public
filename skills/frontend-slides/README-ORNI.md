# frontend-slides — integration Orni-skills

> Skill **upstream** : [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) (MIT)
> **Auteure originale** : @zarazhangrui (1.3M+ vues sur X — voir video YouTube de RoboNuggets)
> **Version Orni** : 1.0.0

---

## Pourquoi ce skill dans Orni

Generation de decks **HTML one-shot ultra-stylises**. Cas d'usage : pitch decks premium, brand mockups, decks one-off avec wow factor. Pour le "skeleton legacy" reproductible, voir le skill `marp-presentations`.

## Choix Marp vs Frontend Slides

| Critere | `marp-presentations` (`/marp-slides`) | `frontend-slides` (`/frontend-slides`) |
|---------|---------------------------------------|----------------------------------------|
| **Source** | Markdown + frontmatter Marp | HTML one-shot LLM |
| **Output** | HTML + PDF + PPTX | HTML (+ PDF via Playwright) |
| **Tokens output** | ~2-5k / deck (snippets reutilises) | ~30-80k / deck (HTML brut) |
| **Reproductibilite** | Deterministe (palette HSL parametrique) | Drift LLM stochastique |
| **Brand fidelity** | Theme par projet | Pixel-perfect par deck |
| **Animations** | Bespoke transitions Marp limitees | Custom CSS riche (pulse, orbit, particles) |
| **Validation** | Playwright + WCAG + auto-fit | Visual humain |
| **Dark/Light** | Toggle natif | Selon preset |
| **Multi-deck cross-cohesion** | Garanti par theme | Pas garanti |
| **Versioning git friendly** | Markdown diffe-able | HTML brut = noise |
| **Cas typique** | Training, weekly review, technical deck | Pitch unique, brand mockup, demo wow |

**Regle de pouce** : si le deck doit etre repete, versionne, exporte multi-format → Marp. Si one-shot premium pour client / brand demo → Frontend Slides.

## Architecture du skill

```
skills/frontend-slides/
|-- SKILL.md                  # Workflow principal (Phases 0-6)
|-- STYLE_PRESETS.md          # 12 styles curates (dark, light, specialty)
|-- viewport-base.css         # CSS responsive obligatoire pour viewport-fit
|-- html-template.md          # Structure HTML + JS + inline editing
|-- animation-patterns.md     # Patterns CSS/JS par feeling
|-- LICENSE                   # MIT (upstream)
|-- README-ORNI.md            # Ce fichier
`-- scripts/
    |-- extract-pptx.py       # PPT->JSON (requires python-pptx)
    |-- deploy.sh             # Deploy Vercel
    `-- export-pdf.sh         # Export PDF via Playwright
```

## Installation dans un projet

Via Orni :

```
/orni-init-fs                       # installe dans le projet courant
/orni-update-fs                     # met a jour depuis le repo Orni-skills
```

Apres install :
- Commande disponible : `/frontend-slides`
- Skill copie dans `.claude/skills/frontend-slides/`
- Manifest `.claude/orni-manifest.json` mis a jour

## Mise a jour upstream

Le skill suit l'upstream `zarazhangrui/frontend-slides`. Pour rafraichir depuis le repo officiel :

```bash
# Dans Orni-skills :
git clone https://github.com/zarazhangrui/frontend-slides.git /tmp/fs-update
cp /tmp/fs-update/{STYLE_PRESETS.md,viewport-base.css,html-template.md,animation-patterns.md,LICENSE} skills/frontend-slides/
cp /tmp/fs-update/scripts/* skills/frontend-slides/scripts/
# Re-merge SKILL.md a la main (preserver le bandeau Version + reference README-ORNI)
```

Bumper `**Version** : X.Y.Z` en haut de SKILL.md et committer.

## Dependencies optionnelles

| Feature | Dependence |
|---------|-----------|
| PPT->HTML conversion | `pip install python-pptx` |
| Deploy Vercel | Node.js + compte Vercel (gratuit) |
| Export PDF | Node.js (Playwright auto-install) |

Aucune dependence pour la generation HTML elle-meme. Single file, runs anywhere.

## Philosophie

3 cle de l'upstream a preserver :

1. **Show, don't tell** — Generer 3 previews visuels apres mood selection, pas demander des choix abstraits
2. **Anti-AI-slop** — Eviter Inter/Roboto, gradients violets generiques, layouts predictibles
3. **Viewport fit non-negotiable** — Chaque slide tient en 100vh, jamais de scroll interne

## Credits

- Skill original : [@zarazhangrui](https://github.com/zarazhangrui)
- Tutoriel video : [RoboNuggets - Claude HTML Slides](https://www.youtube.com/watch?v=t2ELuj2prA0)
- Integration Orni-skills : @Ornichus (avr 2026)
