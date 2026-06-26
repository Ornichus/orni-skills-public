---
description: 'Compile une liste d URLs articles web en PDF dossier organise par pays/categorie via le skill web-pdf-compile'
---

# /web-pdf-compile - Compiler des articles web en PDF

Capture des articles web (article-only, sans pubs/sidebar/commentaires) et les compile en un PDF dossier structure groupe par pays ou categorie. Adapte aux revues de presse, dossiers d'enquete journalisme, bibliographies de recherche, archives de couverture media multi-sites.

## Utilisation

```
/web-pdf-compile                         # Mode interactif (template config + run)
/web-pdf-compile examples/random-test.json # Run direct sur exemple
/web-pdf-compile probe <url>              # Auto-suggere selectors pour un site
/web-pdf-compile <sources.json>           # Run capture + compile sur config custom
```

## Workflow (4 etapes)

1. **Probe** (optionnel mais recommande pour nouveau site) :
   ```bash
   node .claude/skills/web-pdf-compile/scripts/probe-dom.js <url>
   ```
   Suggere `selectors` (article body) + `extraRemove` (sidebar, comments, pubs).

2. **Editer** `sources.json` avec liste URLs + selectors par site.

3. **Capture** :
   ```bash
   node .claude/skills/web-pdf-compile/scripts/capture.js <sources.json>
   ```
   Genere JPGs article-only par source (Puppeteer + adblock Cliqz + crop).

4. **Compile** :
   ```bash
   node .claude/skills/web-pdf-compile/scripts/compile-pdf.js <sources.json>
   ```
   Genere le PDF final adaptive groupe par pays + cover + TOC + footer.

## Format sources.json

```json
{
  "title": "Titre dossier",
  "subtitle": "Sous-titre",
  "output_dir": "./output/dossier",
  "country_order": [
    { "code": "WW", "name": "Worldwide" }
  ],
  "sources": [
    {
      "id": "01",
      "shortname": "site-article",
      "country": "WW",
      "url": "https://...",
      "selectors": [".article-body"],
      "extraRemove": [".sidebar", ".comments"]
    }
  ]
}
```

Voir `.claude/skills/web-pdf-compile/examples/sources.example.json` pour template complet et `examples/random-test.json` pour cas reel.

## Pre-requis

- Node.js 18+ avec npm install dans `.claude/skills/web-pdf-compile/`
- Chrome installe (Puppeteer-core utilise le Chrome systeme)

Si dependances absentes : suggerer
```bash
cd .claude/skills/web-pdf-compile && npm install
```

## Cas d'usage

- Revue de presse compilee (multi-sources sur un sujet)
- Dossier de preuves journalisme d'investigation
- Bibliographie de recherche avec captures embarquees
- Archive de couverture media multi-sites
- Documentation legale avec preservation de sources

## Limites connues

- Adblock Cliqz EasyList ne couvre pas pubs regionales -> fallback : screenshots manuels uploads dans `articles/NN-shortname/parts/`
- Sites avec Cloudflare anti-bot -> utiliser snapshot Wayback Machine (champ `source: "wayback"`)
- Paywalls non bypasses

## Reference

Voir `.claude/skills/web-pdf-compile/SKILL.md` pour le skill complet (description detaillee + 4 etapes detaillees) et `.claude/skills/web-pdf-compile/PROTOCOLE.md` pour les anti-patterns documentes (8 erreurs apprises pendant le developpement).
