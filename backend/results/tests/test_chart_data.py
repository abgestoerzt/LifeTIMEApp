import pytest
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen
from survey.models import AntwortChoices
from survey.services import antwort_speichern, get_aufgaben_fuer_session

from results.services import prepare_gesamt_chart_data, prepare_kategorie_chart_data


@pytest.fixture
def user_a(db: None) -> User:
    return User.objects.create_user(username="anna", password="pass")


@pytest.fixture
def user_b(db: None) -> User:
    return User.objects.create_user(username="ben", password="pass")


@pytest.fixture
def leere_session(user_a: User, user_b: User) -> PaarSession:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    return s


@pytest.fixture
def session_mit_antworten(user_a: User, user_b: User) -> PaarSession:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    for aufgabe in get_aufgaben_fuer_session(s):
        antwort_speichern(s, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
        antwort_speichern(s, user_b, aufgabe, AntwortChoices.PARTNER, AntwortChoices.PARTNER)
    return s


@pytest.mark.django_db
def test_gesamt_chart_management_summiert_zu_100(session_mit_antworten: PaarSession) -> None:
    data = prepare_gesamt_chart_data(session_mit_antworten)
    total = data["management"]["person_a"] + data["management"]["person_b"]
    assert abs(total - 100.0) < 0.2


@pytest.mark.django_db
def test_gesamt_chart_ausfuehrung_summiert_zu_100(session_mit_antworten: PaarSession) -> None:
    data = prepare_gesamt_chart_data(session_mit_antworten)
    total = data["ausfuehrung"]["person_a"] + data["ausfuehrung"]["person_b"]
    assert abs(total - 100.0) < 0.2


@pytest.mark.django_db
def test_gesamt_chart_labels_korrekt(session_mit_antworten: PaarSession, user_a: User, user_b: User) -> None:
    data = prepare_gesamt_chart_data(session_mit_antworten)
    assert data["label_a"] == user_a.username
    assert data["label_b"] == user_b.username


@pytest.mark.django_db
def test_gesamt_chart_extern_zaehlt_nicht(leere_session: PaarSession) -> None:
    aufgabe = get_aufgaben_fuer_session(leere_session).first()
    assert aufgabe is not None
    antwort_speichern(leere_session, leere_session.partner_a, aufgabe, AntwortChoices.EXTERN, AntwortChoices.EXTERN)
    data = prepare_gesamt_chart_data(leere_session)
    assert data["management"]["person_a"] == 0
    assert data["management"]["person_b"] == 0


@pytest.mark.django_db
def test_gesamt_chart_leer_gibt_50_50(leere_session: PaarSession) -> None:
    data = prepare_gesamt_chart_data(leere_session)
    assert data["management"]["person_a"] == 50.0
    assert data["management"]["person_b"] == 50.0
    assert data["ausfuehrung"]["person_a"] == 50.0
    assert data["ausfuehrung"]["person_b"] == 50.0


@pytest.mark.django_db
def test_kategorie_chart_sortiert_nach_imbalance_absteigend(session_mit_antworten: PaarSession) -> None:
    data = prepare_kategorie_chart_data(session_mit_antworten)
    imbalances = [k["imbalance"] for k in data]
    assert imbalances == sorted(imbalances, reverse=True)


@pytest.mark.django_db
def test_kategorie_chart_ohne_antworten_leer(leere_session: PaarSession) -> None:
    data = prepare_kategorie_chart_data(leere_session)
    assert data == []


@pytest.mark.django_db
def test_kategorie_chart_imbalance_ist_abs_differenz(session_mit_antworten: PaarSession) -> None:
    data = prepare_kategorie_chart_data(session_mit_antworten)
    for entry in data:
        expected = round(abs(entry["person_a"] - entry["person_b"]), 1)
        assert entry["imbalance"] == expected
