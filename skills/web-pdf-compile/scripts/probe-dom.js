#!/usr/bin/env node
// Probe DOM of a URL to identify article selectors and tail elements
// Usage: node probe-dom.js <url>

import puppeteer from 'puppeteer-core';

const CHROME_PATHS = {
  win32: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  darwin: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  linux: '/usr/bin/google-chrome',
};

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const url = process.argv[2];
  if (!url) {
    console.error('Usage: node probe-dom.js <url>');
    process.exit(1);
  }

  const chromePath = CHROME_PATHS[process.platform];
  const browser = await puppeteer.launch({
    executablePath: chromePath, headless: 'new',
    defaultViewport: { width: 1920, height: 1080 },
    args: ['--no-sandbox'],
  });

  try {
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 Chrome/131');
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
    await wait(5000);

    const probe = await page.evaluate(() => {
      const out = { article: [], related: [], comments: [], ads: [], sidebar: [] };

      ['article', 'main', '.entry-content', '.post-content', '.article-content', '.article-body', '.itemFullText', '.itemBody', '.story-body', '.tdb_single_content', '.td-post-content', '.single_post_content_wrapper', '.category-post__post', '.article__content', '[itemprop="articleBody"]'].forEach((sel) => {
        let els; try { els = document.querySelectorAll(sel); } catch { return; }
        for (const el of els) {
          const r = el.getBoundingClientRect();
          const t = (el.textContent || '').trim().length;
          if (r.height > 200 && t > 500) {
            out.article.push({ sel, h: Math.round(r.height), w: Math.round(r.width), top: Math.round(r.top + scrollY), txt: t, density: Math.round(t / r.height * 10) / 10 });
            break;
          }
        }
      });

      ['[class*="related"]', '[class*="similar"]', '[class*="similaire"]', '[class*="latest"]', '[class*="connexes"]', '.related-posts'].forEach((sel) => {
        let els; try { els = document.querySelectorAll(sel); } catch { return; }
        for (const el of els) {
          const r = el.getBoundingClientRect();
          if (r.height > 50) out.related.push({ sel, cls: (el.className || '').toString().slice(0, 60), id: el.id, h: Math.round(r.height), top: Math.round(r.top + scrollY) });
        }
      });

      ['[class*="comment"]', '[id*="comment"]', '[class*="commentaire"]', '#disqus_thread'].forEach((sel) => {
        let els; try { els = document.querySelectorAll(sel); } catch { return; }
        for (const el of els) {
          const r = el.getBoundingClientRect();
          if (r.height > 50) out.comments.push({ sel, cls: (el.className || '').toString().slice(0, 60), id: el.id, h: Math.round(r.height), top: Math.round(r.top + scrollY) });
        }
      });

      ['iframe', '[class*="advert"]', '[class*="adsbygoogle"]', 'ins.adsbygoogle', '.code-block'].forEach((sel) => {
        let els; try { els = document.querySelectorAll(sel); } catch { return; }
        for (const el of els) {
          const r = el.getBoundingClientRect();
          if (r.width > 100 && r.height > 50) out.ads.push({ sel, cls: (el.className || '').toString().slice(0, 50), w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top + scrollY) });
        }
      });

      ['aside', '[class*="sidebar"]'].forEach((sel) => {
        let els; try { els = document.querySelectorAll(sel); } catch { return; }
        for (const el of els) {
          const r = el.getBoundingClientRect();
          if (r.height > 50) out.sidebar.push({ sel, cls: (el.className || '').toString().slice(0, 60), h: Math.round(r.height), top: Math.round(r.top + scrollY) });
        }
      });

      return {
        title: document.title,
        h1: document.querySelector('h1')?.textContent?.trim().slice(0, 100),
        scrollH: document.documentElement.scrollHeight,
        ...out,
      };
    });

    console.log('\n=== PROBE RESULTS ===');
    console.log(`URL: ${url}`);
    console.log(`Title: ${probe.title}`);
    console.log(`H1: ${probe.h1}`);
    console.log(`Page height: ${probe.scrollH}px\n`);

    console.log('--- Article candidates (use first match in selectors[]) ---');
    probe.article.slice(0, 8).forEach((a) => console.log(`  ${a.sel}  ${a.w}x${a.h}px  density=${a.density}  text=${a.txt}ch`));

    console.log('\n--- Tail elements to add to extraRemove[] ---');
    if (probe.related.length) { console.log('Related:'); probe.related.slice(0, 5).forEach((a) => console.log(`  ${a.sel} .${a.cls}  h=${a.h}`)); }
    if (probe.comments.length) { console.log('Comments:'); probe.comments.slice(0, 5).forEach((a) => console.log(`  ${a.sel} .${a.cls}#${a.id}  h=${a.h}`)); }
    if (probe.ads.length) { console.log('Ads:'); probe.ads.slice(0, 8).forEach((a) => console.log(`  ${a.sel} .${a.cls}  ${a.w}x${a.h}`)); }
    if (probe.sidebar.length) { console.log('Sidebar:'); probe.sidebar.slice(0, 5).forEach((a) => console.log(`  ${a.sel} .${a.cls}  h=${a.h}`)); }

    console.log('\n--- Suggested config ---');
    console.log(JSON.stringify({
      selectors: probe.article.slice(0, 3).map((a) => a.sel),
      extraRemove: [
        ...new Set([
          ...probe.related.slice(0, 3).map((a) => '.' + (a.cls.split(' ')[0] || a.sel.replace(/[\[\]"*=]/g, ''))),
          ...probe.comments.slice(0, 3).map((a) => a.id ? `#${a.id}` : '.' + (a.cls.split(' ')[0] || '')),
          ...probe.ads.slice(0, 5).map((a) => '.' + (a.cls.split(' ')[0] || a.sel.replace(/[\[\]"*=]/g, ''))),
        ].filter((s) => s && s !== '.' && s !== '#')),
      ],
    }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
