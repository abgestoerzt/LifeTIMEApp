from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from .models import PaarSession


def paar_erstellen(
    user: User, setup_kinder: bool, setup_haustiere: bool
) -> PaarSession:
    return PaarSession.objects.create(
        partner_a=user,
        invite_expires_at=timezone.now() + timedelta(days=7),
        setup_kinder=setup_kinder,
        setup_haustiere=setup_haustiere,
        status=PaarSession.Status.OFFEN,
    )


def paar_beitreten(user: User, invite_code: str) -> PaarSession | None:
    try:
        session = PaarSession.objects.get(invite_code=invite_code)
    except PaarSession.DoesNotExist:
        return None
    if session.partner_b is not None:
        return None
    if session.partner_a == user:
        return None
    if session.invite_expires_at < timezone.now():
        return None
    session.partner_b = user
    session.status = PaarSession.Status.TEST_LAEUFT
    session.save()
    return session


def get_aktive_session(user: User) -> PaarSession | None:
    session = (
        PaarSession.objects.filter(partner_a=user).order_by("-created_at").first()
        or PaarSession.objects.filter(partner_b=user).order_by("-created_at").first()
    )
    return session
