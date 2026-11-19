# Amendement S2 — recherche du 18 novembre 2026 (post-embargo)

> **Statut :** vérifié par `web_search` + `fetch_page` direct le 18/11/2026, à J-1 de la sortie.
> **Règle absolue :** tout ce qui suit est `press_confirmed` (copies de review / presse accréditée),
> **jamais `official` Rockstar**. Rockstar n'a publié ni liste officielle de cheats, ni liste PSN/Xbox
> de trophées, ni checklist 100 %, ni notes de patch détaillées. Le guide reste **non officiel**.
> **Spoilers :** missions, trophées et checklist 100 % doivent être derrière un `SpoilerToggle` fermé.

---

## 1. Ce qui a changé depuis la synthèse S1

`research_data.json` passe de **201 faits / 19 sections / 86 sources** à
**283 faits / 20 sections / 114 sources** après amendement S2. Chaque fait porte désormais
`{value, status, sources[], source_url, retrieved_at}`, conformément à
`workflow_master.yaml → fact_policy.json_rule`. La nouvelle section est
`visual_identity_and_art_direction`. La clé structurée `s2_press_mission_list`
contient les **93 titres de missions** relevés par Press-Start.

| Correction | Ancien cadrage S1 | Cadrage S2 vérifié |
|---|---|---|
| Cheats | « aucun code ne peut avoir été testé avant la sortie » | GameSpot a chargé une sauvegarde vierge pour tester les prérequis ; Press-Start et GameSpot publient des listes partielles le 18/11. |
| Trophées | deux listes incompatibles, aucune arbitrable | liste Press-Start / PC Gamer du 18/11 directement vérifiée, 55 trophées ; reste non officielle. |
| Missions | « ~100 missions », liste nominative indisponible | 93 titres exacts en 5 chapitres (22 / 13 / 26 / 25 / 7) relevés dans le *story recap*. |
| 100 % | sujet `post_launch_pending` | checklist de presse publiée, mais masquée en jeu jusqu'au générique et à recouper. |
| Codes de coffre | non traité | **aléatoires** : aucune liste statique fiable (GameSpot, plusieurs playthroughs). |
| Direction artistique | palette MegaPrompt seule | orange sunsets, néon violet, pastel Art déco, ombres moody confirmés par PCMag + recoupements. |

Statuts après amendement : `official 52`, `press_confirmed 173`, `community 30`,
`post_launch_pending 17`, `leak_unverified 7`, `speculative 4`. Contradictions arbitrées : **14** ;
corrections du prompt : **12**.

---

## 2. Sources directement ouvertes en S2

