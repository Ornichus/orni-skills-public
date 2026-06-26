# web-pdf-compile

Capture web articles cleanly (article-only — no ads/sidebar/comments) and compile them into a structured PDF dossier organized by country or category.

Standalone Node.js skill — no framework dependency. Works as a Claude Code skill, a Cursor skill, an **MCP server for Claude Desktop**, or just a CLI you run by hand.

**Claude Desktop users** : skip to [`CLAUDE-DESKTOP-SETUP.md`](CLAUDE-DESKTOP-SETUP.md) for plug-and-play install.

## Why

- Press review compilation
- Investigative journalism evidence dossier (multi-source)
- Research bibliography with embedded source captures
- Archive of news coverage on a topic across multiple sites
- Legal documentation requiring source preservation

Ready-to-run example : `examples/random-test.json` = 3 diverse public sources (Wikipedia, StackOverflow, GNU), good for a first compile.

## Prerequisites

- **Node.js 18+** ([nodejs.org](https://nodejs.org/))
- **Google Chrome** installed at the system level (Puppeteer-core uses the system Chrome, not a bundled Chromium — much smaller install).
  - Windows : `C:\Program Files\Google\Chrome\Application\chrome.exe`
  - macOS : `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
  - Linux : `/usr/bin/google-chrome`
  - Custom path : set `"chrome_path"` in your sources JSON.

## Install

```bash
# 1. Extract the skill folder anywhere on your machine
# 2. Install dependencies (~150 MB, mostly puppeteer-core + sharp + pdf-lib)
cd web-pdf-compile
npm install
```

Or use the bundled scripts :
- Windows : double-click `install.bat`
- macOS / Linux : `./install.sh`

## Quick start

```bash
# 1. Probe a site to find which CSS selectors target the article body
npm run probe -- https://example.com/article-url

# 2. Copy examples/sources.example.json and edit with your URLs + selectors

# 3. Capture each article (creates JPG slices)
npm run capture -- my-sources.json

# 4. Compile the final PDF
npm run compile -- my-sources.json
```

The PDF lands at `<output_dir>/COMPILATION.pdf`.

## sources.json format

```json
{
  "title": "Project title",
  "subtitle": "Optional subtitle",
  "output_dir": "./output/my-project",
  "country_order": [
    { "code": "FR", "name": "France" },
    { "code": "US", "name": "United States" }
  ],
  "sources": [
    {
      "id": "01",
      "shortname": "site-slug",
      "country": "FR",
      "url": "https://...",
      "selectors": [".article-body", "main", "article"],
      "extraRemove": [".sidebar", ".comments", ".related"],
      "longwait": false,
      "useHeuristic": false,
      "source": null
    }
  ]
}
```

| Field | Default | Purpose |
|-------|---------|---------|
| `selectors` | `[]` | Ordered list of CSS selectors trying to identify the article body. First match with `height > 200` wins. |
| `extraRemove` | `[]` | Extra CSS selectors to delete before capture (sidebars, ads, popups specific to the site). |
| `longwait` | `false` | Wait 8 s instead of 5 s after page load (for SPA / JS-heavy sites). |
| `useHeuristic` | `false` | Fallback to text-density heuristic if no selector matches. |
| `source` | `null` | Set to `"wayback"` if the URL is a Wayback Machine snapshot — adds a badge in the PDF. |

## Output structure

```
output_dir/
├── COMPILATION.pdf                 # main deliverable
├── articles/NN-shortname/
│   ├── full.jpg                    # full captured article
│   └── parts/part-NN.jpg           # paginated sections
└── results.json                    # manifest
```

## Layout features

- **Cover page** with grouped TOC by country
- **Separator page** per source (country header + title + URL + Wayback badge)
- **Adaptive page sizing** : page height = scaled image height (zero whitespace top/bottom)
- **Auto-trim** of left/right whitespace columns inside each section (handles sites that center content via `max-width` CSS — uniform L/R margins across all sources)
- **Footer** "Source NN — shortname / Section X/Y" on every page

## Critical rules (capture quality)

A clean capture must include : H1 / title, hero photo, full article body, signature.

A clean capture must NOT include : header/nav, footer, sidebar, comments, ads, share buttons, newsletter banners, related posts.

If the adblocker can't catch a regional ad network (some regional networks aren't in EasyList) :
1. Open the article in your own browser (Brave / Firefox + uBlock Origin)
2. Take screenshots manually
3. Drop them into `articles/NN-shortname/parts/` (replacing or alongside auto captures)
4. Keep chronological order in filenames

See `PROTOCOLE.md` for the full ruleset and 8 documented anti-patterns.

## Manual selector fallback (probe)

```bash
npm run probe -- https://target-site.com/some-article
```

Returns suggested `selectors` and `extraRemove` you can paste into your `sources.json`. The probe also flags any sticky/fixed elements, ads, and sidebars detected.

## Limitations

- **Adblock not 100%** : regional ad networks not in EasyList may slip through → use the manual screenshot fallback.
- **Anti-bot pages** : sites with Cloudflare challenge cannot be auto-captured → use Wayback Machine snapshot URL with `"source": "wayback"`.
- **Paywalls** : not bypassed. Use archived versions when accessible.
- **JS-heavy SPAs** : may need `"longwait": true` per source.

## License

MIT — see `LICENSE`.

## Files

```
web-pdf-compile/
├── SKILL.md                  # Skill metadata + workflow (frontmatter triggers)
├── README.md                 # This file
├── PROTOCOLE.md              # Capture rules + anti-patterns
├── LICENSE                   # MIT
├── package.json              # Dependencies + npm scripts
├── install.sh / install.bat  # Convenience installers
├── scripts/
│   ├── capture.js            # Puppeteer + Ghostery adblock + L/R trim
│   ├── compile-pdf.js        # Adaptive PDF + country grouping
│   └── probe-dom.js          # Site selector probe helper
├── CLAUDE-DESKTOP-SETUP.md   # MCP server install for Claude Desktop
├── DISTRIBUTION.md           # How to ship this to a third party
├── scripts/mcp-server.js     # MCP server (stdio transport)
└── examples/
    ├── sources.example.json  # Generic template
    ├── smoke-test.json       # Wikipedia smoke test
    └── random-test.json      # 3 diverse sites
```

## MCP server (Claude Desktop, Claude Code, Cursor, ...)

The bundled `scripts/mcp-server.js` exposes the skill as Model Context Protocol tools. After `npm install`, point any MCP client at it :

```json
{
  "mcpServers": {
    "web-pdf-compile": {
      "command": "node",
      "args": ["/absolute/path/to/scripts/mcp-server.js"]
    }
  }
}
```

Two tools become available :
- `web_pdf_probe(url)` — suggest CSS selectors for an article URL
- `web_pdf_compile_dossier({title, sources, country_order?, output_dir?})` — full capture + PDF pipeline

See [`CLAUDE-DESKTOP-SETUP.md`](CLAUDE-DESKTOP-SETUP.md) for a step-by-step install on Windows / macOS / Linux.
