# Marp Presentations Skill

> **Version** : 5.0.0 | Systeme colorimetrique HSL parametrique + auto-fit + 14 types diagrammes

---

## 1. Architecture

```
skills/marp-presentations/
├── SKILL.md                              # Ce fichier (workflow, regles, structure)
├── charte-graphique-template.md          # Reference de structure pour creer un theme
├── themes/
│   ├── standard/
│   │   ├── theme.md                      # CSS frontmatter + palette + snippets du theme
│   │   ├── charte-graphique.md           # Deck showcase/test visuel complet (33 slides)
│   │   ├── COLOR-SYSTEM.md               # Spec du systeme colorimetrique HSL
│   │   ├── gen_palette.py                # Generateur de palette HSL parametrique
│   │   ├── gen_charte_diagrams.py        # Generateur des SVG Mermaid (derives de la palette)
│   │   ├── screenshot_slides.py          # Screenshot Playwright par slide (dark/light/both)
│   │   └── images/                       # SVG Mermaid + palette preview + snake statique
│   └── {autre-theme}/
│       └── (meme structure)
└── scripts/
    ├── validate_marp.py                  # Validation Playwright (overflow + contraste WCAG)
    ├── fix_svg_sizes.py                  # Fix <br> non-autoclosing + width/height depuis viewBox
    ├── marp_postprocess.py               # Injection du theme CSS + Sommaire + Dark/Light toggle
    └── auto_fit_slides.py                # Mesure overflow + reduit font-size par dichotomie
```

### Themes disponibles

| Theme | Description | Fond dark / light |
|-------|-------------|-------------------|
| `standard` | Neon subtil, 3 niveaux d'imbrication, palette HSL parametrique | `#0f172a` / `#f1f5f9` |

**Theme par defaut : `standard`**

---

## 2. Workflow de generation

```
Comprendre → Charger theme → Planifier → Generer → Render → Postprocess → Auto-fit → Valider → Ouvrir
```

1. **Comprendre** — sujet, audience, ton, donnees source
2. **Charger le theme** — lire `themes/{nom}/theme.md` (defaut : `standard`)
3. **Planifier** — plan des slides (titre, type de contenu, transition)
4. **Generer** — fichier `.md` dans `docs/slides/{YYYY-MM-DD}_{slug}.md`
5. **Render HTML** :
   ```bash
   marp docs/slides/{fichier}.md --html --bespoke.transition -o docs/slides/{fichier}.html
   ```
6. **Postprocess** (injection theme CSS + toggle dark/light + sommaire cliquable) :
   ```bash
   python docs/scripts/marp_postprocess.py docs/slides/{fichier}.html
   ```
7. **Auto-fit** (detection + fix automatique overflow par slide) :
   ```bash
   python docs/scripts/auto_fit_slides.py docs/slides/{fichier}.html
   ```
8. **Valider visuellement** — ouvrir en navigateur (Agent Browser recommande pour audit visuel)
9. **Ouvrir** :
   ```bash
   start docs/slides/{fichier}.html
   ```

**Ne JAMAIS livrer sans avoir execute postprocess + auto-fit.**

### Creer un nouveau theme

1. **Definir l'identite** — nom, fond (dark/light), ton
2. **Creer `themes/{nom}/gen_palette.py`** — copier depuis `themes/standard/gen_palette.py`, ajuster `offset` et eventuellement N
3. **Generer la palette CSS** :
   ```bash
   python themes/{nom}/gen_palette.py --offset {angle} --emit-css
   ```
4. **Integrer le CSS dans `scripts/marp_postprocess.py`** (ou creer un postprocess theme-specifique)
5. **Creer `themes/{nom}/theme.md`** — documentation du theme (palette, snippets, regles)
6. **Generer `themes/{nom}/charte-graphique.md`** — deck showcase (cf. `themes/standard/charte-graphique.md` comme reference)
7. **Regenerer SVG Mermaid** :
   ```bash
   python themes/{nom}/gen_charte_diagrams.py
   ```
8. **Iterer visuellement** — Agent Browser + user review

---

## 3. Systeme colorimetrique HSL (source unique de verite)

La palette est **generee mathematiquement** via `themes/{nom}/gen_palette.py`. **Aucun hex hand-picked** dans le projet.

