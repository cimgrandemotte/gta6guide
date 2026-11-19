#!/usr/bin/env python3
"""
Génère research_data.json (phase S1 — RESEARCH).

Chaque fait porte OBLIGATOIREMENT : id, value, status, sources[],
source_url (1re URL), retrieved_at — voir fact_policy.json_rule.
Amendement S2 du 18/11/2026 : intégration des articles post-embargo vérifiés
par fetch direct ; les nouveaux faits restent `press_confirmed`, jamais `official`.
Statuts : official | press_confirmed | community | leak_unverified |
          post_launch_pending | speculative

Aucune donnée d'après-lancement n'est fabriquée : les sujets indisponibles
sont explicitement listés dans `unavailable_post_launch`.

Usage : python3 tools/build_research_data.py
"""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "research_data.json")
RETRIEVED = "2026-11-18"

# ─── Registre des sources (URLs réellement consultées ce jour) ────────────────
S = {
    "rockstar_vi": "https://www.rockstargames.com/VI",
    "newswire": "https://www.rockstargames.com/newswire",
    "store_fr": "https://store.rockstargames.com/fr/game/buy-gta-vi",
    "rockstar_x": "https://x.com/rockstargames",
    "wikipedia": "https://en.wikipedia.org/wiki/Grand_Theft_Auto_VI",
    "actugaming": "https://www.actugaming.net/gta-6-guide-complet-832971/",
    "gtabase": "https://www.gtabase.com/grand-theft-auto-6/",
    "dotesports": "https://dotesports.com/gta/news/gta-6",
    "dotesports_guide": "https://dotesports.com/gta/guides/gta-6",
    "gtaboss_chars": "https://www.gtaboss.gg/gta-6/guides/gta-6-characters",
    "gtaboss_preorder": "https://www.gtaboss.gg/gta-6/guides/gta-6-preorder-guide",
    "gta6hype": "https://www.gta6hype.com/release/",
    "tracker": "https://tracker.gg/gta6/release-date",
    "metacritic": "https://www.metacritic.com/game/grand-theft-auto-vi/",
    "dexerto": "https://www.dexerto.com/gta/gta-6-is-the-joint-best-reviewed-game-of-the-all-time-3429300/",
    "maketecheasier_reviews": "https://maketecheasier.com/gta-6-reviews-metacritic-score/",
    "independent": "https://www.independent.co.uk/extras/indybest/gadgets-tech/video-games-consoles/gta-6-live-b3085508.html",
    "gamespot_review": "https://www.gamespot.com/reviews/grand-theft-auto-6-review/",
    "digitalspy_review": "https://www.digitalspy.com/tech/a74452071/gta6-review/",
    "trueachievements_review": "https://www.trueachievements.com/news/grand-theft-auto-6-review",
    "screenrant_review": "https://screenrant.com/grand-theft-auto-6-review/",
    "vgtimes": "https://vgtimes.com/games/gta-6/news/",
    "ign_30fps": "https://in.ign.com/grand-theft-auto-vi/276604/gta-6-will-run-at-30fps-on-all-consoles-features-ray-tracing-improvements-on-ps5-pro",
    "pushsquare": "https://www.pushsquare.com/news/2026/11/gta-6-ps5-pro-features-revealed-30fps-target-on-both-consoles",
    "kotaku": "https://kotaku.com/gta-6s-vice-city-is-rockstars-biggest-yet-and-the-whole-map-is-three-times-larger-than-red-dead-redemption-2-2000728978",
    "forbes": "https://www.forbes.com/sites/brianmazique/2026/10/30/gta-6s-map-is-nearly-as-big-as-gta-4-gta-5-and-red-dead-2-combined-plus-a-201-mission-rumor/",
    "tgg_x": "https://x.com/TGGonYT/status/2093478776604860838",
    "redbull": "https://www.redbull.com/us-en/gta-6-gameplay-details",
    "gtavice_flow": "https://www.gtavice.net/news/flow-games-reveals-more-gta-6-details-fuel-system-no-first-person-mode-30-fps-and-more",
    "allthings_rubius": "https://allthings.how/gta-6-gameplay-details-from-el-rubius-11-things-confirmed-from-his-rockstar-session/",
    "shattered": "https://shattered.io/gta-6-open-world-gameplay-systems-2026/",
    "gta6features": "https://gta6features.com/",
    "wanted_tech2geek": "https://www.tech2geek.net/gta-6-police-explained-how-the-new-wanted-system-works/",
    "wanted_fandom": "https://gta.fandom.com/wiki/Wanted_Level_in_Grand_Theft_Auto_VI",
    "wanted_gamesreviews": "https://gamesreviews.com/news/08/gta-6-confirms-return-of-six-star-wanted-level-ditching-gta-5s-five-star-cap/",
    "gtaintel_weapons": "https://gtaintel.com/news/gta-6-confirmed-weapons-list",
    "gamerant_weapons": "https://gamerant.com/grand-theft-auto-gta-6-confirmed-weapons/",
    "allthings_weapons": "https://allthings.how/gta-6-weapons-list-every-confirmed-gun-so-far/",
    "gta6cartel": "https://gta6cartel.com/news/gta-6-cars-list",
    "bible": "https://gta6bible.com/wiki/",
    "gta6guide_fr": "https://gta6guide.fr/",
    "gta6wiki_fr": "https://gta-6-wiki.com/fr/",
    "grandtheft": "https://grandtheft.gg/",
    "explained": "https://gta6explained.com/",
    "leonidastate": "https://leonidastate.guide/",
    "leonidaverse": "https://leonidaverse.com/en/gta-6-map",
    "endgametools": "https://endgametools.com/en/gta-6/",
    "vice_city_app": "https://vice-city.app/",
    "github_atlas": "https://github.com/navanem/gta6-leonida-atlas",
    "github_atlas_fr": "https://github.com/cleementt26/leonida-atlas",
    "github_dispatch": "https://github.com/rhyovar/leonida-dispatch",
    "github_mapx": "https://github.com/gta6mapx/gta6mapx",
    "activities_allthings": "https://allthings.how/gta-6-every-confirmed-side-activity-so-far/",
    "activities_wiki": "https://thegameswiki.com/gta6/wiki/side-activities",
    "economy_gtanerd": "https://gtanerd.com/guides/gta-6-money/",
    "economy_hustle": "https://www.vicecityhustle.com/guides/how-to-make-money-at-launch-gta-6",
    "radio_itech": "https://www.itechguides.com/whats-confirmed-about-gta-6s-radio-soundtrack-and-song-licensing/",
    "radio_meowdb": "https://meowdb.com/gta6/radio",
    "radio_rockstarreport": "https://rockstarreport.com/features/gta-6-radio-stations-soundtrack",
    "weather_endgame": "https://endgametools.com/en/gta-6/news/gta-6-weather",
    "weather_beebom": "https://beebom.com/new-gta-6-weather-screenshots-transform-leonida/",
    "weather_mte": "https://maketecheasier.com/weather-channel-gta-6-leonida-forecast/",
    "online_justjared": "https://www.justjared.com/2026/11/17/gta-6-online-release-date-multiplayer-launch/",
    "online_webtech": "https://www.webtech360.com/detail/gta-6-online-what-we-know-about-multiplayer-as-of-en-trend-hp2-99916641.html",
    "cheats_gtasix": "https://gtasix.org/en/guide/cheats/",
    "cheats_gta6guide": "https://gta6guide.fr/en/gta-6/cheat-codes",
    "cheats_gta6cheatcodes": "https://www.gta6cheatcodes.com/",
    "psnprofiles": "https://forum.psnprofiles.com/topic/201939-probably-fake-rumored-gta-vi-trophies-list/",
    "yaninagames": "https://yaninagames.com/blog/gta-6-achievements/",
    "gamebyte": "https://www.gamebyte.com/gta-6-trophies-list/",
    "pcgamer_trophies": "https://www.pcgamer.com/games/grand-theft-auto/gta-6-achievements-list/",
    "pressstart_trophies": "https://press-start.com.au/news/2026/11/18/gta-6-trophy-list/",
    "easteregg_life": "https://gta6-life.com/en/guides/gta-6-easter-eggs/",
    "easteregg_earlygame": "https://earlygame.com/guides/gaming/gta-6-easter-eggs-hidden-details",
    "reddit_mysteries": "https://www.reddit.com/r/GTA6/comments/1ksg2v4/gta_vi_mysteries/",
    "reddit_gta6game": "https://www.reddit.com/r/gta6game/",
    "yt_106tips": "https://www.youtube.com/watch?v=DeFeDYE5P6w",
    "yt_day1": "https://www.youtube.com/watch?v=a-YFN3ES69M",
    "yt_prelaunch": "https://www.youtube.com/watch?v=UyfLYHAbdAQ",
    "yt_walkthrough": "https://www.youtube.com/watch?v=yBCdznZor38",
    "yt_playlist": "https://www.youtube.com/playlist?list=PLNrk08jMVrPc",
    "yt_hidden": "https://www.youtube.com/watch?v=7WPqL8SPqiE",
    "thebiglead_tips": "https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/",
    "ofzen_launchday": "https://www.ofzenandcomputing.com/gta-6-launch-day-guide-everything-to-do-before-you-play/",
    "eldorado_leaks": "https://www.eldorado.gg/blog/grand-theft-auto-en/gta-6-leaks/",
    "gamesradar": "https://www.gamesradar.com/gta-6-guide/",
    # ─── Sources S2 vérifiées par recherche + fetch direct le 18/11/2026 ────
    "gamespot_cheats": "https://www.gamespot.com/articles/all-gta-6-cheats-and-how-to-unlock-them/",
    "gamespot_tips": "https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/",
    "gamespot_robberies": "https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/",
    "gamespot_dualsense": "https://www.gamespot.com/articles/gta-6-has-a-clever-ps5-dualsense-trick-for-keeping-you-under-the-speed-limit/",
    "gamespot_gym": "https://www.gamespot.com/articles/gta-6-gym-workouts-have-a-useful-trick-that-saves-you-a-lot-of-time/",
    "pressstart_cheats": "https://press-start.com.au/news/2026/11/18/every-grand-theft-auto-6-cheat-how-to-unlock/",
    "pressstart_economy": "https://press-start.com.au/news/2026/11/18/tips-for-managing-your-money-in-grand-theft-auto-6/",
    "pressstart_missions": "https://press-start.com.au/news/2026/11/18/heres-how-many-story-missions-are-in-grand-theft-auto-6/",
    "pressstart_100": "https://press-start.com.au/news/2026/11/18/grand-theft-auto-6-100-percent-checklist/",
    "sportskeeda_wanted": "https://www.sportskeeda.com/gta/how-get-6-star-wanted-level-gta-6-and-escape-police",
    "pcmag_art": "https://au.pcmag.com/games/120955/ive-spent-weeks-in-gta-6s-vice-city-and-i-never-want-to-leave",
    "g2a_art": "https://www.g2a.com/news/gta-6-news/gta-vi-vs-gta-vice-city-iconic-locations-comparison/",
    "rockstarintel_cover": "https://rockstarintel.com/new-gta-6-cover-art-wallpapers-logo-released/",
    "gfinity_cover": "https://www.gfinityesports.com/article/from-gta-1-to-gta-6-the-evolution-of-gtas-iconic-cover-art",
    "vgtimes_cover": "https://vgtimes.com/articles/158598-all-gta-covers.html",
    "gadgets360_reviews": "https://www.gadgets360.com/games/news/gta-6-review-roundup-highest-rated-game-of-all-time-metacritic-ocarina-of-time-rockstar-games-12344575",
    "opencritic_news": "https://opencritic.com/news/39914/gta-6-is-officially-the-best-reviewed-game-of-all-time-on-metacritic",
    "thegamer_reviews": "https://www.thegamer.com/gta-6-review-round-up/",
    "tomsguide_reviews": "https://www.tomsguide.com/news/live/gta-6-review-roundup-live-updates",
    "newswav_live": "https://newswav.com/article/gta-6-launch-live-latest-updates-as-fans-gear-up-for-release-A2611_rPPMKu",
    "rockstarintel_patch": "https://rockstarintel.com/new-gta-vi-update-released-and-not-everyone-has-gotten-it-heres-why/",
    "ggrecon_patch": "https://www.ggrecon.com/articles/gta-6-second-update-before-launch/",
    "mte_patch": "https://maketecheasier.com/gta-6-patch-01-002-001-size/",
    "github_atlas_fork": "https://github.com/mendesjf86/gta6-leonida-atlas",
    "yt_nz_tutorial": "https://www.youtube.com/watch?v=EwBcYsbJu2I",
    "yt_preplay": "https://www.youtube.com/watch?v=P1YTXjZRUpw",
    "gta6nerd_tips": "https://gta6nerd.com/articles/tips-tricks/",
    "independent_preload": "https://www.independent.co.uk/extras/indybest/gadgets-tech/video-games-consoles/gta-6-pre-load-game-release-date-b3083136.html",
}


def fact(fid: str, value: str, status: str, *sources: str, note: str = "") -> dict:
    urls = [S[k] for k in sources]
    assert urls, f"Fait {fid} sans source"
    d = {
        "id": fid,
        "value": value,
        "status": status,
        "sources": urls,
        "source_url": urls[0],  # fact_policy.json_rule : URL primaire de chaque fait
        "retrieved_at": RETRIEVED,
    }
    if note:
        d["note"] = note
    return d


FACTS: dict[str, list[dict]] = {}

