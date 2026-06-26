"""HSL palette generator for the Marp 'standard' theme.

Systeme colorimetrique parametrique :
- N familles reparties **equidistantes** sur le cercle chromatique (hue)
- Saturation et luminosite **constantes** par niveau d'imbrication (L1/L2/L3)
- Symetrique dark/light : inversion des niveaux de luminosite
- Calcule border + strong text deterministiquement depuis le hue

Usage:
    python gen_palette.py                    # N=6 (default), offset=220 (blue)
    python gen_palette.py --n 8 --offset 200
    python gen_palette.py --preview           # genere images/palette-preview.svg
    python gen_palette.py --emit-css          # affiche le bloc CSS a coller dans marp_postprocess.py
"""
from __future__ import annotations

import argparse
import colorsys
from pathlib import Path
from typing import NamedTuple


# =============================================================================
# PARAMETRES DU SYSTEME — les seules valeurs "designer" (le reste est calcule)
# =============================================================================

# Luminosite progressive (darker -> lighter) par niveau d'imbrication
# Dark mode : L1 = tres sombre, L3 = moins sombre
DARK_LIGHTNESS = {"L1": 0.10, "L2": 0.20, "L3": 0.32}
# Light mode : L1 = tres clair, L3 = moins clair (mirroir de dark)
LIGHT_LIGHTNESS = {"L1": 0.92, "L2": 0.85, "L3": 0.75}

# Saturation progressive : L1 plus sourd (fond), L3 plus vif (tag/badge)
# Identique dark/light
SATURATION = {"L1": 0.55, "L2": 0.45, "L3": 0.40}

# Bordure (accent fixe) et texte strong
BORDER_S, BORDER_L = 0.70, 0.55        # border visible, moyenne saturation
STRONG_DARK_S, STRONG_DARK_L = 0.80, 0.80   # strong text sur bg dark = clair
STRONG_LIGHT_S, STRONG_LIGHT_L = 0.70, 0.30  # strong text sur bg light = sombre

# Limite recommandee (au-dela, decrochage perceptuel)
MAX_FAMILIES = 12


# =============================================================================
# NAMED ALIASES — mapping index -> nom (compatible avec la charte existante)
# Ordre choisi pour que N=6 avec offset=220 produise : blue, violet, red, orange, green, cyan
# =============================================================================

# Avec offset=220 et step=60 : 220, 280, 340, 40, 100, 160
ALIAS_N6 = ["blue", "violet", "red", "orange", "green", "cyan"]


# =============================================================================
# UTILITIES
# =============================================================================

class HSL(NamedTuple):
    h: float  # 0-360
    s: float  # 0-1
    l: float  # 0-1

    def to_hex(self) -> str:
        r, g, b = colorsys.hls_to_rgb(self.h / 360.0, self.l, self.s)
        return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

    def to_css(self) -> str:
        return f"hsl({self.h:.0f}, {self.s * 100:.0f}%, {self.l * 100:.0f}%)"


def generate_hues(n: int, offset: float = 220.0) -> list[float]:
    """N hues equidistants sur le cercle, en partant de offset."""
    step = 360.0 / n
    return [(offset + i * step) % 360 for i in range(n)]


def family_colors(hue: float) -> dict[str, HSL]:
    """Retourne toutes les couleurs calculees pour un hue donne."""
    return {
        "l1-dark":  HSL(hue, SATURATION["L1"], DARK_LIGHTNESS["L1"]),
        "l2-dark":  HSL(hue, SATURATION["L2"], DARK_LIGHTNESS["L2"]),
        "l3-dark":  HSL(hue, SATURATION["L3"], DARK_LIGHTNESS["L3"]),
        "l1-light": HSL(hue, SATURATION["L1"], LIGHT_LIGHTNESS["L1"]),
        "l2-light": HSL(hue, SATURATION["L2"], LIGHT_LIGHTNESS["L2"]),
        "l3-light": HSL(hue, SATURATION["L3"], LIGHT_LIGHTNESS["L3"]),
        "border":       HSL(hue, BORDER_S, BORDER_L),
        "strong-dark":  HSL(hue, STRONG_DARK_S, STRONG_DARK_L),
        "strong-light": HSL(hue, STRONG_LIGHT_S, STRONG_LIGHT_L),
    }


# =============================================================================
# CSS EMITTER
# =============================================================================

