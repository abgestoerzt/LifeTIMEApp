from django.db import migrations

KATALOG = [
    {
        "name": "Ernährung",
        "icon": "🍽️",
        "ist_optional": False,
        "reihenfolge": 1,
        "aufgaben": [
            "Wochenmenü planen",
            "Einkaufsliste schreiben",
            "Einkaufen gehen",
            "Kochen",
            "Vorräte prüfen und nachkaufen",
            "Reste verwerten",
        ],
    },
    {
        "name": "Haushalt",
        "icon": "🏠",
        "ist_optional": False,
        "reihenfolge": 2,
        "aufgaben": [
            "Putzplan erstellen",
            "Staubsaugen",
            "Bad putzen",
            "Küche putzen",
            "Wohnung aufräumen",
            "Müll entsorgen und Tonnen rausstellen",
            "Handwerker beauftragen und koordinieren",
        ],
    },
    {
        "name": "Wäsche & Kleidung",
        "icon": "👕",
        "ist_optional": False,
        "reihenfolge": 3,
        "aufgaben": [
            "Wäsche waschen",
            "Wäsche aufhängen und einräumen",
            "Bügeln",
            "Saisonkleidung wechseln",
            "Kleidung nachkaufen",
        ],
    },
    {
        "name": "Finanzen",
        "icon": "💰",
        "ist_optional": False,
        "reihenfolge": 4,
        "aufgaben": [
            "Rechnungen bezahlen",
            "Haushaltsbuch / Budget führen",
            "Steuererklärung",
            "Versicherungen prüfen und verwalten",
            "Sparen und Anlegen",
        ],
    },
    {
        "name": "Wohnen & Technik",
        "icon": "🔧",
        "ist_optional": False,
        "reihenfolge": 5,
        "aufgaben": [
            "Kleine Reparaturen erledigen",
            "Geräte warten und ersetzen",
            "Behördengänge und Ämter",
            "Post bearbeiten",
            "Abonnements und Verträge verwalten",
        ],
    },
    {
        "name": "Gesundheit",
        "icon": "🏥",
        "ist_optional": False,
        "reihenfolge": 6,
        "aufgaben": [
            "Arzttermine organisieren",
            "Medikamente besorgen und verwalten",
            "Vorsorgeuntersuchungen im Blick behalten",
            "Sport und Bewegung einplanen",
        ],
    },
    {
        "name": "Soziales",
        "icon": "🎉",
        "ist_optional": False,
        "reihenfolge": 7,
        "aufgaben": [
            "Geburtstage und Jahrestage im Blick behalten",
            "Geschenke organisieren",
            "Kontakt zu Familie und Freunden pflegen",
            "Einladungen planen und koordinieren",
        ],
    },
    {
        "name": "Freizeit & Urlaub",
        "icon": "✈️",
        "ist_optional": False,
        "reihenfolge": 8,
        "aufgaben": [
            "Freizeitaktivitäten planen",
            "Urlaub recherchieren und buchen",
            "Dates und Ausflüge organisieren",
        ],
    },
    {
        "name": "Kinderbetreuung",
        "icon": "👶",
        "ist_optional": True,
        "reihenfolge": 9,
        "aufgaben": [
            "Kita / Schule koordinieren",
            "Arzttermine der Kinder organisieren",
            "Freizeitaktivitäten der Kinder planen",
            "Schulzeug und Materialien besorgen",
            "Elterngespräche und Schulfeste",
        ],
    },
    {
        "name": "Haustiere",
        "icon": "🐾",
        "ist_optional": True,
        "reihenfolge": 10,
        "aufgaben": [
            "Tiere füttern und versorgen",
            "Tierarzttermine organisieren",
            "Pflege und Pflegeroutinen",
            "Betreuung bei Abwesenheit organisieren",
        ],
    },
]


def erstelle_katalog(apps, schema_editor):  # type: ignore[no-untyped-def]
    Kategorie = apps.get_model("catalog", "Kategorie")
    Aufgabe = apps.get_model("catalog", "Aufgabe")
    for kat_data in KATALOG:
        aufgaben = kat_data.pop("aufgaben")
        kategorie = Kategorie.objects.create(**kat_data)
        for i, bezeichnung in enumerate(aufgaben):
            Aufgabe.objects.create(
                kategorie=kategorie,
                bezeichnung=bezeichnung,
                ist_standard=True,
                reihenfolge=i,
            )


def loesche_katalog(apps, schema_editor):  # type: ignore[no-untyped-def]
    Kategorie = apps.get_model("catalog", "Kategorie")
    Kategorie.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(erstelle_katalog, loesche_katalog),
    ]
