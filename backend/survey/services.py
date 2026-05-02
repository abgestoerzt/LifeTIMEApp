from catalog.models import Aufgabe, Kategorie
from django.contrib.auth.models import User
from django.db.models import QuerySet
from pairs.models import PaarSession

from .models import Antwort, TestAbschluss


def get_kategorien_fuer_session(session: PaarSession) -> QuerySet[Kategorie]:
    qs = Kategorie.objects.prefetch_related("aufgaben")
    if not session.setup_kinder:
        qs = qs.exclude(name="Kinderbetreuung")
    if not session.setup_haustiere:
        qs = qs.exclude(name="Haustiere")
    return qs


def get_aufgaben_fuer_session(session: PaarSession) -> QuerySet[Aufgabe]:
    kategorien = get_kategorien_fuer_session(session)
    standard = Aufgabe.objects.filter(kategorie__in=kategorien, ist_standard=True)
    eigene = Aufgabe.objects.filter(paar_session=session, ist_standard=False)
    return (
        (standard | eigene).distinct().order_by("kategorie__reihenfolge", "reihenfolge")
    )


def antwort_speichern(
    session: PaarSession,
    user: User,
    aufgabe: Aufgabe,
    management: str,
    ausfuehrung: str,
) -> Antwort:
    antwort, _ = Antwort.objects.update_or_create(
        paar_session=session,
        user=user,
        aufgabe=aufgabe,
        defaults={"management": management, "ausfuehrung": ausfuehrung},
    )
    return antwort


def get_fortschritt(session: PaarSession, user: User) -> dict[str, int]:
    gesamt = get_aufgaben_fuer_session(session).count()
    beantwortet = Antwort.objects.filter(paar_session=session, user=user).count()
    return {"gesamt": gesamt, "beantwortet": beantwortet}


def ist_fertig(session: PaarSession, user: User) -> bool:
    fortschritt = get_fortschritt(session, user)
    return (
        fortschritt["beantwortet"] >= fortschritt["gesamt"]
        and fortschritt["gesamt"] > 0
    )


def survey_abschliessen(session: PaarSession, user: User) -> bool:
    if not ist_fertig(session, user):
        return False
    TestAbschluss.objects.get_or_create(paar_session=session, user=user)
    if session.beide_fertig():
        session.status = PaarSession.Status.BEIDE_FERTIG
        session.save()
    return True
