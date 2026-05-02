from django.urls import path

from . import views

app_name = "checkins"

urlpatterns = [
    path("", views.start, name="start"),
    path("auswertung/", views.auswertung, name="auswertung"),
    path("verlauf/", views.verlauf, name="verlauf"),
]
