"""Screenshot all slides of the charte-graphique in dark and/or light mode.

Usage:
    python screenshot_slides.py          # dark mode (default)
    python screenshot_slides.py light    # light mode
    python screenshot_slides.py both     # both modes
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
HTML = (HERE / "charte-graphique.html").resolve()
OUT = HERE / "_screenshots"
OUT.mkdir(exist_ok=True)

MODE = sys.argv[1] if len(sys.argv) > 1 else "dark"
SLIDES = list(range(1, 23))


def capture(mode: str):
    suffix = f"-{mode}" if mode == "light" else ""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 720})
        # Preset localStorage BEFORE any page JS runs
        ctx.add_init_script(f"localStorage.setItem('marpMode', '{mode}')")
        page = ctx.new_page()
        for n in SLIDES:
            url = f"file:///{HTML.as_posix().lstrip('/')}#{n}"
            page.goto(url)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(OUT / f"slide-{n:02d}{suffix}.png"))
            print(f"slide-{n:02d}{suffix}.png")
        browser.close()


if MODE == "both":
    capture("dark")
    capture("light")
else:
    capture(MODE)
print(f"\nScreenshots in {OUT}")
