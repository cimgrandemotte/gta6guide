# S1 — Inventaire des sources et évaluation de fiabilité

Collecte effectuée le **18 novembre 2026** (Europe/Paris, J-1).
86 URLs enregistrées dans `research_data.json → sources_registry`.
Chaque fait du JSON porte `status`, `sources[]` et `retrieved_at`.

---

## Barème appliqué

| Statut | Définition | Poids dans le site |
|---|---|---|
| `official` | Rockstar / Take-Two / PlayStation / Xbox, Newswire, fiches Store, déclarations de développeurs | Badge vert, chiffre affichable |
| `press_confirmed` | Média spécialisé accrédité (preview à Rockstar North, copie de review post-embargo), source primaire citée | Badge bleu, formulation prudente |
| `community` | Wikis, cartes de reconstruction, dépôts GitHub, Reddit, YouTube, forums | Badge violet, toujours « selon la communauté » |
| `leak_unverified` | Fuite 2022 / août 2026, datamine anonyme, liste X sans historique | Badge orange + avertissement explicite |
| `post_launch_pending` | N'existe pas encore légalement | Encart « à compléter après le 19/11/2026 » |
| `speculative` | Déduction éditoriale, estimation chiffrée | Badge gris, jamais dans un compteur |

---

## Tier 1 — Sources primaires officielles

| Source | URL | Ce qui en a été extrait | État |
|---|---|---|---|
| Rockstar Games — site GTA VI | https://www.rockstargames.com/VI | Date 19/11, plateformes, « Plays Best On PS5 », synopsis officiel, trailer 1/2, Launch Trailer, An Extended Look, sections Music / Launch Gallery / Only in Leonida / Media | ✅ accessible |
| Rockstar Newswire | https://www.rockstargames.com/newswire | Calendrier officiel : 03/11 pré-load, 05/11 Launch Gallery, 09/11 The Festival, 10/11 Pre-Load Now, 29/10 Score by Justice, 15/10 Launch Trailer, 08/10 Radio Stations, 17/09 The Album | ✅ accessible |
| Rockstar Store FR | https://store.rockstargames.com/fr/game/buy-gta-vi | 79,99 $US Standard, contenu Ultime détaillé, bonus Vintage Vice City « avant le 20 novembre », boîte = code sans disque, préchargement 10/11, 8 screenshots officiels | ✅ accessible (⚠ le DOM répète la liste Ultime sous Standard → artefact) |
| X @RockstarGames | https://x.com/rockstargames | Post 10/11 préchargement, 12/11 « J-7 » + boîtes en magasin | ✅ posts visibles |
| Wikipedia EN | https://en.wikipedia.org/wiki/Grand_Theft_Auto_VI | Infobox (Justice, RAGE, Rob Nelson, plateformes), gameplay : Criminal Profile, poids/fatigue, activités, limite d'armes, Xbox One via Cloud | ✅ accessible |
| ESRB (via Dot Esports) | https://www.esrb.org/ratings/41627/grand-theft-auto-vi/ | Mature 17+ | ✅ relayé |
| PlayStation / Xbox Support (via presse) | — | 30 FPS cible, PSSR + RT sur PS5 Pro, 212 Go, minuit local, Remote Play | ✅ relayé par IGN / Push Square / ActuGaming |

## Tier 2 — Presse spécialisée (accréditations preview / review)

