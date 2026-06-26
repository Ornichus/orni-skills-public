"""Generate demo SVG diagrams for the Standard theme charte-graphique.

Run from this directory:
    cd skills/marp-presentations/themes/standard
    python gen_charte_diagrams.py

Produces images/pattern-*.svg showing the diagram patterns of the skill.

Les couleurs sont **derivees automatiquement** de `gen_palette.py` (source unique de verite).
Changer la palette (N, offset) dans gen_palette.py -> regenerer ici -> tous les SVG
utilisent les nouvelles couleurs. Aucun hex hardcode ici.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

from gen_palette import ALIAS_N6, family_colors, generate_hues

OUT_DIR = Path(__file__).parent / "images"
OUT_DIR.mkdir(exist_ok=True)

# Derive palette from gen_palette.py (N=6, offset=220 = default)
HUES = generate_hues(6, 220.0)
P = {alias: family_colors(hue) for alias, hue in zip(ALIAS_N6, HUES)}

# Convenience accessors for Mermaid classDef/style strings
def node_fill(family: str) -> str: return P[family]["l2-dark"].to_hex()
def node_stroke(family: str) -> str: return P[family]["border"].to_hex()
def subgraph_fill(family: str) -> str: return P[family]["l1-dark"].to_hex()
def subgraph_stroke(family: str) -> str: return P[family]["border"].to_hex()
def subgraph_title(family: str) -> str: return P[family]["strong-dark"].to_hex()

# Common classDef block used in every diagram — fully derived from palette
CLASSDEF = f"""
    classDef blueStyle fill:{node_fill('blue')},stroke:{node_stroke('blue')},color:#e2e8f0
    classDef violetStyle fill:{node_fill('violet')},stroke:{node_stroke('violet')},color:#e2e8f0
    classDef redStyle fill:{node_fill('red')},stroke:{node_stroke('red')},color:#e2e8f0
    classDef orangeStyle fill:{node_fill('orange')},stroke:{node_stroke('orange')},color:#e2e8f0
    classDef greenStyle fill:{node_fill('green')},stroke:{node_stroke('green')},color:#e2e8f0
    classDef cyanStyle fill:{node_fill('cyan')},stroke:{node_stroke('cyan')},color:#e2e8f0"""

def subgraph_style(name: str, family: str) -> str:
    return f"style {name} fill:{subgraph_fill(family)},stroke:{subgraph_stroke(family)},color:{subgraph_title(family)}"


# =============================================================================
# Theme variables globaux pour Mermaid (derive de la palette HSL)
# Utilise pour gantt, sequence, journey, state, er, quadrant, pie.
# =============================================================================

def mermaid_init(extra_vars: dict | None = None, theme_css: str = "") -> str:
    """Genere un bloc %%{init: ...}%% Mermaid avec theme base + themeVariables HSL + themeCSS force."""
    import json
    base = {
        "background": "#0f172a",
        "primaryColor":       node_fill("blue"),
        "primaryBorderColor": node_stroke("blue"),
        "primaryTextColor":   "#e2e8f0",
        "secondaryColor":     node_fill("green"),
        "tertiaryColor":      node_fill("violet"),
        "lineColor":          "#94a3b8",
        "textColor":          "#e2e8f0",
        "mainBkg":            node_fill("blue"),
        "nodeBorder":         node_stroke("blue"),
        "fontFamily":         "'Segoe UI', system-ui, sans-serif",
    }
    if extra_vars:
        base.update(extra_vars)
    init_obj = {"theme": "base", "themeVariables": base}
    if theme_css:
        init_obj["themeCSS"] = theme_css
    return "%%{init: " + json.dumps(init_obj) + "}%%"


# =============================================================================
# CSS overrides ciblant les classes internes de Mermaid (plus fiable que themeVariables)
# =============================================================================

