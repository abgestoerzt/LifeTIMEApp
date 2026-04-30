# Tasks

## Block 1 — Aufräumen & Setup

- [x] Altes Backend entfernen: `lifecalendar`-App, `LifeTimeApp`-Projektstruktur und `manage.py` löschen
- [x] Neues Django-Projekt aufsetzen: `uv init`, `pyproject.toml` mit allen Abhängigkeiten, `config/`-Struktur
- [x] Settings aufteilen: `config/settings/base.py`, `local.py`, `production.py` mit `python-decouple`
- [x] Ruff, Pyright, pytest in `pyproject.toml` konfigurieren

## Block 2 — Grundstruktur

- [x] 7 Django-Apps anlegen: `accounts`, `pairs`, `catalog`, `survey`, `results`, `plan`, `checkins`
- [x] Jede App mit Grundstruktur versehen: `models.py`, `views.py`, `services.py`, `forms.py`, `urls.py`, `admin.py`, `tests/`
- [x] Datenmodell implementieren: alle Models aus `Konzept.md` in die jeweiligen Apps
- [x] Initiale Migrations erstellen und prüfen
- [x] Django Admin für alle Models registrieren
- [x] Aufgabenkatalog als Fixture oder Data Migration anlegen (~35–40 Standardaufgaben in 8 Kategorien)

## Block 3 — Features

- [x] `accounts`: Registrierung, Login, Logout (Views + Forms + Templates + Tests)
- [x] `pairs`: Paar erstellen, Einladecode generieren, beitreten, Setup (optionale Kategorien wählen)
- [x] `survey`: Test-Flow — kategorieweise Fragen, Fortschritt speichern, Abschluss erkennen
- [x] `results`: Auswertungs-View mit Chart.js — Gesamtverteilung, Kategorien, Wahrnehmungslücken
- [x] `plan`: Umverteilungsplan bearbeiten + Sign-off beider Partner:innen
- [x] `checkins`: Wöchentlicher Check-in Flow + gemeinsame Auswertung + Verlaufs-Chart

## Block 4 — Polish & Qualität

- [x] Base-Template + Dashboard + Landing Page + Bootstrap 5 einbinden
- [x] Ruff check + format auf gesamtem Codebase, Pyright-Fehler beheben
- [x] Alle Tests laufen lassen, Coverage ≥ 80% sicherstellen (89% erreicht)
- [x] Finalen Stand committen und pushen
