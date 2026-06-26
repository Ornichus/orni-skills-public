---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
---

# Frontend Slides Skill

> **Version** : 1.6.0 | Upstream zarazhang/frontend-slides + Niveau 3 Nimbe Liquid Glass v3.0 + Phase 2 Uiverse (~78 composants) + Phase 3 Deck Patterns + Mermaid diagrams (Phase 1 Q5) + Phase 4 Golden document-type + Phase 5 Style « Nimbe » (preset v2.0.0)

> **Source upstream** : https://github.com/zarazhangrui/frontend-slides (MIT, @zarazhangrui)
> **Integration Orni-skills** : voir `README-ORNI.md` pour origine, philosophie d'intégration et guide de choix vs Marp.
> **Styles brandés (Niveau 2 RoboNuggets)** : voir `styles/README.md` pour catalogue (nimbe, etc.). Argument `--style {nom}` pour invoquer un brand book.
> **Niveau 3 — Liquid Glass Components** (style Nimbe) : voir `styles/nimbe/components/SHOWCASE.html` (preview 17 sections + ~78 composants + 3 deck patterns) + `COMPONENTS.md` (doc API). Activation : `<link rel="stylesheet" href="liquid-glass.css">` + `<link rel="stylesheet" href="liquid-glass-extended.css">`. Comprend : phones animés (notif/chat/lockscreen), buttons (7 variants), inputs glass (search/range/checkbox/aurore/conic), loaders (orbit/wave/ring/blob/treefrog/falcon/squid), charts V2 replay-on-view, KPI metrics, mockups laptop rich, cards 3D/flip/glow/pricing + 18 cartes Uiverse adaptées (vampirebat, eagle, elephant, newt, fly, cyber, lionfish, treefrog, robin, liger, rat, dingo, owl, dodo, lion, lizard, soft-dingo), data display (avatars/timeline/calendrier/notif bell/voice wave), feedback (alerts/toasts/tooltips), navigation (breadcrumb/hamburger), patterns backgrounds (3 animés : dolphin/earwig/lion).
> **Phase 2 (2026-04-27)** : 29 composants Uiverse adaptés au style Nimbe Liquid Glass (sections 02 Buttons +2, 03 Inputs +2, 04 Loaders +3, 13 UI Elements +1 switch, 15 NEW "Cartes Showcase Uiverse" 18 cards, 16 NEW "Patterns Backgrounds" 3). Tous theme-aware dark+light. Class prefix `.uv-{type}-{slug}`. Composants non-verbatim — adaptations CSS variables Nimbe uniquement.
> **Phase 3 (2026-04-28) — ADN du système de présentation** : 3 deck patterns réutilisables exposés via `nimbe-deck-helpers.js` (lib autonome, ~200 lignes) + section 17 SHOWCASE démo. (1) **Sidebar lexique** `.lex-sidebar` — nav gauche fixe avec slides cliquables, état persisté localStorage. (2) **Overlay pattern** `.overlay-glass` + `[data-overlay-open]` — détails à la demande sur clic, focus trap + Esc + backdrop close, theme-aware, print-friendly. (3) **Slide Nav** via IntersectionObserver (remplace scroll listener fragile). API : `NimbeDeck.init()` câble les 3 ensemble (sidebar synchro nav). Doc : `COMPONENTS.md` sections 9, 10, 11. Vision : slides minimalistes, contenu détaillé externalisé en overlays — l'orateur déclenche la profondeur seulement quand l'audience le demande.
> **Phase 4 (2026-06-12) — GOLDEN document-type** : le **standard du verre v2** (`styles/nimbe/golden/LIQUID-GLASS-STANDARD-v2.html`, classe `.lg` source unique) sert de **référence à imiter** pour transformer une note ou un document en deck liquid-glass (slide synthèse, overlays de détail, lexique, simulateurs ; validé visuellement + fonctionnellement). Il assemble : le standard du verre + Deck Grammar (slide synthèse → overlay détail `↗` → lexique clic → simulateur) + outillage utilisateur. **Règles apprises (obligatoires)** : (1) **Tokens texte dual-theme `--c-*`** — jamais `var(--nimbe-*)` en `color:` direct : les couleurs brand foncées sont illisibles en dark ; définir `--c-blue/--c-red/--c-violet/--c-cyan/--c-gold/--c-green/--c-orange` foncées en light, claires en dark. (2) **Contraste overlays** : panel à `rgb(tint/.93)` light / `.95` dark — le verre 46 % est illisible pour la lecture longue. (3) **Toolbar utilisateur** : thème + édition WYSIWYG `[data-editable]` (auto-tag des contenus d'overlays `h3,p,td,th,.eyebrow` AVANT assignation des eids) + panneau `Aa` (facteurs `--fs-all/--fs-h1…--fs-small` × clamp, et marge latérale `--mx` 0–200 %) + mini-barre sélection (police px par élément + drag translate de la carte `.lg` parente, persistés `localStorage`, neutralisés en print via `[data-moved]`). (4) **Export PDF** = `window.print()` + `@media print` : forcer `html,body{height:auto;overflow:visible}` (sinon Chromium imprime UNE page), palette light forcée, `.lg` opaque `.95`, masquer TOUS les indicateurs d'interaction (`.arrow`, soulignés `.lex-term`, sliders, `.btn`) ET les textes d'appel à l'action (wrapper `<span class="cta">` masqué print), overlays imprimés en annexes (`position:static` + titre `.print-annex`). (5) **Mode édition** : clic texte = éditer, la flèche `↗`/les `.btn` ouvrent quand même l'overlay. (6) **Représentations** : pipeline serpentin 2 rangées (badges ronds + flèches + dot animé) pour les chaînes de process ; barres fixes en verre teinté `--pc` pour les paliers — préférer les valeurs fixes aux sliders quand la donnée n'est pas paramétrable. (7) **Validation obligatoire** : boucle Playwright headless — gate console/overflow + screenshot PAR slide (attendre ≥ 1,2 s après scrollIntoView : les reveals `.rv` durent 0,6 s + délais) + tests fonctionnels + `node --check` sur le script extrait avant tout test (piège guillemets courbes).
> **Phase 5 (2026-06-13) — Style « NIMBE » (preset v2.0.0)** : le style maison Nimbe (ex « Liquid Glass v2 ») est officiellement nommé **Nimbe** (halos de lumière colorée derrière le verre dépoli). `styles/nimbe/preset.css` **réécrit en v2.0.0** : aligné sur le standard du verre (`.lg`, `LIQUID-GLASS-STANDARD-v2.html`), tokens texte dual-theme `--c-*` **reversés dans le standard + le preset** (lisibilité dark+light — comblement de la dette Phase 4), convention **cyan `#16b6c9` = « Équipe »** (`.row-team`/`.tag.team`/`.b-team`), et nouveau composant **configurateur à règle métier ancrée** (`.builder-*`/`.bt-*` + état `.totals.invalid`/`.team-chip.bad`/`.banner.warn` + correctif 1-clic). Démo de référence : `styles/nimbe/components/NIMBE-DEMO.html` (charge le vrai `preset.css` — validée Playwright : 0 erreur console / 0 overflow / règle métier OK). `--style nimbe` inchangé. Le `.lg` reste le nom **technique** de la surface ; **Nimbe** = nom du **style**.

---

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:

- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:

- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type    | Maximum Content                                           |
| ------------- | --------------------------------------------------------- |
| Title slide   | 1 heading + 1 subtitle + optional tagline                 |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid  | 1 heading + 6 cards maximum (2x3 or 3x2)                  |
| Code slide    | 1 heading + 8-10 lines of code                            |
| Quote slide   | 1 quote (max 3 lines) + attribution                       |
| Image slide   | 1 heading + 1 image (max 60vh height)                     |
| Diagram slide | 1 heading + 1 Mermaid diagram + max ~60 words caption     |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**

### Mode C: Modification Rules

When enhancing existing presentations, viewport fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Must have `max-height: min(50vh, 400px)`. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** `.slide` has `overflow: hidden`, new elements use `clamp()`, images have viewport-relative max-height, content fits at 1280x720
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

**When adding images to existing slides:** Move image to new slide or reduce other content first. Never add images without checking if existing content already fills the viewport.

---

## Phase 1: Content Discovery (New Presentations)

**Ask ALL questions in a single AskUserQuestion call** so the user fills everything out at once:

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options: Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation

**Question 2 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only

**Question 4 — Inline Editing** (header: "Editing"):
Do you need to edit text directly in the browser after generation? Options:

- "Yes (Recommended)" — Can edit text in-browser, auto-save to localStorage, export file
- "No" — Presentation only, keeps file smaller

**Remember the user's editing choice — it determines whether edit-related code is included in Phase 3.**

**Question 5 — Diagrams / Visualisations** (header: "Diagrams", multiSelect: true):
Will the deck need any diagrams or data visualisations? Options:

- A) None — text/cards only
- B) Flowchart / decision tree (Mermaid `graph LR` or `graph TD`)
- C) Timeline / Gantt (project roadmap, chronology)
- D) Architecture / network (components + relations)
- E) Data / KPIs (charts via uPlot, ApexCharts, or Mermaid `pie`)
- F) Mix — multiple diagram types

