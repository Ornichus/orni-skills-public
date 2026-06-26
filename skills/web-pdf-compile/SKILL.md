---
name: web-pdf-compile
description: Capture web articles cleanly (article-only, no ads/sidebar/comments) and compile them into a structured PDF document grouped by country or category. Triggers on "compile articles to PDF", "screenshot articles", "make PDF from URLs", "research dossier", or invocation /web-pdf-compile.
version: 1.0.0
---

# Web PDF Compile

Skill for transforming a list of web article URLs into a clean, organized PDF dossier. Handles ad-blocking, layout cleanup (sidebar/comments/related/share buttons), Wayback fallback for dead pages, country-based grouping, and adaptive PDF page sizing.

## Use cases

- Press review compilation
- Investigative journalism evidence dossier (multi-source confirmation)
- Research bibliography with embedded source captures
- Archive of news coverage on a topic across multiple sites
- Legal documentation requiring source preservation

## Input

JSON file describing sources. See `examples/sources.example.json`.

```json
{
  "title": "Dossier de recherche",
  "subtitle": "Compilation des sources",
  "output_dir": "./output/mon-dossier",
  "country_order": [
    { "code": "WW", "name": "Worldwide" }
  ],
  "sources": [
    {
      "id": "01",
      "shortname": "wikipedia-photosynthesis",
      "country": "WW",
      "url": "https://en.wikipedia.org/wiki/Photosynthesis",
      "selectors": ["#mw-content-text", "main"],
      "extraRemove": [".navbox", ".reflist", ".infobox"]
    }
  ]
}
```

## Workflow (4 steps)

### 1. Probe (optional, recommended for new sites)

Identify CSS selectors for article body + tail elements (sidebar, comments, related, ads).

```bash
node scripts/probe-dom.js <url>
```

Returns suggested `selectors` and `extraRemove` to add to source config.

### 2. Capture

Capture each source as JPGs (full + sectioned).

```bash
node scripts/capture.js <sources.json>
```

Per source :
- Puppeteer headless Chrome + Cliqz adblocker (EasyList)
- Custom request blocking for ad/tracking domains
- Sticky/fixed neutralization
- Tail element removal (per-site `extraRemove`)
- Article bounds detection (selectors → heuristic fallback)
- Horizontal + vertical crop to article-only
- Section overlap 60px (no mid-line cuts)
- Blank section auto-skip (sharp stats stdev < 12)
- Wayback Machine fallback for HTTP errors

Output : `articles/NN-shortname/full.jpg + parts/part-NN.jpg`.

### 3. Manual fallback (optional)

If Cliqz can't block site-specific ads (regional networks not in EasyList) :
- User provides screenshots manually (Brave/Firefox + uBlock)
- Drop into `articles/NN-shortname/parts/`
- **Critical** : verify chronological order matches article flow (use `scripts/verify-order.js`)

### 4. Compile

Generate PDF.

```bash
node scripts/compile-pdf.js <sources.json>
```

- Cover page : title + subtitle + TOC grouped by country
- Per source : separator page (country header + title + URL) + content pages
- **Adaptive page sizing** : page height = scaled image height (zero whitespace)
- Wayback badge for archived sources
- Footer "Source NN — shortname / Section X/Y"

## Critical rules (from PROTOCOLE.md)

### Capture must include
- H1/title, photo principale, body article complet, signature/auteur

### Capture must NOT include
- Header/nav site, footer site, sidebar (PLUS LUS, articles populaires, ARTICLE PRECEDENT/SUIVANT)
- Comments + comment form
- Pubs (banners, inline, overlay)
- Share buttons after article
- Newsletter / subscribe / tags

### Anti-patterns (NEVER do)
- `[class*="comment"]` in universal removal (false positives on `.comment-counter` etc)
- `[id*="ad-"]` in universal removal (matches `#tdb-autoload-article` = the article itself on some themes)
- 2 sections stacked per A4 page (too small)
- Fixed A4 portrait for landscape image (excessive whitespace) → use adaptive sizing
- Slicing without overlap (cuts mid-line)
- Skipping NFC normalize (breaks "cœur" → "cur" in PDF text)

### Verification rules
- After capture : open `articles/NN/parts/part-01.jpg` and `part-last.jpg` visually
- Check : article complete? Sidebar gone? Comments gone? Continuity OK?
- After compile : open PDF, verify each separator page numbered correctly + content order matches website chronology

## Country grouping

`country_order` array defines order. Country headers shown on cover TOC. Sources renumbered sequentially across countries (01, 02... starting fresh per country group is opt-in via `restart_numbering: true`).

Examples country codes : SN, ML, GM, BJ, CI, CD, NG, GH, MA, DZ, TN, EG, ZA...

## Tools required

- Node.js 18+
- Puppeteer-core + system Chrome
- npm packages : `puppeteer-core`, `pdf-lib`, `sharp`, `@cliqz/adblocker-puppeteer`, `cross-fetch`, `pdf-to-img` (optional, for embedding source PDFs)

## Output structure

```
output_dir/
├── COMPILATION.pdf                  # main deliverable
├── articles/NN-shortname/
│   ├── full.jpg
│   └── parts/part-NN.jpg
├── pdfs/                            # downloaded source PDFs (if any)
└── results.json                     # manifest
```

## Examples

See `examples/sources.example.json` for the full template, and `examples/random-test.json` for a ready-to-run example.

## Limitations

- **Adblock not 100%** : regional ad networks not in EasyList may slip through. Use manual fallback or add custom domain blocks per source.
- **Anti-bot pages** : sites with Cloudflare challenge → use Wayback Machine snapshot URL.
- **Paywalls** : not bypassed. Use archived versions when accessible.
- **JS-heavy SPAs** : may need longer `longwait: true` per source.