FACTS["release_and_platforms"] = [
    fact("REL-01", "Sortie officielle : jeudi 19 novembre 2026, déblocage à minuit heure locale (rolling midnight, Nouvelle-Zélande en premier).", "official", "rockstar_vi", "newswire", "gta6hype", "tracker"),
    fact("REL-02", "Plateformes natives : PS5, PS5 Pro, Xbox Series X, Xbox Series S. Aucune version PS4 / Xbox One native.", "official", "rockstar_vi", "actugaming", "dotesports"),
    fact("REL-03", "Aucune version PC annoncée ; des rapports de presse évoquent le T1 2027, sans confirmation Rockstar.", "official", "wikipedia", "actugaming", "dotesports", note="Le T1 2027 est une rumeur de presse, pas une date."),
    fact("REL-04", "Xbox One peut y jouer via Xbox Cloud Gaming (réglages graphiques Series S) ; Remote Play PS5/Xbox confirmé. Ce n'est pas du multijoueur.", "official", "actugaming", "online_webtech", "wikipedia"),
    fact("REL-05", "Deux reports : automne 2025 → 26 mai 2026 (mai 2025) → 19 novembre 2026 (6 novembre 2025).", "official", "tracker", "dotesports", "actugaming"),
    fact("REL-06", "Préchargement ouvert le 10 novembre 2026 (0 h locale PS5, 0 h GMT Xbox) ; jusqu'à 212 Go requis.", "official", "newswire", "gtabase", "dotesports", "actugaming"),
    fact("REL-07", "Boîte physique = code de téléchargement, aucun disque ; expédition estimée au 12 novembre 2026.", "official", "store_fr", "actugaming", "gtabase"),
    fact("REL-08", "Cible 30 FPS sur TOUTES les consoles, y compris PS5 Pro ; pas de mode 60 ni 40 FPS à la sortie. PS5 Pro : PSSR + ombres ray-tracées exclusives.", "official", "ign_30fps", "pushsquare", "independent"),
    fact("REL-09", "ESRB M (Mature 17+) ; classification FR à vérifier sur la fiche store.", "official", "store_fr", "dotesports"),
    fact("REL-10", "Mise à jour firmware PS5 obligatoire signalée le 18/11/2026 pour jouer au lancement.", "press_confirmed", "vgtimes"),
    fact("REL-11", "Le site officiel Rockstar indique « Plays Best On PlayStation 5 » (argument marketing, pas une exclusivité).", "official", "rockstar_vi"),
    fact("REL-12", "8 nominations aux Game Awards 2026, dont Game of the Year (show le 10 décembre 2026).", "press_confirmed", "endgametools"),
]

FACTS["editions_and_pricing"] = [
    fact("EDI-01", "Édition Standard 79,99 $ US / 79,99 € ; Édition Ultime 99,99 $ US / 99,99 €.", "official", "store_fr", "gtabase", "actugaming", "gtaboss_preorder"),
    fact("EDI-02", "Précommandes ouvertes depuis le 25 juin 2026 sur PlayStation Store, Microsoft Store et Rockstar Store.", "official", "gtabase", "gta6wiki_fr", "gtaboss_preorder"),
    fact("EDI-03", "Pack Vintage Vice City : Vapid Stanier 1955, garage, tenues rétro, motif d'arme. Sur le Rockstar Store FR, condition « commande avant le 20 novembre ».", "official", "store_fr", "actugaming", "gtabase", note="Certaines sources anglaises disent « avant le 19/11 » : retenir la mention du store FR et horodater."),
    fact("EDI-04", "1 mois de GTA+ offert pour les précommandes/achats numériques (pas pour les boîtes).", "official", "store_fr", "dotesports", "gtaboss_preorder"),
    fact("EDI-05", "Mise à niveau Standard → Ultime possible après achat (20 $ / 20 € sur Xbox, tarif PS non publié avant possession).", "official", "store_fr", "gtaboss_preorder", "dotesports"),
    fact("EDI-06", "Contenu Ultime listé sur le Rockstar Store FR : Grotti Cheetah 1995, revolvers Hawk & Little Morgan, variantes d'armes personnalisées, véhicules pour la planque de Jason, Ganado rétro, Rideout Customs, Sara's Unisex Salon, Shitzu Squalo, Stock 305, Vapid Dominator Buggy 1967, Electric Fang Tattoo, One-Eyed Willie, collection de voitures classiques, Wyman Car Collection.", "official", "store_fr", "gtabase", note="Le DOM de la page Store répète la même liste sous « Standard » : artefact de parsing, ne pas en déduire que la Standard inclut ces bonus."),
    fact("EDI-07", "Aucune Collector's Edition annoncée ; une « Vice City Collection » (collector merchandising) existe séparément.", "official", "gtaboss_preorder", "rockstar_vi"),
    fact("EDI-08", "Le pack Vintage Vice City est présenté par Dot Esports comme ramenant Tommy Vercetti ; cette affirmation n'est pas confirmée par la fiche Rockstar FR.", "speculative", "dotesports", note="À ne pas publier comme fait."),
    fact("EDI-09", "Certains revendeurs FR ont proposé la Standard autour de 60 € en précommande (promotion, pas prix officiel).", "press_confirmed", "actugaming"),
]

FACTS["story_and_characters"] = [
    fact("CHA-01", "Synopsis officiel : Jason et Lucia, après un coup qui tourne mal, plongés dans un complot criminel à travers tout l'État de Leonida, obligés de compter l'un sur l'autre.", "official", "store_fr", "rockstar_vi"),
    fact("CHA-02", "Deux protagonistes jouables : Jason Duval et Lucia Caminos. Lucia = première protagoniste féminine d'un GTA principal en 3D.", "official", "gtaboss_chars", "actugaming", "dotesports"),
    fact("CHA-03", "Rockstar a publié 8 profils officiels / 9 personnes nommées : Jason, Lucia, Cal Hampton, Boobie Ike, Dre'Quan Priest, Real Dimez (Bae-Luxe & Roxy), Raul Bautista, Brian Heder.", "official", "gtaboss_chars", "store_fr"),
    fact("CHA-04", "Jason : enfance entourée d'escrocs, passage par l'armée, travaille pour des trafiquants des Leonida Keys, vit dans une propriété de Brian Heder à Key Lento.", "official", "gtaboss_chars", "actugaming", "wikipedia"),
    fact("CHA-05", "Lucia : passée par le pénitencier de Leonida, origines familiales à Liberty City, rêve de la « bonne vie » ; combattante amateur.", "official", "gtaboss_chars", "actugaming"),
    fact("CHA-06", "Relation Jason/Lucia : attribut partagé, romance optionnelle, activités communes (conduite, shopping, gym, coiffeur), ignorer les messages dégrade la relation ; pas de bonus de gameplay direct selon Rockstar.", "official", "wikipedia", "redbull", "gtavice_flow"),
    fact("CHA-07", "Système « Criminal Profile » : réputation par personnage, inspirée de l'honneur de RDR2, qui suit si les crimes restent « professionnels » ou versent dans la violence gratuite.", "official", "wikipedia", "dotesports_guide"),
    fact("CHA-08", "Poids / fatigue / morphologie : calories, muscle, masse grasse, force ; transformations limitées par la morphologie de base ; la fatigue se lit sur le visage.", "official", "wikipedia", "gtavice_flow", "dotesports_guide"),
    fact("CHA-09", "Jason et Lucia ont des capacités de combat distinctes et des quantités de Focus différentes ; Focus ralentit le temps et révèle les points faibles.", "press_confirmed", "gtavice_flow", "redbull"),
    fact("CHA-10", "La liste longue de PNJ du MegaPrompt (Sal Marino, Nadia Okafor, Krystal Kane, Randy, Camilo, Gator Jim Boone, Gloria Fairweather, Officier Méndez, Tío Beto, Stefanie Gates, Clint Varner, Big Earl, Dr Ansel Moreau, Shérif Clyde Bodine, Valentina, Viktor Sokolov…) provient de leonidaverse.com.", "community", "leonidaverse", note="Ce site précise « An imagined map ahead of release » et ouvre sa carte le 19/11. Ces noms sont des entrées communautaires imaginées, PAS des personnages confirmés."),
    fact("CHA-11", "leonidaverse ajoute une 7e région « Waning Sands » et des collections chiffrées (Jack of Hearts Cards 54, Lucia's Letters 12…) : données spéculatives pré-lancement.", "community", "leonidaverse"),
    fact("CHA-12", "gta6bible.com recense 204 entrées dont 122 estampillées Rockstar-confirmed (110 véhicules, 28 armes, 28 personnages) avec étiquetage de provenance.", "community", "bible"),
    fact("CHA-13", "Wyman, Phil Cassidy et DWNPLY apparaissent dans des wikis communautaires comme personnages mineurs / références, sans profil officiel Rockstar.", "community", "bible", "easteregg_earlygame"),
]

FACTS["map_and_regions"] = [
    fact("MAP-01", "6 régions officiellement présentées : Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga National Park.", "official", "actugaming", "dotesports", "vice_city_app"),
    fact("MAP-02", "Rob Nelson (co-directeur Rockstar North) à TGG : carte 2× GTA V, 3× RDR2 ; Vice City 2× Los Santos ; banlieues 11× celles de Los Santos.", "press_confirmed", "tgg_x", "kotaku", "forbes"),
    fact("MAP-03", "EDGE / NYT corroborent « ≈2× GTA V » et « ≈3× RDR2 » ; Rockstar n'a jamais publié de superficie en km².", "press_confirmed", "forbes", "dotesports"),
    fact("MAP-04", "Météo localisée, persistante et dynamique ; tempêtes tropicales, ouragans, pluie, brouillard marin. Déclaration d'Owen Shepherd (VP Art, Light & Rendering) via The Weather Channel le 16/11/2026 avec 6 screenshots officiels.", "official", "weather_endgame", "weather_beebom", "weather_mte", "actugaming"),
    fact("MAP-05", "Aucune image officielle d'ouragan dans les 6 visuels météo du 16/11 ; les ouragans sont annoncés par la presse (Game Informer) mais non montrés.", "press_confirmed", "weather_endgame", "weather_beebom"),
    fact("MAP-06", "Pas de bascule 2D/3D pour la minicarte ; HUD dynamique, boussole optionnelle, waypoint rapide en maintenant la croix directionnelle bas.", "press_confirmed", "tgg_x"),
    fact("MAP-07", "Reconstruction communautaire GTA VI Mapping / GTADB : ~3 300 lieux chez Endgame Tools, 2 204 lieux interrogeables dans Leonida Atlas. Cartes NON officielles.", "community", "endgametools", "github_atlas", "dotesports", note="À créditer CC BY 4.0 si réutilisées."),
    fact("MAP-08", "leonidastate.guide annonce carte 3D, wiki, radio tuner navigateur et outils créateurs, mais se présente comme « built in public » en cours de construction.", "community", "leonidastate"),
    fact("MAP-09", "leonidaverse.com : carte « imagined » pré-lancement, ouverture annoncée le 19/11/2026, 7 régions et ~2 000 marqueurs spéculatifs.", "community", "leonidaverse"),
    fact("MAP-10", "gta6guide.fr propose une carte interactive FR « guidée par IA » et une base de 185 véhicules identifiés dans les trailers / Extended Look.", "community", "gta6guide_fr"),
    fact("MAP-11", "Endgame Tools : 4 outils sur 9 actifs ; Cheats, Vehicles, Weapons, 100% checklist et Trophies explicitement « Coming soon » car « avant la sortie, aucune source ne vaut la peine d'être crue ».", "community", "endgametools", note="Corrobore la politique d'intégrité du projet."),
    fact("MAP-12", "Vice City : 11 districts selon le MegaPrompt / 20+ districts selon vice-city.app ; aucun découpage officiel chiffré publié par Rockstar.", "community", "vice_city_app"),
]

FACTS["gameplay_mechanics"] = [
    fact("MEC-01", "Limite de port d'armes : 2 armes longues + 2 armes de poing sur soi ; le reste stocké dans le coffre du véhicule (logique RDR2).", "official", "wikipedia", "gtavice_flow", "dotesports_guide"),
    fact("MEC-02", "Carburant fonctionnel : jauge, panne sèche possible, ravitaillement à la station maintenant R2/RT ~10 s ; les stations réparent aussi le véhicule ; réservoirs peuvent fuir/prendre feu.", "official", "redbull", "independent", "gtavice_flow", "gta6features"),
    fact("MEC-03", "Véhicules électriques : recharge en station confirmée dans les previews presse.", "press_confirmed", "gtavice_flow", "gta6features"),
    fact("MEC-04", "Traceurs GPS sur les voitures haut de gamme : la police peut suivre même hors zone de recherche ; retrait payant chez un garage/mécanicien.", "press_confirmed", "allthings_rubius"),
    fact("MEC-05", "Looting animé objet par objet (liasses, lingots, diamants) dans un sac ; coffres de PNJ pillables ; moteur d'une voiture peut être neutralisé par balles.", "press_confirmed", "allthings_rubius", "gtavice_flow"),
    fact("MEC-06", "Changement de personnage instantané à proximité, sans zoom satellite ; bascule possible en plein combat véhicule (le partenaire prend le volant).", "press_confirmed", "gtavice_flow", "gta6features"),
    fact("MEC-07", "Focus : ralentit le temps, met en évidence les points faibles (tête, genou, désarmement) ; auto-visée désactivée par défaut, visée personnalisable.", "press_confirmed", "redbull", "shattered", "thebiglead_tips"),
    fact("MEC-08", "Focus libre (presser les deux sticks) révèle un effet audio circulaire signalant une rencontre unique à proximité.", "press_confirmed", "thebiglead_tips"),
    fact("MEC-09", "PNJ réagissent aux armes dégainées ; le personnage range automatiquement son arme dans une foule.", "press_confirmed", "allthings_weapons", "gtabase"),
    fact("MEC-10", "Croquer / ramper, zip-ties, boucliers humains, transport de corps, changement de main pour l'arme : décrits par la presse spécialisée.", "press_confirmed", "shattered", "gtabase"),
    fact("MEC-11", "Intérieurs entrables : les bâtiments en bleu foncé sur la carte ont au moins une porte accessible ; « 700 bâtiments » est une extrapolation non confirmée.", "press_confirmed", "thebiglead_tips", "explained"),
    fact("MEC-12", "Payer 'n' Spray répare et efface l'association véhicule/recherche ; dégâts sur une voiture volée réduisent sa valeur de revente.", "press_confirmed", "redbull", "gtavice_flow"),
    fact("MEC-13", "Séparer Jason et Lucia pendant une poursuite peut faire baisser d'une étoile le niveau de recherche du personnage contrôlé.", "press_confirmed", "redbull", "gtavice_flow"),
    fact("MEC-14", "Pas de mode first-person complet ; conduite vue 3e et 1re personne disponible selon les previews.", "press_confirmed", "gtavice_flow", "gtabase"),
    fact("MEC-15", "Mode histoire solo sans microtransactions (déclaration Rockstar rapportée à Kinda Funny) ; n'inclut pas les futures extensions ni un éventuel online.", "press_confirmed", "explained"),
    fact("MEC-16", "Campagne structurée en 5 chapitres ; ~100 missions pour TrueAchievements ; 50–80 h pour l'histoire principale, ~80 h avec objectifs optionnels, >200 h pour un testeur presse.", "press_confirmed", "gamespot_review", "digitalspy_review", "trueachievements_review", "redbull"),
    fact("MEC-17", "Dialogue contextuel Saluer / Provoquer avec les PNJ, hérité de RDR2 ; interactions avec les animaux (caresser, gronder, étudier).", "press_confirmed", "gta6features", "activities_allthings"),
    fact("MEC-18", "Plus de 600 000 animations annoncées par Rockstar ; cela accroît la variété, pas nécessairement l'intelligence des PNJ.", "press_confirmed", "explained"),
    fact("MEC-19", "Fuites d'août 2026 (build de développement ancien) : systèmes proches de RDR2, mais non représentatifs du jeu final après l'Extended Look du 27/08.", "leak_unverified", "eldorado_leaks"),
    fact("MEC-20", "Rumeur « 201 missions d'histoire » (compte X remus_r) : non confirmée, à ne pas publier comme chiffre.", "leak_unverified", "forbes"),
]

