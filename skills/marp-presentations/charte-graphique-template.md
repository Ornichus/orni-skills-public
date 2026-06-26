# Template Charte Graphique Marp

Ce template definit la structure obligatoire d'une charte graphique.
Chaque nouveau theme DOIT produire un deck `charte-graphique.md` qui suit cette structure.

La charte graphique sert a la fois de **specification**, **test visuel** et **reference** : si elle rend bien, le theme est valide.

**Reference implementation complete** : `themes/standard/charte-graphique.md` (33 slides) — source de verite visuelle a consulter en cas de doute.

---

## Sections obligatoires

Chaque section teste un type d'element. L'ordre est fixe.

### Section 1 — Typographie & Tableaux (4-5 slides)

```
Slide  1 — [LEAD] Titre du theme + version + description
Slide  2 — [TYPO] H2, H3, body, strong, em, code inline, bloc code
Slide  3 — [TABLE-STD] Tableau standard (4 colonnes, donnees generiques)
Slide  4 — [TABLE-GRADIENT-A] Coloration par ligne (rank-*) avec transition flip
Slide  5 — [TABLE-GRADIENT-B] Coloration par cellule avec transition flip
```

### Section 2 — Composants visuels (5 slides)

```
Slide  6 — [INFO-BOX] 4 variantes : bleu (info) / vert (succes) / orange (warning) / rouge (danger)
Slide  7 — [KPI] 4 KPI cards (L1 par famille de couleur)
Slide  8 — [STEPS] 3 steps numerotes (pastille L2 + barre L1)
Slide  9 — [CARDS-3] 3 cards en colonnes (couleurs differentes)
Slide 10 — [COMPARE-2] Comparatif 2 colonnes (vert vs rouge)
```

### Section 3 — Diagrammes Mermaid, patterns (7-8 slides)

```
Slide 11 — [DECISION-TREE] Arbre de decision pour choisir un pattern Mermaid
Slide 12 — [PATTERN-SUBGRAPH] Subgraph zones (prefere quand groupes logiques)
Slide 13 — [PATTERN-LR-SIMPLE] LR lineaire (3-6 elements)
Slide 14 — [PATTERN-LR-BRANCHING] LR avec branching (fan-out/fan-in, 2D auto)
Slide 15 — [PATTERN-TB-VERTICAL] TB vertical (flux dense sans groupement)
Slide 16 — [PATTERN-LR-WRAP] Snake (SVG statique) — horizontal tres long
Slide 17 — [PATTERN-FEEDBACK] Feedback externe avec node LOOP
Slide 18 — [ANTIPATTERN] Feedback inline (a eviter)
```

### Section 4 — Autres types Mermaid (3-9 slides)

```
Slide 19 — [MERMAID-INTRO-A] Intro Processus & Data (bars : Gantt, Timeline, Sequence, Journey)
Slide 20 — [MERMAID-INTRO-B] Intro Structure & Analyse (bars : Pie, State, ER, Quadrant)
Slides 21-28 — [MERMAID-*] Un slide par type (Gantt, Timeline, Sequence, Journey, Pie, State, ER, Quadrant)
```

### Section 5 — Design system (3 slides)

```
Slide 29 — [IMBRICATION-3] Exemple L1/L2/L3 imbrication
Slide 30 — [PALETTE] Variables CSS (dark / light) sous forme de tableau
Slide 31 — [HSL-SYSTEM] Preview de la palette generee (image palette-preview.svg) + principes
```

### Section 6 — Conclusion (2 slides)

```
Slide 32 — [TRANSITIONS] Tableau des transitions utilisees (fade / flip / fade-out)
Slide 33 — [CLOSING] Section break de fin avec resume du design system
```

**Total : 33 slides.**

---

## Regles de generation

1. **Frontmatter minimal** — pas de `style: |` : le CSS est injecte par `marp_postprocess.py`
2. **Utiliser les classes CSS du systeme L1/L2/L3** (`.l1-blue`, `.l2-green`, `.l3-violet`, etc.)
3. **Utiliser les snippets du theme.md** — chaque pattern HTML vient du theme
4. **Aucun hex hand-picked dans le markdown** — utiliser `var(--name)` si besoin de customisation
5. **Transitions** :
   - Tableaux donnees, KPI, resultats : `<!-- transition: flip -->`
   - Closing + section breaks : `<!-- transition: fade-out -->`
   - Autres : `fade` (global)
6. **Slides sparse** : utiliser `<!-- _class: compact -->` pour centrer verticalement
7. **Annotations** : chaque slide inclut une ligne expliquant les valeurs CSS utilisees
8. **Images/SVG** : chemin relatif `./images/...`, toujours `h:NNN` pour controler la hauteur

---

## Workflow de validation

```bash
cd themes/{nom}/

# 1. Generer les SVG Mermaid depuis la palette HSL
python gen_charte_diagrams.py

# 2. Rendre le deck en HTML
marp charte-graphique.md --html --bespoke.transition -o charte-graphique.html

# 3. Injecter le theme CSS + Sommaire + Dark/Light toggle
python ../../scripts/marp_postprocess.py charte-graphique.html

# 4. Auto-fit : detection + fix automatique d'overflow par slide
python ../../scripts/auto_fit_slides.py charte-graphique.html

# 5. Screenshot Playwright (dark + light)
python screenshot_slides.py both

# 6. Validation visuelle (Agent Browser recommande)
#    Lancer un serveur local : python -m http.server 8765
#    Naviguer sur http://localhost:8765/charte-graphique.html

# 7. Validation technique (overflow + contraste WCAG)
python ../../scripts/validate_marp.py charte-graphique.md
```

**Criteres visuels** :
- Aucune slide en overflow (apres auto-fit : `ALL FIT`)
- Contraste lisible en dark ET light (ratio >= 3:1 via `validate_marp.py`)
- Tables : bordure au niveau de la derniere cellule (pas d'extension), 1ere col left, autres center
- Mermaid : toutes les couleurs derivees de la palette HSL (aucun hex Mermaid par defaut)
- Dark/Light toggle : toutes les classes L1/L2/L3 inversent proprement
