from typing import cast

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import include, path


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    from pairs.services import get_aktive_session

    session = get_aktive_session(cast(User, request.user))
    return render(request, "dashboard.html", {"paar_session": session})


def landing(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        from django.shortcuts import redirect

        return redirect("dashboard")
    return render(request, "landing.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("dashboard/", dashboard, name="dashboard"),
    path("accounts/", include("accounts.urls")),
    path("paar/", include("pairs.urls")),
    path("test/", include("survey.urls")),
    path("auswertung/", include("results.urls")),
    path("umverteilung/", include("plan.urls")),
    path("checkin/", include("checkins.urls")),
    path("katalog/", include("catalog.urls")),
]
