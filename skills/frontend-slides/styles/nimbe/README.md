# Nimbe — Frontend Slides Style

> **Version** : 2.0.0
> **Mode** : Dark/Light dual avec toggle
> **Vibe** : Premium animé corporate

Style maison « Nimbe » pour les decks générés via `/frontend-slides --style nimbe`.

## Contenu du dossier

```
styles/nimbe/
├── preset.css            # CSS injectable dans tout deck généré
├── README.md             # Ce fichier
├── golden/               # Références « standard du verre » à imiter
│   ├── LIQUID-GLASS-STANDARD.html
│   └── LIQUID-GLASS-STANDARD-v2.html
└── components/           # Niveau 3 — Composants signature Nimbe
    ├── liquid-glass.css           # Bibliothèque de composants verre
    ├── liquid-glass-extended.css  # Composants Uiverse adaptés
    ├── nimbe-deck-helpers.js      # Helpers JS (sidebar, overlays, nav)
    ├── COMPONENTS.md              # Doc API (markup + classes + variables)
    ├── SHOWCASE.html              # Showcase preview interactif
    └── NIMBE-DEMO.html            # Démo du style (charge le vrai preset.css)
```

## Usage rapide

### Générer un deck Nimbe

```
/frontend-slides --style nimbe "Sujet du deck"
```

L'agent :
1. Injecte `preset.css` (couche style) dans le deck généré
2. Ajoute `components/liquid-glass.css` + `liquid-glass-extended.css` si des composants Niveau 3 sont utilisés
3. Utilise les composants signature (verre `.lg`, KPI glass, tables `.ptable`, configurateur à règle métier, etc.)
4. Respecte les règles d'or et anti-patterns

### Voir le showcase composants

Ouvrir `components/SHOWCASE.html` pour parcourir les composants avec preview live, ou lire `components/COMPONENTS.md` pour la doc API (markup + classes).

### Voir le standard du verre

Ouvrir `golden/LIQUID-GLASS-STANDARD-v2.html` dans un navigateur (toggle dark/light en haut à droite) : c'est la source unique de vérité de la surface `.lg`.

## Palette canonique

```css
--nimbe-blue: #0027a3;   /* accent primaire */
--nimbe-red:  #a1140e;   /* accent secondaire */
--bg-dark: #050508;
--bg-light: #FAFAFA;
```

Stack font : Outfit (display) + DM Sans (body) — Google Fonts.

## Règles d'or

1. `clamp()` partout pour font-size et spacing
2. Viewport fit obligatoire (100vh, overflow hidden)
3. Outfit + DM Sans uniquement (jamais d'autre font)
4. Eyebrow systématique sur sections
5. Surface `.lg` obligatoire pour toute carte de contenu
6. Stagger reveals sur grilles 3+ items
7. Highlight bleu/gradient dans titres H1/H2
8. Tokens texte `--c-*` pour toute couleur de texte (lisibilité bi-thème)
9. Métriques avec gradient text (`.metric`)
10. Dark/Light toggle présent (signature)

## Anti-patterns à éviter

- Fonts génériques (Inter, Roboto, Arial, system-ui)
- Gradient violet sur blanc (AI slop)
- Drop shadow non-tinted
- Border-radius < 0.75rem
- Text body > 70ch sans wrap
- Couleurs hors palette canonique
- Couleur d'accent brute (`var(--nimbe-*)`) en couleur de texte (illisible en dark)

## Mise à jour du style

Pour faire évoluer le style :

1. Éditer `preset.css` (couche style injectable)
2. Mettre à jour `golden/LIQUID-GLASS-STANDARD-v2.html` en cohérence (standard du verre)
3. Bumper la version (header `**Version** : X.Y.Z`)
4. Re-screenshoter via Playwright pour validation
5. Tester sur un deck pilote avant déploiement

## Validation visuelle

Workflow de validation après modifications :

```bash
# 1. Servir le dossier en local
cd skills/frontend-slides/styles/nimbe/
python -m http.server 8765

# 2. Ouvrir le showcase et le standard du verre
# http://localhost:8765/components/SHOWCASE.html
# http://localhost:8765/golden/LIQUID-GLASS-STANDARD-v2.html

# 3. Tester :
#    - Toggle dark/light (bouton top-right)
#    - Hover sur cards (lift + glow)
#    - Sheen qui suit la souris
#    - Tous les composants rendus correctement

# 4. Screenshots pour archive (via Playwright)
```

## Crédits

- Adaptation Frontend Slides : @Ornichus (avr 2026)
