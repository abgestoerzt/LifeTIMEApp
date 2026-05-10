# Custom Tasks — Design

## Data model

No model changes needed. The existing `Aufgabe` model already supports this:

```python
Aufgabe(
    kategorie=<eigene_aufgaben_kategorie>,
    bezeichnung="Gemüsegarten pflegen",
    ist_standard=False,
    paar_session=session,
    erstellt_von=request.user,
)
```

The "Eigene Aufgaben" Kategorie must exist in the database. It's already seeded via the data migration (`0002_aufgabenkatalog.py`) — verify it has `ist_optional=False` so it always shows.

## Service layer (`catalog/services.py`)

```python
def get_eigene_kategorie() -> Kategorie:
    """Returns the fixed 'Eigene Aufgaben' category."""

def aufgabe_erstellen(paar_session: PaarSession, user: User, bezeichnung: str) -> Aufgabe:
    """Creates a custom task for the session. Raises if session status not in {offen, test_laeuft}."""

def aufgabe_loeschen(aufgabe: Aufgabe, user: User) -> None:
    """Deletes a custom task. Raises if already answered or if user didn't create it."""
```

## Views (`catalog/views.py`)

### `aufgabe_erstellen` (POST only)
- `@login_required`
- Gets active session, validates status ∈ {offen, test_laeuft}
- Calls `aufgabe_erstellen()` service
- Redirects to `survey:start`

### `aufgabe_loeschen` (POST only)
- `@login_required`
- Validates aufgabe belongs to user's session
- Validates aufgabe has no Antwort yet
- Calls `aufgabe_loeschen()` service
- Redirects to `survey:start`

## URLs (`catalog/urls.py`)

```
POST /katalog/aufgabe/erstellen/      → catalog:aufgabe_erstellen
POST /katalog/aufgabe/<pk>/loeschen/  → catalog:aufgabe_loeschen
```

Wire into `config/urls.py`:
```python
path("katalog/", include("catalog.urls", namespace="catalog")),
```

## Form (`catalog/forms.py`)

```python
class AufgabeErstellenForm(forms.Form):
    bezeichnung = forms.CharField(max_length=200, label="Aufgabe")
```

## UI integration

The form appears on the **survey start page** (`survey/templates/survey/start.html`), below the category list:

```
┌─ Eigene Aufgaben hinzufügen ──────────────────────────┐
│  [___________________________] [+ Hinzufügen]         │
│                                                        │
│  • Gemüsegarten pflegen  [×]                          │
│  • Mietwohnung verwalten [×]  (× disabled if answered)│
└────────────────────────────────────────────────────────┘
```

The delete `[×]` button is a small POST form (no JS required). Disabled/hidden once the task has any Antwort.

## Access control summary

| Action | Allowed when |
|---|---|
| Add task | status ∈ {offen, test_laeuft}, any partner |
| Delete task | status ∈ {offen, test_laeuft}, task has no Antwort, user is creator |
| View in survey | always (same as standard tasks) |
| View in plan | always |
| View in checkins | always (unless marked abschaffen in plan) |
