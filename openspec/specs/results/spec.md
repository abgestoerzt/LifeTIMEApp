# Spec: Results & Analysis

## Capability

After both partners complete the survey, a joint results page shows the mental load distribution across three views: overall split, per-category breakdown, and a perception gap table. No new data is stored — results are computed live from `Antwort` records.

## Implementation

- `results/services.py`: three scoring functions
- `results/views.py`: `auswertung` view
- `results/models.py`: empty (no models — pure computation over survey data)
- `results/urls.py`: single endpoint

## URL

| URL | Name | Access guard |
|---|---|---|
| `/auswertung/` | `results:auswertung` | `status ∈ {beide_fertig, plan_aktiv}` |

## Scoring logic

### Weights per answer value

| Value | Contributes to partner_a | Contributes to partner_b |
|---|---|---|
| `ich` (answered by A) | +1 | 0 |
| `partner` (answered by A) | 0 | +1 |
| `beide` (answered by A) | +0.5 | +0.5 |
| `extern` | 0 | 0 |
| `nicht_zutreffend` | 0 | 0 |

Note: the scoring uses **each partner's own answers independently**. Both A and B answer every task. The results page shows each person's perception of the distribution, then surfaces discrepancies.

### Gesamtverteilung

- Total weighted score for partner_a and partner_b across all answers
- Calculated separately for `management` and `ausfuehrung` dimensions
- Expressed as percentages (A% + B% = 100% for each dimension, after excluding extern/nicht_zutreffend from denominator)

### Kategorie-Verteilung

- Same calculation as Gesamtverteilung but scoped per `Kategorie`
- Returns one result per category with scores for both partners and both dimensions

### Wahrnehmungslücken (Perception Gaps)

Compares **management answers only** between the two partners for each task:

| Pattern | Type | Meaning |
|---|---|---|
| A: `ich`, B: `ich` | `konflikt` | Both think they're responsible — conflict |
| A: `ich`, B: `beide` | `unsichtbar` | A's work is invisible to B |
| A: `partner`, B: `partner` | `luecke` | Neither partner thinks they own it |
| A: `ich`, B: `partner` | — | Full agreement (no gap) |

Only tasks with an `Antwort` from both partners are evaluated.

## Service functions (`results/services.py`)

| Function | Returns |
|---|---|
| `berechne_gesamtverteilung(session)` | `dict` with management/ausfuehrung % for A and B |
| `berechne_kategorie_verteilung(session)` | `list[dict]` one entry per category |
| `finde_wahrnehmungsluecken(session)` | `list[dict]` with aufgabe + gap type for conflicting tasks |

## View behavior

`auswertung` view:
- Requires login + `session.status ∈ {beide_fertig, plan_aktiv}`
- Calls all three service functions
- Passes results to `results/auswertung.html`
- Template currently displays data as text/tables; charts are added in the `results-charts` change
