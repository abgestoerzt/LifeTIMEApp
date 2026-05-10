# Results Charts — Tasks

- [x] Task 1: Add chart data helpers to results/services.py
- [x] Task 2: Add chart data helper to checkins/services.py
- [ ] Task 3: Update results/views.py
- [ ] Task 4: Update checkins/views.py
- [ ] Task 5: Build donut charts in results/auswertung.html
- [ ] Task 6: Build category bar charts in results/auswertung.html
- [ ] Task 7: Build trend chart in checkins/verlauf.html
- [ ] Task 8: Write tests for chart data helpers

---

## Task 1: Add chart data helpers to results/services.py

Add to `backend/results/services.py`:

**`prepare_gesamt_chart_data(paar_session: PaarSession) -> dict`**
- Call existing `berechne_gesamtverteilung(paar_session)`
- Reshape into `{management: {person_a, person_b}, ausfuehrung: {person_a, person_b}, label_a, label_b}`
- `label_a` = `paar_session.partner_a.get_short_name() or paar_session.partner_a.username`
- `label_b` = same for partner_b
- Percentages rounded to 1 decimal, always sum to 100

**`prepare_kategorie_chart_data(paar_session: PaarSession) -> list[dict]`**
- Call existing `berechne_kategorie_verteilung(paar_session)`
- Map to `[{kategorie, icon, person_a, person_b, imbalance}, ...]`
- Sort descending by `abs(person_a - person_b)`
- Exclude categories with no scoreable answers

---

## Task 2: Add chart data helper to checkins/services.py

Add to `backend/checkins/services.py`:

**`prepare_verlauf_chart_data(paar_session: PaarSession) -> dict`**
- Call existing `get_verlauf(paar_session)`
- Reshape to `{wochen: [...dates as YYYY-MM-DD...], person_a: [...], person_b: [...]}`
- A missing check-in for a partner → `null` for that week's value
- Ja-rate = `ja_count / total * 100`, rounded to 1 decimal

---

## Task 3: Update results/views.py

In the `auswertung` view, add to context:

```python
import json
from results.services import prepare_gesamt_chart_data, prepare_kategorie_chart_data

context["chart_gesamt_json"] = json.dumps(prepare_gesamt_chart_data(session))
context["chart_kategorien_json"] = json.dumps(prepare_kategorie_chart_data(session))
```

---

## Task 4: Update checkins/views.py

In the `verlauf` view, add to context:

```python
import json
from checkins.services import prepare_verlauf_chart_data

context["chart_verlauf_json"] = json.dumps(prepare_verlauf_chart_data(session))
```

---

## Task 5: Build donut charts in results/auswertung.html

In `backend/results/templates/results/auswertung.html`:

1. Add `{{ chart_gesamt_json|json_script:"chart-gesamt-data" }}` in the template body
2. Add two `<canvas id="chart-managen">` and `<canvas id="chart-ausfuehren">` elements in a flex/grid row
3. Add a `<script>` block that:
   - Parses the JSON: `JSON.parse(document.getElementById("chart-gesamt-data").textContent)`
   - Creates two `Chart` instances (type: `"doughnut"`, cutout: `"65%"`)
   - Colors: Person A = `#7C3AED`, Person B = `#10B981`
   - Adds a center-text plugin to show the dominant percentage inside each donut

---

## Task 6: Build category bar charts in results/auswertung.html

1. Add `{{ chart_kategorien_json|json_script:"chart-kategorien-data" }}` in the template body
2. Add `<canvas id="chart-kategorien">` element
3. Add to the `<script>` block:
   - Parse the JSON
   - Create a `Chart` instance (type: `"bar"`, indexAxis: `"y"`)
   - Labels = `icon + " " + kategorie` for each entry
   - Two datasets: Person A (purple) and Person B (green)
   - `borderRadius: 4`, no legend grid lines on y-axis

---

## Task 7: Build trend chart in checkins/verlauf.html

In `backend/checkins/templates/checkins/verlauf.html`:

1. Add `{{ chart_verlauf_json|json_script:"chart-verlauf-data" }}` in the template body
2. Add `<canvas id="chart-verlauf">` element
3. Add a `<script>` block:
   - Parse the JSON
   - Format week labels as "KW XX" from date strings
   - Create a `Chart` instance (type: `"line"`, tension: `0.3`)
   - Two datasets: Person A (purple) and Person B (green)
   - `spanGaps: false` so null values show as gaps (partner hasn't checked in)
   - y-axis: 0–100%, label "% erledigt"

---

## Task 8: Write tests for chart data helpers

Create `backend/results/tests/test_chart_data.py`:

Test `prepare_gesamt_chart_data()`:
- management + ausfuehrung percentages each sum to 100
- label_a and label_b are correct usernames
- extern answers don't affect scores
- empty session returns 50/50

Test `prepare_kategorie_chart_data()`:
- sorted by imbalance descending
- categories with no answers excluded
- imbalance = abs(person_a - person_b)

Create `backend/checkins/tests/test_chart_data.py`:

Test `prepare_verlauf_chart_data()`:
- returns at most 8 entries
- missing partner check-in → null for that position
- ja-rate calculated correctly
