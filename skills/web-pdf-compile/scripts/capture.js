#!/usr/bin/env node
// Capture all sources defined in input JSON
// Usage: node capture.js <sources.json>

import puppeteer from 'puppeteer-core';
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import fetch from 'cross-fetch';
import { PuppeteerBlocker } from '@ghostery/adblocker-puppeteer';

const CHROME_PATHS = {
  win32: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  darwin: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  linux: '/usr/bin/google-chrome',
};

const SAFE_UNIVERSAL = [
  '#wm-ipp-base', '#wm-ipp', '#donato-secondary',
  '.cookie-banner', '#cookie-banner', '#tarteaucitron', '.tarteaucitron',
  'iframe', 'ins.adsbygoogle', '.adsbygoogle', '[class*="adsbygoogle"]',
  '[class*="advert"]', '[id^="aswift"]', '[id^="div-gpt"]',
  '.sharedaddy', '.jp-relatedposts',
];

const NEUTRALIZE_CSS = `
  * { animation: none !important; transition: none !important; }
  *[style*="position:fixed"], *[style*="position: fixed"],
  *[style*="position:sticky"], *[style*="position: sticky"] { position: static !important; }
  header, nav, .navbar, .sticky, [class*="sticky"], [class*="fixed-"] { position: static !important; }
  body { padding-top: 0 !important; }
`;

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const SECTION_H = 1080;
const OVERLAP = 60;
const BLANK_THRESHOLD = 12;

async function neutralize(page, extras) {
  await page.addStyleTag({ content: NEUTRALIZE_CSS });
  await page.evaluate((all) => {
    document.querySelectorAll('header, nav, div, aside, section').forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.position === 'fixed' || cs.position === 'sticky') el.style.position = 'static';
    });
    for (const sel of all) {
      try { document.querySelectorAll(sel).forEach((el) => el.remove()); } catch {}
    }
  }, [...SAFE_UNIVERSAL, ...(extras || [])]);
}

async function findBounds(page, sels, useHeuristic) {
  return await page.evaluate((s, h) => {
    function attachH1(top) {
      const h1 = document.querySelector('h1');
      if (h1) {
        const hr = h1.getBoundingClientRect();
        const ht = Math.floor(hr.top + window.scrollY);
        if (ht < top && top - ht < 1200) return Math.max(0, ht - 30);
      }
      for (const sel of ['.article-title', '.post-title', '.entry-title', '.item-title', 'h2.title']) {
        const el = document.querySelector(sel);
        if (el) {
          const r = el.getBoundingClientRect();
          const t = Math.floor(r.top + window.scrollY);
          if (t < top && top - t < 1200) return Math.max(0, t - 30);
        }
      }
      return top;
    }
    for (const sel of s) {
      let el; try { el = document.querySelector(sel); } catch { continue; }
      if (el) {
        const r = el.getBoundingClientRect();
        if (r.height > 200) {
          const top = Math.max(0, Math.floor(r.top + window.scrollY));
          return {
            top: attachH1(top),
            bottom: Math.ceil(r.bottom + window.scrollY) + 30,
            left: Math.max(0, Math.floor(r.left + window.scrollX) - 20),
            width: Math.min(Math.ceil(r.width) + 40, 1920),
            selector: sel,
          };
        }
      }
    }
    if (h) {
      let best = null;
      for (const el of document.querySelectorAll('div, article, main, section')) {
        const r = el.getBoundingClientRect();
        const t = (el.textContent || '').trim().length;
        if (r.height > 400 && r.height < window.innerHeight * 30 && t > 1000) {
          const d = t / r.height;
          if (!best || d > best.density) {
            best = {
              density: d,
              top: Math.floor(r.top + window.scrollY),
              bottom: Math.ceil(r.bottom + window.scrollY),
              left: Math.max(0, Math.floor(r.left + window.scrollX) - 20),
              width: Math.min(Math.ceil(r.width) + 40, 1920),
            };
          }
        }
      }
      if (best) return { ...best, top: attachH1(best.top), selector: 'heuristic' };
    }
    return null;
  }, sels, useHeuristic || false);
}

