#!/usr/bin/env python3
"""Amendement recherche S4 — BUILD_CONTENT_PAGES / groupe G1 (Histoire).

Passe du 18/11/2026 : Rockstar officiel (« Only in Leonida » : Jason, Lucia,
Cal Hampton), presse accréditée (TalkEsport, Press Start, GameSpot), guides
communautaires. Ajoute les faits « histoire / synopsis / chapitres / missions »
et la structure de chapitres canonique, sans jamais promouvoir une source
secondaire en `official`.

Idempotent : marqueur S4_VERIFIED_FACTS.

Usage : python3 tools/patch_research_s4.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S4_VERIFIED_FACTS"
AT = "2026-11-18"

S4_SOURCES = {
    "talkesport_chapters": "https://www.talkesport.com/gta-6/all-gta-6-chapters-missions-list/",
    "talkesport_replay": "https://www.talkesport.com/gta-6/gta-6-replay-missions-manual-save/",
    "press_start_mission_count": "https://press-start.com.au/news/2026/11/18/heres-how-many-story-missions-are-in-grand-theft-auto-6/",
    "gamespot_how_long": "https://www.gamespot.com/articles/how-long-to-beat-gta-6/",
    "rockstar_leonida_jason": "https://www.rockstargames.com/VI/only-in-leonida/jason",
    "rockstar_leonida_lucia": "https://www.rockstargames.com/VI/only-in-leonida/lucia",
    "gadgets360_characters": "https://www.gadgets360.com/games/features/gta-6-characters-guide-grand-theft-auto-vi-jason-duval-lucia-caminos-brian-heder-cal-hampton-boobie-ike-more-9826820",
    "gamerbolt_lucia": "https://www.gamerbolt.com/gta-6-lucia-caminos/",
    "gta6gang_jason": "https://gta6gang.com/pages/gta6-jason.html",
    "beebom_missions": "https://beebom.com/gta-6-missions-list-walkthrough/",
}

# Chapitre : (titre officiel affiché dans le recap, nombre de missions, liste)
CHAPTERS = [
    {
        "number": 1,
        "title": "Just Like Paradise",
        "missions": 22,
        "list": [
            "Prologue", "Gone Fishing", "Gear Up", "Just A Scratch", "Lab Fees",
            "Unwanted Attention", "Pipework", "Hey Arnold!", "Island Dreams",
            "Feng Shui", "Coming Home", "Buck Me", "Clean Up After Donnie",
            "Down To Earth", "Clear Skies", "Day Release", "Swamped",
            "[Nom masqué — spoiler]", "Recalibration", "Tourist Trap",
            "Home Sweet Home", "Discharge Time",
        ],
    },
    {
        "number": 2,
        "title": "Paradise Lost",
        "missions": 13,
        "list": [
            "What's In The Bag?", "Ambulance Chaser", "Just Moved In", "Girls' Trip",
            "Moses", "Daily Driver", "Slam Dunk", "Breakfast Run", "Coffee Break",
            "Afternoon Delight", "Thrillbillies", "Twist Wrist, Smash, Grab",
            "Checking Out",
        ],
    },
    {
        "number": 3,
        "title": "Tits Ass Drug Money",
        "missions": 26,
        "list": [
            "Welcome To Vice City", "Dealer's Choice", "Meet The Heders",
            "Dubious Provenance", "Mami Knows Best", "South Leonida Real Estate",
            "Tyrone", "Here, Kitty Kitty", "Kitter Litter Labs", "Car Service",
            "Top Billing", "Boobie Time", "First Impressions", "Crosstown Traffic",
            "Credit Check", "Steal The Zorrusso For Randy",
            "Sinfrontera National Bank", "Security Expert", "Ride Or Die",
            "Company Property", "The Missing Link", "Safe Word", "Cooties",
            "Bricked Up", "Hidden Charges", "The Cartel Heist",
        ],
    },
    {
        "number": 4,
        "title": "Vice City, Baby",
        "missions": 25,
        "list": [
            "Ocean Beach", "Another Life", "Company Cars", "Lawyer Up", "Party Hard",
            "Heavy Lifting", "Photo/Shoot", "Making Gainz", "Watch It",
            "Cash Injections", "Amateur Hour", "Dirty Work", "Too Much Baggage",
            "Adventures In Babysitting", "Fresh Evidence", "Power Play",
            "Child's Play", "Headliners", "Close Surveillance", "Delivery Method",
            "Team Building", "Fully Catered", "VCIA Takedown", "Sunset",
            "[Nom masqué — spoiler]",
        ],
    },
    {
        "number": 5,
        "title": "Top of the World, Ma",
        "missions": 7,
        "list": [
            "Bird In The Hand", "Taking Liberties", "VC Baby", "Doggie Bag",
            "Operation Savage Glory", "Protective Custody",
            "[Nom masqué — spoiler]",
        ],
    },
]

NEW_FACTS = {
    "missions_endings_trophies": [
        {
            "id": "HST-01",
            "value": "Campagne : 93 missions principales réparties en 5 chapitres, d'après l'onglet Story recap du jeu (TalkEsport, 18/11).",
            "status": "press_confirmed",
            "sources": ["talkesport_chapters", "press_start_mission_count"],
        },
        {
            "id": "HST-02",
            "value": "Répartition des chapitres : Just Like Paradise 22, Paradise Lost 13, Tits Ass Drug Money 26, Vice City, Baby 25, Top of the World, Ma 7.",
            "status": "press_confirmed",
            "sources": ["talkesport_chapters", "press_start_mission_count", "gamespot_how_long"],
        },
        {
            "id": "HST-03",
            "value": "Les listes annonçant 91 missions omettaient deux missions du chapitre 2 (Thrillbillies et Twist Wrist, Smash, Grab) ; le total retenu est 93.",
            "status": "press_confirmed",
            "sources": ["talkesport_chapters", "beebom_missions"],
        },
        {
            "id": "HST-04",
            "value": "Aucun replay des missions terminées : il faut recharger une sauvegarde manuelle ; le jeu propose 15 emplacements, comme GTA V et RDR2.",
            "status": "press_confirmed",
            "sources": ["talkesport_replay"],
        },
        {
            "id": "HST-05",
            "value": "La liste du Story recap est un ordre d'affichage : la structure ouverte du jeu permet de terminer certaines missions dans un autre ordre.",
            "status": "press_confirmed",
            "sources": ["press_start_mission_count", "gamespot_how_long"],
        },
        {
            "id": "HST-06",
            "value": "Durées contradictoires : GameSpot ≥65 h pour la campagne, 90–100 h avec le contenu annexe, 200 h+ pour le 100 % ; Press Start ~50 h ; TrueAchievements ~50–80 h.",
            "status": "press_confirmed",
            "sources": ["gamespot_how_long", "press_start_mission_count"],
        },
        {
            "id": "MIS-10",
            "value": "Le nom de la dernière mission du chapitre 4 et celui de la mission finale sont masqués par la presse pour éviter les spoilers ; aucune fin officielle validée par Rockstar.",
            "status": "post_launch_pending",
            "sources": ["talkesport_chapters", "gamespot_how_long"],
        },
        {
            "id": "HST-11",
            "value": "GameSpot (18/11) : au moins 65 h pour la campagne, 90–100 h en explorant les annexes, plus de 200 h pour le 100 % ; aucun journaliste n'a bouclé le 100 % au moment de la publication.",
            "status": "press_confirmed",
            "sources": ["gamespot_how_long"],
        },
        {
            "id": "HST-07",
            "value": "Le chapitre 3 est le plus long de la campagne et se referme sur The Cartel Heist ; le chapitre 5 est le plus court avec 7 missions.",
            "status": "press_confirmed",
            "sources": ["talkesport_chapters"],
        },
        {
            "id": "HST-08",
            "value": "Aucune confirmation de fins multiples : la structure en 5 chapitres est documentée, les variantes de fin restent une hypothèse communautaire.",
            "status": "speculative",
            "sources": ["gta6gang_jason", "beebom_missions"],
        },
        {
            "id": "HST-09",
            "value": "La campagne démarre par le Prologue (Lucia au pénitencier de Leonida) puis Gone Fishing avec Jason ; Coming Home fait se rencontrer les deux protagonistes.",
            "status": "press_confirmed",
            "sources": ["talkesport_chapters", "beebom_missions"],
        },
        {
            "id": "HST-10",
            "value": "Deux braquages majeurs structurent le chapitre 3 : Sinfrontera National Bank et The Cartel Heist.",
            "status": "press_confirmed",
            "sources": ["talkesport_chapters"],
        },
    ],
    "story_and_characters": [
        {
            "id": "CHA-18",
            "value": "Bio officielle Jason : « Jason veut une vie facile, mais les choses ne font que devenir plus difficiles » ; enfance parmi les escrocs, passage dans l'Army, puis les Keys chez les trafiquants locaux.",
            "status": "official",
            "sources": ["rockstar_leonida_jason"],
        },
        {
            "id": "CHA-19",
            "value": "Bio officielle Lucia : son père lui a appris à se battre dès qu'elle a su marcher ; la prison pour avoir défendu sa famille, la sortie grâce à la chance, « désormais uniquement des choix intelligents ».",
            "status": "official",
            "sources": ["rockstar_leonida_lucia"],
        },
        {
            "id": "CHA-20",
            "value": "Bio officielle Lucia : elle veut la belle vie dont sa mère rêvait depuis leurs années à Liberty City, et compte prendre les choses en main plutôt que fantasmer.",
            "status": "official",
            "sources": ["rockstar_leonida_lucia"],
        },
        {
            "id": "CHA-21",
            "value": "Cal Hampton (officiel) : ami de Jason et associé de Brian, il écoute les communications des Coast Guard avec quelques bières et des onglets privés ouverts.",
            "status": "official",
            "sources": ["rockstar_leonida_jason"],
        },
        {
            "id": "CHA-22",
            "value": "Répliques officielles publiées par Rockstar : « If anything happens, I'm right behind you », « Another day in paradise, right? », « The only thing that matters is who you know and what you got ».",
            "status": "official",
            "sources": ["rockstar_leonida_jason", "rockstar_leonida_lucia"],
        },
        {
            "id": "CHA-23",
            "value": "Rockstar présente la rencontre avec Lucia comme pouvant être la meilleure ou la pire chose arrivée à Jason ; la romance est optionnelle, la fin reste ouverte.",
            "status": "official",
            "sources": ["rockstar_leonida_jason", "rockstar_leonida_lucia"],
        },
        {
            "id": "CHA-24",
            "value": "Capacités spéciales (Combat Focus / Deadeye pour Jason, tir de précision au ralenti pour Lucia) : décrites par des guides, jamais confirmées par Rockstar — à traiter en hypothèse.",
            "status": "speculative",
            "sources": ["gta6gang_jason", "gamerbolt_lucia"],
        },
        {
            "id": "CHA-25",
            "value": "Comédiens : Dylan Rourke (Jason) et Manni L. Perez (Lucia) sont rapportés par la presse et la communauté ; Rockstar n'a pas publié de distribution complète.",
            "status": "community",
            "sources": ["gta6gang_jason", "gamerbolt_lucia"],
        },
        {
            "id": "CHA-26",
            "value": "Âge, nationalité et motif exact de l'incarcération de Lucia ne sont pas communiqués ; Lucia et sa mère ont vécu à Liberty City sans que ce soit présenté comme son lieu de naissance.",
            "status": "official",
            "sources": ["rockstar_leonida_lucia"],
        },
        {
            "id": "CHA-27",
            "value": "Bascule Jason / Lucia en monde ouvert et dans les missions compatibles, missions verrouillées sur un seul protagoniste, appel ou SMS pour faire venir le partenaire : mécanique décrite par la presse.",
            "status": "press_confirmed",
            "sources": ["gadgets360_characters", "gamerbolt_lucia"],
        },
    ],
}


def resolve(key_or_url: str, registry: dict[str, str]) -> str:
    if key_or_url.startswith("http"):
        return key_or_url
    url = S4_SOURCES.get(key_or_url) or registry.get(key_or_url)
    if not url:
        raise KeyError(key_or_url)
    return url


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("s4_amendment", {}).get("marker") == MARKER:
        print("research_data.json : déjà patché en S4 — aucune duplication.")
        return

    registry = data["sources_registry"]
    added_sources = 0
    for key, url in S4_SOURCES.items():
        if key not in registry:
            registry[key] = url
            added_sources += 1

    added_facts = 0
    for section, entries in NEW_FACTS.items():
        bucket = data["facts"].setdefault(section, [])
        existing = {f["id"] for f in bucket}
        for entry in entries:
            if entry["id"] in existing:
                continue
            urls = [resolve(s, registry) for s in entry["sources"]]
            bucket.append({
                "id": entry["id"],
                "value": entry["value"],
                "status": entry["status"],
                "sources": urls,
                "source_url": urls[0],
                "retrieved_at": AT,
            })
            added_facts += 1

    data["s4_chapter_structure"] = {
        "marker": MARKER,
        "status": "press_confirmed",
        "not_official": "Aucune liste de missions officielle publiée par Rockstar ; structure reconstituée depuis l'onglet Story recap.",
        "spoiler": True,
        "total_missions": sum(c["missions"] for c in CHAPTERS),
        "chapters": CHAPTERS,
        "sources": [S4_SOURCES["talkesport_chapters"], S4_SOURCES["press_start_mission_count"]],
        "retrieved_at": AT,
    }

    flat = [f for sec in data["facts"].values() for f in sec]
    data.setdefault("meta", {}).setdefault("totals", {})
    data["meta"]["totals"]["facts"] = len(flat)
    data["meta"]["totals"]["sources_registered"] = len(registry)
    data["meta"]["totals"]["sections"] = len(data["facts"])
    data["s4_amendment"] = {
        "marker": MARKER,
        "at": AT,
        "state": "S4",
        "batch": "G1",
        "pages": ["pages/histoire/index.html", "pages/histoire/synopsis.html", "pages/histoire/missions.html"],
        "facts_added": added_facts,
        "sources_added": added_sources,
        "surfaces": ["rockstar_officiel", "presse_accreditee", "forums", "YouTube", "GitHub", "Reddit", "reseau_social"],
        "policy": "Aucune source secondaire promue en official ; les capacités spéciales et les fins multiples restent speculative.",
    }

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Amendement S4 appliqué : +{added_facts} faits, +{added_sources} sources, "
        f"{len(flat)} faits au total, {len(registry)} sources enregistrées, "
        f"{data['s4_chapter_structure']['total_missions']} missions sur 5 chapitres."
    )


if __name__ == "__main__":
    main()
