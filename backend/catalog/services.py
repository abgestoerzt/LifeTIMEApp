from django.contrib.auth.models import User

from pairs.models import PaarSession
from survey.models import Antwort

from .models import Aufgabe, Kategorie


def get_eigene_kategorie() -> Kategorie:
    return Kategorie.objects.get(name="Eigene Aufgaben")


def aufgabe_erstellen(
    paar_session: PaarSession, user: User, bezeichnung: str
) -> Aufgabe:
    if paar_session.status not in (
        PaarSession.Status.OFFEN,
        PaarSession.Status.TEST_LAEUFT,
    ):
        raise ValueError("Aufgaben können nur hinzugefügt werden, solange der Test läuft.")
    return Aufgabe.objects.create(
        kategorie=get_eigene_kategorie(),
        bezeichnung=bezeichnung.strip(),
        ist_standard=False,
        paar_session=paar_session,
        erstellt_von=user,
    )


def aufgabe_loeschen(aufgabe: Aufgabe, user: User) -> None:
    if aufgabe.erstellt_von != user:
        raise PermissionError("Nur die Person, die diese Aufgabe erstellt hat, kann sie löschen.")
    if Antwort.objects.filter(aufgabe=aufgabe).exists():
        raise ValueError("Aufgaben, die bereits beantwortet wurden, können nicht gelöscht werden.")
    aufgabe.delete()
