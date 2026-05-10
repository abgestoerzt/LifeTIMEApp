# Test Coverage — Design

## Test infrastructure

All tests use `pytest` + `pytest-django`. Configuration already lives in `pyproject.toml`.

### Factories (`tests/factories.py` at project root or per-app)

One shared `conftest.py` at `backend/conftest.py` exposes all factories as fixtures:

```python
# backend/conftest.py
import pytest
from tests.factories import UserFactory, PaarSessionFactory, ...
```

Factory definitions in `backend/tests/factories.py`:

```
UserFactory               → django.contrib.auth.User
PaarSessionFactory        → pairs.PaarSession (partner_a set, partner_b None)
PaarSessionMitPartnerFactory → PaarSession with both partners + status=test_laeuft
KategorieFactory          → catalog.Kategorie
AufgabeFactory            → catalog.Aufgabe (ist_standard=True)
AntwortFactory            → survey.Antwort
TestAbschlussFactory      → survey.TestAbschluss
UmverteilungFactory       → plan.Umverteilung
CheckInFactory            → checkins.CheckIn
CheckInAntwortFactory     → checkins.CheckInAntwort
```

All factories use `factory.SubFactory` for FK relationships. No hardcoded PKs.

## Per-app test plan

### `pairs` — `tests/test_services.py`

| Function | Tests |
|---|---|
| `paar_erstellen()` | creates session with partner_a, status=offen, invite_code set, expires in 7 days |
| `paar_beitreten()` | joins successfully with valid code; raises on expired code; raises on already-used code; raises on own code |
| `get_aktive_session()` | returns session for partner_a; returns session for partner_b; returns None if no session |

### `survey` — `tests/test_services.py`

| Function | Tests |
|---|---|
| `get_kategorien_fuer_session()` | returns standard categories; includes Kinder when setup_kinder=True; excludes Haustiere when setup_haustiere=False |
| `get_aufgaben_fuer_session()` | returns standard tasks; includes custom tasks for this session; excludes custom tasks for other sessions |
| `antwort_speichern()` | creates new Antwort; updates existing (idempotent); stores correct management+ausfuehrung |
| `get_fortschritt()` | returns 0/N at start; returns N/N when all answered |
| `ist_fertig()` | False at start; True when all tasks answered |
| `survey_abschliessen()` | creates TestAbschluss; sets status=beide_fertig when both users done; does not double-count |

### `results` — `tests/test_services.py`

| Function | Tests |
|---|---|
| `berechne_gesamtverteilung()` | ich=1.0 for A, partner=1.0 for B; beide=0.5/0.5; extern=0; trifft_nicht_zu=0 |
| `berechne_kategorie_verteilung()` | returns correct per-category split; handles empty category |
| `finde_wahrnehmungsluecken()` | detects `konflikt` (both say Ich); detects `unsichtbar` (A says Ich, B says Beide); detects `luecke` (both say Partner); no gap when in agreement |

### `plan` — `tests/test_services.py`

| Function | Tests |
|---|---|
| `get_oder_erstelle_plan()` | creates one Umverteilung per Aufgabe; idempotent on second call |
| `plan_speichern()` | updates management_neu + ausfuehrung_neu; resets signoff_a + signoff_b when plan changes |
| `signoff_setzen()` | sets signoff for correct partner; sets session.status=plan_aktiv when both signed; does not activate if only one signed |
| `hat_signiert()` | True after signoff; False before |
| `Umverteilung.beide_signiert()` | True when both True; False otherwise |

### `checkins` — `tests/test_services.py`

| Function | Tests |
|---|---|
| `get_montag()` | returns Monday for a Wednesday input; returns same date for a Monday input |
| `checkin_starten()` | creates CheckIn for correct week; idempotent if already started |
| `checkin_speichern()` | creates CheckInAntwort per task; updates existing |
| `beide_haben_eingecheckt()` | False with 1 check-in; True with 2 check-ins for same week |
| `get_verlauf()` | returns 8 entries max; correct ja-count per week |

## View tests

All view tests use Django's `test.Client` (via `pytest-django`'s `client` fixture).

Pattern per view:
1. **Auth guard** — unauthenticated request → 302 to `/login/`
2. **Status guard** — wrong session status → redirect or 403
3. **Happy path** — correct setup → 200 with expected context or correct redirect

### Key views to cover

| App | View | Guards |
|---|---|---|
| `pairs` | erstellen, einladung, beitreten | login required |
| `survey` | start, kategorie, abschliessen | login + partner_b must exist |
| `results` | auswertung | login + status ∈ {beide_fertig, plan_aktiv} |
| `plan` | bearbeiten, signoff | login + status=beide_fertig or plan_aktiv |
| `checkins` | start, auswertung, verlauf | login + status=plan_aktiv |
| `config` | dashboard | login required |

## Coverage target

Run with:
```bash
uv run pytest --cov=backend --cov-report=term-missing --cov-fail-under=80
```

Exclusions (add to `pyproject.toml`):
```toml
[tool.coverage.run]
omit = ["*/migrations/*", "*/admin.py", "manage.py", "*/wsgi.py", "*/asgi.py"]
```
