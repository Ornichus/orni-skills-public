# Nimbe — Components Library (Niveau 3)

> **Version** : 1.0.0 | 8 familles de composants signature
> **Dépendance** : preset.css (variables CSS de base)
> **Activation** : `<link rel="stylesheet" href="components.css">` après preset.css

Les composants Niveau 3 enrichissent les slides au-delà des éléments base (eyebrow, card-bezel, KPI glass, marquee). Ils répondent à des besoins narratifs spécifiques : signal vivant, données animées, mockups premium, démos techniques, plans, brouillons, indicateurs visuels.

---

## Sommaire

1. [Motion Pads](#1-motion-pads) — `.motion-pulse` · `.motion-ripple` · `.motion-breath` · `.motion-glow`
2. [Animated Charts](#2-animated-charts) — `.chart-bar` · `.chart-line` · `.chart-pie` · `.chart-donut`
3. [UI Mockups](#3-ui-mockups) — `.mockup-phone` · `.mockup-laptop` · `.mockup-browser`
4. [Terminal](#4-terminal) — `.terminal` · `.terminal-prompt` · `.typewriter`
5. [Isometric](#5-isometric) — `.iso-cube` · `.iso-stack` · `.iso-grid-floor`
6. [Blueprint](#6-blueprint) — `.blueprint` · `.crop-mark` · `.blueprint-shape`
7. [Notebook](#7-notebook) — `.notebook` · `.doodle` · `.strike` · `.check`
8. [Data-viz](#8-data-viz) — `.gauge` · `.sparkline` · `.heatmap` · `.progress-radial` · `.counter`

---

## 1. Motion Pads

### `.motion-pulse` — Heartbeat ring

Cercle plein avec 2 rings d'expansion concentriques. Idéal pour signaler une activité continue (scan radar, broadcast, signal actif).

```html
<div class="motion-pulse">
  <svg width="20" height="20"><!-- icône --></svg>
</div>
```

### `.motion-ripple` — Touch interaction

Onde concentrique avec 3 dots décalés dans le temps (animation 3s linear).

```html
<div class="motion-ripple">
  <span></span><span></span><span></span>
</div>
```

### `.motion-breath` — Live status pill

Pill texte avec dot vert qui respire (box-shadow expansion). Pour status "en ligne", "production", "live".

```html
<span class="motion-breath">Live · Production</span>
```

### `.motion-glow` — Premium accent border

Conic-gradient rotatif autour d'une carte. Filter hue-rotate animé. Pour CTA premium, top metric, awards.

```html
<div class="motion-glow">
  <div class="motion-glow-inner">
    <!-- contenu -->
  </div>
</div>
```

---

## 2. Animated Charts

### `.chart-bar` — Bar chart vertical animé

Bars HTML pure (sans SVG). Animation `bar-grow` scale-Y depuis bottom, stagger 0.1s. Variante `.bar.accent` pour barre d'highlight (rouge).

```html
<div class="chart-bar">
  <div class="bar" style="height: 30%;"><span class="bar-label">2020</span></div>
  <div class="bar accent" style="height: 92%;"><span class="bar-label">2025</span></div>
</div>
```

### `.chart-line` — Line chart SVG draw

Path stroke-dasharray + dashoffset animé (line-draw 2s). Area fill séparée (line-fill 1s delay 1.4s). Points circles fade-in delay incrémental.

```html
<svg class="chart-line" viewBox="0 0 400 180" preserveAspectRatio="none">
  <defs>
    <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0027a3" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#0027a3" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <path class="area" d="..."/>
  <path class="line" d="..."/>
  <circle class="point" cx="50" cy="120" r="4"/>
</svg>
```

### `.chart-pie` — Pie CSS conic-gradient

Pure CSS conic-gradient. Animation `pie-spin-in` rotate -90→0 + scale 0.8→1. Hole central via `::after` (donut style). Labels `.value` + `.label` au centre via `.chart-pie-center`.

```html
<div class="chart-pie">
  <div class="chart-pie-center">
    <div class="value">62%</div>
    <div class="label">Adoption</div>
  </div>
</div>
```

### `.chart-donut` — Radial progress

SVG circle.progress avec stroke-dasharray (282.7 = 2π·45). `--donut-offset` contrôle remplissage (0 = full, 282.7 = empty). Animation `donut-fill` 1.6s.

```html
<div class="chart-donut" style="--donut-offset: 56;"><!-- 80% rempli -->
  <svg viewBox="0 0 100 100">
    <circle class="track" cx="50" cy="50" r="45"/>
    <circle class="progress" cx="50" cy="50" r="45"/>
  </svg>
  <div class="value">80%</div>
</div>
```

---

## 3. UI Mockups

### `.mockup-phone` — Phone notch + screen

Cadre 14×28rem, border-radius 2.5rem, box-shadow tinted bleu. Notch top via `.mockup-phone-notch`. Content via `.mockup-phone-content` (rows configurables).

```html
<div class="mockup-phone">
  <div class="mockup-phone-screen">
    <div class="mockup-phone-notch"></div>
    <div class="mockup-phone-content">
      <div class="row short"></div>
      <div class="row tall"></div>
    </div>
  </div>
</div>
```

### `.mockup-laptop` — Laptop screen + base

Aspect-ratio 16:10, base avec encoche centrale. Display configurable (gradient bleu par défaut, ou injection HTML/SVG).

```html
<div class="mockup-laptop">
  <div class="mockup-laptop-screen">
    <div class="mockup-laptop-display">
      <!-- contenu écran -->
    </div>
  </div>
  <div class="mockup-laptop-base"></div>
</div>
```

### `.mockup-browser` — Browser chrome bar + content

Barre 3 dots (rouge/jaune/vert) + URL bar + content area. Pour montrer dashboards, web apps.

```html
<div class="mockup-browser">
  <div class="mockup-browser-bar">
    <span class="dot r"></span>
    <span class="dot y"></span>
    <span class="dot g"></span>
    <span class="url">nimbe.example/dashboard</span>
  </div>
  <div class="mockup-browser-content">
    <!-- KPIs, charts, content -->
  </div>
</div>
```

---

## 4. Terminal

### `.terminal` — Code window premium

Fenêtre noir avec barre + lignes. Couleurs syntax : `.terminal-prompt` (bleu), `.terminal-cmd` (blanc), `.terminal-out` (gris), `.terminal-success` (vert), `.terminal-error` (rouge).

```html
<div class="terminal">
  <div class="terminal-bar">
    <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
    <span class="title">deploy.sh</span>
  </div>
  <div class="terminal-body">
    <span class="terminal-line"><span class="terminal-prompt">$</span> <span class="terminal-cmd">nimbe deploy</span></span>
    <span class="terminal-line"><span class="terminal-success">✓ Deploy successful</span></span>
    <span class="terminal-line">
      <span class="terminal-prompt">$</span>
      <span class="typewriter">nimbe status<span class="terminal-cursor"></span></span>
    </span>
  </div>
</div>
```

### `.typewriter` + `.terminal-cursor`

Animation typing 2.4s steps(30) + cursor blink 1s. Combinable.

---

## 5. Isometric

### `.iso-cube` — 3D cube perspective

6 faces transform-style preserve-3d. Animation float verticale 4s alternate. Pour visualiser containers, modules, services.

```html
<div class="isometric-stage">
  <div class="iso-cube">
    <div class="face top"></div>
    <div class="face bottom"></div>
    <div class="face front"></div>
    <div class="face back"></div>
    <div class="face left"></div>
    <div class="face right"></div>
  </div>
</div>
```

### `.iso-stack` — Empilement de blocs

3 blocs décalés en Y. Bloc 2 = accent rouge. Pour stacks tech, layers, niveaux.

```html
<div class="iso-stack">
  <div class="block"></div>
  <div class="block"></div>
  <div class="block"></div>
</div>
```

---

## 6. Blueprint

### `.blueprint` — Technical drawing grid

Fond bleu nuit + grid double (1rem fine + 5rem épais). 4 crop-marks aux coins (TL/TR/BL/BR). Title bar avec scale ratio.

```html
<div class="blueprint">
  <span class="crop-mark tl"></span>
  <span class="crop-mark tr"></span>
  <span class="crop-mark bl"></span>
  <span class="crop-mark br"></span>
  <div class="blueprint-title">
    <span>BP-01 · Architecture</span>
    <span>SCALE 1:1</span>
  </div>
  <div class="blueprint-shape">EDGE NODE</div>
</div>
```

### `.blueprint-shape`

Border dashed avec radius 4px. Représente entité technique dans schéma.

---

## 7. Notebook

### `.notebook` — Paper texture lined

Fond crème + lignes horizontales bleues + marge rouge gauche. Font Caveat 1.25rem (Google Fonts auto-importée par components.css).

```html
<div class="notebook">
  <div style="font-weight: 700; font-size: 1.5rem; color: var(--nimbe-blue);">Titre note</div>
  <span class="check">Item validé</span>
  <span class="strike">Item barré</span>
  <span class="doodle">Mot mis en avant</span>
</div>
```

### `.check` · `.strike` · `.doodle`

Helpers signature. `.check` ajoute ✓ vert. `.strike` line-through rouge. `.doodle` bleu gras.

⚠️ Le notebook ne respecte pas le toggle dark/light (papier crème volontaire en toute condition).

---

## 8. Data-viz

### `.gauge` — Semi-circle meter

SVG path semi-circle. `--gauge-offset` (0 → 314 = vide → plein). `--gauge-angle` (0 → 180deg) pour aiguille (si présente).

```html
<div class="gauge" style="--gauge-offset: 80;">
  <svg viewBox="0 0 200 100">
    <defs>
      <linearGradient id="gaugeGradient" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#a1140e"/>
        <stop offset="100%" stop-color="#4f8ef7"/>
      </linearGradient>
    </defs>
    <path class="track" d="M 20,100 A 80,80 0 0 1 180,100"/>
    <path class="fill" d="M 20,100 A 80,80 0 0 1 180,100"/>
  </svg>
  <div class="gauge-value">72</div>
</div>
```

### `.sparkline` — Mini line chart

SVG path stroke + area fill animé. Largeur viewBox 300×60 par défaut.

```html
<svg class="sparkline" viewBox="0 0 300 60" preserveAspectRatio="none">
  <path class="area" d="M 0,40 L ... L 300,12 L 300,60 L 0,60 Z"/>
  <path d="M 0,40 L ... L 300,12"/>
</svg>
```

### `.heatmap` — Activity dot-grid

Grid 12 colonnes (configurable via inline style). Cell levels : `.l1` `.l2` `.l3` `.l4` (intensité bleu) + `.r1` `.r2` (accent rouge).

```html
<div class="heatmap" style="grid-template-columns: repeat(7, 1fr);">
  <div class="cell"></div>
  <div class="cell l2"></div>
  <div class="cell l4"></div>
  <div class="cell r2"></div>
</div>
```

### `.progress-radial` — Conic-gradient progress

Pure CSS via conic-gradient. `--p` valeur 0-100.

```html
<div class="progress-radial" style="--p: 75;">
  <span class="progress-radial-value">75%</span>
</div>
```

### `.counter` — Stat hit number

Texte gradient bleu + Outfit 800 + size metric-xl. Pour count-up effects (JS optionnel).

```html
<div class="counter">12.4K</div>
```

---

## Règles d'usage

1. **Motion pads** : 1 par slide max (signal fort, pas saturer).
2. **Charts** : préférer 1 chart dominant sur slide dédiée plutôt que 4 mini-charts compactés.
3. **Mockups** : un mockup = preuve visuelle d'une fonctionnalité. Pas décoratif.
4. **Terminal** : usage limité aux slides techniques/dev/deploy. Trop "geek" pour pitch C-level.
5. **Isometric** : excellent pour archi cloud, infrastructure. Animation float subtile (pas de spin distractive).
6. **Blueprint** : rappelle ingénierie, plan technique. Cible audience souveraineté/infra.
7. **Notebook** : usage occasionnel pour brainstorm, MVP slide, anti-cliché AI.
8. **Data-viz** : combiner gauge + sparkline + counter sur slide dashboard. Garder même couleur dominante.

## Anti-patterns Niveau 3

- ❌ Mélanger blueprint + notebook sur même slide (collision de styles techniques)
- ❌ Saturer une slide avec 4+ motion pads (effet kitsch)
- ❌ Charts SVG sans animation (perd la signature premium)
- ❌ Mockup phone + laptop + browser sur même slide (overload device)
- ❌ Terminal lignes > 12 (illisible en plein écran)
- ❌ Heatmap > 100 cells (devient noise)

---

# Phase 3 — Deck Patterns (ADN du système de présentation)

> Ces trois patterns forment l'ossature des decks Nimbe : **slides condensées au maximum, navigation fluide, détails à la demande**. Ils sont conçus pour être copiés inline dans n'importe quel deck HTML standalone OU chargés via le helper `nimbe-deck-helpers.js`.

## 9. Sidebar Lexique (`.lex-sidebar`)

Navigation gauche fixe avec liste cliquable des slides. Les titres sont auto-extraits depuis chaque `<section class="slide">` (priorité h1 → h2 → eyebrow → fallback "Slide N"). État collapsed/expanded persisté en localStorage.

### Structure HTML

```html
<button class="lex-sidebar-toggle" aria-label="Toggle sidebar">☰</button>
<nav class="lex-sidebar" aria-label="Navigation slides">
  <div class="lex-sidebar-header">
    <span class="lex-sidebar-title">Sommaire</span>
  </div>
  <!-- .lex-sidebar-list est créée et peuplée par JS -->
</nav>
```

### Activation JS

```js
const sidebar = NimbeDeck.setupSidebar();
// ou avec options custom :
NimbeDeck.setupSidebar({
  slides: '.slide',
  sidebar: '.lex-sidebar',
  toggle: '.lex-sidebar-toggle',
  storageKey: 'mon-deck-sidebar'
});
```

### Comportement
- Auto-collapsed si `window.innerWidth < 1280` (premier load)
- Toggle hamburger bascule l'état + persiste localStorage
- Click sur item → `scrollIntoView({ behavior: 'smooth' })`
- Item `.active` synchro automatique via `setupSlideNav` (voir #11)

---

## 10. Overlay Pattern (`.overlay-glass` + `[data-overlay-open]`)

**ADN du système** : permet de garder les slides minimalistes (1 idée, peu de texte) tout en exposant des détails approfondis à la demande. L'utilisateur clique sur un item → un overlay glass plein écran s'ouvre avec le contenu détaillé.

### Cas d'usage typiques
- Carte produit → détails techniques + roadmap
- Chip "LLM" → comparatif des modèles
- Item "Tegmark scénario X" → développement complet
- Logo client → étude de cas

### Structure HTML

**Trigger** (n'importe quel élément) :

```html
<div class="card" data-overlay-open="llm-detail">
  <h3>LLM</h3>
  <p>Modèles de langage</p>
</div>
```

> Le JS ajoute automatiquement la class `.expandable-trigger` (curseur pointer + flèche `↗` au hover).

**Overlay container** (placé en fin de `<body>`, avant `<script>`) :

```html
<div class="overlay-glass" id="llm-detail" role="dialog" aria-modal="true" hidden>
  <button class="overlay-close" aria-label="Fermer">×</button>
  <div class="overlay-content">
    <h2>Large Language Models</h2>
    <p>Présentation détaillée…</p>
    <h3>Acteurs majeurs</h3>
    <ul>
      <li>OpenAI — GPT-4o, o1</li>
      <li>Anthropic — Claude 4.7</li>
      <li>Google DeepMind — Gemini 2</li>
    </ul>
  </div>
</div>
```

### Activation JS

```js
const overlays = NimbeDeck.setupOverlays();
// API utilisable depuis ailleurs si besoin :
overlays.open('llm-detail');
overlays.close(document.getElementById('llm-detail'));
overlays.closeAll();
```

### Comportement
- Click trigger → ouvre l'overlay correspondant (animation fade + scale-up 350ms)
- Fermeture : bouton ×, click backdrop, touche Escape
- `body.overlay-open` empêche scroll background
- Focus trap : focus auto sur bouton fermer à l'ouverture, restauré au trigger à la fermeture
- Compatible theme dark/light (background backdrop bascule via `:root[data-theme]`)

### Anti-patterns
- ❌ Imbriquer un overlay dans un autre (utiliser navigation séquentielle si besoin)
- ❌ Mettre du contenu critique uniquement dans un overlay (le PDF print ne le verra pas — voir section "Print")
- ❌ Plus de 6 overlays par slide (saturation cognitive — split en sous-slides)

### Print / PDF
Pour export PDF complet (overlays inclus inline), ajouter en fin de `<style>` :

```css
@media print {
  .overlay-glass { display: block !important; opacity: 1 !important;
                   position: static !important; padding: 1rem !important;
                   background: transparent !important; }
  .overlay-content { transform: none !important; max-width: 100% !important;
                     max-height: none !important; box-shadow: none !important; }
  .overlay-close, .lex-sidebar, .lex-sidebar-toggle, .nav-dots { display: none !important; }
}
```

---

## 11. Slide Nav (right dots + progress bar)

Indicateur visuel de progression : dots verticaux à droite + barre top. Synchronisation slide active via IntersectionObserver (plus fiable que scroll listener avec scroll-snap).

### Structure HTML

```html
<div class="progress-bar" id="progressBar"></div>
<div class="nav-dots" id="navDots"></div>
```

CSS minimal requis (à inclure si pas déjà dans le deck) :

```css
.progress-bar { position: fixed; top: 0; left: 0; height: 3px;
                background: linear-gradient(90deg, var(--nimbe-blue), var(--nimbe-red));
                width: 0%; z-index: 1000; transition: width 200ms; }
.nav-dots { position: fixed; right: 1rem; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 0.5rem; z-index: 999; }
.nav-dot { width: 0.5rem; height: 0.5rem; border-radius: 50%;
           background: var(--text-subtle); cursor: pointer; transition: all 200ms; }
.nav-dot.active { background: var(--nimbe-blue); transform: scale(1.4);
                  box-shadow: 0 0 8px var(--nimbe-blue-glow); }
.nav-dot:hover { background: var(--nimbe-blue-light); }
```

### Activation JS

```js
const nav = NimbeDeck.setupSlideNav({
  threshold: 0.55,                      // % visible pour activer la dot
  onActive: (idx) => { /* sync sidebar, track analytics, etc. */ }
});
```

### One-call init (sidebar + nav + overlays liés)

```js
const ctrl = NimbeDeck.init();
// ctrl.sidebar, ctrl.nav, ctrl.overlays disponibles
```

`init()` câble automatiquement le sidebar à `setActive()` via `onActive`, donc la dot active ET l'item sidebar actif restent synchro sans config.

---

## Anti-patterns Phase 3

- ❌ Sidebar avec > 50 entrées (illisible — split en sections ou skip overview slides)
- ❌ Overlay qui contient une autre slide complète (utiliser routing/SPA à la place)
- ❌ Trigger overlay sans indicateur visuel (le `.expandable-trigger ::after ↗` est essentiel)
- ❌ Désactiver l'IntersectionObserver pour revenir au scroll listener (perte de fiabilité scroll-snap)
- ❌ Forcer la sidebar visible sur mobile (<768px) — préférer collapsed par défaut

---

## 12. Configurateur à règle métier ancrée (`.builder-*` / `.totals.invalid`)

Composant interactif (style **Nimbe**) : un formulaire ajoute des lignes à une liste ; une **invariante métier** est revalidée à chaque changement et **peint un état visuel** quand elle est violée, avec correctif en un clic. Validé sur un deck de configuration de licences puis généralisé dans `preset.css`.

### Cas d'usage
- Configurateur de licences / d'offres avec contrainte (ex. « tout plan Équipe exige ≥ 1 siège admin »)
- Panier / devis avec règle de cohérence (quota minimum, dépendance entre options)
- Tout formulaire « liste + total » où une combinaison invalide doit être **signalée sans bloquer** la saisie

### Classes CSS (dans `preset.css`)
- Saisie : `.builder-form` + `.bf-field`/`.bf-grow`/`.bf-cap`/`.bf-input`/`.bf-select`/`.bf-add`/`.bf-hint`
- Liste + total : `.builder-grid` (2 col) → `.builder-table` (`.bt-head`/`.bt-body`/`.bt-row`, `.qty`, `.badge`+`.b-team`/`.b-ind`, `.bt-del`) + `.totals`
- États : `.totals.invalid` (cadre rouge) · `.team-chip` (`.ok`/`.bad`) · `.banner` (`.warn`/`.soft`, avec bouton correctif)
- Lignes « Équipe » : `.bt-row.team` (teinte cyan) — cohérent avec `.row-team` des tables `.ptable`

### Logique JS — l'invariante
Le cœur = une fonction `render()` qui recalcule l'état à **chaque mutation** (ajout / quantité / suppression) et applique/retire les classes :

```js
function render(){
  // ... rendu des lignes + totaux ...
  const tc = teamCounts();                  // agrège la donnée surveillée
  if (tc.total > 0 && tc.prem === 0){        // ← INVARIANTE VIOLÉE
    totWrap.classList.add('invalid');
    statusEl.className = 'team-chip bad';
    banner.className   = 'banner warn';      // bandeau + bouton correctif 1-clic
  } else {                                   // ← OK
    totWrap.classList.remove('invalid');
    statusEl.className = 'team-chip ok';
  }
}
```

Le **correctif 1-clic** est un bouton injecté dans `.banner.warn` qui appelle l'action de réparation (ex. `addItem('Administrateur', 'prem')`) → `render()` repasse l'état en valide.

### Démo de référence
`NIMBE-DEMO.html` (même dossier) — configurateur complet, **pré-rempli en état invalide** pour illustrer la règle. Charge le vrai `preset.css`. Validé Playwright (`~/.orni/visual-check/nimbe-check.js`) : 0 erreur console, 0 overflow, transition invalide→valide OK.

### Anti-patterns
- ❌ Bloquer la saisie (`disabled`) au lieu de signaler — l'utilisateur doit pouvoir construire **puis** corriger
- ❌ Valider seulement à la soumission — revalider à **chaque** mutation
- ❌ Signaler sans correctif — toujours offrir le bouton « réparer » dans le bandeau