**If A is chosen, skip diagram setup in Phase 3.** Otherwise, in Phase 3 include the Mermaid v11 setup from [html-template.md](html-template.md) "Diagram Integration" section (script tag + `mermaid.initialize` with `useMaxWidth: false` on every chart type — the v11 default shrinks SVGs to ~200px). Match Mermaid theme to the chosen style preset (see the table in html-template.md).

> **[DIFFERE] Phase 2 preview Mermaid** — for now, Phase 2 style previews stay text-only (no live diagram render). The diagram answer from Q5 only drives Phase 3 generation. Adding interactive Mermaid preview to Phase 2 is queued but not implemented.

If user has content, ask them to share it.

### Step 1.2: Image Evaluation (if images provided)

If user selected "No images" → skip to Phase 2.

If user provides an image folder:

1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **View each image** — Use the Read tool (Claude is multimodal)
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm via AskUserQuestion** (header: "Outline"): "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

**Logo in previews:** If a usable logo was identified, embed it (base64) into each style preview in Phase 2 — the user sees their brand styled three different ways.

---

## Phase 2: Style Discovery

**This is the "show, don't tell" phase.** Most people can't articulate design preferences in words.

### Step 2.0: Style Path

Ask how they want to choose (header: "Style"):

- "Show me options" (recommended) — Generate 3 previews based on mood
- "I know what I want" — Pick from preset list directly

