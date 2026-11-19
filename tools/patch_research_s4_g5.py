#!/usr/bin/env python3
"""Amendement recherche S4 / groupe G5 — Musique, Online, Codes.

Idempotent : marqueur `s4_amendments.g5.marker == "S4_G5_VERIFIED_FACTS"`.
Les identifiants sont renumérotés automatiquement par section pour éviter toute
collision avec le corpus S1/S2 existant (MUS / ONL / CHE).

Règle dure appliquée ici : **aucun code de triche n'est publié**. Rockstar n'a
diffusé aucune combinaison, aucun numéro de téléphone et aucune commande pour
GTA VI au 18/11/2026. La page correspondante explique la situation et refuse de
recopier les listes de GTA V présentées comme des codes de GTA VI.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S4_G5_VERIFIED_FACTS"

SOURCES = {
    "thetechhacker_radio": {
        "title": "GTA 6 Radio Stations and Soundtrack: Full Confirmed List",
        "publisher": "The Tech Hacker",
        "url": "https://thetechhacker.com/2026/11/16/gta-6-radio-stations-soundtrack-score/",
        "date": "2026-11-16",
        "kind": "guide",
        "status": "official",
    },
    "grandtheft_radio": {
        "title": "GTA 6 Radio Stations: Hosts, Genres, and Features",
        "publisher": "Grand Theft",
        "url": "https://grandtheft.gg/gta-6-radio-stations/",
        "date": "2026-10-09",
        "kind": "guide",
        "status": "official",
    },
    "djcara_radio": {
        "title": "GTA 6 Radio Songs List: Every Track Confirmed So Far",
        "publisher": "DJ Cara",
        "url": "https://djcara.com/blog/gta-6-radio-songs-list-every-track-confirmed-so-far/",
        "date": "2026-11-10",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "25yearslater_radio": {
        "title": "Rockstar Reveals Six GTA 6 Radio Stations and Their First 18 Songs",
        "publisher": "25 Years Later",
        "url": "https://25yearslatersite.com/gaming/news/rockstar-reveals-six-gta-6-radio-stations-and-their-first-18-songs/",
        "date": "2026-10-22",
        "kind": "presse (annonce du 08/10/2026)",
        "status": "official",
    },
    "soundtrackost_gta6": {
        "title": "GTA 6 Soundtrack (2026) — All The Songs in Grand Theft Auto VI",
        "publisher": "Soundtrack OST",
        "url": "https://soundtrackost.com/gta-6-all-the-songs/",
        "date": "2026-10-29",
        "kind": "base de données musicale",
        "status": "press_confirmed",
    },
    "kotaku_radio": {
        "title": "Here's Every Song And Radio Station Confirmed (So Far) In GTA 6",
        "publisher": "Kotaku",
        "url": "https://kotaku.com/every-song-and-radio-station-weve-spotted-in-the-gta-6-leaks-2000727661",
        "date": "2026-10-08",
        "kind": "presse",
        "status": "press_confirmed",
    },
    "gamesgg_radio": {
        "title": "GTA 6 Full Soundtrack: All Radio Stations & Songs",
        "publisher": "Games.gg",
        "url": "https://games.gg/grand-theft-auto-vi/guides/grand-theft-auto-6-all-previewed-radio-stations-songs/",
        "date": "2026-11-11",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "justjared_online": {
        "title": "GTA 6 Online Release Date: Will GTA 6 Have Multiplayer at Launch?",
        "publisher": "Just Jared",
        "url": "https://www.justjared.com/2026/11/17/gta-6-online-release-date-multiplayer-launch/",
        "date": "2026-11-17",
        "kind": "presse",
        "status": "official",
    },
    "gta6online_tracker": {
        "title": "GTA 6 Online Status and Release Date Tracker",
        "publisher": "TheGTA6Online",
        "url": "https://thegta6online.com/",
        "date": "2026-11-19",
        "kind": "tracker (statut par affirmation)",
        "status": "press_confirmed",
    },
    "upblazed_online": {
        "title": "Will GTA 6 Have Online Multiplayer? (Confirmed Facts)",
        "publisher": "Upblazed",
        "url": "https://upblazed.com/guides/gta-6-online-multiplayer",
        "date": "2026-09-10",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "webtech360_online": {
        "title": "GTA 6 Online: Preload Is Live, Multiplayer Still Unannounced",
        "publisher": "WebTech360",
        "url": "https://www.webtech360.com/detail/gta-6-online-what-we-know-about-multiplayer-as-of-en-trend-hp2-99916641.html",
        "date": "2026-11-11",
        "kind": "presse",
        "status": "press_confirmed",
    },
    "cheatcc_gta6": {
        "title": "GTA 6 Cheat Codes (November 2026): Will GTA 6 Have Cheats?",
        "publisher": "CheatCC",
        "url": "https://www.cheatcc.com/articles/gta-6-cheats/",
        "date": "2026-11-01",
        "kind": "référence triches",
        "status": "press_confirmed",
    },
    "allgta6cheats": {
        "title": "GTA 6 Cheat Codes for PS5, Xbox and PC: Full List (2026)",
        "publisher": "AllGTA6Cheats",
        "url": "https://allgta6cheats.com/",
        "date": "2026-10-18",
        "kind": "agrégateur de triches",
        "status": "speculative",
    },
    "gtacheatcodes_site": {
        "title": "GTA 6 Cheat Codes: All 35 PS5, Xbox, PC & Phone Cheats",
        "publisher": "GTACheat.codes",
        "url": "https://gtacheat.codes/",
        "date": "2026-09-09",
        "kind": "agrégateur de triches",
        "status": "speculative",
    },
    "allgta6cheatcodes_site": {
        "title": "GTA 6 Cheats and Cheat Codes for PS5, Xbox and PC (2026)",
        "publisher": "AllGTA6CheatCodes",
        "url": "https://allgta6cheatcodes.com/",
        "date": "2026-10-18",
        "kind": "agrégateur de triches",
        "status": "speculative",
    },
}

FACTS = {
    "soundtrack_and_radio": [
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "Six stations ont été présentées par Rockstar le 08/10/2026 sur le site officiel : Flash FM (pop, Robyn et Alex Consani), Cocoteo FM (Latin moderne, Bad Bunny en El Martillo et RaiNao en La Gata), Back Country Radio (country, Morgan Wallen en MW et Lana Del Rey en Delta Dawne), AfroBank FM (musiques africaines, Burna Boy et Palms Trax), The Chamber 106.6 (metal, Kerry King et Tom Araya de Slayer) et Dirty South Classics (rap du Sud, Trick Daddy et Trina).",
            "source_url": "https://25yearslatersite.com/gaming/news/rockstar-reveals-six-gta-6-radio-stations-and-their-first-18-songs/",
            "source_label": "Annonce Rockstar du 08/10/2026, relayée par 25 Years Later",
        },
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "Rockstar présente cette programmation comme « la sélection radio la plus vaste et la plus éclectique jamais proposée dans un jeu », et précise que d'autres stations existent, du rock classique aux émissions de débat.",
            "source_url": "https://thetechhacker.com/2026/11/16/gta-6-radio-stations-soundtrack-score/",
            "source_label": "The Tech Hacker, 16/11/2026",
        },
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "L'album officiel « Grand Theft Auto VI: The Album », réalisé avec Atlantic Records, compte 34 titres originaux et sort le 19/11/2026, le même jour que le jeu.",
            "source_url": "https://thetechhacker.com/2026/11/16/gta-6-radio-stations-soundtrack-score/",
            "source_label": "Annonce album Rockstar",
        },
        {
            "id": "MUS-XX",
            "status": "press_confirmed",
            "text": "Six singles de l'album sont déjà disponibles : « That's It » (Yung Lean feat. Future et Metro Boomin), « RHYNO » (Travis Scott, produit par Guy-Manuel de Homem-Christo), « Sexy Magic » (CA7RIEL et Paco Amoroso, PinkPantheress, Fred again.., Etienne de Crécy), « Last Thing You Need » (Morgan Wallen), « Macacoa 2000 » (Rauw Alejandro) et « Bright Lights, Big City » (Keith Richards).",
            "source_url": "https://soundtrackost.com/gta-6-all-the-songs/",
            "source_label": "Soundtrack OST / annonce album",
        },
        {
            "id": "MUS-XX",
            "status": "press_confirmed",
            "text": "La bande originale instrumentale, signée Justice, compte 30 pistes et sort séparément le 11/12/2026.",
            "source_url": "https://thetechhacker.com/2026/11/16/gta-6-radio-stations-soundtrack-score/",
            "source_label": "The Tech Hacker",
        },
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "Flash FM revient : Rockstar la qualifie d'« institution de Vice City ». Trois titres au moins sont confirmés — « Good Ones » de Charli xcx, « Electric Feel » de MGMT et « Midnight Sun (Girls Trip) » de Zara Larsson et PinkPantheress.",
            "source_url": "https://grandtheft.gg/gta-6-radio-stations/",
            "source_label": "Grand Theft, stations confirmées",
        },
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "The Chamber 106.6 est animée par Kerry King et Tom Araya de Slayer, et diffuse notamment « Raining Blood » de Slayer, « I'm Broken » de Pantera et « I » de Black Sabbath.",
            "source_url": "https://25yearslatersite.com/gaming/news/rockstar-reveals-six-gta-6-radio-stations-and-their-first-18-songs/",
            "source_label": "Rockstar, 08/10/2026",
        },
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "Dirty South Classics est animée par Trick Daddy et Trina, avec « Like A Pimp » de David Banner et Lil' Flip, « Who Dat » de JT Money et Solé, et « Born N Raised » de DJ Khaled avec Trick Daddy, Rick Ross et Pitbull.",
            "source_url": "https://djcara.com/blog/gta-6-radio-songs-list-every-track-confirmed-so-far/",
            "source_label": "DJ Cara, liste des titres confirmés",
        },
        {
            "id": "MUS-XX",
            "status": "press_confirmed",
            "text": "Back Country Radio diffuse notamment « Rhinestone Cowboy » de Glen Campbell, « The Fireman » de George Strait, « Need a Little Time Off for Bad Behavior » de David Allan Coe, « Don't Come Home A-Drinkin' » de Loretta Lynn et « The Conversation » de Hank Williams Jr. et Waylon Jennings. Un reporter itinérant, Mud Dog Mike, intervient depuis son hydroglisseur dans les Grassrivers.",
            "source_url": "https://djcara.com/blog/gta-6-radio-songs-list-every-track-confirmed-so-far/",
            "source_label": "DJ Cara",
        },
        {
            "id": "MUS-XX",
            "status": "press_confirmed",
            "text": "Cocoteo FM couvre bachata, merengue, dembow et reggaeton, avec « EoO » de Bad Bunny, « Canalla » de Romeo Santos et El Chaval de la Bachata, « Si Es Trucho Es Trucho (Remix) » d'Axel Rulay avec Farruko et El Alfa, et « Girl » de Myke Towers.",
            "source_url": "https://djcara.com/blog/gta-6-radio-songs-list-every-track-confirmed-so-far/",
            "source_label": "DJ Cara",
        },
        {
            "id": "MUS-XX",
            "status": "press_confirmed",
            "text": "AfroBank FM va des classiques africains du XXe siècle à l'amapiano et au 3-step, avec « Joha » d'Asake, « Gye Wani » de Pat Thomas avec Ebo Taylor et « Shay'sana » de DJ Lag et Robot Boii avec Kamo Mphela.",
            "source_url": "https://25yearslatersite.com/gaming/news/rockstar-reveals-six-gta-6-radio-stations-and-their-first-18-songs/",
            "source_label": "Rockstar, 08/10/2026",
        },
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "Le jeu permet d'écouter la radio à pied, au casque, et propose des podcasts à la demande — une première dans la série.",
            "source_url": "https://thetechhacker.com/2026/11/16/gta-6-radio-stations-soundtrack-score/",
            "source_label": "The Tech Hacker",
        },
        {
            "id": "MUS-XX",
            "status": "official",
            "text": "Trailer 1 est intégralement monté sur « Love Is a Long Road » de Tom Petty (1989). Trailer 2 utilise six titres, dont « Hot Together » des Pointer Sisters et « Thunder Island » de Jay Ferguson.",
            "source_url": "https://kotaku.com/every-song-and-radio-station-weve-spotted-in-the-gta-6-leaks-2000727661",
            "source_label": "Kotaku, relevé des trailers",
        },
        {
            "id": "MUS-XX",
            "status": "community",
            "text": "Des noms de stations non confirmés circulent depuis des fuites (Kaleidoscope FM, Worldwide FM, Emotion 98.3, Radio ON-U, Symphony FM, Stockyard FM, CircoLoco Records Radio, The Wipe, La Ola, V-Rock). Quatre des treize noms de la fuite ont depuis été officialisés, les autres non.",
            "source_url": "https://djcara.com/blog/gta-6-radio-songs-list-every-track-confirmed-so-far/",
            "source_label": "DJ Cara / Red Bull — liste de fuite non confirmée",
        },
        {
            "id": "MUS-XX",
            "status": "post_launch_pending",
            "text": "Rockstar n'a pas annoncé publiquement la liste complète des stations ni la tracklist intégrale avant le lancement. Pour situer : GTA V comptait plus de 240 morceaux sur 17 stations au lancement.",
            "source_url": "https://djcara.com/blog/gta-6-radio-songs-list-every-track-confirmed-so-far/",
            "source_label": "DJ Cara (citant Red Bull)",
        },
    ],
    "online": [
        {
            "id": "ONL-XX",
            "status": "official",
            "text": "GTA VI sort le 19/11/2026 comme jeu strictement solo : Rockstar et Take-Two le décrivent comme une « expérience solo », et la fiche PlayStation indique un joueur, avec jeu hors ligne activé.",
            "source_url": "https://www.justjared.com/2026/11/17/gta-6-online-release-date-multiplayer-launch/",
            "source_label": "Just Jared, 17/11/2026 (fiches officielles PlayStation / Rockstar)",
        },
        {
            "id": "ONL-XX",
            "status": "official",
            "text": "Aucun mode en ligne, aucune coopération et aucun multijoueur n'a été annoncé pour GTA VI, ni au lancement ni après. Aucun nom, aucune date, aucune révélation.",
            "source_url": "https://upblazed.com/guides/gta-6-online-multiplayer",
            "source_label": "Upblazed — état des annonces",
        },
        {
            "id": "ONL-XX",
            "status": "official",
            "text": "Take-Two a confirmé que le GTA Online actuel (celui de GTA V) continuera d'être alimenté en contenu et en événements après la sortie de GTA VI.",
            "source_url": "https://www.justjared.com/2026/11/17/gta-6-online-release-date-multiplayer-launch/",
            "source_label": "Just Jared / Take-Two",
        },
        {
            "id": "ONL-XX",
            "status": "community",
            "text": "Le PDG de Twitch, Dan Clancy, a déclaré en septembre 2026 qu'il s'attend à un multijoueur « l'année prochaine », soit 2027. Il s'agit d'une anticipation de partenaire, pas d'une annonce de Rockstar.",
            "source_url": "https://www.justjared.com/2026/11/17/gta-6-online-release-date-multiplayer-launch/",
            "source_label": "Dan Clancy (Twitch) via Bloomberg, relayé par Just Jared",
        },
        {
            "id": "ONL-XX",
            "status": "community",
            "text": "Une fenêtre de décembre 2026 circule, attribuée à un leaker ayant un historique correct sur d'autres jeux. Rockstar n'a ni confirmé ni infirmé.",
            "source_url": "https://upblazed.com/guides/gta-6-online-multiplayer",
            "source_label": "Upblazed — rumeur explicitement non confirmée",
        },
        {
            "id": "ONL-XX",
            "status": "post_launch_pending",
            "text": "Aucune information sur le transfert de progression, d'argent ou d'achats depuis GTA Online, ni sur le cross-play, ni sur un modèle économique pour un futur mode en ligne.",
            "source_url": "https://upblazed.com/guides/gta-6-online-multiplayer",
            "source_label": "Upblazed",
        },
        {
            "id": "ONL-XX",
            "status": "official",
            "text": "Le préchargement numérique a ouvert le 10/11/2026. Rockstar confirme aussi l'accès via Xbox Cloud Gaming sur consoles compatibles et la prise en charge du Remote Play — deux fonctions de diffusion, qui ne constituent en rien un multijoueur.",
            "source_url": "https://www.webtech360.com/detail/gta-6-online-what-we-know-about-multiplayer-as-of-en-trend-hp2-99916641.html",
            "source_label": "WebTech360, 11/11/2026",
        },
        {
            "id": "ONL-XX",
            "status": "official",
            "text": "Les précommandes numériques éligibles donnent un mois de GTA+ offert ; l'abonnement se renouvelle ensuite au tarif mensuel normal sauf résiliation. Cette offre ne donne aucun accès à un mode multijoueur.",
            "source_url": "https://www.justjared.com/2026/11/17/gta-6-online-release-date-multiplayer-launch/",
            "source_label": "Just Jared",
        },
        {
            "id": "ONL-XX",
            "status": "press_confirmed",
            "text": "Aucune version PC n'est annoncée pour le lancement : le jeu sort sur PS5 et Xbox Series X|S, et les copies physiques contiennent un code de téléchargement plutôt qu'un disque.",
            "source_url": "https://neonsect.com/gta-6/gta-6-online-launch/",
            "source_label": "Neonsect",
        },
    ],
    "cheats": [
        {
            "id": "CHE-XX",
            "status": "official",
            "text": "Au 18/11/2026, Rockstar n'a publié aucun code de triche, aucune combinaison de manettes et aucun numéro de téléphone pour GTA VI. Le compte officiel est zéro.",
            "source_url": "https://www.cheatcc.com/articles/gta-6-cheats/",
            "source_label": "CheatCC, 01/11/2026",
        },
        {
            "id": "CHE-XX",
            "status": "post_launch_pending",
            "text": "Tous les jeux GTA principaux depuis GTA III ont comporté des triches : il est probable que GTA VI en ait aussi, mais rien n'est confirmé et la nature du système (codes, téléphone, menu) n'est pas connue.",
            "source_url": "https://www.cheatcc.com/articles/gta-6-cheats/",
            "source_label": "CheatCC",
        },
        {
            "id": "CHE-XX",
            "status": "speculative",
            "text": "Les listes qui circulent et présentent des combinaisons PS5/Xbox ou des numéros 1-999 pour GTA VI recopient en réalité les codes de GTA V. Elles ne sont adossées à aucune source Rockstar et sont à traiter comme des prédictions.",
            "source_url": "https://allgta6cheats.com/",
            "source_label": "AllGTA6Cheats — liste présentée sans source primaire",
        },
        {
            "id": "CHE-XX",
            "status": "speculative",
            "text": "Exemples de codes GTA V fréquemment re-étiquetés « GTA 6 » : 1-999-724-654-5537 (PAINKILLER, invincibilité temporaire), 1-999-887-853 (TURTLE, santé et armure maximales), 1-999-866-587 (TOOLUP, armes et munitions), 1-999-529-93787 (LAWYERUP, une étoile de moins), 1-999-384-48483 (FUGITIVE, une étoile de plus).",
            "source_url": "https://allgta6cheatcodes.com/",
            "source_label": "AllGTA6CheatCodes / CheatCC — codes d'origine GTA V",
        },
        {
            "id": "CHE-XX",
            "status": "post_launch_pending",
            "text": "Le format d'entrée des codes dans GTA VI n'est pas documenté. Dans GTA V, la méthode était un numéro à composer depuis le téléphone in-game (préfixe 1-999) ou une commande saisie au clavier sur PC. Rien n'indique que ce format soit conservé.",
            "source_url": "https://www.cheatcc.com/articles/gta-6-cheats/",
            "source_label": "CheatCC",
        },
        {
            "id": "CHE-XX",
            "status": "post_launch_pending",
            "text": "Les conséquences classiques des triches (désactivation des trophées et succès, sauvegarde marquée) n'ont pas été confirmées pour GTA VI. Dans GTA V, activer une triche bloquait les trophées de la session.",
            "source_url": "https://www.cheatcc.com/articles/gta-6-cheats/",
            "source_label": "CheatCC",
        },
    ],
}


def _renumber(data: dict) -> None:
    facts = data.get("facts", {})
    prefix = {"soundtrack_and_radio": "MUS", "online": "ONL", "cheats": "CHE"}
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
    g5 = amend.setdefault("g5", {})

    if g5.get("marker") == MARKER:
        print("research_data.json : déjà patché en S4/G5 — aucune duplication.")
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
                "added_in": "S4_G5",
            })
            added_facts += 1

    g5.update({
        "marker": MARKER,
        "at": "2026-11-18",
        "pages": [
            "pages/musique/index.html",
            "pages/online/index.html",
            "pages/codes/index.html",
        ],
        "facts_added": added_facts,
        "sources_added": added_src,
        "ids": {s: [f["id"] for f in items] for s, items in FACTS.items()},
        "policy": "Aucun code de triche publié : 0 code officiel au 18/11/2026.",
    })

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in facts.values())
    print(f"Amendement S4/G5 appliqué : +{added_facts} faits, +{added_src} sources, "
          f"{total} faits au total, {len(sources)} sources enregistrées.")


if __name__ == "__main__":
    main()
