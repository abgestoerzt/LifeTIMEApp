# Spec: Survey (Mental Load Test)

## Capability

Each partner independently answers two questions per task: who manages it, and who executes it. Answers are saved incrementally so the test can be paused and resumed. When both partners finish, the session advances to `beide_fertig`.

## Implementation

- `survey/models.py`: `Antwort`, `TestAbschluss`
- `survey/services.py`: full service layer (see below)
- `survey/views.py`: `start`, `kategorie`, `abschliessen`
- `survey/urls.py`: wired under `/test/`

## Data model

```
Antwort
├─ paar_session (FK)
├─ user (FK)
├─ aufgabe (FK)
├─ management (CHOICES)     — who thinks/plans/initiates
├─ ausfuehrung (CHOICES)    — who physically does it
└─ beantwortet_at (auto_now)
unique_together: (paar_session, user, aufgabe)

TestAbschluss
├─ paar_session (FK)
├─ user (FK)
└─ abgeschlossen_at (auto_now_add)
unique_together: (paar_session, user)
```

## Answer choices (both dimensions)

| Value | Label |
|---|---|
| `ich` | Ich |
| `partner` | Mein:e Partner:in |
| `beide` | Wir beide gleichermaßen |
| `extern` | Jemand anderes / extern |
| `nicht_zutreffend` | Trifft auf uns nicht zu |

## URLs

| URL | Name | Description |
|---|---|---|
| `/test/` | `survey:start` | Category overview + progress |
| `/test/<kategorie_id>/` | `survey:kategorie` | All tasks in one category |
| `/test/abschliessen/` | `survey:abschliessen` | Mark test complete |

## Behavior

### Start page
- Lists all visible categories (filtered by `setup_kinder`, `setup_haustiere`)
- Shows answered/total count per category
- Links to each category's task page
- Access: requires `partner_b` to have joined (status ≠ `offen`)

### Category page
- Shows all tasks in the category with two radio groups per task (management + ausfuehrung)
- Pre-fills previously saved answers
- POST → calls `antwort_speichern()` for each task → redirects back to `survey:start`
- Answers saved via `update_or_create` — idempotent, partial saves are fine

### Completing the test
- "Abschliessen" button on start page (shown when `ist_fertig()` returns True)
- POST to `survey:abschliessen` → calls `survey_abschliessen()`
- `survey_abschliessen()`: creates `TestAbschluss`, sets `status=beide_fertig` if both partners now have a `TestAbschluss`

## Service functions (`survey/services.py`)

| Function | Description |
|---|---|
| `get_kategorien_fuer_session(session)` | Returns Kategorie queryset filtered by setup flags |
| `get_aufgaben_fuer_session(session)` | Returns all Aufgabe for visible categories + custom tasks |
| `antwort_speichern(session, user, aufgabe_id, management, ausfuehrung)` | Creates or updates Antwort |
| `get_fortschritt(session, user)` | Returns `(answered_count, total_count)` tuple |
| `ist_fertig(session, user)` | Returns True when answered == total |
| `survey_abschliessen(session, user)` | Creates TestAbschluss, advances status if both done |

## Privacy constraint

Neither partner can see the other's answers until both have completed the survey and status = `beide_fertig`. This is enforced by the results view access check, not the survey views.