FACTS["weapons"] = [
    fact("WPN-01", "4 armes nommées par Rockstar lui-même : Moreland 850 (fusil à pompe, nom affiché en jeu), revolvers Hawk & Little Morgan, Girardi ES9 (Jason), Klose K17 (Lucia).", "official", "gtaintel_weapons", "store_fr"),
    fact("WPN-02", "18 armes avec preuve de première partie recensées par GTA Intel ; ~15 noms circulant issus des fichiers leaks sont rejetés faute de preuve.", "press_confirmed", "gtaintel_weapons"),
    fact("WPN-03", "Catégories vues : pistolets/revolvers, fusils à pompe, SMG/MG, fusils d'assaut, snipers, armes lourdes (lance-grenades, RPG, fusil-harpon), projectiles (Molotov, grenade, flashbang, fumigène), mêlée, Taser.", "press_confirmed", "allthings_weapons", "gamerant_weapons", "bible"),
    fact("WPN-04", "Personnalisation : chargeurs, silencieux, optiques, lampes, teintes, livrées, munitions spéciales ; armes « partagées » entre Jason et Lucia.", "press_confirmed", "gtabase", "allthings_weapons"),
    fact("WPN-05", "Roue d'armes redessinée en 8 emplacements (armes, outils, projectiles, consommables santé/endurance).", "press_confirmed", "allthings_weapons", "gtavice_flow"),
    fact("WPN-06", "Armes achetées chez Phil's Ammu-Nation ou récupérées sur les ennemis ; le stockage prolongé n'entraîne pas de perte définitive.", "press_confirmed", "allthings_weapons", "gtavice_flow"),
    fact("WPN-07", "Double maniement (dual-wield) NON confirmé ; le choix de la main est confirmé.", "press_confirmed", "gta6features"),
    fact("WPN-08", "gta6bible.com : 28 armes indexées avec provenance ; GTA Intel : 18 seulement avec preuve first-party. Écart dû aux critères d'inclusion.", "community", "bible", "gtaintel_weapons"),
    fact("WPN-09", "Statistiques chiffrées (dégâts, cadence, portée, prix, localisation) par arme : non publiées officiellement avant la sortie.", "post_launch_pending", "endgametools", "gtabase"),
]

FACTS["vehicles"] = [
    fact("VEH-01", "6 véhicules officiellement nommés par Rockstar (contenu Ultime / bonus) : '95 Grotti Cheetah, Vapid Ganado, '67 Vapid Dominator Buggy, Dinka Enduro, Shitzu Squalo, Crest Kayak.", "official", "gta6cartel", "store_fr"),
    fact("VEH-02", "Bonus précommande : Vapid Stanier 1955 + garage.", "official", "store_fr", "actugaming"),
    fact("VEH-03", "Le chiffre « 200+ véhicules » est un décompte de fans mêlant trailers et fuite 2022 ; Rockstar n'a publié aucun nombre. ~100 modèles identifiables sur matériel officiel seul.", "community", "gta6cartel", "gtabase"),
    fact("VEH-04", "gta6guide.fr annonce 185 véhicules identifiés dans les trailers et l'Extended Look ; gta6bible.com en indexe 110 ; vice-city.app 172. Bases communautaires divergentes.", "community", "gta6guide_fr", "bible", "vice_city_app"),
    fact("VEH-05", "Catégories confirmées visuellement : sportives, muscle, SUV, berlines, vans, motos, bateaux (airboat, jet-ski, hors-bord, yacht), avions/hydravions, hélicoptères, véhicules d'urgence, électriques.", "community", "bible", "gta6cartel", "gtabase"),
    fact("VEH-06", "Mécaniques véhicule : intérieurs interactifs (compteurs, éclairage), personnalisation en ateliers spécialisés, garages avec casier d'armes et coffre de butin, livraison du véhicule personnel via une appli.", "press_confirmed", "allthings_rubius", "gtabase"),
    fact("VEH-07", "Vol de voiture : crochetage minijeu au stick, clonage de clé électronique sur modèles sécurisés, scan Focus révélant policiers et valeur du véhicule avant le vol.", "press_confirmed", "allthings_rubius", "shattered"),
    fact("VEH-08", "Supercars volables dès le début si l'on dispose de l'équipement adapté ; pas de verrou de progression artificiel.", "press_confirmed", "gtavice_flow"),
    fact("VEH-09", "Astuce hands-on : pousser un véhicule en marchant contre lui jusqu'au prompt, puis maintenir Carré ; attaque avec la portière (Carré) en voiture, coup de pied sur moto.", "press_confirmed", "thebiglead_tips"),
    fact("VEH-10", "Fiches véhicule chiffrées (vitesse max, accélération, maniabilité, armure, prix, localisation) : non publiées officiellement avant la sortie.", "post_launch_pending", "endgametools"),
]

FACTS["police_and_wanted"] = [
    fact("POL-01", "Retour du système 6 étoiles (GTA V plafonnait à 5) ; confirmé par l'Extended Look et Rob Nelson.", "official", "wanted_gamesreviews", "wanted_fandom", "trueachievements_review"),
    fact("POL-02", "Un crime ne déclenche une recherche QUE s'il est vu par un témoin, signalé par une alarme ou capté par CCTV.", "official", "wanted_tech2geek", "redbull", "wanted_gamesreviews"),
    fact("POL-03", "Le HUD suit séparément : description physique, tenue, véhicule, compagnon, CCTV. Chaque indice s'efface indépendamment.", "press_confirmed", "wanted_fandom", "wanted_tech2geek"),
    fact("POL-04", "Étoiles blanches pleines = poursuite active ; blanches clignotantes = recherche dernière position ; rouges = poursuite rompue mais « Heat » active dans la zone.", "press_confirmed", "wanted_gamesreviews", "wanted_fandom"),
    fact("POL-05", "Changer de tenue complète (magasin ou coffre) efface l'indice vêtement ; changer uniquement chapeau/lunettes ne suffit pas. Changer de coiffure agit sur le signalement physique.", "press_confirmed", "wanted_fandom", "trueachievements_review"),
    fact("POL-06", "Abandonner ou brûler le véhicule identifié retire l'indice véhicule ; détruire les images CCTV et se séparer de son partenaire réduisent la pression.", "press_confirmed", "redbull", "wanted_gamesreviews", "wanted_fandom"),
    fact("POL-07", "Le port d'un masque AVANT le crime empêche l'identification faciale : la prévention coûte moins cher que le nettoyage post-crime.", "press_confirmed", "wanted_tech2geek", "wanted_gamesreviews"),
    fact("POL-08", "À 6 étoiles, la zone de Heat peut couvrir toute la carte ; la police y chasse au profil plutôt qu'à la position.", "press_confirmed", "wanted_tech2geek", "digitalspy_review"),
    fact("POL-09", "Pay 'n' Spray efface l'association véhicule/recherche.", "press_confirmed", "redbull"),
    fact("POL-10", "Comportement par étoile désormais décrit par la presse accréditée : 3/4 étoiles = hélicoptères (qui finissent par manquer de carburant), 5 étoiles = unités NOOSE en Humvees et hélicoptères d'attaque, 6 étoiles = la police poursuit jusqu'à la mort du joueur. Aucun tableau officiel Rockstar publié.", "press_confirmed", "trueachievements_review", "sportskeeda_wanted", "wanted_gamesreviews", note="Détails de presse post-embargo, à recouper en jeu après le 19/11/2026."),
]

FACTS["economy"] = [
    fact("ECO-01", "Trois formes d'argent décrites dans les previews : cash sur soi (perdable), compte ATM / carte, solde numérique BuckMe (protégé).", "press_confirmed", "economy_hustle", "economy_gtanerd"),
    fact("ECO-02", "Butin physique dans un sac, non dépensable directement : revente à des fences spécialisés (bijoux, véhicules, art, contrebande) qui se débloquent en progressant.", "press_confirmed", "economy_gtanerd", "economy_hustle"),
    fact("ECO-03", "Cinq paliers de braquage : supérette/phone shop, bijouterie, banque, compound de gang, fourgons / mini-coups ; chaque niveau change risque et gain.", "press_confirmed", "economy_gtanerd"),
    fact("ECO-04", "Certaines missions d'histoire sont conditionnées à un objectif d'argent (cash gate) : le braquage devient nécessaire à la progression.", "press_confirmed", "economy_gtanerd", "economy_hustle"),
    fact("ECO-05", "Braquages = chaînes de décisions : choix du masque, arbitrage coffre/registre, sortie, estimation sur carte, coût de nettoyage ; dommages réduisent la valeur de revente d'une voiture.", "press_confirmed", "economy_hustle", "gtavice_flow"),
    fact("ECO-06", "Garages achetables (stockage butin, armes, véhicules) ; Rockstar a indiqué qu'acheter une maison n'a pas de sens pour des fugitifs. Pas de revenu passif confirmé.", "press_confirmed", "economy_hustle", "gtabase"),
    fact("ECO-07", "Conseil récurrent : déposer l'argent après chaque coup (ATM / BuckMe) pour ne pas le perdre lors d'une mort ou d'une arrestation.", "press_confirmed", "economy_gtanerd", "economy_hustle"),
    fact("ECO-08", "Hors montants explicitement testés par la presse (abonnement Scooter Bros Premium 12 500 $), les payouts, prix de propriétés et rendements circulant en ligne restent des estimations de fans, non vérifiées.", "speculative", "gta6nerd_tips", "pressstart_economy", note="gta6nerd.com recycle des conseils génériques de GTA V (revenu passif, Pay'n'Spray) : ne pas en dériver de mécaniques GTA VI."),
]

FACTS["activities"] = [
    fact("ACT-01", "Activités confirmées (Wikipedia / Extended Look) : parachutisme, lutte, basket, exercice, kayak, plongée sous-marine.", "official", "wikipedia"),
    fact("ACT-02", "Sports & fitness : basket (R2 pour tirer), musculation (L2/R2 alternés), MMA/cage fighting, backyard wrestling, mini-golf, billard.", "press_confirmed", "activities_allthings", "activities_wiki"),
    fact("ACT-03", "Eau & plein air : pêche, chasse (Mount Kalaga), kayak/canoë, plongée (récifs, épaves), jet-ski, airboat dans les marais.", "press_confirmed", "activities_allthings", "activities_wiki"),
    fact("ACT-04", "Courses : street race, motocross/dirt bike (compteur de tours et position), Gellhorn International Raceway, Thrillbilly Mud Club, courses d'arène type Daytona.", "press_confirmed", "activities_allthings", "activities_wiki"),
    fact("ACT-05", "Stand de tir chronométré (TARGETS REMAINING, par time), skydiving/base-jump, casinos/paris, nightlife (NINE 1 NINE, Jack of Hearts, bars).", "press_confirmed", "activities_allthings", "activities_wiki"),
    fact("ACT-06", "Vie quotidienne : TV, réseaux sociaux in-game, appareil photo du téléphone, nourrir/caresser/étudier les animaux, espionner les voisins, trottinettes électriques.", "press_confirmed", "activities_allthings", "explained"),
    fact("ACT-07", "Le basketball augmente la statistique Focus de Jason ; la salle de sport influe sur muscle/force/endurance.", "press_confirmed", "activities_allthings", "activities_wiki"),
    fact("ACT-08", "Les activités secondaires ne sont pas requises pour finir l'histoire mais comptent dans le 100 %.", "press_confirmed", "activities_allthings"),
]

