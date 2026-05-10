# Spec: Custom Task Management

## Capability

Partners can add free-text tasks to their session's survey. These tasks behave identically to standard catalog tasks in every downstream flow (survey, plan, check-ins).

## Functional requirements

### Adding a task
- Both partners may add custom tasks
- Available while `PaarSession.status ∈ {offen, test_laeuft}`
- Input: a single `bezeichnung` field (1–200 characters, required)
- Task is immediately visible to both partners in the survey

### Deleting a task
- Only the partner who created the task may delete it
- Deletion is only possible if the task has no `Antwort` records yet (i.e. neither partner has answered it)
- Once answered, the task is permanent for the session

### Visibility
- Custom tasks appear in the "Eigene Aufgaben" category in the survey
- Custom tasks are included in `get_aufgaben_fuer_session()` results
- Custom tasks appear in the redistribution plan alongside standard tasks
- Custom tasks appear in weekly check-ins (unless `abschaffen` is set in plan)

### Error cases
- Attempt to add task when status is `beide_fertig` or `plan_aktiv` → reject with user-visible error
- Attempt to delete an answered task → reject with user-visible error
- Empty or whitespace-only `bezeichnung` → form validation error

## Non-functional requirements

- No JavaScript required — form submit and page reload is acceptable
- Task addition/deletion must be idempotent from a data perspective (no duplicate task names enforced, that's intentional)

## Data invariants

- `Aufgabe.ist_standard = False`
- `Aufgabe.paar_session` points to the current session (non-null)
- `Aufgabe.erstellt_von` points to the creating user (non-null)
- `Aufgabe.kategorie` points to the fixed "Eigene Aufgaben" Kategorie