PIE_CSS = f"""
.pieTitleText {{ fill: #e2e8f0 !important; font-weight: 700; }}
.pieCircle {{ stroke: #0f172a !important; stroke-width: 2px !important; opacity: 1 !important; }}
.pieOuterCircle {{ stroke: {node_stroke('blue')} !important; }}
.legend text {{ fill: #e2e8f0 !important; }}
/* Couleurs vives (border) pour les tranches — override toute valeur par defaut */
g > path.pieCircle:nth-of-type(1), path.pieCircle:nth-child(1) {{ fill: {node_stroke('blue')} !important; }}
g > path.pieCircle:nth-of-type(2), path.pieCircle:nth-child(2) {{ fill: {node_stroke('green')} !important; }}
g > path.pieCircle:nth-of-type(3), path.pieCircle:nth-child(3) {{ fill: {node_stroke('violet')} !important; }}
g > path.pieCircle:nth-of-type(4), path.pieCircle:nth-child(4) {{ fill: {node_stroke('orange')} !important; }}
g > path.pieCircle:nth-of-type(5), path.pieCircle:nth-child(5) {{ fill: {node_stroke('cyan')} !important; }}
g > path.pieCircle:nth-of-type(6), path.pieCircle:nth-child(6) {{ fill: {node_stroke('red')} !important; }}
.slice {{ fill: #ffffff !important; font-weight: 700; }}
"""

GANTT_CSS = f"""
.grid .tick line {{ stroke: #334155 !important; stroke-opacity: 0.5; }}
.grid path {{ stroke-width: 0; }}
.grid .tick text, .tick text {{ fill: #94a3b8 !important; }}
text.titleText {{ fill: #e2e8f0 !important; }}
text.sectionTitle {{ fill: #e2e8f0 !important; font-weight: 700; }}
.section0, .section2 {{ fill: {subgraph_fill('blue')} !important; }}
.section1, .section3 {{ fill: {subgraph_fill('violet')} !important; }}
rect.task {{ fill: {node_fill('blue')} !important; stroke: {node_stroke('blue')} !important; }}
rect.task0, rect.task2 {{ fill: {node_fill('blue')} !important; }}
rect.task1, rect.task3 {{ fill: {node_fill('violet')} !important; }}
rect.done0, rect.done1, rect.done2, rect.done3 {{ fill: {node_fill('green')} !important; stroke: {node_stroke('green')} !important; }}
rect.active0, rect.active1, rect.active2, rect.active3 {{ fill: {node_fill('orange')} !important; stroke: {node_stroke('orange')} !important; }}
rect.crit0, rect.crit1, rect.crit2, rect.crit3 {{ fill: {node_fill('red')} !important; stroke: {node_stroke('red')} !important; }}
.taskText, .taskTextOutsideRight, .taskTextOutsideLeft {{ fill: #e2e8f0 !important; }}
"""

SEQUENCE_CSS = f"""
.actor {{ fill: {node_fill('blue')} !important; stroke: {node_stroke('blue')} !important; }}
text.actor > tspan, text.actor {{ fill: #e2e8f0 !important; font-weight: 700; }}
.messageLine0, .messageLine1 {{ stroke: #94a3b8 !important; }}
text.messageText {{ fill: #e2e8f0 !important; }}
line.loopLine {{ stroke: #94a3b8 !important; }}
.labelBox {{ fill: {node_fill('violet')} !important; stroke: {node_stroke('violet')} !important; }}
.labelText, .labelText > tspan {{ fill: #e2e8f0 !important; }}
.activation0 {{ fill: {node_fill('green')} !important; stroke: {node_stroke('green')} !important; }}
.activation1 {{ fill: {node_fill('orange')} !important; stroke: {node_stroke('orange')} !important; }}
.activation2 {{ fill: {node_fill('red')} !important; stroke: {node_stroke('red')} !important; }}
.actor-line {{ stroke: #475569 !important; }}
.note {{ fill: {node_fill('orange')} !important; stroke: {node_stroke('orange')} !important; }}
"""

JOURNEY_CSS = f"""
.section-1, .section1 {{ fill: {subgraph_fill('blue')} !important; }}
.section-2, .section2 {{ fill: {subgraph_fill('green')} !important; }}
.section-3, .section3 {{ fill: {subgraph_fill('violet')} !important; }}
text.titleText, text.label {{ fill: #e2e8f0 !important; font-weight: 700; }}
.task-type-0 circle, .task-type-0 {{ fill: {node_fill('red')} !important; }}
.task-type-1 circle, .task-type-1 {{ fill: {node_fill('orange')} !important; }}
.task-type-2 circle, .task-type-2 {{ fill: {node_fill('green')} !important; }}
.task-type-3 circle, .task-type-3 {{ fill: {node_fill('blue')} !important; }}
.task-type-4 circle, .task-type-4 {{ fill: {node_fill('cyan')} !important; }}
.task text, .actor-text {{ fill: #e2e8f0 !important; }}
text {{ fill: #e2e8f0 !important; }}
"""

