from datetime import date, timedelta

from django.contrib.auth.models import User
from pairs.models import PaarSession
from plan.models import Umverteilung

from .models import CheckIn, CheckInAntwort


def get_montag(d: date) -> date:
    return d - timedelta(days=d.weekday())


def checkin_starten(session: PaarSession, user: User) -> CheckIn:
    woche = get_montag(date.today())
    checkin, _ = CheckIn.objects.get_or_create(
        paar_session=session, woche=woche, user=user
    )
    return checkin


def checkin_speichern(checkin: CheckIn, daten: dict[str, str]) -> None:
    for key, status in daten.items():
        if key.startswith("aufgabe_"):
            aufgabe_id = int(key.split("_")[1])
            CheckInAntwort.objects.update_or_create(
                checkin=checkin,
                aufgabe_id=aufgabe_id,
                defaults={"status": status},
            )


def get_checkin_aufgaben(session: PaarSession) -> list[Umverteilung]:
    return list(
        Umverteilung.objects.filter(paar_session=session)
        .exclude(management_neu="abschaffen")
        .select_related("aufgabe__kategorie")
    )


def beide_haben_eingecheckt(session: PaarSession, woche: date) -> bool:
    if not session.partner_b:
        return False
    return CheckIn.objects.filter(paar_session=session, woche=woche).count() >= 2


def get_verlauf(session: PaarSession, wochen: int = 8) -> list[dict]:
    checkins = CheckIn.objects.filter(paar_session=session).order_by("-woche")
    wochen_dict: dict[date, dict] = {}
    for ci in checkins:
        if ci.woche not in wochen_dict:
            wochen_dict[ci.woche] = {
                "woche": ci.woche,
                "anzahl_ja": 0,
                "anzahl_gesamt": 0,
            }
        antworten = CheckInAntwort.objects.filter(checkin=ci)
        wochen_dict[ci.woche]["anzahl_gesamt"] += antworten.count()
        wochen_dict[ci.woche]["anzahl_ja"] += antworten.filter(status="ja").count()
    return sorted(wochen_dict.values(), key=lambda x: x["woche"])[-wochen:]
