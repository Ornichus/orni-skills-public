#!/usr/bin/env node
// Compile captured articles into PDF
// Usage: node compile-pdf.js <sources.json>

import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import fs from 'fs';
import path from 'path';

const A4_W = 595.28;
const A4_H = 841.89;
const M = 14;
const USABLE_W = A4_W - M * 2;
const FOOTER_H = 14;
const MAX_PAGE_H = A4_H * 1.6;

function clean(text) {
  if (text == null) return '';
  let s = String(text).normalize('NFC');
  s = s.replace(/[“”„‟]/g, '"');
  s = s.replace(/[‘’‚‛]/g, "'");
  s = s.replace(/[–—―]/g, '-');
  s = s.replace(/…/g, '...');
  s = s.replace(/ /g, ' ');
  s = s.replace(/[̀-ͯ]/g, '');
  s = s.replace(/\s+/g, ' ');
  s = s.replace(/[^ -~ -ÿŒœŠšŸŽžƒˆ˜‰€™]/g, '');
  return s;
}

function dt(page, text, opts) {
  page.drawText(clean(text), opts);
}

function wrapToWidth(text, font, fontSize, maxWidth) {
  const words = clean(text).split(/\s+/);
  const lines = [];
  let cur = '';
  for (const w of words) {
    const test = cur ? cur + ' ' + w : w;
    if (font.widthOfTextAtSize(test, fontSize) > maxWidth && cur) { lines.push(cur); cur = w; }
    else cur = test;
  }
  if (cur) lines.push(cur);
  return lines;
}

function fitTitleSize(text, font, maxWidth, maxLines, maxSize, minSize) {
  for (let size = maxSize; size >= minSize; size -= 1) {
    const lines = wrapToWidth(text, font, size, maxWidth);
    if (lines.length <= maxLines) return { size, lines };
  }
  return { size: minSize, lines: wrapToWidth(text, font, minSize, maxWidth).slice(0, maxLines) };
}

async function addCoverPage(pdf, results, config) {
  const fontB = await pdf.embedFont(StandardFonts.HelveticaBold);
  const fontR = await pdf.embedFont(StandardFonts.Helvetica);
  const page = pdf.addPage([A4_W, A4_H]);

  dt(page, config.title || 'Compilation', { x: M, y: A4_H - 80, size: 28, font: fontB });
  if (config.subtitle) {
    dt(page, config.subtitle, { x: M, y: A4_H - 110, size: 14, font: fontR, color: rgb(0.3, 0.3, 0.3) });
  }
  dt(page, `${results.length} sources - généré ${new Date().toISOString().slice(0, 10)}`, {
    x: M, y: A4_H - 130, size: 10, font: fontR, color: rgb(0.5, 0.5, 0.5),
  });
  page.drawLine({ start: { x: M, y: A4_H - 145 }, end: { x: A4_W - M, y: A4_H - 145 }, thickness: 0.5, color: rgb(0.7, 0.7, 0.7) });

  const NUM_W = 22, BADGE_W = 60;
  let y = A4_H - 175;
  let prevCountry = null;
  for (const r of results) {
    if (y < 60) break;
    if (r.country !== prevCountry) {
      y -= 4;
      dt(page, (r.countryName || r.country || '').toUpperCase(), { x: M, y, size: 11, font: fontB, color: rgb(0.1, 0.1, 0.1) });
      page.drawLine({ start: { x: M + 100, y: y + 4 }, end: { x: A4_W - M, y: y + 4 }, thickness: 0.3, color: rgb(0.7, 0.7, 0.7) });
      y -= 16;
      prevCountry = r.country;
    }
    const isWayback = r.source === 'wayback';
    const textMaxW = USABLE_W - NUM_W - (isWayback ? BADGE_W + 8 : 0);
    dt(page, `${r.id}.`, { x: M, y, size: 10, font: fontB });
    const lines = wrapToWidth(r.title || r.shortname, fontR, 10, textMaxW).slice(0, 2);
    let yy = y;
    for (const l of lines) { dt(page, l, { x: M + NUM_W, y: yy, size: 10, font: fontR }); yy -= 12; }
    if (isWayback) dt(page, '[Wayback]', { x: A4_W - M - BADGE_W, y, size: 8, font: fontB, color: rgb(0.85, 0.4, 0) });
    y -= (lines.length * 12) + 6;
  }
}