### Principes

- **Hue equidistant** : `hue_i = (offset + i × 360°/N) mod 360` pour N familles
- **Saturation et luminosite constantes par niveau** d'imbrication (L1/L2/L3)
- **Light mode = inversion symetrique** des luminosites
- **Border + strong text calcules** depuis le hue (S=70%/L=55% pour border, etc.)

### Parametres par defaut (theme standard)

| Niveau | Lightness dark | Lightness light | Saturation |
|--------|----------------|-----------------|------------|
| L1 (standalone) | 10% | 92% | 55% |
| L2 (nested) | 20% | 85% | 45% |
| L3 (deeply nested) | 32% | 75% | 40% |

- **N = 6 familles** (blue, violet, red, orange, green, cyan), offset 220°
- **Max recommande : 12 familles** (step 30°)

### Utilisation dans un deck

- Utiliser les classes CSS `.l1-{couleur}`, `.l2-{couleur}`, `.l3-{couleur}` (jamais de hex hand-picked)
- Pour les Mermaid : utiliser `classDef` derives de la palette (voir `gen_charte_diagrams.py` comme template)
- Pour regenerer la palette (N, offset differents) : `python gen_palette.py --n 8 --offset 200 --emit-css` puis coller le bloc dans `marp_postprocess.py`

---

## 4. Systeme 3 niveaux d'imbrication

| Niveau | Usage | Classe CSS |
|--------|-------|------------|
| **L1** | Cadre standalone (info box, KPI, card, step bar, sans imbrication) | `.l1-blue`, `.l1-green`, ... |
| **L2** | Element imbrique dans un L1 (pastille, badge, node interne subgraph) | `.l2-*` |
| **L3** | Sous-element imbrique dans un L2 (tag, detail) | `.l3-*` |

**Regle** : **toujours** utiliser les classes, jamais de styles inline. Le `strong` dans un cadre prend automatiquement la couleur de la famille (plus claire en dark, plus foncee en light).

**Classe auxiliaire** :
- `.box` — padding + border-radius de base (toujours combiner avec `.l1-*` / `.l2-*` / `.l3-*`)
- `.box.la` — ajoute un `border-left-width: 4px` pour l'accent lateral
- `.compact` sur `<section>` — centre verticalement le contenu (pour slides sparse)

---

## 5. Regles critiques

### Overflow — auto-detection

**Le script `auto_fit_slides.py` mesure et fixe automatiquement** les slides qui depassent 720px :
- Dichotomie sur `font-size` entre 18px et 26px pour chaque slide en overflow
- Injecte un override CSS par slide (`section:nth-of-type(N) { font-size: Xpx !important; }`)
- Report console : "Slide N [+XXpx]: YYpx"

**Regle d'or** : lancer `auto_fit_slides.py` apres `marp_postprocess.py`.
Si un slide est force a 18px (minimum), prevoir de le splitter manuellement.

### Contraste

- Script `validate_marp.py` mesure le ratio WCAG pour chaque element texte
- Exit 1 si overflow ou contraste < 3:1
- Complement de l'auto-fit (focus sur la lisibilite, pas la taille)

### Transitions

| Contexte | Transition | Directive |
|----------|-----------|-----------|
| **Standard** | `fade` | `transition: fade` (frontmatter global) |
| **Donnees / resultats** | `flip` | `<!-- transition: flip -->` (par slide) |
| **Section break** | `fade-out` | `<!-- transition: fade-out -->` (par slide) |

**Flag CLI obligatoire** : `--bespoke.transition`

### Tableaux

**Colonnes** : la 1ere colonne est **left-align** (labels), les autres sont **center** (valeurs numeriques).
**Largeur** : auto (se contracte au contenu), max 100%, centre horizontalement.

**Coloration gradient** (comparatifs) :

| Classe | Couleur | Usage |
|--------|---------|-------|
| `rank-top` | vert (L2 green dark / L2 green light) | Meilleur |
| `rank-good` | vert-jaune | Bon |
| `rank-mid` | jaune | Moyen |
| `rank-low` | orange | Faible |
| `rank-bottom` | rouge | Pire |

