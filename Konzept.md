# Konzept: Mental Load App für Paare

> **Status:** Entwurf – zur gemeinsamen Besprechung

---

## 1. Was ist Mental Load?

Mental Load bezeichnet die **unsichtbare Organisationsarbeit** im Alltag: nicht nur Aufgaben *erledigen*, sondern an sie *denken*, sie *planen*, *koordinieren* und *im Blick behalten*. Das unterscheidet sich wesentlich vom schlichten "Wer putzt das Bad?" – entscheidend ist, wer dafür sorgt, dass es überhaupt auf der Agenda steht.

Studien zeigen, dass dieser kognitive und emotionale Anteil der Haushaltsarbeit stark ungleich verteilt ist, meist zu Lasten einer Person (meistens Frauen). Das Konzept geht auf die Comic-Autorin Emma zurück ("Fallait y penser", 2017) und wurde durch Organisationen wie **Equal Care Day** (klische\*esc e.V.) mit konkreten Testinstrumenten greifbar gemacht.

---

## 2. Ziel der App

Eine Web-App, die Paaren ermöglicht:

1. **Den Mental Load Test getrennt voneinander durchzuführen** – jede:r beantwortet für sich, ohne die Antworten der anderen Person zu sehen
2. **Eine gemeinsame Auswertung zu sehen** – visualisierte Gegenüberstellung: Wer trägt wie viel Last in welchen Bereichen?
3. **Aufgaben gemeinsam neu zu verteilen** – einen Umverteilungsplan erstellen und festhalten

Nicht: eine Schuldzuweisung. **Ja:** ein Gesprächseinstieg mit konkreter Grundlage.

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

### 3.3 Kategorien und Aufgaben (@home)

> **Offene Frage:** Verwenden wir den exakten Aufgabenkatalog von Equal Care Day oder entwickeln wir einen eigenen? Lizenzfrage klären.

Vorgeschlagene Kategorien (angelehnt an den ECD-Test):

| Kategorie | Beispielaufgaben |
|---|---|
| **Ernährung** | Mahlzeiten planen, Einkaufsliste, Kochen, Vorräte prüfen |
| **Haushalt** | Putzen, Aufräumen, Müll, Renovierungen beauftragen |
| **Wäsche & Kleidung** | Waschen, Bügeln, Kleidung einkaufen |
| **Finanzen** | Rechnungen, Budget, Steuern, Versicherungen |
| **Wohnen & Technik** | Reparaturen, Geräte warten, Behördengänge |
| **Gesundheit** | Arzttermine, Medikamente, Vorsorge |
| **Soziales** | Geburtstage, Geschenke, Kontakt zu Familie/Freunden |
| **Freizeit & Urlaub** | Planung, Buchungen, Aktivitäten |
| *(optional)* **Kinderbetreuung** | Schule, Arzt, Aktivitäten der Kinder |
| *(optional)* **Haustiere** | Füttern, Tierarzt, Pflege |

Geschätzte Aufgabenzahl: **~30–50 Aufgaben** gesamt (konfigurierbar).

### 3.4 Testdauer

Ca. 10–15 Minuten. Man muss den Test nicht in einem Stück fertigmachen (Fortschritt wird gespeichert).

---

## 4. User Flow

```
[Person A]                          [Person B]
    |                                    |
Registrierung                    Registrierung
    |                                    |
Paar erstellen ──── Einladecode ────> Paar beitreten
    |                                    |
Test unabhängig                  Test unabhängig
durchführen                      durchführen
    |                                    |
    └──────── Beide fertig? ─────────────┘
                    |
             Gemeinsame Auswertung
                    |
             Umverteilungsplan
                    |
                Speichern / Drucken
```

### Details

- Solange einer noch nicht fertig ist, bleibt die Auswertung gesperrt
- Keine Person sieht die Antworten der anderen, bevor beide fertig sind
- Der Einladecode ist zeitlich begrenzt (z.B. 7 Tage)

---

## 5. Auswertung – Visualisierung

### 5.1 Übersicht (Dashboard)

- **Gesamtverteilung:** Wer trägt wie viel Mental Load (in %) gesamt?
- Aufgeteilt nach: Denken vs. Ausführen

### 5.2 Kategorie-Ansicht

- Pro Kategorie: Balkendiagramm oder Heatmap
- Farben: Person A / Person B / Beide / Extern

