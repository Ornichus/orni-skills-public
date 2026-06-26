# Excalidraw Diagram Skill

> **Version**: 1.0.0 | Derniere mise a jour: 2026-03-03

Skill de generation de diagrammes Excalidraw avec validation visuelle automatique.
Source: https://github.com/coleam00/excalidraw-diagram-skill

---

## Core Philosophy

Diagrams should **ARGUE, not DISPLAY**. The visual structure must mirror the concept's behavior.

Two self-check questions before finalizing any diagram:
1. **The Isomorphism Test**: Remove all text — does structure alone communicate the concept? If not, redesign.
2. **The Education Test**: Could someone learn something concrete from this, or does it just label boxes?

---

## Output Convention

- **Directory**: `docs/diagrams/` (created automatically if missing)
- **Naming**: `{slug}-{YYYY-MM-DD}.excalidraw` (e.g., `auth-flow-2026-03-03.excalidraw`)
- **Viewer**: Open with Obsidian Excalidraw plugin or load on excalidraw.com

---

## Workflow

### Step 1: Assess Depth

Before starting, determine diagram complexity:

| Type | When | Strategy |
|------|------|----------|
| **Simple/Conceptual** | Abstract shapes, mental models, philosophies | Build in single pass |
| **Comprehensive/Technical** | Systems, architectures, tutorials with evidence artifacts | Build section-by-section |

### Step 2: Research (technical diagrams only)

For technical diagrams, look up actual specs before drawing:
- Real JSON/data formats
- Actual event names and API endpoints
- Real function signatures
- Concrete examples from docs

### Step 3: Understand Deeply

For each concept in the diagram, ask: what does it actually DO? Not just what it IS.

### Step 4: Map Concepts to Visual Patterns

Each major concept should use a DIFFERENT visual pattern for variety:

| Pattern | Use For | Structure |
|---------|---------|-----------|
| **Fan-Out** | One-to-many (sources, root causes) | Central → multiple targets |
| **Convergence** | Many-to-one (aggregation, funnels) | Multiple → single |
| **Tree** | Parent-child hierarchy | `line` elements + free-floating text (no boxes) |
| **Spiral/Cycle** | Feedback loops, iterations | Sequence with arrow returning to start |
| **Cloud** | Abstract state, context, memory | Overlapping ellipses |
| **Assembly Line** | Transformations, pipelines | Input → Process Box → Output |
| **Side-by-Side** | Comparisons, before/after, trade-offs | Parallel structures |
| **Gap/Break** | Phase transitions, time jumps | Visual whitespace between phases |

### Step 5: Ensure Variety

Check that adjacent sections use different patterns. Boxes → boxes → boxes is a failure.

### Step 6: Generate JSON

Read references before generating:
- `.claude/skills/excal-diagram/references/color-palette.md` for colors
- `.claude/skills/excal-diagram/references/element-templates.md` for JSON templates
- `.claude/skills/excal-diagram/references/json-schema.md` for schema

**Large diagrams (>15 elements):** Build section-by-section. Claude Code has a ~32,000 token output limit per response. Build each section separately, then review cross-section spacing and bindings.

Save to: `docs/diagrams/{slug}-{date}.excalidraw`

### Step 7: Render & Validate (MANDATORY)

This step is NOT optional. Every diagram must be visually validated.

```bash
# Utiliser uv ou python -m uv selon disponibilite
cd .claude/skills/excal-diagram/references && uv run python render_excalidraw.py ../../docs/diagrams/{filename}.excalidraw
# Fallback si uv pas dans le PATH:
# cd .claude/skills/excal-diagram/references && python -m uv run python render_excalidraw.py ../../docs/diagrams/{filename}.excalidraw
```

Then use the Read tool on the generated PNG to view it. Iterate until:
- Rendered matches planned design
- No text clipped or overflowing
- Arrows connect to intended elements
- Balanced composition, no large voids
- Labels are readable

Typically 2-4 iterations.

---

## Evidence Artifacts

For technical diagrams, embed real data to prove accuracy and educate:

