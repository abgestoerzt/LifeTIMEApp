import pytest
from django.contrib.auth.models import User

from pairs.services import paar_erstellen


@pytest.fixture
def user_a(db: None) -> User:
    return User.objects.create_user(username="anna", password="pass")


@pytest.fixture
def user_b(db: None) -> User:
    return User.objects.create_user(username="ben", password="pass")


@pytest.mark.django_db
def test_paarsession_str(user_a: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    assert "anna" in str(session)


@pytest.mark.django_db
def test_beide_fertig_false_wenn_kein_partner_b(user_a: User) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    assert session.beide_fertig() is False


@pytest.mark.django_db
def test_beide_fertig_false_wenn_nur_einer_fertig(user_a: User, user_b: User) -> None:
    from survey.models import TestAbschluss

    from pairs.services import paar_beitreten

    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(session.invite_code))
    session.refresh_from_db()
    TestAbschluss.objects.create(paar_session=session, user=user_a)
    assert session.beide_fertig() is False


@pytest.mark.django_db
def test_beide_fertig_true_wenn_beide_abgeschlossen(user_a: User, user_b: User) -> None:
    from survey.models import TestAbschluss

    from pairs.services import paar_beitreten

    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(session.invite_code))
    session.refresh_from_db()
    TestAbschluss.objects.create(paar_session=session, user=user_a)
    TestAbschluss.objects.create(paar_session=session, user=user_b)
    assert session.beide_fertig() is True
