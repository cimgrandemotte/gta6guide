#!/usr/bin/env python3
"""Amendement recherche S4 / groupe G7 — Outils & social, Divers, FAQ.

Idempotent : marqueur `s4_amendments.g7.marker == "S4_G7_VERIFIED_FACTS"`.

Ce dernier groupe ferme S4. Il couvre trois terrains :
  • les outils communautaires et les créateurs (GitHub, Discord, YouTube, Reddit) ;
  • la page « Divers » (identité visuelle, Leonida, ambiance) ;
  • la FAQ technique (plateformes, prix, préchargement, performances 30 fps).

Aucune donnée de performance n'est inventée : les chiffres 30 fps / 1440p / PSSR
viennent de la Newswire Rockstar du 10/11/2026 et de l'analyse Digital Foundry.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S4_G7_VERIFIED_FACTS"

SOURCES = {
    "github_vorxeo_companion": {
        "title": "gta6-companion — GTA 6 Companion Platform (carte interactive, tracker 100 %, planificateur)",
        "publisher": "GitHub · Vorxeo",
        "url": "https://github.com/Vorxeo/gta6-companion",
        "date": "2026-11",
        "kind": "dépôt GitHub (projet fan)",
        "status": "community",
    },
    "github_topic_companion": {
        "title": "GitHub Topics · companion-app (dont rookdex, companion GTA VI)",
        "publisher": "GitHub",
        "url": "https://github.com/topics/companion-app?o=desc&s=updated",
        "date": "2026-11-06",
        "kind": "index de dépôts",
        "status": "community",
    },
    "sixstar_games": {
        "title": "SIXSTAR — GTA 6 Companion: Interactive Map & 100% Tracker",
        "publisher": "SIXSTAR",
        "url": "https://sixstar.games/",
        "date": "2026-11",
        "kind": "outil web communautaire",
        "status": "community",
    },
    "gtahub_wanted": {
        "title": "Wanted — GTA 6 Companion App for iPhone & Android",
        "publisher": "GTA Hub · Wanted",
        "url": "https://gtahub.app/",
        "date": "2026-11",
        "kind": "application mobile fan",
        "status": "community",
    },
    "play_countdown": {
        "title": "Companion & Countdown: GTA 6 (Google Play)",
        "publisher": "Google Play",
        "url": "https://play.google.com/store/apps/details?id=com.gtavicountdown.app",
        "date": "2026-11-04",
        "kind": "application mobile fan",
        "status": "community",
    },
    "gta6hype_creators": {
        "title": "Best GTA Content Creators: The Biggest Channels, Ranked",
        "publisher": "GTA6 Hype",
        "url": "https://www.gta6hype.com/blog/best-gta6-content-creators/",
        "date": "2026-09-16",
        "kind": "panorama de chaînes YouTube",
        "status": "community",
    },
    "gta6everything_youtube": {
        "title": "GTA YouTubers: the best-known GTA 5 and GTA 6 channels in 2026",
        "publisher": "GTA6 Everything",
        "url": "https://www.gta6everything.com/creators/youtube",
        "date": "2026-10-22",
        "kind": "annuaire de créateurs",
        "status": "community",
    },
    "reddit_youtubers": {
        "title": "What YouTubers do you recommend for GTA 6 coverage? (r/GTA6)",
        "publisher": "Reddit · r/GTA6",
        "url": "https://www.reddit.com/r/GTA6/comments/1uuxta2/what_youtubers_do_you_recommend_for_gta_6_coverage/",
        "date": "2026-07-13",
        "kind": "forum",
        "status": "community",
    },
    "timesaver_fps": {
        "title": "GTA 6 FPS Confirmed: 30 on Every Console, Even PS5 Pro",
        "publisher": "TimeSaver",
        "url": "https://timesaver.gg/blog/gta-6-60fps-performance-mode-ps5-xbox",
        "date": "2026-11-10",
        "kind": "synthèse Newswire",
        "status": "official",
    },
    "altchar_digitalfoundry": {
        "title": "GTA VI dips as low as 23fps on base PS5 in heavy action, Digital Foundry finds",
        "publisher": "AltChar",
        "url": "https://www.altchar.com/game-news/gta-vi-dips-as-low-as-23fps-on-base-ps5-in-heavy-action-digital-foundry-finds-aJybE7x7IsZa",
        "date": "2026-11-18",
        "kind": "presse (analyse technique)",
        "status": "press_confirmed",
    },
    "vgtimes_digitalfoundry": {
        "title": "Ray Tracing, Realistic Physics, and 30 FPS: Digital Foundry Takes a Technical Deep Dive Into GTA 6",
        "publisher": "VGTimes",
        "url": "https://vgtimes.com/gaming-news/175004-ray-tracing-realistic-physics-and-30-fps-digital-foundry-takes-a-technical-deep-dive-into-gta-6.html",
        "date": "2026-11-18",
        "kind": "presse (analyse technique)",
        "status": "press_confirmed",
    },
    "gamertagmythras_faq": {
        "title": "GTA 6: Everything We Know Before the November 19 Launch",
        "publisher": "Gamertag Mythras",
        "url": "https://gamertagmythras.com/blog/gta-6/gta-6-everything-we-know",
        "date": "2026-11-14",
        "kind": "FAQ de lancement",
        "status": "official",
    },
    "leonidaverse_editions": {
        "title": "GTA 6 Standard vs Ultimate: Differences, $79.99 vs $99.99",
        "publisher": "Leonida Verse",
        "url": "https://leonidaverse.com/en/faq/gta-6-editions",
        "date": "2026-11-05",
        "kind": "FAQ éditions",
        "status": "official",
    },
    "gamenewsplus_faq": {
        "title": "GTA 6 Release Date, Price, Platforms & PC Status",
        "publisher": "GameNewsPlus",
        "url": "https://gamenewsplus.net/news/gta-6-release-date-price-platforms-pc-version-everything-we-know-38767/",
        "date": "2026-11-04",
        "kind": "FAQ",
        "status": "press_confirmed",
    },
    "realdigitaltech_faq": {
        "title": "GTA 6 release date, price and editions: everything to know before November 19",
        "publisher": "Real Digital Tech",
        "url": "https://realdigitaltech.com/articles/gta-6-release-guide/",
        "date": "2026-10-17",
        "kind": "FAQ",
        "status": "press_confirmed",
    },
}

FACTS = {
    "community_tools_and_social": [
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "SIXSTAR est un outil web communautaire : carte interactive de Leonida plus suivi de complétion 100 %, conçu pour être utilisé sur téléphone pendant qu'on joue sur console. Il se présente explicitement comme un projet de fans, non affilié à Rockstar.",
            "source_url": "https://sixstar.games/",
            "source_label": "SIXSTAR, page publique du projet",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Sur GitHub, plusieurs dépôts de compagnons GTA VI existent, dont « gta6-companion » (carte interactive, tracker 100 %, planificateur de session, simulateur d'économie) et « rookdex » (compte à rebours, tracker, état des informations confirmées, sans compte).",
            "source_url": "https://github.com/Vorxeo/gta6-companion",
            "source_label": "GitHub · Vorxeo/gta6-companion et topic companion-app",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Côté mobile, des applications fan existent déjà : « Wanted » (profils de personnages, carte communautaire, véhicules, missions) et « Companion & Countdown » (compte à rebours, widgets, carte de Vice City, dossiers de personnages). Aucune n'est officielle.",
            "source_url": "https://gtahub.app/",
            "source_label": "GTA Hub · Wanted / Google Play · Companion & Countdown",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Aucun de ces outils ne peut être complet au lancement : leurs cartes et leurs bases de collectibles se remplissent avec les découvertes des joueurs. La qualité d'un tracker se juge donc à sa fraîcheur, pas à sa promesse.",
            "source_url": "https://sixstar.games/",
            "source_label": "SIXSTAR — carte communautaire en temps réel",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Chaînes YouTube les plus suivies pour GTA (tous jeux confondus) : Nought (~8,05 M), SpeirsTheAmazingHD (~5,54 M), GTA Series Videos (~4,13 M), Onespot Gaming (~3,57 M), MrBossFTW (~3,19 M), Treyten (~3,04 M), DarkViperAU (~2,31 M), TGG (~2,24 M).",
            "source_url": "https://www.gta6hype.com/blog/best-gta6-content-creators/",
            "source_label": "GTA6 Hype, relevé des pages de chaînes",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Répartition par usage : GTA Series Videos pour les walkthroughs propres et les trailers officiels, MrBossFTW pour le volume d'actualité quotidienne, Onespot Gaming pour le détail véhicules et graphismes, DarkViperAU pour l'analyse (speedrun, run pacifiste), Digital Foundry pour la technique, TGG et GTA VI O'Clock pour l'actualité GTA VI.",
            "source_url": "https://www.gta6hype.com/blog/best-gta6-content-creators/",
            "source_label": "GTA6 Hype",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Consensus de r/GTA6 sur les créateurs à suivre : privilégier ceux qui font de la vérification plutôt que du volume. Les noms qui reviennent le plus sont TGG, GTA VI O'Clock, Sav, Badger Goodger, DarkViperAU et GTA Series Videos ; les chaînes de « slop » quotidien sont explicitement écartées.",
            "source_url": "https://www.reddit.com/r/GTA6/comments/1uuxta2/what_youtubers_do_you_recommend_for_gta_6_coverage/",
            "source_label": "Reddit r/GTA6",
        },
        {
            "id": "OUT-XX",
            "status": "community",
            "text": "Bonne pratique de lecture : une chaîne qui publie plusieurs vidéos par jour sur un jeu à peine sorti produit surtout du commentaire, pas de la vérification. Croiser systématiquement avec une source écrite datée.",
            "source_url": "https://www.reddit.com/r/GTA6/comments/1uuxta2/what_youtubers_do_you_recommend_for_gta_6_coverage/",
            "source_label": "Reddit r/GTA6 (synthèse des recommandations)",
        },
    ],
    "visual_identity_and_art_direction": [
        {
            "id": "DIV-XX",
            "status": "press_confirmed",
            "text": "Digital Foundry qualifie GTA VI de « jeu le plus visuellement marquant de la génération », avec un rendu interne de 1440p sur PS5 comme sur PS5 Pro, la différence se faisant à l'upscaling (PSSR sur Pro).",
            "source_url": "https://www.altchar.com/game-news/gta-vi-dips-as-low-as-23fps-on-base-ps5-in-heavy-action-digital-foundry-finds-aJybE7x7IsZa",
            "source_label": "Digital Foundry via AltChar, 18/11/2026",
        },
        {
            "id": "DIV-XX",
            "status": "press_confirmed",
            "text": "Le jeu utilise le ray tracing pour l'illumination globale et les reflets sur les deux consoles ; les ombres ray-tracées sont réservées à la PS5 Pro. Digital Foundry parle de l'une des meilleures implémentations vues à ce jour.",
            "source_url": "https://vgtimes.com/gaming-news/175004-ray-tracing-realistic-physics-and-30-fps-digital-foundry-takes-a-technical-deep-dive-into-gta-6.html",
            "source_label": "Digital Foundry via VGTimes",
        },
        {
            "id": "DIV-XX",
            "status": "press_confirmed",
            "text": "Chaque personnage, PNJ compris, utilise un système de cheveux à mèches simulées physiquement qui réagissent au vent, au mouvement et à l'immersion dans l'eau — l'un des postes de coût rendant un mode 60 fps irréalisable sur ces consoles.",
            "source_url": "https://vgtimes.com/gaming-news/175004-ray-tracing-realistic-physics-and-30-fps-digital-foundry-takes-a-technical-deep-dive-into-gta-6.html",
            "source_label": "Digital Foundry via VGTimes",
        },
        {
            "id": "DIV-XX",
            "status": "press_confirmed",
            "text": "Le HDR prend en charge des pics spéculaires dépassant 1 500 nits, ce qui place le rendu des néons et des reflets largement au-dessus des standards habituels.",
            "source_url": "https://vgtimes.com/gaming-news/175004-ray-tracing-realistic-physics-and-30-fps-digital-foundry-takes-a-technical-deep-dive-into-gta-6.html",
            "source_label": "Digital Foundry via VGTimes",
        },
        {
            "id": "DIV-XX",
            "status": "press_confirmed",
            "text": "L'architecture des quartiers, les infrastructures routières et la disposition générale sont jugées remarquablement crédibles par l'analyse technique, au point que la ville se lit comme une vraie ville plutôt qu'un décor de jeu.",
            "source_url": "https://vgtimes.com/gaming-news/175004-ray-tracing-realistic-physics-and-30-fps-digital-foundry-takes-a-technical-deep-dive-into-gta-6.html",
            "source_label": "Digital Foundry via VGTimes",
        },
    ],
    "unavailable_post_launch": [
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "Date de sortie : jeudi 19 novembre 2026. Rockstar a fixé cette date le 6 novembre 2025 après un premier report à mai 2026 ; elle était toujours officielle au 14 novembre 2026.",
            "source_url": "https://gamertagmythras.com/blog/gta-6/gta-6-everything-we-know",
            "source_label": "Rockstar Newswire, synthèse du 14/11/2026",
        },
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "Plateformes : PlayStation 5 (améliorée sur PS5 Pro) et Xbox Series X|S. Aucune version PS4, Xbox One, Switch 2 ni PC n'est annoncée.",
            "source_url": "https://gamenewsplus.net/news/gta-6-release-date-price-platforms-pc-version-everything-we-know-38767/",
            "source_label": "GameNewsPlus, état des annonces",
        },
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "Prix : 79,99 $ l'édition Standard (79,99 € en France), 99,99 $ l'édition Ultimate (99,99 €), soit 20 $ de plus. Une mise à niveau Ultimate existe séparément, à environ 20 $.",
            "source_url": "https://leonidaverse.com/en/faq/gta-6-editions",
            "source_label": "Leonida Verse, FAQ éditions (prix PlayStation Store)",
        },
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "L'édition Ultimate est uniquement numérique. La Standard existe en numérique ou en boîte contenant un code de téléchargement — il n'y a pas de disque. Il n'y a pas d'édition « Special ».",
            "source_url": "https://realdigitaltech.com/articles/gta-6-release-guide/",
            "source_label": "Real Digital Tech",
        },
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "Préchargement ouvert le 10 novembre 2026 : à minuit heure locale sur PS5, à 0 h GMT pour le monde entier sur Xbox Series X|S. Jusqu'à 212 Go d'espace nécessaire selon la machine.",
            "source_url": "https://gamertagmythras.com/blog/gta-6/gta-6-everything-we-know",
            "source_label": "Rockstar Newswire",
        },
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "Bonus de précommande : le pack Vintage Vice City avant le 20 novembre, plus un mois de GTA+ sur les précommandes numériques. La boîte collector « The Goodtime State » est vendue 399,99 $ sans le jeu.",
            "source_url": "https://leonidaverse.com/en/faq/gta-6-editions",
            "source_label": "Leonida Verse",
        },
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "Fréquence d'images : Rockstar confirme une cible de 30 fps sur toutes les consoles actuelles, PS5 Pro incluse. Aucun mode 60 fps ni 40 fps n'est annoncé au lancement.",
            "source_url": "https://timesaver.gg/blog/gta-6-60fps-performance-mode-ps5-xbox",
            "source_label": "Rockstar Newswire du 10/11/2026, relayée par TimeSaver",
        },
        {
            "id": "FAQ-XX",
            "status": "press_confirmed",
            "text": "Digital Foundry mesure un rythme régulier de 33,3 ms (30 fps) en fonctionnement normal sur PS5, avec des chutes jusqu'à 23 fps lors d'actions lourdes soutenues. Sur PS5 Pro, le 30 fps est quasi constant, avec une chute brève à 24 fps dans le pire cas.",
            "source_url": "https://www.altchar.com/game-news/gta-vi-dips-as-low-as-23fps-on-base-ps5-in-heavy-action-digital-foundry-finds-aJybE7x7IsZa",
            "source_label": "Digital Foundry via AltChar, 18/11/2026",
        },
        {
            "id": "FAQ-XX",
            "status": "press_confirmed",
            "text": "PS5 Pro : deux avantages exclusifs documentés, l'upscaling PSSR (image qui « passe pour du 4K natif ») et les ombres ray-tracées. Pas de gain de fréquence d'images.",
            "source_url": "https://timesaver.gg/blog/gta-6-60fps-performance-mode-ps5-xbox",
            "source_label": "Rockstar Newswire / Digital Foundry",
        },
        {
            "id": "FAQ-XX",
            "status": "official",
            "text": "Le jeu est jouable en streaming via Xbox Cloud Gaming sur Xbox One et Xbox Series X|S depuis 1 h du matin (heure de l'Est) le 19 novembre, et prend en charge le Remote Play. Ce sont des fonctions de diffusion, pas du multijoueur.",
            "source_url": "https://gamertagmythras.com/blog/gta-6/gta-6-everything-we-know",
            "source_label": "Rockstar Newswire",
        },
        {
            "id": "FAQ-XX",
            "status": "post_launch_pending",
            "text": "Non annoncé au 18/11/2026 : version PC et configuration requise, carte du monde complète et dimensions officielles, modes de performance et résolutions natives par console côté Xbox, disponibilité Game Pass ou PlayStation Plus.",
            "source_url": "https://gamenewsplus.net/news/gta-6-release-date-price-platforms-pc-version-everything-we-know-38767/",
            "source_label": "GameNewsPlus",
        },
    ],
}


def _renumber(data: dict) -> None:
    facts = data.get("facts", {})
    prefix = {
        "community_tools_and_social": "OUT",
        "visual_identity_and_art_direction": "DIV",
        "unavailable_post_launch": "FAQ",
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
    g7 = amend.setdefault("g7", {})

    if g7.get("marker") == MARKER:
        print("research_data.json : déjà patché en S4/G7 — aucune duplication.")
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
                "added_in": "S4_G7",
            })
            added_facts += 1

    g7.update({
        "marker": MARKER,
        "at": "2026-11-18",
        "pages": [
            "pages/outils/index.html",
            "pages/divers/index.html",
            "pages/faq/index.html",
        ],
        "facts_added": added_facts,
        "sources_added": added_src,
        "ids": {s: [f["id"] for f in items] for s, items in FACTS.items()},
        "policy": "Tous les outils et créateurs sont community : aucun n'est affilié à Rockstar. Performances = Newswire + Digital Foundry uniquement.",
    })

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in facts.values())
    print(f"Amendement S4/G7 appliqué : +{added_facts} faits, +{added_src} sources, "
          f"{total} faits au total, {len(sources)} sources enregistrées.")


if __name__ == "__main__":
    main()
