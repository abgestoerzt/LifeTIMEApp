from django.contrib.auth.models import User
from django.db import models


class Kategorie(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default="📋")
    ist_optional = models.BooleanField(default=False)
    reihenfolge = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["reihenfolge"]

    def __str__(self) -> str:
        return self.name


class Aufgabe(models.Model):
    kategorie = models.ForeignKey(
        Kategorie,
        on_delete=models.CASCADE,
        related_name="aufgaben",
        null=True,
        blank=True,
    )
    bezeichnung = models.CharField(max_length=200)
    ist_standard = models.BooleanField(default=True)
    paar_session = models.ForeignKey(
        "pairs.PaarSession",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="eigene_aufgaben",
    )
    erstellt_von = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reihenfolge = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["reihenfolge", "id"]

    def __str__(self) -> str:
        return self.bezeichnung
