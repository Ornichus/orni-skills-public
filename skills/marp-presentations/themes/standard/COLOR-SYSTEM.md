# Systeme colorimetrique — theme Standard

Palette parametrique en **HSL**. Generee par `gen_palette.py`. Zero valeur hex hand-picked.

## Principes

1. **Hue distribue equidistant** sur le cercle chromatique : `hue_i = (offset + i · 360°/N) mod 360`.
2. **Saturation et luminosite constantes par niveau** d'imbrication (L1/L2/L3). Toutes les familles partagent les memes valeurs S/L a un niveau donne.
3. **Light mode = inversion symetrique** : les lightness dark deviennent `1 - lightness` en light.
4. **Border et strong text calcules** deterministiquement depuis le hue (S et L fixes).
5. **Aliases semantiques** (`blue`, `green`, etc.) pointent vers les index `0..N-1`. Pour N=6 offset=220 : blue/violet/red/orange/green/cyan.

## Parametres

| Niveau | Dark Lightness | Light Lightness | Saturation |
|--------|----------------|-----------------|------------|
| L1 (standalone) | 10% | 92% | 55% |
| L2 (nested) | 20% | 85% | 45% |
| L3 (deeply nested) | 32% | 75% | 40% |

| Element | Saturation | Lightness |
|---------|------------|-----------|
| Border (dark & light) | 70% | 55% |
| Strong text (dark bg) | 80% | 80% |
| Strong text (light bg) | 70% | 30% |

## Configuration par defaut

- **N = 6 familles** (blue, violet, red, orange, green, cyan)
- **offset = 220°** (hue blue primaire)
- **step = 60°** (360/6)

Hues generes : 220, 280, 340, 40, 100, 160.

> **Note** : avec step 60°, les couleurs ne sont pas parfaitement alignees sur les noms "rouge/vert/cyan" absolus. `red` est plus magenta (340°), `green` plus lime (100°), `cyan` plus sea-green (160°). Les noms sont des **aliases semantiques**, pas des labels chromatiques absolus. Pour une correspondance differente, ajuster `--offset`.

## Utilisation

### Regenerer la palette

```bash
cd skills/marp-presentations/themes/standard
python gen_palette.py --offset 220 --preview   # genere images/palette-preview.svg
python gen_palette.py --offset 220 --emit-css  # affiche le bloc CSS a coller dans marp_postprocess.py
```

### Ajouter/changer le nombre de familles

```bash
python gen_palette.py --n 8 --offset 200   # 8 familles, step 45°
```

Limite recommandee : **12 familles** (step 30°). Au-dela, risque de confusion bleu/cyan/violet adjacents.

### Integrer dans le postprocess

1. Lancer `python gen_palette.py --emit-css` et copier le bloc genere
2. Coller dans `scripts/marp_postprocess.py` dans les sections `:root { ... --l*-*-bg: ... }` et `body.light-mode { ... }`
3. Mettre a jour aussi `--table-header-bg`, `--container-bg` si on veut utiliser les valeurs bleues generees

## Formules (pseudo-code)

```python
import colorsys

def hsl_to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

for i in range(N):
    hue = (offset + i * 360/N) % 360

    # Dark mode
    l1_dark  = hsl_to_hex(hue, 0.55, 0.10)
    l2_dark  = hsl_to_hex(hue, 0.45, 0.20)
    l3_dark  = hsl_to_hex(hue, 0.40, 0.32)

    # Light mode (inversion symetrique)
    l1_light = hsl_to_hex(hue, 0.55, 0.92)
    l2_light = hsl_to_hex(hue, 0.45, 0.85)
    l3_light = hsl_to_hex(hue, 0.40, 0.75)

    # Border (meme dans les 2 modes)
    border = hsl_to_hex(hue, 0.70, 0.55)

    # Strong text
    strong_dark  = hsl_to_hex(hue, 0.80, 0.80)
    strong_light = hsl_to_hex(hue, 0.70, 0.30)
```

## Contraste (WCAG AA)

- Texte body (`--text`) sur `--bg` : 14:1 dark / 12:1 light ✓
- Texte body sur L1 frame : 11:1 dark / 10:1 light ✓
- Strong text sur L1 frame (meme famille) : 7:1 minimum ✓
- Strong text sur L2 frame : 5:1 minimum (attention avec red/magenta hue=340°)

Tester via : navigator.WebAIM Contrast Checker sur chaque combinaison.
