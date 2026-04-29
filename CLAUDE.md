# CLAUDE.md – Projektrichtlinien

## Projekt

Mental Load App für Paare. Django-Web-App (kein separates Frontend-Framework).
Konzept: siehe `Konzept.md`.

---

## Tooling & Setup

### Paketmanager: uv

Ausschließlich `uv` verwenden. Kein `pip` direkt, kein `requirements.txt`.

```bash
uv run python manage.py ...     # Django-Befehle
uv run pytest                   # Tests
uv run ruff check .             # Linting
uv run pyright                  # Type-Check
```

Abhängigkeiten in `pyproject.toml` verwalten:
```bash
uv add <paket>          # Laufzeit-Abhängigkeit
uv add --dev <paket>    # Dev-Abhängigkeit
```

### pyproject.toml

Alle Tool-Konfigurationen leben in `pyproject.toml` — keine separaten `.cfg`, `.ini` oder `setup.py`-Dateien.

---

## Code-Qualität

### Ruff (Linting + Formatting)

Ruff ist das einzige Linting/Formatting-Tool. Kein Pylint, kein Black, kein isort.

Konfiguration in `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "DJ",  # flake8-django
]
ignore = ["E501"]  # line length wird von formatter gehandhabt

[tool.ruff.format]
quote-style = "double"
```

Vor jedem Commit: `uv run ruff check . && uv run ruff format .`

### Pyright (Type-Checking)

Basic Mode. `django-stubs` ist installiert — Django-Typen sind also verfügbar.

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "basic"
djangoSettingsModule = "config.settings"
```

Alle neuen Funktionen und Views sollen Return-Types und Parameter-Types haben.
Bestehende Django-Generics (CBVs, Mixins) müssen nicht komplett annotiert werden.

---

## Architektur

### Django Apps (eine pro Feature-Domain)

```
backend/
  config/          # settings, urls, wsgi, asgi – kein App-Code hier
  accounts/        # Registrierung, Login, Logout, User-Profil
  pairs/           # PaarSession, Einladecode, Setup (opt. Kategorien)
  catalog/         # Kategorie, Aufgabe (Standard + paar-eigene Tasks)
  survey/          # Test-Durchführung, Antworten speichern
  results/         # Auswertung, Scoring-Logik, Chart-Daten
  plan/            # Umverteilungsplan, Sign-off
  checkins/        # Wöchentliche Check-ins, Verlauf
```

**Wichtig:** App heißt `survey`, nicht `test` — `test` kollidiert mit pytest.

### Interne Struktur jeder App

```
<app>/
  models.py        # Nur Datenbankmodelle, keine Business-Logik
  views.py         # Nur Request/Response-Handling
  services.py      # Business-Logik (reine Python-Funktionen, kein Request-Objekt)
  forms.py         # Django Forms / Validierung
  urls.py          # URL-Definitionen
  admin.py         # Admin-Konfiguration
  tests/
    __init__.py
    test_models.py
    test_views.py
    test_services.py
```

### Prinzipien

- **Models:** Nur Datenbankstruktur und einfache Properties. Keine komplexe Logik.
- **Views:** Nur HTTP-Handling. Delegieren an Services.
- **Services:** Reine Python-Funktionen mit klaren Signaturen. Keine Django-Request-Objekte als Parameter. Hier lebt die Business-Logik.
- **Keine zirkulären Imports** zwischen Apps. Abhängigkeitsrichtung: `results` → `survey` → `catalog` ← `plan`.
- Keine Logik in Templates.
- Keine rohen SQL-Queries außer in begründeten Ausnahmefällen.

---

## Testing

### Framework: pytest + pytest-django

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings"
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### Regel: Jede Funktion und jede View braucht mindestens einen Unit-Test

- Jede Service-Funktion → mind. ein Test in `test_services.py`
- Jede View → mind. ein Test in `test_views.py` (mit Django Test Client)
- Jedes Model mit Methoden → Test in `test_models.py`
- Neue Funktion ohne Test = unfertig

### Test-Stil

```python
# Gut: Beschreibender Name, ein Assert pro Test
def test_scoring_gibt_korrekte_gesamtverteilung_zurueck():
    ...

# Gut: Explizite Fixtures statt globaler State
@pytest.fixture
def paar_session(partner_a, partner_b):
    ...
```

- `factory_boy` für Test-Fixtures verwenden (keine hartkodierten PKs)
- Tests sollen unabhängig sein und in beliebiger Reihenfolge laufen
- Kein `time.sleep()` in Tests

### Coverage

Ziel: ≥ 80% Coverage. Messen mit `pytest-cov`:
```bash
uv run pytest --cov=. --cov-report=term-missing
```

---

## Django-Konventionen

- `config/` enthält Settings, Root-URLs, WSGI/ASGI — kein App-Code
- Settings in `config/settings/base.py`, `local.py`, `production.py`
- Keine hardkodierten Secrets — `.env` via `python-decouple` oder `django-environ`
- URL-Namen immer mit App-Prefix: `pairs:erstellen`, `survey:start`, etc.
- Migrations: immer committen, nie manuell editieren

---

## Abhängigkeiten (geplant)

```toml
[project]
dependencies = [
    "django>=5.2",
    "django-stubs",
    "python-decouple",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-django",
    "pytest-cov",
    "factory-boy",
    "ruff",
    "pyright",
]
```

---

## Was wir NICHT machen

- Kein Pylint (Ruff reicht)
- Kein Black (Ruff Format reicht)
- Kein isort separat (Ruff I-Rules reichen)
- Kein `requirements.txt` (pyproject.toml + uv)
- Keine Logik in Templates
- Keine Views ohne Tests
- Kein Spaghetti-Code: Logik gehört in Services, nicht in Views oder Models