FACTS["soundtrack_and_radio"] = [
    fact("SND-01", "Justice (Gaspard Augé & Xavier de Rosnay) compose la score originale adaptative — annonce Newswire du 29/10/2026.", "official", "newswire", "wikipedia", "radio_meowdb"),
    fact("SND-02", "6 stations radio officiellement prévisualisées le 08/10/2026 : Cocoteo (latin, El Martillo & La Gata), Back Country (country, MW & Delta Dawne), Afro Bank FM (amapiano, Burna & Palmsy), The Chamber (metal, DJ Kerry & DJ Tom), Flash FM (pop, Robyn & Alex), Dirty South Classics (rap/hip-hop, Trick & Trina).", "official", "newswire", "radio_itech", "radio_rockstarreport"),
    fact("SND-03", "Grand Theft Auto VI: The Album — 34 titres originaux avec Atlantic Records, sortie le 19/11/2026.", "official", "newswire", "radio_itech", "radio_meowdb"),
    fact("SND-04", "9 titres de l'album nommés : That's It (Yung Lean feat. Future & Metro Boomin), RHYNO (Travis Scott), Sexy Magic, Flower in a Hurricane (Justice feat. Tame Impala, SZA, King Gizzard), Last Thing You Need (Morgan Wallen), Suzuki (Fuerza Regida), Macacoa 2000 (Rauw Alejandro), Don't Chart (Cardi B), Bright Lights, Big City (Keith Richards).", "press_confirmed", "radio_rockstarreport", "radio_meowdb"),
    fact("SND-05", "Grand Theft Auto VI: Original Score (Justice) annoncé pour le 11/12/2026, 30 pistes (+ bonus digital), streaming/CD/vinyle ; singles Flower in a Hurricane et Pusher (avec Gesaffelstein).", "press_confirmed", "radio_rockstarreport", "radio_meowdb", "radio_itech", note="Apple Music NZ listait 50 pistes : divergence 30 vs 50, à trancher à la sortie."),
    fact("SND-06", "Flower in a Hurricane = chanson du launch trailer (15/10/2026) ET titre de l'album ; cela ne prouve PAS une diffusion en radio in-game.", "official", "newswire", "radio_itech"),
    fact("SND-07", "Podcasts à la demande confirmés dans l'univers radio ; playlist complète station par station non publiée.", "official", "radio_itech", "radio_rockstarreport"),
    fact("SND-08", "leonidastate.guide propose un « radio tuner » navigateur : outil communautaire, pas une source officielle de tracklist.", "community", "leonidastate"),
]

FACTS["online"] = [
    fact("ONL-01", "Rockstar décrit GTA VI comme une expérience SOLO ; aucun mode en ligne, co-op ou multijoueur au lancement le 19/11/2026.", "official", "online_justjared", "dotesports", "gtabase", "online_webtech"),
    fact("ONL-02", "La fiche PlayStation Store indique 1 joueur et jeu hors-ligne activé.", "official", "online_justjared"),
    fact("ONL-03", "Aucune date, aucun nom, aucun mode, aucune économie annoncés pour un hypothétique « GTA VI Online » ; rumeurs 2027 / décembre 2026 non confirmées.", "official", "online_justjared", "online_webtech"),
    fact("ONL-04", "GTA Online (GTA V) continue d'être supporté ; Take-Two confirme la poursuite du contenu. Aucun transfert de personnage/argent/véhicules annoncé.", "official", "online_justjared", "online_webtech"),
    fact("ONL-05", "Xbox Cloud Gaming et Remote Play = diffusion de jeu solo, pas une preuve de multijoueur.", "official", "online_webtech"),
    fact("ONL-06", "Un « format online 32 joueurs » a été évoqué dans un dossier prud'homal à Glasgow : ce n'est pas une annonce produit.", "leak_unverified", "online_webtech"),
    fact("ONL-07", "GTABase déduit de l'absence d'online que « le prochain GTA Online sera un jeu standalone » : inférence éditoriale, pas une déclaration Rockstar.", "speculative", "gtabase"),
    fact("ONL-08", "Page P14 (GTA VI Online) du site doit être un hub de statut officiel + rumeurs étiquetées, PAS un guide de modes inexistants.", "post_launch_pending", "online_justjared", "endgametools"),
]

FACTS["cheats"] = [
    fact("CHT-01", "Rockstar n'a PAS publié de liste officielle de codes de triche au 18/11/2026 ; en revanche GameSpot et Press-Start ont testé les cheats sur copies de review post-embargo.", "press_confirmed", "gamespot_cheats", "pressstart_cheats", note="Ne jamais présenter ces listes comme « officielles Rockstar » : ce sont des relevés de presse accréditée, encore partiels."),
    fact("CHT-02", "Avant l'embargo du 18/11/2026, les « listes de cheats GTA 6 » en ligne recyclaient GTA V ou étaient inventées (UNCONFIRMED). Après l'embargo, GameSpot et Press-Start publient des listes issues de copies de review, encore évolutives.", "press_confirmed", "cheats_gtasix", "cheats_gta6cheatcodes", "gamespot_cheats", "pressstart_cheats"),
    fact("CHT-03", "Risque de sécurité : les téléchargements promettant des « cheats GTA 6 » pré-lancement sont des leurres malware.", "press_confirmed", "cheats_gtasix"),
    fact("CHT-04", "Saisie vérifiée par la presse : ouvrir le téléphone iFruit, maintenir L1 + R1 puis composer la séquence à la croix directionnelle. Terminer l'histoire au moins une fois est un prérequis. L'impact sur les trophées reste à recouper.", "press_confirmed", "gamespot_cheats", "pressstart_cheats", "endgametools", note="GameSpot précise avoir chargé une sauvegarde vierge pour tester l'échec des codes avant la fin de l'histoire."),
]

FACTS["missions_endings_trophies"] = [
    fact("MIS-01", "Campagne en 5 chapitres, ~100 missions selon TrueAchievements ; heists majeurs traités comme des séquences de film Michael Mann.", "press_confirmed", "gamespot_review", "trueachievements_review"),
    fact("MIS-02", "Durée : 50–80 h pour l'histoire, ~80 h avec objectifs optionnels (Rob Nelson), >200 h pour un testeur de Digital Spy.", "press_confirmed", "digitalspy_review", "trueachievements_review", "redbull"),
    fact("MIS-03", "Liste nominative exhaustive des missions avec synopsis, récompenses et stratégies : non publiée officiellement.", "post_launch_pending", "endgametools", "actugaming"),
    fact("MIS-04", "Fins alternatives : Rockstar a évoqué des objectifs optionnels ayant des répercussions narratives, mais n'a PAS confirmé de fins multiples.", "press_confirmed", "explained"),
    fact("MIS-05", "Datamine TexFunz2 (07/11/2026) : 55 succès configurés (54 valeurs 1–54 + une à 1000). Aucun nom officiel.", "leak_unverified", "yaninagames", "gamebyte", "psnprofiles"),
    fact("MIS-06", "La « liste complète des 55 trophées » diffusée sur X le 08/11 (Welcome to Vice, Florida Man, etc.) est jugée probablement FAKE par PSNProfiles et la communauté : mentions de difficulté hard et de co-op absentes du jeu, ton générique type IA.", "leak_unverified", "psnprofiles", "gamebyte", "yaninagames"),
    fact("MIS-07", "Le 18/11/2026, PC Gamer et Press-Start publient une liste DIFFÉRENTE (Vice Got a Price!, Just Like Paradise, Breakfast Run, The Cartel Heist, VCIA Takedown, WAiNK It à 100 lieux…), cohérente avec des copies de review post-embargo.", "press_confirmed", "pcgamer_trophies", "pressstart_trophies", note="Crédibilité supérieure à la rumeur du 08/11 mais nécessite recoupement avec les listes PSN/Xbox officielles avant publication comme « confirmé »."),
    fact("MIS-08", "Deux listes de trophées incompatibles circulent ; arbitrage S2 après fetch direct : la liste Press-Start / PC Gamer du 18/11/2026 est cohérente avec une copie de review et bien plus crédible que la rumeur générique du 08/11, mais elle reste NON officielle et doit être recoupée avec PSN / Xbox.", "press_confirmed", "pcgamer_trophies", "pressstart_trophies", "psnprofiles"),
    fact("MIS-09", "Aucune liste officielle PSN / Xbox de trophées ou succès publiée au 18/11/2026.", "official", "yaninagames", "endgametools"),
]

FACTS["easter_eggs_and_secrets"] = [
    fact("EGG-01", "Rockstar n'a officiellement nommé AUCUN easter egg de GTA VI.", "official", "easteregg_life"),
    fact("EGG-02", "Clins d'œil repérés dans le matériel officiel : Ocean View Hotel (Trailer 1), Phil's Ammu-Nation et gecko en chemise de Vercetti (Trailer 2), Sea Sparrow + moto + supercar jaune aux emplacements de la jaquette 2002, décor RDR2 près d'Annesburg dans la pub « Prairie Sandwich Box Meal » (Extended Look).", "press_confirmed", "easteregg_life", "easteregg_earlygame"),
    fact("EGG-03", "Hawk & Little Morgan Revolvers « sourcés du Vercetti Estate » avec gravures de palmiers (Ultime) ; autocollant Fleeca sur le frigo de Jason ; sticker Everett Morgan (RDR Online).", "press_confirmed", "easteregg_earlygame", "gtaintel_weapons"),
    fact("EGG-04", "Référence Liberty City dans le profil officiel de Lucia ; iguane peint portant la chemise de Tommy Vercetti.", "press_confirmed", "easteregg_earlygame", "gtaboss_chars"),
    fact("EGG-05", "Rumeurs non validées : QR code / ARG caché dans un trailer, codes sur les panneaux publicitaires.", "leak_unverified", "easteregg_life"),
    fact("EGG-06", "Fuite 2022 : événements « Missing Tourists », Skunk Ape, UFO, fantômes, ~1 600 random events. Build de développement ancien, non représentatif.", "leak_unverified", "reddit_mysteries", "eldorado_leaks"),
    fact("EGG-07", "Mystères communautaires anticipés dans Grassrivers / Mount Kalaga (créatures, épaves, lampadaire, etc.) : souhaits de fans, pas du contenu confirmé.", "community", "reddit_mysteries"),
    fact("EGG-08", "YouTube : vidéos « 100+ hidden details » (29/08/2026) et « 41 Easter Eggs » pré-lancement = analyses de trailers, pas de découvertes in-game.", "community", "yt_hidden"),
    fact("EGG-09", "Easter eggs découverts en jeu par la communauté : n'existent pas encore au 18/11/2026.", "post_launch_pending", "endgametools", "easteregg_life"),
]

FACTS["tips_strategies_techniques"] = [
    fact("TIP-01", "Avant un braquage : enfiler un masque empêche l'identification faciale, bien plus efficace que de nettoyer les indices après coup.", "press_confirmed", "wanted_tech2geek", "wanted_gamesreviews"),
    fact("TIP-02", "Fuite : surveiller les ICÔNES sous les étoiles, pas seulement le nombre d'étoiles ; chaque indice (visage, tenue, CCTV, véhicule, compagnon) se traite séparément.", "press_confirmed", "wanted_fandom", "wanted_tech2geek"),
    fact("TIP-03", "Changer de TENUE COMPLÈTE (magasin ou coffre du véhicule personnel) — un simple chapeau ou des lunettes ne suffit pas.", "press_confirmed", "wanted_fandom", "trueachievements_review"),
    fact("TIP-04", "Abandonner/brûler le véhicule repéré fait disparaître l'icône véhicule ; une voiture de police peut alors passer sans reconnaître le nouveau véhicule.", "press_confirmed", "redbull", "wanted_gamesreviews"),
    fact("TIP-05", "Se séparer de Jason/Lucia pendant la poursuite divise l'attention policière et peut retirer une étoile au personnage contrôlé.", "press_confirmed", "redbull", "gtavice_flow"),
    fact("TIP-06", "Anticiper le plein : le carburant se vide lentement, mais voler une voiture déjà basse peut coincer en pleine poursuite ; repérer les stations (elles réparent aussi).", "press_confirmed", "gtavice_flow", "redbull"),
    fact("TIP-07", "Avant de voler : utiliser le scan Focus pour voir les policiers proches et la valeur du véhicule ; viser le moteur d'une voiture adversaire pour l'immobiliser.", "press_confirmed", "allthings_rubius"),
    fact("TIP-08", "Préparer son loadout : 2 longues + 2 poings seulement, le reste dans le coffre. Revenir au véhicule pour changer d'armes en cours de mission.", "press_confirmed", "wikipedia", "gtavice_flow"),
    fact("TIP-09", "Stocker des tenues de rechange dans le coffre : change d'apparence immédiat pour casser un signalement.", "press_confirmed", "gtavice_flow", "trueachievements_review"),
    fact("TIP-10", "Argent : déposer au plus vite (ATM puis BuckMe) après chaque coup ; le cash transporté se perd à la mort / arrestation.", "press_confirmed", "economy_gtanerd", "economy_hustle"),
    fact("TIP-11", "Prioriser les missions d'histoire au début : elles débloquent outils de vol, relations avec les fences et accès aux braquages à plus forte valeur ; certaines sont conditionnées à un capital.", "press_confirmed", "economy_hustle", "ofzen_launchday"),
    fact("TIP-12", "Investir dans l'infrastructure (outils de vol, véhicule de fuite sans traceur, garage, Pay 'n' Spray, coiffeur/barbier) avant les cosmétiques.", "press_confirmed", "economy_hustle"),
    fact("TIP-13", "Ne pas endommager un véhicule destiné à la revente : les dégâts réduisent directement le prix chez le fence.", "press_confirmed", "gtavice_flow"),
    fact("TIP-14", "Focus libre (L3+R3) : un halo audio circulaire signale une rencontre unique à proximité ; explorer ces signaux plutôt que foncer aux marqueurs.", "press_confirmed", "thebiglead_tips", "shattered"),
    fact("TIP-15", "Carte : les bâtiments en bleu FONCÉ sont entrables ; faire pivoter la carte pour repérer les portes.", "press_confirmed", "thebiglead_tips"),
    fact("TIP-16", "Pousser un véhicule bloqué en marchant contre lui jusqu'au prompt, puis maintenir Carré ; portière = attaque (Carré en voiture), coup de pied sur moto (utile en course).", "press_confirmed", "thebiglead_tips"),
    fact("TIP-17", "Bascule de personnage en pleine poursuite à moto : le partenaire prend le guidon pendant que le joueur tire.", "press_confirmed", "gtavice_flow"),
    fact("TIP-18", "Entretenir la relation Jason/Lucia (sorties, gym, shopping, messages) : système de role-play sans bonus de stats directs, mais influence certaines situations de mission.", "press_confirmed", "redbull", "wikipedia"),
    fact("TIP-19", "Entretenir la condition physique (sommeil, gym, alimentation) : poids, muscle et fatigue modifient l'apparence et les attributs.", "press_confirmed", "wikipedia", "gtavice_flow"),
    fact("TIP-20", "YouTube : « 106 Tips & Tricks » (12/11), « 12 choses à faire Day 1 » (22/10), « Ultimate Pre-Launch Guide » (14/11), playlist Tips & Tricks. Contenu pré-sortie basé sur previews : à étiqueter communautaire, à re-vérifier après le 19/11.", "community", "yt_106tips", "yt_day1", "yt_prelaunch", "yt_playlist"),
    fact("TIP-21", "Une vidéo « 100% Walkthrough Part 1 » datée du 15/11/2026 (avant la sortie) circule : origine douteuse, ne pas en extraire de stratégies comme vérifiées.", "community", "yt_walkthrough", note="Signal de contenu pré-launch potentiellement généré / fuite."),
    fact("TIP-22", "GrandTheft.gg publie le 18/11/2026 une dizaine de guides « how to get armored cars / weapon locations / police stations / safehouses » : publiés avant l'accès public au jeu, donc à traiter comme non vérifiés.", "community", "grandtheft", note="Risque majeur de contenu spéculatif généré en masse."),
    fact("TIP-23", "Test presse 140 h (TheBigLead, 18/11) : 8 astuces issues d'une vraie session de review — source de tips la plus solide de la journée.", "press_confirmed", "thebiglead_tips"),
]

