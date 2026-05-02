import pytest
from catalog.models import Aufgabe
from django.contrib.auth.models import User
from pairs.models import PaarSession
from pairs.services import paar_beitreten, paar_erstellen

from survey.models import AntwortChoices
from survey.services import (
    antwort_speichern,
    get_aufgaben_fuer_session,
    get_fortschritt,
    ist_fertig,
    survey_abschliessen,
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
    return s


@pytest.fixture
def erste_aufgabe(db: None) -> Aufgabe:
    return Aufgabe.objects.filter(ist_standard=True).first()  # type: ignore[return-value]


@pytest.mark.django_db
def test_get_aufgaben_exkludiert_kinder_wenn_nicht_gesetzt(
    user_a: User, user_b: User
) -> None:
    s = paar_erstellen(user_a, setup_kinder=False, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    aufgaben = get_aufgaben_fuer_session(s)
    namen = [a.kategorie.name for a in aufgaben if a.kategorie]
    assert "Kinderbetreuung" not in namen


@pytest.mark.django_db
def test_get_aufgaben_inkludiert_kinder_wenn_gesetzt(
    user_a: User, user_b: User
) -> None:
    s = paar_erstellen(user_a, setup_kinder=True, setup_haustiere=False)
    paar_beitreten(user_b, str(s.invite_code))
    s.refresh_from_db()
    aufgaben = get_aufgaben_fuer_session(s)
    namen = [a.kategorie.name for a in aufgaben if a.kategorie]
    assert "Kinderbetreuung" in namen


@pytest.mark.django_db
def test_antwort_speichern_erstellt_eintrag(
    session: PaarSession, user_a: User, erste_aufgabe: Aufgabe
) -> None:
    antwort = antwort_speichern(
        session, user_a, erste_aufgabe, AntwortChoices.ICH, AntwortChoices.PARTNER
    )
    assert antwort.pk is not None
    assert antwort.management == AntwortChoices.ICH
    assert antwort.ausfuehrung == AntwortChoices.PARTNER


@pytest.mark.django_db
def test_antwort_speichern_aktualisiert_bestehende(
    session: PaarSession, user_a: User, erste_aufgabe: Aufgabe
) -> None:
    antwort_speichern(
        session, user_a, erste_aufgabe, AntwortChoices.ICH, AntwortChoices.BEIDE
    )
    antwort = antwort_speichern(
        session, user_a, erste_aufgabe, AntwortChoices.PARTNER, AntwortChoices.BEIDE
    )
    from survey.models import Antwort

    assert (
        Antwort.objects.filter(
            paar_session=session, user=user_a, aufgabe=erste_aufgabe
        ).count()
        == 1
    )
    assert antwort.management == AntwortChoices.PARTNER


@pytest.mark.django_db
def test_get_fortschritt_zaehlt_korrekt(
    session: PaarSession, user_a: User, erste_aufgabe: Aufgabe
) -> None:
    fp = get_fortschritt(session, user_a)
    assert fp["beantwortet"] == 0
    antwort_speichern(
        session, user_a, erste_aufgabe, AntwortChoices.ICH, AntwortChoices.ICH
    )
    fp = get_fortschritt(session, user_a)
    assert fp["beantwortet"] == 1


@pytest.mark.django_db
def test_ist_fertig_false_wenn_nicht_alle_beantwortet(
    session: PaarSession, user_a: User
) -> None:
    assert ist_fertig(session, user_a) is False


@pytest.mark.django_db
def test_survey_abschliessen_schlaegt_fehl_wenn_nicht_fertig(
    session: PaarSession, user_a: User
) -> None:
    result = survey_abschliessen(session, user_a)
    assert result is False


@pytest.mark.django_db
def test_survey_abschliessen_setzt_beide_fertig_status(
    session: PaarSession, user_a: User, user_b: User
) -> None:
    aufgaben = list(get_aufgaben_fuer_session(session))
    for aufgabe in aufgaben:
        antwort_speichern(
            session, user_a, aufgabe, AntwortChoices.ICH, AntwortChoices.ICH
        )
        antwort_speichern(
            session, user_b, aufgabe, AntwortChoices.PARTNER, AntwortChoices.PARTNER
        )
    survey_abschliessen(session, user_a)
    survey_abschliessen(session, user_b)
    session.refresh_from_db()
    assert session.status == PaarSession.Status.BEIDE_FERTIG
