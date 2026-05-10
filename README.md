# LifeTIME App

**Mental Load sichtbar machen. Gemeinsam neu verteilen. Dranbleiben.**

---

## Das Problem

Wer denkt eigentlich daran, dass der Kühlschrank leer ist? Wer hat die Arzttermine im Kopf, plant das Wochenende, behält die Finanzen im Blick?

Das ist **Mental Load** — die unsichtbare Organisationsarbeit im Alltag. Nicht nur Aufgaben *erledigen*, sondern an sie *denken*, sie *planen*, *koordinieren* und *im Blick behalten*. Der Unterschied ist entscheidend: jemand kann die Wäsche aufhängen, ohne jemals daran gedacht zu haben, dass sie überhaupt gewaschen werden muss.

Studien zeigen, dass dieser kognitive und emotionale Anteil der Haushaltsarbeit stark ungleich verteilt ist — meistens zu Lasten einer Person. Das Tückische: Es passiert oft unbewusst, und beide Partner haben unterschiedliche Wahrnehmungen davon. Was die eine Person als ihre Last empfindet, nimmt die andere Person vielleicht gar nicht als solche wahr.

Das führt zu Frustration, Erschöpfung und dem Gefühl, nicht gesehen zu werden — ohne dass irgendjemand böswillig handelt.

---

## Die Lösung

LifeTIME ist eine Web-App für Paare, die dieses Problem konkret und sachlich angeht:

1. **Test getrennt durchführen** — beide Partner beantworten unabhängig voneinander für ~35–45 Alltagsaufgaben: Wer denkt/plant das? Wer führt es aus? Keine gegenseitige Beeinflussung.

2. **Gemeinsame Auswertung** — visualisierte Gegenüberstellung: Wer trägt wie viel Last, in welchen Bereichen? Und wo weichen die Wahrnehmungen voneinander ab? ("Ich dachte, ich mache das — du auch?")

3. **Umverteilungsplan** — Aufgaben konkret neu zuweisen, den Plan gemeinsam unterzeichnen. Kein unverbindliches Gespräch, sondern eine gemeinsame Vereinbarung.

4. **Wöchentliche Check-ins** — regelmäßig prüfen: Hat der neue Plan diese Woche funktioniert? Fortschritt über Zeit verfolgen.

Nicht Schuldzuweisung. Sondern ein Gesprächseinstieg mit konkreter Grundlage — und ein Werkzeug für langfristige Veränderung.

---

## Use Case

**Persona:** Ein Paar, das das Gefühl hat, dass die Haushaltsorganisation ungleich verteilt ist — aber nicht genau weiß, wo und wie. Oder das dieses Gespräch immer wieder führt, ohne zu einer konkreten Veränderung zu kommen.

**Ablauf:**

```
Person A                                Person B
    │                                       │
Registrieren & Paar erstellen          Registrieren & beitreten
    │                 (Einladecode, 7 Tage gültig)
Setup: Kinder? Haustiere?                  │
    │                                       │
    ├──────────── Test ─────────────────────┤
    │                                       │
Aufgaben unabhängig beantworten    Aufgaben unabhängig beantworten
(Antworten der anderen Person           (gegenseitig nicht sichtbar)
 nicht sichtbar)
    │                                       │
    └──────── Beide fertig? ────────────────┘
                      │
            Gemeinsame Auswertung
            ├─ Gesamtverteilung (Denken vs. Ausführen)
            ├─ Kategorien-Breakdown
            └─ Wahrnehmungslücken (wer sieht was?)
                      │
            Umverteilungsplan erstellen
            ├─ Neue Zuweisung je Aufgabe
            ├─ Person A unterzeichnet ✓
            └─ Person B unterzeichnet ✓
                      │
            Wöchentliche Check-ins
            └─ Funktioniert der Plan im Alltag?
```

**Was der Test misst:** Für jede Aufgabe zwei Dimensionen — *Denken/Managen* (Wer hat es im Kopf?) und *Ausführen* (Wer macht es konkret?). Beides getrennt zu betrachten macht die unsichtbare Arbeit sichtbar.

**Was die Auswertung zeigt:** Gesamtanteile, Kategorie-Charts, und besonders: Wahrnehmungslücken — also Aufgaben, bei denen beide "Ich" angekreuzt haben (Konflikt), oder bei denen eine Person ihre eigene Arbeit gar nicht gesehen bekommt (Unsichtbar).

---

## Stack

Django 5.x · Django Templates · SQLite (Entwicklung) / PostgreSQL (Produktion) · Chart.js · Tailwind CSS

---

## Lokales Setup

### Voraussetzungen

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (`brew install uv` auf macOS)

### 1. Abhängigkeiten installieren

```bash
uv sync
```

### 2. Umgebungsvariablen konfigurieren

```bash
cp backend/.env.example backend/.env
```

`backend/.env` öffnen und `SECRET_KEY` setzen:

```bash
# Sicheren Key generieren:
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Datenbank migrieren

```bash
uv run python backend/manage.py migrate
```

### 4. Dev-Server starten

```bash
uv run python backend/manage.py runserver
```

App läuft unter [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. (Optional) Superuser anlegen

```bash
uv run python backend/manage.py createsuperuser
```

Admin: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## Entwicklung

```bash
uv run python backend/manage.py ...     # Django-Befehle
uv run pytest                           # Tests
uv run pytest --cov=. --cov-report=term-missing  # Tests mit Coverage
uv run ruff check .                     # Linting
uv run ruff format .                    # Formatierung
uv run pyright                          # Type-Check
```

---

## Projektstruktur

```
LifeTIMEApp/
├── backend/
│   ├── config/          # Settings, Root-URLs, WSGI/ASGI
│   ├── accounts/        # Registrierung, Login, User-Profil
│   ├── pairs/           # Paar-Session, Einladecode
│   ├── catalog/         # Kategorien und Aufgaben (inkl. eigene)
│   ├── survey/          # Test-Durchführung, Antworten
│   ├── results/         # Auswertung und Scoring-Logik
│   ├── plan/            # Umverteilungsplan, Sign-off
│   ├── checkins/        # Wöchentliche Check-ins, Verlauf
│   └── manage.py
├── openspec/            # Feature-Specs und Proposals
├── pyproject.toml       # Abhängigkeiten + Tool-Konfiguration
└── uv.lock
```

Settings: `backend/config/settings/base.py` (gemeinsam), `local.py` (Entwicklung), `production.py` (Produktion).
