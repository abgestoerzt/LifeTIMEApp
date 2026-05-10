from datetime import date

import pytest
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen

from checkins.models import CheckInAntwort
from checkins.services import (
    beide_haben_eingecheckt,
    checkin_speichern,
    checkin_starten,
    get_checkin_aufgaben,
    get_montag,
    get_verlauf,
)
from plan.services import get_oder_erstelle_plan
from survey.models import AntwortChoices
from survey.services import antwort_speichern, get_aufgaben_fuer_session


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
    s.status = PaarSession.Status.PLAN_AKTIV
    s.save()
    return s


@pytest.mark.django_db
def test_get_montag_gibt_montag_zurueck() -> None:
    montag = get_montag(date(2024, 4, 17))  # Mittwoch
    assert montag == date(2024, 4, 15)


@pytest.mark.django_db
def test_checkin_starten_erstellt_eintrag(session: PaarSession, user_a: User) -> None:
    ci = checkin_starten(session, user_a)
    assert ci.pk is not None
    assert ci.user == user_a


@pytest.mark.django_db
def test_beide_haben_eingecheckt_false_wenn_nur_einer(
    session: PaarSession, user_a: User
) -> None:
    woche = get_montag(date.today())
    checkin_starten(session, user_a)
    assert beide_haben_eingecheckt(session, woche) is False


@pytest.mark.django_db
def test_beide_haben_eingecheckt_true_wenn_beide(
    session: PaarSession, user_a: User, user_b: User
) -> None:
    woche = get_montag(date.today())
    checkin_starten(session, user_a)
    checkin_starten(session, user_b)
    assert beide_haben_eingecheckt(session, woche) is True


@pytest.mark.django_db
def test_get_verlauf_leer_ohne_checkins(session: PaarSession) -> None:
    result = get_verlauf(session)
    assert result == []


@pytest.mark.django_db
def test_checkin_starten_idempotent(session: PaarSession, user_a: User) -> None:
    ci1 = checkin_starten(session, user_a)
    ci2 = checkin_starten(session, user_a)
    assert ci1.pk == ci2.pk


@pytest.mark.django_db
def test_get_montag_montag_bleibt_montag() -> None:
    montag = get_montag(date(2024, 4, 15))
    assert montag == date(2024, 4, 15)


@pytest.mark.django_db
def test_get_montag_sonntag_gibt_vorherigen_montag() -> None:
    montag = get_montag(date(2024, 4, 21))  # Sonntag
    assert montag == date(2024, 4, 15)


@pytest.fixture
def session_mit_plan(
    user_a: User, user_b: User, db: None
) -> PaarSession:
    from pairs.services import paar_beitreten, paar_erstellen

    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    s.status = PaarSession.Status.PLAN_AKTIV
    s.save()
    for aufgabe in get_aufgaben_fuer_session(s):
        antwort_speichern(s, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
        antwort_speichern(
            s, user_b, aufgabe, AntwortChoices.PARTNER, AntwortChoices.PARTNER
        )
    get_oder_erstelle_plan(s)
    return s


@pytest.mark.django_db
def test_get_checkin_aufgaben_gibt_umverteilungen_zurueck(
    session_mit_plan: PaarSession,
) -> None:
    aufgaben = get_checkin_aufgaben(session_mit_plan)
    assert len(aufgaben) > 0


@pytest.mark.django_db
def test_get_checkin_aufgaben_exkludiert_abschaffen(
    session_mit_plan: PaarSession,
) -> None:
    from plan.models import Umverteilung

    Umverteilung.objects.filter(paar_session=session_mit_plan).update(
        management_neu="abschaffen"
    )
    aufgaben = get_checkin_aufgaben(session_mit_plan)
    assert len(aufgaben) == 0


@pytest.mark.django_db
def test_checkin_speichern_erstellt_antworten(
    session_mit_plan: PaarSession, user_a: User
) -> None:
    ci = checkin_starten(session_mit_plan, user_a)
    aufgaben = get_checkin_aufgaben(session_mit_plan)
    daten = {f"aufgabe_{u.aufgabe_id}": "ja" for u in aufgaben}
    checkin_speichern(ci, daten)
    assert CheckInAntwort.objects.filter(checkin=ci).count() == len(aufgaben)


@pytest.mark.django_db
def test_checkin_speichern_idempotent(
    session_mit_plan: PaarSession, user_a: User
) -> None:
    ci = checkin_starten(session_mit_plan, user_a)
    aufgaben = get_checkin_aufgaben(session_mit_plan)
    daten = {f"aufgabe_{u.aufgabe_id}": "ja" for u in aufgaben}
    checkin_speichern(ci, daten)
    checkin_speichern(ci, daten)
    assert CheckInAntwort.objects.filter(checkin=ci).count() == len(aufgaben)


@pytest.mark.django_db
def test_get_verlauf_zaehlt_ja_antworten(
    session_mit_plan: PaarSession, user_a: User
) -> None:
    ci = checkin_starten(session_mit_plan, user_a)
    aufgaben = get_checkin_aufgaben(session_mit_plan)
    daten = {f"aufgabe_{u.aufgabe_id}": "ja" for u in aufgaben}
    checkin_speichern(ci, daten)
    verlauf = get_verlauf(session_mit_plan)
    assert len(verlauf) == 1
    assert verlauf[0]["anzahl_ja"] == len(aufgaben)
    assert verlauf[0]["anzahl_gesamt"] == len(aufgaben)
