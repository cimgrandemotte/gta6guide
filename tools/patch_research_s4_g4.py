#!/usr/bin/env python3
"""Amendement recherche S4 / groupe G4 — Police, Économie, Activités.

Idempotent : le marqueur `s4_amendments.g4.marker == "S4_G4_VERIFIED_FACTS"`
empêche toute duplication si le script est relancé.

Faits ajoutés :
    POL-01 … POL-09   (section police_and_wanted)
    ECO-01 … ECO-09   (section economy)
    ACT-01 … ACT-10   (section activities)

Les sources sont enregistrées dans `sources_registry` et chaque fait porte un
`source_url` (règle projet : 100 % de couverture).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S4_G4_VERIFIED_FACTS_V2"

SOURCES = {
    "leonidahub_wanted": {
        "title": "GTA 6 wanted system guide: how the new police AI works and how to evade it",
        "publisher": "LEONIDA.HUB",
        "url": "https://www.leonidahub.co.uk/guides/gta-6-wanted-system-guide",
        "date": "2026-11",
        "kind": "guide spécialisé",
        "status": "press_confirmed",
    },
    "technerdiness_police": {
        "title": "GTA 6: How to Avoid the Police Before a Chase Starts",
        "publisher": "Tech Nerdiness",
        "url": "https://www.technerdiness.com/gta/gta-6-how-to-avoid-police-before-chase/",
        "date": "2026-08-28",
        "kind": "retranscription de l'Extended Look (Rob Nelson)",
        "status": "press_confirmed",
    },
    "xboxplay_wanted": {
        "title": "GTA 6 Wanted Levels Explained: How to Lose the Police Fast",
        "publisher": "XboxPlay",
        "url": "https://xboxplay.games/grand-theft-auto-6/how-to-lose-the-cops-in-gta-6-all-wanted-levels-explained-77302",
        "date": "2026-11-13",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "questduo_wanted": {
        "title": "How to Escape Wanted Level in GTA 6?",
        "publisher": "QuestDuo",
        "url": "https://questduo.com/grand-theft-auto-6/how-to-escape-wanted-level-in-gta-6/",
        "date": "2026-11-10",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "stealthygaming_wanted": {
        "title": "GTA 6 Wanted Level Explained: 6 Stars & Criminal Profile",
        "publisher": "Stealthy Gaming",
        "url": "https://stealthygaming.com/gta-6-wanted-level/",
        "date": "2026-11-17",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "reddit_preview_summary": {
        "title": "My entire GTA 6 preview, summarized (r/GTA6)",
        "publisher": "Reddit · r/GTA6",
        "url": "https://www.reddit.com/r/GTA6/comments/1w7ow99/my_entire_gta_6_preview_summarized/",
        "date": "2026-09-05",
        "kind": "forum (compte rendu de preview)",
        "status": "community",
    },
    "thegameswiki_law": {
        "title": "Law Enforcement — Grand Theft Auto VI Wiki",
        "publisher": "The Games Wiki",
        "url": "https://thegameswiki.com/gta6/wiki/law-enforcement",
        "date": "2026-11-07",
        "kind": "wiki communautaire",
        "status": "community",
    },
    "gtabase_previews": {
        "title": "GTA 6 Previews Roundup: All New Gameplay Features Revealed",
        "publisher": "GTABase",
        "url": "https://www.gtabase.com/articles/gta-6/gta-6-previews-recap-all-new-gameplay-features-revealed",
        "date": "2026-09-21",
        "kind": "récapitulatif de previews",
        "status": "press_confirmed",
    },
    "talkesport_robberies": {
        "title": "GTA 6 Robberies: Rockstar Confirms You Can Rob Almost Any Store in Leonida",
        "publisher": "TalkEsport",
        "url": "https://www.talkesport.com/gta-6/gta-6-robberies-rob-any-store/",
        "date": "2026-10-07",
        "kind": "retranscription IGN / Rob Nelson",
        "status": "press_confirmed",
    },
    "timesaver_robberies": {
        "title": "GTA 6 Robberies: Can You Rob Stores & Banks in Free Roam? Everything Confirmed",
        "publisher": "TimeSaver",
        "url": "https://timesaver.gg/blog/gta-6-robberies-confirmed-2026",
        "date": "2026-08-31",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "howtoplayhub_money": {
        "title": "GTA 6 Money: How to Make Money — Everything Confirmed",
        "publisher": "HowToPlayHub",
        "url": "https://howtoplayhub.com/gta-6/how-to-make-money",
        "date": "2026-09-05",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "viceatlas_economy": {
        "title": "GTA 6 economy: how money, loot and fences work",
        "publisher": "Vice Atlas",
        "url": "https://www.vice-atlas.com/briefings/gta6-economy-and-businesses/",
        "date": "2026-10-02",
        "kind": "briefing (dossier de vérification)",
        "status": "press_confirmed",
    },
    "thegameswiki_activities": {
        "title": "Side Activities — Grand Theft Auto VI Wiki",
        "publisher": "The Games Wiki",
        "url": "https://thegameswiki.com/gta6/wiki/side-activities",
        "date": "2026-09-23",
        "kind": "wiki communautaire",
        "status": "community",
    },
    "altchar_activities": {
        "title": "GTA 6 side activities and mini-games: Everything confirmed so far",
        "publisher": "AltChar",
        "url": "https://www.altchar.com/game-news/gta-6-side-activities-and-mini-games-everything-confirmed-so-far-a7Bxd8l86IF8",
        "date": "2026-09-04",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "grandtheft_activities": {
        "title": "Best Things to Do in GTA 6 Outside the Main Storyline",
        "publisher": "Grand Theft",
        "url": "https://grandtheft.gg/gta-6-best-activities-outside-main-storyline",
        "date": "2026-11-16",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "driffle_activities": {
        "title": "GTA 6 Activities & Side Missions: Everything Confirmed So Far",
        "publisher": "Driffle",
        "url": "https://driffle.com/blog/gta-6-activities-side-missions-everything-confirmed-so-far/",
        "date": "2026-08-15",
        "kind": "guide",
        "status": "press_confirmed",
    },
    "sportskeeda_activities": {
        "title": "All side activities in GTA 6: Basketball, kayaking, gym, and more",
        "publisher": "Sportskeeda",
        "url": "https://www.sportskeeda.com/gta/all-side-activities-gta-6-basketball-kayaking-gym",
        "date": "2026-09-03",
        "kind": "guide",
        "status": "press_confirmed",
    },
}

FACTS = {
    "police_and_wanted": [
        {
            "id": "POL-02",
            "status": "official",
            "text": "Aucune intervention sans témoin ni alarme : Rob Nelson a confirmé que la police ne réagit que si un PNJ assiste au crime ou si une alarme se déclenche.",
            "source_url": "https://www.technerdiness.com/gta/gta-6-how-to-avoid-police-before-chase/",
            "source_label": "Rob Nelson, Extended Look (28/08/2026)",
        },
        {
            "id": "POL-03",
            "status": "official",
            "text": "Quatre identifiants sont diffusés par radio quand un crime est signalé : le visage, la tenue, le véhicule et le fait que Jason et Lucia sont ensemble.",
            "source_url": "https://questduo.com/grand-theft-auto-6/how-to-escape-wanted-level-in-gta-6/",
            "source_label": "Extended Look, relevé des icônes de chaleur",
        },
        {
            "id": "POL-04",
            "status": "press_confirmed",
            "text": "Quatre états d'étoiles se lisent sur la jauge : creuses (crime signalé, aucun signalement de votre apparence), blanches pleines (identification + ligne de vue), blanches clignotantes (ligne de vue perdue, recherche en cours), rouges (poursuite terminée, zone chaude encore active).",
            "source_url": "https://xboxplay.games/grand-theft-auto-6/how-to-lose-the-cops-in-gta-6-all-wanted-levels-explained-77302",
            "source_label": "XboxPlay, 13/11/2026",
        },
        {
            "id": "POL-05",
            "status": "press_confirmed",
            "text": "La zone de recherche s'affiche comme une zone rouge sur la minimap, entourée d'un anneau plus clair : sortir des deux efface la recherche plus sûrement que la seule course.",
            "source_url": "https://www.reddit.com/r/GTA6/comments/1w7ow99/my_entire_gta_6_preview_summarized/",
            "source_label": "Compte rendu de preview r/GTA6 (zone rouge + anneau clair)",
        },
        {
            "id": "POL-07",
            "status": "press_confirmed",
            "text": "Les caméras-piétons des policiers alimentent le profil : si un agent filme votre visage, le port du masque ne suffit plus à effacer l'identifiant.",
            "source_url": "https://www.leonidahub.co.uk/guides/gta-6-wanted-system-guide",
            "source_label": "LEONIDA.HUB",
        },
        {
            "id": "POL-08",
            "status": "press_confirmed",
            "text": "La police n'apparaît plus comme une icône par voiture sur la minimap : la capacité Focus sert de substitut pour repérer les agents à travers les murs.",
            "source_url": "https://www.reddit.com/r/GTA6/comments/1w7ow99/my_entire_gta_6_preview_summarized/",
            "source_label": "Compte rendu de preview r/GTA6",
        },
        {
            "id": "POL-09",
            "status": "press_confirmed",
            "text": "Rater un braquage de magasin fait établir un périmètre autour de la boutique, au cas où le joueur reviendrait ; chaque véhicule de police transporte un fusil à pompe ou d'assaut dans le coffre.",
            "source_url": "https://www.reddit.com/r/GTA6/comments/1w7ow99/my_entire_gta_6_preview_summarized/",
            "source_label": "Compte rendu de preview r/GTA6",
        },
        {
            "id": "POL-10",
            "status": "community",
            "text": "Une dizaine d'agences distinctes (VCPD, Vice Beach Police, Vice-Dale Police, shérif de Leonard County, patrouille autoroutière de Leonida, POACH, garde-côtes, FIB) sont identifiées à partir des livrées et des panneaux, sans guide officiel de Rockstar.",
            "source_url": "https://thegameswiki.com/gta6/wiki/law-enforcement",
            "source_label": "The Games Wiki, compilation communautaire",
        },
        {
            "id": "POL-11",
            "status": "community",
            "text": "Véhicules de police repérés dans les médias officiels : interceptor moderne, ancienne berline Stanier, Buffalo STX de poursuite, SUV Police Interceptor Utility, Gauntlet Interceptor noir et beige de la patrouille autoroutière, Ghost à décals rétro-réfléchissants, Brute Riot blindé et hélicoptère de type Maverick.",
            "source_url": "https://thegameswiki.com/gta6/wiki/law-enforcement",
            "source_label": "The Games Wiki / relevés de trailers",
        },
    ],
    "economy": [
        {
            "id": "ECO-01",
            "status": "official",
            "text": "Trois formes d'argent coexistent : l'argent en banque (conservé), le liquide sur soi (perdu en cas de mort ou d'arrestation avant dépôt) et le butin en sac (sans valeur tant qu'un receleur ne l'a pas racheté).",
            "source_url": "https://www.vice-atlas.com/briefings/gta6-economy-and-businesses/",
            "source_label": "Vice Atlas, briefing économie (Extended Look + previews)",
        },
        {
            "id": "ECO-02",
            "status": "official",
            "text": "Le liquide ne se dépose qu'aux distributeurs automatiques, jamais depuis le téléphone : le compte est joint entre Jason et Lucia.",
            "source_url": "https://www.gtabase.com/articles/gta-6/gta-6-previews-recap-all-new-gameplay-features-revealed",
            "source_label": "GTABase, récapitulatif de previews",
        },
        {
            "id": "ECO-03",
            "status": "official",
            "text": "Rob Nelson : on peut dévaliser « à peu près n'importe quoi » — boutique d'écouteurs, banque, agence de prêt sur salaire, fourrière de police — seul ou à deux, sans mission scriptée.",
            "source_url": "https://www.talkesport.com/gta-6/gta-6-robberies-rob-any-store/",
            "source_label": "Rob Nelson à IGN, relayé par TalkEsport",
        },
        {
            "id": "ECO-04",
            "status": "press_confirmed",
            "text": "Le coffre impose un arbitrage vitesse/rendement : le faire sauter est rapide mais détruit une partie des valeurs ; chercher la combinaison conserve tout le butin mais laisse le temps à la police d'encercler le bâtiment.",
            "source_url": "https://timesaver.gg/blog/gta-6-robberies-confirmed-2026",
            "source_label": "TimeSaver, synthèse des previews",
        },
        {
            "id": "ECO-05",
            "status": "press_confirmed",
            "text": "Les receleurs sont spécialisés — voitures, drogues, bijoux — et se rencontrent via l'histoire ; les billets de banque marqués exigent un receleur particulier.",
            "source_url": "https://www.vice-atlas.com/briefings/gta6-economy-and-businesses/",
            "source_label": "Vice Atlas",
        },
        {
            "id": "ECO-06",
            "status": "press_confirmed",
            "text": "Certaines missions d'histoire exigent d'atteindre un montant en caisse avant de se débloquer : le braquage libre alimente donc directement la progression narrative.",
            "source_url": "https://howtoplayhub.com/gta-6/how-to-make-money",
            "source_label": "HowToPlayHub, Extended Look du 27/08/2026",
        },
        {
            "id": "ECO-07",
            "status": "press_confirmed",
            "text": "Un braquage de quartier rapporte au mieux quelques milliers de dollars et n'apparaît pas sur la carte ; les grosses cibles (boutiques de bijoux, petites banques, repaires de gangs, fourgons blindés) sont marquées et rapportent davantage.",
            "source_url": "https://www.talkesport.com/gta-6/gta-6-robberies-rob-any-store/",
            "source_label": "TalkEsport / GTABase",
        },
        {
            "id": "ECO-08",
            "status": "press_confirmed",
            "text": "Voler proprement vaut mieux que voler vite : un véhicule endommagé pendant le vol ou la livraison fait chuter fortement l'offre du receleur.",
            "source_url": "https://www.gtabase.com/articles/gta-6/gta-6-previews-recap-all-new-gameplay-features-revealed",
            "source_label": "GTABase",
        },
        {
            "id": "ECO-09",
            "status": "press_confirmed",
            "text": "Les sacs de butin ont un volume : un sac plus grand se choisit en préparation, mais la capacité du coffre du véhicule fixe la limite absolue.",
            "source_url": "https://www.gtabase.com/articles/gta-6/gta-6-previews-recap-all-new-gameplay-features-revealed",
            "source_label": "GTABase",
        },
        {
            "id": "ECO-10",
            "status": "post_launch_pending",
            "text": "L'achat et la gestion d'entreprises par le joueur ne sont pas confirmés par Rockstar ; aucune grille de revenus, de coût d'achat ou de rentabilité n'est publiée.",
            "source_url": "https://www.vice-atlas.com/briefings/gta6-economy-and-businesses/",
            "source_label": "Vice Atlas — « l'empire économique n'est pas documenté »",
        },
        {
            "id": "ECO-11",
            "status": "speculative",
            "text": "Les tableaux de revenus passifs circulant (montants par entreprise, gains horaires, listes de braquages à plusieurs millions) reposent sur des schémas de GTA Online et sont explicitement des estimations pré-lancement.",
            "source_url": "https://vicecitymethods.com/money-methods",
            "source_label": "vicecitymethods.com — mention « pre-launch estimate »",
        },
    ],
    "activities": [
        {
            "id": "ACT-01",
            "status": "official",
            "text": "Pêche confirmée par Rockstar au parc national du Mont Kalaga : Jason pêche depuis un bateau ou une berge, y compris avec Cal Hampton dans le trailer 2.",
            "source_url": "https://thegameswiki.com/gta6/wiki/side-activities",
            "source_label": "Site officiel Rockstar + trailer 2",
        },
        {
            "id": "ACT-02",
            "status": "official",
            "text": "La chasse est confirmée au Mont Kalaga et dans les Grassrivers ; Rob Nelson précise que la pêche reste un loisir, sans cuisson ni vente obligatoire comme dans Red Dead Redemption 2.",
            "source_url": "https://www.altchar.com/game-news/gta-6-side-activities-and-mini-games-everything-confirmed-so-far-a7Bxd8l86IF8",
            "source_label": "AltChar, propos de Rob Nelson",
        },
        {
            "id": "ACT-03",
            "status": "press_confirmed",
            "text": "Le mini-golf apparaît pour la première fois dans la série, sur une capture officielle où Cal Hampton pose sur un parcours décoré d'alligators et de cascades artificielles.",
            "source_url": "https://thegameswiki.com/gta6/wiki/side-activities",
            "source_label": "Capture officielle Rockstar",
        },
        {
            "id": "ACT-04",
            "status": "press_confirmed",
            "text": "La salle de sport revient avec un effet sur les statistiques : soulever des poids à la plage en Jason ou frapper le sac en Lucia améliore santé et endurance.",
            "source_url": "https://grandtheft.gg/gta-6-best-activities-outside-main-storyline",
            "source_label": "Grand Theft, 16/11/2026",
        },
        {
            "id": "ACT-05",
            "status": "press_confirmed",
            "text": "Lucia peut combattre en cage (MMA) et parier sur des combats ; c'est une activité de rue à part entière, rémunératrice.",
            "source_url": "https://grandtheft.gg/gta-6-best-activities-outside-main-storyline",
            "source_label": "Grand Theft",
        },
        {
            "id": "ACT-06",
            "status": "press_confirmed",
            "text": "La chasse au trésor animalier s'appuie sur un bestiaire de plus de 170 espèces à répertorier dans les zones sauvages de Leonida.",
            "source_url": "https://grandtheft.gg/gta-6-best-activities-outside-main-storyline",
            "source_label": "Grand Theft",
        },
        {
            "id": "ACT-07",
            "status": "press_confirmed",
            "text": "Le Thrillbilly Mud Club organise des courses de moto et de quad hors piste autour du Mont Kalaga ; un circuit existe à Port Gellhorn.",
            "source_url": "https://grandtheft.gg/gta-6-best-activities-outside-main-storyline",
            "source_label": "Grand Theft",
        },
        {
            "id": "ACT-08",
            "status": "press_confirmed",
            "text": "Activités nautiques et subaquatiques confirmées : kayak dans les rivières du parc, jet-ski sur la côte et aux Keys, plongée autonome pour l'exploration sous-marine.",
            "source_url": "https://www.altchar.com/game-news/gta-6-side-activities-and-mini-games-everything-confirmed-so-far-a7Bxd8l86IF8",
            "source_label": "AltChar",
        },
        {
            "id": "ACT-09",
            "status": "press_confirmed",
            "text": "Activités sociales et de loisir : billard et fléchettes dans les bars, basket sur les toits et chez Jason, football de plage, boîtes de nuit et clubs, télévision et jeux vidéo in-game.",
            "source_url": "https://driffle.com/blog/gta-6-activities-side-missions-everything-confirmed-so-far/",
            "source_label": "Driffle",
        },
        {
            "id": "ACT-10",
            "status": "press_confirmed",
            "text": "Les activités de couple (pêche, courses, kayak) entretiennent la relation entre Jason et Lucia, qui influence ensuite les missions.",
            "source_url": "https://www.sportskeeda.com/gta/all-side-activities-gta-6-basketball-kayaking-gym",
            "source_label": "Sportskeeda",
        },
        {
            "id": "ACT-11",
            "status": "community",
            "text": "Sports et loisirs repérés dans les images mais non confirmés comme jouables : tennis sur les courts, catch de jardin, stand de tir, zoo, base-jump et parachute.",
            "source_url": "https://thegameswiki.com/gta6/wiki/side-activities",
            "source_label": "The Games Wiki (mention « playability unconfirmed »)",
        },
    ],
}


def _renumber(data: dict) -> None:
    """Réattribue des identifiants libres par section (POL / ECO / ACT)."""
    facts = data.get("facts", {})
    prefix = {"police_and_wanted": "POL", "economy": "ECO", "activities": "ACT"}
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
    g4 = amend.setdefault("g4", {})

    if g4.get("marker") == MARKER:
        print("research_data.json : déjà patché en S4/G4 — aucune duplication.")
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
                "added_in": "S4_G4",
            })
            added_facts += 1

    g4.update({
        "marker": MARKER,
        "at": "2026-11-18",
        "pages": [
            "pages/police/index.html",
            "pages/economie/index.html",
            "pages/activites/index.html",
        ],
        "facts_added": added_facts,
        "sources_added": added_src,
        "ids": {
            "police_and_wanted": [f["id"] for f in FACTS["police_and_wanted"]],
            "economy": [f["id"] for f in FACTS["economy"]],
            "activities": [f["id"] for f in FACTS["activities"]],
        },
    })

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    total_facts = sum(len(v) for v in facts.values())
    print(
        f"Amendement S4/G4 appliqué : +{added_facts} faits, +{added_src} sources, "
        f"{total_facts} faits au total, {len(sources)} sources enregistrées."
    )


if __name__ == "__main__":
    main()
