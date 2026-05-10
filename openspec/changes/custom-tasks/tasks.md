# Custom Tasks — Tasks

- [x] Task 1: Implement catalog/services.py
- [x] Task 2: Create form and views
- [x] Task 3: Add URLs
- [x] Task 4: Update survey start template
- [x] Task 5: Write tests

---

## Task 1: Implement catalog/services.py

Create `backend/catalog/services.py` with three functions:

**`get_eigene_kategorie() -> Kategorie`**
- Query `Kategorie.objects.get(name="Eigene Aufgaben")`
- This category is already seeded in migration `0002_aufgabenkatalog.py` — verify it exists and has `ist_optional=False`

**`aufgabe_erstellen(paar_session: PaarSession, user: User, bezeichnung: str) -> Aufgabe`**
- Raise `ValueError` if `paar_session.status not in ("offen", "test_laeuft")`
- Create and return `Aufgabe(kategorie=get_eigene_kategorie(), bezeichnung=bezeichnung.strip(), ist_standard=False, paar_session=paar_session, erstellt_von=user)`

**`aufgabe_loeschen(aufgabe: Aufgabe, user: User) -> None`**
- Raise `PermissionError` if `aufgabe.erstellt_von != user`
- Raise `ValueError` if `Antwort.objects.filter(aufgabe=aufgabe).exists()`
- Delete the aufgabe

---

## Task 2: Create form and views

**`backend/catalog/forms.py`**

```python
class AufgabeErstellenForm(forms.Form):
    bezeichnung = forms.CharField(max_length=200, label="Aufgabe", strip=True)
```

**`backend/catalog/views.py`**

`aufgabe_erstellen(request)`:
- `@login_required`, POST only (return 405 for GET)
- Get active session via `pairs.services.get_aktive_session(request.user)` — redirect to dashboard if None
- Validate `AufgabeErstellenForm`, call `catalog.services.aufgabe_erstellen()`
- On `ValueError` (wrong status): add form error and redirect back to `survey:start`
- On success: redirect to `survey:start`

`aufgabe_loeschen(request, pk)`:
- `@login_required`, POST only
- Get `Aufgabe` by pk, verify `aufgabe.paar_session == get_aktive_session(request.user)`
- Call `catalog.services.aufgabe_loeschen()` — catch `PermissionError` and `ValueError`, redirect with error message
- On success: redirect to `survey:start`

---

## Task 3: Add URLs

Create `backend/catalog/urls.py`:

```python
app_name = "catalog"
urlpatterns = [
    path("aufgabe/erstellen/", views.aufgabe_erstellen, name="aufgabe_erstellen"),
    path("aufgabe/<int:pk>/loeschen/", views.aufgabe_loeschen, name="aufgabe_loeschen"),
]
```

Add to `backend/config/urls.py`:
```python
path("katalog/", include("catalog.urls", namespace="catalog")),
```

---

## Task 4: Update survey start template

In `backend/survey/templates/survey/start.html`, add a section below the category list:

- A form (`action="{% url 'catalog:aufgabe_erstellen' %}"`, method=POST) with a text input and submit button
- A list of existing custom tasks with a delete button per task (small POST form, `action="{% url 'catalog:aufgabe_loeschen' task.pk %}"`)
- Show delete button only if `task.erstellt_von == request.user` and task has no answers

The view needs to pass `eigene_aufgaben` to the template context — update `survey/views.py`'s `start` view to include:
```python
from catalog.services import get_eigene_kategorie
eigene_aufgaben = Aufgabe.objects.filter(paar_session=session, ist_standard=False)
```

---

## Task 5: Write tests

Create `backend/catalog/tests/__init__.py` and `backend/catalog/tests/test_services.py`.

Test `aufgabe_erstellen()`:
- Creates task with correct FK values
- Raises ValueError when status is `beide_fertig`
- bezeichnung is stripped of whitespace

Test `aufgabe_loeschen()`:
- Deletes task when user is creator and task has no answers
- Raises PermissionError when called by non-creator
- Raises ValueError when task already has an Antwort

Create `backend/catalog/tests/test_views.py`.

Test `aufgabe_erstellen` view:
- Requires login
- POST with valid data → creates task, redirects to survey:start
- POST when status=beide_fertig → redirects with error, no task created

Test `aufgabe_loeschen` view:
- Requires login
- POST by creator, no answers → deletes, redirects
- POST by other user → no delete, error response
