import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from pairs.models import PaarSession
from pairs.services import paar_erstellen


@pytest.fixture
def user_a(db: None) -> User:
    return User.objects.create_user(username="anna", password="pass")


@pytest.fixture
def user_b(db: None) -> User:
    return User.objects.create_user(username="ben", password="pass")


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.django_db
def test_erstellen_get_erfordert_login(client: Client) -> None:
    response = client.get(reverse("pairs:erstellen"))
    assert response.status_code == 302
    assert "/accounts/login" in response["Location"]


@pytest.mark.django_db
def test_erstellen_get_zeigt_formular(client: Client, user_a: User) -> None:
    client.force_login(user_a)
    response = client.get(reverse("pairs:erstellen"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_erstellen_post_erstellt_session(client: Client, user_a: User) -> None:
    client.force_login(user_a)
    response = client.post(
        reverse("pairs:erstellen"), {"setup_kinder": False, "setup_haustiere": False}
    )
    assert response.status_code == 302
    assert PaarSession.objects.filter(partner_a=user_a).exists()


@pytest.mark.django_db
def test_beitreten_get_zeigt_formular(client: Client, user_b: User) -> None:
    client.force_login(user_b)
    response = client.get(reverse("pairs:beitreten"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_beitreten_post_gueltiger_code(
    client: Client, user_a: User, user_b: User
) -> None:
    session = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    client.force_login(user_b)
    response = client.post(
        reverse("pairs:beitreten"), {"invite_code": str(session.invite_code)}
    )
    assert response.status_code == 302
    session.refresh_from_db()
    assert session.partner_b == user_b


@pytest.mark.django_db
def test_beitreten_post_ungueltiger_code_zeigt_fehler(
    client: Client, user_b: User
) -> None:
    client.force_login(user_b)
    response = client.post(
        reverse("pairs:beitreten"),
        {"invite_code": "00000000-0000-0000-0000-000000000000"},
    )
    assert response.status_code == 200
    assert response.context["error"] is not None
