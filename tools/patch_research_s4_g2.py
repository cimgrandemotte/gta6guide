#!/usr/bin/env python3
"""Amendement recherche S4 — groupe G2 (Personnages).

Passe du 18/11/2026 : fiches officielles « Only in Leonida », presse accréditée
(CBC, IGN, TheClick, GameSpot), suivi de distribution, Reddit. Ajoute les faits
de distribution et de gameplay des personnages sans promouvoir une source
secondaire en `official`.

Idempotent : marqueur S4_G2_VERIFIED_FACTS.

Usage : python3 tools/patch_research_s4_g2.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S4_G2_VERIFIED_FACTS"
AT = "2026-11-18"

SOURCES = {
    "rockstar_only_in_leonida": "https://www.rockstargames.com/VI/only-in-leonida",
    "rockstar_vi_ultimate": "https://www.rockstargames.com/VI",
    "ign_gameplay_details": "https://www.ign.com/articles/gta-6-new-gameplay-details",
    "cbc_review": "https://www.cbc.ca/news/entertainment/grand-theft-auto-vi-review-9.7425005",
    "theclick_characters": "https://www.theclick.gg/gta-6-characters-list/",
    "gamespot_tips": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
    "castingcompanion_cast": "https://castingcompanion.com/blog/gta-6-cast-who-plays-lucia-jason",
    "gamingpromax_voice": "https://gamingpromax.com/gta-6-jason-lucia-voice-actors/",
    "reddit_villain": "https://www.reddit.com/r/GTA6/comments/1wjukhy/gta_6s_main_vilain/",
}

FACTS = {
    "story_and_characters": [
        {
            "id": "CAST-01",
            "value": "Rockstar a publié 8 fiches de personnages couvrant 9 personnes nommées (Jason, Lucia, Cal, Boobie, Dre'Quan, Bae-Luxe, Roxy, Raul, Brian), plus Lori et DWNPLY cités dans les biographies.",
            "status": "official",
            "sources": ["rockstar_only_in_leonida"],
        },
        {
            "id": "CAST-02",
            "value": "Brian Heder : trafiquant « de la grande époque » des Keys, écoule la marchandise via son chantier naval avec sa troisième épouse Lori ; Jason loge gratuitement chez lui et rembourse en intimidations.",
            "status": "official",
            "sources": ["rockstar_only_in_leonida", "theclick_characters"],
        },
        {
            "id": "CAST-03",
            "value": "Boobie Ike : légende locale de Vice City, empire bâti sur l'immobilier, un club de strip-tease et un studio d'enregistrement ; « tout sourire jusqu'à ce qu'il faille parler affaires ».",
            "status": "official",
            "sources": ["rockstar_only_in_leonida", "theclick_characters"],
        },
        {
            "id": "CAST-04",
            "value": "Dre'Quan Priest : « plus hustler que gangster », ancien dealer devenu patron de label ; il signe Real Dimez sur Only Raw Records et rêve de sortir du circuit des clubs de Boobie.",
            "status": "official",
            "sources": ["rockstar_only_in_leonida", "theclick_characters"],
        },
        {
            "id": "CAST-05",
            "value": "Real Dimez (Bae-Luxe et Roxy) : amies depuis le lycée, elles ont transformé des rackets de dealers en titres et en présence sociale ; un premier tube avec DWNPLY, puis cinq ans de vaches maigres avant Only Raw Records.",
            "status": "official",
            "sources": ["rockstar_only_in_leonida", "theclick_characters"],
        },
        {
            "id": "CAST-06",
            "value": "Raul Bautista : braqueur de banques chevronné, charme et culot, recrute des talents pour des coups de plus en plus risqués ; son équipe finira par devoir doubler la mise ou se retirer.",
            "status": "official",
            "sources": ["rockstar_only_in_leonida", "theclick_characters"],
        },
        {
            "id": "CAST-07",
            "value": "Wyman est nommé dans le descriptif de l'édition Ultimate comme fixer et collecteur local, sans fiche de personnage ni visuel officiel dédié.",
            "status": "press_confirmed",
            "sources": ["rockstar_vi_ultimate", "theclick_characters"],
        },
        {
            "id": "CAST-08",
            "value": "Distribution : Stephen Root a confirmé sa participation (Associated Press, septembre 2026) et Variety l'identifie comme la voix de Brian Heder ; Jim Santangeli a confirmé un petit rôle non identifié.",
            "status": "press_confirmed",
            "sources": ["castingcompanion_cast", "gamingpromax_voice"],
        },
        {
            "id": "CAST-09",
            "value": "Manni L. Perez est identifiée comme la voix de Lucia via sa nomination Best Performance aux Game Awards 2026 (17/11/2026) ; Rockstar n'a publié aucune liste de distribution.",
            "status": "press_confirmed",
            "sources": ["gamingpromax_voice", "castingcompanion_cast"],
        },
        {
            "id": "CAST-10",
            "value": "Jason Duval reste sans comédien confirmé au 18/11 : Dylan Rourke est l'attribution la plus citée ; Troy Baker et Roger Craig Smith ont explicitement démenti.",
            "status": "community",
            "sources": ["castingcompanion_cast", "gamingpromax_voice"],
        },
        {
            "id": "CAST-11",
            "value": "Méndez apparaît nommé dans le matériel officiel de l'Extended Look ; John Ortiz est rapporté comme voix, sans confirmation.",
            "status": "press_confirmed",
            "sources": ["castingcompanion_cast"],
        },
        {
            "id": "CAST-12",
            "value": "D'après la critique CBC du 18/11, l'équipe de voleurs et de perceurs de coffres de Raul Bautista accompagne Jason et Lucia dans une série de braquages à forts enjeux.",
            "status": "press_confirmed",
            "sources": ["cbc_review"],
        },
        {
            "id": "CAST-13",
            "value": "Aucun antagoniste principal n'a été officialisé au 18/11 : Boobie Ike, Raul et Brian sont tour à tour suspectés par la communauté, sans preuve.",
            "status": "speculative",
            "sources": ["reddit_villain"],
        },
        {
            "id": "CAST-14",
            "value": "La chevillère électronique de Lucia joue un rôle narratif et sert de point de départ à son rapprochement avec Jason (détails de la démo Rockstar relayés par IGN).",
            "status": "press_confirmed",
            "sources": ["ign_gameplay_details"],
        },
        {
            "id": "CAST-15",
            "value": "Stats des protagonistes : Santé, Endurance et Focus ; musculation pour la santé, cardio pour l'endurance, activités « mindfulness » (pêche, billard, câlin à un chat) pour le Focus — seul le Focus est permanent.",
            "status": "press_confirmed",
            "sources": ["gamespot_tips", "ign_gameplay_details"],
        },
        {
            "id": "CAST-16",
            "value": "Lucia à l'entraînement : sac de frappe et circuits en salle dans la démo ; elle recharge un fusil à pompe d'une main et conduite en fuite pendant que Jason tire.",
            "status": "press_confirmed",
            "sources": ["ign_gameplay_details", "gamespot_tips"],
        },
    ]
}


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("s4_amendments", {}).get("g2", {}).get("marker") == MARKER:
        print("research_data.json : déjà patché en S4/G2 — aucune duplication.")
        return

    registry = data["sources_registry"]
    added_sources = 0
    for key, url in SOURCES.items():
        if key not in registry:
            registry[key] = url
            added_sources += 1

    added = 0
    for section, entries in FACTS.items():
        bucket = data["facts"].setdefault(section, [])
        existing = {f["id"] for f in bucket}
        for entry in entries:
            if entry["id"] in existing:
                continue
            urls = [SOURCES[s] if s in SOURCES else registry[s] for s in entry["sources"]]
            bucket.append({
                "id": entry["id"],
                "value": entry["value"],
                "status": entry["status"],
                "sources": urls,
                "source_url": urls[0],
                "retrieved_at": AT,
            })
            added += 1

    flat = [f for sec in data["facts"].values() for f in sec]
    totals = data.setdefault("meta", {}).setdefault("totals", {})
    totals["facts"] = len(flat)
    totals["sources_registered"] = len(registry)
    totals["sections"] = len(data["facts"])

    data.setdefault("s4_amendments", {})["g2"] = {
        "marker": MARKER,
        "at": AT,
        "state": "S4",
        "batch": "G2",
        "pages": ["pages/personnages/lucia.html", "pages/personnages/secondaires.html", "pages/personnages/index.html"],
        "facts_added": added,
        "sources_added": added_sources,
        "surfaces": ["rockstar_officiel", "presse_accreditee", "reddit", "forums", "reseaux_sociaux"],
        "policy": "Fiches Rockstar = official ; distribution = press_confirmed sauf démentis/non-confirmations (community) ; théories d'antagoniste = speculative.",
    }
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Amendement S4/G2 appliqué : +{added} faits, +{added_sources} sources, "
        f"{len(flat)} faits au total, {len(registry)} sources enregistrées."
    )


if __name__ == "__main__":
    main()
