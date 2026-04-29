from django.contrib.auth.models import User
from django.db import models


class AntwortChoices(models.TextChoices):
    ICH = "ich", "Ich"
    PARTNER = "partner", "Mein:e Partner:in"
    BEIDE = "beide", "Wir beide"
    EXTERN = "extern", "Jemand anderes"
    NICHT_ZUTREFFEND = "nicht_zutreffend", "Trifft nicht zu"


class Antwort(models.Model):
    paar_session = models.ForeignKey(
        "pairs.PaarSession", on_delete=models.CASCADE, related_name="antworten"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="antworten")
    aufgabe = models.ForeignKey(
        "catalog.Aufgabe", on_delete=models.CASCADE, related_name="antworten"
    )
    management = models.CharField(max_length=20, choices=AntwortChoices.choices)
    ausfuehrung = models.CharField(max_length=20, choices=AntwortChoices.choices)
    beantwortet_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("paar_session", "user", "aufgabe")]

    def __str__(self) -> str:
        return f"{self.user.username} – {self.aufgabe}"


class TestAbschluss(models.Model):
    paar_session = models.ForeignKey(
        "pairs.PaarSession", on_delete=models.CASCADE, related_name="abschluesse"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="test_abschluesse"
    )
    abgeschlossen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("paar_session", "user")]

    def __str__(self) -> str:
        return f"{self.user.username} fertig in {self.paar_session}"