FACTS["press_reviews"] = [
    fact("REV-01", "Embargo critiques levé le 18/11/2026 vers 11:00 GMT, calé sur le déblocage néo-zélandais.", "press_confirmed", "maketecheasier_reviews", "dexerto"),
    fact("REV-02", "Metascore PS5 = 99, « Universal Acclaim » / « Must-Play », à égalité avec Ocarina of Time. Compteur passé de 100 (11:10 GMT) à 109 puis 146 critiques dans la journée : INSTANTANÉ ÉVOLUTIF.", "press_confirmed", "metacritic", "maketecheasier_reviews", "dexerto", "vgtimes", note="À horodater systématiquement sur la page News."),
    fact("REV-03", "Xbox Series X : 99 (9 critiques au relevé de 11:10 GMT). Score utilisateur encore « tbd » ; fausses notes utilisateurs nettoyées.", "press_confirmed", "maketecheasier_reviews", "dexerto"),
    fact("REV-04", "Notes individuelles : IGN 10, Game Informer 10, GameSpot 10, Push Square 10, IGN France 100, Everyeye.it 100, ScreenRant 10 ; note la plus basse relevée 80 (ScreenHub).", "press_confirmed", "metacritic", "gamespot_review", "screenrant_review", "independent"),
    fact("REV-05", "Critique récurrente : 30 FPS sans mode 60 même sur PS5 Pro ; quelques objets flottants et rares chutes de framerate, aucun crash ni bug bloquant selon The Independent.", "press_confirmed", "independent", "pushsquare", "ign_30fps"),
    fact("REV-06", "Éloges convergents : densité du monde, duo Jason/Lucia, animations, météo, heists ; réserve sur un rythme qui s'essouffle en fin de campagne.", "press_confirmed", "gamespot_review", "digitalspy_review", "screenrant_review"),
    fact("REV-07", "Avant le 18/11, tout « Metascore GTA 6 » circulant était faux ; plusieurs sites avaient documenté ces rumeurs.", "press_confirmed", "metacritic", "dexerto"),
]

FACTS["community_tools_and_social"] = [
    fact("COM-01", "GitHub navanem/gta6-leonida-atlas : atlas open-source local-first, 2 204 lieux, Vite+React+TypeScript, Leaflet, Zustand, Dexie/IndexedDB, Three.js, licence AGPL-3.0 ; données GTADB sous CC BY 4.0.", "community", "github_atlas"),
    fact("COM-02", "GitHub cleementt26/leonida-atlas : atlas FR, fond de carte © YANIS V16 & GTA VI Mapping Community via GTADB (CC BY 4.0), filtres de fiabilité, tactile.", "community", "github_atlas_fr"),
    fact("COM-03", "GitHub rhyovar/leonida-dispatch : companion app (countdown, carte 6 comtés, cast dossier, tracker localStorage) ; l'auteur signale explicitement ses données tracker/database/collectibles comme « placeholder » et son crew planner comme spéculatif.", "community", "github_dispatch"),
    fact("COM-04", "GitHub gta6mapx/gta6mapx : carte interactive « evidence-labeled intel ».", "community", "github_mapx"),
    fact("COM-05", "X @RockstarGames : 10/11 préchargement disponible, 12/11 « plus qu'une semaine » et disponibilité des boîtes avec code en magasin.", "official", "rockstar_x", "newswire"),
    fact("COM-06", "The Weather Channel (@weatherchannel) : thread X du 16/11/2026 à 20:40 UTC, 6 screenshots officiels Rockstar + prévisions fictives pour Leonida.", "official", "weather_mte", "weather_endgame"),
    fact("COM-07", "Reddit r/GTA6 : thread « GTA VI Mysteries » (2025) sur les souhaits de mystères et les events des leaks 2022 ; r/gta6game : discussions PC/performances et réactions mitigées aux previews.", "community", "reddit_mysteries", "reddit_gta6game", note="Recherche Reddit ciblée peu productive ce jour : à approfondir après le 19/11 quand les vrais retours arriveront."),
    fact("COM-08", "leonidastate.guide est « built in public » et diffuse aussi sur TikTok, YouTube @sokragta, Twitch, Instagram, Threads, X, Bluesky, Discord.", "community", "leonidastate"),
    fact("COM-09", "Newswire Rockstar, calendrier officiel récent : 03/11 pré-load, 05/11 Launch Gallery, 09/11 GTA VI: The Festival (Miami), 10/11 Pre-Load Now, 29/10 Score by Justice, 15/10 Launch Trailer, 08/10 Radio Stations, 24/09 Vice City Collection, 17/09 The Album.", "official", "newswire", "gta6guide_fr"),
    fact("COM-10", "La recherche Instagram @rockstargames n'a pas renvoyé de résultats exploitables ce jour ; la Launch Gallery officielle (05/11) reste la source de screenshots haute résolution.", "official", "newswire", "rockstar_vi"),
]

FACTS["unavailable_post_launch"] = [
    fact("N/A-01", "Liste exhaustive et officielle des missions (noms, synopsis, récompenses, stratégies).", "post_launch_pending", "actugaming", "endgametools"),
    fact("N/A-02", "Fins alternatives détaillées et conditions de déclenchement.", "post_launch_pending", "explained"),
    fact("N/A-03", "Publication officielle Rockstar de la liste exhaustive des cheats, de l'impact trophées et des codes encore manquants : toujours en attente. Les listes GameSpot / Press-Start du 18/11/2026 sont partielles et évolutives.", "post_launch_pending", "cheats_gtasix", "gamespot_cheats", "pressstart_cheats"),
    fact("N/A-04", "Liste officielle PSN / Xbox des trophées et succès + stratégies associées : toujours en attente. La liste de presse du 18/11 (55 trophées, Platinum « Vice Got A Price! ») reste à recouper.", "post_launch_pending", "yaninagames", "endgametools", "pressstart_trophies"),
    fact("N/A-05", "Collectibles : noms, localisations exactes et récompenses OFFICIELS. Une checklist 100 % de presse a été publiée le 18/11/2026, mais les coordonnées in-game et le recoupement communautaire restent post-lancement.", "post_launch_pending", "endgametools", "pressstart_100"),
    fact("N/A-06", "Easter eggs et mystères découverts EN JEU par la communauté.", "post_launch_pending", "easteregg_life", "endgametools"),
    fact("N/A-07", "Statistiques chiffrées complètes de toutes les armes et de tous les véhicules.", "post_launch_pending", "endgametools", "bible"),
    fact("N/A-08", "GTA VI Online : modes, missions coop, économie, Shark Cards, progression.", "post_launch_pending", "online_justjared"),
    fact("N/A-09", "Historique des patches / mises à jour post-lancement.", "post_launch_pending", "vgtimes"),
    fact("N/A-10", "Scores critiques définitifs et note utilisateurs Metacritic stabilisée.", "post_launch_pending", "metacritic"),
    fact("N/A-11", "Carte officielle complète de Leonida publiée par Rockstar (seule une reconstruction communautaire existe).", "post_launch_pending", "dotesports", "endgametools"),
    fact("N/A-12", "Glitches / exploits légaux découverts post-lancement.", "post_launch_pending", "endgametools"),
]


# ─── S2_VERIFIED_FACTS ───────────────────────────────────────────────────────
# Faits vérifiés par fetch direct le 18/11/2026 après la levée d'embargo.
# Statut `press_confirmed` par défaut : Rockstar n'a PAS publié ces listes.
# ─────────────────────────────────────────────────────────────────────────────

FACTS["release_and_platforms"] += [
    fact("REL-13", "Déblocage à minuit heure locale, sans early access : les joueurs néo-zélandais accèdent au jeu ~13 h avant le Royaume-Uni ; The Independent recommande d'éviter Internet dès 11 h GMT le 18/11 pour esquiver les spoilers.", "press_confirmed", "independent", "newswav_live"),
    fact("REL-14", "Une mise à jour firmware PS5 est obligatoire avant de pouvoir lancer GTA VI : PlayStation Support US l'a confirmé sur X le 18/11/2026 à 01 h 25, sans détailler le patch (sécurité).", "press_confirmed", "independent", "newswav_live"),
    fact("REL-15", "Second patch pré-lancement version 1.002.001 / 1.0.2.1 : 602,5 Mo sur PS5, 1,59 Go sur Xbox Series, déploiement PS5 progressif. Rockstar n'a publié AUCUNE note de patch ; installation obligatoire avant le 19/11.", "press_confirmed", "rockstarintel_patch", "ggrecon_patch", "mte_patch", "newswav_live", note="Ne pas confondre avec les ~212 Go du préchargement initial ni avec le firmware PS5 système."),
]

FACTS["editions_and_pricing"] += [
    fact("EDI-10", "Tarifs UK relevés le 18/11/2026 : Standard PS5 69,99 £ (64,99 £ en promo Argos), Ultimate PS5/Xbox 89,99 £. Ce sont des prix revendeurs UK, pas les tarifs officiels FR.", "press_confirmed", "independent", "newswav_live"),
    fact("EDI-11", "Contenu du pack Vintage Vice City détaillé par The Independent : Vapid Stanier 1955, garage Shore Court près d'Ocean Beach, 2 tenues Vice City, coiffures vintage, skin d'arme tropical inspiré de la chemise de Tommy Vercetti. Dernier jour de précommande le 18/11.", "press_confirmed", "independent", "newswav_live"),
    fact("EDI-12", "Ultimate Edition : véhicules exclusifs ('67 Vapid Dominator Buggy, '95 Grotti Cheetah, Dinka Enduro, Crest Kayak, Shitzu Squalo), mods Ganado, ateliers Rideout Customs et One-Eyed Willie's, mais AUSSI missions, vêtements et options de personnalisation exclusifs selon The Independent.", "press_confirmed", "independent", "store_fr", note="Croiser avec la fiche Rockstar Store FR (EDI-06) ; la liste presse ajoute des missions exclusives non détaillées sur le Store."),
]

FACTS["story_and_characters"] += [
    fact("CHA-14", "TrueAchievements décrit Jason comme ancien « Special Forces Marauder » et petit trafiquant, Lucia sortant de prison ; le duo démarre comme simples coursiers avant de monter en puissance (vols de voitures, commerces, bijouteries, banques).", "press_confirmed", "trueachievements_review"),
    fact("CHA-15", "Système de « Criminal Profile » : cinq profils par protagoniste, de Professional (crimes propres, sans victimes) à Irredeemable (trait permanent déclenché par la violence excessive et les exécutions). Le profil influence la relation et les performances.", "press_confirmed", "trueachievements_review", note="Source = test Xbox Series X ~80 h de Tom West ; pas de fiche officielle Rockstar détaillant les 5 seuils."),
    fact("CHA-16", "La relation Jason/Lucia se dégrade si le joueur ne les fait pas passer du temps ensemble, ne répond pas aux appels ou néglige les gestes comme se tenir la main ; un tireur non létal met un ennemi au sol, l'exécuter reste un choix plus sombre.", "press_confirmed", "trueachievements_review", "gamespot_cheats"),
    fact("CHA-17", "Cal, Raul, Andy, Kenton, Billy, Randy, Tyrone et Bret apparaissent dans les listes de missions / trophées de presse du 18/11 ; ils ne font PAS partie des 8 profils officiels Rockstar et doivent être badgés « presse / à recouper ».", "press_confirmed", "pressstart_trophies", "pressstart_missions", note="Éviter de fusionner cette liste avec le cast officiel CHA-03."),
]

FACTS["map_and_regions"] += [
    fact("MAP-13", "Lieux nommés par la presse post-embargo : Mile Zero airstrip (chars, véhicules blindés, gunships), Vice City Airport / VCIA et Mike Zero Air Station (zones restreintes à 5 étoiles), Gellhorn Raceway, Thrillbilly Mud Club, Boone Speedway, Ocean Beach, Key Lento, Sinfrontera National Bank.", "press_confirmed", "trueachievements_review", "sportskeeda_wanted", "gamespot_cheats", "pressstart_missions", note="Noms issus de guides presse, PAS d'une carte officielle publiée par Rockstar."),
    fact("MAP-14", "Réseau de transport rapide décrit par GameSpot : RydeMe (trajet + 100 $ pour arriver instantanément), bus et trains avec horaires, et bascule de personnage qui ramène près de la planque — il n'existe PAS de fast travel par simple point sur la carte.", "press_confirmed", "gamespot_tips"),
    fact("MAP-15", "« Hot Areas » : après rupture du contact visuel, certaines zones deviennent temporairement interdites ; y revenir trop tôt fait reconnaître le joueur et relance la poursuite. Mécanique comparée à Red Dead Redemption 2 par Sportskeeda.", "press_confirmed", "sportskeeda_wanted"),
]

