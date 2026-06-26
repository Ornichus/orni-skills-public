---
description: 'Genere un design system complet (HTML scrollable + brand book A4 PDF) depuis une reference brand (URL, screenshot, description)'
---

# /design-system - Generer un design system + brand book A4

Cree deux artifacts publics partageables depuis une reference brand : `design-system.html` (page scrollable colors/fonts/principles/components/wordmarks) + `brand-book-a4.pdf` (single page A4 portrait print-ready).

**A NE PAS CONFONDRE** :
- `/design-system` = artifact public partageable (HTML + PDF) pour clients/partenaires
- `/frontend-slides --new-style {nom}` = module interne consume par decks (BRAND-BOOK.md + preset.css)

Voir `.claude/skills/design-system/README-ORNI.md` pour l'arbre de decision complet.

## Utilisation

```
/design-system                                    # Mode interactif (demande la reference)
/design-system https://exemple.com               # Extract URL via WebFetch
/design-system "Acme - primary #ff4444, font Inter, tagline Ship faster"
/design-system [path/to/screenshot.png]          # Extract depuis image
```

## Workflow combine (methode RoboNuggets complete)

```
1. /design-system https://exemple.com
   -> design/design-system.html (scrollable)
   -> design/brand-book-a4.pdf (print-ready)

2. (Optionnel) /frontend-slides --new-style nom-brand (input: design/)
   -> skills/frontend-slides/styles/{nom-brand}/{BRAND-BOOK.md, preset.css}

3. /frontend-slides --style nom-brand "Sujet du deck"
   -> docs/presentations/{date}_{slug}/index.html (deck branded)
```

## Instructions

### Etape 1 : Charger le skill

1. Lire `.claude/skills/design-system/SKILL.md` (workflow extract -> generate -> render PDF)
2. Lire `.claude/skills/design-system/examples/template.html` (skeleton A4 avec {{TOKENS}})
3. Si reference absente dans les arguments : demander en une seule question (URL / Screenshot / Description)

### Etape 2 : Suivre le workflow du SKILL

Le SKILL.md decrit le workflow complet :

- **Extract** : si URL -> WebFetch + parse CSS/HTML, si screenshot -> Read image, si description -> parse texte
- **Confirm** : lister ce qui a ete extrait, demander uniquement les gaps
- **Generate** : ecrire `design/design-system.html` (scrollable) + `design/brand-book-a4.html` (A4)
- **Render PDF** : headless Edge/Chrome -> `design/brand-book-a4.pdf`
- **Show** : afficher chemins + ouvrir dans navigateur si possible
- **Iterate** : feedback utilisateur

### Etape 3 : Regles non-negociables

1. **Extract before asking** : pre-remplir tout ce qui est extractible avant de demander
2. **Never invent brand details** : palette/fonts/logos/principles viennent de la reference ou de l'utilisateur, jamais inventes
3. **Never redraw logos** : SVG exact de la reference, jamais redessine. Si raster -> demander SVG ou laisser placeholder
4. **Drop sections sans source** : mieux vaut skipper une section que la remplir de fiction
5. **Match the brand** : surfaces/radius/border/typo viennent de la reference, ne pas imposer un style par defaut
6. **Fit on one A4** : si overflow, tighten padding ou drop section. JAMAIS de scroll dans le brand-book
7. **Self-contained HTML** : Google Fonts CDN + inline CSS + inline SVG. Pas de build step
8. **Render the PDF** : ne pas livrer juste le HTML, finir avec headless Edge/Chrome

### Etape 4 : Sortie

Par defaut, generer dans :

```
design/
|-- design-system.html        # Page scrollable
|-- brand-book-a4.html        # A4 portrait HTML
`-- brand-book-a4.pdf         # PDF rendered via headless browser
```

Sauf si l'utilisateur indique un autre emplacement.

### Etape 5 : Apres generation

Afficher :

```
## Design system genere

- Reference : {URL / screenshot / description}
- Files :
  - design/design-system.html (scrollable, N sections)
  - design/brand-book-a4.html (A4 portrait)
  - design/brand-book-a4.pdf (print-ready)
- Palette extraite : {primary} {secondary} {tertiary} (+ N accents)
- Fonts : {display} + {mono}
- Sections incluses : {liste}
- Sections droppees (pas de source) : {liste si applicable}

### Ouvrir
- HTML : ouvrir dans navigateur
- PDF : design/brand-book-a4.pdf

### Workflow suivant
- Pour creer un module deck branded : `/frontend-slides --new-style {nom-brand}` (input: design/)
- Pour iterer : decrire les changements souhaites
```

## Quand utiliser /design-system vs /frontend-slides --new-style

| Besoin | Commande |
|--------|----------|
| Document partageable client/partenaire | `/design-system` |
| Module interne pour deck branded | `/frontend-slides --new-style` |
| Les deux (workflow RoboNuggets complet) | `/design-system` puis `/frontend-slides --new-style` |

## Reference upstream

Skill source : https://github.com/robonuggets/design-system (MIT, RoboNuggets)
Tutoriel : https://www.youtube.com/watch?v=t2ELuj2prA0 (niveau 2 Brand Book)