**Deux patterns** :
- **Meilleur element** : classes sur la ligne entiere
- **Meilleures donnees** : classes par cellule (chaque colonne son propre meilleur)

**IMPORTANT** : tables avec rank-* doivent etre en HTML `<table>` (pas Markdown) — les classes CSS sur `<td>` n'existent pas en Markdown.

### Dark/Light toggle

- Injecte automatiquement par `marp_postprocess.py`
- Bouton top-right "Mode clair" / "Mode sombre"
- Raccourci clavier `D`
- Implementation : toggle `body.light-mode` class → toutes les variables CSS s'inversent (--bg, --text, --l1-*-bg, etc.)

### Sommaire cliquable

- Injecte automatiquement par `marp_postprocess.py`
- Bouton top-left "Sommaire" → slide 2 (ou modifier `HOME_HASH`)
- Raccourci clavier `H`
- Rend les lignes de table cliquables (quand la cellule contient juste un numero de page)

---

## 6. Diagrammes Mermaid

**Toujours SVG**, jamais PNG. Les couleurs sont **derivees automatiquement** de `gen_palette.py` (aucun hex hand-picked).

### Arbre de decision — choix du pattern

| Situation | Pattern | Keyword |
|-----------|---------|---------|
| Groupes logiques clairs | **Subgraph zones** | `graph LR` + `subgraph A[1 NOM]` |
| 3-6 elements simples | **LR lineaire** | `graph LR` + fleches directes |
| Fan-out / fan-in / diamond | **LR branching** | `graph LR` + multiples fleches (2D auto) |
| Flux dense vertical (7+) | **TB vertical** | `graph TB` |
| Flux horizontal tres long (10+) | **LR wrap (snake)** | SVG statique (Mermaid ne sait pas faire) |
| Boucle feedback | **Feedback externe** | Node `LOOP` hors flux principal + `-.->` |

**Anti-pattern** : boucle dans flux principal → Mermaid reordonne les nodes, casse l'ordre visuel.

### Autres types Mermaid supportes

| Type | Usage | Commande Mermaid |
|------|-------|------------------|
| `gantt` | Roadmap projet (dates + sections + done/active/crit) | `gantt` + `dateFormat` |
| `timeline` | Chronologie historique | `timeline` |
| `sequenceDiagram` | Interactions acteurs (sync/async) | `sequenceDiagram` |
| `journey` | Parcours utilisateur (score satisfaction) | `journey` |
| `pie` | Repartition / proportions | `pie showData` |
| `stateDiagram-v2` | Machine a etats + transitions | `stateDiagram-v2` |
| `erDiagram` | Schema BDD (entites + relations) | `erDiagram` |
| `quadrantChart` | Matrice 2x2 (priorisation impact/effort) | `quadrantChart` |

**Theming** : ces types utilisent `mermaid_init()` dans `gen_charte_diagrams.py` qui injecte `themeCSS` + `themeVariables`. Pour pie/gantt/quadrant, `post_process_svg()` applique les fills directement sur les elements (Mermaid themeVariables peu fiable pour ces types).

### Embed dans un deck

```markdown
![h:380](./images/mon-diagramme.svg)
```

- Toujours `h:` (hauteur) pour eviter que l'image deborde
- Chemin relatif depuis le `.md` du deck

---

## 7. Selection du theme

Quand l'utilisateur invoque `/marp-slides` :

1. **Theme explicite** : `/marp-slides --theme corporate "Mon sujet"` → charger `themes/corporate/theme.md`
2. **Theme par defaut** : si non specifie → `standard`
3. **Theme inexistant** : informer l'utilisateur des themes disponibles (lister `themes/*/theme.md`)

Le fichier `theme.md` contient :
- La palette (hex de reference, generee par `gen_palette.py`)
- Les snippets HTML pour chaque type d'element
- Les regles specifiques du theme

---

## 8. Scripts

### `scripts/validate_marp.py`

```bash
python docs/scripts/validate_marp.py docs/slides/mon-deck.md
```

Playwright headless 1280x720. Mesure `scrollHeight` vs `clientHeight` + ratio contraste WCAG. Exit 1 si probleme, 0 si ALL CLEAR.

### `scripts/marp_postprocess.py`

```bash
python docs/scripts/marp_postprocess.py docs/slides/mon-deck.html
```

