# Element Templates

Copy-paste JSON templates for every element type used in Excalidraw diagrams.

---

## Free-Floating Text

```json
{
  "id": "text1",
  "type": "text",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 25,
  "text": "Label text here",
  "fontSize": 20,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  "strokeColor": "#1e40af",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "seed": 1,
  "isDeleted": false,
  "groupIds": [],
  "locked": false
}
```

---

## Line (structural, not arrow)

```json
{
  "id": "line1",
  "type": "line",
  "x": 100,
  "y": 100,
  "width": 0,
  "height": 200,
  "points": [[0, 0], [0, 200]],
  "strokeColor": "#1e3a5f",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "seed": 2,
  "isDeleted": false,
  "groupIds": [],
  "locked": false
}
```

---

## Small Marker Dot

```json
{
  "id": "dot1",
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 12,
  "height": 12,
  "strokeColor": "#1e3a5f",
  "backgroundColor": "#3b82f6",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "seed": 3,
  "isDeleted": false,
  "groupIds": [],
  "locked": false,
  "boundElements": []
}
```

---

## Rectangle (with rounded corners)

```json
{
  "id": "rect1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 180,
  "height": 90,
  "strokeColor": "#1e3a5f",
  "backgroundColor": "#3b82f6",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "roundness": { "type": 3 },
  "seed": 4,
  "isDeleted": false,
  "groupIds": [],
  "locked": false,
  "boundElements": [
    { "id": "text_rect1", "type": "text" }
  ]
}
```

---

## Text (centered in shape)

```json
{
  "id": "text_rect1",
  "type": "text",
  "x": 110,
  "y": 120,
  "width": 160,
  "height": 25,
  "text": "Process Step",
  "fontSize": 20,
  "fontFamily": 3,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "rect1",
  "strokeColor": "#ffffff",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "seed": 5,
  "isDeleted": false,
  "groupIds": [],
  "locked": false
}
```

---

## Arrow

```json
{
  "id": "arrow1",
  "type": "arrow",
  "x": 280,
  "y": 145,
  "width": 100,
  "height": 0,
  "points": [[0, 0], [100, 0]],
  "strokeColor": "#1e3a5f",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "seed": 6,
  "isDeleted": false,
  "groupIds": [],
  "locked": false,
  "startBinding": { "elementId": "rect1", "focus": 0, "gap": 2 },
  "endBinding": { "elementId": "rect2", "focus": 0, "gap": 2 },
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

---

## Common Properties (all elements)

```json
{
  "roughness": 0,
  "opacity": 100,
  "fontFamily": 3,
  "seed": "<unique number>",
  "isDeleted": false,
  "groupIds": [],
  "locked": false
}
```
