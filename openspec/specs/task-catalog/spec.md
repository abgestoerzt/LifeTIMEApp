# Spec: Task Catalog

## Capability

A fixed catalog of ~45 standard household tasks organized into categories. Tasks are the atomic unit that both partners answer during the survey, plan in the redistribution, and track in check-ins.

## Implementation

- `catalog/models.py`: `Kategorie`, `Aufgabe`
- `catalog/migrations/0002_aufgabenkatalog.py`: data migration that seeds all standard tasks
- `catalog/admin.py`: full admin interface for both models
- `catalog/services.py`: empty (stub, populated by the custom-tasks change)
- `catalog/views.py`: empty (stub, populated by the custom-tasks change)

## Data model

```
Kategorie
├─ name (str)
├─ icon (str — emoji)
├─ ist_optional (bool)   — True for Kinderbetreuung + Haustiere
└─ reihenfolge (int)     — display order

Aufgabe
├─ kategorie (FK Kategorie, nullable)
├─ bezeichnung (str)
├─ ist_standard (bool)   — False = couple-created custom task
├─ paar_session (FK PaarSession, nullable) — set only for custom tasks
├─ erstellt_von (FK User)
└─ reihenfolge (int)
```

## Standard categories (10 total)

| # | Name | Icon | Optional |
|---|---|---|---|
| 1 | Ernährung | 🍽️ | No |
| 2 | Haushalt | 🏠 | No |
| 3 | Wäsche & Kleidung | 👕 | No |
| 4 | Finanzen | 💰 | No |
| 5 | Wohnen & Technik | 🔧 | No |
| 6 | Gesundheit | 🏥 | No |
| 7 | Soziales & Familie | 🎉 | No |
| 8 | Freizeit & Urlaub | ✈️ | No |
| 9 | Kinderbetreuung | 👶 | **Yes** |
| 10 | Haustiere | 🐾 | **Yes** |

Plus a special "Eigene Aufgaben" category for couple-created tasks.

## Task filtering per session

Tasks shown in the survey are filtered by `PaarSession.setup_kinder` and `PaarSession.setup_haustiere`:
- `ist_optional=False` categories always shown
- Kinderbetreuung shown only if `setup_kinder=True`
- Haustiere shown only if `setup_haustiere=True`
- Custom tasks (`ist_standard=False`) shown only for their own session

This filtering is implemented in `survey/services.py`, not in the catalog app.

## Invariants

- Standard tasks (`ist_standard=True`) have `paar_session=None`
- Custom tasks (`ist_standard=False`) always have `paar_session` and `erstellt_von` set
- Standard tasks are never deleted or edited (seeded via migration, treated as read-only)
