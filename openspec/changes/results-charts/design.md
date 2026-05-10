# Results Charts — Design

## Data flow

No new models or API endpoints. The view passes JSON directly into the template via a `json_script` tag (Django 2.1+), which avoids XSS risks from inline `{{ variable }}` injection into `<script>` blocks.

```python
# view
import json
context["chart_gesamt"] = json.dumps(prepare_gesamt_chart_data(verteilung))
context["chart_kategorien"] = json.dumps(prepare_kategorie_chart_data(kategorien))
```

```html
<!-- template -->
{{ chart_gesamt|json_script:"chart-gesamt-data" }}
<script>
  const data = JSON.parse(document.getElementById("chart-gesamt-data").textContent);
</script>
```

## Chart 1: Gesamtverteilung (two donuts)

Two `<canvas>` elements side by side, one per dimension.

```
┌── Denken / Managen ──┐   ┌── Ausführen ─────────┐
│     ╭──────╮         │   │     ╭──────╮          │
│  ███│ 62%  │░░░      │   │  ██ │ 45%  │░░░░░░    │
│     ╰──────╯         │   │     ╰──────╯          │
│  ■ Person A  □ Person B  │   │  ■ Person A  □ Person B │
└──────────────────────┘   └──────────────────────┘
```

Data shape:
```json
{
  "management": {"person_a": 62, "person_b": 38},
  "ausfuehrung": {"person_a": 45, "person_b": 55},
  "label_a": "Tobias",
  "label_b": "Anna"
}
```

Chart.js config: `type: "doughnut"`, `cutout: "65%"`, percentage in center via plugin or custom label overlay.

Colors:
- Person A: `#7C3AED` (purple-600)
- Person B: `#10B981` (emerald-500)

## Chart 2: Kategorie-Ansicht (horizontal bars)

One horizontal bar chart. Each category is a group of two bars (Person A / Person B), stacked or grouped. Sorted by absolute imbalance (|A% - B%|), most unequal first.

```
Ernährung      ████████████████░░░░░  A: 78%  B: 22%
Haushalt       █████████████░░░░░░░░  A: 65%  B: 35%
Finanzen       ██████████░░░░░░░░░░░  A: 50%  B: 50%
```

Data shape:
```json
[
  {
    "kategorie": "Ernährung",
    "icon": "🍽️",
    "person_a": 78,
    "person_b": 22,
    "imbalance": 56
  },
  ...
]
```

Sorted in view: `sorted(kategorien, key=lambda k: abs(k["person_a"] - k["person_b"]), reverse=True)`

Chart.js config: `type: "bar"`, `indexAxis: "y"` (horizontal).

## Chart 3: Check-in Verlauf (line chart)

Line chart of ja-rate (%) per week, last 8 weeks.

```
100% ┤         ●
 80% ┤    ●────╯
 60% ┤●───╯
 40% ┤
     └──────────────────
     KW18 KW19 KW20 KW21
```

Two lines: Person A and Person B (same purple/green colors).

Data shape (from existing `get_verlauf()` service):
```json
{
  "wochen": ["2025-04-28", "2025-05-05", ...],
  "person_a": [60, 75, 80, 100],
  "person_b": [40, 60, 70, 90]
}
```

The existing `get_verlauf()` returns a dict per week — update it to return this shape, or add a separate `prepare_verlauf_chart_data()` helper in `checkins/services.py`.

Chart.js config: `type: "line"`, `tension: 0.3` (slight curve).

## Service changes

### `results/services.py`
Add two helpers (called by the view, not the existing scoring functions):

```python
def prepare_gesamt_chart_data(paar_session: PaarSession) -> dict: ...
def prepare_kategorie_chart_data(paar_session: PaarSession) -> list[dict]: ...
```

These call the existing `berechne_gesamtverteilung()` and `berechne_kategorie_verteilung()` and reshape the output for Chart.js.

### `checkins/services.py`
Add:
```python
def prepare_verlauf_chart_data(paar_session: PaarSession) -> dict: ...
```

Calls existing `get_verlauf()` and reshapes to the `{wochen, person_a, person_b}` format.

## View changes

### `results/views.py` — `auswertung`
Add to context:
```python
context["chart_gesamt_json"] = json.dumps(prepare_gesamt_chart_data(session))
context["chart_kategorien_json"] = json.dumps(prepare_kategorie_chart_data(session))
```

### `checkins/views.py` — `verlauf`
Add to context:
```python
context["chart_verlauf_json"] = json.dumps(prepare_verlauf_chart_data(session))
```
