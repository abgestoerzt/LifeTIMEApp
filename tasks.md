# Tasks

## Block 1 — Aufräumen & Setup

- [ ] Altes Backend entfernen: `lifecalendar`-App, `LifeTimeApp`-Projektstruktur und `manage.py` löschen
- [ ] Neues Django-Projekt aufsetzen: `uv init`, `pyproject.toml` mit allen Abhängigkeiten, `config/`-Struktur
- [ ] Settings aufteilen: `config/settings/base.py`, `local.py`, `production.py` mit `python-decouple`
- [ ] Ruff, Pyright, pytest in `pyproject.toml` konfigurieren

## Block 2 — Grundstruktur

- [ ] 7 Django-Apps anlegen: `accounts`, `pairs`, `catalog`, `survey`, `results`, `plan`, `checkins`
- [ ] Jede App mit Grundstruktur versehen: `models.py`, `views.py`, `services.py`, `forms.py`, `urls.py`, `admin.py`, `tests/`
- [ ] Datenmodell implementieren: alle Models aus `Konzept.md` in die jeweiligen Apps
- [ ] Initiale Migrations erstellen und prüfen
- [ ] Django Admin für alle Models registrieren
- [ ] Aufgabenkatalog als Fixture oder Data Migration anlegen (~35–40 Standardaufgaben in 8 Kategorien)

## Block 3 — Features

- [ ] `accounts`: Registrierung, Login, Logout (Views + Forms + Templates + Tests)
- [ ] `pairs`: Paar erstellen, Einladecode generieren, beitreten, Setup (optionale Kategorien wählen)
- [ ] `survey`: Test-Flow — kategorieweise Fragen, Fortschritt speichern, Abschluss erkennen
- [ ] `results`: Auswertungs-View mit Chart.js — Gesamtverteilung, Kategorien, Wahrnehmungslücken
- [ ] `plan`: Umverteilungsplan bearbeiten + Sign-off beider Partner:innen
- [ ] `checkins`: Wöchentlicher Check-in Flow + gemeinsame Auswertung + Verlaufs-Chart

## Block 4 — Polish & Qualität

- [ ] Base-Template + Dashboard + Landing Page + Bootstrap 5 einbinden
- [ ] Ruff check + format auf gesamtem Codebase, Pyright-Fehler beheben
- [ ] Alle Tests laufen lassen, Coverage ≥ 80% sicherstellen
- [ ] Finalen Stand committen und pushen
