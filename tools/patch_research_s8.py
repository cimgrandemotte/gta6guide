#!/usr/bin/env python3
"""Amendement recherche S8 — reviews (embargo levé le 18/11/2026, 11:00 UTC).

Marqueur `s8_amendment.marker == "S8_REVIEWS_VERIFIED"`. Idempotent.

Le 18 novembre à 11:00 UTC, l'embargo presse a été levé et les notes ont été
publiées. C'est un basculement majeur du corpus : les agrégats passent de
`post_launch_pending` à `press_confirmed`, et la page `pages/reviews/index.html`
devient la page la plus consultée du guide à J-1.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S8_REVIEWS_VERIFIED"

SOURCES = {
    "metacritic_gta6": {
        "title": "GTA VI — Metascore (PS5) 99 sur 109 critiques",
        "publisher": "Metacritic",
        "url": "https://www.metacritic.com/game/grand-theft-auto-vi/",
        "date": "2026-11-18",
        "kind": "agrégateur",
        "status": "press_confirmed",
    },
    "opencritic_gta6": {
        "title": "GTA VI — Top Critic Average 98-99, 100 % de recommandations",
        "publisher": "OpenCritic",
        "url": "https://opencritic.com/game/grand-theft-auto-vi",
        "date": "2026-11-18",
        "kind": "agrégateur",
        "status": "press_confirmed",
    },
    "wolfsgaming_reviews": {
        "title": "GTA 6 reviews are in, and Rockstar might have actually done it",
        "publisher": "Wolf's Gaming Blog",
        "url": "https://wolfsgamingblog.com/2026/11/18/gta-6-reviews-are-in-and-rockstar-might-have-actually-done-it/",
        "date": "2026-11-18",
        "kind": "synthèse de notes",
        "status": "press_confirmed",
    },
    "stealthygaming_reviews": {
        "title": "GTA 6 Reviews Roundup: Metacritic 99 & What Critics Say",
        "publisher": "Stealthy Gaming",
        "url": "https://stealthygaming.com/gta-6-reviews/",
        "date": "2026-11-18",
        "kind": "synthèse de notes",
        "status": "press_confirmed",
    },
    "progameguides_launch": {
        "title": "GTA 6 Launch Day Guide: Unlock Times, Pre-Load, Editions",
        "publisher": "ProGameGuides",
        "url": "https://progameguides.com/gta/gta-6-launch-day-guide/",
        "date": "2026-11-18",
        "kind": "guide de lancement",
        "status": "press_confirmed",
    },
    "rockpapershotgun_release": {
        "title": "GTA 6 release time, launch date, preload, file size",
        "publisher": "Rock Paper Shotgun",
        "url": "https://www.rockpapershotgun.com/gta-6-release-time-date",
        "date": "2026-11-18",
        "kind": "presse",
        "status": "press_confirmed",
    },
    "forbes_release_time": {
        "title": "GTA VI Release Date And Time On PS5 And Xbox Series X, Download Size",
        "publisher": "Forbes · Erik Kain",
        "url": "https://www.forbes.com/sites/erikkain/2026/11/16/gta-6-release-date-time-ps5-xbox-series-x-download-size-day-one-update/",
        "date": "2026-11-16",
        "kind": "presse",
        "status": "press_confirmed",
    },
}

FACTS = {
    "press_reviews": [
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Embargo levé le mercredi 18 novembre 2026 à 11:00 UTC, soit moins d'un jour avant le lancement — et au moment même où le jeu s'ouvrait en Nouvelle-Zélande. Metacritic affichait 99 sur la version PS5 dès les premières heures.",
            "source_url": "https://stealthygaming.com/gta-6-reviews/",
            "source_label": "Synthèses de presse du 18/11/2026",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Metacritic PS5 : 99 sur 109 critiques, environ 80 notes parfaites et aucune sous 90. La version Xbox Series X|S affiche également 99, mais sur beaucoup moins de tests, la majorité des rédactions ayant joué sur PS5.",
            "source_url": "https://www.metacritic.com/game/grand-theft-auto-vi/",
            "source_label": "Metacritic, 18/11/2026",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "OpenCritic : moyenne des critiques entre 98 et 99 selon l'heure du relevé, avec 100 % de recommandations. Le jeu prend la première place du classement du site, devant Baldur's Gate 3, Breath of the Wild et Red Dead Redemption 2.",
            "source_url": "https://opencritic.com/game/grand-theft-auto-vi",
            "source_label": "OpenCritic, 18/11/2026",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Un 99 égale le record de The Legend of Zelda: Ocarina of Time (1998), mais avec un tout autre volume : 22 critiques à l'époque, plus de 100 aujourd'hui. C'est aussi le meilleur score de Rockstar, devant GTA IV (98), GTA V (97) et Red Dead Redemption 2 (97).",
            "source_url": "https://stealthygaming.com/gta-6-reviews/",
            "source_label": "Metacritic via Stealthy Gaming",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Notes parfaites relevées : IGN 10/10 (Luke Reilly), GameSpot, Eurogamer 5/5 (Chris Tapsell), GamesRadar+ 5/5 (Josh West), Push Square 10/10 (Sammy Barker), VGC 5/5 (Jordan Middler), The Guardian 5/5 (Keza MacDonald), Empire 5/5, TechRadar 5/5 (Rob Dwiar), Windows Central 5/5 (Jez Corden), Shacknews 10/10, MMORPG 10/10.",
            "source_url": "https://wolfsgamingblog.com/2026/11/18/gta-6-reviews-are-in-and-rockstar-might-have-actually-done-it/",
            "source_label": "Wolf's Gaming Blog — relevé des notes publiées",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Ce que la critique retient le plus : la densité de Leonida, la relation entre Jason et Lucia, et la liberté laissée au joueur. Push Square parle du « monde ouvert le plus profond et le plus abouti depuis Red Dead Redemption 2 » ; GamesRadar+ du « bac à sable le plus fidèle de sa génération ».",
            "source_url": "https://wolfsgamingblog.com/2026/11/18/gta-6-reviews-are-in-and-rockstar-might-have-actually-done-it/",
            "source_label": "Wolf's Gaming Blog",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Les critiques récurrentes, dans l'ordre de fréquence : le plafond à 30 fps et des chutes ponctuelles en zone dense, des commandes contextuelles trop chargées (Kotaku cite un coup de pied déclenché au lieu d'un rechargement), un rythme narratif qui s'essouffle sur la seconde moitié, et des ennemis lourdement blindés qui deviennent des éponges à balles.",
            "source_url": "https://stealthygaming.com/gta-6-reviews/",
            "source_label": "Synthèse Stealthy Gaming / Kotaku / TheSixthAxis / Push Square",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Le score le plus bas relevé dans la première vague est 9/10 (TheSixthAxis), qui salue Jason et Lucia, le casting secondaire et la liberté d'approche des missions, mais regrette une histoire qui accroche moins et une police peu menaçante.",
            "source_url": "https://wolfsgamingblog.com/2026/11/18/gta-6-reviews-are-in-and-rockstar-might-have-actually-done-it/",
            "source_label": "Wolf's Gaming Blog — TheSixthAxis",
        },
        {
            "id": "REV-XX",
            "status": "community",
            "text": "Avant l'ouverture des notes, la page Metacritic du jeu a été inondée de notes d'utilisateurs inventées (un 6,5 sur cinq votes). Elles ont été retirées. Le score utilisateur n'a de sens qu'une fois le jeu accessible à tous.",
            "source_url": "https://nexorift.blogspot.com/2026/11/gta-6-reviews-99-metacritic-best-ever-score.html",
            "source_label": "Relevé de modération Metacritic",
        },
    ],
    "release_and_platforms": [
        {
            "id": "REL-XX",
            "status": "official",
            "text": "Lancement à minuit heure locale dans chaque région le 19 novembre 2026, sur PS5 et Xbox Series X|S : un déploiement roulant pays par pays, pas une ouverture simultanée mondiale.",
            "source_url": "https://www.rockpapershotgun.com/gta-6-release-time-date",
            "source_label": "Rockstar Support, relayé par Rock Paper Shotgun",
        },
        {
            "id": "REL-XX",
            "status": "press_confirmed",
            "text": "La Nouvelle-Zélande ouvre la marche à 00:00 NZDT, soit 11:00 UTC le 18 novembre — six heures avant la côte est des États-Unis et une demi-journée avant l'Europe.",
            "source_url": "https://www.technobezz.com/gta-6-release-time",
            "source_label": "PlayStation Store / relevés régionaux",
        },
        {
            "id": "REL-XX",
            "status": "press_confirmed",
            "text": "Exception à la règle de minuit : aux États-Unis et au Canada, la version PS5 se débloque d'un bloc à 05:00 UTC, soit minuit heure de l'Est (21 h sur la côte ouest le 18). Le Royaume-Uni ouvre à minuit UTC, l'Europe centrale à minuit CET.",
            "source_url": "https://progameguides.com/gta/gta-6-launch-day-guide/",
            "source_label": "PlayStation Store via ProGameGuides",
        },
        {
            "id": "REL-XX",
            "status": "official",
            "text": "Xbox Cloud Gaming est la seule vraie exception : le streaming commence à 1 h du matin (heure de l'Est) le 19 novembre pour tout le monde, soit 22 h le 18 sur la côte ouest.",
            "source_url": "https://thetechhacker.com/2026/11/17/gta-6-release-time-us-time-zones/",
            "source_label": "Xbox Wire",
        },
        {
            "id": "REL-XX",
            "status": "press_confirmed",
            "text": "Aucun patch du jour J n'a été annoncé séparément au 16 novembre. Ce qui est certain : préchargement ouvert depuis le 10/11 (minuit local sur PS5, 0 h GMT sur Xbox), jusqu'à 212 Go requis, et deux patchs déjà absorbés avant le lancement (01.002.000 puis 01.002.001).",
            "source_url": "https://www.forbes.com/sites/erikkain/2026/11/16/gta-6-release-date-time-ps5-xbox-series-x-download-size-day-one-update/",
            "source_label": "Forbes, 16/11/2026",
        },
    ],
}


def _renumber(data: dict) -> None:
    facts = data.get("facts", {})
    prefix = {"press_reviews": "REV", "release_and_platforms": "REL"}
    for section, items in FACTS.items():
        used = set()
        for f in facts.get(section, []):
            m = re.match(r"^([A-Z]+)-(\d+)$", str(f.get("id", "")))
            if m:
                used.add(int(m.group(2)))
        nxt = max(used) + 1 if used else 1
        for item in items:
            item["id"] = f"{prefix[section]}-{nxt:02d}"
            nxt += 1


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("s8_amendment", {}).get("marker") == MARKER:
        print("research_data.json : déjà patché en S8 — aucune duplication.")
        return

    _renumber(data)
    sources = data.setdefault("sources_registry", {})
    added_src = 0
    for k, v in SOURCES.items():
        if k not in sources:
            sources[k] = v
            added_src += 1

    facts = data.setdefault("facts", {})
    added = 0
    for section, items in FACTS.items():
        bucket = facts.setdefault(section, [])
        ids = {f.get("id") for f in bucket}
        for item in items:
            if item["id"] in ids:
                continue
            bucket.append({
                "id": item["id"],
                "status": item["status"],
                "fact": item["text"],
                "source_url": item["source_url"],
                "source_label": item["source_label"],
                "added_in": "S8",
            })
            added += 1

    data["s8_amendment"] = {
        "marker": MARKER,
        "at": "2026-11-18T13:00:00Z",
        "event": "Levée d'embargo presse à 11:00 UTC le 18/11/2026",
        "facts_added": added,
        "sources_added": added_src,
        "ids": {s: [f["id"] for f in items] for s, items in FACTS.items()},
        "scores": {"metacritic_ps5": 99, "metacritic_reviews": 109,
                   "opencritic": "98-99", "recommend_rate": 1.0, "lowest_score": "9/10"},
        "policy": "Les agrégats sont datés et volatils : toute note est présentée avec son horodatage et son volume de critiques.",
    }

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in facts.values())
    print(f"Amendement S8 appliqué : +{added} faits, +{added_src} sources, {total} faits, {len(sources)} sources.")


if __name__ == "__main__":
    main()
