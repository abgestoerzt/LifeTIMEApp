import pytest
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen
from survey.models import AntwortChoices
from survey.services import antwort_speichern, get_aufgaben_fuer_session

from results.services import (
    berechne_gesamtverteilung,
    berechne_kategorie_verteilung,
    finde_wahrnehmungsluecken,
)


@pytest.fixture
def user_a(db: None) -> User:
    return User.objects.create_user(username="anna", password="pass")


@pytest.fixture
def user_b(db: None) -> User:
    return User.objects.create_user(username="ben", password="pass")


@pytest.fixture
def session_mit_antworten(user_a: User, user_b: User) -> PaarSession:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    for aufgabe in get_aufgaben_fuer_session(s):
        antwort_speichern(s, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
        antwort_speichern(
            s, user_b, aufgabe, AntwortChoices.PARTNER, AntwortChoices.PARTNER
        )
    return s


@pytest.mark.django_db
def test_gesamtverteilung_gibt_zwei_dimensionen_zurueck(
    session_mit_antworten: PaarSession,
) -> None:
    result = berechne_gesamtverteilung(session_mit_antworten)
    assert "management" in result
    assert "ausfuehrung" in result


@pytest.mark.django_db
def test_gesamtverteilung_summiert_zu_100(session_mit_antworten: PaarSession) -> None:
    result = berechne_gesamtverteilung(session_mit_antworten)
    total = result["management"]["partner_a"] + result["management"]["partner_b"]
    assert abs(total - 100.0) < 1


@pytest.mark.django_db
def test_wahrnehmungsluecken_leer_bei_uebereinstimmung(
    session_mit_antworten: PaarSession,
) -> None:
    luecken = finde_wahrnehmungsluecken(session_mit_antworten)
    assert isinstance(luecken, list)


@pytest.mark.django_db
def test_wahrnehmungsluecken_findet_konflikt(user_a: User, user_b: User) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    aufgabe = get_aufgaben_fuer_session(s).first()
    assert aufgabe is not None
    antwort_speichern(s, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
    antwort_speichern(s, user_b, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
    luecken = finde_wahrnehmungsluecken(s)
    assert any(eintrag["markierung"] == "konflikt" for eintrag in luecken)


@pytest.mark.django_db
def test_wahrnehmungsluecken_findet_unsichtbar(user_a: User, user_b: User) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    aufgabe = get_aufgaben_fuer_session(s).first()
    assert aufgabe is not None
    antwort_speichern(s, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH)
    antwort_speichern(s, user_b, aufgabe, AntwortChoices.BEIDE, AntwortChoices.BEIDE)
    luecken = finde_wahrnehmungsluecken(s)
    assert any(eintrag["markierung"] == "unsichtbar" for eintrag in luecken)


@pytest.mark.django_db
def test_wahrnehmungsluecken_findet_luecke(user_a: User, user_b: User) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    aufgabe = get_aufgaben_fuer_session(s).first()
    assert aufgabe is not None
    antwort_speichern(s, user_a, aufgabe, AntwortChoices.PARTNER, AntwortChoices.ICH)
    antwort_speichern(s, user_b, aufgabe, AntwortChoices.PARTNER, AntwortChoices.ICH)
    luecken = finde_wahrnehmungsluecken(s)
    assert any(eintrag["markierung"] == "luecke" for eintrag in luecken)


@pytest.mark.django_db
def test_gesamtverteilung_beide_gibt_50_50(user_a: User, user_b: User) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    aufgabe = get_aufgaben_fuer_session(s).first()
    assert aufgabe is not None
    antwort_speichern(s, user_a, aufgabe, AntwortChoices.BEIDE, AntwortChoices.BEIDE)
    result = berechne_gesamtverteilung(s)
    assert result["management"]["partner_a"] == 50.0
    assert result["management"]["partner_b"] == 50.0


@pytest.mark.django_db
def test_gesamtverteilung_extern_zaehlt_nicht(user_a: User, user_b: User) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    aufgabe = get_aufgaben_fuer_session(s).first()
    assert aufgabe is not None
    antwort_speichern(s, user_a, aufgabe, AntwortChoices.EXTERN, AntwortChoices.EXTERN)
    result = berechne_gesamtverteilung(s)
    assert result["management"]["partner_a"] == 0
    assert result["management"]["partner_b"] == 0


@pytest.mark.django_db
def test_kategorie_verteilung_gibt_liste_zurueck(
    session_mit_antworten: PaarSession,
) -> None:
    result = berechne_kategorie_verteilung(session_mit_antworten)
    assert isinstance(result, list)
    assert len(result) > 0


@pytest.mark.django_db
def test_kategorie_verteilung_enthaelt_erwartete_felder(
    session_mit_antworten: PaarSession,
) -> None:
    result = berechne_kategorie_verteilung(session_mit_antworten)
    eintrag = result[0]
    assert "kategorie" in eintrag
    assert "management_a" in eintrag
    assert "management_b" in eintrag
    assert "ausfuehrung_a" in eintrag
    assert "ausfuehrung_b" in eintrag


@pytest.mark.django_db
def test_kategorie_verteilung_ohne_antworten_leer(user_a: User, user_b: User) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    result = berechne_kategorie_verteilung(s)
    assert result == []
