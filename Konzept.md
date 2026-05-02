# Konzept: Mental Load App für Paare

> **Status:** Finalisiert ✓

---

## 1. Was ist Mental Load?

Mental Load bezeichnet die **unsichtbare Organisationsarbeit** im Alltag: nicht nur Aufgaben *erledigen*, sondern an sie *denken*, sie *planen*, *koordinieren* und *im Blick behalten*. Das unterscheidet sich wesentlich vom schlichten "Wer putzt das Bad?" – entscheidend ist, wer dafür sorgt, dass es überhaupt auf der Agenda steht.

Studien zeigen, dass dieser kognitive und emotionale Anteil der Haushaltsarbeit stark ungleich verteilt ist, meist zu Lasten einer Person (meistens Frauen). Das Konzept geht auf die Comic-Autorin Emma zurück ("Fallait y penser", 2017) und wurde durch Organisationen wie **Equal Care Day** (klische\*esc e.V.) mit konkreten Testinstrumenten greifbar gemacht.

---

## 2. Ziel der App

Eine Web-App, die Paaren ermöglicht:

1. **Den Mental Load Test getrennt voneinander durchzuführen** – jede:r beantwortet für sich, ohne die Antworten der anderen Person zu sehen
2. **Eine gemeinsame Auswertung zu sehen** – visualisierte Gegenüberstellung: Wer trägt wie viel Last in welchen Bereichen?
3. **Aufgaben gemeinsam neu zu verteilen und den Plan gemeinsam zu unterzeichnen**
4. **Wöchentliche Check-ins durchführen** – regelmäßig prüfen, ob der neue Plan im Alltag funktioniert

Nicht: eine Schuldzuweisung. **Ja:** ein Gesprächseinstieg mit konkreter Grundlage — und ein Werkzeug für langfristige Veränderung.

---

## 3. Der Test – Struktur und Logik

### 3.1 Kernunterscheidung

Für jede Aufgabe wird unterschieden:

| Dimension | Bedeutung |
|---|---|
| **Denken / Managen** | Wer hat diese Aufgabe im Kopf, plant sie, initiiert sie? |
| **Ausführen** | Wer macht sie konkret? |

Diese Trennung ist der Kern: jemand kann eine Aufgabe *ausführen*, ohne sie jemals *zu managen* – und umgekehrt.

### 3.2 Antwortoptionen (je Aufgabe, je Dimension)

- Ich
- Mein:e Partner:in
- Wir beide gleichermaßen
- Jemand anderes / extern
- Trifft auf uns nicht zu

### 3.3 Aufgabenkatalog

Basis: Aufgabenkatalog angelehnt an Equal Care Day @home — frei adaptiert.
Zusätzlich können **Paare eigene Aufgaben** hinzufügen, die in ihrem Alltag relevant sind.

#### Kategorien und Beispielaufgaben

| Kategorie | Beispielaufgaben |
|---|---|
| **Ernährung** | Wochenmenü planen, Einkaufsliste schreiben, Einkaufen, Kochen, Vorräte prüfen, Reste verwerten |
| **Haushalt** | Putzplan, Staubsaugen, Bad putzen, Küche putzen, Müll, Wohnung aufräumen, Handwerker beauftragen |
| **Wäsche & Kleidung** | Wäsche waschen, Wäsche aufhängen/einräumen, Bügeln, Saisonkleidung wechseln, Kleidung nachkaufen |
| **Finanzen** | Rechnungen bezahlen, Haushaltsbuch/Budget, Steuererklärung, Versicherungen prüfen, Sparen/Anlegen |
| **Wohnen & Technik** | Kleine Reparaturen, Geräte warten, Behördengänge, Post bearbeiten, Abonnements verwalten |
| **Gesundheit** | Arzttermine organisieren, Medikamente, Vorsorgeuntersuchungen, Sport/Bewegung einplanen |
| **Soziales** | Geburtstage im Blick haben, Geschenke, Kontakt zu Familie/Freunden pflegen, Einladungen |
| **Freizeit & Urlaub** | Aktivitäten planen, Urlaub buchen, Dates/Ausflüge organisieren |
| *(optional)* **Kinderbetreuung** | Kita/Schule, Arzttermine Kinder, Aktivitäten, Schulzeug, Elterngespräche |
| *(optional)* **Haustiere** | Füttern, Tierarzt, Pflege, Betreuung bei Abwesenheit |
| **Eigene Aufgaben** | Frei definierbar durch das Paar |

**Optionale Kategorien** (Kinderbetreuung, Haustiere) werden beim Setup des Tests aktiviert/deaktiviert.

Geschätzte Aufgabenzahl: **~35–45 Aufgaben** + individuelle Ergänzungen.

### 3.4 Testdauer und Fortschritt