STATE_CSS = f"""
.node rect, .node circle, .node polygon {{ fill: {node_fill('blue')} !important; stroke: {node_stroke('blue')} !important; }}
.node .label, .nodeLabel {{ fill: #e2e8f0 !important; }}
.edgeLabel, .edgeLabel rect {{ fill: #0f172a !important; }}
.edgeLabel span, .edgeLabel text {{ color: #e2e8f0 !important; fill: #e2e8f0 !important; }}
.edgePath .path {{ stroke: #94a3b8 !important; }}
.arrowheadPath {{ fill: #94a3b8 !important; stroke: #94a3b8 !important; }}
.cluster rect {{ fill: {subgraph_fill('blue')} !important; stroke: {subgraph_stroke('blue')} !important; }}
"""

ER_CSS = f"""
.er.entityBox {{ fill: {node_fill('blue')} !important; stroke: {node_stroke('blue')} !important; }}
.er.attributeBoxEven {{ fill: {subgraph_fill('blue')} !important; }}
.er.attributeBoxOdd {{ fill: {subgraph_fill('violet')} !important; }}
.er.entityLabel, .entityLabel {{ fill: #e2e8f0 !important; font-weight: 700; }}
text {{ fill: #e2e8f0 !important; }}
.er.relationshipLabel, .er.relationshipLabelBox {{ fill: #e2e8f0 !important; }}
.er.relationshipLabelBox {{ fill: #0f172a !important; }}
.er.relationshipLine {{ stroke: #94a3b8 !important; }}
"""

QUADRANT_CSS = f"""
.quadrant-point {{ fill: {node_fill('cyan')} !important; stroke: {node_stroke('cyan')} !important; }}
.quadrant-point-text {{ fill: #e2e8f0 !important; }}
.quadrant-title, .quadrant-axis-label, text {{ fill: #e2e8f0 !important; }}
.quadrant-quadrant1, g.quadrants > rect:nth-of-type(1) {{ fill: {subgraph_fill('green')} !important; }}
.quadrant-quadrant2, g.quadrants > rect:nth-of-type(2) {{ fill: {subgraph_fill('blue')} !important; }}
.quadrant-quadrant3, g.quadrants > rect:nth-of-type(3) {{ fill: {subgraph_fill('red')} !important; }}
.quadrant-quadrant4, g.quadrants > rect:nth-of-type(4) {{ fill: {subgraph_fill('orange')} !important; }}
"""

TIMELINE_CSS = f"""
.section-0 {{ fill: {subgraph_fill('blue')} !important; }}
.section-1 {{ fill: {subgraph_fill('green')} !important; }}
.section-2 {{ fill: {subgraph_fill('violet')} !important; }}
.node rect, .node circle {{ fill: {node_fill('blue')} !important; stroke: {node_stroke('blue')} !important; }}
.label, text {{ fill: #e2e8f0 !important; }}
.edgePath .path, path.edge {{ stroke: #94a3b8 !important; }}
"""