FACTS["gameplay_mechanics"] += [
    fact("MEC-21", "Trois statistiques centrales : Health, Stamina, Focus. Musculation = santé, course/vélo/kayak = endurance, pêche/billard/méditation = Focus (gain permanent). Manger, dormir et se doucher donnent des buffs temporaires signalés par cœur rose / éclair bleu / œil violet.", "press_confirmed", "gamespot_tips"),
    fact("MEC-22", "Aller à la salle EN COUPLE fait progresser Jason ET Lucia simultanément, quel que soit le personnage contrôlé ; l'appli fitness suit une fenêtre d'entraînement qui se rouvre environ chaque jour in-game.", "press_confirmed", "gamespot_tips", "gamespot_gym"),
    fact("MEC-23", "Focus libre (L3 + R3) colore les ennemis en rouge, les objets interactifs en jaune et l'argent en vert ; il révèle les ennemis à travers les murs, les notes contenant des codes de coffre, les traces d'animaux et les objets de valeur dans un coffre.", "press_confirmed", "gamespot_tips", "gamespot_robberies"),
    fact("MEC-24", "Vol de véhicule : l'appli WAiNK (croix directionnelle Haut) affiche système de sécurité, prix de revente et coût d'immatriculation. Alarmes, traceurs standards et traceurs avancés (ping police si déplacement) ; voitures haut de gamme = cloner de clé, immatriculation au Pay 'n' Spray, livraison via Scooter Bros.", "press_confirmed", "gamespot_tips", "gamespot_dualsense"),
    fact("MEC-25", "Braquages : niveau de sécurité Low / Medium / High sur la carte ; contrôle de la foule, désactivation de l'alarme via panneau blanc, destruction ou neutralisation CCTV, puis caisse et arrière-salle. Le Snap Gun (déblocage histoire) ouvre les serrures sans alarme.", "press_confirmed", "gamespot_robberies"),
    fact("MEC-26", "Codes de coffre ALÉATOIRES : GameSpot confirme sur plusieurs parties qu'ils changent d'un joueur à l'autre et d'un braquage à l'autre, y compris pour un même commerce. Aucune liste statique de codes n'est fiable ; utiliser Focus pour trouver notes / écrans / gardes.", "press_confirmed", "gamespot_robberies", note="Conséquence directe pour P11/P12 : ne JAMAIS publier de « liste de safe codes »."),
    fact("MEC-27", "Butins de banque : billets marqués avec packs de teinture à revendre à un fence ; le brouilleur de pack de teinture se débloque au Chapitre 3. Caméras « cloud » = preuves indestructibles, donc à détruire avant d'être vu ; les coffres-forts de grande banque s'ouvrent brièvement à l'arrivée d'un fourgon blindé.", "press_confirmed", "gamespot_robberies"),
    fact("MEC-28", "Sur PS5, les gâchettes adaptatives DualSense opposent une résistance à l'approche de la limite de vitesse : aide pour circuler légalement sans attirer la police, sans empêcher de dépasser la limite.", "press_confirmed", "gamespot_dualsense"),
    fact("MEC-29", "Vol de voiture de base : Slim Jim + mini-jeu de démarrage (« hotwire ») décrits par TrueAchievements ; les outils plus avancés se débloquent au fil de l'histoire.", "press_confirmed", "trueachievements_review", "gamespot_tips"),
]

FACTS["weapons"] += [
    fact("WPN-10", "Noms d'armes / objets issus des cheats de presse : Mason & Keen Shortstraw (fusil à pompe explosif), Hauners H-AT, MTL Pumper, Hauners P-996 LAZER, Hauners Rhino Tank. Ce sont des entrées du menu Progress / de cheats, pas une liste d'armes officielle.", "press_confirmed", "gamespot_cheats", "pressstart_cheats", note="Ne pas confondre avec les 4 armes nommées par Rockstar (WPN-01)."),
]

FACTS["vehicles"] += [
    fact("VEH-11", "Véhicules invoquables par cheats après défis : Interstate Ambulance, Airboat 09, Bravado Banshee, Tuff BMX, Maibatsu Boomazoom, Nagasaki Carbon RS, '65 Vapid Dominator, Progen Emerus, Inflatable Flamingo, MTL Pumper, Vapid Stanier G2 Taxi, Hauners P-996 LAZER, HVY Bulldozer, Lapwing Mallard, Brimstone Golfer, Hauners Rhino Tank, Maibatsu Sanchez, Nagasaki Sea Sparrow, Speeder 700 GT, Truffade Thrax, Western Zombie Bobber.", "press_confirmed", "gamespot_cheats", "pressstart_cheats", note="Liste de presse partielle, plusieurs codes « TBC » chez Press-Start ; ne pas présenter comme catalogue officiel Rockstar."),
    fact("VEH-12", "Scooter Bros : service de livraison du véhicule assigné ; l'abonnement Premium coûte 12 500 $ et offre 3 dépôts gratuits par jour in-game selon Press-Start. Le jeu facture sinon jusqu'à plusieurs centaines de dollars selon la distance.", "press_confirmed", "pressstart_economy", "gamespot_dualsense"),
]

FACTS["police_and_wanted"] += [
    fact("POL-11", "Sportskeeda : abattre un policier déclenche immédiatement 3 étoiles ; pénétrer dans une zone restreinte (Vice City Airport / Mike Zero Air Station) donne 5 étoiles ; prolonger l'affrontement en tuant des policiers mène à 6 étoiles. Les deux protagonistes peuvent partager le même niveau de recherche.", "press_confirmed", "sportskeeda_wanted", note="Procédure décrite par un guide presse, pas par Rockstar ; à recouper en jeu."),
    fact("POL-12", "Fuite : briser la ligne de vue fait passer les étoiles au ROUGE (recherche toujours active) ; changer d'apparence / tenue / voiture / armes et éviter les « Hot Areas » permet de faire retomber la Heat.", "press_confirmed", "sportskeeda_wanted", "wanted_fandom"),
    fact("POL-13", "Le coffre du véhicule sert d'inventaire de fuite : jusqu'à 5 tenues, l'armurerie complète et des sacs de drogue, bijoux ou billets marqués. Changer de tenue ou retirer chapeau / lunettes modifie l'identification visuelle.", "press_confirmed", "trueachievements_review"),
    fact("POL-14", "TrueAchievements : à 3/4 étoiles les hélicoptères poursuivent mais doivent rentrer faute de carburant ; à 5 étoiles, NOOSE en Humvees avec mitrailleuses + hélicoptères d'attaque ; à 6 étoiles, message explicite « la police ne s'arrêtera qu'après votre mort ».", "press_confirmed", "trueachievements_review"),
    fact("POL-15", "Mile Zero airstrip : chars, blindés, gunships et véhicules militaires disponibles pour prolonger un 6 étoiles. Zone citée par TrueAchievements ; Sportskeeda orthographie « Mike Zero Air Station » : divergence de nom à signaler.", "press_confirmed", "trueachievements_review", "sportskeeda_wanted", note="Arbitrage : afficher les deux graphies avec badge « presse » jusqu'à recoupement in-game."),
]

FACTS["economy"] += [
    fact("ECO-09", "Press-Start : revendre des voitures volées à un revendeur (Moses ou autre) est le revenu rapide le plus sûr ; braquages de gang / commerces plus risqués, braquages de coffres de banque = plus gros gains mais poursuite brutale.", "press_confirmed", "pressstart_economy", "gamespot_tips"),
    fact("ECO-10", "L'argent existe en cash sur soi, compte bancaire / carte via ATM et épargne long terme BuckMe. Le cash physique se perd définitivement à la mort ou à l'arrestation : déposer après chaque coup.", "press_confirmed", "pressstart_economy", "economy_hustle"),
    fact("ECO-11", "Piège économique vérifié : alimenter trop tôt l'épargne BuckMe à long terme peut bloquer des quêtes exigeant un capital disponible (« cash gate »). Press-Start conseille de reporter cette épargne tant que des dépenses d'histoire sont possibles.", "press_confirmed", "pressstart_economy"),
    fact("ECO-12", "Scooter Bros Premium (12 500 $, 3 livraisons gratuites / jour in-game) est présenté comme un investissement rentable malgré son coût initial ; les petits vols de piétons restent des appoints, pas un revenu structurant.", "press_confirmed", "pressstart_economy"),
    fact("ECO-13", "GameSpot : les braquages de commerces, restaurants et PNJ sont la principale source de revenus ; les établissements ont un niveau de sécurité et trois points à gérer (foule, alarme, caméras).", "press_confirmed", "gamespot_tips", "gamespot_robberies"),
]

FACTS["activities"] += [
    fact("ACT-09", "Activités testées par TrueAchievements : défis de pêche, plongée sur épaves, mud racing, mini-golf, et « traîner un distributeur de billets derrière soi » pendant une poursuite. Des buffs et de l'argent récompensent les activités.", "press_confirmed", "trueachievements_review"),
    fact("ACT-10", "Checklist 100 % de presse : 100 tâches optionnelles, 39 opérations de gang, 22 braquages de banque, 34 smash'n'grabs, 50 stick-ups, 100 emplacements WAiNK, 15 points de méditation, 100 flamants cocaïne, 300 stunts, 70 challenges, 200 véhicules de base, 50 armes standard et 100 animaux à découvrir.", "press_confirmed", "pressstart_100", note="Liste masquée jusqu'au générique de fin : SPOILER MAJEUR, à placer derrière SpoilerToggle. Chiffres de presse, pas de checklist officielle Rockstar."),
    fact("ACT-11", "Le basketball, la pêche, le billard et la méditation augmentent Focus ; la salle de sport et le cardio augmentent Health / Stamina. Les anneaux de fitness se ferment environ une fois par jour in-game.", "press_confirmed", "gamespot_tips", "trueachievements_review"),
]

FACTS["soundtrack_and_radio"] += [
    fact("SND-09", "Deux éditions vinyle annoncées : « GTA VI: The Album » (34 titres, artistes dont Travis Scott, PinkPantheress, Yung Lean, Keith Richards) à 44,99 £ chez Amazon UK, édition exclusive 2 vinyles rose/violet splatter + gatefold + poster, expédition le 20/11/2026.", "press_confirmed", "newswav_live", "newswire", note="Prix et variante Amazon UK : ne pas confondre avec un prix officiel FR."),
]

FACTS["cheats"] += [
    fact("CHT-05", "Prérequis vérifié : terminer l'histoire au moins une fois. GameSpot a chargé une sauvegarde vierge pour confirmer qu'aucun code ne fonctionne avant le générique de fin.", "press_confirmed", "gamespot_cheats", "pressstart_cheats"),
    fact("CHT-06", "Après activation d'un cheat, GameSpot indique qu'il n'est plus possible de sauvegarder la partie. Les défis déjà accomplis avant la fin de l'histoire sont pris en compte au moment du déblocage.", "press_confirmed", "gamespot_cheats"),
    fact("CHT-07", "Les cheats sont classés dans un onglet dédié du menu après l'histoire, par catégories, chacun avec une condition et une séquence directionnelle qui n'apparaît qu'une fois le défi rempli.", "press_confirmed", "pressstart_cheats", "gamespot_cheats"),
    fact("CHT-08", "Joueur : 250 000 $ (Up, Right, Down, Left, Up, Left, Down, Right), Drunk (2 500 $ d'alcool), Raise Heat Level (perdre 3 étoiles 25 fois), Raise Wanted Level (50 fois), Unlimited Focus, No Fall Damage (20 chutes de ~12 m), Parachute (50 sauts ≥ 91,5 m), Body Armor (100 workouts), Repair Vehicle (10 victoires sur 3 circuits), Unlimited Nitrous (50 stunt jumps).", "press_confirmed", "gamespot_cheats", "pressstart_cheats", note="Certaines saisies restent « TBC » chez Press-Start ; GameSpot fournit une partie des codes."),
    fact("CHT-09", "Combat : Max Ammo / Infinite Ammo / No Reload se débloquent avec 25 médailles bronze / argent / or au stand de tir ; All Explosive Weapons (100 grenades), Incendiary Ammo (100 ennemis brûlés), Exploding Bottles (100 Molotov), Explosive Shotgun (100 ennemis avec dégâts explosifs), Hauners H-AT (100 véhicules détruits).", "press_confirmed", "gamespot_cheats", "pressstart_cheats"),
    fact("CHT-10", "Filtres d'écran / environnement : Golden Hour (4 h à se tenir la main), Powdered Sugar (scanner tous les débris spatiaux avec WAiNK), Pinhole (25 opérations de gang en duo), Neon Jungle (16 véhicules Girlypop), Cataclysm, Videotape, Dark Mirror (500 000 $ de véhicules revendus), Migraine (survivre 6 min à 6 étoiles), Bubblegum (24 cartes Vice City Flamingos), Pixel Art, Hellscape (100 voitures de police volées).", "press_confirmed", "gamespot_cheats", "pressstart_cheats", note="Conditions relevées dans deux guides de presse ; GameSpot annonce explicitement une mise à jour progressive."),
    fact("CHT-11", "Divergence détectée : GameSpot donne « Finish the story » pour Cycle Weather et « TBC / Finish story » pour plusieurs déblocages, Press-Start donne « Reveal the entire map » ; les séquences Attack Force diffèrent aussi. Afficher un badge « divergence presse » plutôt que trancher.", "press_confirmed", "gamespot_cheats", "pressstart_cheats"),
    fact("CHT-12", "Aucun code de triche n'est publié par Rockstar Games lui-même au 18/11/2026 : les listes de GameSpot et Press-Start sont des relevés de presse sur copies de review, potentiellement incomplets et susceptibles d'évoluer après le 19/11.", "press_confirmed", "gamespot_cheats", "pressstart_cheats", "newswire"),
    fact("CHT-13", "Le guide GameSpot « All GTA 6 Cheats » est daté du 18/11/2026 12:13 UTC et modifié à 12:18 UTC ; Press-Start publie sa liste le même jour. Les deux pages conseillent de revenir pour les codes encore manquants.", "press_confirmed", "gamespot_cheats", "pressstart_cheats"),
]

