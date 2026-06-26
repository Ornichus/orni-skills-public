---
description: 'Genere une presentation HTML one-shot stylisee (decks pitch / brand mockup) via le skill frontend-slides'
---

# /frontend-slides - Generer une presentation HTML

Cree une presentation HTML mono-fichier au format zarazhang/frontend-slides : zero dependance, 12 styles curates, viewport-fit obligatoire, animations CSS/JS riches.

**A NE PAS CONFONDRE avec `/marp-slides`** :
- `/marp-slides` = Markdown -> HTML/PDF/PPTX, theme reproductible, decks recurrents
- `/frontend-slides` = HTML one-shot ultra-stylise, pitch unique, brand mockup

Voir `.claude/skills/frontend-slides/README-ORNI.md` pour l'arbre de decision complet.

## Utilisation

```
/frontend-slides                                    # Mode interactif complet (recommande)
/frontend-slides "Pitch deck startup IA"
/frontend-slides --style nimbe "Pitch premium"      # Style maison Nimbe
/frontend-slides convert presentation.pptx
/frontend-slides enhance ./mon-deck/index.html
```

## Styles disponibles (custom brands)

Si l'utilisateur passe `--style {nom}` :

1. Charger `.claude/skills/frontend-slides/styles/{nom}/README.md` (doc du style)
2. Charger `.claude/skills/frontend-slides/styles/{nom}/preset.css` (CSS injectable)
3. **NE PAS** suivre Phase 2 (Style Discovery) — le style est imposé
4. Suivre Phase 3 directement avec les snippets et règles du brand

Si style inexistant : lister les styles disponibles via `ls styles/` et demander.

Si `--style` absent : suivre le workflow upstream classique (Phase 2 mood selection + 3 previews).

## Instructions

### Etape 1 : Charger le skill

1. Lire `.claude/skills/frontend-slides/SKILL.md` (workflow Phases 0-6)
2. **Determiner le style :**
   - Si `--style {nom}` -> charger `.claude/skills/frontend-slides/styles/{nom}/README.md` + `preset.css` (skip Phase 2)
   - Sinon -> Phase 2 mood selection (workflow upstream)
   - Si style inexistant -> lister styles dispos et demander
3. Identifier le mode :
   - **Mode A (New)** : creation de zero -> Phase 1
   - **Mode B (PPT Conversion)** : `convert <fichier.pptx>` -> Phase 4
   - **Mode C (Enhancement)** : `enhance <fichier.html>` -> Mode C rules
4. Si argument absent : demander en une seule fois (Purpose / Length / Content / Editing / Diagrams)

### Etape 2 : Suivre le workflow du SKILL

Le SKILL.md decrit le workflow complet en 6 phases. Le respecter strictement :

- **Phase 1** : Content discovery (5 questions en un seul AskUserQuestion : Purpose, Length, Content, Editing, Diagrams). Q5 Diagrams active la pipeline Mermaid en Phase 3 (cf. `html-template.md` section "Diagram Integration"). Preview Mermaid en Phase 2 = [DIFFERE].
- **Phase 2** : Style discovery via mood selection + 3 previews HTML generes (lire `STYLE_PRESETS.md`)
- **Phase 3** : Generation HTML mono-fichier (lire `viewport-base.css`, `html-template.md`, `animation-patterns.md`)
- **Phase 4** : PPT -> HTML conversion (script `scripts/extract-pptx.py`)
- **Phase 5** : Delivery (clean .claude-design/, open browser, summary)
- **Phase 6** : Optional share (Vercel deploy, PDF export)

### Etape 3 : Regles non-negociables

1. **Viewport fit** : chaque `.slide` tient en 100vh, `overflow: hidden`, jamais de scroll interne
2. **Anti-AI-slop** : pas de Inter/Roboto/Arial en display, pas de gradient violet sur blanc, pas de layouts generiques
3. **`clamp()` partout** : font-size et spacing en `clamp(min, preferred, max)` exclusivement
4. **`viewport-base.css` integre** : copier le contenu COMPLET du fichier dans le `<style>` du deck genere
5. **Fonts Fontshare/Google** : jamais de system fonts en display
6. **Commentaires de section** : chaque bloc HTML/CSS/JS porte un `/* === SECTION === */`

### Etape 4 : Sortie

Par defaut, generer dans :

```
docs/presentations/{YYYY-MM-DD}_{slug}/
|-- index.html        # deck principal
`-- assets/           # images si fournies
```

Sauf si l'utilisateur indique un autre emplacement.

### Etape 5 : Apres generation

Afficher :

```
## Presentation generee

- Fichier : `docs/presentations/{slug}/index.html`
- Style : {nom du preset}
- Slides : N
- Editing inline : oui/non

### Navigation
- Fleches / Espace / Page Up-Down
- Touch swipe sur mobile
- E pour activer le mode edit (si active)
- Ctrl+S pour sauvegarder l'edit (si active)

### Partage optionnel
- Deploy Vercel : `bash .claude/skills/frontend-slides/scripts/deploy.sh docs/presentations/{slug}/`
- Export PDF : `bash .claude/skills/frontend-slides/scripts/export-pdf.sh docs/presentations/{slug}/index.html`
```

## Quand basculer vers `/marp-slides`

Si l'utilisateur veut :
- Plusieurs decks coherents entre eux (theme partage)
- Export PowerPoint (PPTX)
- Versioning git friendly (Markdown diffe-able)
- Validation contraste WCAG
- Decks data-heavy avec tables comparatives, KPIs, Mermaid

-> Suggerer `/marp-slides` plutot.

## Reference upstream

Skill source : https://github.com/zarazhangrui/frontend-slides (MIT, @zarazhangrui)
Tutoriel : https://www.youtube.com/watch?v=t2ELuj2prA0
