from typing import cast

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from . import services
from .forms import BeitretenForm, PaarErstellenForm


@login_required
def erstellen(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    if request.method == "POST":
        form = PaarErstellenForm(request.POST)
        if form.is_valid():
            session = services.paar_erstellen(
                user=user,
                setup_kinder=form.cleaned_data["setup_kinder"],
                setup_haustiere=form.cleaned_data["setup_haustiere"],
            )
            return redirect("pairs:einladung", pk=session.pk)
    else:
        form = PaarErstellenForm()
    return render(request, "pairs/erstellen.html", {"form": form})


@login_required
def einladung(request: HttpRequest, pk: int) -> HttpResponse:
    session = services.get_aktive_session(cast(User, request.user))
    if not session or session.pk != pk:
        return redirect("dashboard")
    return render(request, "pairs/einladung.html", {"session": session})


@login_required
def beitreten(request: HttpRequest) -> HttpResponse:
    error = None
    if request.method == "POST":
        form = BeitretenForm(request.POST)
        if form.is_valid():
            session = services.paar_beitreten(
                user=cast(User, request.user),
                invite_code=str(form.cleaned_data["invite_code"]),
            )
            if session:
                return redirect("dashboard")
            error = "Code ungültig, abgelaufen oder bereits verwendet."
    else:
        form = BeitretenForm()
    return render(request, "pairs/beitreten.html", {"form": form, "error": error})
