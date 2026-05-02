import uuid

from django.contrib.auth.models import User
from django.db import models


class PaarSession(models.Model):
    class Status(models.TextChoices):
        OFFEN = "offen", "Offen"
        TEST_LAEUFT = "test_laeuft", "Test läuft"
        BEIDE_FERTIG = "beide_fertig", "Beide fertig"
        PLAN_AKTIV = "plan_aktiv", "Plan aktiv"

    partner_a = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sessions_als_a"
    )
    partner_b = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sessions_als_b",
    )
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    invite_expires_at = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OFFEN
    )
    setup_kinder = models.BooleanField(default=False)
    setup_haustiere = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        b = self.partner_b.username if self.partner_b else "?"
        return f"{self.partner_a.username} & {b}"

    def beide_fertig(self) -> bool:
        from survey.models import TestAbschluss

        if not self.partner_b:
            return False
        a_fertig = TestAbschluss.objects.filter(
            paar_session=self, user=self.partner_a
        ).exists()
        b_fertig = TestAbschluss.objects.filter(
            paar_session=self, user=self.partner_b
        ).exists()
        return a_fertig and b_fertig
