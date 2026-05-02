from django.urls import path

from . import views

app_name = "pairs"

urlpatterns = [
    path("erstellen/", views.erstellen, name="erstellen"),
    path("einladung/<int:pk>/", views.einladung, name="einladung"),
    path("beitreten/", views.beitreten, name="beitreten"),
]