DIAGRAMS = {
    # Pattern 1: Subgraph zones — cas prefere quand on a des groupes logiques
    "pattern-subgraph-zones": f"""graph LR
    subgraph A[1 SOURCES]
        S1[YouTube]
        S2[RSS]
        S3[Docs]
    end
    subgraph B[2 TRAITEMENT]
        T1[Extract]
        T2[Analyse]
    end
    subgraph C[3 STOCKAGE]
        ST1[Index]
        ST2[Base]
    end
    A ==> B ==> C
{CLASSDEF}
    class S1,S2,S3 blueStyle
    class T1,T2 greenStyle
    class ST1,ST2 redStyle
    {subgraph_style('A', 'blue')}
    {subgraph_style('B', 'green')}
    {subgraph_style('C', 'red')}""",

    # Pattern 2: LR lineaire simple — peu d'elements, pas de groupement necessaire
    "pattern-linear-lr": f"""graph LR
    A[Input] --> B[Parse] --> C[Transform] --> D[Validate] --> E[Output]
{CLASSDEF}
    class A blueStyle
    class B greenStyle
    class C violetStyle
    class D orangeStyle
    class E cyanStyle""",

    # Pattern 3: LR avec branching — fan-out/fan-in cree des colonnes paralleles (2D naturelle)
    "pattern-lr-branching": f"""graph LR
    Q[Question] --> E1[Moteur 1]
    Q --> E2[Moteur 2]
    Q --> E3[Moteur 3]
    Q --> E4[Moteur 4]
    E1 --> F[Fusion]
    E2 --> F
    E3 --> F
    E4 --> F
    F --> S1[Score]
    F --> S2[Tri]
    S1 --> R[Resultats]
    S2 --> R
{CLASSDEF}
    class Q orangeStyle
    class E1 blueStyle
    class E2 greenStyle
    class E3 violetStyle
    class E4 cyanStyle
    class F redStyle
    class S1,S2 orangeStyle
    class R greenStyle""",

    # Pattern 4: TB vertical — flux dense naturellement vertical
    "pattern-vertical-tb": f"""graph TB
    N1[Collecte donnees] --> N2[Validation format]
    N2 --> N3[Enrichissement]
    N3 --> N4[Deduplication]
    N4 --> N5[Classification]
    N5 --> N6[Indexation]
    N6 --> N7[Publication]
{CLASSDEF}
    class N1 blueStyle
    class N2 greenStyle
    class N3 violetStyle
    class N4 orangeStyle
    class N5 cyanStyle
    class N6 redStyle
    class N7 greenStyle""",

    # Pattern 6: Feedback externe — boucle geree proprement sans casser le flux principal
    "pattern-feedback-external": f"""graph LR
    A[Spec] ==> B[Build] ==> C[Test] ==> D[Deploy]
    LOOP[Diagnostic] -.ajuste.-> A
    D -.echec.-> LOOP
{CLASSDEF}
    class A blueStyle
    class B greenStyle
    class C violetStyle
    class D orangeStyle
    class LOOP redStyle""",

    # Anti-pattern: feedback arrow dans le flux principal casse l'ordre visuel (a ne pas faire)
    "antipattern-feedback-inline": f"""graph LR
    A[Spec] --> B[Build]
    B --> C[Test]
    C --> D[Deploy]
    D --> A
{CLASSDEF}
    class A blueStyle
    class B greenStyle
    class C violetStyle
    class D orangeStyle""",

    # =====================================================================
    # Autres types Mermaid supportes nativement — tous themees via palette HSL
    # =====================================================================

    # Gantt — roadmap projet
    "mermaid-gantt": mermaid_init(theme_css=GANTT_CSS) + """
gantt
    title Roadmap 2026
    dateFormat YYYY-MM-DD
    axisFormat %b
    section Phase 1
    Recherche       :done,   a1, 2026-01-01, 30d
    Prototype       :done,   a2, after a1, 20d
    section Phase 2
    Design          :active, b1, 2026-02-15, 25d
    Developpement   :        b2, after b1, 40d
    section Phase 3
    Tests           :crit,   c1, 2026-04-01, 20d
    Deploiement     :        c2, after c1, 10d""",

    # Timeline — chronologie
    "mermaid-timeline": mermaid_init(theme_css=TIMELINE_CSS) + """
timeline
    title Historique du projet
    2024 : Ideation : Premier prototype
    2025 : Beta lancee : 1000 utilisateurs
    2026 : V1.0 publique : Levee de fonds""",

    # SequenceDiagram — interactions
    "mermaid-sequence": mermaid_init(theme_css=SEQUENCE_CSS) + """
sequenceDiagram
    actor User
    participant UI as Interface
    participant API
    participant DB
    User->>UI: Clique login
    UI->>API: POST /auth
    activate API
    API->>DB: Verify credentials
    DB-->>API: OK
    API-->>UI: JWT token
    deactivate API
    UI-->>User: Dashboard""",

    # Journey — parcours utilisateur
    "mermaid-journey": mermaid_init(theme_css=JOURNEY_CSS) + """
journey
    title Parcours achat en ligne
    section Decouverte
      Recherche Google: 3: Visiteur
      Atterrit sur site: 4: Visiteur
    section Exploration
      Parcourt catalogue: 5: Visiteur
      Clique produit: 5: Visiteur
    section Conversion
      Ajoute au panier: 4: Client
      Paiement: 3: Client
      Confirmation: 5: Client""",

    # Pie — repartition
    "mermaid-pie": mermaid_init(theme_css=PIE_CSS) + """
pie showData
    title Repartition du budget
    "Produit" : 40
    "Marketing" : 25
    "Operations" : 20
    "R and D" : 15""",

    # StateDiagram — machine a etats
    "mermaid-state": mermaid_init(theme_css=STATE_CSS) + """
stateDiagram-v2
    [*] --> Idle
    Idle --> Fetching : start
    Fetching --> Success : 200 OK
    Fetching --> Error : 4xx / 5xx
    Success --> Idle : reset
    Error --> Fetching : retry
    Error --> [*] : abandon""",

    # ER Diagram — entite-relation
    "mermaid-er": mermaid_init(theme_css=ER_CSS) + """
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    PRODUCT ||--o{ ITEM : included_in
    USER {
        int id PK
        string email
        string name
    }
    ORDER {
        int id PK
        int user_id FK
        date created
        float total
    }
    ITEM {
        int order_id FK
        int product_id FK
        int quantity
    }
    PRODUCT {
        int id PK
        string sku
        string name
    }""",

    # Quadrant Chart — priorisation
    "mermaid-quadrant": mermaid_init(theme_css=QUADRANT_CSS) + """
quadrantChart
    title Priorisation impact vs effort
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Prioritaire
    quadrant-2 Quick wins
    quadrant-3 Ignorer
    quadrant-4 Deleguer
    Feature A: [0.3, 0.8]
    Feature B: [0.7, 0.9]
    Tech debt: [0.8, 0.4]
    Cleanup: [0.2, 0.3]
    Refactor: [0.6, 0.6]""",
}

