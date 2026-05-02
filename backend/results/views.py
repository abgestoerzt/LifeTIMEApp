from typing import cast

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from pairs.models import PaarSession
from pairs.services import get_aktive_session

from . import services


@login_required
def auswertung(request: HttpRequest) -> HttpResponse:
    session = get_aktive_session(cast(User, request.user))
    if not session or session.status not in (
        PaarSession.Status.BEIDE_FERTIG,
        PaarSession.Status.PLAN_AKTIV,
    ):
        return redirect("dashboard")

    gesamtverteilung = services.berechne_gesamtverteilung(session)
    kategorien = services.berechne_kategorie_verteilung(session)
    luecken = services.finde_wahrnehmungsluecken(session)

    return render(
        request,
        "results/auswertung.html",
        {
            "session": session,
            "gesamtverteilung": gesamtverteilung,
            "kategorien": kategorien,
            "luecken": luecken,
            "partner_a": session.partner_a,
            "partner_b": session.partner_b,
        },
    )
