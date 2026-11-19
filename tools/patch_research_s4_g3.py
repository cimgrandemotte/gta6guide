#!/usr/bin/env python3
"""Amendement recherche S4 — groupe G3 (Vice City, armes, véhicules).

Passe du 18/11/2026 : relevés officiels (Trailer 1/2, promo, édition Vintage),
presse accréditée (IGN, GameSpot, Red Bull, Eurogamer, CBC), guides communautaires
et Reddit. Ajoute les faits de géographie urbaine, d'arsenal et de vol de véhicules
sans promouvoir une source secondaire en `official`.

Idempotent : marqueur S4_G3_VERIFIED_FACTS.

Usage : python3 tools/patch_research_s4_g3.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S4_G3_VERIFIED_FACTS"
AT = "2026-11-18"

SOURCES = {
    "gta6locations_districts": "https://gta6locations.com/vice-city-neighborhoods/",
    "leonidahub_weapons": "https://www.leonidahub.co.uk/guides/gta-6-weapons-guide-loadouts",
    "skycoach_weapons": "https://skycoach.gg/blog/gta-6/articles/all-weapons-list",
    "overgear_best_weapons": "https://overgear.com/guides/gta-6/best-weapons-by-role/",
    "gtabase_carstealing": "https://www.gtabase.com/articles/gta-6/gta-6-car-stealing-guide-how-to-steal-sell-keep-vehicles",
    "eurogamer_carstealing": "https://www.eurogamer.net/how-to-steal-cars-gta-6",
    "gta6how_phoneapps": "https://gta6.how/gameplay/phone-apps/",
    "redbull_gameplay": "https://www.redbull.com/us-en/gta-6-gameplay-details",
    "sportskeeda_weapons": "https://www.sportskeeda.com/gta/all-gta-6-weapons-throwables-equipment",
    "technerdiness_weapons": "https://www.technerdiness.com/gta/gta-6-weapons-list/",
    "gtabites_vehicles": "https://www.gtabites.com/vehicles",
    "reddit_loadout": "https://www.reddit.com/r/GTA6/comments/1iqvz9r/realistically_speaking_we_dont_need_to_carry_too/",
}

FACTS = {
    "map_and_regions": [
        {
            "id": "VCX-01",
            "value": "Six quartiers de Vice City sont nommés par Rockstar à l'écran ou dans sa copie : Peacock Bay, Southside, Tequesta, Tisha-Wocka, Stockyard et Ocean Beach — aucun autre nom n'est officiellement confirmé.",
            "status": "official",
            "sources": ["gta6locations_districts"],
        },
        {
            "id": "VCX-02",
            "value": "Peacock Bay et Southside apparaissent sur un panneau de sortie de l'Interstate 97 dans le Trailer 2 ; Tequesta figure sur un panneau Route 3 de captures officielles.",
            "status": "official",
            "sources": ["gta6locations_districts"],
        },
        {
            "id": "VCX-03",
            "value": "Tisha-Wocka est cité dans la copie promo de Rockstar (marché aux puces) ; Stockyard apparaît dans le Trailer 1 lors d'un rassemblement de voitures.",
            "status": "official",
            "sources": ["gta6locations_districts"],
        },
        {
            "id": "VCX-04",
            "value": "Ocean Beach est nommé dans la description du pack Vintage Vice City, qui situe le garage personnel Shore Court près d'Ocean Beach.",
            "status": "official",
            "sources": ["gta6locations_districts"],
        },
        {
            "id": "VCX-05",
            "value": "Waning Sands est une ville incorporée distincte au nord de Vice City, dans le comté de Leonard : nommée dans le Trailer 1 mais hors des limites de la ville.",
            "status": "official",
            "sources": ["gta6locations_districts"],
        },
        {
            "id": "VCX-06",
            "value": "Hiérarchie administrative : Vice City désigne l'agglomération, Vice Beach la ville côtière Art déco, Ocean Beach le quartier balnéaire sud — le tout dans le comté de Vice-Dale.",
            "status": "official",
            "sources": ["gta6locations_districts"],
        },
        {
            "id": "VCX-07",
            "value": "Noms circulant hors sources officielles (Little Havana, Viceport, Vice Point, Rockridge, Starfish Island) : issus de fuites de 2022 ou de wikis communautaires, non confirmés par Rockstar.",
            "status": "community",
            "sources": ["gta6locations_districts"],
        },
        {
            "id": "VCX-08",
            "value": "Les quartiers balnéaires concentrent des événements sociaux (sport de plage, boîtes, défilés de voitures) décrits par la presse ; les zones portuaires et industrielles servent de décor aux braquages et à la contrebande.",
            "status": "press_confirmed",
            "sources": ["redbull_gameplay", "gta6locations_districts"],
        },
    ],
    "weapons": [
        {
            "id": "ARS-01",
            "value": "Système de port limité : deux armes longues et deux armes de poing au maximum sur soi, le reste dans le coffre du véhicule — hérité de Red Dead Redemption 2.",
            "status": "press_confirmed",
            "sources": ["leonidahub_weapons", "skycoach_weapons"],
        },
        {
            "id": "ARS-02",
            "value": "Le véhicule personnel sert d'armurerie mobile ; les Ammu-Nation disposent de casiers d'armes pour changer de chargement.",
            "status": "press_confirmed",
            "sources": ["skycoach_weapons"],
        },
        {
            "id": "ARS-03",
            "value": "Armes nommées dans le matériel officiel : Girardi ES9 (poing de Jason), Klose K17 (poing de Lucia), Hawk & Little Morgan (revolver à lunette), Mustang .357, Nipper .38, Moreland 850 (fusil à pompe), Duke 556 (fusil d'assaut), MP5-style SMG, Combat MG, lance-grenades, RPG, fusil de sniper, Speargun.",
            "status": "press_confirmed",
            "sources": ["skycoach_weapons", "overgear_best_weapons", "sportskeeda_weapons"],
        },
        {
            "id": "ARS-04",
            "value": "Armes et finitions exclusives à l'Ultimate Edition : Girardi ES9 et Klose K17 gravés, revolvers Hawk et Little Morgan, plus une finition « Vintage Vice City » via le pack de précommande.",
            "status": "press_confirmed",
            "sources": ["skycoach_weapons", "overgear_best_weapons"],
        },
        {
            "id": "ARS-05",
            "value": "Nouvel emplacement « équipement » dans la roue : Tracker Jammer, Zip Ties, Loot Bag, Trauma Kit, jumelles, clé USB, auto-dialer, coupe-boulons, lampe torche et speargun.",
            "status": "press_confirmed",
            "sources": ["leonidahub_weapons"],
        },
        {
            "id": "ARS-06",
            "value": "Aucune liste d'arsenal officielle publiée par Rockstar au 18/11 : les noms de modèles hors Ultimate Edition sont en partie attribués par la communauté.",
            "status": "official",
            "sources": ["technerdiness_weapons"],
        },
        {
            "id": "ARS-07",
            "value": "Porter une arme visible déclenche des réactions de panique et l'attention de la police ; le personnage rengaine automatiquement dans les zones civiles denses.",
            "status": "press_confirmed",
            "sources": ["leonidahub_weapons"],
        },
        {
            "id": "ARS-08",
            "value": "Corps à corps tactique : prise d'otage humain, port et déplacement de corps, fouille d'ennemis et combat sous-marin au speargun.",
            "status": "press_confirmed",
            "sources": ["leonidahub_weapons", "technerdiness_weapons"],
        },
        {
            "id": "ARS-09",
            "value": "Les « meilleures armes » publiées (Duke 556 en polyvalent, Moreland 850 en proche, fusil à verrou en longue portée) sont des recommandations de rédaction, pas des statistiques officielles.",
            "status": "speculative",
            "sources": ["overgear_best_weapons", "reddit_loadout"],
        },
    ],
    "vehicles": [
        {
            "id": "CAR-01",
            "value": "Vol de véhicule en plusieurs étapes : repérage, scan, choix de l'outil, effraction, gestion de l'alarme et du traceur, puis décision de vendre ou d'immatriculer.",
            "status": "press_confirmed",
            "sources": ["gtabase_carstealing", "eurogamer_carstealing"],
        },
        {
            "id": "CAR-02",
            "value": "L'application WAINK (crochetage/scan) affiche le niveau de sécurité, l'outil requis, le palier de traceur, le coût d'immatriculation et la valeur de revente avant l'effraction.",
            "status": "press_confirmed",
            "sources": ["gta6how_phoneapps", "gtabase_carstealing"],
        },
        {
            "id": "CAR-03",
            "value": "Trois paliers d'effraction : arracher le conducteur d'une voiture occupée, tige de crochetage ou vitre cassée sur les modèles anciens, clonage de clé sur les modèles à antidémarrage électronique.",
            "status": "press_confirmed",
            "sources": ["eurogamer_carstealing", "gtabase_carstealing"],
        },
        {
            "id": "CAR-04",
            "value": "Le clonage de clé s'obtient en travaillant pour des receleurs pendant l'histoire ; certains véhicules restent inaccessibles au début du jeu.",
            "status": "press_confirmed",
            "sources": ["gtabase_carstealing", "redbull_gameplay"],
        },
        {
            "id": "CAR-05",
            "value": "Un traceur avancé fait « pinguer » la police si la voiture s'éloigne trop de son point de départ : la seule parade connue consiste à rouler vite.",
            "status": "press_confirmed",
            "sources": ["eurogamer_carstealing", "redbull_gameplay"],
        },
        {
            "id": "CAR-06",
            "value": "L'immatriculation d'un véhicule volé se fait au Pay 'n' Spray contre des frais, dégressifs selon la valeur du véhicule ; le garage personnel permet de stocker la flotte.",
            "status": "press_confirmed",
            "sources": ["gtabase_carstealing", "redbull_gameplay"],
        },
        {
            "id": "CAR-07",
            "value": "Déplacements : RydeMe (VTC, saut direct au passager pour 100 $), transports en commun à horaires, et Scooter Bros qui livre la voiture personnelle.",
            "status": "press_confirmed",
            "sources": ["gamespot_tips", "gta6how_phoneapps"],
        },
        {
            "id": "CAR-08",
            "value": "Véhicules de l'édition Ultimate (Schyster Deviant, Declasse Mamba GT, Vapid Riata, Canis Kamacho, coupé Sirius) débloqués progressivement au fil de l'histoire.",
            "status": "press_confirmed",
            "sources": ["gtabites_vehicles"],
        },
        {
            "id": "CAR-09",
            "value": "Aucune vitesse de pointe officielle publiée : les classements « voiture la plus rapide » circulent avec des valeurs estimées et doivent être lus comme des estimations.",
            "status": "speculative",
            "sources": ["gtabites_vehicles"],
        },
        {
            "id": "CAR-10",
            "value": "Le chiffre de 300 véhicules uniques relayé par certains guides n'est pas confirmé par Rockstar ; seules les classes (super, sport, muscle, SUV, tout-terrain, nautique, aérien) sont documentées.",
            "status": "community",
            "sources": ["gtabites_vehicles"],
        },
    ],
}


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("s4_amendments", {}).get("g3", {}).get("marker") == MARKER:
        print("research_data.json : déjà patché en S4/G3 — aucune duplication.")
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

    data.setdefault("s4_amendments", {})["g3"] = {
        "marker": MARKER,
        "at": AT,
        "state": "S4",
        "batch": "G3",
        "pages": ["pages/carte/vice-city.html", "pages/armes/index.html", "pages/vehicules/index.html"],
        "facts_added": added,
        "sources_added": added_sources,
        "surfaces": ["rockstar_officiel", "trailers", "presse_accreditee", "guides_communaute", "reddit"],
        "policy": "Quartiers nommés à l'écran = official ; système d'armes et de vol = press_confirmed ; noms de modèles communautaires et classements de vitesse = community/speculative.",
    }
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Amendement S4/G3 appliqué : +{added} faits, +{added_sources} sources, "
        f"{len(flat)} faits au total, {len(registry)} sources enregistrées."
    )


if __name__ == "__main__":
    main()