Ca. 10–15 Minuten. Fortschritt wird gespeichert — der Test muss nicht in einem Stück abgeschlossen werden.

---

## 4. Vollständiger User Flow

```
[Person A]                              [Person B]
    |                                        |
Registrierung (Account)             Registrierung (Account)
    |                                        |
Paar erstellen                       Einladecode eingeben
(erhält Einladecode, 7 Tage gültig)       |
    |                                   Paar beigetreten
    |                                        |
Setup: Optionale Kategorien wählen          |
(Kinder? Haustiere?)                        |
    |                                        |
    ├──────────── Test-Phase ────────────────┤
    |                                        |
Test unabhängig durchführen         Test unabhängig durchführen
(Antworten der anderen Person           (Antworten der anderen Person
 nicht sichtbar)                         nicht sichtbar)
    |                                        |
    └──────────── Beide fertig? ─────────────┘
                        |
              ┌─ Gemeinsame Auswertung ─┐
              │  - Gesamtverteilung     │
              │  - Kategorien-Charts    │
              │  - Wahrnehmungslücken   │
              └─────────────────────────┘
                        |
              ┌─ Umverteilungsplan ─────┐
              │  - Neue Zuweisung       │
              │    je Aufgabe           │
              │  - Person A signiert ✓  │
              │  - Person B signiert ✓  │
              └─────────────────────────┘
                        |
              ┌─ Wöchentliche Check-ins ┐
              │  (ab jetzt, dauerhaft)  │
              └─────────────────────────┘
```

### Flow-Details

- Solange einer noch nicht fertig ist: Auswertung gesperrt, Status sichtbar ("Partner:in noch nicht fertig")
- Einladecode: 7 Tage gültig, einmalig verwendbar
- Kategorien-Setup macht nur Person A (die das Paar erstellt)

---

## 5. Auswertung

### 5.1 Gesamtübersicht

- **Donut-Chart oder Balken:** Gesamtanteil Mental Load — Person A vs. Person B
- Aufgeteilt: Denken/Managen vs. Ausführen (zwei separate Werte)
- Highlight: "Unsichtbare Arbeit" = hoher Management-Anteil bei einer Person

### 5.2 Kategorie-Ansicht

- Pro Kategorie: Balkendiagramm (Person A / Person B / Beide / Extern)
- Sortiert nach Ungleichgewicht — die schiefstes Kategorien oben

### 5.3 Aufgaben-Detailansicht (Wahrnehmungslücken)

Tabellarisch: jede Aufgabe, Antwort A, Antwort B, Bewertung

Besonders markiert:
| Muster | Bedeutung | Markierung |
|---|---|---|
| A: "Ich" — B: "Ich" | Beide denken sie machen es | ⚠️ Konflikt |
| A: "Ich" — B: "Beide" | A's Arbeit wird nicht gesehen | 👁️ Unsichtbar |
| A: "Partner:in" — B: "Partner:in" | Niemand macht es wirklich | ❓ Lücke |
| A: "Ich" — B: "Partner:in" | Volle Übereinstimmung | ✓ |

---

## 6. Umverteilungsplan

### Wie es funktioniert

Nach der Auswertung erstellen beide gemeinsam einen neuen Verteilungsplan:
- Für jede Aufgabe: neue Zuweisung für Management + Ausführung
- Optionen: Person A / Person B / Beide / Extern / Aufgabe abschaffen

### Sign-off / Unterzeichnung

Beide Partner:innen müssen den Plan explizit **bestätigen** ("Ich stimme diesem Plan zu"):
- Erst wenn beide unterzeichnet haben, gilt der Plan als aktiv
- Unterzeichnung wird mit Timestamp gespeichert
- Plan kann danach bearbeitet werden → löst neuen Sign-off-Prozess aus

### Export

- Druckansicht / PDF-Export des Plans als gemeinsames Dokument

---

## 7. Wöchentliche Check-ins

### Idee

Jede Woche können (und sollen) beide Partner:innen unabhängig voneinander einen kurzen Check-in machen:  
**"Wie gut hat die neue Aufgabenverteilung diese Woche funktioniert?"**

### Ablauf

1. Dashboard zeigt: "Check-in für diese Woche ausstehend"
2. Jede Person geht durch die Aufgaben aus dem Umverteilungsplan
3. Pro Aufgabe: **Hat das diese Woche funktioniert?**
   - ✅ Ja
   - ⚠️ Teilweise
   - ❌ Nein / nicht passiert
4. Optional: kurze Notiz (Freitext)
5. Wenn beide eingecheckt haben: **gemeinsame Check-in-Auswertung** sichtbar

### Check-in-Auswertung

- Welche Aufgaben laufen gut?
- Welche stocken noch? (Bei beiden oder nur bei einer Person anders wahrgenommen?)
- Trend über Zeit: Fortschritts-Chart ("Woche 1 bis heute")