| Source | URL | Apport |
|---|---|---|
| The Independent (live 18/11) | https://www.independent.co.uk/extras/indybest/gadgets-tech/video-games-consoles/gta-6-live-b3085508.html | Ravitaillement confirmé, 30 FPS, review 65 h, bugs mineurs sans crash, Metascore 99 |
| IGN | https://in.ign.com/grand-theft-auto-vi/276604/gta-6-will-run-at-30fps-on-all-consoles-features-ray-tracing-improvements-on-ps5-pro | Déclaration officielle 30 FPS toutes consoles |
| Push Square | https://www.pushsquare.com/news/2026/11/gta-6-ps5-pro-features-revealed-30fps-target-on-both-consoles | 10/10, absence de 60 FPS sur PS5 Pro |
| GameSpot | https://www.gamespot.com/reviews/grand-theft-auto-6-review/ | 10/10, 5 chapitres, heists « Michael Mann » |
| Digital Spy | https://www.digitalspy.com/tech/a74452071/gta6-review/ | Review 200 h, 50–80 h d'histoire, Heat par zone |
| TrueAchievements | https://www.trueachievements.com/news/grand-theft-auto-6-review | ~100 missions, 80 h, six étoiles, identification par tenue |
| ScreenRant | https://screenrant.com/grand-theft-auto-6-review/ | 10.0, duo Jason/Lucia |
| Metacritic | https://www.metacritic.com/game/grand-theft-auto-vi/ | 99 / 146 critiques, 100 % positives, note utilisateur tbd |
| Dexerto / Make Tech Easier / VG Times | [Dexerto](https://www.dexerto.com/gta/gta-6-is-the-joint-best-reviewed-game-of-the-all-time-3429300/) · [MTE](https://maketecheasier.com/gta-6-reviews-metacritic-score/) · [VGTimes](https://vgtimes.com/games/gta-6/news/) | Embargo 11:00 GMT le 18/11, compteur 100→109→146, actualités du jour (firmware PS5, déblocage NZ, Game Awards) |
| Kotaku / Forbes / X @TGGonYT | [Kotaku](https://kotaku.com/gta-6s-vice-city-is-rockstars-biggest-yet-and-the-whole-map-is-three-times-larger-than-red-dead-redemption-2-2000728978) · [Forbes](https://www.forbes.com/sites/brianmazique/2026/10/30/gta-6s-map-is-nearly-as-big-as-gta-4-gta-5-and-red-dead-2-combined-plus-a-201-mission-rumor/) · [TGG](https://x.com/TGGonYT/status/2093478776604860838) | Rob Nelson : 2× GTA V, 3× RDR2, Vice City 2× Los Santos, banlieues 11× ; minicarte sans bascule 2D/3D |
| Red Bull / GTAVice.net (Flow Games) / AllThings.how (El Rubius) | [RedBull](https://www.redbull.com/us-en/gta-6-gameplay-details) · [GTAVice](https://www.gtavice.net/news/flow-games-reveals-more-gta-6-details-fuel-system-no-first-person-mode-30-fps-and-more) · [AllThings.how](https://allthings.how/gta-6-gameplay-details-from-el-rubius-11-things-confirmed-from-his-rockstar-session/) | Systèmes détaillés : carburant, coffre, traceurs GPS, Focus, relation, poids, bascule en combat, séparation duo |
| Dot Esports / GTA Boss / GTA Intel / GTA6 Cartel | [Dot](https://dotesports.com/gta/news/gta-6) · [Boss](https://www.gtaboss.gg/gta-6/guides/gta-6-characters) · [Intel](https://gtaintel.com/news/gta-6-confirmed-weapons-list) · [Cartel](https://gta6cartel.com/news/gta-6-cars-list) | Prix, cast officiel (8 profils), 18 armes avec preuve first-party, 6 véhicules nommés, débunk du « 200+ » |
| ActuGaming (FR) | https://www.actugaming.net/gta-6-guide-complet-832971/ | FAQ FR très complète : 79,99 € / 99,99 €, Xbox One via Cloud, météo/ouragans, 212 Go, 6 régions, préchargement |
| PC Gamer / Press-Start (18/11) | [PC Gamer](https://www.pcgamer.com/games/grand-theft-auto/gta-6-achievements-list/) · [Press-Start](https://press-start.com.au/news/2026/11/18/gta-6-trophy-list/) | Liste de succès « Vice Got a Price! » post-embargo — à recouper avec PSN/Xbox |
| PSNProfiles / GameByte / YaninaGames | [PSN](https://forum.psnprofiles.com/topic/201939-probably-fake-rumored-gta-vi-trophies-list/) · [GameByte](https://www.gamebyte.com/gta-6-trophies-list/) · [Yanina](https://yaninagames.com/blog/gta-6-achievements/) | Débunk de la fausse liste de 55 trophées (08/11) ; datamine TexFunz2 = compte seul |
| The Weather Channel (via Endgame Tools / Beebom / MTE) | [Endgame](https://endgametools.com/en/gta-6/news/gta-6-weather) · [Beebom](https://beebom.com/new-gta-6-weather-screenshots-transform-leonida/) · [MTE](https://maketecheasier.com/weather-channel-gta-6-leonida-forecast/) | 6 screenshots officiels 16/11, déclaration Owen Shepherd : météo localisée / persistante / dynamique |
| Tech2Geek / GTA Fandom / GamesReviews | [Tech2Geek](https://www.tech2geek.net/gta-6-police-explained-how-the-new-wanted-system-works/) · [Fandom](https://gta.fandom.com/wiki/Wanted_Level_in_Grand_Theft_Auto_VI) · [GamesReviews](https://gamesreviews.com/news/08/gta-6-confirms-return-of-six-star-wanted-level-ditching-gta-5s-five-star-cap/) | Système 6 étoiles, indices HUD, témoins/alarme/CCTV, Heat |
| TheBigLead (18/11) | https://www.thebiglead.com/gta-6-tips-the-game-doesnt-tell-you/ | **8 astuces issues d'une session de 140 h** : pousser véhicule, portière, Focus libre, bâtiments bleu foncé |
| Just Jared / WebTech360 / GTASix | [JustJared](https://www.justjared.com/2026/11/17/gta-6-online-release-date-multiplayer-launch/) · [WebTech](https://www.webtech360.com/detail/gta-6-online-what-we-know-about-multiplayer-as-of-en-trend-hp2-99916641.html) · [GTASix](https://gtasix.org/en/guide/cheats/) | Solo au lancement, GTA Online maintenu, aucun code de triche officiel, risque malware |

## Tier 3 — Wikis, cartes et bases communautaires

| Source | URL | Apport | Fiabilité |
|---|---|---|---|
| GTA6 Guide FR | https://gta6guide.fr/ | Carte IA, 185 véhicules, codes de triche « ce qui est connu / ce qui ne l'est pas », galerie officielle | Bonne (distingue confirmé / rumeur) |
| GTA-6-Wiki FR | https://gta-6-wiki.com/fr/ | Wiki FR, pages personnages/lieux/armes/véhicules/carte, Extended Look 26 min + 63 captures | Bonne |
| GTA6 Bible Wiki | https://gta6bible.com/wiki/ | 204 entrées dont 122 « Rockstar-confirmed », 110 véhicules, 28 armes, 28 personnages, 7 catégories | Bonne (provenance étiquetée) |
| GrandTheft.gg | https://grandtheft.gg/ | ⚠ Publie le 18/11 des guides de localisation (armes, safehouses, commissariats) **avant l'accès public** | **Non vérifié** — ne pas en dériver de données |
| GTA6 Explained | https://gta6explained.com/ | Analyses « Verified Analysis » qui débunkent 700 bâtiments, 600 000 animations, microtransactions, fins multiples | Bonne (démarche critique) |
| GTABase | https://www.gtabase.com/grand-theft-auto-6/ | Features guide MAJ 17/11, prix FR/US, contenu Ultime, single-player | Bonne, mais une inférence « Online standalone » est spéculative |
| Leonida State Guide | https://leonidastate.guide/ | Carte 3D, wiki, radio tuner navigateur, outils créateurs, « built in public » | Projet en construction |
| LeonidaVerse | https://leonidaverse.com/en/gta-6-map | ⚠ **« An imagined map ahead of release »** : 7 régions (Waning Sands), ~2 000 marqueurs, ~40 PNJ, collections chiffrées ; ouverture annoncée le 19/11 | **Spéculatif** — origine de la liste de PNJ du MegaPrompt |
| Endgame Tools | https://endgametools.com/en/gta-6/ | Carte GTA VI Mapping ~3 300 lieux **explicitement présentée comme reconstruction** ; 5 outils sur 9 « Coming soon » | Excellente honnêteté : « avant la sortie, aucune source ne vaut la peine d'être crue » |
| vice-city.app | https://vice-city.app/ | 31 personnages, 163 lieux, 172 véhicules, 37 armes, 216 titres radio, « charted by hand from launch day » | Communautaire, chiffres à badge |
| GTA Intel / GTA6 Cartel / GTA6 Quest Vault / Esports Guides / GTA6 Features | multiples | Bases armes/véhicules, comparatifs de mécaniques | Qualité inégale, toujours recouper |
| GTA Boss, gta6hype, tracker.gg, GamesRadar | [Boss](https://www.gtaboss.gg/gta-6/guides/gta-6-preorder-guide) · [Hype](https://www.gta6hype.com/release/) · [Tracker](https://tracker.gg/gta6/release-date) · [GamesRadar](https://www.gamesradar.com/gta-6-guide/) | Éditions, timeline des reports, hub | GamesRadar : page JS, contenu peu extractible ce jour |

## Tier 3 bis — GitHub (outils open-source pour S5)

| Dépôt | Stack / licence | Utilité pour notre carte |
|---|---|---|
| [navanem/gta6-leonida-atlas](https://github.com/navanem/gta6-leonida-atlas) | Vite + React + TS strict, Leaflet, Zustand, Dexie/IndexedDB, Three.js ; AGPL-3.0 ; données GTADB **CC BY 4.0** ; 2 204 lieux, 6 régions, v0.8.0 | Modèle d'architecture pour `map_leonida.js`, notion d'« evidence » par marqueur |
| [cleementt26/leonida-atlas](https://github.com/cleementt26/leonida-atlas) | Atlas **FR**, filtres de fiabilité, tactile ; © YANIS V16 & GTA VI Mapping Community via GTADB CC BY 4.0 | Libellés FR des régions, UX filtres |
| [rhyovar/leonida-dispatch](https://github.com/rhyovar/leonida-dispatch) | Companion app, tracker `localStorage`, MIT (code) ; l'auteur marque tracker/database/collectibles « placeholder » et crew planner « spéculatif » | Patron pour notre checklist 100 % (P17) |
| [gta6mapx/gta6mapx](https://github.com/gta6mapx/gta6mapx) | Carte « evidence-labeled intel » | Idée de badges de preuve sur les marqueurs |

⚠ Si des coordonnées GTADB sont réutilisées en S5, **crédit CC BY 4.0 obligatoire** + mention « reconstruction communautaire, carte non officielle ».

## Tier 3 ter — Réseaux sociaux / vidéo / forums

| Canal | Résultat | Traitement |
|---|---|---|
| X @RockstarGames | 2 posts officiels exploités (10/11, 12/11) | `official` |
| X @weatherchannel | Thread du 16/11, 20:40 UTC, 6 screenshots + déclaration Owen Shepherd | `official` (visuels fournis par Rockstar) |
| X @TGGonYT | Citation directe de Rob Nelson sur la taille de la carte (28/08) | `press_confirmed` |
| YouTube | [106 Tips (12/11)](https://www.youtube.com/watch?v=DeFeDYE5P6w), [12 choses Day 1 (22/10)](https://www.youtube.com/watch?v=a-YFN3ES69M), [Ultimate Pre-Launch Guide (14/11)](https://www.youtube.com/watch?v=UyfLYHAbdAQ), [playlist Tips](https://www.youtube.com/playlist?list=PLNrk08jMVrPc), [100+ hidden details](https://www.youtube.com/watch?v=7WPqL8SPqiE), [« 100% Walkthrough Part 1 » daté 15/11](https://www.youtube.com/watch?v=yBCdznZor38) | `community` — la dernière est antérieure à la sortie, origine douteuse |
| Reddit r/GTA6 / r/gta6game | Thread « GTA VI Mysteries » (souhaits + leaks 2022), discussions PC/30 FPS, réactions mitigées aux previews | `community` ; recherche ciblée peu productive, à refaire après le 19/11 |
| PSNProfiles forums | Thread « [Probably Fake] Rumored GTA VI trophies list » | Source de débunk |
| Instagram @rockstargames | Aucun résultat exploitable ce jour | Utiliser la **Launch Gallery** officielle (Newswire 05/11) comme source de visuels |

## Tier 4 — Leaks

| Source | Traitement |
|---|---|
| [Eldorado.gg — GTA 6 Leaks](https://www.eldorado.gg/blog/grand-theft-auto-en/gta-6-leaks/) (URL redirigée vers la liste d'armes) | Fuites d'août 2026 = build de développement **ancien**, non représentatif après l'Extended Look du 27/08 |
| Fuite 2022 (via [Reddit](https://www.reddit.com/r/GTA6/comments/1ksg2v4/gta_vi_mysteries/)) | ~1 600 random events, Skunk Ape, UFO, « Missing Tourists » : à n'afficher qu'avec badge `leak_unverified` |
| Datamine TexFunz2 (07/11) | Le **compte** 55 succès est rapporté ; les **noms** circulant sont faux |

---

## 🔴 Pièges identifiés pendant la collecte

1. **Sites SEO / agrégateurs** se présentant comme des sources officielles (gta6cheatcodes, gta6matrix, ordergta6, gta6wiki.io, neoteo, thegta-6.com…). Toujours remonter à Rockstar / PlayStation / Xbox.
2. **Pages datées du 19/11/2026** alors que nous sommes le 18/11 (décalage d'indexation / fuseau NZ). Ne pas les traiter comme « après sortie ».
3. **Guides « post-launch » publiés avant la sortie** (GrandTheft.gg 18/11, walkthrough YouTube 15/11) : contenu invérifiable, probablement généré en masse.
4. **Deux listes de trophées incompatibles** : la rumeur générique du 08/11 (fake) et la liste post-embargo du 18/11 (plus crédible mais non officielle).
5. **Chiffres de bases communautaires divergents** : 200+/185/172/110/~100 véhicules ; 28/18 armes ; 6/7 régions.
6. **DOM du Rockstar Store FR** répétant la liste Ultime sous l'édition Standard.

→ Toutes ces divergences sont arbitrées dans `research_data.json → contradictions_and_arbitrations`.


---

## Amendement S2 — 28 sources supplémentaires vérifiées le 18/11/2026

> Après la levée d'embargo, `research_data.json` passe à **283 faits / 20 sections / 114 sources**.
> Ces ajouts sont `press_confirmed` ou `community`, **jamais `official`** : Rockstar n'a pas publié
> les listes de cheats / trophées / missions / 100 %. Détail complet : `research_s2_addendum.md`.

### Tier 2 — Presse accréditée post-embargo (fetch direct)

| Source | Apport |
|---|---|
| [GameSpot — All GTA 6 Cheats](https://www.gamespot.com/articles/all-gta-6-cheats-and-how-to-unlock-them/) | prérequis fin d'histoire, L1+R1 + D-pad, plus de sauvegarde, 60+ cheats, codes TBC |
| [GameSpot — 13 tips](https://www.gamespot.com/articles/gta-6-tips-everything-i-wish-i-knew-before-i-started-playing/) | Health/Stamina/Focus, gym duo, RydeMe, WAiNK, alarmes / traceurs |
| [GameSpot — Safe codes & robberies](https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/) | **codes aléatoires**, Snap Gun, CCTV cloud, billets marqués, fourgon / vault |
| [GameSpot — DualSense](https://www.gamespot.com/articles/gta-6-has-a-clever-ps5-dualsense-trick-for-keeping-you-under-the-speed-limit/) | gâchettes adaptatives et limite de vitesse |
| [GameSpot — Gym](https://www.gamespot.com/articles/gta-6-gym-workouts-have-a-useful-trick-that-saves-you-a-lot-of-time/) | entraînement en duo = 2 personnages |
| [Press-Start — Cheats](https://press-start.com.au/news/2026/11/18/every-grand-theft-auto-6-cheat-how-to-unlock/) | catégories, conditions chiffrées, onglet post-générique |
| [Press-Start — Économie](https://press-start.com.au/news/2026/11/18/tips-for-managing-your-money-in-grand-theft-auto-6/) | ATM, BuckMe, Scooter Bros Premium 12 500 $, coffres, revente |
| [Press-Start — Trophées](https://press-start.com.au/news/2026/11/18/gta-6-trophy-list/) | 55 trophées, Platine `Vice Got A Price!`, `A Long Road` |
| [Press-Start — 93 missions](https://press-start.com.au/news/2026/11/18/heres-how-many-story-missions-are-in-grand-theft-auto-6/) | 5 chapitres, 93 titres, ~50 h |
| [Press-Start — 100 % checklist](https://press-start.com.au/news/2026/11/18/grand-theft-auto-6-100-percent-checklist/) | checklist masquée jusqu'aux crédits ; SPOILERS |
| [TrueAchievements — review 10/10](https://www.trueachievements.com/news/grand-theft-auto-6-review) | ~80 h, 5 profils criminels, coffre 5 tenues, 6★, Mile Zero |
| [Sportskeeda — 6 étoiles](https://www.sportskeeda.com/gta/how-get-6-star-wanted-level-gta-6-and-escape-police) | 3★ / 5★ / 6★, étoiles rouges, Hot Areas |
| [The Independent — live](https://www.independent.co.uk/extras/indybest/gadgets-tech/video-games-consoles/gta-6-live-b3085508.html) | minuit local, firmware PS5, Vintage / Ultimate, ESRB M |
| [Newswav — syndication live](https://newswav.com/article/gta-6-launch-live-latest-updates-as-fans-gear-up-for-release-A2611_rPPMKu) | patch 602,5 Mo / 1,59 Go, vinyle 34 titres, pas d'early access |
| [RockstarINTEL — patch 1.002.001](https://rockstarintel.com/new-gta-vi-update-released-and-not-everyone-has-gotten-it-heres-why/) | version, taille, déploiement progressif, 211,9 Go |
| [GGRecon — second update](https://www.ggrecon.com/articles/gta-6-second-update-before-launch/) | recoupement patch, aucune note officielle |
| [Make Tech Easier — patch](https://maketecheasier.com/gta-6-patch-01-002-001-size/) | 602,5 Mo / 1,6 Go, version 01.002.001 |
| [Gadgets360 — roundup](https://www.gadgets360.com/games/news/gta-6-review-roundup-highest-rated-game-of-all-time-metacritic-ocarina-of-time-rockstar-games-12344575) | Metacritic 99 / 146, OpenCritic 98 / 54, 100 % recommandent |
| [OpenCritic — direct](https://opencritic.com/news/39914/gta-6-is-officially-the-best-reviewed-game-of-all-time-on-metacritic) | fiche **98 Mighty**, article 99 / 98 reviews = instantané |
| [TheGamer — roundup](https://www.thegamer.com/gta-6-review-round-up/) | IGN / GameSpot / VGC, 99 annoncé sur les deux agrégateurs (à arbitrer) |
| [Tom's Guide — live](https://www.tomsguide.com/news/live/gta-6-review-roundup-live-updates) | *fetch 403* ; extrait de recherche : roundup 99 / 100 % recommandent |
| [PCMag — art direction](https://au.pcmag.com/games/120955/ive-spent-weeks-in-gta-6s-vice-city-and-i-never-want-to-leave) | *fetch 403* ; extrait vérifié : orange sunsets, néon violet, ombres moody |
| [Gfinity — cover art](https://www.gfinityesports.com/article/from-gta-1-to-gta-6-the-evolution-of-gtas-iconic-cover-art) | jaquette rose / violet / orange, continuité Vice City 2002 |
| [VGTimes — covers](https://vgtimes.com/articles/158598-all-gta-covers.html) | palette néon, duo Jason/Lucia |
| [RockstarINTEL — key art](https://rockstarintel.com/new-gta-6-cover-art-wallpapers-logo-released/) | logo VI dégradé néon pink / purple / orange |
| [G2A — Vice City then/now](https://www.g2a.com/news/gta-6-news/gta-vi-vs-gta-vice-city-iconic-locations-comparison/) | pastel Art déco, jour chaud / nuit néon |

### Tier 3 — Communauté / outils / vidéos

| Source | Traitement |
|---|---|
| [GitHub mendesjf86/gta6-leonida-atlas](https://github.com/mendesjf86/gta6-leonida-atlas) | fork v0.8.1, ~2 198 entrées GTADB, 554 tests + 10 E2E annoncés ; NON officiel |
| [YouTube `EwBcYsbJu2I`](https://www.youtube.com/watch?v=EwBcYsbJu2I) / [`P1YTXjZRUpw`](https://www.youtube.com/watch?v=P1YTXjZRUpw) | tutoriels pré-lancement, `community` |
| [gta6nerd.com](https://gta6nerd.com/articles/tips-tricks/) | **écarté** : conseils GTA V recyclés |
| gtapulse.com « color palette » 4.9/5 | **écarté** : page SEO datée janvier 2026, pas de source primaire |

### Pièges S2 supplémentaires

1. L'URL GameSpot `.../1100-6536789/` renvoie un article **Nintendo Switch 2** : utiliser l'URL canonique sans ID.
2. `https://press-start.com.au/news/2026/11/18/heres-grand-theft-auto-6s-full-100-checklist/` redirige vers un slug **100-percent-checklist** / agrégat missions : utiliser l'URL canonique vérifiée.
3. PCMag et Tom's Guide renvoient **HTTP 403** au fetch direct : ne retenir que les extraits de recherche recoupés.
4. Les listes de cheats contiennent encore des `TBC` et divergent entre GameSpot / Press-Start.
5. « 99 sur OpenCritic » circule alors que la fiche directe affiche **98** : horodater et arbitrer.

---

## Amendement S3 — 21 sources proposées (18/11/2026)

Ces URL ont été ajoutées au registre par `tools/patch_research_s3.py` ; le total
`research_data.json` passe de **114 à 135 sources**. Voir `research_s3_addendum.md`
pour les arbitrages et le traitement par surface.

| Clé registre | URL | Surface |
|---|---|---|
| `rockstar_launch_gallery` | <https://www.rockstargames.com/VI/launch-gallery> | Rockstar officiel |
| `x_rockstar_launch_gallery` | <https://x.com/RockstarGames/status/2118357919229964343> | X / forum / social |
| `mezha_firmware` | <https://mezha.net/eng/news/mezha-57890459decccd8af6f62271_sony_confirms_ps5/> | Presse / agrégateur |
| `psinfo_firmware` | <https://www.playstationinfo.de/en/2026/11/18/gta-6-launches-on-ps5-only-with-a-new-update-and-sony-now-confirms-the-requirement/> | Presse / agrégateur |
| `forbes_second_patch` | <https://www.forbes.com/sites/brianmazique/2026/11/17/gta-6-just-got-a-second-update-before-anyone-can-play-it-and-rockstar-still-isnt-saying-what-it-changes/> | Presse / agrégateur |
| `opencritic_reviews_s3` | <https://opencritic.com/game/15398/grand-theft-auto-vi/reviews> | Presse / agrégateur |
| `talkesport_launch_live` | <https://www.talkesport.com/gta-6/gta-6-launch-live-updates/> | Presse / agrégateur |
| `gagadget_reviews` | <https://gagadget.com/en/734770-gta-vi-hits-99-on-metacritic-ahead-of-its-november-19-launch/> | Presse / agrégateur |
| `insider_embargo` | <https://insider-gaming.com/grand-theft-auto-6-review-embargo/> | Presse / agrégateur |
| `gamespot_six_star_s3` | <https://www.gamespot.com/articles/how-to-get-a-six-star-wanted-level-in-gta-6/> | Presse / agrégateur |
| `gamespot_money_s3` | <https://www.gamespot.com/articles/best-ways-to-make-money-fast-in-gta-6/> | Presse / agrégateur |
| `gamespot_robberies_s3` | <https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/> | Presse / agrégateur |
| `psinfo_safe_codes_s3` | <https://www.playstationinfo.de/en/2026/11/18/gta-6-guide-all-known-safe-codes-and-how-to-pull-off-the-heists-successfully/> | Presse / agrégateur |
| `youtube_106_tips_s3` | <https://www.youtube.com/watch?v=DeFeDYE5P6w> | YouTube |
| `reddit_gta6game_s3` | <https://www.reddit.com/r/gta6game/> | Reddit |
| `github_leonida_dispatch_s3` | <https://github.com/rhyovar/leonida-dispatch> | GitHub |
| `github_gta6_atlas_s3` | <https://github.com/jerrysf/gta6-atlas> | GitHub |
| `github_vicecity_mcp_s3` | <https://github.com/fshbeeb/vicecitymission-mcp> | GitHub |
| `x_gtasix_updates_s3` | <https://x.com/gtasix_> | X / forum / social |
| `x_gta6_unlimited_s3` | <https://x.com/GTA_Unlimited/status/2122719536457674969> | X / forum / social |
| `resetera_embargo_s3` | <https://www.resetera.com/threads/insider-gaming-gta-6-review-embargo-drops-at-3-00-am-pt-on-wednesday-november-18.1690603/> | X / forum / social |

**Règle S3 :** seules les entrées `rockstar_*` et le post X officiel
RockstarGames peuvent alimenter `official`. Les autres restent
`press_confirmed` ou `community`, avec badge et horodatage.
