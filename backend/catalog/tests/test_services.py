import pytest
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen
from survey.models import AntwortChoices
from survey.services import antwort_speichern

from catalog.services import aufgabe_erstellen, aufgabe_loeschen


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
    return s


@pytest.mark.django_db
def test_aufgabe_erstellen_legt_aufgabe_an(session: PaarSession, user_a: User) -> None:
    aufgabe = aufgabe_erstellen(session, user_a, "Gemüsegarten pflegen")
    assert aufgabe.pk is not None
    assert aufgabe.bezeichnung == "Gemüsegarten pflegen"
    assert aufgabe.ist_standard is False
    assert aufgabe.paar_session == session
    assert aufgabe.erstellt_von == user_a


@pytest.mark.django_db
def test_aufgabe_erstellen_strippt_leerzeichen(
    session: PaarSession, user_a: User
) -> None:
    aufgabe = aufgabe_erstellen(session, user_a, "  Aufgabe mit Leerzeichen  ")
    assert aufgabe.bezeichnung == "Aufgabe mit Leerzeichen"


@pytest.mark.django_db
def test_aufgabe_erstellen_schlaegt_fehl_wenn_beide_fertig(
    session: PaarSession, user_a: User
) -> None:
    session.status = PaarSession.Status.BEIDE_FERTIG
    session.save()
    with pytest.raises(ValueError):
        aufgabe_erstellen(session, user_a, "Zu spät")


@pytest.mark.django_db
def test_aufgabe_erstellen_schlaegt_fehl_wenn_plan_aktiv(
    session: PaarSession, user_a: User
) -> None:
    session.status = PaarSession.Status.PLAN_AKTIV
    session.save()
    with pytest.raises(ValueError):
        aufgabe_erstellen(session, user_a, "Zu spät")


@pytest.mark.django_db
def test_aufgabe_loeschen_loescht_aufgabe(
    session: PaarSession, user_a: User
) -> None:
    from catalog.models import Aufgabe

    aufgabe = aufgabe_erstellen(session, user_a, "Löschen Test")
    pk = aufgabe.pk
    aufgabe_loeschen(aufgabe, user_a)
    assert not Aufgabe.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_aufgabe_loeschen_schlaegt_fehl_wenn_nicht_ersteller(
    session: PaarSession, user_a: User, user_b: User
) -> None:
    aufgabe = aufgabe_erstellen(session, user_a, "Nur meine")
    with pytest.raises(PermissionError):
        aufgabe_loeschen(aufgabe, user_b)


@pytest.mark.django_db
def test_aufgabe_loeschen_schlaegt_fehl_wenn_beantwortet(
    session: PaarSession, user_a: User
) -> None:
    aufgabe = aufgabe_erstellen(session, user_a, "Schon beantwortet")
    antwort_speichern(session, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
    with pytest.raises(ValueError):
        aufgabe_loeschen(aufgabe, user_a)