### Erinnerung

- Kein automatischer E-Mail-Versand in v1
- Stattdessen: prominente Anzeige auf dem Dashboard ("Letzter Check-in: vor 9 Tagen")

---

## 8. Technisches Konzept

### 8.1 Stack

- **Backend + Frontend:** Django 5.x, Django Templates
- **Datenbank:** SQLite (Entwicklung) → PostgreSQL (Produktion)
- **Styling:** Bootstrap 5 via CDN
- **Charts:** Chart.js via CDN
- **Kein** separates JS-Framework

### 8.2 Datenmodell

```
User (Django built-in)

PaarSession
  ├─ partner_a (FK User)
  ├─ partner_b (FK User, nullable bis Beitritt)
  ├─ invite_code (unique, zufällig generiert)
  ├─ invite_expires_at (DateTimeField)
  ├─ status: [offen, test_laeuft, beide_fertig, plan_aktiv]
  ├─ setup_kinder (bool)
  ├─ setup_haustiere (bool)
  └─ created_at

Kategorie
  ├─ name
  ├─ icon (emoji oder CSS-Klasse)
  ├─ ist_optional (bool)
  └─ reihenfolge

Aufgabe
  ├─ kategorie (FK Kategorie, nullable für eigene Aufgaben)
  ├─ bezeichnung
  ├─ ist_standard (bool) – False = selbst erstellt vom Paar
  ├─ paar_session (FK PaarSession, nullable für Standardaufgaben)
  └─ reihenfolge

CHOICES = [ich, partner, beide, extern, trifft_nicht_zu]

Antwort
  ├─ paar_session (FK)
  ├─ user (FK)
  ├─ aufgabe (FK)
  ├─ management (CHOICES)
  └─ ausfuehrung (CHOICES)

PLAN_CHOICES = [person_a, person_b, beide, extern, abschaffen]

Umverteilung
  ├─ paar_session (FK)
  ├─ aufgabe (FK)
  ├─ management_neu (PLAN_CHOICES)
  ├─ ausfuehrung_neu (PLAN_CHOICES)
  ├─ signoff_a (bool, default False)
  ├─ signoff_a_at (DateTimeField, nullable)
  ├─ signoff_b (bool, default False)
  └─ signoff_b_at (DateTimeField, nullable)

CheckIn
  ├─ paar_session (FK)
  ├─ woche (DateField – Montag der jeweiligen Woche)
  ├─ user (FK)
  └─ abgeschlossen_at (DateTimeField)

CheckInAntwort
  ├─ checkin (FK CheckIn)
  ├─ aufgabe (FK)
  ├─ status: [ja, teilweise, nein]
  └─ notiz (TextField, blank)
```

### 8.3 URL-Struktur

```
/                           – Landing Page
/registrieren/              – Registrierung
/login/                     – Login
/logout/                    – Logout
/dashboard/                 – Übersicht (nach Login)

/paar/erstellen/            – Neues Paar + Einladecode generieren
/paar/beitreten/            – Einladecode eingeben
/paar/setup/                – Optionale Kategorien wählen

/test/                      – Test starten / fortsetzen
/test/<kategorie_id>/       – Test: Aufgaben einer Kategorie

/auswertung/                – Gemeinsame Auswertung
/umverteilung/              – Umverteilungsplan bearbeiten
/umverteilung/signoff/      – Plan unterzeichnen

/checkin/                   – Wöchentlichen Check-in starten
/checkin/auswertung/        – Gemeinsame Check-in-Auswertung
/checkin/verlauf/           – Fortschrittsverlauf über Zeit
```

---

## 9. Was ist NICHT der Scope (v1)

- Keine Mobile App (responsives Web reicht)
- Kein Echtzeit / WebSocket
- Kein Chat / Kommentarfunktion
- Keine E-Mail-Benachrichtigungen
- Keine sozialen Features
- Kein Abo / Bezahlmodell
- Kein Mehrsprachigkeit (erst Deutsch)

---

## 10. Implementierungs-Reihenfolge

1. **Repo aufräumen** – altes `lifecalendar`-App entfernen, neue App `mentalload` anlegen
2. **Datenmodell** – alle Models, Migrations, Admin
3. **Auth-Flow** – Registrierung, Login, Logout
4. **Pairing-Flow** – Paar erstellen, Einladecode, beitreten, Setup
5. **Test-Flow** – Test durchführen (kategorieweise, Fortschritt speichern)
6. **Auswertung** – Charts, Wahrnehmungslücken
7. **Umverteilungsplan** – Bearbeiten + Sign-off
8. **Wöchentliche Check-ins** – Check-in Flow + Verlaufsansicht
9. **Polish** – Landing Page, Dashboard, responsive Design
