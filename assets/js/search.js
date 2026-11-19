/* ═══════════════════════════════════════════════════════════════════════════
   search.js — S3 / BUILD_CORE_PAGES · finalisé S27
   Index local uniquement : aucune requête réseau, aucun fichier de travail
   embarqué. Le corpus de recherche reste hors du site publié.

   Le moteur reste 100 % local : aucune API, aucun CDN, aucun localhost.
   Si le fetch relatif échoue dans l'aperçu sandbox, l'index de base suffit.
   ═══════════════════════════════════════════════════════════════════════════ */
import { asset, normalize, escapeHTML } from './utils.js';

const STATUS_LABEL = {
  official: 'OFFICIEL',
  press_confirmed: 'PRESSE · 18/11',
  community: 'COMMUNAUTÉ',
  speculative: 'ESTIMATION',
  leak_unverified: 'FUITE NON VÉRIFIÉE',
  post_launch_pending: 'EN ATTENTE · 19/11'
};

/** Index synchronously available before components.js initializes SearchEngine. */
export const searchIndex = [
  { title: "Fil du lancement — 18 novembre", path: "pages/news/index.html", section: "News",
    status: "press_confirmed", thumb: "assets/images/news/news_desk_dawn_phones_01.jpg",
    text: "correctifs 1.002 01.002.001 firmware PS5 horaires fuseaux performance 30 fps argent liquide fausses informations codes" },
  { title: 'Accueil définitif', section: 'Hub', url: asset('index.html'), thumb: asset('assets/images/heroes/homepage_hero_sunset_ocean_drive_01.jpg') },
  { title: 'Sortie, plateformes et patches', section: 'Officiel', url: asset('index.html#officiel'), thumb: asset('assets/images/heroes/homepage_vice_city_art_deco_01.jpg') },
  { title: 'Guide de démarrage J-1', section: 'Guide', url: asset('index.html#guide-demarrage'), thumb: asset('assets/images/missions/homepage_heist_getaway_01.jpg') },
  { title: 'Stratégies 6 étoiles et économie', section: 'PRESSE · 18/11', url: asset('index.html#strategies'), thumb: asset('assets/images/vehicles/homepage_supercar_night_01.jpg') },
  { title: 'Codes de coffre : divergence arbitrée', section: 'SPOILER', url: asset('index.html#arbitrages'), thumb: asset('assets/images/weapons/homepage_arsenal_neon_01.jpg') },
  { title: 'Reviews : OpenCritic et Metacritic', section: 'PRESSE · 18/11', url: asset('index.html#reviews'), thumb: asset('assets/images/heroes/homepage_neon_street_rain_01.jpg') },
  { title: 'Galerie cinématographique S2', section: 'Visuels', url: asset('index.html#galerie-s2'), thumb: asset('assets/images/heroes/homepage_hero_vicecity_night_01.jpg') },
  { title: 'Galerie cinématographique S3', section: 'Visuels', url: asset('index.html#galerie-s3'), thumb: asset('assets/images/map/homepage_leonida_aerial_teaser_01.jpg') },
                { title: 'Histoire & chapitres', section: 'Histoire · S4', url: asset('pages/histoire/index.html'), thumb: asset('assets/images/story/story_finale_highway_sunrise_01.jpg') },
  { title: 'Synopsis officiel et bios', section: 'Histoire · S4', url: asset('pages/histoire/synopsis.html'), thumb: asset('assets/images/story/story_duo_motel_doorway_01.jpg') },
  { title: 'Missions : 93 en 5 chapitres', section: 'Histoire · SPOILER', url: asset('pages/histoire/missions.html'), thumb: asset('assets/images/story/story_heist_planning_table_01.jpg') },
  { title: 'Chapitre 1 : le pénitencier de Leonida', section: 'Histoire · PRESSE · 18/11', url: asset('pages/histoire/missions.html#chapitre-1'), thumb: asset('assets/images/story/story_prologue_prison_corridor_01.jpg') },
  { title: 'Jason Duval : bio officielle', section: 'Personnage', url: asset('pages/histoire/synopsis.html#jason'), thumb: asset('assets/images/story/story_jason_portrait_neon_01.jpg') },
  { title: 'Lucia Caminos : bio officielle', section: 'Personnage', url: asset('pages/histoire/synopsis.html#lucia'), thumb: asset('assets/images/story/story_lucia_release_gate_01.jpg') },
  { title: 'Hub personnages', section: 'Personnages · S4', url: asset('pages/personnages/index.html'), thumb: asset('assets/images/characters/lucia_boxing_gym_01.jpg') },
  { title: 'Lucia Caminos : portrait complet', section: 'Personnages · S4', url: asset('pages/personnages/lucia.html'), thumb: asset('assets/images/characters/lucia_neon_portrait_01.jpg') },
  { title: 'Personnages secondaires', section: 'Personnages · S4', url: asset('pages/personnages/secondaires.html'), thumb: asset('assets/images/characters/boobie_ike_club_01.jpg') },
  { title: 'Vice City : 6 quartiers officiels', section: 'Carte · S4', url: asset('pages/carte/vice-city.html'), thumb: asset('assets/images/vicecity/vicecity_ocean_drive_pastel_01.jpg') },
  { title: 'Waning Sands (hors Vice City)', section: 'Carte · OFFICIEL', url: asset('pages/carte/vice-city.html#hors'), thumb: asset('assets/images/vicecity/vicecity_downtown_neon_dusk_01.jpg') },
  { title: 'Quartiers non confirmés : ce qu’on écarte', section: 'Carte · VÉRIFICATION', url: asset('pages/carte/vice-city.html#hors'), thumb: asset('assets/images/vicecity/vicecity_little_havana_street_01.jpg') },
  { title: 'Armes : portage 2+2 et coffre', section: 'Armes · S4', url: asset('pages/armes/index.html'), thumb: asset('assets/images/weapons/weapons_armory_trunk_01.jpg') },
  { title: 'Familles d\'armes et chargements', section: 'Armes · S4', url: asset('pages/armes/index.html#chargements'), thumb: asset('assets/images/weapons/weapons_pistol_closeup_01.jpg') },
  { title: 'Véhicules : trois paliers de vol', section: 'Véhicules · S4', url: asset('pages/vehicules/index.html'), thumb: asset('assets/images/vehicles/vehicles_supercar_causeway_01.jpg') },
  { title: 'WAINK, traceurs et Pay \'n\' Spray', section: 'Véhicules · S4', url: asset('pages/vehicules/index.html#waink'), thumb: asset('assets/images/vehicles/vehicles_muscle_pay_n_spray_01.jpg') },
  { title: 'Police : six étoiles et témoins', section: 'Police · S4', url: asset('pages/police/index.html'), thumb: asset('assets/images/police/police_roadblock_night_01.jpg') },
  { title: 'Les quatre identifiants à effacer', section: 'Police · S4', url: asset('pages/police/index.html#identifiants'), thumb: asset('assets/images/police/police_k9_tracking_swamp_01.jpg') },
  { title: 'Protocole d\'évasion pas à pas', section: 'Police · S4', url: asset('pages/police/index.html#evasion'), thumb: asset('assets/images/police/police_helicopter_searchlight_01.jpg') },
  { title: 'Économie : trois formes d\'argent', section: 'Économie · S4', url: asset('pages/economie/index.html#argent'), thumb: asset('assets/images/economie/economie_atm_cash_night_01.jpg') },
  { title: 'Braquages et coffres', section: 'Économie · S4', url: asset('pages/economie/index.html#braquages'), thumb: asset('assets/images/economie/economie_bank_vault_duffel_01.jpg') },
  { title: 'Receleurs et butin', section: 'Économie · S4', url: asset('pages/economie/index.html#fences'), thumb: asset('assets/images/economie/economie_fence_pawnshop_01.jpg') },
  { title: 'Activités confirmées', section: 'Activités · S4', url: asset('pages/activites/index.html'), thumb: asset('assets/images/activites/activites_airboat_everglades_01.jpg') },
  { title: 'Combat en cage (MMA)', section: 'Activités · S4', url: asset('pages/activites/index.html#sport'), thumb: asset('assets/images/activites/activites_cage_fight_01.jpg') },
  { title: 'Mini-golf et sorties', section: 'Activités · S4', url: asset('pages/activites/index.html#social'), thumb: asset('assets/images/activites/activites_minigolf_neon_01.jpg') },
  { title: 'Musique : 6 stations confirmées', section: 'Musique · S4', url: asset('pages/musique/index.html'), thumb: asset('assets/images/musique/musique_radio_studio_neon_01.jpg') },
  { title: 'Album 34 titres et score de Justice', section: 'Musique · OFFICIEL', url: asset('pages/musique/index.html#album'), thumb: asset('assets/images/musique/musique_vinyl_wall_shop_01.jpg') },
  { title: 'Titres confirmés par station', section: 'Musique · S4', url: asset('pages/musique/index.html#titres'), thumb: asset('assets/images/musique/musique_dj_booth_crowd_01.jpg') },
  { title: 'Online : solo au lancement', section: 'Online · OFFICIEL', url: asset('pages/online/index.html'), thumb: asset('assets/images/online/online_crew_garage_meet_01.jpg') },
  { title: 'GTA Online actuel maintenu', section: 'Online · OFFICIEL', url: asset('pages/online/index.html#gtaonline'), thumb: asset('assets/images/online/online_server_room_01.jpg') },
  { title: 'Codes : aucun code officiel', section: 'Codes · S4', url: asset('pages/codes/index.html'), thumb: asset('assets/images/codes/codes_phone_dialpad_night_01.jpg') },
  { title: 'Pourquoi les listes recyclent GTA V', section: 'Codes · ESTIMATION', url: asset('pages/codes/index.html#pourquoi'), thumb: asset('assets/images/codes/codes_notebook_handwritten_01.jpg') },
  { title: 'Trophées : 55 succès et le platine', section: 'Trophées · S4', url: asset('pages/trophees/index.html'), thumb: asset('assets/images/trophees/trophees_trophy_shelf_neon_01.jpg') },
  { title: 'Checklist 100 % et point manquable', section: 'Trophées · S4', url: asset('pages/trophees/index.html#cent'), thumb: asset('assets/images/trophees/trophees_checklist_notebook_01.jpg') },
  { title: 'Secrets : clins d\'œil vérifiés', section: 'Secrets · S4', url: asset('pages/secrets/index.html'), thumb: asset('assets/images/secrets/secrets_ufo_swamp_night_01.jpg') },
  { title: 'Clins d\'œil Vice City datés', section: 'Secrets · S4', url: asset('pages/secrets/index.html#vice'), thumb: asset('assets/images/secrets/secrets_wall_mural_street_01.jpg') },
  { title: 'Tips : le Focus détecteur', section: 'Tips · S4', url: asset('pages/tips/index.html#focus'), thumb: asset('assets/images/tips/tips_focus_mode_alley_01.jpg') },
  { title: 'Lunette, silencieux, coffres', section: 'Tips · S4', url: asset('pages/tips/index.html#armes'), thumb: asset('assets/images/tips/tips_safe_cracking_01.jpg') },
  { title: 'Menu véhicule et coups de portière', section: 'Tips · S4', url: asset('pages/tips/index.html#vehicules'), thumb: asset('assets/images/tips/tips_map_glovebox_01.jpg') },
  { title: 'Lumière, ray tracing et 1440p', section: 'Divers · S4', url: asset('pages/divers/index.html#lumiere'), thumb: asset('assets/images/divers/divers_marina_boats_golden_01.jpg') },
  { title: 'Cheveux simulés : pourquoi pas de 60 fps', section: 'Divers · S4', url: asset('pages/divers/index.html#cheveux'), thumb: asset('assets/images/divers/divers_leonida_road_trip_dawn_01.jpg') },
  { title: 'Orage tropical et rendu des sols mouillés', section: 'Divers · S4', url: asset('pages/divers/index.html#ville'), thumb: asset('assets/images/divers/divers_storm_palms_skyline_01.jpg') },
  { title: 'Prix, éditions et coffret Goodtime State', section: 'FAQ · S4', url: asset('pages/faq/index.html#prix'), thumb: asset('assets/images/faq/faq_versions_stack_01.jpg') },
  { title: 'PC : aucune version annoncée', section: 'FAQ · S4', url: asset('pages/faq/index.html#plateformes'), thumb: asset('assets/images/faq/faq_versions_stack_01.jpg') },
  { title: '30 fps partout : mesures Digital Foundry', section: 'FAQ · S4', url: asset('pages/faq/index.html#fps'), thumb: asset('assets/images/faq/faq_question_notes_wall_01.jpg') },
  { title: 'Préchargement : jusqu\'à 212 Go', section: 'FAQ · S4', url: asset('pages/faq/index.html#prechargement'), thumb: asset('assets/images/faq/faq_install_progress_screen_01.jpg') },
  { title: 'Carte interactive de Leonida — 28 lieux', section: 'Carte · S5', url: asset('pages/carte/index.html#carte-outil'), thumb: asset('assets/images/map/map_leonida_atlas_desk_01.jpg') },
  { title: "La carte officielle n'est pas interactive", section: 'Carte · S5', url: asset('pages/carte/index.html#officielle'), thumb: asset('assets/images/map/map_vicecity_neon_grid_01.jpg') },
  { title: 'Trois itinéraires de découverte', section: 'Carte · S5', url: asset('pages/carte/index.html#itineraires'), thumb: asset('assets/images/map/map_highway_causeway_air_01.jpg') },
  { title: 'Checklist 100 % sauvegardée localement', section: 'Collectibles · S5', url: asset('pages/collectibles/index.html#tracker'), thumb: asset('assets/images/collectibles/collec_checklist_clipboard_01.jpg') },
  { title: '80 challenges, seuils 50 et 70', section: 'Collectibles · S5', url: asset('pages/collectibles/index.html#regles'), thumb: asset('assets/images/collectibles/collec_shells_jar_01.jpg') },
  { title: '18 séries de 480 cartes à collectionner', section: 'Collectibles · S5', url: asset('pages/collectibles/index.html#cartes'), thumb: asset('assets/images/collectibles/collec_cards_flamingo_flatlay_01.jpg') },
  { title: 'Quiz GTA VI — 30 questions vérifiées', section: 'Quiz · S5', url: asset('pages/quiz/index.html#quiz'), thumb: asset('assets/images/quiz/quiz_neon_trivia_board_01.jpg') },
  { title: 'Rapport QA : accessibilité et performance', section: 'QA · S6', url: asset('pages/qa/index.html#resultat'), thumb: asset('assets/images/qa/qa_accessibility_keyboard_01.jpg') },
  { title: 'Contrastes WCAG calculés', section: 'QA · S6', url: asset('pages/qa/index.html#contrastes'), thumb: asset('assets/images/qa/qa_contrast_cards_macro_01.jpg') },
  { title: 'Livraison finale : structure et récapitulatif', section: 'Livraison · S7', url: asset('pages/final/index.html#recap'), thumb: asset('assets/images/final/final_sunrise_causeway_wide_01.jpg') },
  { title: 'Tests presse : 99 sur Metacritic', section: 'Reviews · S8', url: asset('pages/reviews/index.html#verdict'), thumb: asset('assets/images/reviews/review_neon_scorecard_01.jpg') },
  { title: 'Horaires de déblocage par région', section: 'Reviews · S8', url: asset('pages/reviews/index.html#horaires'), thumb: asset('assets/images/reviews/review_midnight_launch_queue_01.jpg') },
  { title: 'Liste de vérification du soir de sortie', section: 'Outils · S23', url: asset('pages/outils/index.html#firmware-outil'), thumb: asset('assets/images/fixes/fixes_console_download_night_01.jpg') },
  { title: 'Se déplacer : pas de téléportation, trois méthodes', section: 'Tips · S26', url: asset('pages/tips/index.html#se-deplacer'), thumb: asset('assets/images/deplacement/move_rideshare_curb_night_01.jpg') },
  { title: 'Voler intelligemment : scanner avant de casser', section: 'Véhicules · S26', url: asset('pages/vehicules/index.html#voler'), thumb: asset('assets/images/deplacement/move_waink_scan_phone_night_01.jpg') },
  { title: 'Les vrais seuils du 100 % (15/18 séries, 300/397 cascades)', section: 'Collectibles · S29', url: asset('pages/collectibles/index.html#seuils-reels'), thumb: asset('assets/images/completion/flamingo_pink_lawn_dusk_01.jpg') },
  { title: 'Réglages et règles de métier de la première semaine', section: 'Tips · S31', url: asset('pages/tips/index.html#reglages-et-metier'), thumb: asset('assets/images/reglages/controller_settings_dark_room_01.jpg') },
  { title: 'Pourquoi 30 fps partout : mesures et explication Rockstar', section: 'Reviews · S31', url: asset('pages/reviews/index.html#30-fps-explique'), thumb: asset('assets/images/reglages/frame_pacing_rays_dusk_01.jpg') },
  { title: 'La soirée de lancement : la panne PSN, pas le jeu', section: 'News · S30', url: asset('pages/news/index.html#soir-de-sortie'), thumb: asset('assets/images/soir-lancement/psn_outage_black_screen_01.jpg') },
  { title: '99 sur Metacritic et la déclaration de Sam Houser', section: 'Reviews · S30', url: asset('pages/reviews/index.html#record-99'), thumb: asset('assets/images/soir-lancement/metacritic_99_newsroom_01.jpg') },
  { title: 'Premières trouvailles : oeuf de la tour, Bigfoot, Belville', section: 'Secrets · S28', url: asset('pages/secrets/index.html#premieres-trouvailles'), thumb: asset('assets/images/jour1/bird_nest_eggs_tower_01.jpg') },
  { title: 'Deux corrections de chiffres assumées (tailles 1.002)', section: 'News · S28', url: asset('pages/news/index.html#correctif-tailles'), thumb: asset('assets/images/jour1/day_one_patch_console_bedroom_01.jpg') },
  { title: 'Avant minuit : firmware PS5 et patch de lancement', section: 'Lancement · S27', url: asset('pages/lancement/index.html#avant-minuit'), thumb: asset('assets/images/depart/launch_console_firmware_update_01.jpg') },
  { title: 'Argent, coffre et entraînement : trois habitudes', section: 'Tips · S27', url: asset('pages/tips/index.html#argent-et-coffre'), thumb: asset('assets/images/depart/money_stash_drawer_home_01.jpg') },
  { title: 'La route de l’argent, chapitre par chapitre', section: 'Économie · S27', url: asset('pages/economie/index.html#route-argent'), thumb: asset('assets/images/depart/money_bank_vault_duffel_01.jpg') },
  { title: 'Cartes et checklists open source', section: 'Outils · S27', url: asset('pages/outils/index.html#cartes-communautaires'), thumb: asset('assets/images/depart/money_comm_maps_setup_night_01.jpg') },
  { title: 'Où en est le jeu au soir du 19', section: 'News · S26', url: asset('pages/news/index.html#etat-j2'), thumb: asset('assets/images/deplacement/move_night_street_quiet_shop_01.jpg') },
  { title: 'Ventes : pourquoi 17 millions n’est pas un chiffre officiel', section: 'News · S25', url: asset('pages/news/index.html#chiffres'), thumb: asset('assets/images/sales/sales_tally_board_night_01.jpg') },
  { title: 'Le direct de 24 h et le piège à spoilers', section: 'Lancement · S25', url: asset('pages/lancement/index.html#direct'), thumb: asset('assets/images/news/news_livestream_watch_party_night_01.jpg') },
  { title: 'Les premières heures : les quatre paquets des Keys', section: 'Économie · S25', url: asset('pages/economie/index.html#keys'), thumb: asset('assets/images/economie/economie_keys_boat_packages_01.jpg') },
  { title: 'Les gestes du premier jour : Dolores, plancher, portes', section: 'Tips · S25', url: asset('pages/tips/index.html#premier-jour'), thumb: asset('assets/images/tips/tips_floorboards_cash_stash_01.jpg') },
  { title: 'Chiffres de vente : officiel, estimé, projeté', section: 'FAQ · S25', url: asset('pages/faq/index.html#chiffres-faq'), thumb: asset('assets/images/news/news_correction_desk_lamp_01.jpg') },
  { title: 'Mesures console par console : qui tient 30 fps', section: 'News · S24', url: asset('pages/news/index.html#mesures'), thumb: asset('assets/images/perf/perf_frame_analysis_desk_01.jpg') },
  { title: 'Panne PlayStation du 18/11 et dépannage', section: 'News · S24', url: asset('pages/news/index.html#reseau'), thumb: asset('assets/images/perf/perf_signin_error_screen_01.jpg') },
  { title: 'Qui tient vraiment 30 images par seconde', section: 'Lancement · S24', url: asset('pages/lancement/index.html#cadences'), thumb: asset('assets/images/perf/perf_pro_console_living_room_01.jpg') },
  { title: '1440p, trois upscalers, deux résultats', section: 'Divers · S24', url: asset('pages/divers/index.html#upscaling'), thumb: asset('assets/images/perf/perf_upscaler_comparison_wall_01.jpg') },
  { title: 'Entretien et stabilité : ce qui dépend de vous', section: 'FAQ · S24', url: asset('pages/faq/index.html#entretien'), thumb: asset('assets/images/perf/perf_thermal_probe_bench_01.jpg') },
  { title: 'Firmware PS5 26.07-14.23.00 obligatoire', section: 'News · S23', url: asset('pages/news/index.html#firmware'), thumb: asset('assets/images/fixes/fixes_firmware_dashboard_dawn_01.jpg') },
  { title: 'Notes de version : ce que les correctifs changent', section: 'Lancement · S23', url: asset('pages/lancement/index.html#notes'), thumb: asset('assets/images/fixes/fixes_patch_waves_room_01.jpg') },
  { title: 'Reconnaissance avant braquage : alarme, caméras, gardes', section: 'Police · S23', url: asset('pages/police/index.html#reconnaissance'), thumb: asset('assets/images/police/police_alarm_panel_backroom_01.jpg') },
  { title: 'Les quatre receleurs et ce qu’ils paient', section: 'Économie · S23', url: asset('pages/economie/index.html#receleurs'), thumb: asset('assets/images/economie/economie_fence_garage_dusk_01.jpg') },
  { title: 'Quatre réflexes que le jeu ne dit pas', section: 'Tips · S23', url: asset('pages/tips/index.html#reflexes'), thumb: asset('assets/images/tips/tips_trunk_outfit_switch_01.jpg') },
  { title: 'Nuit de lancement : la première heure', section: 'Lancement · S9', url: asset('pages/lancement/index.html#premiere-heure'), thumb: asset('assets/images/lancement/lancement_first_drive_dash_01.jpg') },
  { title: 'Technique mesurée : Series X, Series S, PS5', section: 'Lancement · S9', url: asset('pages/lancement/index.html#technique'), thumb: asset('assets/images/lancement/lancement_corner_store_3am_01.jpg') },
  { title: 'Les 51 armes, avec leur visuel', section: 'Catalogue · S10', url: asset('pages/armes/index.html#v-title'), thumb: asset('assets/images/objets/armes/service-carbine.jpg') },
  { title: 'Catalogue visuel : 152 véhicules', section: 'Catalogue · S10', url: asset('pages/vehicules/index.html#catalogue'), thumb: asset('assets/images/objets/vehicules/emerus.jpg') },
  { title: 'Les vraies cartes de Leonida', section: 'Cartes · S10', url: asset('pages/carte/index.html#cartes-reelles'), thumb: asset('assets/images/cartes/carte_leonida_officielle_poster.jpg') },
  { title: 'La faune de Leonida : 27 espèces', section: 'Collectibles · S10', url: asset('pages/collectibles/index.html#faune'), thumb: asset('assets/images/animaux/manatee.jpg') },
  { title: 'Distribution et comédiens', section: 'PRESSE · 18/11', url: asset('pages/personnages/index.html#qui-title'), thumb: asset('assets/images/characters/cast_duo_wanted_poster_01.jpg') },
  { title: 'Vice City', section: 'Carte', url: '#', thumb: asset('assets/images/heroes/vicecity_districts_night_01.jpg'), soon: 'S4' },
  { title: 'Leonida Keys', section: 'Carte', url: '#', thumb: asset('assets/images/map/leonida_keys_paradise_01.jpg'), soon: 'S4' },
  { title: 'Jason Duval', section: 'Personnage', url: '#', thumb: asset('assets/images/characters/characters_jason_fullbody_01.jpg'), soon: 'S4' },
  { title: 'Lucia Caminos', section: 'Personnage', url: '#', thumb: asset('assets/images/characters/characters_lucia_fullbody_01.jpg'), soon: 'S4' },
  { title: 'Carte interactive', section: 'Carte', url: '#', thumb: asset('assets/images/map/map_leonida_aerial_01.jpg'), soon: 'S5' }
];

window.GTA6_SEARCH_INDEX = searchIndex.slice();

export function searchLocal(query, index = window.GTA6_SEARCH_INDEX || searchIndex) {
  const q = normalize(query).trim();
  if (q.length < 2) return [];
  return index.filter((item) => normalize(`${item.title} ${item.section}`).includes(q)).slice(0, 8);
}

/** Conservé pour compatibilité : l'index local est désormais la seule source,
 *  le corpus de recherche n'étant pas publié sur le site. */
export function augmentFromResearch() {
  return Promise.resolve(window.GTA6_SEARCH_INDEX || searchIndex);
}