### 5.3 Aufgaben-Detailansicht

- Tabellarisch: jede Aufgabe, Antwort A, Antwort B, Übereinstimmung/Unterschied
- Besonders markiert: **Wahrnehmungslücken** (A sagt "Ich", B sagt auch "Ich" → Konfliktpotenzial) oder (A sagt "Ich", B sagt "Beide" → Unsichtbare Arbeit)

---

## 6. Umverteilungsplan (Schritt 2)

Nach der Auswertung können beide gemeinsam festlegen:

- Wer übernimmt eine Aufgabe künftig (Management + Ausführung)?
- Optionen: Ich / Partner:in / Beide / Extern / Abschaffen

Der Plan wird gespeichert und kann exportiert / ausgedruckt werden.

> **Offene Frage:** Soll der Umverteilungsplan von beiden bestätigt werden müssen ("Sign-off")? Oder reicht ein gemeinsamer Entwurf?

---

## 7. Technisches Konzept

### 7.1 Stack (wie besprochen: reines Django)

- **Backend + Frontend:** Django 5.x, Django Templates
- **Datenbank:** SQLite (Entwicklung) → PostgreSQL (Produktion, optional)
- **Styling:** CSS (Bootstrap oder Tailwind via CDN) — kein JS-Framework
- **Charts:** Chart.js via CDN

### 7.2 Datenmodell (Entwurf)

```
User (Django built-in)
  └─ PaarSession
        ├─ partner_a (FK User)
        ├─ partner_b (FK User, nullable bis Beitritt)
        ├─ invite_code
        ├─ status: [offen, beide_fertig, ausgewertet]
        └─ created_at

Kategorie
  ├─ name
  ├─ icon
  └─ reihenfolge

Aufgabe
  ├─ kategorie (FK)
  ├─ bezeichnung
  ├─ optional (bool) – z.B. Kinderbetreuung
  └─ reihenfolge

Antwort
  ├─ paar_session (FK)
  ├─ user (FK)
  ├─ aufgabe (FK)
  ├─ management: [ich, partner, beide, extern, trifft_nicht_zu]
  └─ ausfuehrung: [ich, partner, beide, extern, trifft_nicht_zu]

Umverteilung
  ├─ paar_session (FK)
  ├─ aufgabe (FK)
  ├─ management_neu: [ich_a, ich_b, beide, extern, abschaffen]
  └─ ausfuehrung_neu: [ich_a, ich_b, beide, extern, abschaffen]
```

### 7.3 URL-Struktur

```
/                      – Landing Page
/registrieren/         – Registration
/login/                – Login
/paar/erstellen/       – Neues Paar + Einladecode
/paar/beitreten/       – Einladecode eingeben
/test/                 – Test durchführen (mit Fortschritt)
/auswertung/           – Gemeinsame Auswertung (nur wenn beide fertig)
/umverteilung/         – Umverteilungsplan bearbeiten
```

---

## 8. Offene Fragen / Diskussionspunkte

1. **Lizenz der Testfragen:** Eigenen Aufgabenkatalog erstellen oder bestehenden adaptieren?
2. **Kinderbetreuung:** Als optionaler Bereich zu Beginn wählbar (je nach Lebenssituation)?
3. **Anonym oder Account-basiert?** Accounts ermöglichen Rückschau und Wiederholung — aber erhöhen Hürde.
4. **Sprache:** Erst nur Deutsch? Englisch später?
5. **Umverteilungs-Sign-off:** Muss Plan von beiden bestätigt werden?
6. **Re-Test:** Sollen Paare denselben Test nach 3/6 Monaten wiederholen können, um Fortschritt zu messen?
7. **Mehrsprachige Kategorienamen:** Oder fix Deutsch?

---

## 9. Was ist NICHT der Scope (v1)

- Keine Mobile App (responsive Web reicht)
- Kein Echtzeit (kein WebSocket)
- Kein Chat / Kommentarfunktion
- Keine sozialen Features
- Kein Abo / Bezahlmodell

---

## 10. Nächste Schritte

1. Konzept besprechen und finalisieren
2. Aufgabenkatalog erstellen (ca. 30–40 Aufgaben)
3. Datenmodell implementieren
4. Auth + Pairing Flow
5. Test-Flow
6. Auswertungs-View + Charts
7. Umverteilungsplan
