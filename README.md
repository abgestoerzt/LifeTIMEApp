# LifeTIME App

Mental Load App für Paare. Django-Web-App mit SQLite für lokale Entwicklung.

## Voraussetzungen

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (`brew install uv` auf macOS)

## Lokales Setup

### 1. Abhängigkeiten installieren

```bash
uv sync
```

### 2. Umgebungsvariablen konfigurieren

Erstelle die Datei `backend/.env` (liegt **nicht** im Repo):

```bash
cp backend/.env.example backend/.env
```

Dann `backend/.env` öffnen und `SECRET_KEY` mit einem echten Wert befüllen:

```bash
# Einen sicheren Key generieren:
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Resultierende `backend/.env`:

```
SECRET_KEY=<generierter-key>
DEBUG=True
```

### 3. Datenbank migrieren

```bash
uv run python backend/manage.py migrate
```

### 4. Dev-Server starten

```bash
uv run python backend/manage.py runserver
```

Die App läuft dann unter [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. (Optional) Superuser anlegen

```bash
uv run python backend/manage.py createsuperuser
```

Admin-Interface: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## Entwicklung

Alle Befehle werden vom **Projektroot** aus mit `uv run` ausgeführt:

```bash
uv run python backend/manage.py ...     # Django-Befehle
uv run pytest                           # Tests
uv run ruff check .                     # Linting
uv run ruff format .                    # Formatierung
uv run pyright                          # Type-Check
```

### Tests mit Coverage

```bash
uv run pytest --cov=. --cov-report=term-missing
```

---

## Projektstruktur

```
LifeTIMEApp/
├── backend/
│   ├── config/          # Settings, Root-URLs, WSGI/ASGI
│   ├── accounts/        # Registrierung, Login, User-Profil
│   ├── pairs/           # Paar-Session, Einladecode
│   ├── catalog/         # Kategorien und Aufgaben
│   ├── survey/          # Test-Durchführung
│   ├── results/         # Auswertung und Scoring
│   ├── plan/            # Umverteilungsplan
│   ├── checkins/        # Wöchentliche Check-ins
│   └── manage.py
├── pyproject.toml       # Abhängigkeiten + Tool-Konfiguration
└── uv.lock
```

Settings-Dateien: `backend/config/settings/base.py` (gemeinsam), `local.py` (Entwicklung), `production.py` (Produktion).