# =============================================================================
# Pattern 5 LR wrap (snake) — SVG statique genere directement via Python.
# Mermaid ne sait pas faire un vrai snake (direction LR dans subgraphs empiles).
# On genere donc manuellement mais SANS hex hardcode — tout vient de la palette.
# =============================================================================

def gen_lr_wrap_svg() -> str:
    """Snake pattern : 11 etapes, un seul cadre, retour vers la gauche."""
    container_bg = subgraph_fill("blue")
    container_stroke = subgraph_stroke("blue")

    # Ordre des familles cycliques pour les 11 etapes
    fam_cycle = ["blue", "green", "violet", "orange", "cyan", "red",
                 "blue", "green", "violet", "orange", "cyan"]
    names = [f"Etape {i+1}" for i in range(11)]
    # Layout positions (0..4 = row1 L->R, 5 = corner, 6..10 = row2 R->L)
    # x for each step: row1 x=110,270,430,590,750 (E1..E5), corner x=750 (E6), row2 x=750,590,430,270,110 (E7..E11)
    positions = [
        (110, 70),  (270, 70),  (430, 70),  (590, 70),  (750, 70),   # Row 1 E1-E5
        (750, 150),                                                    # Corner E6
        (750, 230), (590, 230), (430, 230), (270, 230), (110, 230),    # Row 2 E7-E11 (R->L visual)
    ]

    lines = []
    lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 340" width="1000" height="340" font-family="\'Segoe UI\', system-ui, sans-serif" font-size="18">')
    lines.append('  <defs>')
    lines.append('    <marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto">')
    lines.append('      <path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/>')
    lines.append('    </marker>')
    lines.append('  </defs>')
    lines.append(f'  <rect x="30" y="30" width="940" height="290" rx="10" fill="{container_bg}" stroke="{container_stroke}" stroke-width="1.5"/>')

    # Boxes
    for i, ((x, y), fam, name) in enumerate(zip(positions, fam_cycle, names)):
        fill = node_fill(fam)
        stroke = node_stroke(fam)
        lines.append(f'  <rect x="{x}" y="{y}" width="140" height="50" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{x + 70}" y="{y + 31}" fill="#e2e8f0" text-anchor="middle">{name}</text>')

    # Arrows row 1 (E1->E5, 4 arrows) at y=95
    for i in range(4):
        x1 = 110 + 140 + i * 160
        x2 = 110 + 160 + i * 160
        lines.append(f'  <line x1="{x1}" y1="95" x2="{x2}" y2="95" stroke="#94a3b8" stroke-width="2" marker-end="url(#arr)"/>')
    # E5->E6 (vertical)
    lines.append('  <line x1="820" y1="120" x2="820" y2="150" stroke="#94a3b8" stroke-width="2" marker-end="url(#arr)"/>')
    # E6->E7 (vertical)
    lines.append('  <line x1="820" y1="200" x2="820" y2="230" stroke="#94a3b8" stroke-width="2" marker-end="url(#arr)"/>')
    # Arrows row 2 (E7->E11 going R->L) at y=255
    for i in range(4):
        x1 = 750 - i * 160
        x2 = 750 - 20 - i * 160
        lines.append(f'  <line x1="{x1}" y1="255" x2="{x2}" y2="255" stroke="#94a3b8" stroke-width="2" marker-end="url(#arr)"/>')

    lines.append('</svg>')
    return "\n".join(lines)


