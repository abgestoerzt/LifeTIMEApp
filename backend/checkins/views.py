import json
from datetime import date
from typing import cast

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from pairs.models import PaarSession
from pairs.services import get_aktive_session

from . import services
from .models import CheckIn, CheckInAntwort


@login_required
def start(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    session = get_aktive_session(user)
    if not session or session.status != PaarSession.Status.PLAN_AKTIV:
        return redirect("dashboard")

    woche = services.get_montag(date.today())
    bestehendes_checkin = CheckIn.objects.filter(
        paar_session=session, woche=woche, user=user
    ).first()

    if bestehendes_checkin:
        return redirect("checkins:auswertung")

    aufgaben = services.get_checkin_aufgaben(session)

    if request.method == "POST":
        checkin = services.checkin_starten(session, user)
        services.checkin_speichern(checkin, request.POST)
        return redirect("checkins:auswertung")

    return render(
        request,
        "checkins/start.html",
        {
            "aufgaben": aufgaben,
            "woche": woche,
        },
    )


@login_required
def auswertung(request: HttpRequest) -> HttpResponse:
    session = get_aktive_session(cast(User, request.user))
    if not session:
        return redirect("dashboard")

    woche = services.get_montag(date.today())
    checkins = CheckIn.objects.filter(paar_session=session, woche=woche)
    beide_fertig = services.beide_haben_eingecheckt(session, woche)

    antworten_pro_checkin = []
    for ci in checkins:
        antworten = CheckInAntwort.objects.filter(checkin=ci).select_related("aufgabe")
        antworten_pro_checkin.append({"checkin": ci, "antworten": antworten})

    return render(
        request,
        "checkins/auswertung.html",
        {
            "session": session,
            "woche": woche,
            "beide_fertig": beide_fertig,
            "antworten_pro_checkin": antworten_pro_checkin,
            "partner_a": session.partner_a,
            "partner_b": session.partner_b,
        },
    )


@login_required
def verlauf(request: HttpRequest) -> HttpResponse:
    session = get_aktive_session(cast(User, request.user))
    if not session:
        return redirect("dashboard")

    verlauf_daten = services.get_verlauf(session)
    return render(
        request,
        "checkins/verlauf.html",
        {
            "verlauf": verlauf_daten,
            "chart_verlauf_json": json.dumps(services.prepare_verlauf_chart_data(session)),
        },
    )
