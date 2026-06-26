# PROTOCOLE — Capture & Compilation d'articles web en PDF

Version 1.0 — Apr 2026

Référence pour MCP/Skill futur. Consolide toutes les règles apprises.

---

## OBJECTIF

Compiler un PDF lisible regroupant N articles web sourcés. Chaque article :
- Capturé propre (article seul, sans pollution)
- Inséré dans PDF avec mise en page optimale (zéro whitespace inutile)

---

## PHASE 1 — CAPTURE

### 1.1 Préparation environnement

- **Tool** : Puppeteer (Node.js) avec Chrome système
- **Viewport initial** : 1920×1080
- **User-Agent** : Chrome desktop récent
- **Lang headers** : `Accept-Language: fr-FR,fr;q=0.9,en;q=0.8`
- **Timeout navigation** : 90s networkidle2, fallback 60s domcontentloaded

### 1.2 Anti-bot / Wayback fallback

Si site bloque (403/captcha) :
1. Tenter Wayback Machine via `https://archive.org/wayback/available?url=...`
2. Utiliser snapshot le plus récent
3. Marquer `source: 'wayback'` dans manifest

### 1.3 Blocage requêtes ad/tracking

`page.setRequestInterception(true)` + abort sur :
```
doubleclick.net, googleadservices.com, googlesyndication.com,
adservice.google.com, adsystem.com, amazon-adsystem.com,
pagead2.googlesyndication.com, criteo.com, taboola.com,
outbrain.com, mgid.com, facebook.com/tr, connect.facebook.net,
analytics.google.com, google-analytics.com,
scorecardresearch.com, quantserve.com
```

### 1.4 Chargement page

1. Navigate URL
2. Wait `networkidle2` (90s) → fallback `domcontentloaded` (60s)
3. Wait fixe : 4-8s (longer pour Wayback / sites lents)
4. Cliquer bouton "Refuser cookies" / "Reject" / "Continuer sans accepter" / "Décliner"
5. Wait 1-2s

### 1.5 Lazy-load trigger

Scroll progressif jusqu'au bas pour déclencher lazy images/iframes :
```js
await new Promise(r => {
  let t = 0;
  const i = setInterval(() => {
    scrollBy(0, 600); t += 600;
    if (t >= document.documentElement.scrollHeight) { clearInterval(i); r(); }
  }, 80);
});
```

Puis `scrollTo(0, 0)` + wait 1s.

### 1.6 Neutralisation sticky/fixed

Inject CSS :
```css
* { animation: none !important; transition: none !important; }
*[style*="position:fixed"], *[style*="position:sticky"] { position: static !important; }
header, nav, .navbar, .sticky, [class*="sticky"], [class*="fixed-"] { position: static !important; }
body { padding-top: 0 !important; }
```

Plus JS : `getComputedStyle(el).position === 'fixed'/'sticky'` → `el.style.position = 'static'`.

### 1.7 Removal universel sécuritaire

⚠️ **MINIMAL** pour éviter de casser l'article. Ne pas inclure `[class*="comment"]` ou `[id*="ad-"]` qui ont des faux-positifs.

```
#wm-ipp-base, #wm-ipp, #donato-secondary  (Wayback toolbar)
.cookie-banner, #cookie-banner, #tarteaucitron, .tarteaucitron
iframe
ins.adsbygoogle, .adsbygoogle, [class*="adsbygoogle"]
[class*="advert"], [id^="aswift"], [id^="div-gpt"]
.sharedaddy, .jp-relatedposts
```

### 1.8 Removal spécifique par site (extraRemove)

À déterminer via **probe DOM** avant capture finale. Pattern :
1. Naviguer page une première fois
2. Identifier conteneur article (selector)
3. Identifier dans/autour : sidebar, related, comments, share, footer, ads inline
4. Établir selectors précis dans `extraRemove`

Exemples par CMS :
- **WordPress + theme générique** : `.entry-footer, .author-bio, #comments`
- **Joomla K2** : `.itemRatingBlock, .itemSocialSharing, .itemRelated, .itemNavigation, .itemAuthorBlock`
- **Site d'actualité custom (exemple)** : `.category-post__sidebar, .comments__wrap, .post-sidebar-featured`
- **Portail multi-rubriques (exemple)** : `.section-related-posts, .section-comments, .col-sidebar, .sidebar-widget`
- **TagDiv (Newspaper theme)** : `.tdb_single_related, .td_block_related_posts, .td-post-tags`

