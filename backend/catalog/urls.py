from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("aufgabe/erstellen/", views.aufgabe_erstellen, name="aufgabe_erstellen"),
    path("aufgabe/<int:pk>/loeschen/", views.aufgabe_loeschen, name="aufgabe_loeschen"),
]
