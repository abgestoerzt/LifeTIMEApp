from django.contrib import admin

from .models import Aufgabe, Kategorie


@admin.register(Kategorie)
class KategorieAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "ist_optional", "reihenfolge"]
    ordering = ["reihenfolge"]


@admin.register(Aufgabe)
class AufgabeAdmin(admin.ModelAdmin):
    list_display = ["bezeichnung", "kategorie", "ist_standard", "reihenfolge"]
    list_filter = ["kategorie", "ist_standard"]
    ordering = ["kategorie__reihenfolge", "reihenfolge"]
