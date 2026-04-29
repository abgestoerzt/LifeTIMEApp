import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen


@pytest.fixture
def user_a(db: None) -> User:
    return User.objects.create_user(username="anna", password="pass")


@pytest.fixture
def user_b(db: None) -> User:
    return User.objects.create_user(username="ben", password="pass")


@pytest.mark.django_db
def test_bearbeiten_erfordert_login() -> None:
    response = Client().get(reverse("plan:bearbeiten"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_bearbeiten_zeigt_plan_bei_beide_fertig(user_a: User, user_b: User) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.status = PaarSession.Status.BEIDE_FERTIG
    s.save()
    c = Client()
    c.force_login(user_a)
    response = c.get(reverse("plan:bearbeiten"))
    assert response.status_code == 200