**If direct selection:** Show preset picker and skip to Phase 3. Available presets are defined in [STYLE_PRESETS.md](STYLE_PRESETS.md).

### Step 2.1: Mood Selection (Guided Discovery)

Ask (header: "Vibe", multiSelect: true, max 2):
What feeling should the audience have? Options:

- Impressed/Confident — Professional, trustworthy
- Excited/Energized — Innovative, bold
- Calm/Focused — Clear, thoughtful
- Inspired/Moved — Emotional, memorable

### Step 2.2: Generate 3 Style Previews

Based on mood, generate 3 distinct single-slide HTML previews showing typography, colors, animation, and overall aesthetic. Read [STYLE_PRESETS.md](STYLE_PRESETS.md) for available presets and their specifications.

| Mood                | Suggested Presets                                  |
| ------------------- | -------------------------------------------------- |
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical       |
| Excited/Energized   | Creative Voltage, Neon Cyber, Split Pastel         |
| Calm/Focused        | Notebook Tabs, Paper & Ink, Swiss Modern           |
| Inspired/Moved      | Dark Botanical, Vintage Editorial, Pastel Geometry |

Save previews to `.claude-design/slide-previews/` (style-a.html, style-b.html, style-c.html). Each should be self-contained, ~50-100 lines, showing one animated title slide.

Open each preview automatically for the user.

### Step 2.3: User Picks

Ask (header: "Style"):
Which style preview do you prefer? Options: Style A: [Name] / Style B: [Name] / Style C: [Name] / Mix elements

