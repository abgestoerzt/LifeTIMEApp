from django.contrib import admin

from .models import Antwort, TestAbschluss


@admin.register(Antwort)
class AntwortAdmin(admin.ModelAdmin):
    list_display = ["user", "aufgabe", "management", "ausfuehrung", "beantwortet_at"]
    list_filter = ["management", "ausfuehrung"]


@admin.register(TestAbschluss)
class TestAbschlussAdmin(admin.ModelAdmin):
    list_display = ["user", "paar_session", "abgeschlossen_at"]
