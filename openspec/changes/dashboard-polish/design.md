# Dashboard Polish — Design

## Dashboard states

The dashboard renders one of five distinct states based on session status and check-in data:

```
State                Condition                           CTA
─────────────────── ─────────────────────────────────── ──────────────────────────────
no_session          get_aktive_session() is None         "Paar erstellen" or "Beitreten"
waiting_for_partner status=offen                         Show invite code link
survey_in_progress  status=test_laeuft                  "Test fortsetzen" + progress
results_ready       status=beide_fertig                  "Auswertung ansehen"
plan_active         status=plan_aktiv                    Check-in block (see below)
```

## Check-in block (plan_active state)

```
┌─ Wöchentlicher Check-in ──────────────────────────────────┐
│                                                             │
│  [A] Noch nicht eingecheckt diese Woche    [→ Check-in]   │
│  — oder —                                                   │
│  [A] ✓ Eingecheckt                                         │
│  [B] Noch nicht eingecheckt                                │
│  — oder —                                                   │
│  [A] ✓ [B] ✓ Beide fertig → [Auswertung ansehen]          │
│                                                             │
│  Letzter Check-in: vor 9 Tagen                             │
└─────────────────────────────────────────────────────────────┘
```

Sub-states:
1. **eigener_checkin_ausstehend** — current user hasn't checked in this week → big CTA button
2. **partner_ausstehend** — current user done, partner hasn't → "Warte auf [Name]..."
3. **beide_erledigt** — both done → link to check-in Auswertung
4. **kein_checkin_je** — plan_aktiv but no check-ins yet → "Noch keinen Check-in gemacht — jetzt starten"

Plus, regardless of sub-state: show "Letzter Check-in: vor X Tagen" (or "Heute" / "Diese Woche" / "vor X Wochen").

## Service additions

Add to `checkins/services.py`:

```python
def get_checkin_status(paar_session: PaarSession, user: User) -> dict:
    """
    Returns:
    {
      "user_done_this_week": bool,
      "partner_done_this_week": bool,
      "letzter_checkin_tage": int | None,  # days since user's last check-in, None if never
    }
    """
```

## View changes (`config/views.py` — `dashboard`)

```python
from pairs.services import get_aktive_session
from checkins.services import get_checkin_status

def dashboard(request):
    session = get_aktive_session(request.user)
    context = {"session": session}
    if session and session.status == "plan_aktiv":
        context["checkin_status"] = get_checkin_status(session, request.user)
    return render(request, "dashboard.html", context)
```

## Template structure (`templates/dashboard.html`)

Use `{% if %}`/`{% elif %}` blocks on `session.status`:

```
{% if not session %}
  → Pair-creation CTA

{% elif session.status == "offen" %}
  → Invite code reminder + link to /paar/einladung/

{% elif session.status == "test_laeuft" %}
  → Progress bar (answered / total) + "Test fortsetzen" button
  → Show partner status: "Partner:in noch nicht fertig" or checkmark

{% elif session.status == "beide_fertig" %}
  → "Auswertung bereit" card with link

{% elif session.status == "plan_aktiv" %}
  → Check-in block (see above)
{% endif %}
```

## Landing page (`templates/landing.html`)

For logged-out visitors. Minimal but real:

```
┌─────────────────────────────────────────────────────┐
│  LifeTIME                                           │
│  Mental Load sichtbar machen.                       │
│                                                     │
│  Wer plant? Wer macht? Wer trägt die Last?         │
│  Findet es gemeinsam heraus.                        │
│                                                     │
│  [Kostenlos starten]    [Einladung annehmen]        │
└─────────────────────────────────────────────────────┘
```

3-step explainer below: Test → Auswertung → Plan → Check-ins.
No backend changes needed — pure template.
