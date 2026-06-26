---
description: 'Génère une présentation Marp (Markdown → slides HTML/PDF/PPTX)'
---

# /marp-slides - Générer une présentation Marp

Crée une présentation professionnelle au format Marp à partir d'un sujet, de données, ou d'un brief.

## Utilisation

```
/marp-slides                                    # Mode interactif, theme standard
/marp-slides "Titre de la présentation"
/marp-slides rapport données.csv
/marp-slides tech "Architecture du projet"
/marp-slides --theme corporate "Mon pitch"      # Theme specifique
/marp-slides --new-theme "minimal-light"        # Creer un nouveau theme
```

## Instructions

### Étape 1 : Charger le skill et le theme

1. Lire `.claude/skills/marp-presentations/SKILL.md` (workflow, regles, structure)
2. **Determiner le theme :**
   - Si `--theme {nom}` → charger `.claude/skills/marp-presentations/themes/{nom}/theme.md`
   - Si `--new-theme {nom}` → aller au workflow "Creer un theme" (voir plus bas)
   - Sinon → charger `.claude/skills/marp-presentations/themes/standard/theme.md`
3. Si le theme demande n'existe pas → lister les themes disponibles et demander

### Étape 2 : Comprendre la demande

| Paramètre | Source | Défaut |
|-----------|--------|--------|
| **Sujet** | Argument ou conversation | Demander |
| **Type** | `rapport`, `tech`, `guide`, `pitch`, `custom` | Inférer du sujet |
| **Theme** | `--theme {nom}` | `standard` |
| **Données source** | Fichier CSV/JSON/texte mentionné | Aucun |
| **Audience** | Mentionnée ou inférée | Technique |
| **Nombre de slides** | Mentionné ou selon type | 8-12 |

**Si le sujet est ambigu :** poser UNE question claire, pas un interrogatoire.

### Étape 3 : Planifier le deck

AVANT de générer, créer un plan de slides avec transitions :

```
1. [LEAD] Titre + sous-titre (fade)
2. [CONTEXTE] Problème / situation (fade)
3-N. [CONTENU] Slides de contenu (fade / flip pour données)
N. [SECTION BREAK] si changement de partie (fade-out)
N+1. [CLOSING] Conclusion / CTA (fade)
```

Afficher le plan à l'utilisateur pour validation rapide.
**Exception :** si la demande est très claire et spécifique, générer directement.

### Étape 4 : Générer la présentation

1. Créer le répertoire si absent :
   ```bash
   mkdir -p docs/slides
   ```

2. Nommer le fichier : `docs/slides/{YYYY-MM-DD}_{sujet-slug}.md`

3. Générer le contenu Marp en suivant le `theme.md` charge :
   - **CSS frontmatter** : copier le bloc tel quel depuis theme.md
   - **Palette** : utiliser les couleurs definies dans theme.md
   - **Snippets** : utiliser les elements HTML du theme.md (KPIs, boxes, cards, steps, etc.)

4. **Règles de génération :**
   - Copier le frontmatter CSS du theme.md tel quel
   - `transition: fade` en global, `<!-- transition: flip -->` pour données, `<!-- transition: fade-out -->` pour section breaks
   - Slide 1 = toujours `<!-- _class: lead -->` avec titre
   - Seule classe autorisée : `lead` (pas de `invert`, `closing`, ni custom)
   - **Règle des 10 lignes** : max 10 lignes visibles par slide (titre exclus), splitter sinon
   - Utiliser les snippets du theme — ne pas inventer de styles
   - HTML uniquement pour les éléments visuels (KPIs, boxes, cards)
   - Le reste en Markdown pur

### Étape 5 : Données source (si applicable)

Si l'utilisateur fournit un fichier de données :

1. Lire et analyser le fichier (CSV, JSON, texte)
2. Extraire les métriques clés → KPI cards (snippets du theme)
3. Identifier les tendances → tableaux stylisés (CSS du theme)
4. Synthétiser les insights → info boxes colorées (snippets du theme)
5. Diagrammes → Mermaid SVG si pertinent (section 5 du SKILL.md)

### Étape 6 : Validation

Si `docs/scripts/validate_marp.py` existe :

```bash
python docs/scripts/validate_marp.py docs/slides/{fichier}.md
```

- **OVERFLOW** → splitter la slide, re-valider
- **LOW CONTRAST** → corriger les couleurs, re-valider
- **Boucler jusqu'à ALL CLEAR**

Si le script n'existe pas : vérifier manuellement la règle des 10 lignes.

### Étape 7 : Export et ouverture

```bash
# HTML avec transitions
marp docs/slides/{f}.md --html --bespoke.transition -o docs/slides/{f}.html

# Ouvrir dans le navigateur
start docs/slides/{f}.html
```

Afficher le rapport :

```
## Présentation générée

- Fichier : `docs/slides/{nom}.md`
- Slides : N slides
- Type : {type}
- Theme : {nom du theme}

### Export additionnel

- **PDF** : `marp docs/slides/{nom}.md --pdf -o docs/slides/{nom}.pdf`
- **PowerPoint** : `marp docs/slides/{nom}.md --pptx -o docs/slides/{nom}.pptx`
- **Live** : `marp -s docs/slides/`
```

---

## Workflow : Creer un nouveau theme

Declenche par `/marp-slides --new-theme {nom}`.

### Étape A : Definir l'identite

Demander a l'utilisateur :
- **Fond** : sombre, clair, couleur ?
- **Ton** : corporate, fun, minimaliste, technique ?
- **Palette** : couleurs imposees (charte existante) ou libre ?
- **Cas d'usage** : quel type de presentations ?

### Étape B : Creer theme.md

1. Creer `.claude/skills/marp-presentations/themes/{nom}/`
2. Generer `theme.md` en suivant la structure de `themes/standard/theme.md` :
   - Identite (nom, description, fond)
   - CSS frontmatter complet
   - Palette (roles, couleurs, usages)
   - Couleurs par type (info/succes/warning/danger/violet/cyan)
   - Snippets pour chaque element (KPI, info box, cards, steps, comparatif, section break)
   - Transitions
   - Palette Mermaid (si fond sombre : hex fonces ; si fond clair : hex clairs)

### Étape C : Generer la charte graphique

1. Lire `.claude/skills/marp-presentations/charte-graphique-template.md`
2. Generer `themes/{nom}/charte-graphique.md` — 14 slides obligatoires
3. Rendre en HTML : `marp themes/{nom}/charte-graphique.md --html --bespoke.transition -o themes/{nom}/charte-graphique.html`
4. Ouvrir dans le navigateur

### Étape D : Iterer

L'utilisateur review la charte visuellement. Boucle :
1. Feedback ("tableaux trop serres", "KPIs trop petits", "couleur trop flashy")
2. Corriger theme.md + charte-graphique.md
3. Re-rendre HTML
4. Re-ouvrir

**Quand l'utilisateur valide → le theme est pret pour /marp-slides --theme {nom}**

---

## Types de présentations

| Type | Quand | Slides | Style |
|------|-------|--------|-------|
| `rapport` | Données, KPIs, résultats | 8-15 | Dense, tableaux, charts |
| `tech` | Architecture, ADRs, stack | 6-12 | Code, diagrammes, comparaisons |
| `guide` | Tutoriel, how-to, recette | 4-8 | Étapes numérotées, visuels |
| `pitch` | Vente, proposition, idée | 5-10 | Aéré, impact, CTA fort |
| `custom` | Autre | Variable | Adapté au besoin |
