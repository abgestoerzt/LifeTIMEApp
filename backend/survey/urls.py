from django.urls import path

from . import views

app_name = "survey"

urlpatterns = [
    path("", views.start, name="start"),
    path("kategorie/<int:kategorie_id>/", views.kategorie, name="kategorie"),
    path("abschliessen/", views.abschliessen, name="abschliessen"),
]
