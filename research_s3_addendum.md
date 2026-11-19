# Addendum S3 — BUILD_CORE_PAGES · 18/11/2026

**Objet.** Passe de recherche temps réel effectuée avant la construction de la homepage définitive : internet général, presse accréditée, forums, YouTube, GitHub, Reddit et réseaux sociaux. Les résultats sont intégrés à `research_data.json` par `tools/patch_research_s3.py` avec `source_url` sur **303 / 303 faits**, **135 sources** et **20 sections**. Aucune donnée de presse / communauté / réseau social n'est promue `official`.

**Volume de la passe S3.** 17 recherches ciblées (`web_search`) et 16 lectures directes (`fetch_page`). Surfaces couvertes : Rockstar officiel, Newswire, Store, GameSpot, Press-Start / S2, Forbes / Yahoo / VICE / TechTimes, Mezha / PlayStationInfo / TechBriefly, OpenCritic, Metacritic via round-ups, Insider Gaming / ResetEra, PlayStationInfo, X / RockstarGames / comptes de fans, YouTube, Reddit, GitHub. Les pages 403 / modales / SEO contradictoires déjà écartées en S1/S2 n'ont pas été réutilisées comme preuves.

## 1. Politique d'affichage

| Statut `research_data.json` | Badge homepage | Règle |
|---|---|---|
| `official` | `OFFICIEL` | Uniquement Rockstar / Take-Two / PlayStation / Xbox primaire. |
| `press_confirmed` | `PRESSE · 18/11` | Relevé accrédité ou direct du 18/11, horodaté, jamais « publication Rockstar ». |
| `community` | `COMMUNAUTÉ` | Forum, GitHub, YouTube, Reddit, X, agrégation de fan. |
| `post_launch_pending` | `EN ATTENTE · 19/11` | Section indisponible légalement / recoupement en jeu requis. |
| `leak_unverified` | `FUITE NON VÉRIFIÉE` | Jamais affichée comme fait de gameplay. |
| `speculative` | `ESTIMATION` | Déduction explicitement étiquetée. |

Tout contenu sensible (missions, codes, fins, routes 6 étoiles, conditions de trophées) est derrière un **SpoilerToggle** avec `aria-expanded` / `aria-controls`. Les chiffres visibles de la homepage sont vérifiés par `tools/check_s3.py` contre `research_data.json` via `data-verify-number`.

## 2. Sources primaires officielles

