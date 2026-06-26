"""Fix Mermaid SVG files for Marp embedding.

Usage:
    python fix_svg_sizes.py [directory]

Defaults to docs/slides/images/ if no directory given.

Fixes:
  1. Self-closing <br/> tags (Mermaid generates <br> which breaks SVG parsing in <img>)
  2. Explicit width/height attributes (Mermaid outputs width="100%" only; Marp needs explicit dims)
  3. Removes max-width inline style so Marp can resize freely
"""
import re
import sys
from pathlib import Path


def fix_svg(svg_file: Path) -> bool:
    """Returns True if file was modified."""
    content = svg_file.read_text(encoding="utf-8")
    original = content

    # 1. Self-close <br> tags (SVG strict parser)
    content = content.replace("<br>", "<br/>")

    # 2. Inject explicit width/height from viewBox
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', content)
    if m:
        vb_w, vb_h = m.group(1), m.group(2)
        content = re.sub(
            r'<svg([^>]*?)width="100%"([^>]*?)>',
            f'<svg\\1width="{vb_w}" height="{vb_h}"\\2>',
            content,
            count=1,
        )

    # 3. Remove max-width inline style
    content = re.sub(r'style="max-width: [^"]+;?"', "", content, count=1)

    if content != original:
        svg_file.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    svg_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/slides/images")
    if not svg_dir.exists():
        print(f"Directory not found: {svg_dir}")
        sys.exit(1)

    fixed = 0
    total = 0
    for svg_file in svg_dir.glob("*.svg"):
        total += 1
        if fix_svg(svg_file):
            fixed += 1
            print(f"FIXED: {svg_file.name}")
        else:
            print(f"UNCHANGED: {svg_file.name}")
    print(f"\n{fixed}/{total} SVG files fixed")


if __name__ == "__main__":
    main()