⚠️ **Ne JAMAIS** mettre dans extraRemove un selector qui matche le conteneur article lui-même (ex : `#tdb-autoload-article` est l'article lui-même selon le thème).

### 1.9 Détection conteneur article

**Selectors par ordre de spécificité** (premier match valide) :
1. Selectors site-spécifiques (probe-driven)
2. `article .entry-content`, `article .post-content`, `article .article-content`
3. `article`
4. `[itemprop=articleBody]`
5. `.entry-content`, `.post-content`, `.article-content`
6. `main article`
7. **Fallback heuristique** : div avec densité texte max (txtLen / height) parmi candidats > 400px hauteur

Critères validation : `height > 200px AND textLength > 500 chars`.

### 1.10 Inclusion titre H1

Si conteneur article ne contient pas H1 :
- Chercher H1 du document
- Si H1 est < 1200px au-dessus du conteneur → étendre `top` jusqu'à H1 - 30px

Aussi essayer : `.article-title`, `.post-title`, `.entry-title`, `.item-title`.

### 1.11 Capture screenshot

1. `page.setViewport({ width: 1920, height: min(articleHeight + 400, 16000) })`
2. Re-neutraliser après resize (sticky peut réapparaître)
3. `page.screenshot({ type: 'jpeg', quality: 88, fullPage: true })`

### 1.12 Crop bounding box

Sharp extract :
```js
const { left, top, width, height } = articleBounds;
sharp(buf).extract({ left, top, width, height })
```

→ Article-only, ZÉRO sidebar latéral.

### 1.13 Découpage en sections

- Hauteur section : 1080px
- **Overlap : 60px** entre sections (évite de couper mid-line)
- Skip sections < 100px (résidus)

### 1.14 Détection sections blanches

Sharp stats :
```js
const stats = await sharp(buf).stats();
const totalStdDev = stats.channels.reduce((s, c) => s + c.stdev, 0);
if (totalStdDev < 12) skip;  // section quasi-uniforme = blanche
```

### 1.15 Output structure

```
articles/NN-shortname/
├── full.jpg          (image article complète)
└── parts/
    ├── part-01.jpg
    ├── part-02.jpg
    └── ...
```

`results.json` manifest : id, shortname, url, source, status, title, articleHeight, articleWidth, sections, selectorUsed.

---

## PHASE 2 — COMPILATION PDF

### 2.1 Format

- Page de garde : A4 portrait (595.28 × 841.89 pt)
- Page séparateur : A4 portrait
- Page contenu : **adaptive page sizing**

### 2.2 Page de garde

- Titre principal taille 28pt
- Sous-titre taille 14pt gris
- Date + nb sources gris
- Ligne séparation
- TOC : numéro + titre wrap 2 lignes max
- Badge `[Wayback]` si applicable, taille 8pt orange, à droite
- ⚠️ Si badge wayback : réduire largeur texte TOC pour pas chevaucher

### 2.3 Page séparateur (1 par source)

- Top-gauche : `SOURCE NN` gris taille 11pt
- Si wayback : badge orange "Source archivée — Wayback" top-droite
- Centre : titre source taille **dynamique 14-28pt** (fitTitleSize)
  - Auto-shrink jusqu'à fit en 6 lignes max
- Pied : URL en gris taille 8pt (wrap 3 lignes max)

### 2.4 Page contenu (adaptive)

**Règle clé** : zéro whitespace.

```
drawW = USABLE_W (largeur fixe = A4_W - 2×margin)
drawH = drawW × (img.height / img.width)
pageH = drawH + footerH + 2×margin   (capé à 1.6×A4_H)
```

→ Page sized exactement pour l'image. Image fit largeur 100%.

Si image très haute (> 1.6×A4) : scale down hauteur.

### 2.5 Footer page contenu

- Gauche : `Source NN — shortname` gris 8pt
- Droite : `Section X/Y` gris 8pt
- Y = M/2 (centré dans marge basse)

### 2.6 Encoding texte (WinAnsi safe)

Helvetica standard ne supporte pas tout Unicode. Helper `clean()` :

```js
function clean(text) {
  let s = String(text).normalize('NFC');
  // Smart quotes → ASCII
  s = s.replace(/[“”„‟]/g, '"');
  s = s.replace(/[‘’‚‛]/g, "'");
  s = s.replace(/[–—―]/g, '-');
  s = s.replace(/…/g, '...');
  s = s.replace(/ /g, ' ');
  // Combining diacriticals (failed NFC)
  s = s.replace(/[̀-ͯ]/g, '');
  // Whitespace normalize
  s = s.replace(/\s+/g, ' ');
  // Drop chars hors WinAnsi range
  s = s.replace(/[^ -~ -ÿŒœŠšŸŽžƒˆ˜‰€™]/g, '');
  return s;
}
```

Toujours wrapper `drawText` avec `clean()`.

### 2.7 Skip JPGs corrompus

Si JPG < 4KB → ignore. Sinon `pdf.embedJpg` peut crash.

---

## PHASE 3 — VALIDATION VISUELLE

### 3.1 Server local

```bash
cd output-dir && python -m http.server 8765
```

### 3.2 Per-source visual check

Via Agent Browser, ouvrir :
- `http://localhost:8765/articles/NN-shortname/full.jpg` (vue ensemble)
- `http://localhost:8765/articles/NN-shortname/parts/part-01.jpg` (début)
- `http://localhost:8765/articles/NN-shortname/parts/part-XX.jpg` (fin)
- `http://localhost:8765/COMPILATION.pdf` (PDF final)

### 3.3 Critères validation

✅ Doit contenir :
- H1/titre article
- Photo principale article
- Body article complet
- Signature/auteur, date

❌ Ne doit PAS contenir :
- Header/nav site
- Footer site
- Sidebar (PLUS LUS, articles populaires/similaires/à lire aussi)
- Section commentaires + formulaire commentaire
- Pubs (banner, inline, overlay)
- Boutons partage social après article
- Newsletter/subscribe widget
- Tags/mots-clés
- Articles précédent/suivant nav
- Article previous/next links

### 3.4 Itération

Si défaut détecté :
1. Identifier root cause (probe DOM)
2. Mettre à jour `extraRemove` ou `selectors`
3. Re-capture seul article concerné
4. Re-compile PDF

---

## PHASE 4 — ANTI-PATTERNS À ÉVITER

❌ **Universal removal trop large** : `[class*="comment"]`, `[id*="ad-"]`, `aside`, `.sidebar` → faux-positifs (matchent classes article-related innocentes).

❌ **Removal du conteneur article** : ex `#tdb-autoload-article` est l'article lui-même selon le thème, pas une pub.

❌ **Pages multi-image stacked** : 2 sections par page = trop petit, illisible.

❌ **Page A4 fixe pour image landscape** : whitespace excessif top/bottom.

❌ **Slicing sans overlap** : coupe mid-line, dernière ligne tronquée.

❌ **Skip Unicode normalize** : "cœur" → "cur", combining diacritics crash.

❌ **Pas de horizontal crop** : sidebar à droite reste dans capture.

❌ **clipBox dans pdf-lib drawImage** : n'existe pas, image redessinée plein.

❌ **NAO PDF intégré tel quel** : texte vectoriel non cohérent avec autres screenshots → rasteriser ou skip.

---

## PHASE 5 — STRUCTURE FUTURE MCP/Skill

### 5.1 Inputs

```json
{
  "sources": [
    {
      "id": "01",
      "shortname": "site-name",
      "url": "https://...",
      "selectors": ["specific-selector", "fallback-1", "fallback-2"],
      "extraRemove": ["site-specific-removal-selectors"],
      "useHeuristic": false,
      "longwait": false
    }
  ],
  "output_dir": "./output",
  "compile_options": {
    "title": "...",
    "subtitle": "...",
    "skip_ids": ["04"]
  }
}
```

### 5.2 Outputs

```
output/
├── COMPILATION.pdf
├── articles/NN-shortname/{full.jpg, parts/}
├── results.json
└── PROTOCOLE.md (this file)
```

### 5.3 Sub-agents possibles

- **Probe agent** : analyse DOM 1 site, retourne selectors recommandés
- **Capture agent** : exécute capture 1 source
- **Validator agent** : ouvre JPGs via http server, score qualité, flag issues
- **Compiler agent** : génère PDF final

Mode mono-orchestrateur recommandé pour < 20 sources (overhead multi-agent > gain).

---

## CHECKLIST RAPIDE — chaque source

```
[ ] URL accessible (sinon Wayback)
[ ] Probe DOM → selectors article
[ ] Probe DOM → selectors sidebar/comments/related/ads/CTA
[ ] Capture avec request blocking + neutralize + crop H+W
[ ] Section overlap 60px
[ ] Skip blank
[ ] Verify visual : full.jpg + part-01.jpg + part-last.jpg
[ ] Cocher critères 3.3
[ ] Re-itérer si nécessaire
```
