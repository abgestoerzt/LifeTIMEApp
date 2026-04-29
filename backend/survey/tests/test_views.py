import pytest
from catalog.models import Aufgabe, Kategorie
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen

from survey.models import AntwortChoices


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


@pytest.fixture
def client_a(user_a: User) -> Client:
    c = Client()
    c.force_login(user_a)
    return c


@pytest.mark.django_db
def test_start_erfordert_login() -> None:
    response = Client().get(reverse("survey:start"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_start_zeigt_kategorien(client_a: Client, session: PaarSession) -> None:
    response = client_a.get(reverse("survey:start"))
    assert response.status_code == 200
    assert "kategorien" in response.context


@pytest.mark.django_db
def test_start_leitet_weiter_ohne_session(user_a: User) -> None:
    c = Client()
    c.force_login(user_a)
    response = c.get(reverse("survey:start"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_kategorie_speichert_antworten(client_a: Client, session: PaarSession) -> None:
    kat = Kategorie.objects.first()
    assert kat is not None
    aufgaben = list(Aufgabe.objects.filter(kategorie=kat, ist_standard=True))
    data = {}
    for a in aufgaben:
        data[f"management_{a.pk}"] = AntwortChoices.ICH
        data[f"ausfuehrung_{a.pk}"] = AntwortChoices.BEIDE
    response = client_a.post(reverse("survey:kategorie", args=[kat.pk]), data)
    assert response.status_code == 302

    from django.contrib.auth.models import User

    from survey.models import Antwort

    user = User.objects.get(username="anna")
    assert Antwort.objects.filter(paar_session=session, user=user).count() == len(
        aufgaben
    )


@pytest.mark.django_db
def test_abschliessen_ohne_alle_antworten_bleibt_auf_dashboard(
    client_a: Client, session: PaarSession
) -> None:
    response = client_a.post(reverse("survey:abschliessen"))
    assert response.status_code == 302
    session.refresh_from_db()
    assert session.status != PaarSession.Status.BEIDE_FERTIG
