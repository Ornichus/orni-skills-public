# Excalidraw JSON Schema Reference

Reference for generating valid Excalidraw JSON files.

---

## Root Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

---

## Element Types

| Type | Use For |
|------|---------|
| `rectangle` | Processes, actions, components |
| `ellipse` | Entry/exit points, external systems, markers |
| `diamond` | Decisions, conditionals |
| `arrow` | Connections with direction |
| `text` | Labels (free-floating or inside shapes) |
| `line` | Non-arrow connections, structural lines |
| `frame` | Grouping containers |

---

## Key Properties (all elements)

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `type` | string | Element type (see above) |
| `x`, `y` | number | Position |
| `width`, `height` | number | Dimensions |
| `strokeColor` | string | Border/outline color (hex) |
| `backgroundColor` | string | Fill color (hex or "transparent") |
| `fillStyle` | string | `"solid"`, `"hachure"`, `"cross-hatch"` |
| `strokeWidth` | number | Border thickness (1, 2, 4) |
| `strokeStyle` | string | `"solid"`, `"dashed"`, `"dotted"` |
| `roughness` | number | 0 = smooth (always use 0) |
| `opacity` | number | 0-100 |
| `seed` | number | Unique number per element |
| `isDeleted` | boolean | Always `false` |
| `groupIds` | array | Group memberships |
| `locked` | boolean | Usually `false` |

---

## Text Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | The displayed text |
| `fontSize` | number | Size in pixels (16, 20, 28, 36) |
| `fontFamily` | number | 3 = monospace (always use 3) |
| `textAlign` | string | `"left"`, `"center"`, `"right"` |
| `verticalAlign` | string | `"top"`, `"middle"` |
| `containerId` | string/null | ID of parent shape (null = free-floating) |

---

## Arrow/Line Properties

| Property | Type | Description |
|----------|------|-------------|
| `points` | array | `[[x1,y1], [x2,y2], ...]` relative to element x,y |
| `startBinding` | object/null | Connection to start element |
| `endBinding` | object/null | Connection to end element |
| `startArrowhead` | string/null | `null`, `"arrow"`, `"bar"`, `"dot"` |
| `endArrowhead` | string/null | `null`, `"arrow"`, `"bar"`, `"dot"` |

### Binding Format

```json
{
  "elementId": "targetShapeId",
  "focus": 0,
  "gap": 2
}
```

---

## Shape-Specific

### Rounded Rectangle

```json
"roundness": { "type": 3 }
```

### Bound Elements (shape with text inside)

```json
"boundElements": [
  { "id": "textElementId", "type": "text" }
]
```
