import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def user(db: None) -> User:
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.mark.django_db
def test_registrieren_get_zeigt_formular(client: Client) -> None:
    response = client.get(reverse("accounts:registrieren"))
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_registrieren_post_erstellt_user_und_leitet_weiter(client: Client) -> None:
    response = client.post(
        reverse("accounts:registrieren"),
        {
            "username": "neueruser",
            "password1": "sehrgeheimesPasswort123!",
            "password2": "sehrgeheimesPasswort123!",
        },
    )
    assert response.status_code == 302
    assert User.objects.filter(username="neueruser").exists()


@pytest.mark.django_db
def test_registrieren_post_ungueltig_zeigt_fehler(client: Client) -> None:
    response = client.post(
        reverse("accounts:registrieren"),
        {"username": "x", "password1": "abc", "password2": "xyz"},
    )
    assert response.status_code == 200
    assert response.context["form"].errors


@pytest.mark.django_db
def test_registrieren_weiterleitung_wenn_eingeloggt(client: Client, user: User) -> None:
    client.force_login(user)
    response = client.get(reverse("accounts:registrieren"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_get_zeigt_formular(client: Client) -> None:
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post_mit_gueltigen_daten(client: Client, user: User) -> None:
    response = client.post(
        reverse("accounts:login"),
        {"username": "testuser", "password": "testpass123"},
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_beendet_session(client: Client, user: User) -> None:
    client.force_login(user)
    response = client.post(reverse("accounts:logout"))
    assert response.status_code == 302