FACTS["missions_endings_trophies"] += [
    fact("MIS-10", "Press-Start relève 93 missions d'histoire exactes dans l'onglet « story recap », réparties en 5 chapitres : 22 + 13 + 26 + 25 + 7. Le testeur a bouclé la campagne en un peu moins de 50 h, temps partagé équitablement entre Jason et Lucia.", "press_confirmed", "pressstart_missions", note="SPOILER : la liste complète des titres est dans `s2_press_mission_list`. « ~100 missions » de TrueAchievements est un arrondi ; retenir 93 chiffré par le recap."),
    fact("MIS-11", "Titres de chapitre / trophées : Paradise Lost (Chap. 1), Tits Ass Drug Money (Chap. 2), Vice City, Baby! (Chap. 3), Top of the World, Ma (Chap. 4), You Gotta Know When To Get Off (mission finale), Just Like Paradise (Gone Fishing).", "press_confirmed", "pressstart_trophies", "pressstart_missions", note="Noms de trophées de presse, SPOILER, à protéger par SpoilerToggle."),
    fact("MIS-12", "Missions notables nommées : Prologue, Gone Fishing, Buck Me, Breakfast Run, The Cartel Heist, Welcome To Vice City, Sinfrontera National Bank, Child's Play, Headliners, VCIA Takedown, Operation Savage Glory, The End Of The Road ; les missions peuvent se terminer hors ordre affiché.", "press_confirmed", "pressstart_missions", "pressstart_trophies"),
    fact("MIS-13", "Press-Start : 55 trophées / succès dont le Platine « Vice Got A Price! » (ou Mythic sur Xbox) et « A Long Road » pour le 100 %. Estimation >100 h pour le complet, ~50 h pour l'histoire seule.", "press_confirmed", "pressstart_trophies", "pressstart_100", note="Liste de presse post-embargo, PAS une liste PSN / Xbox officielle."),
    fact("MIS-14", "Exemples de succès de presse : Trust (Breakfast Run), Break the Bank (The Cartel Heist), Hi-Jacked (VCIA Takedown), Snow Storm (Operation Savage Glory), Cunning Stunts (250 stunts), You WAiNKer! (100 lieux WAiNK), Maximum Withdrawal (5 coffres de banque), Dime on the Dollar (250 000 $ de billets marqués blanchis).", "press_confirmed", "pressstart_trophies"),
    fact("MIS-15", "La checklist 100 % reste masquée jusqu'au générique de fin ; Press-Start prévient explicitement que sa publication contient des SPOILERS. Le site doit utiliser un SpoilerToggle fermé par défaut.", "press_confirmed", "pressstart_100", "pressstart_trophies"),
    fact("MIS-16", "TrueAchievements : ~100 missions, rythme « slow-burn », ~80 h pour l'histoire avec entretien de la condition physique, 20 succès débloqués sans connaître le total ; un éventuel trophée lié au tracker 100 % supposerait une completion très longue.", "press_confirmed", "trueachievements_review"),
]

FACTS["tips_strategies_techniques"] += [
    fact("TIP-24", "Routine de survie GameSpot : dormir la nuit, sport le matin, manger au frigo, se doucher ; ces buffs durent jusqu'à la mort ou la fin de session. Ne pas négliger Health / Stamina / Focus sous peine de désavantage.", "press_confirmed", "gamespot_tips"),
    fact("TIP-25", "Astuce gain de temps : aller à la salle avec le couple fait progresser les DEUX personnages en un seul entraînement ; refermer l'anneau fitness puis consommer une barre / shake protéiné pour verrouiller les gains.", "press_confirmed", "gamespot_tips", "gamespot_gym"),
    fact("TIP-26", "Toujours activer Focus hors combat : repérage des ennemis à travers les murs, des notes de codes de coffre, des objets jaunes, de l'argent vert et des valeurs cachées dans les coffres de voiture.", "press_confirmed", "gamespot_tips", "gamespot_robberies"),
    fact("TIP-27", "Voyager vite sans fast travel classique : RydeMe + 100 $ pour l'arrivée instantanée, bus / train gratuits mais à horaires, ou bascule de personnage pour revenir près de la planque du partenaire.", "press_confirmed", "gamespot_tips"),
    fact("TIP-28", "Avant de voler : ouvrir WAiNK pour lire alarme / traceur / prix de revente / coût d'immatriculation. Un traceur avancé exige de rouler vite pour cesser le ping ; une voiture sans clé demande un cloneur.", "press_confirmed", "gamespot_tips"),
    fact("TIP-29", "Braquage propre : repérer le niveau de sécurité sur la carte, gérer la foule (le partenaire aide), désactiver l'alarme au panneau blanc, détruire les preuves CCTV ou tirer les caméras au silencieux, puis vider caisse et arrière-salle.", "press_confirmed", "gamespot_robberies"),
    fact("TIP-30", "Ne jamais chercher une « liste de safe codes » : les codes sont aléatoires. Utiliser Focus pour trouver le code sur un garde, un post-it ou un écran ; à défaut crocheter le petit coffre ou forcer le lockbox.", "press_confirmed", "gamespot_robberies"),
    fact("TIP-31", "Banques : attendre le fourgon blindé pour l'ouverture temporaire du coffre-fort, suivre le fourgon ou utiliser l'info de Yasmani (Chap. 3) ; brouilleur de packs de teinture indispensable pour les billets marqués ; détruire les caméras cloud avant d'être vu.", "press_confirmed", "gamespot_robberies"),
    fact("TIP-32", "Économie : vendre des voitures volées et braquer des coffres de banque, déposer immédiatement le cash aux ATM, éviter de tout placer en épargne BuckMe longue durée au début (cash gates), rentabiliser Scooter Bros Premium 12 500 $.", "press_confirmed", "pressstart_economy", "gamespot_tips"),
    fact("TIP-33", "6 étoiles : tuer un policier pour démarrer à 3 étoiles, entrer en zone restreinte pour 5, continuer le combat pour 6 ; pour fuir, casser la ligne de vue, surveiller les étoiles rouges, changer tenue / véhicule / armes et éviter les Hot Areas.", "press_confirmed", "sportskeeda_wanted", "trueachievements_review", note="Technique de presse à recouper en jeu ; ne pas confondre avec une stratégie officielle."),
    fact("TIP-34", "Cheats : finir l'histoire d'abord, cocher les défis en cours de route, mais ne jamais activer un code sur une sauvegarde que l'on veut conserver (plus de sauvegarde possible après usage).", "press_confirmed", "gamespot_cheats", "pressstart_cheats"),
    fact("TIP-35", "PS5 : installer le firmware système obligatoire ET le patch de jeu 1.002.001 avant minuit ; les gâchettes adaptatives aident à rester sous la limite de vitesse pour éviter l'attention policière.", "press_confirmed", "independent", "rockstarintel_patch", "gamespot_dualsense"),
    fact("TIP-36", "YouTube / communauté S2 : tutoriels « NZ time » (EwBcYsbJu2I), « complete pre-play guide » (P1YTXjZRUpw) et « 106 Tips » (DeFeDYE5P6w). Recherche Reddit du 18/11 encore pauvre en retours de joueurs réels : privilégier les tests presse accrédités jusqu'au 19/11.", "community", "yt_nz_tutorial", "yt_preplay", "yt_106tips", "reddit_mysteries"),
]

FACTS["press_reviews"] += [
    fact("REV-08", "Direction artistique (PCMag, 18/11) : ombres « moody », éclairage spectaculaire, couchers de soleil orange « impossibly perfect », palette néon violette spirituellement '80s sans être anachronique — « réalisme et direction artistique ne s'excluent pas ». La conduite et le tir ne sont plus « maladroits / clunky » selon le testeur.", "press_confirmed", "pcmag_art", note="Fetch direct PCMag = HTTP 403 ; extrait de recherche + recoupement Gfinity / G2A / VGTimes / RockstarINTEL. Base des tokens --c-sunset, --c-violet, --c-pastel."),
    fact("REV-09", "Identité visuelle recoupée : jaquette 2026 rose / orange / violet, hôtels pastel Art déco d'Ocean Beach, néons magenta / cyan sur chaussée mouillée la nuit, soleil chaud le jour. Continuité assumée avec GTA: Vice City (2002) et le fantasy gangster / boating.", "press_confirmed", "gfinity_cover", "vgtimes_cover", "rockstarintel_cover", "g2a_art"),
    fact("REV-10", "Gadgets360 (18/11, 18:03 IST) : Metacritic 99 sur 146 critiques, à égalité avec Ocarina of Time ; OpenCritic 98 (54 critiques) et 100 % de critiques recommandent le jeu. IGN 10/10, GameSpot 10/10, VGC 5/5, Eurogamer 5/5, Washington Post 4/4, Bloomberg « masterpiece ». Instantané évolutif.", "press_confirmed", "gadgets360_reviews", "opencritic_news", "thegamer_reviews", note="OpenCritic DIRECT = 98 « Mighty ». Plusieurs roundups annoncent 99 : arbitrage en faveur du chiffre de la plateforme elle-même."),
    fact("REV-11", "OpenCritic publie le 18/11 un article Screen Rant annonçant « 99 Metascore based on 98 critic reviews » ; la fiche du jeu affiche 98. Le nombre de critiques (98 → 146) et l'agrégat doivent être horodatés, jamais figés.", "press_confirmed", "opencritic_news", "gadgets360_reviews"),
    fact("REV-12", "TrueAchievements attribue 10/10 après ~80 h sur Xbox Series X, 20 succès débloqués : éloge du rythme lent, des systèmes RPG (profils criminels, relation, condition physique) et du souci du détail (débris de collisions, PNJ, événements aléatoires).", "press_confirmed", "trueachievements_review"),
    fact("REV-13", "The Independent / Newswav (18/11) : pas d'accès anticipé payant, déblocage à minuit local, mise à jour PS5 obligatoire, budget estimé 1–1,5 Md$ par des analystes (NON confirmé par Rockstar), classification ESRB M 17+, 8 nominations aux Game Awards 2026.", "press_confirmed", "independent", "newswav_live", note="Le budget est une estimation d'analystes Business Insider, pas un chiffre officiel Take-Two."),
]

FACTS["community_tools_and_social"] += [
    fact("COM-11", "GitHub mendesjf86/gta6-leonida-atlas : fork de navanem (7 commits de retard), 19 commits, v0.8.1 « crawlable Atlas pages », 554 tests unitaires et 10 tests E2E Chromium annoncés dans l'historique ; données GTADB ~2 198 entrées (2 091 positionnées, 107 non positionnées, 6 régionales). Toujours NON officiel.", "community", "github_atlas_fork", "github_atlas"),
    fact("COM-12", "Recherche S2 YouTube / GitHub / Reddit / réseaux : deux nouvelles vidéos de pré-lancement référencées, un fork d'atlas vérifié, un live The Independent syndiqué par Newswav. Reddit r/GTA6 reste peu exploitable avant le déblocage public ; réseaux sociaux = surtout relais d'annonces officielles.", "community", "yt_nz_tutorial", "yt_preplay", "github_atlas_fork", "reddit_mysteries", "newswav_live"),
    fact("COM-13", "Piège S2 : gta6nerd.com publie des conseils génériques calqués sur GTA V (revenu passif, mode manuel, Pay 'n' Spray) ; gtapulse.com publie une « analyse » de palette notée 4.9/5 datée de janvier 2026. Ces pages SEO sont écartées du corpus de faits.", "community", "gta6nerd_tips", "pcmag_art", note="Règle : privilégier presse accréditée post-embargo + sources primaires Rockstar."),
]

FACTS["visual_identity_and_art_direction"] = [
    fact("ART-01", "Palette de base du projet (MegaPrompt) : #FF2D78 rose, #00D4FF bleu, #FFD700 or, #0A0A0F noir, #12121C bleu nuit, #1A1A2E carte, #FFFFFF blanc, #B0B8D4 gris bleuté, #00FF9D vert, #FF4444 alerte.", "official", "rockstar_vi", "newswire"),
    fact("ART-02", "Tokens dérivés S2 vérifiés : --c-sunset #FF8A3D (couchers de soleil orange), --c-violet #8B5CF6 (néon violet), --c-pastel #FFB8D9 (Art déco pastel), --c-teal #2DE1C2 (lagon des Keys), --c-deep-purple #2A1B4D (crépuscule).", "press_confirmed", "pcmag_art", "gfinity_cover", "g2a_art"),
    fact("ART-03", "Jour = chaud / naturel (pêche, corail, ambre, ciel bleu lavande, eau bleue, palmiers) ; nuit = fantasy néon (magenta, cyan, bleu électrique, rose vif, reflets sur bitume mouillé, halos sodium-orange). Deux identités pour les mêmes lieux.", "press_confirmed", "g2a_art", "pcmag_art", "vgtimes_cover"),
    fact("ART-04", "Le front de mer Art déco est plus clair, plus pastel et moins contrasté ; Vice City assume une « réalité haute en couleur » (saturation ~15 % au-dessus du réel) plutôt que le naturalisme de Red Dead Redemption 2.", "press_confirmed", "g2a_art", "pcmag_art", note="Analyse visuelle de presse / comparatif de trailers, pas une déclaration technique Rockstar."),
    fact("ART-05", "Conséquence design : héros en dégradé sunset → rose → violet, lueurs néon sur bitume, scanlines CRT discrètes, cartes bleu nuit et pastilles dorées ; aucune illustration générée n'est présentée comme capture officielle.", "speculative", "pcmag_art", "gfinity_cover", note="Déduction éditoriale explicite appliquée dans design_system.css / animations.css."),
]