HTML_TEMPLATE = """<!DOCTYPE html><html><head>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
</head><body style="background:transparent;margin:0;">
<pre class="mermaid">{mmd}</pre>
<script>
mermaid.initialize({{
  startOnLoad: true,
  theme: 'dark',
  flowchart: {{ useMaxWidth: false }},
  themeCSS: {theme_css_json}
}});
</script>
</body></html>"""

# Global themeCSS combining all overrides — applied to every diagram render
import json as _json
GLOBAL_THEME_CSS = PIE_CSS + GANTT_CSS + SEQUENCE_CSS + JOURNEY_CSS + STATE_CSS + ER_CSS + QUADRANT_CSS + TIMELINE_CSS


import re as _re

PALETTE_CYCLE = ["blue", "green", "violet", "orange", "cyan", "red"]


def post_process_svg(name: str, svg: str) -> str:
    """Re-ecrit les fills des elements SVG pour forcer la palette HSL."""
    if name == "mermaid-pie":
        # Couleurs vives (border = saturation 70%, lightness 55%) pour les tranches
        bright_colors = [node_stroke(fam) for fam in PALETTE_CYCLE]
        cycle = iter(bright_colors)
        def _rep(m):
            try:
                color = next(cycle)
            except StopIteration:
                color = bright_colors[0]
            attrs = m.group(0)
            return _re.sub(r'fill="[^"]*"', f'fill="{color}"', attrs)
        svg = _re.sub(r'<path class="pieCircle"[^>]*>', _rep, svg)
        # Retirer l'opacite par defaut Mermaid (opacity:0.7) qui assombrit nos couleurs
        svg = _re.sub(r'\.pieCircle\{[^}]*\}', '.pieCircle{stroke:#0f172a;stroke-width:2px;opacity:1;}', svg)
        # Legend rects : match par style inline (pas de class)
        cycle_leg = iter(bright_colors)
        def _rep_leg(m):
            try:
                color = next(cycle_leg)
            except StopIteration:
                color = bright_colors[0]
            return _re.sub(r'fill:[^;"]+(;|")', f'fill:{color};', m.group(0), count=1).replace(
                m.group(0).split('style=')[1], f'"fill:{color};stroke:{color};"'
            ) if False else _re.sub(r'style="[^"]*"', f'style="fill:{color};stroke:{color};"', m.group(0))
        svg = _re.sub(r'<rect[^>]*style="[^"]*"[^>]*width="18"[^>]*>', _rep_leg, svg)
        # Pie title / legend text : blanc
        svg = _re.sub(r'\.pieTitleText\{[^}]*\}',
                      '.pieTitleText{text-anchor:middle;font-size:22px;fill:#e2e8f0;font-family:"Segoe UI",system-ui,sans-serif;font-weight:700;}', svg)
        svg = _re.sub(r'\.legend text\{[^}]*\}',
                      '.legend text{fill:#e2e8f0;font-family:"Segoe UI",system-ui,sans-serif;font-size:15px;}', svg)
        svg = _re.sub(r'\.slice\{[^}]*\}',
                      '.slice{font-family:"Segoe UI",system-ui,sans-serif;fill:#ffffff;font-size:16px;font-weight:700;}', svg)
        return svg

    if name == "mermaid-quadrant":
        # 4 zones : utilise L2 (plus vif que L1) pour etre visible
        q_colors = [node_fill("green"), node_fill("blue"),
                    node_fill("red"),   node_fill("orange")]
        # Target rects with fill like "#1f2020" / "#24..." (les 4 gris de Mermaid par defaut)
        matches = list(_re.finditer(r'<rect\s+fill="#[0-9a-fA-F]{6}"\s+height="\d+"\s+width="\d+"\s+y="\d+"\s+x="\d+"[^>]*>', svg))
        for idx, m in enumerate(matches[:4]):
            old = m.group(0)
            new = _re.sub(r'fill="#[0-9a-fA-F]{6}"', f'fill="{q_colors[idx]}"', old, count=1)
            svg = svg.replace(old, new, 1)
        # Points circles
        svg = _re.sub(
            r'(<circle[^>]*)fill="#[0-9a-fA-F]{6}"',
            lambda m: m.group(1) + f'fill="{node_fill("cyan")}"',
            svg,
        )
        # Remove NaN HSL values
        svg = svg.replace('hsl(180, 1.5873015873%, NaN%)', '#e2e8f0')
        svg = _re.sub(r'hsl\([^)]*NaN[^)]*\)', '#e2e8f0', svg)
        return svg

    if name == "mermaid-gantt":
        # Remplacer fills des sections, tasks, done, active, crit
        rules = [
            (r'<rect[^>]*class="section0"[^>]*>', subgraph_fill("blue")),
            (r'<rect[^>]*class="section1"[^>]*>', subgraph_fill("violet")),
            (r'<rect[^>]*class="section2"[^>]*>', subgraph_fill("blue")),
            (r'<rect[^>]*class="section3"[^>]*>', subgraph_fill("violet")),
            (r'<rect[^>]*class="task [^"]*"[^>]*>', node_fill("blue")),
            (r'<rect[^>]*class="done[^"]*"[^>]*>', node_fill("green")),
            (r'<rect[^>]*class="active[^"]*"[^>]*>', node_fill("orange")),
            (r'<rect[^>]*class="crit[^"]*"[^>]*>', node_fill("red")),
        ]
        for pat, col in rules:
            svg = _re.sub(pat, lambda m, c=col: _re.sub(r'fill="[^"]*"', f'fill="{c}"', m.group(0)), svg)
        return svg

    # Pour sequence / journey / state / er / timeline : on a deja un theme dark
    # acceptable. On force juste les principaux fills si besoin.
    return svg


def main():
    theme_css_json = _json.dumps(GLOBAL_THEME_CSS)
    # 1. Generate Mermaid SVGs via Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ok = 0
        for name, mmd in DIAGRAMS.items():
            page = browser.new_page()
            page.set_content(HTML_TEMPLATE.format(mmd=mmd, theme_css_json=theme_css_json))
            page.wait_for_timeout(3500)
            svg = page.evaluate("() => document.querySelector('.mermaid svg')?.outerHTML")
            if svg:
                svg = post_process_svg(name, svg)
                (OUT_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")
                print(f"OK: {name}.svg ({len(svg)} chars)")
                ok += 1
            else:
                print(f"FAIL: {name}")
            page.close()
        browser.close()

    # 2. Generate LR wrap SVG manually (Mermaid cannot do true snake)
    wrap_svg = gen_lr_wrap_svg()
    (OUT_DIR / "pattern-lr-wrap.svg").write_text(wrap_svg, encoding="utf-8")
    print(f"OK: pattern-lr-wrap.svg ({len(wrap_svg)} chars) [static SVG from palette]")

    print(f"\n{ok + 1}/{len(DIAGRAMS) + 1} diagrams generated in {OUT_DIR}")


if __name__ == "__main__":
    main()
