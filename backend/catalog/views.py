from typing import cast

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from pairs.services import get_aktive_session

from . import services
from .forms import AufgabeErstellenForm
from .models import Aufgabe


@login_required
def aufgabe_erstellen(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponse(status=405)
    user = cast(User, request.user)
    session = get_aktive_session(user)
    if not session:
        return redirect("dashboard")
    form = AufgabeErstellenForm(request.POST)
    if form.is_valid():
        try:
            services.aufgabe_erstellen(
                paar_session=session,
                user=user,
                bezeichnung=form.cleaned_data["bezeichnung"],
            )
        except ValueError:
            pass
    return redirect("survey:start")


@login_required
def aufgabe_loeschen(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponse(status=405)
    user = cast(User, request.user)
    session = get_aktive_session(user)
    aufgabe = get_object_or_404(Aufgabe, pk=pk)
    if not session or aufgabe.paar_session != session:
        return redirect("survey:start")
    try:
        services.aufgabe_loeschen(aufgabe=aufgabe, user=user)
    except (PermissionError, ValueError):
        pass
    return redirect("survey:start")