# Liste structurée des 93 missions relevées par Press-Start (SPOILERS).
S2_PRESS_MISSIONS = {
    "status": "press_confirmed",
    "not_official": True,
    "spoiler": True,
    "source_url": S["pressstart_missions"],
    "retrieved_at": RETRIEVED,
    "total": 93,
    "chapters": {
        "Chapitre 1": ["Prologue", "Gone Fishing", "Gear Up", "Just A Scratch", "Lab Fees", "Unwanted Attention", "Pipework", "Hey Arnold!", "Island Dreams", "Feng Shui", "Coming Home", "Buck Me", "Clean Up After Donnie", "Down To Earth", "Clear Skies", "Day Release", "Swamped", "Don Gone", "Recalibration", "Tourist Trap", "Home Sweet Home", "Discharge Time"],
        "Chapitre 2": ["What's In The Bag?", "Ambulance Chaser", "Just Moved In", "Girls' Trip", "Moses", "Daily Driver", "Slam Dunk", "Breakfast Run", "Coffee Break", "Afternoon Delight", "Thrillbillies", "Twist Wrist, Smash, Grab", "Checking Out"],
        "Chapitre 3": ["Welcome To Vice City", "Dealer's Choice", "Meet The Heders", "Dubious Provenance", "Mami Knows Best", "South Leonida Real Estate", "Tyrone", "Here, Kitty Kitty", "Kitter Litter Labs", "Car Service", "Top Billing", "Boobie Time", "First Impressions", "Crosstown Traffic", "Credit Check", "Steal The Zorrusso For Randy", "Sinfrontera National Bank", "Security Expert", "Ride Or Die", "Company Property", "The Missing Link", "Safe Word", "Cooties", "Bricked Up", "Hidden Charges", "The Cartel Heist"],
        "Chapitre 4": ["Ocean Beach", "Another Life", "Company Cars", "Lawyer Up", "Party Hard", "Heavy Lifting", "Photo/Shoot", "Making Gainz", "Watch It", "Cash Injections", "Amateur Hour", "Dirty Work", "Too Much Baggage", "Adventures In Babysitting", "Fresh Evidence", "Power Play", "Child's Play", "Headliners", "Close Surveillance", "Delivery Method", "Team Building", "Fully Catered", "VCIA Takedown", "Sunset", "Starting From Zero"],
        "Chapitre 5": ["Bird In The Hand", "Taking Liberties", "VC Baby", "Doggie Bag", "Operation Savage Glory", "Protective Custody", "The End Of The Road"],
    },
    "note": "Titres relevés dans l'onglet « story recap » d'une copie de review Press-Start. Ordre affiché ≠ ordre de complétion obligatoire. Aucune liste officielle Rockstar publiée.",
}
assert sum(len(v) for v in S2_PRESS_MISSIONS["chapters"].values()) == 93

# ─── 4. Métadonnées, arbitrages S2 et clé structurée dans build() ───────────

def build() -> dict:
    flat = [f for group in FACTS.values() for f in group]
    counts: dict[str, int] = {}
    for f in flat:
        counts[f["status"]] = counts.get(f["status"], 0) + 1
    return {
        "meta": {
            "project": "GTA VI — The Ultimate Guide",
            "phase": "S1 — RESEARCH + S2 — DESIGN_SYSTEM (amendement 18/11/2026)",
            "generated_at": RETRIEVED,
            "timezone": "Europe/Paris",
            "build_context": "J-1 avant la sortie officielle du 19/11/2026 ; embargo critiques levé le 18/11/2026 ; S2 = vérification directe des articles de presse post-embargo.",
            "status_vocabulary": {
                "official": "Source primaire Rockstar / Take-Two / PlayStation / Xbox.",
                "press_confirmed": "Média spécialisé crédible, souvent accrédité preview/review, source primaire citée.",
                "community": "Wiki, carte, dépôt GitHub, forum, vidéo : reconstruction ou analyse de fan.",
                "leak_unverified": "Fuite ou rumeur, build de développement ou liste anonyme.",
                "post_launch_pending": "N'existe pas encore légalement ; structure de page prête, contenu en attente.",
                "speculative": "Estimation / déduction éditoriale explicitement étiquetée.",
            },
            "integrity_rule": "Aucun fait post-launch n'est fabriqué. Chaque fait porte {value, status, sources[], source_url, retrieved_at}. Les relevés de copies de review restent press_confirmed, jamais official.",
            "s2_amendment": {
                "at": "2026-11-18",
                "direct_fetches": ["GameSpot cheats", "GameSpot 13 tips", "GameSpot robberies", "GameSpot DualSense", "GameSpot gym", "Press-Start cheats", "Press-Start economy", "Press-Start trophies", "Press-Start 93 missions", "Press-Start 100% checklist", "TrueAchievements review", "Sportskeeda 6-star", "Independent live", "Newswav live", "OpenCritic", "Gadgets360", "RockstarINTEL patch", "GitHub fork"],
                "policy": "Les listes post-embargo sont des relevés de presse accréditée, non des publications Rockstar ; badges + SpoilerToggle obligatoires.",
                "design_tokens_added": ["--c-sunset", "--c-violet", "--c-pastel", "--c-teal", "--c-deep-purple"],
            },
            "totals": {
                "facts": len(flat),
                "sections": len(FACTS),
                "sources_registered": len(S),
                "by_status": counts,
            },
            "sections": {k: len(v) for k, v in FACTS.items()},
        },
        "sources_registry": S,
        "facts": FACTS,
        "s2_press_mission_list": S2_PRESS_MISSIONS,
        "contradictions_and_arbitrations": [
            {
                "topic": "Cheats : conditions et séquences",
                "conflict": "GameSpot (18/11, 12:13 UTC) et Press-Start (18/11) divergent sur certains déblocages (Cycle Weather : finir l'histoire vs révéler toute la carte) et sur la saisie Attack Force ; plusieurs codes restent TBC.",
                "arbitration": "Afficher les deux versions avec badge « divergence presse », ne publier que les séquences concordantes ou explicitement testées par GameSpot, et attendre le recoupement en jeu du 19/11.",
            },
            {
                "topic": "Nombre de missions d'histoire",
                "conflict": "TrueAchievements parle de « presque 100 missions » ; l'onglet story recap relevé par Press-Start compte exactement 93 missions en 5 chapitres.",
                "arbitration": "Retenir 93 (décompte précis) avec source_url Press-Start, et signaler « ~100 » comme arrondi de review. Aucune liste officielle Rockstar.",
            },
            {
                "topic": "OpenCritic 98 vs 99",
                "conflict": "La fiche OpenCritic directe et Gadgets360 affichent 98 « Mighty » ; TheGamer / Tom's Guide annoncent 99 sur OpenCritic.",
                "arbitration": "Retenir 98 avec 100 % de recommandation, horodater le relevé (18/11/2026) et ne pas fusionner Metacritic 99 avec OpenCritic.",
            },
            {
                "topic": "Codes de triche « indisponibles à J-1 »",
                "conflict": "research_data.json S1 affirmait qu'aucun code ne pouvait avoir été testé avant la sortie ; GameSpot et Press-Start ont joué à des copies de review et publié des listes le 18/11.",
                "arbitration": "CHT-01/02/04 réécrits en press_confirmed ; N/A-03 conserve l'attente d'une publication OFFICIELLE Rockstar et d'une liste exhaustive. Ne jamais dire « officiels ».",
            },
            {
                "topic": "Liste des trophées",
                "conflict": "Liste générique de 55 noms (08/11, X anonyme) vs liste « Vice Got a Price! » (18/11, PC Gamer / Press-Start).",
                "arbitration": "La première est jugée fake par PSNProfiles (difficulté hard, co-op inexistants). La seconde est plus crédible (post-embargo) mais reste à recouper avec PSN/Xbox. Aucune liste officielle publiée.",
            },
            {
                "topic": "Nombre de véhicules",
                "conflict": "200+ / 185 / 172 / 110 / ~100 selon les bases communautaires.",
                "arbitration": "Rockstar n'a publié aucun chiffre. Afficher une fourchette avec badge « estimation communautaire », jamais un compteur prétendument officiel.",
            },
            {
                "topic": "Nombre d'armes",
                "conflict": "28 (gta6bible) vs 18 avec preuve first-party (GTA Intel).",
                "arbitration": "Dépend du critère d'inclusion (visuel trailer vs nom officiel). Présenter les deux avec leurs définitions.",
            },
            {
                "topic": "Régions de Leonida",
                "conflict": "6 régions officielles vs 7 avec « Waning Sands » (leonidaverse).",
                "arbitration": "Retenir 6 officielles ; « Waning Sands » = région imaginée par la communauté, à exclure de la carte officielle.",
            },
            {
                "topic": "Personnages secondaires",
                "conflict": "8 profils officiels vs ~22 noms du MegaPrompt.",
                "arbitration": "Les noms supplémentaires viennent de la carte « imagined » de leonidaverse. À placer dans une section « Communauté / non confirmé », jamais dans le cast officiel.",
            },
            {
                "topic": "Pistes du score Justice",
                "conflict": "30 pistes (annonce Rockstar via trackers) vs 50 pistes (listing Apple Music NZ).",
                "arbitration": "Conserver 30 avec note de divergence, re-vérifier le 11/12/2026.",
            },
            {
                "topic": "Date limite du bonus précommande",
                "conflict": "« avant le 20 novembre » (Rockstar Store FR) vs « avant le 19/11 » (presse EN).",
                "arbitration": "Citer la formulation du store FR et horodater ; ne pas trancher à la place de Rockstar.",
            },
            {
                "topic": "Contenu des éditions sur le Store",
                "conflict": "Le DOM de la page Store FR répète la liste Ultime sous l'édition Standard.",
                "arbitration": "Artefact de parsing d'un carrousel JS. Recouper avec GTABase / Dot Esports / GTA Boss : la Standard contient le jeu + bonus de précommande uniquement.",
            },
            {
                "topic": "Guides « post-launch » publiés avant la sortie",
                "conflict": "GrandTheft.gg (18/11) publie localisations d'armes/safehouses, une chaîne YouTube publie un « 100% Walkthrough » le 15/11.",
                "arbitration": "Contenu non vérifiable avant l'accès public. Étiqueter communautaire / non vérifié ; ne pas en dériver de données structurées.",
            },
            {
                "topic": "GTA VI Online",
                "conflict": "Page P14 du MegaPrompt demande modes/missions/économie vs Rockstar décrit un jeu solo sans online annoncé.",
                "arbitration": "Livrer un hub de statut officiel + rumeurs étiquetées ; aucune fiche de mode inventée.",
            },
        ],
        "mega_prompt_corrections": [
            "S2 (18/11) : les « codes officiels indisponibles » sont désormais une liste de PRESSE post-embargo, partielle et non officielle — corriger CHT-01/02/04 et N/A-03.",
            "S2 (18/11) : 93 missions d'histoire sont nommées par Press-Start (story recap) ; ~100 était un arrondi. Les fins détaillées et stratégies restent non publiées officiellement.",
            "S2 (18/11) : la checklist 100 % et les 55 trophées sont connus via copies de review, mais restent à recouper avec PSN / Xbox ; SpoilerToggle obligatoire.",
            "S2 (18/11) : safe codes ALÉATOIRES — interdire toute page « liste de codes de coffre » statique.",
            "« Pas de version Xbox One » : vrai en natif, faux via Xbox Cloud Gaming (annonce du 10/11/2026).",
            "« 2× GTA V / 3× RDR2 » : désormais confirmé par Rob Nelson (TGG, août 2026) et EDGE/NYT — passer de `community` à `press_confirmed`.",
            "« 62 espèces d'oiseaux », « 5 comtés » : aucune source primaire trouvée ; restent non vérifiés, à ne pas afficher.",
            "« Citation Rob Nelson juillet 2026 » : l'interview TGG date d'août 2026 (27–28/08).",
            "« 11 districts de Vice City » : non chiffré officiellement (20+ selon vice-city.app).",
            "« Justice a confirmé composer le score » : confirmé, annonce Newswire du 29/10/2026.",
            "« GTA VI Online » : non annoncé ; le jeu est solo au lancement.",
            "« Toutes les missions / cheats / trophées / collectibles / easter eggs » : indisponibles à J-1, voir unavailable_post_launch.",
        ],
        "next_research_pass": [
            "Dès le 19/11/2026 : recouper en jeu les 93 missions, les 55 trophées, la checklist 100 % et les codes de coffre aléatoires.",
            "Vérifier l'impact exact des cheats sur la sauvegarde et les trophées, et compléter les séquences TBC.",
            "Après le 19/11/2026 : récupérer les listes officielles PSN / Xbox de trophées.",
            "Recenser les codes de triche vérifiés en jeu (avec date de test) et leur impact trophées.",
            "Collecter les localisations de collectibles via cartes communautaires créditées CC BY 4.0.",
            "Suivre Reddit r/GTA6, YouTube et GitHub pour les découvertes post-launch réelles.",
            "Stabiliser le Metascore et la note utilisateurs, historiser les patches.",
            "Vérifier la playlist radio complète station par station et le nombre de pistes du score Justice.",
        ],
    }


if __name__ == "__main__":
    data = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"✓ {OUT}")
    print(f"  {data['meta']['totals']['facts']} faits · "
          f"{data['meta']['totals']['sections']} sections · "
          f"{data['meta']['totals']['sources_registered']} sources")
    print(f"  statuts : {data['meta']['totals']['by_status']}")