def emit_css(n: int, offset: float) -> str:
    """Genere le bloc CSS complet (dark mode defaut + body.light-mode)."""
    if n > MAX_FAMILIES:
        raise ValueError(f"N={n} depasse la limite recommandee ({MAX_FAMILIES})")

    hues = generate_hues(n, offset)
    aliases = ALIAS_N6 if n == 6 else [f"c{i}" for i in range(n)]

    lines = []
    lines.append("/* ===== GENERATED PALETTE (HSL) — do not edit by hand ===== */")
    lines.append(f"/* N = {n} families, offset = {offset}, step = {360 / n:.1f} */")
    lines.append("")

    # Dark mode (:root defaults)
    lines.append(":root {")
    for i, hue in enumerate(hues):
        alias = aliases[i]
        c = family_colors(hue)
        lines.append(f"  /* Famille {i} ({alias}) — hue {hue:.0f} */")
        lines.append(f"  --l1-{alias}-bg: {c['l1-dark'].to_hex()};")
        lines.append(f"  --l2-{alias}-bg: {c['l2-dark'].to_hex()};")
        lines.append(f"  --l3-{alias}-bg: {c['l3-dark'].to_hex()};")
        lines.append(f"  --{alias}-border: {c['border'].to_hex()};")
        lines.append(f"  --{alias}-strong: {c['strong-dark'].to_hex()};")
    lines.append("}")
    lines.append("")

    # Light mode overrides
    lines.append("body.light-mode {")
    for i, hue in enumerate(hues):
        alias = aliases[i]
        c = family_colors(hue)
        lines.append(f"  --l1-{alias}-bg: {c['l1-light'].to_hex()};")
        lines.append(f"  --l2-{alias}-bg: {c['l2-light'].to_hex()};")
        lines.append(f"  --l3-{alias}-bg: {c['l3-light'].to_hex()};")
        lines.append(f"  --{alias}-strong: {c['strong-light'].to_hex()};")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


# =============================================================================
# SVG PREVIEW
# =============================================================================

def emit_preview_svg(n: int, offset: float, out_path: Path) -> None:
    """Genere un SVG preview : matrice N familles x 3 niveaux x 2 modes."""
    hues = generate_hues(n, offset)
    aliases = ALIAS_N6 if n == 6 else [f"c{i}" for i in range(n)]

    box_w, box_h = 140, 60
    gap = 10
    left_pad = 110  # labels
    top_pad = 40    # headers
    header_h = 30

    cols = 6  # L1-dark, L2-dark, L3-dark, L1-light, L2-light, L3-light
    col_labels = ["L1 dark", "L2 dark", "L3 dark", "L1 light", "L2 light", "L3 light"]

    width = left_pad + cols * (box_w + gap) + 20
    height = top_pad + n * (box_h + gap) + 20

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="\'Segoe UI\', system-ui, sans-serif" font-size="13">']
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#0f172a"/>')

    # Column headers
    for ci, label in enumerate(col_labels):
        x = left_pad + ci * (box_w + gap) + box_w / 2
        svg.append(f'<text x="{x:.0f}" y="{top_pad - 10}" fill="#94a3b8" text-anchor="middle" font-size="12">{label}</text>')

    # Rows
    for ri, hue in enumerate(hues):
        alias = aliases[ri]
        c = family_colors(hue)

        y = top_pad + ri * (box_h + gap)
        # Row label
        svg.append(f'<text x="{left_pad - 10}" y="{y + box_h / 2 + 4}" fill="#e2e8f0" text-anchor="end" font-weight="700">{alias} ({hue:.0f}°)</text>')

        for ci, key in enumerate(["l1-dark", "l2-dark", "l3-dark", "l1-light", "l2-light", "l3-light"]):
            x = left_pad + ci * (box_w + gap)
            color = c[key]
            border = c["border"]
            strong = c["strong-dark"] if "dark" in key else c["strong-light"]
            svg.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8" fill="{color.to_hex()}" stroke="{border.to_hex()}" stroke-width="1.5"/>')
            svg.append(f'<text x="{x + box_w / 2}" y="{y + box_h / 2 - 2}" fill="{strong.to_hex()}" text-anchor="middle" font-weight="700">{color.to_hex()}</text>')
            svg.append(f'<text x="{x + box_w / 2}" y="{y + box_h / 2 + 14}" fill="{strong.to_hex()}" text-anchor="middle" font-size="10" opacity="0.75">{color.to_css()}</text>')

    svg.append('</svg>')
    out_path.write_text("\n".join(svg), encoding="utf-8")


# =============================================================================
# CLI
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=6, help="Nombre de familles (default: 6, max: %(default)s)")
    ap.add_argument("--offset", type=float, default=220.0, help="Hue de depart en degres (default: 220 = bleu)")
    ap.add_argument("--preview", action="store_true", help="Genere images/palette-preview.svg")
    ap.add_argument("--emit-css", action="store_true", help="Affiche le bloc CSS (stdout)")
    args = ap.parse_args()

    if not args.emit_css and not args.preview:
        # Default: emit both
        args.emit_css = True
        args.preview = True

    if args.emit_css:
        print(emit_css(args.n, args.offset))

    if args.preview:
        here = Path(__file__).parent
        out = here / "images" / "palette-preview.svg"
        out.parent.mkdir(exist_ok=True)
        emit_preview_svg(args.n, args.offset, out)
        print(f"\nPreview SVG: {out}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
