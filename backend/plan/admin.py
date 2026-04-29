from django.contrib import admin

from .models import Umverteilung


@admin.register(Umverteilung)
class UmverteilungAdmin(admin.ModelAdmin):
    list_display = [
        "aufgabe",
        "paar_session",
        "management_neu",
        "ausfuehrung_neu",
        "signoff_a",
        "signoff_b",
    ]
    list_filter = ["signoff_a", "signoff_b"]
