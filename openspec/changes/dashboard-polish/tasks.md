# Dashboard Polish — Tasks

## Task 1: Add get_checkin_status to checkins/services.py

Add to `backend/checkins/services.py`:

**`get_checkin_status(paar_session: PaarSession, user: User) -> dict`**

Returns:
```python
{
    "user_done_this_week": bool,
    "partner_done_this_week": bool,
    "letzter_checkin_tage": int | None,  # days since user's last completed check-in; None if never
}
```

Implementation:
- `woche = get_montag(date.today())`
- `user_done_this_week = CheckIn.objects.filter(paar_session=paar_session, user=user, woche=woche).exists()`
- Partner is whichever of partner_a / partner_b is not `user`
- `partner_done_this_week` = same query for partner
- `letzter_checkin_tage`: find the most recent `CheckIn.abgeschlossen_at` for this user; compute `(now - abgeschlossen_at).days`; return None if no check-in exists

---

## Task 2: Update config/views.py dashboard view

Update `backend/config/views.py`:

```python
from pairs.services import get_aktive_session
from checkins.services import get_checkin_status

@login_required
def dashboard(request):
    session = get_aktive_session(request.user)
    context: dict = {"session": session}
    if session and session.status == "plan_aktiv":
        context["checkin_status"] = get_checkin_status(session, request.user)
    return render(request, "dashboard.html", context)
```

Also pass `survey_fortschritt` for the `test_laeuft` state:
```python
if session and session.status == "test_laeuft":
    from survey.services import get_fortschritt
    answered, total = get_fortschritt(session, request.user)
    context["survey_beantwortet"] = answered
    context["survey_gesamt"] = total
```

---

## Task 3: Rewrite templates/dashboard.html

Replace the current minimal template with a state-driven layout.

**No session:**
- Card: "Noch kein Paar erstellt"
- Two buttons: "Paar erstellen" → `/paar/erstellen/` and "Einladung annehmen" → `/paar/beitreten/`

**status=offen:**
- Card: "Warte auf Partner:in"
- Show link to `/paar/einladung/<session.pk>/` to share the invite code again
- Explain that the test starts once partner joins

**status=test_laeuft:**
- Card: "Test läuft"
- Progress bar: `survey_beantwortet / survey_gesamt` tasks answered
- Button: "Test fortsetzen" → `/test/`
- Partner status indicator (no data about partner's progress is shown — just "Partner:in noch nicht fertig" or a checkmark icon if they've finished)

**status=beide_fertig:**
- Card: "Auswertung bereit" (highlighted, e.g. purple border)
- Button: "Auswertung ansehen" → `/auswertung/`

**status=plan_aktiv:**
- Check-in block using `checkin_status` context:
  - If `not user_done_this_week`: big button "Check-in starten" → `/checkin/`
  - If `user_done_this_week and not partner_done_this_week`: "Du hast eingecheckt. Warte auf [partner name]..."
  - If `user_done_this_week and partner_done_this_week`: "Beide fertig!" + "Check-in Auswertung" → `/checkin/auswertung/`
- Below the check-in block: `letzter_checkin_tage` display
  - None → "Noch keinen Check-in gemacht"
  - 0 → "Heute eingecheckt"
  - 1 → "Gestern eingecheckt"
  - N → "Letzter Check-in: vor {{ n }} Tagen"
- Also show links to Auswertung, Umverteilungsplan, Verlauf as secondary actions

---

## Task 4: Rewrite templates/landing.html

Replace the current landing page with a proper public homepage.

Sections:
1. **Hero**: App name, tagline "Mental Load sichtbar machen", two CTAs: "Kostenlos starten" (→ /registrieren/) and "Einladung annehmen" (→ /paar/beitreten/)
2. **How it works**: 3-step visual (Test → Auswertung → Plan)
3. **Footer**: minimal (no links needed)

Use the same color variables as the rest of the app (purple/green).

---

## Task 5: Write tests

Create `backend/checkins/tests/test_checkin_status.py`:

Test `get_checkin_status()`:
- `user_done_this_week=False` when no check-in this week
- `user_done_this_week=True` after check-in created for this week
- `partner_done_this_week=True` when partner has check-in this week
- `letzter_checkin_tage=None` when user has never checked in
- `letzter_checkin_tage=0` when check-in was today
- `letzter_checkin_tage=7` when check-in was 7 days ago

Create `backend/config/tests/test_views.py` (or add to existing):

Test `dashboard` view:
- Requires login
- Renders with no session → no session context
- Renders with status=offen → session in context
- Renders with status=plan_aktiv → `checkin_status` in context
- Renders with status=test_laeuft → `survey_beantwortet` and `survey_gesamt` in context
