#!/usr/bin/env python3
"""Amendement S3 — BUILD_CORE_PAGES (18/11/2026).

Idempotent : ajoute les faits/sources/arbitrages issus de la passe temps réel
(internet, presse, forums, YouTube, GitHub, Reddit, réseaux sociaux) sans
écraser les 283 faits S1/S2 ni la liste des 93 missions de presse.

Règle éditoriale : aucune donnée de presse / communauté / réseau social n'est
promue `official`. Les sources primaires Rockstar restent prioritaires pour la
date, les plateformes, le préchargement et la galerie de lancement.

Usage :
    python3 tools/patch_research_s3.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S3_VERIFIED_FACTS"
RETRIEVED = "2026-11-18"

S3_SOURCES = {
    "rockstar_launch_gallery": "https://www.rockstargames.com/VI/launch-gallery",
    "x_rockstar_launch_gallery": "https://x.com/RockstarGames/status/2118357919229964343",
    "mezha_firmware": "https://mezha.net/eng/news/mezha-57890459decccd8af6f62271_sony_confirms_ps5/",
    "psinfo_firmware": "https://www.playstationinfo.de/en/2026/11/18/gta-6-launches-on-ps5-only-with-a-new-update-and-sony-now-confirms-the-requirement/",
    "forbes_second_patch": "https://www.forbes.com/sites/brianmazique/2026/11/17/gta-6-just-got-a-second-update-before-anyone-can-play-it-and-rockstar-still-isnt-saying-what-it-changes/",
    "opencritic_reviews_s3": "https://opencritic.com/game/15398/grand-theft-auto-vi/reviews",
    "talkesport_launch_live": "https://www.talkesport.com/gta-6/gta-6-launch-live-updates/",
    "gagadget_reviews": "https://gagadget.com/en/734770-gta-vi-hits-99-on-metacritic-ahead-of-its-november-19-launch/",
    "insider_embargo": "https://insider-gaming.com/grand-theft-auto-6-review-embargo/",
    "gamespot_six_star_s3": "https://www.gamespot.com/articles/how-to-get-a-six-star-wanted-level-in-gta-6/",
    "gamespot_money_s3": "https://www.gamespot.com/articles/best-ways-to-make-money-fast-in-gta-6/",
    "gamespot_robberies_s3": "https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/",
    "psinfo_safe_codes_s3": "https://www.playstationinfo.de/en/2026/11/18/gta-6-guide-all-known-safe-codes-and-how-to-pull-off-the-heists-successfully/",
    "youtube_106_tips_s3": "https://www.youtube.com/watch?v=DeFeDYE5P6w",
    "reddit_gta6game_s3": "https://www.reddit.com/r/gta6game/",
    "github_leonida_dispatch_s3": "https://github.com/rhyovar/leonida-dispatch",
    "github_gta6_atlas_s3": "https://github.com/jerrysf/gta6-atlas",
    "github_vicecity_mcp_s3": "https://github.com/fshbeeb/vicecitymission-mcp",
    "x_gtasix_updates_s3": "https://x.com/gtasix_",
    "x_gta6_unlimited_s3": "https://x.com/GTA_Unlimited/status/2122719536457674969",
    "resetera_embargo_s3": "https://www.resetera.com/threads/insider-gaming-gta-6-review-embargo-drops-at-3-00-am-pt-on-wednesday-november-18.1690603/",
}

S3_FACTS = {
    "release_and_platforms": [
        {
            "id": "S3-REL-01",
            "value": "PS5 : le firmware système 26.07-14.23.00 (1,267 Go, publié le 17/11/2026) est signalé comme requis avant le lancement de GTA VI ; l'avertissement vient de PlayStation Support US sur X, relayé par Rockstar Games et couvert par la presse le 18/11. Le post X primaire n'a pas été fetché directement : statut presse, pas « official ».",
            "status": "press_confirmed",
            "sources": ["mezha_firmware", "psinfo_firmware"],
            "source_url": "https://mezha.net/eng/news/mezha-57890459decccd8af6f62271_sony_confirms_ps5/",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-REL-02",
            "value": "Deux patches pré-lancement sont rapportés avant le 19/11 : 01.002.000 le 13/11 (~1 Go PS5) et 01.002.001 le 16/11 (602,5 Mo PS5 ; ~1,59 Go Xbox Series X|S, taille Xbox non confirmée par Rockstar). Le déploiement PS5 aurait été échelonné en trois vagues ; aucune note de patch Rockstar n'a été publiée.",
            "status": "press_confirmed",
            "sources": ["forbes_second_patch"],
            "source_url": "https://www.forbes.com/sites/brianmazique/2026/11/17/gta-6-just-got-a-second-update-before-anyone-can-play-it-and-rockstar-still-isnt-saying-what-it-changes/",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-REL-03",
            "value": "Au 18/11/2026, aucun day-one patch n'est confirmé par Rockstar et aucune note officielle n'explique les correctifs 01.002.000 / 01.002.001 ; la vérification des notes et du comportement en jeu reste post-lancement.",
            "status": "post_launch_pending",
            "sources": ["forbes_second_patch", "newswire"],
            "source_url": "https://www.forbes.com/sites/brianmazique/2026/11/17/gta-6-just-got-a-second-update-before-anyone-can-play-it-and-rockstar-still-isnt-saying-what-it-changes/",
            "retrieved_at": RETRIEVED,
        },
    ],
    "press_reviews": [
        {
            "id": "S3-REV-01",
            "value": "Relevé direct OpenCritic du 18/11/2026 : Top Critic Average 98/100, 100 % de recommandation, 63 critiques dans le JSON-LD, jeu classé au 100e percentile. Instantané horodaté, distinct des agrégats Metacritic.",
            "status": "press_confirmed",
            "sources": ["opencritic_reviews_s3"],
            "source_url": "https://opencritic.com/game/15398/grand-theft-auto-vi/reviews",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-REV-02",
            "value": "Relevés de presse du 18/11 : Metacritic 99/146 critiques dans un live, 98 OpenCritic avec 100 % de recommandation ; d'autres instantanés citent 99/100 ou 99/109 critiques. Ce sont des captures temporelles, jamais un score officiel unique.",
            "status": "press_confirmed",
            "sources": ["talkesport_launch_live", "gagadget_reviews"],
            "source_url": "https://www.talkesport.com/gta-6/gta-6-launch-live-updates/",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-REV-03",
            "value": "L'embargo du 18/11/2026 vers 11:00 GMT / 12:00 CET provient de métadonnées, d'Insider Gaming et de forums ; Rockstar n'a pas publié d'horaire officiel. Les critiques sont effectivement en ligne le 18/11, mais l'horaire reste une reconstruction communautaire.",
            "status": "community",
            "sources": ["insider_embargo", "resetera_embargo_s3"],
            "source_url": "https://insider-gaming.com/grand-theft-auto-6-review-embargo/",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-REV-04",
            "value": "Synthèses de reviews du 18/11 : éloges du monde, des personnages et de la direction artistique ; réserves récurrentes sur des contrôles denses, quelques missions jugées injustes, du « ghosting » en mêlée et du rubber-banding en course. Relevé de presse, pas verdict Rockstar.",
            "status": "press_confirmed",
            "sources": ["gagadget_reviews", "opencritic_reviews_s3"],
            "source_url": "https://gagadget.com/en/734770-gta-vi-hits-99-on-metacritic-ahead-of-its-november-19-launch/",
            "retrieved_at": RETRIEVED,
        },
    ],
    "tips_strategies_techniques": [
        {
            "id": "S3-TIP-01",
            "value": "GameSpot (18/11) : pour atteindre 6 étoiles, rester sur les lieux après un policier abattu, prolonger la poursuite ~10 min jusqu'à 5 étoiles puis 10–15 min supplémentaires, quitter le centre de Vice City vers Leonard/Lummox ou Kelly County, utiliser un véhicule solide et des armes automatiques ; les Hot Areas restent surveillées et imposent de changer tenue, apparence et véhicule.",
            "status": "press_confirmed",
            "sources": ["gamespot_six_star_s3"],
            "source_url": "https://www.gamespot.com/articles/how-to-get-a-six-star-wanted-level-in-gta-6/",
            "retrieved_at": RETRIEVED,
            "spoiler": True,
        },
        {
            "id": "S3-TIP-02",
            "value": "GameSpot (18/11) : revenus rapides via plongées au trésor de Kenton, planques de gang (icônes jaunes / revendeurs), contrats de voitures Moses et Randy, Pay'N'Spray, puis banques Fleeca et commerces haut de gamme après le milieu de l'histoire avec Dye Pack Jammers ; section Starlet Motel en Lucia signalée comme spoilée.",
            "status": "press_confirmed",
            "sources": ["gamespot_money_s3"],
            "source_url": "https://www.gamespot.com/articles/best-ways-to-make-money-fast-in-gta-6/",
            "retrieved_at": RETRIEVED,
            "spoiler": True,
        },
        {
            "id": "S3-TIP-03",
            "value": "GameSpot (18/11) : braquages classés Low / Medium / High ; contrôler la foule, neutraliser l'alarme sur le panneau blanc, détruire ou éviter les CCTV, utiliser le Snap Gun pour les accès arrière, le Focus pour repérer codes et caméras, et un Dye Pack Jammer débloqué au chapitre 3 pour les billets marqués. Les coffres de grande banque s'ouvrent via le camion blindé / Yasmani.",
            "status": "press_confirmed",
            "sources": ["gamespot_robberies_s3"],
            "source_url": "https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/",
            "retrieved_at": RETRIEVED,
            "spoiler": True,
        },
        {
            "id": "S3-TIP-04",
            "value": "GameSpot (18/11, plusieurs playthroughs) : les codes de coffre sont aléatoires, y compris lors d'un second braquage du même commerce ; aucun code universel fiable ne doit être publié. Le code se cherche sur un garde, une note, un écran ou à proximité ; petits coffres et lockboxes peuvent être crochetés ou forcés.",
            "status": "press_confirmed",
            "sources": ["gamespot_robberies_s3"],
            "source_url": "https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-TIP-05",
            "value": "PlayStationInfo (18/11) reprend de PowerPyx trois combinaisons 1680 / 6815 / 0104 pour la chaîne de missions « Yasmani's Jewelry Jobs » et précise qu'elles sont spécifiques à trois boutiques, pas universelles. L'article utilise une image étiquetée « KI Bild » et diverge de GameSpot sur l'aléatoire : ces codes ne sont pas publiés comme liste de référence.",
            "status": "community",
            "sources": ["psinfo_safe_codes_s3"],
            "source_url": "https://www.playstationinfo.de/en/2026/11/18/gta-6-guide-all-known-safe-codes-and-how-to-pull-off-the-heists-successfully/",
            "retrieved_at": RETRIEVED,
            "spoiler": True,
        },
        {
            "id": "S3-TIP-06",
            "value": "YouTube (12/11/2026, 1ceStream, 14:02) : compilation communautaire « 106 Insane GTA 6 Mechanics » annonçant 212 Go de préchargement et couvrant carte, météo, véhicules, combat, police, économie et synergie des protagonistes. Agrégation de sources multiples, à ne pas traiter comme documentation officielle.",
            "status": "community",
            "sources": ["youtube_106_tips_s3"],
            "source_url": "https://www.youtube.com/watch?v=DeFeDYE5P6w",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-TIP-07",
            "value": "Reddit r/gta6game : les résultats de recherche du 18/11 remontent surtout une spéculation PC datée de 2021 sur les CPU/GPU requis ; aucune config PC officielle n'est annoncée. Ce fil est un signal communautaire stale, pas une source de lancement.",
            "status": "community",
            "sources": ["reddit_gta6game_s3"],
            "source_url": "https://www.reddit.com/r/gta6game/",
            "retrieved_at": RETRIEVED,
        },
    ],
    "community_tools_and_social": [
        {
            "id": "S3-COM-01",
            "value": "Rockstar Games sur X (5/11/2026) : « See you in Leonida on November 19 » et lien vers la Launch Gallery officielle rockstargames.com/VI/launch-gallery. Message officiel confirmant la communication autour de la date et des screenshots.",
            "status": "official",
            "sources": ["x_rockstar_launch_gallery", "rockstar_launch_gallery"],
            "source_url": "https://x.com/RockstarGames/status/2118357919229964343",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-COM-02",
            "value": "GitHub rhyovar/leonida-dispatch : compagnon fan-made non officiel (countdown, carte interactive, dossier de casting, tracker, base de données, crew planner, trailer vault), 18 commits, documentation du 10/10 signalant explicitement des données placeholder jusqu'au lancement. Modèle d'UX communautaire, pas source de vérité gameplay.",
            "status": "community",
            "sources": ["github_leonida_dispatch_s3"],
            "source_url": "https://github.com/rhyovar/leonida-dispatch",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-COM-03",
            "value": "GitHub jerrysf/gta6-atlas : atlas Next.js fan-made avec recherche, carte MapLibre, checklist 100 % persistée et pipeline « launch day » ; le README indique des datasets de missions / collectibles intentionnellement vides jusqu'aux positions vérifiées en jeu après le 19/11/2026.",
            "status": "community",
            "sources": ["github_gta6_atlas_s3"],
            "source_url": "https://github.com/jerrysf/gta6-atlas",
            "retrieved_at": RETRIEVED,
        },
        {
            "id": "S3-COM-04",
            "value": "X / réseaux sociaux : comptes de fans et de countdown, messages « See you in Leonida », annonces de lives, chiffres de précommandes et claims de complétion express circulent le 18/11. Ces signaux d'engouement restent non vérifiés ; le guide les badge COMMUNAUTÉ et n'en déduit aucune mécanique ni donnée chiffrée.",
            "status": "community",
            "sources": ["x_gtasix_updates_s3", "x_gta6_unlimited_s3"],
            "source_url": "https://x.com/gtasix_",
            "retrieved_at": RETRIEVED,
        },
    ],
    "map_and_regions": [
        {
            "id": "S3-MAP-01",
            "value": "GitHub fshbeeb/vicecitymission-mcp : serveur MCP communautaire exposant ~1 900 landmarks appariés à des lieux réels de Floride / Miami via map.gtadb.org (CC BY 4.0). Les broches sont des données communautaires, pas une cartographie officielle Rockstar ni des positions vérifiées en jeu.",
            "status": "community",
            "sources": ["github_vicecity_mcp_s3"],
            "source_url": "https://github.com/fshbeeb/vicecitymission-mcp",
            "retrieved_at": RETRIEVED,
        },
    ],
    "unavailable_post_launch": [
        {
            "id": "S3-PEND-01",
            "value": "Au 18/11/2026, Rockstar n'a publié ni liste officielle de trophées PSN/Xbox, ni liste de cheats, ni checklist 100 %, ni notes de patch, ni cartographie interactive, ni annonce GTA VI Online. Le recoupement PSN / Xbox / in-game et les éventuelles notes du 19/11 restent post_launch_pending.",
            "status": "post_launch_pending",
            "sources": ["newswire", "rockstar_vi"],
            "source_url": "https://www.rockstargames.com/newswire",
            "retrieved_at": RETRIEVED,
        },
    ],
}


def source_url_list(fact: dict) -> list[str]:
    """Remplace les clés du registre par des URL, en gardant source_url en tête."""
    primary = fact["source_url"]
    urls = [primary]
    for key in fact.get("sources", []):
        url = S3_SOURCES.get(key)
        if url and url not in urls:
            urls.append(url)
    fact["sources"] = urls
    return urls


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("meta", {}).get("s3_amendment", {}).get("marker") == MARKER:
        print("research_data.json : déjà patché en S3 — aucune duplication.")
        return

    for key, url in S3_SOURCES.items():
        data["sources_registry"].setdefault(key, url)

    added = 0
    for section, facts in S3_FACTS.items():
        data["facts"].setdefault(section, [])
        existing = {f["id"] for f in data["facts"][section]}
        for fact in facts:
            if fact["id"] in existing:
                continue
            prepared = dict(fact)
            source_url_list(prepared)
            data["facts"][section].append(prepared)
            added += 1

    contradictions = [
        {
            "topic": "Codes de coffre : aléatoire GameSpot vs codes statiques PlayStationInfo",
            "conflict": "GameSpot rapporte des codes randomisés sur plusieurs playthroughs ; PlayStationInfo cite PowerPyx et trois combinaisons spécifiques à la chaîne Yasmani.",
            "arbitration": "Ne publier aucune liste universelle. Badge PRESSE · 18/11 pour l'aléatoire, COMMUNAUTÉ / SPOILER pour les codes mission-specific, et recoupement in-game obligatoire après le 19/11.",
        },
        {
            "topic": "Scores du 18/11 : instantanés multiples",
            "conflict": "OpenCritic direct 98/100 %/63 critiques ; Metacritic 99/146 dans un live ; d'autres round-ups 98/54, 99/100, 99/109.",
            "arbitration": "Afficher chaque chiffre avec son agrégateur, son horodatage et son nombre de critiques ; ne jamais fusionner OpenCritic et Metacritic.",
        },
        {
            "topic": "Firmware 14.23 et patches pré-lancement",
            "conflict": "Presse et comptes X relaient une exigence PS5 14.23, deux builds 01.002.000 / 01.002.001 et des tailles différentes, sans notes Rockstar.",
            "arbitration": "Badge PRESSE · 18/11, distinguer firmware système et patch jeu, préciser l'absence de notes officielles et ne pas annoncer de day-one patch.",
        },
        {
            "topic": "Embargo critiques : horaire rapporté vs publication officielle",
            "conflict": "Insider Gaming / ResetEra / métadonnées pointent 11:00 GMT le 18/11 ; Rockstar n'a pas publié d'horaire.",
            "arbitration": "Conserver « reviews en ligne le 18/11 » comme fait de presse, et « 11:00 GMT » comme reconstruction communautaire non officialisée.",
        },
    ]
    data["contradictions_and_arbitrations"].extend(contradictions)

    data["mega_prompt_corrections"].extend([
        "S3 (18/11) : Rockstar Newswire / VI / Store / X officiel priment sur les pages SEO qui avancent des dates, prix ou préchargements contradictoires.",
        "S3 (18/11) : aucun « code de coffre universel » ; les combinaisons de mission ne sont ni officielles ni généralisables.",
        "S3 (18/11) : les chiffres sociaux (précommandes, lives, complétion express) sont des signaux d'hype, pas des faits vérifiés.",
        "S3 (18/11) : ne pas additionner / moyenner les scores Metacritic et OpenCritic ; chaque snapshot garde sa source et son horodatage.",
    ])

    data["next_research_pass"].extend([
        "Dès le 19/11/2026 : recouper en jeu les codes de coffre aléatoires, les 93 missions, les 55 trophées de presse et la checklist 100 %.",
        "Dès le 19/11/2026 : vérifier les notes de patch Rockstar, le firmware PS5 14.23, l'éventuel day-one patch et les tailles d'installation finales.",
        "Après le lancement : confirmer toute annonce GTA VI Online / PC / transfert GTA Online à partir de Rockstar uniquement.",
        "Après le lancement : remplacer les datasets placeholder des outils GitHub par des positions et statistiques vérifiées en jeu.",
    ])

    flat = [f for section in data["facts"].values() for f in section]
    by_status: dict[str, int] = {}
    for f in flat:
        by_status[f["status"]] = by_status.get(f["status"], 0) + 1
    section_counts = {k: len(v) for k, v in data["facts"].items()}

    data["meta"]["phase"] = "S1 — RESEARCH + S2 — DESIGN_SYSTEM + S3 — BUILD_CORE_PAGES (amendement 18/11/2026)"
    data["meta"]["build_context"] = "J-1 avant la sortie officielle du 19/11/2026 ; passe S3 temps réel : presse post-embargo, Rockstar officiel, forums, YouTube, GitHub, Reddit et réseaux sociaux. Intégrité : badge de statut + SpoilerToggle sur toute donnée non officielle."
    data["meta"]["totals"] = {
        "facts": len(flat),
        "sections": len(data["facts"]),
        "sources_registered": len(data["sources_registry"]),
        "by_status": by_status,
        "s3_new_facts": added,
        "s3_new_sources": len(S3_SOURCES),
    }
    data["meta"]["sections"] = section_counts
    data["meta"]["status_vocabulary"]["social_or_hype"] = "Publication X / réseau social non vérifiée ; classée `community`, jamais `official`."
    data["meta"]["s3_amendment"] = {
        "marker": MARKER,
        "at": RETRIEVED,
        "surfaces": ["web", "forums", "YouTube", "GitHub", "Reddit", "X / social", "presse accréditée", "Rockstar officiel"],
        "direct_fetches": [
            "Rockstar Newswire", "Rockstar VI", "GameSpot 6-star", "GameSpot money",
            "GameSpot safe codes / robberies", "PlayStationInfo safe codes", "OpenCritic reviews",
            "GitHub rhyovar/leonida-dispatch", "GitHub jerrysf/gta6-atlas", "Forbes patch 01.002.001",
            "X RockstarGames launch gallery", "YouTube 106 tips", "Mezha firmware",
        ],
        "policy": "OFFICIEL réservé aux sources Rockstar / Sony / Xbox primaires ; PRESSE · 18/11 pour les relevés accrédités ; COMMUNAUTÉ pour forums / GitHub / YouTube / Reddit / X ; SPOILER pour missions, codes, fins et routes 6 étoiles ; EN ATTENTE pour tout contenu post-launch.",
        "badge_policy": {
            "official": "OFFICIEL",
            "press_confirmed": "PRESSE · 18/11",
            "community": "COMMUNAUTÉ",
            "leak_unverified": "FUITE NON VÉRIFIÉE",
            "post_launch_pending": "EN ATTENTE · 19/11",
            "speculative": "ESTIMATION",
        },
        "assets": {
            "images": "Lot S3 IMG011–IMG020 : 10 JPG cinématographiques 1920×1080 / 1280×1920, q95 progressif ; s'ajoutent au lot S2 IMG001–IMG010 sans le remplacer.",
            "audio": "Lot S3 AUD011–AUD012 : 2 MP3 originaux ; le lecteur S3 expose les 12 MP3 locaux.",
        },
        "no_official_numbers": "Les chiffres affichés par la homepage sont extraits de research_data.json ; les compteurs dynamiques se dégradent en « — » si le JSON local est indisponible dans l'aperçu sandbox.",
    }
    data["s3_research_matrix"] = {
        "official": ["https://www.rockstargames.com/newswire", "https://www.rockstargames.com/VI", "https://www.rockstargames.com/VI/launch-gallery", "https://x.com/RockstarGames/status/2118357919229964343"],
        "press": ["https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/", "https://www.gamespot.com/articles/how-to-get-a-six-star-wanted-level-in-gta-6/", "https://www.gamespot.com/articles/best-ways-to-make-money-fast-in-gta-6/", "https://opencritic.com/game/15398/grand-theft-auto-vi/reviews", "https://www.forbes.com/sites/brianmazique/2026/11/17/gta-6-just-got-a-second-update-before-anyone-can-play-it-and-rockstar-still-isnt-saying-what-it-changes/", "https://mezha.net/eng/news/mezha-57890459decccd8af6f62271_sony_confirms_ps5/"],
        "community": ["https://www.youtube.com/watch?v=DeFeDYE5P6w", "https://www.reddit.com/r/gta6game/", "https://github.com/rhyovar/leonida-dispatch", "https://github.com/jerrysf/gta6-atlas", "https://github.com/fshbeeb/vicecitymission-mcp", "https://www.resetera.com/threads/insider-gaming-gta-6-review-embargo-drops-at-3-00-am-pt-on-wednesday-november-18.1690603/"],
        "social": ["https://x.com/gtasix_", "https://x.com/GTA_Unlimited/status/2122719536457674969"],
    }

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Amendement S3 appliqué : +{added} faits, +{len(S3_SOURCES)} sources proposées, {len(flat)} faits au total, {len(data['sources_registry'])} sources enregistrées.")


if __name__ == "__main__":
    main()
