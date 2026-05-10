# Spec: Weekly Check-ins

## Capability

Once the redistribution plan is active, both partners independently check in each week to report how well each task went. When both have checked in, a joint view shows where the plan is working and where it isn't. A trend view shows progress over the last 8 weeks.

## Implementation

- `checkins/models.py`: `CheckIn`, `CheckInAntwort`
- `checkins/services.py`: full service layer
- `checkins/views.py`: `start`, `auswertung`, `verlauf`
- `checkins/urls.py`: wired under `/checkin/`

## Data model

```
CheckIn
├─ paar_session (FK)
├─ woche (DateField)         — always the Monday of the current week
├─ user (FK)
└─ abgeschlossen_at (auto_now_add)
unique_together: (paar_session, woche, user)

CheckInAntwort
├─ checkin (FK CheckIn)
├─ aufgabe (FK)
├─ status (CHOICES: ja, teilweise, nein)
└─ notiz (TextField, blank=True)
unique_together: (checkin, aufgabe)
```

## Check-in answer choices

| Value | Label |
|---|---|
| `ja` | ✅ Ja, hat funktioniert |
| `teilweise` | ⚠️ Teilweise |
| `nein` | ❌ Nein / nicht passiert |

## URLs

| URL | Name | Access | Description |
|---|---|---|---|
| `/checkin/` | `checkins:start` | login + plan_aktiv | Do this week's check-in |
| `/checkin/auswertung/` | `checkins:auswertung` | login + plan_aktiv | Joint view (both must be done) |
| `/checkin/verlauf/` | `checkins:verlauf` | login + plan_aktiv | 8-week trend |

## Behavior

### Check-in start
- Shows all tasks from the redistribution plan (excludes `abschaffen` tasks)
- Per task: 3-option radio (ja / teilweise / nein) + optional free-text note
- POST → `checkin_speichern(checkin, POST_data)` → saves/updates `CheckInAntwort` per task
- Week is keyed to the Monday of the current week (`get_montag(today)`)
- `checkin_starten(session, user)` creates the `CheckIn` record; idempotent if already started

### Joint auswertung
- Only accessible when `beide_haben_eingecheckt(session, woche)` is True
- Shows both partners' responses side by side per task
- Highlights discrepancies (one says "ja", other says "nein")

### Verlauf (trend)
- `get_verlauf(session)` returns last 8 weeks of data
- Per week: count of "ja" answers and total answers per partner
- Displayed as a trend chart (wired up in the `results-charts` change)

## Service functions (`checkins/services.py`)

| Function | Description |
|---|---|
| `get_montag(date)` | Returns Monday of the week containing `date` |
| `checkin_starten(session, user)` | Creates CheckIn for current week; idempotent |
| `checkin_speichern(checkin, data)` | Saves CheckInAntwort records from POST data |
| `get_checkin_aufgaben(session)` | Returns Umverteilungen excluding `abschaffen` |
| `beide_haben_eingecheckt(session, woche)` | True when 2 CheckIns exist for the week |
| `get_verlauf(session)` | Returns last 8 weeks of ja/total counts |

## Reminder mechanism

No automated reminders in v1. The dashboard (see `dashboard-polish` change) shows:
- "Check-in diese Woche ausstehend" when the user hasn't checked in yet
- "Letzter Check-in: vor X Tagen" to create urgency