| Source | URL | Apport |
|---|---|---|
| GameSpot — cheats | <https://www.gamespot.com/articles/all-gta-6-cheats-and-how-to-unlock-them/> | prérequis « finir l'histoire », saisie iFruit + L1/R1 + D-pad, impossibilité de sauvegarder après cheat, ~60 entrées, nombreux codes `TBC`, article daté 12:13 UTC et mis à jour 12:18 UTC. |
| Press-Start — cheats | <https://press-start.com.au/news/2026/11/18/every-grand-theft-auto-6-cheat-how-to-unlock/> | onglet dédié après générique, catégories Player / Combat / Spawn Vehicle / Environment / Screen Filters, conditions chiffrées. |
| Press-Start — économie | <https://press-start.com.au/news/2026/11/18/tips-for-managing-your-money-in-grand-theft-auto-6/> | revente de voitures, ATM, cash perdu à la mort/arrestation, piège BuckMe, Scooter Bros Premium 12 500 $ / 3 livraisons par jour, coffres de banque, mugging. |
| Press-Start — trophées | <https://press-start.com.au/news/2026/11/18/gta-6-trophy-list/> | 55 trophées, Platine `Vice Got A Price!`, `A Long Road`, noms de chapitres et de missions. |
| Press-Start — missions | <https://press-start.com.au/news/2026/11/18/heres-how-many-story-missions-are-in-grand-theft-auto-6/> | **93 missions** en 5 chapitres, ~50 h pour l'histoire, titres dans `research_data.json`. |
| Press-Start — 100 % | <https://press-start.com.au/news/2026/11/18/grand-theft-auto-6-100-percent-checklist/> | checklist masquée jusqu'aux crédits : 100 tâches optionnelles, 39 opérations de gang, 22 banques, 100 WAiNK, 300 stunts, 200 véhicules, 50 armes, 100 animaux. |
| TrueAchievements — review | <https://www.trueachievements.com/news/grand-theft-auto-6-review> | ~80 h, ~100 missions, 5 profils criminels, relation, coffre = 5 tenues + armurerie + butin, 3/4★ hélicoptères, 5★ NOOSE, 6★ « jusqu'à la mort », Mile Zero airstrip, 10/10. |
| Sportskeeda — 6 étoiles | <https://www.sportskeeda.com/gta/how-get-6-star-wanted-level-gta-6-and-escape-police> | tuer un policier = 3★, zones restreintes = 5★, tuer des policiers = 6★, étoiles rouges, Hot Areas, changement d'apparence / véhicule / armes. |
| GameSpot — 13 tips | <https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/> | Health / Stamina / Focus, gym en couple, Focus codes couleurs, RydeMe 100 $, bus/trains, WAiNK, alarmes / traceurs / cloneur. |
| GameSpot — braquages | <https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/> | sécurité Low/Medium/High, Snap Gun, **safe codes aléatoires**, CCTV cloud, billets marqués, brouilleur Chap. 3, vault + fourgon. |
| GameSpot — DualSense | <https://www.gamespot.com/articles/gta-6-has-a-clever-ps5-dualsense-trick-for-keeping-you-under-the-speed-limit/> | gâchettes adaptatives = résistance près de la limite de vitesse. |
| GameSpot — gym | <https://www.gamespot.com/articles/gta-6-gym-workouts-have-a-useful-trick-that-saves-you-a-lot-of-time/> | entraînement en duo fait progresser les deux protagonistes. |
| The Independent — live | <https://www.independent.co.uk/extras/indybest/gadgets-tech/video-games-consoles/gta-6-live-b3085508.html> | minuit local, NZ ~13 h avant UK, firmware PS5 obligatoire, Vintage / Ultimate, ESRB M, estimations budget **non officielles**. |
| Newswav (syndication) | <https://newswav.com/article/gta-6-launch-live-latest-updates-as-fans-gear-up-for-release-A2611_rPPMKu> | second patch 602,5 Mo PS5 / 1,59 Go Xbox, vinyle 34 titres, pas d'early access. |
| RockstarINTEL — patch | <https://rockstarintel.com/new-gta-vi-update-released-and-not-everyone-has-gotten-it-heres-why/> | version 1.002.001 / 1.0.2.1, déploiement PS5 progressif, 211,9 Go sur Xbox, aucune note de patch. |
| Gadgets360 — roundup | <https://www.gadgets360.com/games/news/gta-6-review-roundup-highest-rated-game-of-all-time-metacritic-ocarina-of-time-rockstar-games-12344575> | Metacritic 99 / 146 critiques, OpenCritic 98 / 54 critiques, 100 % recommandent, IGN / GameSpot / VGC / Eurogamer / WaPo. |
| OpenCritic (direct) | <https://opencritic.com/news/39914/gta-6-is-officially-the-best-reviewed-game-of-all-time-on-metacritic> | fiche du jeu **98 « Mighty »** ; article Screen Rant « 99 Metascore / 98 reviews » = instantané. |
| PCMag — art direction | <https://au.pcmag.com/games/120955/ive-spent-weeks-in-gta-6s-vice-city-and-i-never-want-to-leave> | *fetch direct HTTP 403* ; extrait de recherche vérifié : moody shadows, orange sunsets, palette néon violet, esprit '80s, réalisme + direction artistique. |
| Gfinity / VGTimes / RockstarINTEL / G2A | voir `research_sources.md` | jaquette rose/orange/violet, néon magenta/cyan, pastel Art déco, Ocean Beach, continuité Vice City 2002. |
| GitHub fork | <https://github.com/mendesjf86/gta6-leonida-atlas> | fork 19 commits / v0.8.1, ~2 198 entrées GTADB, 554 tests + 10 E2E annoncés ; **communautaire**. |
| YouTube S2 | `EwBcYsbJu2I`, `P1YTXjZRUpw`, `DeFeDYE5P6w` | tutoriels pré-lancement, à traiter comme communautaire. |

