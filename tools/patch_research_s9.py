#!/usr/bin/env python3
"""Amendement recherche S9 — LAUNCH_NIGHT (retours joueurs et technique mesurée).

Marqueur `s9_amendment.marker == "S9_LAUNCH_NIGHT_VERIFIED"`. Idempotent.

Deux apports majeurs par rapport à S8 :
  • l'analyse Digital Foundry porte désormais sur la **version commerciale**,
    consoles Xbox incluses (Series S à ~720p, Series X ~1440p, chutes à ~20 fps) ;
  • les retours joueurs de la première nuit (déblocage néo-zélandais, astuce du
    changement de région, préchargement, scores utilisateurs et leur calendrier).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S9_LAUNCH_NIGHT_VERIFIED"

SOURCES = {
    "df_xbox_series": {
        "title": "GTA 6 Runs at 1440p and 30 FPS on Xbox Series X, While Series S Struggles at 720p",
        "publisher": "TwistedVoxel (analyse Digital Foundry)",
        "url": "https://twistedvoxel.com/gta-6-xbox-series-x-vs-series-s-performance/",
        "date": "2026-11-18",
        "kind": "presse (analyse technique)",
        "status": "press_confirmed",
    },
    "df_xbox_drops": {
        "title": "GTA VI runs slightly worse on Xbox Series X than PS5 in heavy action, dropping to around 20fps",
        "publisher": "AltChar (analyse Digital Foundry)",
        "url": "https://www.altchar.com/game-news/gta-vi-runs-slightly-worse-on-xbox-series-x-than-ps5-in-heavy-action-dropping-to-around-20fps-a82743n2RfEW",
        "date": "2026-11-18",
        "kind": "presse (analyse technique)",
        "status": "press_confirmed",
    },
    "reddit_nz_trick": {
        "title": "So the New Zealand trick is not working for GTA 6? (r/xbox)",
        "publisher": "Reddit · r/xbox",
        "url": "https://www.reddit.com/r/xbox/comments/1xw6xl0/so_the_new_zealand_trick_is_not_working_for_gta_6/",
        "date": "2026-11-14",
        "kind": "forum",
        "status": "community",
    },
    "reddit_preload_bugs": {
        "title": "Pre-load FAQ's and Bugs (r/GTA6)",
        "publisher": "Reddit · r/GTA6",
        "url": "https://www.reddit.com/r/GTA6/comments/1xr3uqg/preload_faqs_and_bugs/",
        "date": "2026-11-10",
        "kind": "forum",
        "status": "community",
    },
    "reddit_first_hours": {
        "title": "What's the first thing you are doing as soon as you load into GTA 6? (r/GTA)",
        "publisher": "Reddit · r/GTA",
        "url": "https://www.reddit.com/r/GTA/comments/1uop7wq/whats_the_first_thing_you_are_doing_as_soon_as/",
        "date": "2026-07-06",
        "kind": "forum",
        "status": "community",
    },
    "gulfnews_nz": {
        "title": "GTA 6 early reviews set internet on fire: first driving clips, 99 Metacritic claim",
        "publisher": "Gulf News",
        "url": "https://gulfnews.com/technology/gaming/gta-6-early-reviews-set-internet-alight-first-driving-clips-99-metacritic-claim-fuel-unprecedented-hype-1.500752451",
        "date": "2026-11-18",
        "kind": "presse",
        "status": "press_confirmed",
    },
    "churchofnerds_user_scores": {
        "title": "GTA 6 Reviews Roundup: Metacritic Score and What Critics Say — calendrier des notes utilisateurs",
        "publisher": "Church of Nerds",
        "url": "https://www.churchofnerds.com/blogs/news/gta-6-reviews-roundup-metacritic-score",
        "date": "2026-11-18",
        "kind": "presse",
        "status": "press_confirmed",
    },
    "outputlag_roundup": {
        "title": "GTA 6 review roundup: 99 on Metacritic, and not a single mixed or negative review",
        "publisher": "Output Lag",
        "url": "https://outputlag.com/news/gta-6-review-roundup/",
        "date": "2026-11-18",
        "kind": "presse (synthèse de 18 tests)",
        "status": "press_confirmed",
    },
}

FACTS = {
    "press_reviews": [
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Digital Foundry a mesuré la version commerciale sur Xbox Series X : environ 1440p interne, 33 ms stables en jeu courant, mais des chutes à 21 fps dans une fusillade avec la police et jusqu'à environ 20 fps dans le pire cas — légèrement en dessous de la PS5, testée à 23 fps dans une scène comparable.",
            "source_url": "https://www.altchar.com/game-news/gta-vi-runs-slightly-worse-on-xbox-series-x-than-ps5-in-heavy-action-dropping-to-around-20fps-a82743n2RfEW",
            "source_label": "Digital Foundry via AltChar, 18/11/2026",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Xbox Series S : environ 720p interne, éclairage moins précis, reflets plus doux, ombres et nuages de moindre résolution, eau plus plate et pop-in plus visible. Selon Digital Foundry, l'image finale reste meilleure que ce que 720p suggère, mais l'écart avec la Series X est important.",
            "source_url": "https://twistedvoxel.com/gta-6-xbox-series-x-vs-series-s-performance/",
            "source_label": "Digital Foundry via TwistedVoxel, 18/11/2026",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Deux points techniques rassurants sur Series X : le VRR en sortie 120 Hz lisse les chutes, et la latence mesurée tourne autour de 180 ms — comparable aux autres jeux Rockstar à 30 fps. Les cinématiques ne souffrent plus du tremblement d'animation qui affectait le moteur RAGE depuis des années.",
            "source_url": "https://www.altchar.com/game-news/gta-vi-runs-slightly-worse-on-xbox-series-x-than-ps5-in-heavy-action-dropping-to-around-20fps-a82743n2RfEW",
            "source_label": "Digital Foundry via AltChar",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Sur Xbox Series X, l'illumination globale et les reflets sont bien calculés par ray tracing, mais les ombres restent des shadow maps classiques : les ombres ray-tracées demeurent l'exclusivité de la PS5 Pro.",
            "source_url": "https://twistedvoxel.com/gta-6-xbox-series-x-vs-series-s-performance/",
            "source_label": "Digital Foundry via TwistedVoxel",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Metacritic n'ouvre les notes utilisateurs que 36 heures après le lancement : le premier score public ne peut donc pas apparaître avant le vendredi 20 novembre. Les « 6,5 sur 5 votes » qui ont circulé avant la sortie étaient des notes fabriquées, retirées depuis.",
            "source_url": "https://www.churchofnerds.com/blogs/news/gta-6-reviews-roundup-metacritic-score",
            "source_label": "Metacritic via Church of Nerds / Gadgets Now",
        },
        {
            "id": "REV-XX",
            "status": "press_confirmed",
            "text": "Sur 18 tests dépouillés par une synthèse indépendante : les 18 saluent le monde lui-même, 16 sur 18 citent Jason et Lucia comme la meilleure carte du jeu, et deux réserves reviennent — la courbe d'apprentissage du réalisme (voitures fragiles, factures de réparation, corvées quotidiennes) pour qui arrive de GTA V, et l'absence de mode 60 fps.",
            "source_url": "https://outputlag.com/news/gta-6-review-roundup/",
            "source_label": "Output Lag — dépouillement de 18 tests",
        },
    ],
    "release_and_platforms": [
        {
            "id": "REL-XX",
            "status": "press_confirmed",
            "text": "La première ouverture réelle a eu lieu en Nouvelle-Zélande le 18 novembre à 11:00 UTC. Les premiers extraits publiés par des joueurs néo-zélandais montrent la conduite de nuit et la circulation ; une streameuse locale l'a décrit comme « un festin visuel ».",
            "source_url": "https://gulfnews.com/technology/gaming/gta-6-early-reviews-set-internet-alight-first-driving-clips-99-metacritic-claim-fuel-unprecedented-hype-1.500752451",
            "source_label": "Gulf News / NZ Herald, 18/11/2026",
        },
        {
            "id": "REL-XX",
            "status": "community",
            "text": "L'« astuce néo-zélandaise » : sur Xbox, changer la région de la console dans les réglages suffit à avancer l'heure de déblocage, et le jeu démarre avec votre propre version. Sur PS5, cela ne fonctionne pas : il faut un compte PSN néo-zélandais et un achat sur ce store, donc payer deux fois.",
            "source_url": "https://www.reddit.com/r/xbox/comments/1xw6xl0/so_the_new_zealand_trick_is_not_working_for_gta_6/",
            "source_label": "Reddit r/xbox / GamesRadar",
        },
        {
            "id": "REL-XX",
            "status": "community",
            "text": "Bug de préchargement documenté sur Xbox : le téléchargement affiche bien environ 200 Go puis se termine sur un fichier de quelques centaines de Mo. Plusieurs joueurs ont dû supprimer et relancer l'installation ; d'autres signalent qu'un changement de région suivi d'une visite au store propose une seconde installation complète.",
            "source_url": "https://www.reddit.com/r/GTA6/comments/1xr3uqg/preload_faqs_and_bugs/",
            "source_label": "Reddit r/GTA6",
        },
        {
            "id": "REL-XX",
            "status": "community",
            "text": "Rumeurs de comptes PSN néo-zélandais suspendus après usage de l'astuce : aucune confirmation de Sony ni de Rockstar au 18/11. À traiter comme non vérifié, pas comme un fait.",
            "source_url": "https://gulfnews.com/technology/gaming/gta-6-early-reviews-set-internet-alight-first-driving-clips-99-metacritic-claim-fuel-unprecedented-hype-1.500752451",
            "source_label": "Gulf News (aucune confirmation officielle)",
        },
    ],
    "tips_strategies_techniques": [
        {
            "id": "TIP-XX",
            "status": "community",
            "text": "Consensus des forums sur les premières heures : ne pas traverser la carte d'emblée. Explorer à pied le quartier de départ, écouter la radio en roulant, entrer dans deux ou trois intérieurs, puis enchaîner quelques missions avant de partir en exploration libre.",
            "source_url": "https://www.reddit.com/r/GTA/comments/1uop7wq/whats_the_first_thing_you_are_doing_as_soon_as/",
            "source_label": "Reddit r/GTA (fil de 2026)",
        },
        {
            "id": "TIP-XX",
            "status": "community",
            "text": "Deux réflexes de réglages cités en boucle par les joueurs : couper le flou de mouvement et le grain de film dès le premier menu, et vérifier la luminosité HDR avant de juger le rendu nocturne.",
            "source_url": "https://www.reddit.com/r/GTA/comments/1uop7wq/whats_the_first_thing_you_are_doing_as_soon_as/",
            "source_label": "Reddit r/GTA",
        },
        {
            "id": "TIP-XX",
            "status": "community",
            "text": "Protection anti-spoiler la plus citée : la fenêtre dangereuse va de l'ouverture néo-zélandaise (11:00 UTC le 18) à minuit local, soit environ douze heures. Les mesures efficaces : couper les mots-masqués sur X et TikTok, quitter les fils d'actualité, éviter les titres de vidéos YouTube.",
            "source_url": "https://gulfnews.com/technology/gaming/gta-6-early-reviews-set-internet-alight-first-driving-clips-99-metacritic-claim-fuel-unprecedented-hype-1.500752451",
            "source_label": "Gulf News / guides anti-spoiler",
        },
    ],
}


def _renumber(data: dict) -> None:
    facts = data.get("facts", {})
    prefix = {"press_reviews": "REV", "release_and_platforms": "REL", "tips_strategies_techniques": "TIP"}
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
    if data.get("s9_amendment", {}).get("marker") == MARKER:
        print("research_data.json : déjà patché en S9 — aucune duplication.")
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
                "added_in": "S9",
            })
            added += 1

    data["s9_amendment"] = {
        "marker": MARKER,
        "at": "2026-11-18T15:30:00Z",
        "event": "Première nuit de lancement (NZ) + analyse Digital Foundry des versions retail Xbox",
        "facts_added": added,
        "sources_added": added_src,
        "ids": {s: [f["id"] for f in items] for s, items in FACTS.items()},
        "specs": {"series_x": "~1440p, 30 fps stable, chutes ~20 fps en combat dense, VRR 120 Hz",
                  "series_s": "~720p, sous 30 fps fréquemment",
                  "ps5": "1440p, chutes 23 fps mesurées",
                  "user_scores": "Metacritic ouvre les notes utilisateurs 36 h après le lancement"},
        "policy": "Astuce NZ, bugs de préchargement et suspensions de comptes = community / non vérifié. Aucune spéculation sur le contenu du jeu.",
    }

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in facts.values())
    print(f"Amendement S9 appliqué : +{added} faits, +{added_src} sources, {total} faits, {len(sources)} sources.")


if __name__ == "__main__":
    main()
