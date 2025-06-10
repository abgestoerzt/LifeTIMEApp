from django.urls import path
from . import views

urlpatterns = [
    path("", views.calender_list_view, name="entries_list"),
]