| Type | When | How |
|------|------|-----|
| Code snippets | APIs, integrations | Dark rectangle (`#1e293b`) + syntax-colored text |
| Data/JSON examples | Data formats, schemas | Dark rectangle + green text (`#22c55e`) |
| Event/step sequences | Protocols, workflows | Timeline pattern (line + dots + labels) |
| UI mockups | Actual output/results | Nested rectangles |
| API/method names | Real function calls | Actual names from docs |

---

## Multi-Zoom Architecture

Design diagrams with 3 levels of detail:

1. **Level 1 — Summary**: Full pipeline overview (visible when zoomed out)
2. **Level 2 — Sections**: Labeled regions grouping related components
3. **Level 3 — Detail**: Evidence artifacts, code snippets, specific data (visible when zoomed in)

---

## Container vs Free-Floating Text

Default to **free-floating text**. Add containers only when:
- It's a focal point that needs emphasis
- Visual grouping is needed
- Arrows need to connect to it
- The shape carries semantic meaning (ellipse = entry, diamond = decision)
- It represents a distinct "thing" (service, component)

**Target: <30% of text elements inside containers.**

---

## Shape Meaning

| What | Shape |
|------|-------|
| Labels, descriptions, section titles | Free-floating text (no shape) |
| Timeline markers | Small `ellipse` (10-20px) |
| Start/trigger/input | `ellipse` |
| Decision/condition | `diamond` |
| Process/action/step | `rectangle` |
| Hierarchy | Lines + text (no boxes) |

---

## Layout Principles

### Size Hierarchy
| Role | Size |
|------|------|
| Hero (most important) | 300x150px |
| Primary | 180x90px |
| Secondary | 120x60px |
| Small/detail | 60x40px |

### Spacing
- Hero element: 200px+ empty space around it
- Between sections: 100px+ gap
- Between elements in section: 40-60px

### Arrows
- Every relationship MUST have an arrow (position alone doesn't show relationships)
- Use source element's stroke color for arrow color
- Arrows should have clear paths (no overlapping)

---

## Quality Checklist

Before delivering any diagram, verify:

### Research & Evidence
- [ ] Technical diagrams include real specs/data (not placeholder)
- [ ] Code snippets use actual syntax
- [ ] API names are real

### Conceptual Accuracy
- [ ] Isomorphism test passes (structure mirrors concept)
- [ ] Education test passes (teaches something concrete)
- [ ] Each section uses a different visual pattern

### Container Discipline
- [ ] <30% of text in containers
- [ ] No unnecessary boxes
- [ ] Free-floating text for labels/descriptions

### Structural Completeness
- [ ] Every relationship has an arrow
- [ ] Size hierarchy communicates importance
- [ ] No orphan elements (everything connected or grouped)

### Technical Correctness
- [ ] Valid Excalidraw JSON
- [ ] All IDs unique
- [ ] Bindings reference correct element IDs
- [ ] Colors match palette

### Visual Validation
- [ ] PNG rendered and reviewed
- [ ] No clipped text
- [ ] No overlapping elements
- [ ] Balanced composition
- [ ] Readable at intended zoom level

---

## Fichiers de configuration (reference)

| Fichier | Role | Versionne ? |
|---------|------|-------------|
| `.claude/skills/excal-diagram/SKILL.md` | Instructions du skill | Oui (orni-manifest) |
| `.claude/skills/excal-diagram/references/color-palette.md` | Palette de couleurs | Oui (customisable) |
| `.claude/skills/excal-diagram/references/element-templates.md` | Templates JSON | Oui |
| `.claude/skills/excal-diagram/references/json-schema.md` | Schema reference | Oui |
| `.claude/skills/excal-diagram/references/render_excalidraw.py` | Script de rendu | Oui |
| `.claude/skills/excal-diagram/references/render_template.html` | Template HTML | Oui |
| `.claude/skills/excal-diagram/references/pyproject.toml` | Dependances Python | Oui |
| `docs/diagrams/` | Dossier de sortie | Non (contenu local) |

---

## Changelog

| Date | Version | Changements |
|------|---------|-------------|
| 2026-03-03 | 1.0.0 | Version initiale (fork adapte de coleam00/excalidraw-diagram-skill) |