**Écartés :** `gta6nerd.com` (conseils GTA V recyclés), `gtapulse.com` (analyse de palette notée 4.9/5, datée janvier 2026, allure SEO), `leonidaverse.com` carte « imagined », GrandTheft.gg guides pré-lancement, vidéo « 100 % Walkthrough » du 15/11, rumeur 201 missions, budget 1–1,5 Md$ présenté comme officiel.

---

## 3. Contradictions arbitrées en S2

1. **Cheats** : GameSpot `Cycle Weather = finir l'histoire`, Press-Start `= révéler toute la carte` ; séquence `Attack Force` différente. → badge « divergence presse », ne publier que les saisies concordantes ou testées, attendre le 19/11.
2. **Missions** : `~100` (TrueAchievements, arrondi) vs **93** (story recap Press-Start). → retenir 93, signaler l'arrondi.
3. **OpenCritic** : fiche directe et Gadgets360 = **98**, roundups TheGamer / Tom's Guide = **99**. → retenir 98 « Mighty » + 100 % de recommandation, horodater ; ne pas confondre avec Metacritic 99.
4. **Disponibilité des cheats** : S1 disait « aucun test possible avant sortie ». → corrigé : copies de review accréditées, mais **aucune publication officielle Rockstar** et listes encore partielles.
5. **Mike Zero vs Mile Zero** : Sportskeeda et TrueAchievements ne concordent pas sur l'orthographe de la base aérienne. → afficher les deux avec badge presse jusqu'à recoupement in-game.

---

## 4. Conséquences directes sur le build

- **P11 / P12 / P17 / P20** : alimenter avec `press_confirmed`, **pas** `official` ; `SpoilerToggle` fermé par défaut pour missions, trophées, 100 % ; `CopyButton` uniquement pour les séquences concordantes ; **aucune page « liste de safe codes »**.
- **P06 / S5** : garder les **6 régions officielles** ; les lieux de presse (Mile Zero, VCIA, Gellhorn Raceway…) sont une couche `press_confirmed` distincte des ~2 198 points GTADB `community`.
- **P18** : actualités horodatées 18/11 — firmware PS5, patch 1.002.001, Metacritic 99 / 146 critiques, OpenCritic 98 / 54, 100 % recommandent, vinyle 34 titres.
- **P19 quiz** : 6 régions, 6 étoiles, 2 longues + 2 poings, Justice, 19/11/2026, 93 missions (source Press-Start), safe codes aléatoires.
- **Design system** : tokens dérivés `--c-sunset #FF8A3D`, `--c-violet #8B5CF6`, `--c-pastel #FFB8D9`, `--c-teal #2DE1C2`, `--c-deep-purple #2A1B4D` ; dégradés sunset → rose → violet, scanlines CRT, lueurs sur bitume mouillé.
- **Intégrité** : toutes les illustrations JPG sont originales IA et **jamais** présentées comme captures Rockstar ; voir `assets/images/CREDITS.md`. Tous les MP3 sont des signaux synthétiques originaux ; voir `assets/audio/CREDITS.md`.

---

## 5. Ce qui reste réellement en attente après le 19/11

Publication officielle Rockstar des cheats, liste PSN/Xbox des trophées, checklist 100 % officielle,
localisations de collectibles, Easter eggs découverts **en jeu**, statistiques complètes d'armes /
véhicules, modes GTA VI Online, historique de patches, score utilisateurs stabilisé, carte officielle
complète, glitches post-lancement, fins détaillées, et recoupement des séquences de cheats `TBC`.
