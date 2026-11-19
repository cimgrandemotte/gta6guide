#!/usr/bin/env python3
"""
Patch S2 du générateur `tools/build_research_data.py`.

Objectifs (18/11/2026, après vérification directe des articles post-embargo) :
  1. Ajouter `source_url` à CHAQUE fait (`workflow_master.yaml → fact_policy.json_rule`).
  2. Corriger le cadrage S1 « aucun code de triche / post_launch_pending » :
     GameSpot, Press-Start et TrueAchievements ont joué à des copies de review.
  3. Ajouter les faits S2 vérifiés (jamais étiquetés `official` Rockstar) :
     cheats, 93 missions, 55 trophées, 100 % checklist, économie, 6 étoiles,
     astuces GameSpot, direction artistique, scores, patches, outils communautaires.
  4. Ajouter des arbitrages de contradictions et une liste structurée des 93 missions.

Le patch est idempotent : un marqueur `S2_VERIFIED_FACTS` évite tout double ajout.
Usage : python3 tools/patch_research_s2.py && python3 tools/build_research_data.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "tools" / "build_research_data.py"
text = GEN.read_text(encoding="utf-8")

if "S2_VERIFIED_FACTS" in text:
    print("✓ Générateur déjà patché en S2 (rien à refaire).")
    raise SystemExit(0)

# ─── 1. Docstring, registre de sources, helper `fact()` ──────────────────────
text = text.replace(
    "Chaque fait porte OBLIGATOIREMENT : id, value, status, sources[], retrieved_at.",
    "Chaque fait porte OBLIGATOIREMENT : id, value, status, sources[],\n"
    "source_url (1re URL), retrieved_at — voir fact_policy.json_rule.\n"
    "Amendement S2 du 18/11/2026 : intégration des articles post-embargo vérifiés\n"
    "par fetch direct ; les nouveaux faits restent `press_confirmed`, jamais `official`."
)

SOURCES_S2 = '''    # ─── Sources S2 vérifiées par recherche + fetch direct le 18/11/2026 ────
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
'''
needle = '    "gamesradar": "https://www.gamesradar.com/gta-6-guide/",\n}'
assert needle in text, "Fin du registre S introuvable"
text = text.replace(needle, '    "gamesradar": "https://www.gamesradar.com/gta-6-guide/",\n' + SOURCES_S2 + '}')

needle = '''    d = {
        "id": fid,
        "value": value,
        "status": status,
        "sources": urls,
        "retrieved_at": RETRIEVED,
    }'''
assert needle in text, "Helper fact() introuvable"
text = text.replace(needle, '''    d = {
        "id": fid,
        "value": value,
        "status": status,
        "sources": urls,
        "source_url": urls[0],  # fact_policy.json_rule : URL primaire de chaque fait
        "retrieved_at": RETRIEVED,
    }''')

# ─── 2. Correction des faits S1 devenus faux / incomplets après l'embargo ────
def set_fact(fid: str, replacement: str) -> None:
    global text
    pat = re.compile(r'^    fact\("' + re.escape(fid) + r'",.*\n', re.M)
    assert pat.search(text), f"Fait {fid} introuvable"
    # Une ligne de fait dans une liste Python DOIT se terminer par une virgule.
    line = replacement.rstrip()
    if not line.endswith(','):
        line += ','
    text = pat.sub(line + "\n", text, count=1)

set_fact("CHT-01", '''    fact("CHT-01", "Rockstar n'a PAS publié de liste officielle de codes de triche au 18/11/2026 ; en revanche GameSpot et Press-Start ont testé les cheats sur copies de review post-embargo.", "press_confirmed", "gamespot_cheats", "pressstart_cheats", note="Ne jamais présenter ces listes comme « officielles Rockstar » : ce sont des relevés de presse accréditée, encore partiels.")''')
set_fact("CHT-02", '''    fact("CHT-02", "Avant l'embargo du 18/11/2026, les « listes de cheats GTA 6 » en ligne recyclaient GTA V ou étaient inventées (UNCONFIRMED). Après l'embargo, GameSpot et Press-Start publient des listes issues de copies de review, encore évolutives.", "press_confirmed", "cheats_gtasix", "cheats_gta6cheatcodes", "gamespot_cheats", "pressstart_cheats")''')
set_fact("CHT-04", '''    fact("CHT-04", "Saisie vérifiée par la presse : ouvrir le téléphone iFruit, maintenir L1 + R1 puis composer la séquence à la croix directionnelle. Terminer l'histoire au moins une fois est un prérequis. L'impact sur les trophées reste à recouper.", "press_confirmed", "gamespot_cheats", "pressstart_cheats", "endgametools", note="GameSpot précise avoir chargé une sauvegarde vierge pour tester l'échec des codes avant la fin de l'histoire.")''')
set_fact("POL-10", '''    fact("POL-10", "Comportement par étoile désormais décrit par la presse accréditée : 3/4 étoiles = hélicoptères (qui finissent par manquer de carburant), 5 étoiles = unités NOOSE en Humvees et hélicoptères d'attaque, 6 étoiles = la police poursuit jusqu'à la mort du joueur. Aucun tableau officiel Rockstar publié.", "press_confirmed", "trueachievements_review", "sportskeeda_wanted", "wanted_gamesreviews", note="Détails de presse post-embargo, à recouper en jeu après le 19/11/2026.")''')
set_fact("ECO-08", '''    fact("ECO-08", "Hors montants explicitement testés par la presse (abonnement Scooter Bros Premium 12 500 $), les payouts, prix de propriétés et rendements circulant en ligne restent des estimations de fans, non vérifiées.", "speculative", "gta6nerd_tips", "pressstart_economy", note="gta6nerd.com recycle des conseils génériques de GTA V (revenu passif, Pay'n'Spray) : ne pas en dériver de mécaniques GTA VI.")''')
set_fact("MIS-08", '''    fact("MIS-08", "Deux listes de trophées incompatibles circulent ; arbitrage S2 après fetch direct : la liste Press-Start / PC Gamer du 18/11/2026 est cohérente avec une copie de review et bien plus crédible que la rumeur générique du 08/11, mais elle reste NON officielle et doit être recoupée avec PSN / Xbox.", "press_confirmed", "pcgamer_trophies", "pressstart_trophies", "psnprofiles")''')
set_fact("N/A-03", '''    fact("N/A-03", "Publication officielle Rockstar de la liste exhaustive des cheats, de l'impact trophées et des codes encore manquants : toujours en attente. Les listes GameSpot / Press-Start du 18/11/2026 sont partielles et évolutives.", "post_launch_pending", "cheats_gtasix", "gamespot_cheats", "pressstart_cheats")''')
set_fact("N/A-04", '''    fact("N/A-04", "Liste officielle PSN / Xbox des trophées et succès + stratégies associées : toujours en attente. La liste de presse du 18/11 (55 trophées, Platinum « Vice Got A Price! ») reste à recouper.", "post_launch_pending", "yaninagames", "endgametools", "pressstart_trophies")''')
set_fact("N/A-05", '''    fact("N/A-05", "Collectibles : noms, localisations exactes et récompenses OFFICIELS. Une checklist 100 % de presse a été publiée le 18/11/2026, mais les coordonnées in-game et le recoupement communautaire restent post-lancement.", "post_launch_pending", "endgametools", "pressstart_100")''')

# ─── 3. Bloc de faits S2 + liste structurée des 93 missions ─────────────────
S2_BLOCK = r'''
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
'''
text = text.replace("\ndef build() -> dict:\n", S2_BLOCK + "\ndef build() -> dict:\n")

text = text.replace('            "phase": "S1 — RESEARCH",', '            "phase": "S1 — RESEARCH + S2 — DESIGN_SYSTEM (amendement 18/11/2026)",')
text = text.replace(
    '            "build_context": "J-1 avant la sortie officielle du 19/11/2026 ; embargo critiques levé le 18/11/2026.",',
    '            "build_context": "J-1 avant la sortie officielle du 19/11/2026 ; embargo critiques levé le 18/11/2026 ; S2 = vérification directe des articles de presse post-embargo.",'
)
text = text.replace(
    '            "integrity_rule": "Aucun fait post-launch n\'est fabriqué. Chaque fait porte statut + sources + date de collecte.",',
    '            "integrity_rule": "Aucun fait post-launch n\'est fabriqué. Chaque fait porte {value, status, sources[], source_url, retrieved_at}. Les relevés de copies de review restent press_confirmed, jamais official.",\n'
    '            "s2_amendment": {\n'
    '                "at": "2026-11-18",\n'
    '                "direct_fetches": ["GameSpot cheats", "GameSpot 13 tips", "GameSpot robberies", "GameSpot DualSense", "GameSpot gym", "Press-Start cheats", "Press-Start economy", "Press-Start trophies", "Press-Start 93 missions", "Press-Start 100% checklist", "TrueAchievements review", "Sportskeeda 6-star", "Independent live", "Newswav live", "OpenCritic", "Gadgets360", "RockstarINTEL patch", "GitHub fork"],\n'
    '                "policy": "Les listes post-embargo sont des relevés de presse accréditée, non des publications Rockstar ; badges + SpoilerToggle obligatoires.",\n'
    '                "design_tokens_added": ["--c-sunset", "--c-violet", "--c-pastel", "--c-teal", "--c-deep-purple"],\n'
    '            },'
)

CONTRADICTIONS_S2 = '''        "contradictions_and_arbitrations": [
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
'''
assert '        "contradictions_and_arbitrations": [\n' in text
text = text.replace('        "contradictions_and_arbitrations": [\n', CONTRADICTIONS_S2, 1)

MEGA_CORRECTIONS_S2 = '''        "mega_prompt_corrections": [
            "S2 (18/11) : les « codes officiels indisponibles » sont désormais une liste de PRESSE post-embargo, partielle et non officielle — corriger CHT-01/02/04 et N/A-03.",
            "S2 (18/11) : 93 missions d'histoire sont nommées par Press-Start (story recap) ; ~100 était un arrondi. Les fins détaillées et stratégies restent non publiées officiellement.",
            "S2 (18/11) : la checklist 100 % et les 55 trophées sont connus via copies de review, mais restent à recouper avec PSN / Xbox ; SpoilerToggle obligatoire.",
            "S2 (18/11) : safe codes ALÉATOIRES — interdire toute page « liste de codes de coffre » statique.",
'''
assert '        "mega_prompt_corrections": [\n' in text
text = text.replace('        "mega_prompt_corrections": [\n', MEGA_CORRECTIONS_S2, 1)

NEXT_RESEARCH_S2 = '''        "next_research_pass": [
            "Dès le 19/11/2026 : recouper en jeu les 93 missions, les 55 trophées, la checklist 100 % et les codes de coffre aléatoires.",
            "Vérifier l'impact exact des cheats sur la sauvegarde et les trophées, et compléter les séquences TBC.",
'''
assert '        "next_research_pass": [\n' in text
text = text.replace('        "next_research_pass": [\n', NEXT_RESEARCH_S2, 1)

needle = '        "facts": FACTS,\n'
assert needle in text
text = text.replace(needle, '        "facts": FACTS,\n        "s2_press_mission_list": S2_PRESS_MISSIONS,\n', 1)

GEN.write_text(text, encoding="utf-8")
print(f"✓ {GEN} patché : sources S2, source_url universel, faits post-embargo, 93 missions, arbitrages.")
