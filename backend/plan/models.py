from django.db import models


class PlanChoices(models.TextChoices):
    PERSON_A = "person_a", "Partner:in A"
    PERSON_B = "person_b", "Partner:in B"
    BEIDE = "beide", "Wir beide"
    EXTERN = "extern", "Jemand anderes"
    ABSCHAFFEN = "abschaffen", "Aufgabe abschaffen"


class Umverteilung(models.Model):
    paar_session = models.ForeignKey(
        "pairs.PaarSession", on_delete=models.CASCADE, related_name="umverteilungen"
    )
    aufgabe = models.ForeignKey(
        "catalog.Aufgabe", on_delete=models.CASCADE, related_name="umverteilungen"
    )
    management_neu = models.CharField(max_length=20, choices=PlanChoices.choices)
    ausfuehrung_neu = models.CharField(max_length=20, choices=PlanChoices.choices)
    signoff_a = models.BooleanField(default=False)
    signoff_a_at = models.DateTimeField(null=True, blank=True)
    signoff_b = models.BooleanField(default=False)
    signoff_b_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("paar_session", "aufgabe")]

    def __str__(self) -> str:
        return f"Plan: {self.aufgabe} in {self.paar_session}"

    def beide_signiert(self) -> bool:
        return self.signoff_a and self.signoff_b