async function addSeparatorPage(pdf, item) {
  const fontB = await pdf.embedFont(StandardFonts.HelveticaBold);
  const fontR = await pdf.embedFont(StandardFonts.Helvetica);
  const page = pdf.addPage([A4_W, A4_H]);

  const sourceLabel = item.countryName ? `SOURCE ${item.id} — ${item.countryName.toUpperCase()}` : `SOURCE ${item.id}`;
  dt(page, sourceLabel, { x: M, y: A4_H - M - 12, size: 11, font: fontB, color: rgb(0.5, 0.5, 0.5) });

  if (item.source === 'wayback') {
    page.drawRectangle({ x: A4_W - M - 165, y: A4_H - M - 18, width: 165, height: 16, color: rgb(0.95, 0.85, 0.7) });
    dt(page, 'Source archivée — Wayback', { x: A4_W - M - 159, y: A4_H - M - 14, size: 8, font: fontB, color: rgb(0.7, 0.35, 0) });
  }

  const title = item.title || item.shortname;
  const fit = fitTitleSize(title, fontB, USABLE_W, 6, 28, 14);
  const totalH = fit.lines.length * fit.size * 1.2;
  let yt = A4_H / 2 + totalH / 2;
  for (const l of fit.lines) { dt(page, l, { x: M, y: yt, size: fit.size, font: fontB }); yt -= fit.size * 1.2; }

  page.drawLine({ start: { x: M, y: A4_H / 2 - totalH / 2 - 16 }, end: { x: M + 80, y: A4_H / 2 - totalH / 2 - 16 }, thickness: 1, color: rgb(0.3, 0.3, 0.3) });

  if (item.url) {
    const urlLines = wrapToWidth(item.url, fontR, 8, USABLE_W);
    let yu = M + 20 + (Math.min(urlLines.length, 3) - 1) * 10;
    dt(page, 'Lien source :', { x: M, y: yu + 12, size: 8, font: fontB, color: rgb(0.5, 0.5, 0.5) });
    for (const l of urlLines.slice(0, 3)) { dt(page, l, { x: M, y: yu, size: 8, font: fontR, color: rgb(0.3, 0.3, 0.6) }); yu -= 10; }
  }
}

async function loadImage(pdf, filePath) {
  const bytes = fs.readFileSync(filePath);
  if (bytes.length < 4000) return null;
  const isPng = filePath.toLowerCase().endsWith('.png');
  try { return isPng ? await pdf.embedPng(bytes) : await pdf.embedJpg(bytes); }
  catch (e) { console.error(`  embed fail ${path.basename(filePath)}: ${e.message}`); return null; }
}

