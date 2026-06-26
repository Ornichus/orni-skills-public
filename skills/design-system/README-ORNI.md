# design-system — integration Orni-skills

> Skill **upstream** : [robonuggets/design-system](https://github.com/robonuggets/design-system) (MIT)
> **Auteur original** : RoboNuggets (cf. video YouTube niveau 2 méthode Brand Book)
> **Version Orni** : 1.0.0

---

## Pourquoi ce skill dans Orni

Génération d'**artifacts publics partageables** depuis n'importe quelle référence brand (URL, screenshot, description). Cas d'usage : extraire une charte existante en 2 fichiers polish (design-system.html scrollable + brand-book-a4.pdf print-ready) à transmettre à un client, partenaire, ou équipe externe.

**Complémentaire de `frontend-slides`** : design-system produit les artifacts publics, frontend-slides consomme la palette/typo extraite pour générer des decks brandés.

## Choix design-system vs frontend-slides

| Critère | `design-system` (`/design-system`) | `frontend-slides --new-style` |
|---------|-----------------------------------|-------------------------------|
| **Output** | `design-system.html` scrollable + `brand-book-a4.pdf` A4 | `styles/{nom}/BRAND-BOOK.md` + `preset.css` interne |
| **Audience** | Externe (clients, partenaires) | Interne (skill consume pour decks) |
| **Format** | Page web + PDF print | Markdown + CSS module |
| **Niveau** | Niveau 2 RoboNuggets (extract brand) | Niveau 2 RoboNuggets (style brand) |
| **Déclencheur** | "Make a design system for X" | "Génère un style branded pour deck" |
| **Réutilisation** | Document signé point-in-time | Module versionné re-utilisé par decks |

**Règle de pouce** : `/design-system` quand tu veux **partager une charte** ; `/frontend-slides --new-style` quand tu veux **alimenter le moteur de decks** avec un nouveau brand book interne.

## Workflow combiné méthode RoboNuggets complète

```
1. /design-system https://exemple.com
   → design/design-system.html (scrollable)
   → design/brand-book-a4.pdf (print-ready A4)

2. /frontend-slides --new-style nom-brand (input: design/)
   → skills/frontend-slides/styles/{nom-brand}/BRAND-BOOK.md (12 sections)
   → skills/frontend-slides/styles/{nom-brand}/preset.css (variables CSS + classes)
   → skills/frontend-slides/styles/{nom-brand}/BRAND-BOOK.html (preview interactif)

3. /frontend-slides --style nom-brand "Sujet du deck"
   → docs/presentations/{date}_{slug}/index.html (deck branded)
```

Étape 1 = artifacts publics, étape 2 = module interne, étape 3 = consommation.

## Architecture du skill

```
skills/design-system/
|-- SKILL.md                  # Workflow extract → generate → render PDF
|-- README-ORNI.md            # Ce fichier
|-- LICENSE                   # MIT (upstream)
`-- examples/
    `-- template.html         # Structural skeleton avec {{TOKENS}} A4 portrait
```

## Installation dans un projet

Via Orni :

```
/orni-init-ds                       # installe dans le projet courant
/orni-update-ds                     # met à jour depuis le repo Orni-skills
```

Après install :
- Commande disponible : `/design-system`
- Skill copié dans `.claude/skills/design-system/`
- Manifest `.claude/orni-manifest.json` mis à jour

## Mise à jour upstream

Le skill suit l'upstream `robonuggets/design-system`. Pour rafraîchir depuis le repo officiel :

```bash
# Dans Orni-skills :
git clone https://github.com/robonuggets/design-system.git /tmp/ds-update
cp /tmp/ds-update/LICENSE skills/design-system/LICENSE
cp /tmp/ds-update/.claude/skills/design-system/examples/template.html skills/design-system/examples/template.html
# Re-merge SKILL.md à la main (préserver le bandeau Version + référence README-ORNI + section Combinaison)
```

Bumper `**Version** : X.Y.Z` en haut de SKILL.md et commiter.

## Dépendances obligatoires

| Feature | Dépendance |
|---------|-----------|
| Render PDF | Microsoft Edge (Windows) ou Chrome/Chromium (mac/linux) headless |
| Extract URL | WebFetch (natif Claude Code) |
| Inline SVG logo | User fournit SVG (pas raster) |

Pas de dépendance Node/Python pour la génération HTML elle-même. Self-contained.

## Philosophie

3 règles upstream à préserver :

1. **Extract before asking** — pré-remplir tout ce qui est extractible avant de demander à l'utilisateur
2. **Never invent brand details** — palette/fonts/logos/principles viennent de la référence ou de l'utilisateur, jamais inventés
3. **Drop sections without source** — mieux vaut skipper une section que la remplir de fiction

## Credits

- Skill original : [robonuggets/design-system](https://github.com/robonuggets/design-system) (MIT)
- Tutoriel vidéo : [RoboNuggets - Claude HTML Slides](https://www.youtube.com/watch?v=t2ELuj2prA0) (niveau 2 Brand Book)
- Intégration Orni-skills : @Ornichus (avr 2026)
