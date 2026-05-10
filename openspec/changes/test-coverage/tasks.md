# Test Coverage — Tasks

- [x] Task 1: Factories and conftest
- [x] Task 2: Test pairs/services
- [x] Task 3: Test survey/services
- [x] Task 4: Test results/services
- [x] Task 5: Test plan/services
- [x] Task 6: Test checkins/services
- [x] Task 7: Test views
- [x] Task 8: Coverage check and gap fill

---

## Task 1: Factories and conftest

Create `backend/tests/__init__.py`, `backend/tests/factories.py`, and `backend/conftest.py`.

Implement factory-boy factories for:
- `UserFactory` (django User, unique username via `factory.Sequence`)
- `PaarSessionFactory` (partner_a from UserFactory, partner_b=None, status=offen)
- `PaarSessionMitPartnerFactory` (both partners set, status=test_laeuft)
- `KategorieFactory` (name, icon, ist_optional=False, reihenfolge sequence)
- `AufgabeFactory` (FK to KategorieFactory, ist_standard=True)
- `AntwortFactory` (FK to PaarSession, User, Aufgabe; management=ich, ausfuehrung=ich)
- `TestAbschlussFactory` (FK to PaarSession, User)
- `UmverteilungFactory` (FK to PaarSession, Aufgabe; management_neu=beide, ausfuehrung_neu=beide)
- `CheckInFactory` (FK to PaarSession, User; woche=Monday of today)
- `CheckInAntwortFactory` (FK to CheckIn, Aufgabe; status=ja)

In `backend/conftest.py`, register fixtures so all test files can use factories without importing them.

Add `pytest-cov` and `coverage` to dev dependencies if not already present:
```bash
uv add --dev pytest-cov coverage
```

Add to `pyproject.toml`:
```toml
[tool.coverage.run]
omit = ["*/migrations/*", "*/admin.py", "manage.py", "*/wsgi.py", "*/asgi.py", "*/tests/*"]
```

---

## Task 2: Test pairs/services

Create `backend/pairs/tests/test_services.py`.

Test `paar_erstellen(user)`:
- Returns a PaarSession with partner_a=user
- Status is `offen`
- invite_code is set (not None)
- invite_expires_at is ~7 days from now

Test `paar_beitreten(user, code)`:
- Joins successfully: sets partner_b, returns session
- Raises (or returns error) when code is expired
- Raises when code belongs to user's own session
- Raises when session already has a partner_b

Test `get_aktive_session(user)`:
- Returns session when user is partner_a
- Returns session when user is partner_b
- Returns None when user has no session

---

## Task 3: Test survey/services

Create `backend/survey/tests/test_services.py`.

Test `get_kategorien_fuer_session(paar_session)`:
- Returns non-optional categories always
- Includes Kinderbetreuung when setup_kinder=True
- Excludes Haustiere when setup_haustiere=False

Test `get_aufgaben_fuer_session(paar_session)`:
- Returns standard tasks for visible categories
- Includes custom tasks belonging to this session
- Excludes custom tasks belonging to another session

Test `antwort_speichern(paar_session, user, aufgabe_id, management, ausfuehrung)`:
- Creates Antwort on first call
- Updates Antwort on second call with same aufgabe (update_or_create is idempotent)
- Stores correct management and ausfuehrung values

Test `get_fortschritt(paar_session, user)`:
- Returns `(0, N)` when no answers saved
- Returns `(N, N)` when all tasks answered

Test `ist_fertig(paar_session, user)`:
- Returns False with no answers
- Returns True when all tasks answered

Test `survey_abschliessen(paar_session, user)`:
- Creates a TestAbschluss record
- Status stays `test_laeuft` when only one partner is done
- Status becomes `beide_fertig` when both partners have a TestAbschluss

---

## Task 4: Test results/services

Create `backend/results/tests/test_services.py`.

Test `berechne_gesamtverteilung(paar_session)`:
- When A answers `ich` for all: A gets 100%, B gets 0%
- When both answer `beide`: A and B each get 50%
- `extern` and `trifft_nicht_zu` do not contribute to either partner's score
- Management and Ausführung are returned as separate values

Test `berechne_kategorie_verteilung(paar_session)`:
- Returns a result entry per Kategorie
- Scores per category match the same weighting logic as Gesamtverteilung
- An empty category (no answers) does not raise

Test `finde_wahrnehmungsluecken(paar_session)`:
- A says `ich`, B says `ich` → type `konflikt`
- A says `ich`, B says `beide` → type `unsichtbar`
- A says `partner`, B says `partner` → type `luecke`
- A says `ich`, B says `partner` → no gap (agreement)

---

## Task 5: Test plan/services

Create `backend/plan/tests/test_services.py`.

Test `get_oder_erstelle_plan(paar_session)`:
- Creates one Umverteilung per Aufgabe in the session
- Calling it twice does not create duplicates

Test `plan_speichern(paar_session, data)`:
- Updates management_neu and ausfuehrung_neu from POST data
- Resets signoff_a=False and signoff_b=False when plan values change

Test `signoff_setzen(paar_session, user)`:
- Sets signoff for partner_a when called by partner_a
- Sets signoff for partner_b when called by partner_b
- Sets session.status=plan_aktiv when both have signed
- Does not activate if only one has signed
- Sets signoff timestamp

Test `hat_signiert(paar_session, user)`:
- Returns True after signoff
- Returns False before

Test `Umverteilung.beide_signiert()`:
- Returns True when signoff_a=True and signoff_b=True
- Returns False otherwise

---

## Task 6: Test checkins/services

Create `backend/checkins/tests/test_services.py`.

Test `get_montag(date)`:
- Wednesday input → Monday of same week
- Monday input → same date returned
- Sunday input → Monday of same week

Test `checkin_starten(paar_session, user)`:
- Creates a CheckIn for the current week (Monday)
- Second call returns existing CheckIn (idempotent)

Test `checkin_speichern(checkin, data)`:
- Creates one CheckInAntwort per Aufgabe
- Calling twice updates, does not duplicate

Test `beide_haben_eingecheckt(paar_session, woche)`:
- False when only one CheckIn exists for the week
- True when two CheckIns exist for the week

Test `get_verlauf(paar_session)`:
- Returns at most 8 entries
- Each entry has the correct ja-count and total

---

## Task 7: Test views

Create `test_views.py` in `pairs/tests/`, `survey/tests/`, `results/tests/`, `plan/tests/`, `checkins/tests/`.

For every view, write at minimum:
- Auth guard: unauthenticated → 302 to /login/
- Status guard (where applicable): wrong session status → redirect or 403
- Happy path: correct preconditions → 200

Views to cover: `pairs:erstellen`, `pairs:einladung`, `pairs:beitreten`, `survey:start`, `survey:kategorie`, `survey:abschliessen`, `results:auswertung`, `plan:bearbeiten`, `plan:signoff`, `checkins:start`, `checkins:auswertung`, `checkins:verlauf`, `config:dashboard`.

---

## Task 8: Coverage check and gap fill

Run:
```bash
uv run pytest --cov=backend --cov-report=term-missing --cov-fail-under=80
```

Review the missing-lines report. For any uncovered line that is reachable code (not just migration/admin), add a targeted test. Commit once `--cov-fail-under=80` passes cleanly.
