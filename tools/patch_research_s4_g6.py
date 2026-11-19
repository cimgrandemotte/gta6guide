#!/usr/bin/env python3
"""Amendement recherche S4 / groupe G6 — Trophées, Secrets, Tips.

Idempotent : marqueur `s4_amendments.g6.marker == "S4_G6_VERIFIED_FACTS"`.

⚠ Depuis la sortie du 19/11/2026, la liste des 55 trophées et la checklist 100 %
sont publiques. En revanche, **aucun code de triche** n'est publié par ce projet :
la page Codes reste à zéro code (voir patch G5).

Règle appliquée : les noms de trophées liés à l'histoire et les conditions de la
checklist sont `official`/`press_confirmed` ; toute coordonnée d'easter egg non
documentée par une source primaire reste `community` et passe derrière un
SpoilerToggle.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S4_G6_VERIFIED_FACTS"

SOURCES = {
    "gtaboom_trophies": {
        "title": "Every GTA 6 Trophy and Achievement at Launch and How to Unlock Them",
        "publisher": "GTA Boom",
        "url": "https://www.gtaboom.com/every-gta-6-trophy-and-achievement-at-launch-and-how-to-unlock-them-fc5f",
        "date": "2026-11-18",
        "kind": "liste de trophées",
        "status": "press_confirmed",
    },
    "gamespew_trophies": {
        "title": "Here's the full trophy/achievement list for Grand Theft Auto VI",
        "publisher": "GameSpew",
        "url": "https://www.gamespew.com/2026/11/heres-the-full-trophy-achievement-list-for-grand-theft-auto-vi/",
        "date": "2026-11-18",
        "kind": "liste de trophées",
        "status": "press_confirmed",
    },
    "beebom_trophies": {
        "title": "GTA 6 Trophy List: How to Unlock All Trophies and Achievements",
        "publisher": "Beebom",
        "url": "https://beebom.com/gta-6-trophy-achievements-list/",
        "date": "2026-11-18",
        "kind": "liste de trophées (rareté)",
        "status": "press_confirmed",
    },
    "powerpyx_roadmap": {
        "title": "GTA 6 Trophy Guide & Roadmap",
        "publisher": "PowerPyx",
        "url": "https://www.powerpyx.com/gta-6-grand-theft-auto-vi-trophy-guide-roadmap/",
        "date": "2026-11-18",
        "kind": "guide trophées / roadmap",
        "status": "press_confirmed",
    },
    "powerpyx_100": {
        "title": "GTA 6 100% Completion Checklist & Guide",
        "publisher": "PowerPyx",
        "url": "https://www.powerpyx.com/gta-6-100-completion-checklist-guide/",
        "date": "2026-11-18",
        "kind": "checklist 100 %",
        "status": "press_confirmed",
    },
    "powerpyx_wiki": {
        "title": "GTA 6 Wiki & Strategy Guide (base de collectibles)",
        "publisher": "PowerPyx",
        "url": "https://www.powerpyx.com/gta-6-grand-theft-auto-vi-wiki-strategy-guide/",
        "date": "2026-11-18",
        "kind": "base de données",
        "status": "press_confirmed",
    },
    "reddit_trophies": {
        "title": "[GTA 6] How are you guys planning to tackle the platinum trophy? (r/Trophies)",
        "publisher": "Reddit · r/Trophies",
        "url": "https://www.reddit.com/r/Trophies/comments/1xd1ji4/gta_6_how_are_you_guys_planning_to_tackle_the/",
        "date": "2026-10-23",
        "kind": "forum",
        "status": "community",
    },
    "gamespot_tips": {
        "title": "GTA 6 Tips: Everything I Wish I Knew Before I Started Playing",
        "publisher": "GameSpot",
        "url": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
        "date": "2026-11-18",
        "kind": "guide pratique (post-embargo)",
        "status": "press_confirmed",
    },
    "biglead_tips": {
        "title": "8 GTA 6 tips the game doesn't tell you, from someone who's played for 140 hours",
        "publisher": "The Big Lead",
        "url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
        "date": "2026-11-18",
        "kind": "guide pratique",
        "status": "press_confirmed",
    },
    "gta6life_easter": {
        "title": "GTA 6 easter eggs: 7 Vice City and Red Dead nods already spotted",
        "publisher": "GTA6 Life",
        "url": "https://gta6-life.com/en/guides/gta-6-easter-eggs/",
        "date": "2026-11-16",
        "kind": "relevé d'easter eggs vérifiés sur médias officiels",
        "status": "press_confirmed",
    },
    "gta6loop_easter": {
        "title": "GTA 6 Easter Eggs: Confirmed Callbacks & Hidden Details",
        "publisher": "GTA6 Loop",
        "url": "https://gta6loop.com/easter-eggs",
        "date": "2026-07-25",
        "kind": "guide (sépare confirmé / théorie)",
        "status": "press_confirmed",
    },
    "grandtheft_extended": {
        "title": "GTA 6 Extended Look Easter Eggs and Hidden Details",
        "publisher": "Grand Theft",
        "url": "https://grandtheft.gg/gta-6-extended-look-easter-eggs",
        "date": "2026-08-29",
        "kind": "relevé image par image",
        "status": "press_confirmed",
    },
    "gtavispot_easter": {
        "title": "GTA 6 Easter Eggs: Every Secret & Pop Culture Reference",
        "publisher": "GTA VI Spot",
        "url": "https://gtavispot.com/map/easter-eggs/",
        "date": "2026-06-25",
        "kind": "carte d'easter eggs (non sourcée)",
        "status": "community",
    },
    "vicecitymethods_easter": {
        "title": "GTA 6 Easter Eggs & Secrets: All Hidden References",
        "publisher": "Vice City Methods",
        "url": "https://vicecitymethods.com/easter-eggs/gta-6-easter-eggs-secrets",
        "date": "2026-08-01",
        "kind": "guide (mélange confirmé et inventé)",
        "status": "community",
    },
}

FACTS = {
    "missions_endings_trophies": [
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "GTA VI compte 55 trophées et succès au lancement sur PS5 et Xbox Series X|S, dont 28 cachés et 27 visibles, et aucun trophée lié à un mode en ligne — celui-ci n'existe pas encore.",
            "source_url": "https://beebom.com/gta-6-trophy-achievements-list/",
            "source_label": "Beebom, liste avec raretés",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Le platine s'appelle « Vice Got a Price! » et se débloque en obtenant tous les autres trophées ; son texte est « Congratulations! You're a Leonida Legend ».",
            "source_url": "https://www.gtaboom.com/every-gta-6-trophy-and-achievement-at-launch-and-how-to-unlock-them-fc5f",
            "source_label": "GTA Boom",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Six trophées récompensent la progression narrative, un par chapitre plus le final : « Just Like Paradise » (Gone Fishing), « Paradise Lost » (chapitre 1), « T**s Ass Drug Money » (chapitre 2, nom censuré sur les trackers), « Vice City, Baby! » (chapitre 3), « Top Of The World, Ma » (chapitre 4) et « You Gotta Know When to Get Off » (mission finale).",
            "source_url": "https://www.gamespew.com/2026/11/heres-the-full-trophy-achievement-list-for-grand-theft-auto-vi/",
            "source_label": "GameSpew",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Six trophées de mission nommée : « Trust » (Breakfast Run), « Break the Bank » (The Cartel Heist), « Family Matters » (Child's Play), « DWNFALL » (Headliners), « Hi-Jacked » (VCIA Takedown) et « Snow Storm » (Operation Savage Glory).",
            "source_url": "https://onemoregame.ph/2026/11/grand-theft-auto-vi-trophy-list/",
            "source_label": "One More Game",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Deux trophées d'or seulement : « You Gotta Know When to Get Off » (mission finale) et « A Long Road » (100 % de complétion). Le platine mis à part, le reste est en bronze et argent.",
            "source_url": "https://beebom.com/gta-6-trophy-achievements-list/",
            "source_label": "Beebom",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "La checklist 100 % n'apparaît qu'après l'histoire, dans Progress > Stats > 100% Completion, mais la progression faite pendant l'histoire est comptabilisée rétroactivement.",
            "source_url": "https://www.powerpyx.com/gta-6-100-completion-checklist-guide/",
            "source_label": "PowerPyx",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Rien n'est manquable pour la checklist 100 % : tout reste faisable en libre après l'histoire. Exigences réelles : 200 véhicules scannés sur 557, 100 animaux étudiés sur 255, 100 lieux WAiNK sur 125, 33 découvertes sous-marines sur 33.",
            "source_url": "https://www.powerpyx.com/gta-6-100-completion-checklist-guide/",
            "source_label": "PowerPyx",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "La checklist est volontairement clémente : elle représente environ 60 % du vrai contenu. Plusieurs catégories ne demandent qu'une fraction des objets — 15 sets de cartes sur 18, 5 sets de Kenton sur 7, 30 magazines sur 34, 100 flamants de cocaïne sur 125, 15 spots de méditation sur 18.",
            "source_url": "https://www.powerpyx.com/gta-6-100-completion-checklist-guide/",
            "source_label": "PowerPyx",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Le seul point réellement manquable concerne un trophée de méditation : le premier spot, à la maison de Jason, n'est accessible qu'au chapitre 1. Méditer avec Jason ET Lucia au même endroit compte pour deux.",
            "source_url": "https://www.powerpyx.com/gta-6-grand-theft-auto-vi-trophy-guide-roadmap/",
            "source_label": "PowerPyx, roadmap",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Durées annoncées : 60–80 h pour l'histoire, environ 200 h pour la checklist 100 %, plus de 300 h pour un vrai 100 % intégral. Il n'y a ni médailles d'or de mission ni fonction de rejouabilité de mission.",
            "source_url": "https://www.powerpyx.com/gta-6-grand-theft-auto-vi-wiki-strategy-guide/",
            "source_label": "PowerPyx, wiki",
        },
        {
            "id": "TRO-XX",
            "status": "press_confirmed",
            "text": "Base de collecte du jeu : 557 véhicules (277 modèles de base et 280 remarquables), 196 armes (53 armes à feu, 9 de mêlée, 4 explosifs, 130 variantes) et 255 animaux répartis en huit familles.",
            "source_url": "https://www.powerpyx.com/gta-6-grand-theft-auto-vi-wiki-strategy-guide/",
            "source_label": "PowerPyx, wiki",
        },
        {
            "id": "TRO-XX",
            "status": "community",
            "text": "Consensus de joueurs sur la préparation du platine : traiter les manquables en premier, puis l'histoire, puis le contenu annexe et les défis de performance. Les platines Rockstar sont surtout chronophages plus que difficiles.",
            "source_url": "https://www.reddit.com/r/Trophies/comments/1xd1ji4/gta_6_how_are_you_guys_planning_to_tackle_the/",
            "source_label": "Reddit r/Trophies",
        },
    ],
    "easter_eggs_and_secrets": [
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "Rockstar n'a jamais nommé un seul easter egg de GTA VI dans sa communication officielle. Tous les clins d'œil listés ici viennent de relevés de médias officiels (trailers, cover, Extended Look) par la presse et la communauté.",
            "source_url": "https://gta6-life.com/en/guides/gta-6-easter-eggs/",
            "source_label": "GTA6 Life, 16/11/2026",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "Trailer 1 (05/12/2023) montre l'Ocean View Hotel, premier planque de Vice City en 2002, et un autocollant « Petty Forever ».",
            "source_url": "https://gta6-life.com/en/guides/gta-6-easter-eggs/",
            "source_label": "GTA6 Life, relevé daté",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "Trailer 2 (06/05/2025) montre une armurerie nommée « Phil's Ammu-Nation », référence à Phil Cassidy de GTA III et Vice City. Un gecko peint sur le mur du magasin porte la chemise hawaïenne bleue de Tommy Vercetti — détail repéré seulement le 21/06/2026.",
            "source_url": "https://gta6-life.com/en/guides/gta-6-easter-eggs/",
            "source_label": "GTA6 Life / PC Gamer",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "La cover art du 19/06/2026 reprend trois emplacements de la cover de 2002 : un Sea Sparrow, une moto et une supercar jaune à la place de l'Infernus.",
            "source_url": "https://gta6-life.com/en/guides/gta-6-easter-eggs/",
            "source_label": "GTA6 Life / IGN",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "L'Extended Look du 27/08/2026 contient un clin d'œil interne : la publicité parodique du « Prairie Sandwich Box Meal » (à 7 min 34) est filmée sur un décor de Red Dead Redemption 2, au nord d'Annesburg.",
            "source_url": "https://gta6-life.com/en/guides/gta-6-easter-eggs/",
            "source_label": "GTA6 Life (identification communautaire du décor)",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "L'appartement de Lucia dans l'Extended Look contient une œuvre de style Vice City, identifiée comme un tirage de Patrick Nagel, et un ours en peluche rappelant celui de Trevor dans GTA V.",
            "source_url": "https://grandtheft.gg/gta-6-extended-look-easter-eggs",
            "source_label": "Grand Theft, relevé image par image",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "Le pseudo « @ScooterBros » apparaît dans le chat d'un livestream in-game : c'est un rappel de la vidéo virale « Scooter Brothers » de 2008 (GTA IV), déjà citée par Trevor dans GTA V.",
            "source_url": "https://grandtheft.gg/gta-6-extended-look-easter-eggs",
            "source_label": "Grand Theft",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "Un appartement de l'Extended Look reprend la disposition de celui de Dexter Morgan dans la série Dexter, elle-même située à Miami — inspiration réelle de Vice City.",
            "source_url": "https://grandtheft.gg/gta-6-extended-look-easter-eggs",
            "source_label": "Grand Theft",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "Le nom de l'État, « Leonida », renvoie à l'explorateur Juan Ponce de León, qui mena la première expédition européenne en Floride en 1513.",
            "source_url": "https://gta6loop.com/easter-eggs",
            "source_label": "GTA6 Loop (sépare confirmé et théorie)",
        },
        {
            "id": "SEC-XX",
            "status": "press_confirmed",
            "text": "Clins d'œil confirmés dans les médias officiels : le retour de la marque Patriot Beer (GTA IV et V), la façade « Only in Leonida » (parodie de Florida Man) et la bannière du club Nine1Nine.",
            "source_url": "https://gta6loop.com/easter-eggs",
            "source_label": "GTA6 Loop",
        },
        {
            "id": "SEC-XX",
            "status": "community",
            "text": "Les coordonnées précises d'easter eggs « jouables » (soucoupe volante au mont Kalaga à 3 h du matin, chambre au chainsaw façon Scarface à Ocean Beach, épave d'OVNI au nord, Skunk Ape des Grassrivers, portrait de Tommy Vercetti à Star Island) proviennent de cartes communautaires non sourcées et ne sont confirmées par aucune source primaire.",
            "source_url": "https://gtavispot.com/map/easter-eggs/",
            "source_label": "GTA VI Spot — carte communautaire",
        },
        {
            "id": "SEC-XX",
            "status": "community",
            "text": "Certaines « listes d'easter eggs » mélangent des clins d'œil attestés et des inventions pures (Malibu Club « ouvert avec du synth-wave », ruines du manoir Vercetti, jumeaux numériques de personnages). Le tri n'est possible qu'en revenant aux médias officiels.",
            "source_url": "https://vicecitymethods.com/easter-eggs/gta-6-easter-eggs-secrets",
            "source_label": "Vice City Methods — exemple de mélange confirmé/inventé",
        },
    ],
    "tips_strategies_techniques": [
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Trois statistiques principales : santé, endurance et Focus. La musculation augmente la barre de santé, le cardio (course, vélo, kayak) l'endurance, et les activités « mindfulness » (pêche, billard) le Focus.",
            "source_url": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
            "source_label": "GameSpot, 18/11/2026",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Le Focus sert à voir les ennemis à travers les murs, repérer les notes contenant des codes de coffre, suivre les traces d'animaux et deviner si quelqu'un cache des objets de valeur dans un coffre de voiture.",
            "source_url": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
            "source_label": "GameSpot",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Les deux accessoires d'arme les plus rentables sont la lunette et le silencieux : une arme équipée d'une lunette passe en vue subjective en cliquant le stick droit (impossible avec les mires métalliques), et le silencieux retarde l'arrivée de la police, y compris lors d'un assaut de repaire de gang.",
            "source_url": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
            "source_label": "GameSpot",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Le jeu est découpé en chapitres, chacun centré sur une planque différente. Une fois passé au chapitre suivant, on ne revient pas en arrière sans sauvegarde manuelle : sauvegarder à chaque chapitre est le seul moyen de revisiter les anciennes planques et les dialogues manqués.",
            "source_url": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
            "source_label": "GameSpot",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Les flingues s'entendent : si quelqu'un signale des coups de feu, la police vient. Jouer non létal est possible — crever deux pneus fait partir en tête-à-queue un véhicule poursuivant, et tirer en direction d'un hélicoptère le fait reculer, ce que le pilote annonce à la radio.",
            "source_url": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
            "source_label": "GameSpot",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "On peut pousser un véhicule à la main : marcher contre lui jusqu'à l'invite, puis maintenir la touche d'action. Utile pour remettre à l'eau un bateau échoué ou redresser une voiture retournée sans payer de remorquage.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead, 140 h de jeu",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "En voiture, la touche d'action ouvre la portière pour frapper un passant, un motard ou quelqu'un qui tente de vous extraire du véhicule ; à moto, cela devient un coup de pied — de quoi déstabiliser des adversaires en course.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Maintenir gauche sur la croix directionnelle ouvre la radio ; pousser le stick vers le haut depuis ce menu ouvre le menu du véhicule : warnings, pleins phares, vitres, capote des décapotables. Une pression gauche ou droite sur la croix actionne le clignotant.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Un coffre s'ouvre avec n'importe quelle explosion, pas seulement un bâton de dynamite : grenade, bonbonne de propane ou lance-roquettes font l'affaire si le code manque.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Pour nager longtemps : démarrer en surface, cliquer le stick pour accélérer (deux fois pour la vitesse maximale), puis plonger quand l'endurance est vide — sous l'eau, la jauge passe en capacité pulmonaire et permet de continuer à pleine vitesse.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Repérage avant un braquage : entrer comme client, verrouiller un garde comme pour interagir et appuyer à droite sur la croix pour le marquer. Une flèche reste au-dessus de sa tête pendant le braquage.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Lecture de la carte : les bâtiments bleu foncé sont ceux que l'on peut pénétrer — parfois seulement le garage ou un couloir. Il faut faire tourner la carte pour trouver les portes, et guetter l'invite d'interaction à l'approche.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead",
        },
        {
            "id": "TIP-XX",
            "status": "press_confirmed",
            "text": "Le Focus sert aussi de détecteur d'événements : un halo circulaire sonore apparaît quand une rencontre unique se trouve à proximité. C'est le signal pour ne pas passer à côté d'un contenu optionnel.",
            "source_url": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
            "source_label": "The Big Lead",
        },
    ],
}


def _renumber(data: dict) -> None:
    facts = data.get("facts", {})
    prefix = {
        "missions_endings_trophies": "TRO",
        "easter_eggs_and_secrets": "SEC",
        "tips_strategies_techniques": "TIP",
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
    amend = data.setdefault("s4_amendments", {})
    g6 = amend.setdefault("g6", {})

    if g6.get("marker") == MARKER:
        print("research_data.json : déjà patché en S4/G6 — aucune duplication.")
        return

    _renumber(data)

    sources = data.setdefault("sources_registry", {})
    added_src = 0
    for key, payload in SOURCES.items():
        if key not in sources:
            sources[key] = payload
            added_src += 1

    facts = data.setdefault("facts", {})
    added_facts = 0
    for section, items in FACTS.items():
        bucket = facts.setdefault(section, [])
        existing = {f.get("id") for f in bucket}
        for item in items:
            if item["id"] in existing:
                continue
            bucket.append({
                "id": item["id"],
                "status": item["status"],
                "fact": item["text"],
                "source_url": item["source_url"],
                "source_label": item["source_label"],
                "added_in": "S4_G6",
            })
            added_facts += 1

    g6.update({
        "marker": MARKER,
        "at": "2026-11-18",
        "pages": [
            "pages/trophees/index.html",
            "pages/secrets/index.html",
            "pages/tips/index.html",
        ],
        "facts_added": added_facts,
        "sources_added": added_src,
        "ids": {s: [f["id"] for f in items] for s, items in FACTS.items()},
        "policy": "Easter eggs : seuls les clins d'œil relevés dans des médias officiels sont retenus ; les coordonnées non sourcées restent community et derrière SpoilerToggle.",
    })

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in facts.values())
    print(f"Amendement S4/G6 appliqué : +{added_facts} faits, +{added_src} sources, "
          f"{total} faits au total, {len(sources)} sources enregistrées.")


if __name__ == "__main__":
    main()
