import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_erstellen() -> None:
    user = User.objects.create_user(username="anna", password="pass123")
    assert user.pk is not None
    assert user.username == "anna"
