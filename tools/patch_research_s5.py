#!/usr/bin/env python3
"""Amendement recherche S5 — INTERACTIVE_FEATURES.

Marqueur `s5_amendment.marker == "S5_VERIFIED_FACTS"`. Idempotent.

Trois surfaces :
  • le projet cartographique communautaire (atlas, versions, licences, volumes) ;
  • les trackers de complétion et la structure réelle du 100 % (challenges,
    séries de cartes) telle que la documentent les guides post-embargo ;
  • la culture quiz / trivia et l'état de la carte officielle au lancement.

Aucun chiffre de complétion n'est inventé : les 80 challenges, 18 séries de
480 cartes et les seuils 50/70 viennent de PowerPyx (18/11/2026).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S5_VERIFIED_FACTS"

SOURCES = {
    "leonidaexplorer_map": {
        "title": "GTA 6 Map: Interactive Leonida & Vice City Map (3D) — 3 339 points",
        "publisher": "Leonida Explorer",
        "url": "https://leonidaexplorer.com/map/",
        "date": "2026-11-19",
        "kind": "carte communautaire 3D",
        "status": "community",
    },
    "mapheist_map": {
        "title": "GTA 6 interactive map: Leonida and Vice City, every known place",
        "publisher": "MapHeist",
        "url": "https://mapheist.com/en/map/",
        "date": "2026-11-17",
        "kind": "carte communautaire + méthodologie",
        "status": "community",
    },
    "gtadb_tiles": {
        "title": "GTA VI Map Tiles & Landmarks Data — base YANIS (CC BY 4.0)",
        "publisher": "gtadb.org (projet de cartographie communautaire)",
        "url": "https://map.gtadb.org/",
        "date": "2026-11",
        "kind": "jeu de données ouvert",
        "status": "community",
    },
    "gta6mapsize": {
        "title": "GTA 6 Map: Interactive Map of Leonida and Vice City — ce qui est confirmé vs fuité",
        "publisher": "GTA6 MapSize",
        "url": "https://gta6mapsize.com/",
        "date": "2026-09-03",
        "kind": "atlas communautaire",
        "status": "community",
    },
    "sixintelhq_map": {
        "title": "GTA 6 Map: Free Interactive Map — carte officielle imprimable au lancement",
        "publisher": "Six Intel HQ",
        "url": "https://sixintelhq.com/map",
        "date": "2026-11-18",
        "kind": "carte communautaire + veille officielle",
        "status": "press_confirmed",
    },
    "forbes_map_wildlife": {
        "title": "GTA 6's Map Is About Twice The Size Of GTA 5, With Hurricanes And 170 Animal Species",
        "publisher": "Forbes · Brian Mazique",
        "url": "https://www.forbes.com/sites/brianmazique/2026/10/06/gta-6s-map-is-about-twice-the-size-of-gta-5-with-hurricanes-and-170-animal-species/",
        "date": "2026-10-06",
        "kind": "presse (couverture Game Informer)",
        "status": "press_confirmed",
    },
    "powerpyx_collectibles": {
        "title": "GTA 6 Collectible Guide — Progress Database (~3 000 entrées)",
        "publisher": "PowerPyx",
        "url": "https://www.powerpyx.com/guide/gta-6-grand-theft-auto-vi/",
        "date": "2026-11-18",
        "kind": "guide post-embargo",
        "status": "press_confirmed",
    },
    "powerpyx_challenges": {
        "title": "GTA 6 All Challenges Guide — 80 challenges, 8 catégories",
        "publisher": "PowerPyx",
        "url": "https://www.powerpyx.com/gta-6-all-challenges-guide/",
        "date": "2026-11-18",
        "kind": "guide post-embargo",
        "status": "press_confirmed",
    },
    "progressbar": {
        "title": "ProgressBar — GTA 6 100% completion tracker (live le 19/11)",
        "publisher": "ProgressBar",
        "url": "https://progressbar.gg/",
        "date": "2026-11",
        "kind": "outil fan de suivi",
        "status": "community",
    },
    "upblazed_tracker": {
        "title": "GTA 6 100% Completion Tracker & Checklist (sauvegarde locale)",
        "publisher": "Upblazed",
        "url": "https://upblazed.com/tools/gta-6-completion-tracker",
        "date": "2026-11",
        "kind": "outil fan de suivi",
        "status": "community",
    },
    "crowdparty_trivia": {
        "title": "30+ GTA Trivia Questions and Answers",
        "publisher": "CrowdParty",
        "url": "https://crowdparty.app/blog/30-gta-trivia-questions-and-answers-to-test-your-grand-theft-auto-knowledge/",
        "date": "2026-11-04",
        "kind": "banque de questions",
        "status": "community",
    },
    "randomtrivia_gta": {
        "title": "120 Grand Theft Auto Trivia Questions & Answers",
        "publisher": "Random Trivia",
        "url": "https://randomtrivia.co/grand-theft-auto-trivia/",
        "date": "2026-08-15",
        "kind": "banque de questions",
        "status": "community",
    },
    "guardian_quiz": {
        "title": "Thursday news quiz — GTA VI main characters",
        "publisher": "The Guardian",
        "url": "https://www.theguardian.com/lifeandstyle/2026/nov/12/the-guardian-thursday-quiz-general-knowledge-topical-news-trivia-272",
        "date": "2026-11-12",
        "kind": "presse (culture générale)",
        "status": "press_confirmed",
    },
    "boostroom_beginner": {
        "title": "GTA 6 Beginner Guide: What New Players Should Know",
        "publisher": "BoostRoom",
        "url": "https://boostroom.com/blog/gta-6-beginner-guide-what-new-players-should-know",
        "date": "2026-07-05",
        "kind": "guide débutant",
        "status": "community",
    },
    "gamespot_100_questions": {
        "title": "GTA 6 Is 100 Days Away, And We Have 100 Questions",
        "publisher": "GameSpot",
        "url": "https://www.gamespot.com/articles/gta-6-is-100-days-away-and-we-have-100-questions/",
        "date": "2026-08-11",
        "kind": "presse (questions ouvertes)",
        "status": "press_confirmed",
    },
}

FACTS = {
    "map_and_regions": [
        {
            "id": "MAP-XX",
            "status": "press_confirmed",
            "text": "Rockstar n'a pas publié de carte interactive officielle. Le 3 novembre 2026, le Newswire a annoncé pour le 19/11 une carte et un poster de jaquette à imprimer, gratuits en téléchargement, puis une version physique double face à 0,99 $ ou offerte avec un achat en boutique Rockstar. C'est une feuille imprimable, pas une carte interactive.",
            "source_url": "https://sixintelhq.com/map",
            "source_label": "Newswire 03/11/2026, relayé par Six Intel HQ",
        },
        {
            "id": "MAP-XX",
            "status": "community",
            "text": "Les cartes interactives de fans s'appuient sur la base communautaire YANIS (projet gtadb.org), reconstruite image par image depuis les trailers et publiée sous licence CC BY 4.0. Chaque épingle porte une étiquette de preuve : confirmée, ou reconstruite.",
            "source_url": "https://mapheist.com/en/map/",
            "source_label": "MapHeist — méthodologie et attribution CC BY 4.0",
        },
        {
            "id": "MAP-XX",
            "status": "community",
            "text": "Ordres de grandeur des atlas de fans au 18/11/2026 : Leonida Explorer revendique 3 339 points cartographiés, 290 lieux nommés et 1 064 vues in-game officielles ; le State of Leonida dépassait 1 500 marqueurs dès sa v12. Ces volumes mesurent l'effort communautaire, pas la taille du jeu.",
            "source_url": "https://leonidaexplorer.com/map/",
            "source_label": "Leonida Explorer / State of Leonida",
        },
        {
            "id": "MAP-XX",
            "status": "press_confirmed",
            "text": "Taille : Rockstar décrit Leonida comme environ deux fois la carte de GTA V et trois fois la zone jouable de Red Dead Redemption 2, sans publier de kilomètres carrés. La mesure communautaire sur matériel fuité avance ≈ 83 km² de terres, soit 1,7 fois GTA V — un chiffre communautaire, jamais officiel.",
            "source_url": "https://gta6mapsize.com/",
            "source_label": "Rockstar (Aaron Garbut) via Forbes / GTA6 MapSize",
        },
        {
            "id": "MAP-XX",
            "status": "press_confirmed",
            "text": "Régions nommées officiellement : Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia et Mount Kalaga National Park. Les six comtés qui circulent (Vice-Dale, Leonard, Kelly, Ambrosia, Mariana, Lummox) proviennent d'un build de 2023 et restent non confirmés.",
            "source_url": "https://gta6mapsize.com/",
            "source_label": "Rockstar + matériel fuité, statuts distingués",
        },
        {
            "id": "MAP-XX",
            "status": "press_confirmed",
            "text": "Météo locale et persistante, ouragans inclus (nuages massifs, vents forts), et plus de 170 espèces animales classées Rare, Découvrable et Légendaire — plus de 60 oiseaux, plus de 30 mammifères terrestres, plus poissons et reptiles.",
            "source_url": "https://www.forbes.com/sites/brianmazique/2026/10/06/gta-6s-map-is-about-twice-the-size-of-gta-5-with-hurricanes-and-170-animal-species/",
            "source_label": "Game Informer / Forbes, 06/10/2026",
        },
        {
            "id": "MAP-XX",
            "status": "community",
            "text": "Conseil d'exploration qui revient partout : progresser par couches — quartier de départ, puis routes proches, puis grands repères, puis régions lointaines. Cela évite l'effet « carte trop grande » des trois premières heures.",
            "source_url": "https://boostroom.com/blog/gta-6-beginner-guide-what-new-players-should-know",
            "source_label": "BoostRoom, guide débutant",
        },
    ],
    "missions_endings_trophies": [
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Le 100 % s'organise autour de 80 challenges répartis en 8 catégories de 10. Terminer n'importe lesquels 50 débloque le trophée « One Last Thing » ; 70 sur 80 sont exigés pour la checklist 100 %.",
            "source_url": "https://www.powerpyx.com/gta-6-all-challenges-guide/",
            "source_label": "PowerPyx, guide des challenges",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Les collectibles passent par une base de progression interne (Menu Carte → Progression) : environ 3 000 entrées couvrant véhicules, animaux, armes et braquages. Certaines sous-catégories n'apparaissent qu'après une première découverte.",
            "source_url": "https://www.powerpyx.com/guide/gta-6-grand-theft-auto-vi/",
            "source_label": "PowerPyx, base de progression",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "18 séries de cartes à collectionner, 480 cartes uniques au total. Trois séries complètes débloquent « Don't Touch My Deck » ; quinze séries complètes sont exigées pour la checklist 100 % et le trophée « A Long Road ».",
            "source_url": "https://www.powerpyx.com/gta-6-all-collectible-card-sets-locations/",
            "source_label": "PowerPyx, séries de cartes",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "La checklist 100 % n'apparaît qu'après la fin de l'histoire, mais la progression réalisée pendant l'histoire est déjà comptée : jouer normalement ne fait donc rien perdre.",
            "source_url": "https://www.powerpyx.com/gta-6-100-completion-checklist-guide/",
            "source_label": "PowerPyx, checklist 100 %",
        },
        {
            "id": "TRO-XX",
            "status": "community",
            "text": "Les trackers de fans (ProgressBar, Upblazed, vice-den) se remplissent au lancement et sauvegardent en local, sans compte. Avant le 19/11, leurs listes sont des gabarits calqués sur GTA V : utiles pour se préparer, pas pour compter.",
            "source_url": "https://progressbar.gg/",
            "source_label": "ProgressBar / Upblazed",
        },
    ],
    "community_tools_and_social": [
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Trois familles d'outils interactifs cohabitent : les cartes (Leonida Explorer, MapHeist, Six Intel HQ), les trackers de complétion (ProgressBar, Upblazed) et la recherche interne du jeu (Menu Carte → Progression), qui reste la seule source de vérité pour votre sauvegarde.",
            "source_url": "https://sixintelhq.com/map",
            "source_label": "Panorama croisé des outils 2026",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Le débat récurrent de r/GTA6 et des serveurs Discord de cartographie : faut-il ouvrir la carte interactive dès la première heure ? Le consensus pratique est de jouer la première région sans carte, puis de l'ouvrir pour la chasse aux collectibles.",
            "source_url": "https://www.reddit.com/r/GTA6/",
            "source_label": "Reddit r/GTA6 et Discord de cartographie",
        },
    ],
    "quiz_and_trivia": [
        {
            "id": "QIZ-XX",
            "status": "community",
            "text": "Les quiz GTA existants mélangent deux registres : la culture de série (Liberty City = New York, Vice City = Miami, Tommy Vercetti = protagoniste de Vice City en 2002) et l'actualité de GTA VI (Leonida, Jason et Lucia, 19 novembre 2026).",
            "source_url": "https://crowdparty.app/blog/30-gta-trivia-questions-and-answers-to-test-your-grand-theft-auto-knowledge/",
            "source_label": "CrowdParty / Random Trivia",
        },
        {
            "id": "QIZ-XX",
            "status": "press_confirmed",
            "text": "Faits vérifiables utilisés dans les quiz de presse : premiers jeux en 1997, GTA VI annoncé d'abord pour 2025 puis repoussé au 19 novembre 2026, premier trailer à environ 90 millions de vues en 24 h selon le Guinness World Records.",
            "source_url": "https://crowdparty.app/blog/30-gta-trivia-questions-and-answers-to-test-your-grand-theft-auto-knowledge/",
            "source_label": "CrowdParty (faits de série et de calendrier)",
        },
        {
            "id": "QIZ-XX",
            "status": "press_confirmed",
            "text": "La presse généraliste s'en sert comme question d'actualité : les deux protagonistes sont Jason Duval et Lucia Caminos. C'est le niveau de notoriété atteint par le jeu la semaine du lancement.",
            "source_url": "https://www.theguardian.com/lifeandstyle/2026/nov/12/the-guardian-thursday-quiz-general-knowledge-topical-news-trivia-272",
            "source_label": "The Guardian, 12/11/2026",
        },
        {
            "id": "QIZ-XX",
            "status": "post_launch_pending",
            "text": "Les questions de quiz sur le contenu interne (nombre de missions, fins, activités secondaires) n'auront de réponses fiables qu'après le 19/11. Un quiz honnête avant le lancement ne pose que des questions de calendrier, de distribution et de géographie nommée.",
            "source_url": "https://www.gamespot.com/articles/gta-6-is-100-days-away-and-we-have-100-questions/",
            "source_label": "GameSpot — 100 questions encore ouvertes",
        },
    ],
}


def _renumber(data: dict) -> None:
    facts = data.get("facts", {})
    prefix = {
        "map_and_regions": "MAP",
        "missions_endings_trophies": "TRO",
        "community_tools_and_social": "OUT",
        "quiz_and_trivia": "QIZ",
    }
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
    existing = data.get("s5_amendment", {})
    if existing.get("marker") == MARKER:
        print("research_data.json : déjà patché en S5 — aucune duplication.")
        return

    _renumber(data)

    sources = data.setdefault("sources_registry", {})
    added_src = 0
    for key, payload in SOURCES.items():
        if key not in sources:
            sources[key] = payload
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
                "added_in": "S5",
            })
            added += 1

    data["s5_amendment"] = {
        "marker": MARKER,
        "at": "2026-11-18",
        "pages": [
            "pages/carte/index.html",
            "pages/collectibles/index.html",
            "pages/quiz/index.html",
        ],
        "facts_added": added,
        "sources_added": added_src,
        "ids": {s: [f["id"] for f in items] for s, items in FACTS.items()},
        "policy": "Cartes et trackers = community ; chiffres de complétion = guides post-embargo (press_confirmed) ; carte officielle = imprimable seulement.",
    }

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in facts.values())
    print(f"Amendement S5 appliqué : +{added} faits, +{added_src} sources, {total} faits, "
          f"{len(sources)} sources.")


if __name__ == "__main__":
    main()