If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 (text, or text + curated images) and style from Phase 2.

If images were provided, the slide outline already incorporates them from Step 1.2. If not, CSS-generated visuals (gradients, shapes, patterns) provide visual interest — this is a fully supported first-class path.

**Before generating, read these supporting files:**

- [html-template.md](html-template.md) — HTML architecture and JS features
- [viewport-base.css](viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference for the chosen feeling

**Key requirements:**

- Single self-contained HTML file, all CSS/JS inline
- Include the FULL contents of viewport-base.css in the `<style>` block
- Use fonts from Fontshare or Google Fonts — never system fonts
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Style selection** — Proceed to Phase 2 for style discovery
4. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)

---

## Phase 5: Delivery

1. **Clean up** — Delete `.claude-design/slide-previews/` if it exists
2. **Open** — Use `open [filename].html` to launch in browser
3. **Summarize** — Tell the user:
   - File location, style name, slide count
   - Navigation: Arrow keys, Space, scroll/swipe, click nav dots
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - If inline editing was enabled: Hover top-left corner or press E to enter edit mode, click any text to edit, Ctrl+S to save

---

## Phase 6: Share & Export (Optional)

After delivery, **ask the user:** _"Would you like to share this presentation? I can deploy it to a live URL (works on any device including phones) or export it as a PDF."_

Options:

- **Deploy to URL** — Shareable link that works on any device
- **Export to PDF** — Universal file for email, Slack, print
- **Both**
- **No thanks**

If the user declines, stop here. If they choose one or both, proceed below.

### 6A: Deploy to a Live URL (Vercel)

This deploys the presentation to Vercel — a free hosting platform. The link works on any device (phones, tablets, laptops) and stays live until the user takes it down.

**If the user has never deployed before, guide them step by step:**

