from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from pairs.models import PaarSession
from pairs.services import get_aktive_session, paar_beitreten, paar_erstellen


@pytest.fixture
def user_a(db: None) -> User:
    return User.objects.create_user(username="anna", password="pass")


@pytest.fixture
def user_b(db: None) -> User:
    return User.objects.create_user(username="ben", password="pass")


@pytest.mark.django_db
def test_paar_erstellen_legt_session_an(user_a: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    assert session.pk is not None
    assert session.partner_a == user_a
    assert session.partner_b is None
    assert session.status == PaarSession.Status.OFFEN


@pytest.mark.django_db
def test_paar_erstellen_mit_kinder_und_haustiere(user_a: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=True, setup_haustiere=True)
    assert session.setup_kinder is True
    assert session.setup_haustiere is True


@pytest.mark.django_db
def test_paar_beitreten_verbindet_partner(user_a: User, user_b: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    result = paar_beitreten(user_b, str(session.invite_code))
    assert result is not None
    assert result.partner_b == user_b
    assert result.status == PaarSession.Status.TEST_LAEUFT


@pytest.mark.django_db
def test_paar_beitreten_ungültiger_code(user_b: User) -> None:
    result = paar_beitreten(user_b, "00000000-0000-0000-0000-000000000000")
    assert result is None


@pytest.mark.django_db
def test_paar_beitreten_eigener_code_schlaegt_fehl(user_a: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    result = paar_beitreten(user_a, str(session.invite_code))
    assert result is None


@pytest.mark.django_db
def test_paar_beitreten_abgelaufener_code(user_a: User, user_b: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    session.invite_expires_at = timezone.now() - timedelta(days=1)
    session.save()
    result = paar_beitreten(user_b, str(session.invite_code))
    assert result is None


@pytest.mark.django_db
def test_get_aktive_session_als_partner_a(user_a: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    result = get_aktive_session(user_a)
    assert result == session


@pytest.mark.django_db
def test_get_aktive_session_als_partner_b(user_a: User, user_b: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(session.invite_code))
    result = get_aktive_session(user_b)
    assert result is not None
    assert result.partner_b == user_b


@pytest.mark.django_db
def test_get_aktive_session_ohne_session(user_a: User) -> None:
    result = get_aktive_session(user_a)
    assert result is None
