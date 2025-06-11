from django.urls import path
from . import views

urlpatterns = [
    path("", views.calender_list_view, name="entries_list"),
    path('api/calendar/', views.calendar_events, name='calendar_events'),  # returns JSON
]