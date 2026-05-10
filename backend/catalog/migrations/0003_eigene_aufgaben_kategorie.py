from django.db import migrations


def add_eigene_aufgaben_kategorie(apps, schema_editor):
    Kategorie = apps.get_model("catalog", "Kategorie")
    Kategorie.objects.get_or_create(
        name="Eigene Aufgaben",
        defaults={
            "icon": "✏️",
            "ist_optional": False,
            "reihenfolge": 99,
        },
    )


def remove_eigene_aufgaben_kategorie(apps, schema_editor):
    Kategorie = apps.get_model("catalog", "Kategorie")
    Kategorie.objects.filter(name="Eigene Aufgaben").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_aufgabenkatalog"),
    ]

    operations = [
        migrations.RunPython(
            add_eigene_aufgaben_kategorie,
            remove_eigene_aufgaben_kategorie,
        ),
    ]