async function addContentPages(pdf, item, outDir) {
  const fontR = await pdf.embedFont(StandardFonts.Helvetica);
  const partsDir = path.join(item.articleDir || path.join(outDir, 'articles', `${item.originalId || item.id}-${item.shortname}`), 'parts');
  if (!fs.existsSync(partsDir)) return 0;
  const files = fs.readdirSync(partsDir).filter((f) => /\.(jpg|jpeg|png)$/i.test(f)).sort();
  if (!files.length) return 0;

  const validFiles = [];
  for (const f of files) {
    const img = await loadImage(pdf, path.join(partsDir, f));
    if (img) validFiles.push({ f, img });
  }
  if (!validFiles.length) return 0;

  let pageCount = 0;
  for (let i = 0; i < validFiles.length; i++) {
    const img = validFiles[i].img;
    const drawW = USABLE_W;
    const drawH = drawW * (img.height / img.width);
    const idealPageH = drawH + FOOTER_H + M * 2;
    const pageH = Math.min(idealPageH, MAX_PAGE_H);

    let finalDrawH = drawH;
    let finalDrawW = drawW;
    if (idealPageH > MAX_PAGE_H) {
      finalDrawH = MAX_PAGE_H - FOOTER_H - M * 2;
      finalDrawW = finalDrawH * (img.width / img.height);
    }

    const page = pdf.addPage([A4_W, pageH]);
    pageCount++;
    const x = (A4_W - finalDrawW) / 2;
    const y = M + FOOTER_H + (pageH - M * 2 - FOOTER_H - finalDrawH);
    page.drawImage(img, { x, y, width: finalDrawW, height: finalDrawH });

    const footerLeft = `Source ${item.id} — ${item.shortname}`;
    const footerRight = `Section ${i + 1}/${validFiles.length}`;
    dt(page, footerLeft, { x: M, y: M / 2, size: 8, font: fontR, color: rgb(0.5, 0.5, 0.5) });
    const rW = fontR.widthOfTextAtSize(clean(footerRight), 8);
    dt(page, footerRight, { x: A4_W - M - rW, y: M / 2, size: 8, font: fontR, color: rgb(0.5, 0.5, 0.5) });
  }
  return pageCount;
}

async function main() {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error('Usage: node compile-pdf.js <sources.json>');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const outDir = path.resolve(config.output_dir || './output');
  const resultsPath = path.join(outDir, 'results.json');
  if (!fs.existsSync(resultsPath)) {
    console.error(`results.json not found at ${resultsPath}. Run capture.js first.`);
    process.exit(1);
  }
  const all = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));

  const skip = new Set(config.skip_ids || []);
  const ordered = [];
  let counter = 0;

  if (config.country_order) {
    for (const country of config.country_order) {
      const code = typeof country === 'string' ? country : country.code;
      const name = typeof country === 'string' ? country : country.name;
      const items = all.filter((r) => r.country === code && r.status === 'ok' && !skip.has(r.id));
      for (const item of items) {
        counter++;
        const newId = String(counter).padStart(2, '0');
        ordered.push({ ...item, originalId: item.id, id: newId, countryName: name });
      }
    }
    // Append uncategorized items
    const uncategorized = all.filter((r) => r.status === 'ok' && !skip.has(r.id) && !ordered.find((o) => o.originalId === r.id));
    for (const item of uncategorized) {
      counter++;
      const newId = String(counter).padStart(2, '0');
      ordered.push({ ...item, originalId: item.id, id: newId, countryName: 'Autres' });
    }
  } else {
    for (const item of all.filter((r) => r.status === 'ok' && !skip.has(r.id))) {
      ordered.push({ ...item, originalId: item.id });
    }
  }

  console.log(`Compiling ${ordered.length} sources`);

  const pdf = await PDFDocument.create();
  pdf.setTitle(config.title || 'Compilation des sources');

  await addCoverPage(pdf, ordered, config);

  let total = 0;
  let prevCountry = null;
  for (const r of ordered) {
    if (r.countryName && r.countryName !== prevCountry) {
      console.log(`\n--- ${r.countryName} ---`);
      prevCountry = r.countryName;
    }
    process.stdout.write(`Source ${r.id} ${r.shortname}: `);
    await addSeparatorPage(pdf, r);
    const n = await addContentPages(pdf, r, outDir);
    total += n;
    console.log(`${n} pages`);
  }

  const finalPdf = path.join(outDir, 'COMPILATION.pdf');
  const bytes = await pdf.save();
  fs.writeFileSync(finalPdf, bytes);
  console.log(`\nFinal PDF: ${finalPdf} (${(bytes.length / 1024 / 1024).toFixed(2)} MB)`);
  console.log(`Total: 1 cover + ${ordered.length} sep + ${total} content = ${1 + ordered.length + total} pages`);
}

main().catch((e) => { console.error(e); process.exit(1); });
