"""Validate Marp slides for overflow and contrast issues.

Usage: python docs/scripts/validate_marp.py docs/slides/my-deck.md

Renders the deck via Marp CLI + Playwright headless, then measures
each slide's content height vs viewport. Reports overflows.
"""
import subprocess, sys, tempfile, json
from pathlib import Path

def main():
    md_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not md_path or not md_path.exists():
        print(f"Usage: python {sys.argv[0]} <path-to-marp.md>")
        sys.exit(1)

    # Step 1: Render to HTML via Marp CLI
    html_path = md_path.with_suffix(".validate.html")
    result = subprocess.run(
        ["marp", str(md_path), "--html", "-o", str(html_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Marp render failed: {result.stderr}")
        sys.exit(1)

    # Step 2: Open in Playwright, measure each slide
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(f"file:///{html_path.resolve().as_posix()}")
        page.wait_for_timeout(1000)  # let Marp JS render

        # Measure all sections
        report = page.evaluate("""() => {
            const sections = document.querySelectorAll('section');
            const results = [];
            for (let i = 0; i < sections.length; i++) {
                const s = sections[i];
                const viewport = s.clientHeight;
                const content = s.scrollHeight;
                const overflow = content - viewport;

                // Get title
                const h = s.querySelector('h1, h2, h3');
                const title = h ? h.textContent.trim().substring(0, 60) : '(no title)';

                // Check contrast: find text elements on light backgrounds
                const contrastIssues = [];
                const textEls = s.querySelectorAll('p, li, span, div, td, strong, code');
                for (const el of textEls) {
                    const style = window.getComputedStyle(el);
                    const color = style.color;
                    const bg = style.backgroundColor;
                    // Parse rgb values
                    const parseRGB = (c) => {
                        const m = c.match(/\\d+/g);
                        return m ? m.map(Number) : [0,0,0];
                    };
                    const [r,g,b] = parseRGB(color);
                    const [br,bg2,bb] = parseRGB(bg);
                    // Luminance
                    const lum = (r2,g2,b2) => {
                        const [rs,gs,bs] = [r2,g2,b2].map(c => {
                            c = c/255;
                            return c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);
                        });
                        return 0.2126*rs + 0.7152*gs + 0.0722*bs;
                    };
                    const textLum = lum(r,g,b);
                    const bgLum = lum(br,bg2,bb);
                    // Only check if bg is not transparent (alpha > 0)
                    if (bg !== 'rgba(0, 0, 0, 0)') {
                        const ratio = (Math.max(textLum, bgLum) + 0.05) / (Math.min(textLum, bgLum) + 0.05);
                        if (ratio < 3.0) {
                            const text = el.textContent.trim().substring(0, 40);
                            if (text.length > 0) {
                                contrastIssues.push({text, ratio: ratio.toFixed(1), color, bg});
                            }
                        }
                    }
                }
                // Deduplicate contrast issues
                const seen = new Set();
                const uniqueContrast = contrastIssues.filter(c => {
                    const key = c.color + c.bg;
                    if (seen.has(key)) return false;
                    seen.add(key);
                    return true;
                });

                results.push({
                    slide: i + 1,
                    title,
                    viewport,
                    content,
                    overflow,
                    contrastIssues: uniqueContrast.slice(0, 3)
                });
            }
            return results;
        }""")

        browser.close()

    # Step 3: Clean up temp HTML
    html_path.unlink(missing_ok=True)

    # Step 4: Print report
    overflows = 0
    contrast_warnings = 0
    print(f"\n{'='*70}")
    print(f"MARP VALIDATION — {md_path.name} ({len(report)} slides)")
    print(f"{'='*70}")

    for r in report:
        status = "OK" if r["overflow"] <= 0 else f"OVERFLOW +{r['overflow']}px"
        icon = "  " if r["overflow"] <= 0 else ">>"
        print(f"{icon} Slide {r['slide']:2d}: [{status:>16s}] {r['title']}")
        if r["overflow"] > 0:
            overflows += 1
        for c in r["contrastIssues"]:
            contrast_warnings += 1
            print(f"      !! LOW CONTRAST ({c['ratio']}:1): \"{c['text']}...\"")
            print(f"         color={c['color']} on bg={c['bg']}")

    print(f"\n{'-'*70}")
    if overflows == 0 and contrast_warnings == 0:
        print(f"ALL CLEAR — {len(report)} slides, 0 overflows, 0 contrast issues")
    else:
        if overflows > 0:
            print(f"OVERFLOW: {overflows} slide(s) exceed 720px viewport")
        if contrast_warnings > 0:
            print(f"CONTRAST: {contrast_warnings} low-contrast text element(s) (ratio < 3:1)")
    print()

    sys.exit(1 if overflows > 0 else 0)


if __name__ == "__main__":
    main()
