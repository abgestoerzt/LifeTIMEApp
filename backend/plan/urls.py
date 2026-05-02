from django.urls import path

from . import views

app_name = "plan"

urlpatterns = [
    path("", views.bearbeiten, name="bearbeiten"),
    path("signoff/", views.signoff, name="signoff"),
]