| Source | Ce qui est retenu | Statut |
|---|---|---|
| [Rockstar Newswire](https://www.rockstargames.com/newswire) | Pré-load 10/11, Festival 09/11, Launch Gallery 05/11, Trailer / Radio / Justice. | OFFICIEL |
| [Rockstar VI](https://www.rockstargames.com/VI) | 19 novembre 2026, PS5 / Xbox Series, « Plays Best On PS5 », Jason / Lucia, médias, Only in Leonida. | OFFICIEL |
| [Launch Gallery](https://www.rockstargames.com/VI/launch-gallery) | Galerie de screenshots communiquée par Rockstar. | OFFICIEL |
| [Rockstar Games sur X · 5/11](https://x.com/RockstarGames/status/2118357919229964343) | « See you in Leonida on November 19 » + lien Launch Gallery. | OFFICIEL |
| [Rockstar Store FR](https://store.rockstargames.com/fr/game/buy-gta-vi) | Standard 79,99 € / Ultimate 99,99 €, Vintage, code-in-box. | OFFICIEL |

Arbitrage : ces sources priment sur les pages SEO qui avancent des dates, prix, préchargements ou modes online contradictoires. Rockstar n'a publié ni liste officielle de trophées / cheats / checklist 100 % / safe codes, ni notes de patch, ni annonce GTA VI Online ou PC.

## 3. Presse post-embargo du 18/11

| Sujet | Relevé | Source directe | Décision |
|---|---|---|---|
| 6 étoiles | Rester après un policier abattu, prolonger la poursuite, quitter le centre vers Leonard / Lummox ou Kelly County, changer tenue / apparence / véhicule. | [GameSpot 6-star](https://www.gamespot.com/articles/how-to-get-a-six-star-wanted-level-in-gta-6/) | PRESSE · 18/11 + SPOILER. |
| Argent rapide | Kenton, planques / revendeurs, Moses / Randy, Pay'N'Spray, Fleeca / commerces haut de gamme, Dye Pack Jammers, Starlet Motel. | [GameSpot money](https://www.gamespot.com/articles/best-ways-to-make-money-fast-in-gta-6/) | PRESSE · 18/11 + SPOILER. |
| Braquages | Low / Medium / High, alarme, CCTV, Snap Gun, Focus, billets marqués, cash trucks / Yasmani. | [GameSpot robberies](https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/) | PRESSE · 18/11 + SPOILER. |
| Codes de coffre | **Aléatoires** sur plusieurs playthroughs ; aucun code universel fiable. | [GameSpot safe codes](https://www.gamespot.com/articles/gta-6-safe-codes-and-robberies-guide/) | Règle de vérité S3. |
| Codes statiques divergents | Trois combinaisons spécifiques à la chaîne Yasmani, reprises de PowerPyx, image « KI Bild ». | [PlayStationInfo](https://www.playstationinfo.de/en/2026/11/18/gta-6-guide-all-known-safe-codes-and-how-to-pull-off-the-heists-successfully/) | COMMUNAUTÉ / SPOILER ; jamais une liste universelle. |
| OpenCritic | 98/100, 100 % de recommandation, 63 critiques dans le JSON-LD, 100e percentile. | [OpenCritic reviews](https://opencritic.com/game/15398/grand-theft-auto-vi/reviews) | PRESSE · 18/11, instantané direct. |
| Metacritic | 99 / 146 critiques dans un live ; autres snapshots 99/100 et 99/109. | [TalkEsport live](https://www.talkesport.com/gta-6/gta-6-launch-live-updates/), [Gagadget round-up](https://gagadget.com/en/734770-gta-vi-hits-99-on-metacritic-ahead-of-its-november-19-launch/) | PRESSE · 18/11 ; ne jamais fusionner avec OpenCritic. |
| Patch pré-lancement | 01.002.000 (~1 Go, 13/11) puis 01.002.001 (602,5 Mo PS5 / ~1,59 Go Xbox, 16/11), trois vagues PS5, aucune note Rockstar. | [Forbes](https://www.forbes.com/sites/brianmazique/2026/11/17/gta-6-just-got-a-second-update-before-anyone-can-play-it-and-rockstar-still-isnt-saying-what-it-changes/) | PRESSE · 18/11 ; aucun day-one patch annoncé. |
| Firmware PS5 | 26.07-14.23.00 / 1,267 Go requis avant GTA VI, selon PlayStation Support US relayé par Rockstar et la presse. | [Mezha](https://mezha.net/eng/news/mezha-57890459decccd8af6f62271_sony_confirms_ps5/), [PlayStationInfo firmware](https://www.playstationinfo.de/en/2026/11/18/gta-6-launches-on-ps5-only-with-a-new-update-and-sony-now-confirms-the-requirement/) | PRESSE · 18/11 ; post X primaire non fetché directement. |
| Embargo | 11:00 GMT / 12:00 CET provient d'Insider Gaming, métadonnées et forums ; Rockstar n'a pas publié d'horaire. | [Insider Gaming](https://insider-gaming.com/grand-theft-auto-6-review-embargo/), [ResetEra](https://www.resetera.com/threads/insider-gaming-gta-6-review-embargo-drops-at-3-00-am-pt-on-wednesday-november-18.1690603/) | COMMUNAUTÉ ; reviews en ligne le 18/11, heure non officialisée. |

## 4. Forums, vidéos, dépôts, réseaux

| Surface | Signal | Traitement |
|---|---|---|
| YouTube | [106 tips / 1ceStream, 12/11, 14:02](https://www.youtube.com/watch?v=DeFeDYE5P6w) : 212 Go, carte, météo, véhicules, police, économie. | COMMUNAUTÉ : compilation de sources, pas une documentation officielle. |
| Reddit | [r/gta6game](https://www.reddit.com/r/gta6game/) : résultats dominés par une vieille spéculation PC de 2021. | COMMUNAUTÉ stale ; aucune config PC officielle. |
| GitHub | [rhyovar/leonida-dispatch](https://github.com/rhyovar/leonida-dispatch) : compagnon fan-made, placeholders explicites. | COMMUNAUTÉ : modèle d'UX, pas de vérité gameplay. |
| GitHub | [jerrysf/gta6-atlas](https://github.com/jerrysf/gta6-atlas) : Next.js, MapLibre, checklist, datasets vides jusqu'au 19/11. | COMMUNAUTÉ : bon patron de dégradation gracieuse. |
| GitHub | [fshbeeb/vicecitymission-mcp](https://github.com/fshbeeb/vicecitymission-mcp) : ~1 900 landmarks communautaires. | COMMUNAUTÉ : pas une cartographie Rockstar. |
| X / social | [RockstarGames](https://x.com/RockstarGames/status/2118357919229964343), [GTA 6 Updates](https://x.com/gtasix_), [GTA 6 Unlimited](https://x.com/GTA_Unlimited/status/2122719536457674969), lives et chiffres de hype. | OFFICIEL pour Rockstar uniquement ; le reste COMMUNAUTÉ, sans chiffre promu. |

## 5. Contradictions arbitrées en S3

1. **Safe codes** : GameSpot « randomisés » vs PlayStationInfo « trois codes mission-specific ». → Aucune liste universelle publiée ; les codes de mission restent masqués, badgés et en attente de recoupement in-game.
2. **Scores** : OpenCritic 98 / 63 critiques vs Metacritic 99 / 146, 99/109, 99/100 et OpenCritic 98 / 54 dans un snapshot plus ancien. → Chaque chiffre garde son agrégateur et son horodatage ; aucune moyenne commune.
3. **Firmware / patches** : 14.23 obligatoire et deux builds pré-lancement sans notes Rockstar. → Distinguer mise à jour système et patch jeu, ne pas annoncer de day-one patch.
4. **Embargo** : 11:00 GMT rapporté vs absence de publication Rockstar. → « Reviews en ligne le 18/11 » = presse ; l'heure = reconstruction communautaire.
5. **Cheats / trophées / missions** : 93 missions, 55 trophées et listes de cheats de presse restent `press_confirmed`, derrière SpoilerToggle, en attente des listes PSN / Xbox / Rockstar.

## 6. médias S3

- **10 JPG** `IMG011–IMG020` générés en haute qualité, puis optimisés par `tools/optimize_images_s3.py` : 9 paysages 1920×1080 + 1 portrait 1280×1920, JPEG q95, 4:4:4, progressif. Aucun PNG / SVG / WebP / AVIF.
- **2 MP3** `AUD011–AUD012` générés par `tools/make_audio_s3.py` via NumPy + lameenc : une ambiance « Sunset Cruise » et un jingle d'ouverture. Aucun WAV, aucun sample sous licence, aucune musique Rockstar.
- Le lecteur S3 expose les **10 MP3 S2 + 2 MP3 S3**, en URLs locales relatives, `preload="none"`, sans autoplay. La homepage intègre les **10 JPG S2** et les **10 JPG S3** via `<img>` avec `alt`, `loading="lazy"` et `width` / `height`.
- Quotas de la réponse respectés : **10 images générées**, **2 audios générés**, soit ≤ 10 de chaque. Formats interdits livrés : 0.

## 7. À recouper après le 19/11

- Codes de coffre, 93 missions, 55 trophées, checklist 100 % et conditions de cheats.
- Notes de patch Rockstar, firmware 14.23, éventuel day-one patch et taille d'installation finale.
- Toute annonce GTA VI Online / PC / transfert GTA Online.
- Remplacement des datasets placeholder GitHub par des positions et statistiques vérifiées en jeu.

**Livrables liés :** `index.html`, `en/index.html`, `assets/js/main.js|search.js|utils.js`, `assets/css/s3_home.css`, `assets/images/CREDITS.md`, `assets/audio/CREDITS.md`, `robots.txt`, `sitemap.xml`, `manifest.json`, `tools/check_s3.py`.
