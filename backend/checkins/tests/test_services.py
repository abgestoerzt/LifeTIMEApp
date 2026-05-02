from datetime import date

import pytest
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen

from checkins.services import (
    beide_haben_eingecheckt,
    checkin_starten,
    get_montag,
    get_verlauf,
)


@pytest.fixture
def user_a(db: None) -> User:
    return User.objects.create_user(username="anna", password="pass")


@pytest.fixture
def user_b(db: None) -> User:
    return User.objects.create_user(username="ben", password="pass")


@pytest.fixture
def session(user_a: User, user_b: User) -> PaarSession:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    s.status = PaarSession.Status.PLAN_AKTIV
    s.save()
    return s


@pytest.mark.django_db
def test_get_montag_gibt_montag_zurueck() -> None:
    montag = get_montag(date(2024, 4, 17))  # Mittwoch
    assert montag == date(2024, 4, 15)


@pytest.mark.django_db
def test_checkin_starten_erstellt_eintrag(session: PaarSession, user_a: User) -> None:
    ci = checkin_starten(session, user_a)
    assert ci.pk is not None
    assert ci.user == user_a


@pytest.mark.django_db
def test_beide_haben_eingecheckt_false_wenn_nur_einer(
    session: PaarSession, user_a: User
) -> None:
    woche = get_montag(date.today())
    checkin_starten(session, user_a)
    assert beide_haben_eingecheckt(session, woche) is False


@pytest.mark.django_db
def test_beide_haben_eingecheckt_true_wenn_beide(
    session: PaarSession, user_a: User, user_b: User
) -> None:
    woche = get_montag(date.today())
    checkin_starten(session, user_a)
    checkin_starten(session, user_b)
    assert beide_haben_eingecheckt(session, woche) is True


@pytest.mark.django_db
def test_get_verlauf_leer_ohne_checkins(session: PaarSession) -> None:
    result = get_verlauf(session)
    assert result == []
