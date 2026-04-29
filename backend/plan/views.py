from typing import cast

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from pairs.models import PaarSession
from pairs.services import get_aktive_session

from . import services
from .models import PlanChoices


@login_required
def bearbeiten(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    session = get_aktive_session(user)
    if not session or session.status not in (
        PaarSession.Status.BEIDE_FERTIG,
        PaarSession.Status.PLAN_AKTIV,
    ):
        return redirect("dashboard")

    if request.method == "POST":
        services.plan_speichern(session, request.POST)
        return redirect("plan:bearbeiten")

    umverteilungen = services.get_oder_erstelle_plan(session)
    hat_signiert = services.hat_signiert(session, user)

    return render(
        request,
        "plan/bearbeiten.html",
        {
            "session": session,
            "umverteilungen": umverteilungen,
            "choices": PlanChoices.choices,
            "hat_signiert": hat_signiert,
            "partner_a": session.partner_a,
            "partner_b": session.partner_b,
        },
    )


@login_required
def signoff(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect("plan:bearbeiten")
    user = cast(User, request.user)
    session = get_aktive_session(user)
    if not session:
        return redirect("dashboard")
    services.signoff_setzen(session, user)
    return redirect("plan:bearbeiten")
