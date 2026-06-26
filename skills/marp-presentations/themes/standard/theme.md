# Theme : Standard

> Fond sombre / clair symetrique — Palette HSL parametrique — 3 niveaux d'imbrication — Neon subtil

## Identite

| Propriete | Valeur |
|-----------|--------|
| **Nom** | `standard` |
| **Fond dark** | `#0f172a` |
| **Fond light** | `#f1f5f9` |
| **Style** | L1/L2/L3 imbrication, glow subtil, dark/light toggle |
| **Ton** | Technique, professionnel, futuriste clean |

---

## Source de verite : `gen_palette.py`

**Ne pas hand-pick de hex.** La palette est generee mathematiquement :

```bash
cd themes/standard
python gen_palette.py --offset 220 --emit-css   # stdout : bloc CSS a coller
python gen_palette.py --preview                  # images/palette-preview.svg
```

**Parametres** : N=6 familles, offset hue 220°, step 60°.
Cf. `COLOR-SYSTEM.md` pour la spec complete.

### Families & hues

| Index | Alias | Hue | Rendu approximatif |
|-------|-------|-----|--------------------|
| 0 | `blue` | 220° | Bleu |
| 1 | `violet` | 280° | Violet |
| 2 | `red` | 340° | Rouge-rose |
| 3 | `orange` | 40° | Orange |
| 4 | `green` | 100° | Vert-lime |
| 5 | `cyan` | 160° | Cyan-teal |

### Valeurs actuelles (dark / light)

| Variable | Dark | Light | Usage |
|----------|------|-------|-------|
| `--bg` | `#0f172a` | `#f1f5f9` | Fond slide |
| `--text` | `#e2e8f0` | `#1e293b` | Corps |
| `--title` | `#a3bef4` | `#163a82` | Titres H2 |
| `--l1-blue-bg` | `#0b1427` | `#dfe6f5` | Cadre L1 bleu |
| `--l2-blue-bg` | `#1c2b49` | `#c7d3e9` | Cadre L2 bleu |
| `--l3-blue-bg` | `#304672` | `#a5b6d8` | Cadre L3 bleu |
| `--blue-border` | `#3b71dc` | `#3b71dc` | Bordure bleu |
| `--blue-strong` | `#a3bef4` | `#163a82` | Texte strong dans cadre bleu |

**Chaque famille (green/red/orange/violet/cyan) suit la meme logique.**

---

## Injection CSS

**Le CSS complet du theme est injecte par `scripts/marp_postprocess.py` apres le rendu Marp**, PAS dans le frontmatter du deck. Raison : Marpit scope les selecteurs `:root` et `body.*` dans `section { }`, ce qui casse les variables CSS et le toggle dark/light.

### Frontmatter minimal pour un deck

```yaml
---
marp: true
theme: default
paginate: true
transition: fade
backgroundColor: #0f172a
color: #e2e8f0
---
```

**Ne rien ajouter de plus**. Le reste vient de `marp_postprocess.py`.

---

## Snippets du theme

### Info Box (L1)

```html
<div class="box la l1-blue">
<strong>Info</strong> — Neutre, informatif.
</div>
```

Famille : `l1-blue` / `l1-green` / `l1-red` / `l1-orange` / `l1-violet` / `l1-cyan`.
Option : `la` ajoute un border-left 4px (accent lateral).

### KPI Card (L1 centree)

```html
<div class="box l1-blue" style="padding: 0.8rem 1.2rem; text-align: center; min-width: 130px;">
  <div style="font-size: 1.8em; font-weight: 800; text-shadow: 0 0 12px rgba(96,165,250,0.4);">7 200+</div>
  <div style="font-size: 0.75em; opacity: 0.75;">Videos indexees</div>
</div>
```

Group de KPI : wrapper `<div style="display: flex; gap: 0.8rem; justify-content: center;">`.

### Step (L2 pastille + L1 barre)

```html
<div style="display: flex; align-items: center; gap: 0.7rem;">
  <div class="box l2-blue" style="padding: 0.35rem 0.7rem; min-width: 34px; text-align: center; font-weight: 800;">1</div>
  <div class="box la l1-blue" style="flex: 1;"><strong>Decouverte</strong> — Ajout de sources</div>
</div>
```

### Card 3 colonnes

```html
<div style="display: flex; gap: 0.8rem;">
  <div class="box l1-red" style="flex: 1; border-top: 3px solid var(--red-border); padding: 0.7rem;">
    <div style="font-weight: 800;">Titre</div>
    <div style="font-size: 0.82em; opacity: 0.85;">Sous-titre</div>
    <div style="font-size: 0.72em; opacity: 0.75;">Description</div>
  </div>
  <div class="box l1-blue" ...>...</div>
  <div class="box l1-green" ...>...</div>
</div>
```

### Comparatif 2 colonnes

```html
<div style="display: flex; gap: 1rem;">
  <div class="box la l1-green" style="flex: 1; padding: 0.8rem;">
    <div style="font-weight: 700;">Champion</div>
    <div style="font-size: 1.8em; font-weight: 800;">82.4%</div>
  </div>
  <div class="box la l1-red" style="flex: 1; padding: 0.8rem;">
    ...
  </div>
</div>
```

### Tables — coloration gradient (rank-*)

**Pattern A — ligne entiere** :
```html
<table style="width: 100%;">
<thead><tr><th>Modele</th><th>Coverage</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td class="rank-top">GPT-5.4</td><td class="rank-top">82.4%</td><td class="rank-top">Champion</td></tr>
<tr><td class="rank-mid">Gemini</td><td class="rank-mid">70.6%</td><td class="rank-mid">Backup</td></tr>
<tr><td class="rank-bottom">DeepSeek</td><td class="rank-bottom">20.6%</td><td class="rank-bottom">Faible</td></tr>
</tbody>
</table>
```

**Pattern B — par cellule** : coloration par colonne independamment.

Classes : `rank-top`, `rank-good`, `rank-mid`, `rank-low`, `rank-bottom`.

### Imbrication 3 niveaux

```html
<div class="box l1-blue" style="padding: 1rem;">
  Level 1
  <div class="box l2-blue" style="padding: 0.7rem;">
    Level 2
    <div class="box l3-blue" style="padding: 0.5rem;">
      Level 3
    </div>
  </div>
</div>
```

### Slide compacte (vertical center)

```markdown
<!-- _class: compact -->

## Titre

Contenu centre verticalement quand il est sparse.
```

---

## Diagrammes Mermaid

Les SVG sont **derives de la palette HSL** par `gen_charte_diagrams.py`. Pour un nouveau diagramme :

1. Ajouter l'entree dans le dict `DIAGRAMS` (ou utiliser `mermaid_init()` pour les types gantt/pie/etc)
2. Referencer en snippet dans le theme.md
3. Regenerer : `python gen_charte_diagrams.py`

Cf. `charte-graphique.md` slides Pattern 1-5 + Mermaid types pour exemples complets.

---

## Charte graphique

Le deck `charte-graphique.md` (33 slides) est la **source de verite visuelle** du theme. A consulter avant tout doute. Regenerer les screenshots apres modification :

```bash
python screenshot_slides.py both   # dark + light
# Sortie : _screenshots/slide-NN.png + slide-NN-light.png
```
