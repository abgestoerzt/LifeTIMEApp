from pairs.models import PaarSession
from survey.models import Antwort, AntwortChoices


def berechne_gesamtverteilung(session: PaarSession) -> dict[str, dict[str, float]]:
    """Berechnet den prozentualen Anteil am Mental Load pro Partner:in."""
    user_a = session.partner_a
    user_b = session.partner_b
    if not user_b:
        return {}

    kategorien = ["management", "ausfuehrung"]
    ergebnis: dict[str, dict[str, float]] = {}

    for dimension in kategorien:
        punkte_a = 0
        punkte_b = 0
        gesamt = 0

        antworten_a = Antwort.objects.filter(paar_session=session, user=user_a)
        for a in antworten_a:
            wert = getattr(a, dimension)
            if wert == AntwortChoices.ICH:
                punkte_a += 1
            elif wert == AntwortChoices.PARTNER:
                punkte_b += 1
            elif wert == AntwortChoices.BEIDE:
                punkte_a += 0.5
                punkte_b += 0.5
            if wert != AntwortChoices.NICHT_ZUTREFFEND:
                gesamt += 1

        ergebnis[dimension] = {
            "partner_a": round(punkte_a / gesamt * 100, 1) if gesamt else 0,
            "partner_b": round(punkte_b / gesamt * 100, 1) if gesamt else 0,
        }
    return ergebnis


def berechne_kategorie_verteilung(session: PaarSession) -> list[dict]:
    """Liefert pro Kategorie den Anteil an Management/Ausführung je Person."""
    from catalog.models import Kategorie

    user_a = session.partner_a
    user_b = session.partner_b
    if not user_b:
        return []

    kategorien = Kategorie.objects.prefetch_related("aufgaben")
    result = []

    for kat in kategorien:
        aufgaben_ids = list(kat.aufgaben.values_list("id", flat=True))  # type: ignore[attr-defined]
        if not aufgaben_ids:
            continue

        antworten_a = Antwort.objects.filter(
            paar_session=session, user=user_a, aufgabe_id__in=aufgaben_ids
        )
        if not antworten_a.exists():
            continue

        def anteil(antworten: object, dimension: str, person: str) -> float:  # type: ignore[return]
            gesamt = 0
            punkte = 0
            for a in antworten:  # type: ignore[union-attr]
                wert = getattr(a, dimension)
                if wert == AntwortChoices.NICHT_ZUTREFFEND:
                    continue
                gesamt += 1
                if (person == "a" and wert == AntwortChoices.ICH) or (
                    person == "b" and wert == AntwortChoices.PARTNER
                ):
                    punkte += 1
                elif wert == AntwortChoices.BEIDE:
                    punkte += 0.5
            return round(punkte / gesamt * 100, 1) if gesamt else 0

        result.append(
            {
                "kategorie": kat,
                "management_a": anteil(antworten_a, "management", "a"),
                "management_b": anteil(antworten_a, "management", "b"),
                "ausfuehrung_a": anteil(antworten_a, "ausfuehrung", "a"),
                "ausfuehrung_b": anteil(antworten_a, "ausfuehrung", "b"),
            }
        )
    return result


def finde_wahrnehmungsluecken(session: PaarSession) -> list[dict]:
    """Vergleicht Antworten beider Partner:innen aufgabenweise."""
    user_a = session.partner_a
    user_b = session.partner_b
    if not user_b:
        return []

    antworten_a = {
        a.aufgabe_id: a  # type: ignore[attr-defined]
        for a in Antwort.objects.filter(paar_session=session, user=user_a)
    }
    antworten_b = {
        a.aufgabe_id: a  # type: ignore[attr-defined]
        for a in Antwort.objects.filter(paar_session=session, user=user_b)
    }

    luecken = []
    for aufgabe_id, ant_a in antworten_a.items():
        ant_b = antworten_b.get(aufgabe_id)
        if not ant_b:
            continue
        markierung = None
        if (
            ant_a.management == AntwortChoices.ICH
            and ant_b.management == AntwortChoices.ICH
        ):
            markierung = "konflikt"
        elif (
            ant_a.management == AntwortChoices.ICH
            and ant_b.management == AntwortChoices.BEIDE
        ):
            markierung = "unsichtbar"
        elif (
            ant_a.management == AntwortChoices.PARTNER
            and ant_b.management == AntwortChoices.PARTNER
        ):
            markierung = "luecke"

        if markierung:
            luecken.append(
                {
                    "aufgabe": ant_a.aufgabe,
                    "antwort_a": ant_a,
                    "antwort_b": ant_b,
                    "markierung": markierung,
                }
            )
    return luecken