async function isBlank(buf) {
  try {
    const stats = await sharp(buf).stats();
    return stats.channels.reduce((s, c) => s + c.stdev, 0) < BLANK_THRESHOLD;
  } catch { return false; }
}

async function processArticle(item, blocker, outDir, chromePath) {
  const articleDir = path.join(outDir, 'articles', `${item.id}-${item.shortname}`);
  const partsDir = path.join(articleDir, 'parts');
  fs.rmSync(articleDir, { recursive: true, force: true });
  fs.mkdirSync(partsDir, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: 'new',
    defaultViewport: { width: 1920, height: 1080 },
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--lang=fr-FR,fr', '--disable-blink-features=AutomationControlled'],
  });

  try {
    const page = await browser.newPage();
    if (blocker) await blocker.enableBlockingInPage(page);
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36');
    await page.setExtraHTTPHeaders({ 'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8' });

    let response;
    try {
      response = await page.goto(item.url, { waitUntil: 'networkidle2', timeout: 90000 });
    } catch {
      response = await page.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    }
    const status = response ? response.status() : 0;
    if (status >= 400) return { id: item.id, status: 'http-error', code: status };

    await wait(item.longwait ? 8000 : 5000);

    await page.evaluate(() => {
      const kw = ['refuser', 'reject', 'continuer sans accepter', 'décliner', 'decline', 'no thanks', 'non merci'];
      const els = document.querySelectorAll('button, a, [role=button], input[type=button]');
      for (const e of els) {
        const t = (e.textContent || e.value || '').toLowerCase().trim();
        if (kw.some((k) => t.includes(k))) { try { e.click(); } catch (_) {} return; }
      }
    });
    await wait(1500);

    await page.evaluate(async () => {
      await new Promise((r) => {
        let total = 0;
        const i = setInterval(() => {
          window.scrollBy(0, 600);
          total += 600;
          if (total >= document.documentElement.scrollHeight) { clearInterval(i); r(); }
        }, 80);
      });
    });
    await wait(2000);
    await page.evaluate(() => window.scrollTo(0, 0));
    await wait(800);
    await neutralize(page, item.extraRemove);
    await wait(1000);

    const bounds = await findBounds(page, item.selectors, item.useHeuristic);
    if (!bounds) return { id: item.id, status: 'no-article-found' };

    await page.setViewport({ width: 1920, height: Math.min(bounds.bottom - bounds.top + 400, 16000) });
    await wait(1000);
    await neutralize(page, item.extraRemove);
    await wait(700);
    const fb = await findBounds(page, item.selectors, item.useHeuristic);
    const top = fb?.top ?? bounds.top;
    const bottom = fb?.bottom ?? bounds.bottom;
    const left = fb?.left ?? bounds.left;
    const width = fb?.width ?? bounds.width;

    const buf = await page.screenshot({ type: 'jpeg', quality: 88, fullPage: true });
    const meta = await sharp(buf).metadata();
    const cropTop = Math.max(0, Math.min(top, meta.height - 100));
    const cropH = Math.min(bottom - cropTop, meta.height - cropTop);
    const cropLeft = Math.max(0, Math.min(left, meta.width - 100));
    let cropW = Math.min(width, meta.width - cropLeft);

    if (cropH < 200) return { id: item.id, status: 'crop-too-small' };

    let article = await sharp(buf).extract({ left: cropLeft, top: cropTop, width: cropW, height: cropH }).jpeg({ quality: 88 }).toBuffer();

    // Horizontal trim : remove uniform whitespace columns (L/R only).
    // Why : sites like routard.com centre article content via Tailwind max-w-Nxl mx-auto,
    // leaving white padding inside the wrapper. Without trim, captured JPG has internal
    // L/R margins that vary per source and render with inconsistent visual width in PDF.
    try {
      const probe = await sharp(article).raw().toBuffer({ resolveWithObject: true });
      const { data, info } = probe;
      const ch = info.channels;
      const W = info.width;
      const H = info.height;
      const PAD = 8;                  // safety padding kept after trim
      const SAMPLE_STEP = Math.max(8, Math.floor(H / 200));
      const COLOR_THRESHOLD = 240;    // pixel >= this on RGB = considered "white-ish"

      function isWhiteCol(x) {
        for (let y = 0; y < H; y += SAMPLE_STEP) {
          const off = (y * W + x) * ch;
          if (data[off] < COLOR_THRESHOLD || data[off + 1] < COLOR_THRESHOLD || data[off + 2] < COLOR_THRESHOLD) return false;
        }
        return true;
      }

      let leftEdge = 0;
      while (leftEdge < W && isWhiteCol(leftEdge)) leftEdge++;
      let rightEdge = W - 1;
      while (rightEdge > leftEdge && isWhiteCol(rightEdge)) rightEdge--;

      const trimL = Math.max(0, leftEdge - PAD);
      const trimR = Math.min(W - 1, rightEdge + PAD);
      const newW = trimR - trimL + 1;

      // Only apply if trim removes >5% of width (otherwise article was already tight)
      if (newW > 200 && (W - newW) / W > 0.05) {
        article = await sharp(article).extract({ left: trimL, top: 0, width: newW, height: H }).jpeg({ quality: 88 }).toBuffer();
        cropW = newW;
      }
    } catch (e) {
      // trim failed, fallback to original article (non-blocking)
    }
    fs.writeFileSync(path.join(articleDir, 'full.jpg'), article);

    const total = Math.ceil(cropH / (SECTION_H - OVERLAP));
    let kept = 0, skipped = 0;
    for (let i = 0; i < total; i++) {
      const t = i * (SECTION_H - OVERLAP);
      const h = Math.min(SECTION_H, cropH - t);
      if (h < 100) { skipped++; continue; }
      const sec = await sharp(article).extract({ left: 0, top: t, width: cropW, height: h }).jpeg({ quality: 88 }).toBuffer();
      if (await isBlank(sec)) { skipped++; continue; }
      kept++;
      fs.writeFileSync(path.join(partsDir, `part-${String(kept).padStart(2, '0')}.jpg`), sec);
    }

    return {
      id: item.id, status: 'ok',
      title: await page.evaluate(() => document.title),
      articleHeight: cropH, articleWidth: cropW,
      sections: kept, sectionsSkipped: skipped,
      articleDir, url: item.url, source: item.source, country: item.country,
      selectorUsed: bounds.selector,
    };
  } finally {
    await browser.close();
  }
}

