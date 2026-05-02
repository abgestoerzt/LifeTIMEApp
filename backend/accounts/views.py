from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import RegistrierungForm


def registrieren(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegistrierungForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegistrierungForm()
    return render(request, "accounts/registrieren.html", {"form": form})
