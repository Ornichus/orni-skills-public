"""Post-process Marp HTML to add navigation + dark/light toggle enhancements.

Usage: python marp_postprocess.py path/to/deck.html

Injects:
  - Full theme CSS (variables + dark/light mode) — injected here because Marpit
    scopes any <style> inside the markdown, breaking :root and body.* selectors.
  - Sommaire button (top-left) + keyboard shortcut 'H' -> navigates to slide 2
  - Clickable sommaire rows (any <td> containing just a page number navigates to that page)
  - Dark/Light toggle button (top-right) + keyboard shortcut 'D'
    Works by toggling `body.light-mode` class, which the theme CSS uses to swap CSS variables.
"""
import sys
from pathlib import Path

INJECT = r"""
<style>
/* ============================================================
   THEME CSS — injected post-Marp so :root / body.light-mode
   selectors are NOT scoped into section { } by Marpit.
   ============================================================ */

/* ===== VARIABLES (dark mode by default) ===== */
:root {
  --bg: #0f172a;
  --lead-bg: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --title: #a3bef4;
  --title-border: #3b71dc;
  --title-shadow: rgba(163,190,244,0.25);
  --lead-h1: #a3bef4;
  --strong: #a3bef4;
  --em: #d9a3f4;
  --link: #3b71dc;
  --code-bg: rgba(30,41,59,0.8);
  --code-color: #e2e8f0;
  --code-border: rgba(51,65,85,0.6);
  --pre-bg: rgba(30,41,59,0.8);
  --table-border: rgba(59,113,220,0.3);
  --table-header-bg: #0b1427;
  --table-row-odd: #1c2b49;
  --table-row-even: #0f172a;
  --container-bg: #0b1427;
  --container-border: #3b71dc;
  --pagination: #475569;

  /* ===== GENERATED PALETTE (HSL) — via gen_palette.py, N=6, offset=220 ===== */
  --l1-blue-bg:   #0b1427; --l2-blue-bg:   #1c2b49; --l3-blue-bg:   #304672;
  --l1-violet-bg: #1e0b27; --l2-violet-bg: #3a1c49; --l3-violet-bg: #5c3072;
  --l1-red-bg:    #270b14; --l2-red-bg:    #491c2b; --l3-red-bg:    #723046;
  --l1-orange-bg: #271e0b; --l2-orange-bg: #493a1c; --l3-orange-bg: #725c30;
  --l1-green-bg:  #14270b; --l2-green-bg:  #2b491c; --l3-green-bg:  #467230;
  --l1-cyan-bg:   #0b271e; --l2-cyan-bg:   #1c493a; --l3-cyan-bg:   #30725c;

  --blue-border:   #3b71dc; --blue-strong:   #a3bef4;
  --violet-border: #a73bdc; --violet-strong: #d9a3f4;
  --red-border:    #dc3b71; --red-strong:    #f4a3be;
  --orange-border: #dca73b; --orange-strong: #f4d9a3;
  --green-border:  #71dc3b; --green-strong:  #bef4a3;
  --cyan-border:   #3bdca7; --cyan-strong:   #a3f4d9;
}

/* ===== LIGHT MODE OVERRIDES ===== */
body.light-mode {
  --bg: #f1f5f9;
  --lead-bg: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 50%, #f1f5f9 100%);
  --text: #1e293b;
  --text-muted: #64748b;
  --title: #163a82;
  --title-border: #3b71dc;
  --title-shadow: rgba(22,58,130,0.12);
  --lead-h1: #163a82;
  --strong: #163a82;
  --em: #5e1682;
  --link: #163a82;
  --code-bg: #e2e8f0;
  --code-color: #1e40af;
  --code-border: #cbd5e1;
  --pre-bg: #e2e8f0;
  --table-border: rgba(59,113,220,0.35);
  --table-header-bg: #dfe6f5;
  --table-row-odd: #c7d3e9;
  --table-row-even: #f8fafc;
  --container-bg: #dfe6f5;
  --container-border: #3b71dc;
  --pagination: #94a3b8;

  /* ===== GENERATED PALETTE LIGHT (HSL) — via gen_palette.py ===== */
  --l1-blue-bg:   #dfe6f5; --l2-blue-bg:   #c7d3e9; --l3-blue-bg:   #a5b6d8;
  --l1-violet-bg: #eedff5; --l2-violet-bg: #dec7e9; --l3-violet-bg: #c7a5d8;
  --l1-red-bg:    #f5dfe6; --l2-red-bg:    #e9c7d3; --l3-red-bg:    #d8a5b6;
  --l1-orange-bg: #f5eedf; --l2-orange-bg: #e9dec7; --l3-orange-bg: #d8c7a5;
  --l1-green-bg:  #e6f5df; --l2-green-bg:  #d3e9c7; --l3-green-bg:  #b6d8a5;
  --l1-cyan-bg:   #dff5ee; --l2-cyan-bg:   #c7e9de; --l3-cyan-bg:   #a5d8c7;

  --blue-strong:   #163a82;
  --violet-strong: #5e1682;
  --red-strong:    #82163a;
  --orange-strong: #825e16;
  --green-strong:  #3a8216;
  --cyan-strong:   #16825e;
}

/* ===== SECTION BASE (force var-based bg/color) ===== */
/* Marp injects inline background-color / color on <section> from frontmatter.
   We override with !important so light-mode actually flips the slide. */
section {
  background-color: var(--bg) !important;
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Segoe UI', system-ui, sans-serif;
  padding: 1.8rem 2.5rem !important;
  font-size: 26px;
  display: flex !important;
  flex-direction: column !important;
  gap: 0.4rem !important;
}
/* Hierarchical spacing: H1 > H2 > H3 > paragraphe */
section > h1 { margin-top: 0 !important; margin-bottom: 1rem !important; }
section > h2 { margin-top: 0 !important; margin-bottom: 0.7rem !important; }
section > h3 { margin-top: 0.35rem !important; margin-bottom: 0.25rem !important; }
section > p, section > ul, section > ol { margin-top: 0.2rem !important; margin-bottom: 0.2rem !important; }
section > div, section > pre, section > table, section > figure { margin-top: 0.35rem !important; margin-bottom: 0.35rem !important; }
section > h2 + p, section > h2 + ul, section > h2 + div { margin-top: 0 !important; }
body.light-mode section {
  background-color: var(--bg) !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* ===== LEAD ===== */
section.lead {
  justify-content: center;
  align-items: center; text-align: center;
  background: var(--lead-bg) !important;
}
body.light-mode section.lead { background: var(--lead-bg) !important; }
section.lead h1 { font-size: 2.5em; margin-bottom: 0.1em; color: var(--lead-h1); text-shadow: 0 0 20px rgba(96,165,250,0.4); }
section.lead h2 { color: var(--text-muted); border: none; font-size: 1.2em; }
section.lead p { font-size: 1em; color: var(--text-muted); }

/* ===== TITRES ===== */
section h2 {
  color: var(--title);
  border-bottom: 3px solid var(--title-border);
  padding-bottom: 0.2em;
  font-size: 1.25em;
  text-shadow: 0 0 12px var(--title-shadow);
  margin: 0 0 0.2rem 0;
}
section h3 { color: var(--text); font-size: 1em; margin-bottom: 0.3rem; }

/* ===== TEXTE ===== */
section strong { color: var(--strong); text-shadow: 0 0 8px rgba(147,197,253,0.15); }
section em     { color: var(--em);     text-shadow: 0 0 8px rgba(196,181,253,0.15); }
section a      { color: var(--link);   text-shadow: 0 0 8px rgba(96,165,250,0.2); }

/* ===== CODE ===== */
section code {
  font-size: 0.78em;
  background: var(--code-bg);
  color: var(--code-color);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--code-border);
  box-shadow: 0 0 4px rgba(51,65,85,0.2);
}
section pre, section marp-pre,
div#\:\$p > svg > foreignObject > section pre,
div#\:\$p > svg > foreignObject > section marp-pre,
div#\:\$p > svg > foreignObject > section :is(pre, marp-pre) {
  border-radius: 8px !important;
  font-size: 0.75em !important;
  background: #1e293b !important;
  background-color: #1e293b !important;
  color: #e2e8f0 !important;
  border: 1px solid var(--code-border) !important;
  box-shadow: 0 0 8px rgba(59,130,246,0.08) !important;
  padding: 0.7rem 0.9rem !important;
}
body.light-mode section pre, body.light-mode section marp-pre,
body.light-mode div#\:\$p > svg > foreignObject > section pre,
body.light-mode div#\:\$p > svg > foreignObject > section marp-pre,
body.light-mode div#\:\$p > svg > foreignObject > section :is(pre, marp-pre) {
  background: #e2e8f0 !important;
  background-color: #e2e8f0 !important;
  color: #1e293b !important;
}
section pre code, section marp-pre code,
section pre *, section marp-pre * {
  background: transparent !important;
  background-color: transparent !important;
  color: inherit !important;
  box-shadow: none !important;
  border: none !important;
}

/* ===== TABLEAUX ===== */
section table {
  font-size: 0.78em;
  display: table !important;
  width: auto !important;
  max-width: 100% !important;
  table-layout: auto !important;
  border-collapse: separate !important;
  border-spacing: 0 !important;
  border: 1px solid var(--container-border) !important;
  background: var(--container-bg) !important;
  box-shadow: 0 0 16px rgba(0,0,0,0.25);
  border-radius: 10px;
  overflow: hidden;
  margin: 0 auto !important;
}
section table thead { display: table-header-group !important; }
section table tbody { display: table-row-group !important; }
section table tr { display: table-row !important; }

/* Cellules : centrees par defaut, sauf la 1ere colonne (labels) */
section td { text-align: center !important; }
section td:first-child { text-align: left !important; }
section th:first-child { text-align: left !important; }
section thead tr {
  background: var(--table-header-bg) !important;
  color: var(--title) !important;
}
body.light-mode section thead tr { color: #1e3a8a !important; }
section thead tr th:first-child { border-radius: 8px 0 0 0 !important; }
section thead tr th:last-child  { border-radius: 0 8px 0 0 !important; }
section th {
  padding: 8px 14px !important;
  font-weight: 700 !important;
  border: none !important;
  border-right: 1px solid rgba(59,130,246,0.25) !important;
  color: var(--title) !important;
}
body.light-mode section th { color: #1e3a8a !important; }
section th:last-child { border-right: none !important; }
section td {
  padding: 8px 14px !important;
  border: none !important;
  border-top: 1px solid var(--table-border) !important;
  border-right: 1px solid var(--table-border) !important;
  color: var(--text) !important;
}
section td:last-child { border-right: none !important; }
section tbody tr:last-child td:first-child { border-radius: 0 0 0 8px !important; }
section tbody tr:last-child td:last-child  { border-radius: 0 0 8px 0 !important; }
section tbody tr                { background: var(--table-row-odd) !important; }
section tbody tr:nth-child(even){ background: var(--table-row-even) !important; }

/* ===== LISTES ===== */
section li { margin-bottom: 0.3em; }
section li::marker { color: var(--link); }

/* ===== PAGINATION ===== */
section::after { color: var(--pagination); }

/* ===== IMAGES (subtle darker tint behind SVG diagrams) ===== */
section img {
  border-radius: 10px;
  display: block;
  margin: 0 auto;
  background: var(--container-bg);
  box-shadow: 0 0 14px rgba(0,0,0,0.2);
}

/* ===== TABLEAU COLORE (gradient performance, identique dark/light) ===== */
section td.rank-top    { color: #16a34a !important; font-weight: 700 !important; text-shadow: 0 0 8px rgba(22,163,74,0.3); }
section td.rank-good   { color: #65a30d !important; font-weight: 600 !important; }
section td.rank-mid    { color: #ca8a04 !important; font-weight: 600 !important; }
section td.rank-low    { color: #ea580c !important; font-weight: 600 !important; }
section td.rank-bottom { color: #dc2626 !important; font-weight: 600 !important; }
body:not(.light-mode) section td.rank-top    { color: #34d399 !important; text-shadow: 0 0 8px rgba(52,211,153,0.3); }
body:not(.light-mode) section td.rank-good   { color: #a3e635 !important; }
body:not(.light-mode) section td.rank-mid    { color: #fbbf24 !important; }
body:not(.light-mode) section td.rank-low    { color: #fb923c !important; }
body:not(.light-mode) section td.rank-bottom { color: #f87171 !important; }

/* ===== SYSTEME 3 NIVEAUX D'IMBRICATION ===== */
section .box     { padding: 0.55rem 0.85rem; border-radius: 10px; }
section .box.la  { border-left-width: 4px !important; }

section .l1-blue   { background: var(--l1-blue-bg); border: 1px solid var(--blue-border); box-shadow: 0 0 12px rgba(59,130,246,0.15); }
section .l2-blue   { background: var(--l2-blue-bg); border: 1px solid var(--blue-border); box-shadow: 0 0 10px rgba(96,165,250,0.12); }
section .l3-blue   { background: var(--l3-blue-bg); border: 1px solid var(--blue-border); box-shadow: 0 0 8px rgba(147,197,253,0.12); }

section .l1-green  { background: var(--l1-green-bg); border: 1px solid var(--green-border); box-shadow: 0 0 12px rgba(16,185,129,0.15); }
section .l2-green  { background: var(--l2-green-bg); border: 1px solid var(--green-border); box-shadow: 0 0 10px rgba(52,211,153,0.12); }
section .l3-green  { background: var(--l3-green-bg); border: 1px solid var(--green-border); box-shadow: 0 0 8px rgba(110,231,183,0.12); }

section .l1-red    { background: var(--l1-red-bg); border: 1px solid var(--red-border); box-shadow: 0 0 12px rgba(248,113,113,0.15); }
section .l2-red    { background: var(--l2-red-bg); border: 1px solid var(--red-border); box-shadow: 0 0 10px rgba(251,113,133,0.12); }
section .l3-red    { background: var(--l3-red-bg); border: 1px solid var(--red-border); box-shadow: 0 0 8px rgba(252,165,165,0.12); }

section .l1-orange { background: var(--l1-orange-bg); border: 1px solid var(--orange-border); box-shadow: 0 0 12px rgba(245,158,11,0.15); }
section .l2-orange { background: var(--l2-orange-bg); border: 1px solid var(--orange-border); box-shadow: 0 0 10px rgba(251,191,36,0.12); }
section .l3-orange { background: var(--l3-orange-bg); border: 1px solid var(--orange-border); box-shadow: 0 0 8px rgba(253,230,138,0.12); }

section .l1-violet { background: var(--l1-violet-bg); border: 1px solid var(--violet-border); box-shadow: 0 0 12px rgba(139,92,246,0.15); }
section .l2-violet { background: var(--l2-violet-bg); border: 1px solid var(--violet-border); box-shadow: 0 0 10px rgba(167,139,250,0.12); }
section .l3-violet { background: var(--l3-violet-bg); border: 1px solid var(--violet-border); box-shadow: 0 0 8px rgba(196,181,253,0.12); }

section .l1-cyan   { background: var(--l1-cyan-bg); border: 1px solid var(--cyan-border); box-shadow: 0 0 12px rgba(6,182,212,0.15); }
section .l2-cyan   { background: var(--l2-cyan-bg); border: 1px solid var(--cyan-border); box-shadow: 0 0 10px rgba(34,211,238,0.12); }
section .l3-cyan   { background: var(--l3-cyan-bg); border: 1px solid var(--cyan-border); box-shadow: 0 0 8px rgba(103,232,249,0.12); }

/* All text inside a frame follows the frame color family (lighter variant) */
section .l1-blue,   section .l2-blue,   section .l3-blue   { color: var(--blue-strong); }
section .l1-green,  section .l2-green,  section .l3-green  { color: var(--green-strong); }
section .l1-red,    section .l2-red,    section .l3-red    { color: var(--red-strong); }
section .l1-orange, section .l2-orange, section .l3-orange { color: var(--orange-strong); }
section .l1-violet, section .l2-violet, section .l3-violet { color: var(--violet-strong); }
section .l1-cyan,   section .l2-cyan,   section .l3-cyan   { color: var(--cyan-strong); }

/* Strong inside a frame gets an extra glow in its family color */
section .l1-blue strong,   section .l2-blue strong,   section .l3-blue strong   { color: var(--blue-strong) !important;   text-shadow: 0 0 8px rgba(191,219,254,0.3); font-weight: 800; }
section .l1-green strong,  section .l2-green strong,  section .l3-green strong  { color: var(--green-strong) !important;  text-shadow: 0 0 8px rgba(187,247,208,0.3); font-weight: 800; }
section .l1-red strong,    section .l2-red strong,    section .l3-red strong    { color: var(--red-strong) !important;    text-shadow: 0 0 8px rgba(254,202,202,0.3); font-weight: 800; }
section .l1-orange strong, section .l2-orange strong, section .l3-orange strong { color: var(--orange-strong) !important; text-shadow: 0 0 8px rgba(254,243,199,0.3); font-weight: 800; }
section .l1-violet strong, section .l2-violet strong, section .l3-violet strong { color: var(--violet-strong) !important; text-shadow: 0 0 8px rgba(221,214,254,0.3); font-weight: 800; }
section .l1-cyan strong,   section .l2-cyan strong,   section .l3-cyan strong   { color: var(--cyan-strong) !important;   text-shadow: 0 0 8px rgba(165,243,252,0.3); font-weight: 800; }

/* ===== CENTRAGE VERTICAL (classe compact) ===== */
section.compact { justify-content: center; }
section.compact > h2:first-child { margin-top: 0; margin-bottom: 0.8rem; flex-shrink: 0; }

/* ===== OVERRIDE inline hard-coded dark colors in light mode ===== */
/* Some slides have inline style="color: #e2e8f0" hard-coded for dark mode;
   in light mode we flip those to the light text color. */
body.light-mode section div[style*="color: #e2e8f0"],
body.light-mode section span[style*="color: #e2e8f0"],
body.light-mode section p[style*="color: #e2e8f0"] { color: var(--text) !important; }

body.light-mode section h1[style*="color: #60a5fa"],
body.light-mode section h2[style*="color: #60a5fa"],
body.light-mode section h3[style*="color: #60a5fa"] { color: var(--lead-h1) !important; }

/* ============================================================
   UI BUTTONS (Sommaire + Dark/Light)
   ============================================================ */
  #homeBtn, #themeToggle {
    position: fixed;
    top: 12px;
    z-index: 9999;
    padding: 6px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 13px;
    backdrop-filter: blur(8px);
    transition: all 0.3s;
    border: 1px solid rgba(148,163,184,0.4);
  }
  #homeBtn { left: 12px; background: rgba(15,23,42,0.85); color: #e2e8f0; }
  #themeToggle { right: 12px; background: rgba(15,23,42,0.85); color: #e2e8f0; }
  body.light-mode #homeBtn, body.light-mode #themeToggle {
    background: rgba(241,245,249,0.9);
    color: #1e293b;
    border-color: rgba(100,116,139,0.4);
  }
  #homeBtn:hover, #themeToggle:hover { transform: translateY(-1px); }
</style>

<button id="homeBtn">Sommaire</button>
<button id="themeToggle">Mode clair</button>

<script>
(function() {
  // --- Sommaire navigation ---
  const homeBtn = document.getElementById('homeBtn');
  const HOME_HASH = '2';

  homeBtn.addEventListener('click', () => { location.hash = HOME_HASH; });

  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'h' || e.key === 'H') location.hash = HOME_HASH;
  });

  document.querySelectorAll('td').forEach(td => {
    const text = td.textContent.trim();
    const pageNum = parseInt(text);
    if (pageNum > 0 && pageNum < 500 && text === String(pageNum)) {
      const row = td.closest('tr');
      if (row) {
        row.style.cursor = 'pointer';
        row.addEventListener('click', () => { location.hash = String(pageNum); });
        row.addEventListener('mouseenter', () => { row.style.background = 'rgba(59,130,246,0.2)'; });
        row.addEventListener('mouseleave', () => { row.style.background = ''; });
      }
    }
  });

  // --- Dark/Light toggle (relies on CSS variables via body.light-mode) ---
  const toggleBtn = document.getElementById('themeToggle');
  const STORAGE_KEY = 'marpMode';
  const saved = localStorage.getItem(STORAGE_KEY) || 'dark';

  function applyMode(mode) {
    if (mode === 'light') {
      document.body.classList.add('light-mode');
      toggleBtn.textContent = 'Mode sombre';
    } else {
      document.body.classList.remove('light-mode');
      toggleBtn.textContent = 'Mode clair';
    }
    localStorage.setItem(STORAGE_KEY, mode);
  }

  applyMode(saved);

  toggleBtn.addEventListener('click', () => {
    applyMode(document.body.classList.contains('light-mode') ? 'dark' : 'light');
  });

  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'd' || e.key === 'D') {
      applyMode(document.body.classList.contains('light-mode') ? 'dark' : 'light');
    }
  });
})();
</script>
"""


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path-to-marp.html>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"File not found: {html_path}")
        sys.exit(1)

    content = html_path.read_text(encoding="utf-8")

    if "homeBtn" in content and "themeToggle" in content:
        print(f"Already post-processed: {html_path.name}")
        sys.exit(0)

    if "</body>" in content:
        content = content.replace("</body>", INJECT + "\n</body>")
    else:
        content += INJECT

    html_path.write_text(content, encoding="utf-8")
    print(f"Post-processed: {html_path.name} (theme CSS + Sommaire + Dark/Light toggle)")


if __name__ == "__main__":
    main()