**Obligatoire apres `marp`**. Injecte :
- Bloc CSS theme complet (variables HSL, dark + light, systeme L1/L2/L3, tables, boxes, fenetre compact)
- Bouton Sommaire (top-left) + raccourci H
- Bouton Dark/Light toggle (top-right) + raccourci D
- Legende cliquable pour tables de sommaire

### `scripts/auto_fit_slides.py`

```bash
python docs/scripts/auto_fit_slides.py docs/slides/mon-deck.html
```

**Recommande apres `marp_postprocess.py`**. Mesure chaque slide via Playwright, ajuste le font-size par dichotomie si overflow. Injecte un `<style id="auto-fit-overrides">` avec overrides par slide.

### `scripts/fix_svg_sizes.py`

```bash
python docs/scripts/fix_svg_sizes.py images/
```

Utility : fix `<br>` non auto-fermants + injecte width/height depuis viewBox. Utile pour les SVG generes par Mermaid. Appele automatiquement par `gen_charte_diagrams.py`.

### `themes/standard/gen_palette.py`

```bash
python themes/standard/gen_palette.py --offset 220 --emit-css          # stdout : bloc CSS
python themes/standard/gen_palette.py --n 8 --offset 200 --preview     # genere images/palette-preview.svg
```

Source unique de verite pour la palette. Modifier les constantes `DARK_LIGHTNESS`, `LIGHT_LIGHTNESS`, `SATURATION` dans ce fichier pour rafraichir tout le systeme.

### `themes/standard/gen_charte_diagrams.py`

```bash
python themes/standard/gen_charte_diagrams.py
```

Regenere tous les SVG Mermaid + le snake statique + la palette preview. Importe `gen_palette.py` comme source de verite pour les couleurs.

---

## 9. Export

```bash
# HTML avec transitions (requis)
marp docs/slides/{f}.md --html --bespoke.transition -o docs/slides/{f}.html
python docs/scripts/marp_postprocess.py docs/slides/{f}.html
python docs/scripts/auto_fit_slides.py docs/slides/{f}.html

# PDF
marp docs/slides/{f}.md --pdf -o docs/slides/{f}.pdf

# PowerPoint
marp docs/slides/{f}.md --pptx -o docs/slides/{f}.pptx

# Serveur live
marp -s docs/slides/
```

---

## 10. Validation visuelle — Agent Browser

**Politique CLAUDE.md** : pour tout audit visuel, utiliser **Agent Browser** (Claude in Chrome) en priorite.
- Outils `mcp__claude-in-chrome__*` : `navigate`, `computer` (screenshot + click), `javascript_tool`, `read_page`
- Playwright MCP Docker en **fallback** uniquement si Agent Browser indisponible (demander a l'utilisateur de reconnecter)

Pour servir les slides au navigateur, lancer un serveur HTTP local :
```bash
cd docs/slides && python -m http.server 8765
```
Puis naviguer sur `http://localhost:8765/{deck}.html#{slideNumber}`.

---

## 11. Changelog v5.0

- **Systeme colorimetrique HSL parametrique** via `gen_palette.py` (remplace les hex hand-picked)
- **3 niveaux d'imbrication** (`.l1-*`, `.l2-*`, `.l3-*`) avec couleurs derivees
- **CSS theme injecte post-Marp** via `marp_postprocess.py` (bypass scoping Marpit de `:root` et `body.*`)
- **Auto-fit slides** : detection + fix automatique d'overflow via dichotomie font-size
- **Toggle Dark/Light fonctionnel** via `body.light-mode` class + variables CSS
- **8 types Mermaid supplementaires** (gantt/timeline/sequence/journey/pie/state/er/quadrant) themees HSL
- **Snake pattern** SVG statique genere depuis la palette (Mermaid incapable de rendre snake)
- **Tables fix** : `display: table` force + `width: auto` + centrage cellules (sauf 1ere col)
- **Spacing hierarchique** : H1 > H2 > H3 > p en margins decroissantes
- **Arbre de decision Mermaid** : 5 patterns + anti-pattern (subgraph zones est prefere, plus de regle "pas de subgraph")
- **Agent Browser** comme validation visuelle par defaut
