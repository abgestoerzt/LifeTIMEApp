from django.contrib import admin

from .models import CheckIn, CheckInAntwort


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ["user", "paar_session", "woche", "abgeschlossen_at"]
    list_filter = ["woche"]


@admin.register(CheckInAntwort)
class CheckInAntwortAdmin(admin.ModelAdmin):
    list_display = ["checkin", "aufgabe", "status"]
    list_filter = ["status"]