async function main() {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error('Usage: node capture.js <sources.json>');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const outDir = path.resolve(config.output_dir || './output');
  fs.mkdirSync(path.join(outDir, 'articles'), { recursive: true });
  fs.mkdirSync(path.join(outDir, 'pdfs'), { recursive: true });

  const chromePath = config.chrome_path || CHROME_PATHS[process.platform];
  if (!fs.existsSync(chromePath)) {
    console.error(`Chrome not found at: ${chromePath}`);
    console.error('Set "chrome_path" in config or install Chrome');
    process.exit(1);
  }

  console.log('Loading adblock filter lists...');
  const blocker = await PuppeteerBlocker.fromPrebuiltAdsAndTracking(fetch);

  const results = [];
  for (const source of config.sources) {
    process.stdout.write(`[${source.id}] ${source.shortname} ... `);
    try {
      const r = await processArticle(source, blocker, outDir, chromePath);
      results.push({ ...source, ...r });
      console.log(r.status, r.sections != null ? `(${r.sections} kept, ${r.sectionsSkipped} blank, ${r.articleHeight}x${r.articleWidth} sel=${r.selectorUsed})` : '');
    } catch (e) {
      console.log('ERROR:', e.message);
      results.push({ ...source, status: 'error', error: e.message });
    }
  }

  fs.writeFileSync(path.join(outDir, 'results.json'), JSON.stringify(results, null, 2));
  const ok = results.filter((r) => r.status === 'ok').length;
  console.log(`\nFinal: ${ok}/${results.length} OK`);
  console.log(`Output: ${outDir}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
