# Spec: Redistribution Plan

## Capability

After reviewing results, both partners collaboratively assign new responsibilities for each task. The plan becomes active only when both partners have explicitly signed it. If the plan is edited after signing, all signatures are reset and both must re-sign.

## Implementation

- `plan/models.py`: `Umverteilung`
- `plan/services.py`: full service layer
- `plan/views.py`: `bearbeiten`, `signoff`
- `plan/urls.py`: wired under `/umverteilung/`

## Data model

```
Umverteilung
├─ paar_session (FK)
├─ aufgabe (FK)
├─ management_neu (PLAN_CHOICES)   — new assignment for management
├─ ausfuehrung_neu (PLAN_CHOICES)  — new assignment for execution
├─ signoff_a (bool, default False)
├─ signoff_a_at (DateTimeField, nullable)
├─ signoff_b (bool, default False)
├─ signoff_b_at (DateTimeField, nullable)
unique_together: (paar_session, aufgabe)

Method:
  beide_signiert() → bool   — True when signoff_a and signoff_b are both True
```

## Plan choices (both dimensions)

| Value | Label |
|---|---|
| `person_a` | Person A (by name) |
| `person_b` | Person B (by name) |
| `beide` | Wir beide |
| `extern` | Jemand anderes / extern |
| `abschaffen` | Aufgabe abschaffen |

## URLs

| URL | Name | Method | Description |
|---|---|---|---|
| `/umverteilung/` | `plan:bearbeiten` | GET, POST | View and edit the plan |
| `/umverteilung/signoff/` | `plan:signoff` | POST only | Sign the plan |

## Behavior

### Plan initialization
- `get_oder_erstelle_plan(session)`: creates one `Umverteilung` per task in the session, defaulting both dimensions to `beide`
- Idempotent: calling it twice does not create duplicates

### Editing the plan
- GET: renders all tasks with current management_neu/ausfuehrung_neu values and a form
- POST: calls `plan_speichern(session, POST_data)` which updates all assignments
- `plan_speichern()` also resets `signoff_a=False`, `signoff_b=False` whenever any value changes (forces re-agreement)

### Signing
- POST to `plan:signoff` → calls `signoff_setzen(session, user)`
- `signoff_setzen()`: sets the correct signoff flag + timestamp for the current user
- If both are now signed (`beide_signiert()`): sets `session.status = plan_aktiv`
- The view shows a "Du hast unterzeichnet" indicator for the current user via `hat_signiert(session, user)`

## Access guard

Both views require login and `session.status ∈ {beide_fertig, plan_aktiv}`.

## Invariants

- One `Umverteilung` per `(paar_session, aufgabe)` — no duplicates
- Signatures are reset atomically when plan is saved (prevents one partner signing while the other edits)
- `abschaffen` tasks are excluded from weekly check-ins
