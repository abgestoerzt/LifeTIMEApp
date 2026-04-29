from django.contrib.auth.models import User
from django.db import models


class CheckIn(models.Model):
    paar_session = models.ForeignKey(
        "pairs.PaarSession", on_delete=models.CASCADE, related_name="checkins"
    )
    woche = models.DateField(help_text="Montag der jeweiligen Woche")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkins")
    abgeschlossen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("paar_session", "woche", "user")]
        ordering = ["-woche"]

    def __str__(self) -> str:
        return f"Check-in {self.user.username} KW {self.woche}"


class CheckInAntwort(models.Model):
    class Status(models.TextChoices):
        JA = "ja", "Ja, hat funktioniert"
        TEILWEISE = "teilweise", "Teilweise"
        NEIN = "nein", "Nein / nicht passiert"

    checkin = models.ForeignKey(
        CheckIn, on_delete=models.CASCADE, related_name="antworten"
    )
    aufgabe = models.ForeignKey(
        "catalog.Aufgabe", on_delete=models.CASCADE, related_name="checkin_antworten"
    )
    status = models.CharField(max_length=10, choices=Status.choices)
    notiz = models.TextField(blank=True)

    class Meta:
        unique_together = [("checkin", "aufgabe")]

    def __str__(self) -> str:
        return f"{self.aufgabe} → {self.status}"
