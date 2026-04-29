from django.contrib.auth.models import User
from django.utils import timezone
from pairs.models import PaarSession
from survey.services import get_aufgaben_fuer_session

from .models import PlanChoices, Umverteilung


def get_oder_erstelle_plan(session: PaarSession) -> list[Umverteilung]:
    """Erstellt fehlende Umverteilungs-Einträge für alle Aufgaben der Session."""
    aufgaben = get_aufgaben_fuer_session(session)
    for aufgabe in aufgaben:
        Umverteilung.objects.get_or_create(
            paar_session=session,
            aufgabe=aufgabe,
            defaults={
                "management_neu": PlanChoices.BEIDE,
                "ausfuehrung_neu": PlanChoices.BEIDE,
            },
        )
    return list(
        Umverteilung.objects.filter(paar_session=session).select_related(
            "aufgabe__kategorie"
        )
    )


def plan_speichern(session: PaarSession, daten: dict[str, str]) -> None:
    """Speichert neue Zuweisungen aus POST-Daten und setzt Signoffs zurück."""
    for umv in Umverteilung.objects.filter(paar_session=session):
        management = daten.get(f"management_{umv.aufgabe_id}")  # type: ignore[attr-defined]
        ausfuehrung = daten.get(f"ausfuehrung_{umv.aufgabe_id}")  # type: ignore[attr-defined]
        changed = False
        if management and management != umv.management_neu:
            umv.management_neu = management
            changed = True
        if ausfuehrung and ausfuehrung != umv.ausfuehrung_neu:
            umv.ausfuehrung_neu = ausfuehrung
            changed = True
        if changed:
            umv.signoff_a = False
            umv.signoff_b = False
            umv.signoff_a_at = None
            umv.signoff_b_at = None
            umv.save()


def signoff_setzen(session: PaarSession, user: User) -> bool:
    """Setzt den Signoff für eine Person. Gibt True zurück wenn beide signiert haben."""
    ist_a = user == session.partner_a
    umverteilungen = Umverteilung.objects.filter(paar_session=session)
    for umv in umverteilungen:
        if ist_a:
            umv.signoff_a = True
            umv.signoff_a_at = timezone.now()
        else:
            umv.signoff_b = True
            umv.signoff_b_at = timezone.now()
        umv.save()

    beide_fertig = all(u.beide_signiert() for u in umverteilungen)
    if beide_fertig:
        session.status = PaarSession.Status.PLAN_AKTIV
        session.save()
    return beide_fertig


def hat_signiert(session: PaarSession, user: User) -> bool:
    umv = Umverteilung.objects.filter(paar_session=session).first()
    if not umv:
        return False
    if user == session.partner_a:
        return umv.signoff_a
    return umv.signoff_b