1. **Check if Vercel CLI is installed** — Run `npx vercel --version`. If not found, install Node.js first (`brew install node` on macOS, or download from https://nodejs.org).

2. **Check if user is logged in** — Run `npx vercel whoami`.
   - If NOT logged in, explain: _"Vercel is a free hosting service. You need an account to deploy. Let me walk you through it:"_
     - Step 1: Ask user to go to https://vercel.com/signup in their browser
     - Step 2: They can sign up with GitHub, Google, email — whatever is easiest
     - Step 3: Once signed up, run `vercel login` and follow the prompts (it opens a browser window to authorize)
     - Step 4: Confirm login with `vercel whoami`
   - Wait for the user to confirm they're logged in before proceeding.

3. **Deploy** — Run the deploy script:

   ```bash
   bash scripts/deploy.sh <path-to-presentation>
   ```

   The script accepts either a folder (with index.html) or a single HTML file.

4. **Share the URL** — Tell the user:
   - The live URL (from the script output)
   - That it works on any device — they can text it, Slack it, email it
   - To take it down later: visit https://vercel.com/dashboard and delete the project
   - The Vercel free tier is generous — they won't be charged

**Deployment gotchas:**

- **Local images/videos must travel with the HTML.** The deploy script auto-detects files referenced via `src="..."` in the HTML and bundles them. But if the presentation references files via CSS `background-image` or unusual paths, those may be missed. **Before deploying, verify:** open the deployed URL and check that all images load. If any are broken, the safest fix is to put the HTML and all its assets into a single folder and deploy the folder instead of a standalone HTML file.
- **Prefer folder deployments when the presentation has many assets.** If the presentation lives in a folder with images alongside it (e.g., `my-deck/index.html` + `my-deck/logo.png`), deploy the folder directly: `bash scripts/deploy.sh ./my-deck/`. This is more reliable than deploying a single HTML file because the entire folder contents are uploaded as-is.
- **Filenames with spaces work but can cause issues.** The script handles spaces in filenames, but Vercel URLs encode spaces as `%20`. If possible, avoid spaces in image filenames. If the user's images have spaces, the script handles it — but if images still break, renaming files to use hyphens instead of spaces is the fix.
- **Redeploying updates the same URL.** Running the deploy script again on the same presentation overwrites the previous deployment. The URL stays the same — no need to share a new link.

### 6B: Export to PDF

This captures each slide as a screenshot and combines them into a PDF. Perfect for email attachments, embedding in documents, or printing.

**Note:** Animations and interactivity are not preserved — the PDF is a static snapshot. This is normal and expected; mention it to the user so they're not surprised.

1. **Run the export script:**

   ```bash
   bash scripts/export-pdf.sh <path-to-html> [output.pdf]
   ```

   If no output path is given, the PDF is saved next to the HTML file.

2. **What happens behind the scenes** (explain briefly to the user):
   - A headless browser opens the presentation at 1920x1080 (standard widescreen)
   - It screenshots each slide one by one
   - All screenshots are combined into a single PDF
   - The script needs Playwright (a browser automation tool) — it will install automatically if missing

3. **If Playwright installation fails:**
   - The most common issue is Chromium not downloading. Run: `npx playwright install chromium`
   - If that fails too, it may be a network/firewall issue. Ask the user to try on a different network.

4. **Deliver the PDF** — The script auto-opens it. Tell the user:
   - The file location and size
   - That it works everywhere — email, Slack, Notion, Google Docs, print
   - Animations are replaced by their final visual state (still looks great, just static)

**PDF export gotchas:**

- **First run is slow.** The script installs Playwright and downloads a Chromium browser (~150MB) into a temp directory. This happens once per run. Warn the user it may take 30-60 seconds the first time — subsequent exports within the same session are faster.
- **Slides must use `class="slide"`.** The export script finds slides by querying `.slide` elements. If the presentation uses a different class name, the script will report "0 slides found" and fail. All presentations generated by this skill use `.slide`, so this only matters for externally-created HTML.
- **Local images must be loadable via HTTP.** The script starts a local server and loads the HTML through it (so Google Fonts and relative image paths work). If images use absolute filesystem paths (e.g., `src="/Users/name/photo.png"`) instead of relative paths (e.g., `src="photo.png"`), they won't load. Generated presentations always use relative paths, but converted or user-provided decks might not — check and fix if needed.
- **Local images appear in the PDF** as long as they are in the same directory as (or relative to) the HTML file. The export script serves the HTML's parent directory over HTTP, so relative paths like `src="photo.png"` resolve correctly — including filenames with spaces. If images still don't appear, check: (1) the image files actually exist at the referenced path, (2) the paths are relative, not absolute filesystem paths like `/Users/name/photo.png`.
- **Large presentations produce large PDFs.** Each slide is captured as a full 1920x1080 PNG screenshot. An 18-slide deck can produce a ~20MB PDF. If the PDF exceeds 10MB, ask the user: _"The PDF is [size]. Would you like me to compress it? It'll look slightly less sharp but the file will be much smaller."_ If yes, re-run the export with the `--compact` flag:
  ```bash
  bash scripts/export-pdf.sh <path-to-html> [output.pdf] --compact
  ```
  This renders at 1280x720 instead of 1920x1080, typically cutting file size by 50-70% with minimal visual difference.

---

## Supporting Files

| File                                               | Purpose                                                              | When to Read              |
| -------------------------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| [STYLE_PRESETS.md](STYLE_PRESETS.md)               | 12 curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| [viewport-base.css](viewport-base.css)             | Mandatory responsive CSS — copy into every presentation              | Phase 3 (generation)      |
| [html-template.md](html-template.md)               | HTML structure, JS features, code quality standards                  | Phase 3 (generation)      |
| [animation-patterns.md](animation-patterns.md)     | CSS/JS animation snippets and effect-to-feeling guide                | Phase 3 (generation)      |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction                             | Phase 4 (conversion)      |
| [scripts/deploy.sh](scripts/deploy.sh)             | Deploy slides to Vercel for instant sharing                          | Phase 6 (sharing)         |
| [scripts/export-pdf.sh](scripts/export-pdf.sh)     | Export slides to PDF                                                 | Phase 6 (sharing)         |
| [README-ORNI.md](README-ORNI.md)                   | Origine, integration Orni, comparaison vs marp-presentations         | Avant install             |
