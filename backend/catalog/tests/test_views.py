import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen

from catalog.models import Aufgabe
from catalog.services import aufgabe_erstellen


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
def test_aufgabe_erstellen_erfordert_login(client: Client) -> None:
    response = client.post(reverse("catalog:aufgabe_erstellen"), {"bezeichnung": "Test"})
    assert response.status_code == 302
    assert "/login/" in response["Location"]


@pytest.mark.django_db
def test_aufgabe_erstellen_erstellt_aufgabe(
    client: Client, user_a: User, session: PaarSession
) -> None:
    client.force_login(user_a)
    response = client.post(
        reverse("catalog:aufgabe_erstellen"), {"bezeichnung": "Neue Aufgabe"}
    )
    assert response.status_code == 302
    assert Aufgabe.objects.filter(paar_session=session, bezeichnung="Neue Aufgabe").exists()


@pytest.mark.django_db
def test_aufgabe_erstellen_schlaegt_fehl_bei_falschem_status(
    client: Client, user_a: User, session: PaarSession
) -> None:
    session.status = PaarSession.Status.BEIDE_FERTIG
    session.save()
    client.force_login(user_a)
    client.post(reverse("catalog:aufgabe_erstellen"), {"bezeichnung": "Zu spät"})
    assert not Aufgabe.objects.filter(paar_session=session, bezeichnung="Zu spät").exists()


@pytest.mark.django_db
def test_aufgabe_loeschen_erfordert_login(
    client: Client, user_a: User, session: PaarSession
) -> None:
    aufgabe = aufgabe_erstellen(session, user_a, "Löschen")
    response = client.post(reverse("catalog:aufgabe_loeschen", args=[aufgabe.pk]))
    assert response.status_code == 302
    assert "/login/" in response["Location"]
    assert Aufgabe.objects.filter(pk=aufgabe.pk).exists()


@pytest.mark.django_db
def test_aufgabe_loeschen_loescht_eigene_aufgabe(
    client: Client, user_a: User, session: PaarSession
) -> None:
    aufgabe = aufgabe_erstellen(session, user_a, "Zu löschen")
    client.force_login(user_a)
    response = client.post(reverse("catalog:aufgabe_loeschen", args=[aufgabe.pk]))
    assert response.status_code == 302
    assert not Aufgabe.objects.filter(pk=aufgabe.pk).exists()


@pytest.mark.django_db
def test_aufgabe_loeschen_verhindert_fremde_aufgabe(
    client: Client, user_a: User, user_b: User, session: PaarSession
) -> None:
    aufgabe = aufgabe_erstellen(session, user_a, "Gehört A")
    client.force_login(user_b)
    client.post(reverse("catalog:aufgabe_loeschen", args=[aufgabe.pk]))
    assert Aufgabe.objects.filter(pk=aufgabe.pk).exists()
