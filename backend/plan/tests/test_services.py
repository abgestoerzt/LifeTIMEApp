import pytest
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen

from plan.services import get_oder_erstelle_plan, hat_signiert, signoff_setzen


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
    s.status = PaarSession.Status.BEIDE_FERTIG
    s.save()
    return s


@pytest.mark.django_db
def test_get_oder_erstelle_plan_erstellt_eintraege(session: PaarSession) -> None:
    umverteilungen = get_oder_erstelle_plan(session)
    assert len(umverteilungen) > 0


@pytest.mark.django_db
def test_hat_signiert_false_nach_erstellung(session: PaarSession, user_a: User) -> None:
    get_oder_erstelle_plan(session)
    assert hat_signiert(session, user_a) is False


@pytest.mark.django_db
def test_signoff_setzt_plan_aktiv_wenn_beide_signiert(
    session: PaarSession, user_a: User, user_b: User
) -> None:
    get_oder_erstelle_plan(session)
    signoff_setzen(session, user_a)
    signoff_setzen(session, user_b)
    session.refresh_from_db()
    assert session.status == PaarSession.Status.PLAN_AKTIV


@pytest.mark.django_db
def test_signoff_setzt_hat_signiert_true(session: PaarSession, user_a: User) -> None:
    get_oder_erstelle_plan(session)
    signoff_setzen(session, user_a)
    assert hat_signiert(session, user_a) is True
