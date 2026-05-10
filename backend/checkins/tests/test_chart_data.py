from datetime import date, timedelta

import pytest
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen
from plan.services import get_oder_erstelle_plan
from survey.models import AntwortChoices
from survey.services import antwort_speichern, get_aufgaben_fuer_session

from checkins.models import CheckIn, CheckInAntwort
from checkins.services import (
    checkin_starten,
    get_checkin_aufgaben,
    get_montag,
    prepare_verlauf_chart_data,
)


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
    for aufgabe in get_aufgaben_fuer_session(s):
        antwort_speichern(s, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
        antwort_speichern(s, user_b, aufgabe, AntwortChoices.PARTNER, AntwortChoices.PARTNER)
    get_oder_erstelle_plan(s)
    return s


def _checkin_mit_ja(session: PaarSession, user: User, woche: date) -> None:
    ci, _ = CheckIn.objects.get_or_create(paar_session=session, woche=woche, user=user)
    for u in get_checkin_aufgaben(session):
        CheckInAntwort.objects.update_or_create(
            checkin=ci, aufgabe_id=u.aufgabe_id, defaults={"status": "ja"}
        )


@pytest.mark.django_db
def test_verlauf_chart_leer_ohne_checkins(session: PaarSession) -> None:
    data = prepare_verlauf_chart_data(session)
    assert data["wochen"] == []
    assert data["person_a"] == []
    assert data["person_b"] == []


@pytest.mark.django_db
def test_verlauf_chart_gibt_maximal_8_eintraege(session: PaarSession, user_a: User) -> None:
    montag = get_montag(date.today())
    for i in range(10):
        woche = montag - timedelta(weeks=i)
        _checkin_mit_ja(session, user_a, woche)
    data = prepare_verlauf_chart_data(session)
    assert len(data["wochen"]) <= 8


@pytest.mark.django_db
def test_verlauf_chart_fehlender_partner_gibt_null(session: PaarSession, user_a: User) -> None:
    woche = get_montag(date.today())
    _checkin_mit_ja(session, user_a, woche)
    data = prepare_verlauf_chart_data(session)
    assert len(data["wochen"]) == 1
    assert data["person_a"][0] is not None
    assert data["person_b"][0] is None


@pytest.mark.django_db
def test_verlauf_chart_ja_rate_korrekt(session: PaarSession, user_a: User) -> None:
    woche = get_montag(date.today())
    aufgaben = get_checkin_aufgaben(session)
    ci, _ = CheckIn.objects.get_or_create(paar_session=session, woche=woche, user=user_a)
    total = len(aufgaben)
    for i, u in enumerate(aufgaben):
        status = "ja" if i < total // 2 else "nein"
        CheckInAntwort.objects.update_or_create(
            checkin=ci, aufgabe_id=u.aufgabe_id, defaults={"status": status}
        )
    data = prepare_verlauf_chart_data(session)
    expected = round((total // 2) / total * 100, 1)
    assert data["person_a"][0] == expected


@pytest.mark.django_db
def test_verlauf_chart_enthaelt_labels(session: PaarSession, user_a: User, user_b: User) -> None:
    data = prepare_verlauf_chart_data(session)
    assert data["label_a"] == user_a.username
    assert data["label_b"] == user_b.username
