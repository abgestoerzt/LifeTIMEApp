from typing import cast

from catalog.forms import AufgabeErstellenForm
from catalog.models import Aufgabe, Kategorie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from pairs.services import get_aktive_session

from . import services
from .models import Antwort, AntwortChoices


@login_required
def start(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    session = get_aktive_session(user)
    if not session or session.partner_b is None:
        return redirect("dashboard")

    if _get_abschluss(session, user):
        return redirect("results:auswertung")

    kategorien = services.get_kategorien_fuer_session(session)
    fortschritt = services.get_fortschritt(session, user)
    beantwortet_ids = set(
        Antwort.objects.filter(paar_session=session, user=user).values_list(
            "aufgabe_id",
            flat=True,  # type: ignore[arg-type]
        )
    )

    kategorien_mit_fortschritt = []
    for kat in kategorien:
        aufgaben = list(Aufgabe.objects.filter(kategorie=kat, ist_standard=True))
        if not session.setup_kinder and kat.name == "Kinderbetreuung":
            continue
        if not session.setup_haustiere and kat.name == "Haustiere":
            continue
        anz_gesamt = len(aufgaben)
        anz_fertig = sum(1 for a in aufgaben if a.pk in beantwortet_ids)
        kategorien_mit_fortschritt.append(
            {
                "kategorie": kat,
                "anz_gesamt": anz_gesamt,
                "anz_fertig": anz_fertig,
                "komplett": anz_fertig == anz_gesamt,
            }
        )

    kann_abschliessen = services.ist_fertig(session, user)
    eigene_aufgaben = Aufgabe.objects.filter(
        paar_session=session, ist_standard=False
    ).select_related("erstellt_von")
    return render(
        request,
        "survey/start.html",
        {
            "session": session,
            "kategorien": kategorien_mit_fortschritt,
            "fortschritt": fortschritt,
            "kann_abschliessen": kann_abschliessen,
            "eigene_aufgaben": eigene_aufgaben,
            "beantwortet_ids": beantwortet_ids,
            "erstellen_form": AufgabeErstellenForm(),
        },
    )


@login_required
def kategorie(request: HttpRequest, kategorie_id: int) -> HttpResponse:
    user = cast(User, request.user)
    session = get_aktive_session(user)
    if not session or session.partner_b is None:
        return redirect("dashboard")

    kat = get_object_or_404(Kategorie, pk=kategorie_id)
    aufgaben = Aufgabe.objects.filter(kategorie=kat, ist_standard=True).order_by(
        "reihenfolge"
    )
    choices = AntwortChoices.choices

    if request.method == "POST":
        for aufgabe in aufgaben:
            management = request.POST.get(f"management_{aufgabe.pk}")
            ausfuehrung = request.POST.get(f"ausfuehrung_{aufgabe.pk}")
            if management and ausfuehrung:
                services.antwort_speichern(
                    session, user, aufgabe, management, ausfuehrung
                )
        return redirect("survey:start")

    bestehende = {
        a.aufgabe_id: a  # type: ignore[attr-defined]
        for a in Antwort.objects.filter(
            paar_session=session, user=user, aufgabe__in=aufgaben
        )
    }
    aufgaben_mit_antwort = [
        {"aufgabe": a, "antwort": bestehende.get(a.pk)} for a in aufgaben
    ]
    return render(
        request,
        "survey/kategorie.html",
        {
            "kategorie": kat,
            "aufgaben": aufgaben_mit_antwort,
            "choices": choices,
        },
    )


@login_required
def abschliessen(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect("survey:start")
    user = cast(User, request.user)
    session = get_aktive_session(user)
    if not session:
        return redirect("dashboard")
    services.survey_abschliessen(session, user)
    return redirect("dashboard")


def _get_abschluss(session: object, user: object) -> bool:
    from .models import TestAbschluss as TA

    return TA.objects.filter(paar_session=session, user=user).exists()  # type: ignore[arg-type]
