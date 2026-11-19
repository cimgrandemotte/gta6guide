# S1 — Synthèse de la recherche (18 novembre 2026, J-1)

> **Fichier de référence lisible.** Les données structurées sont dans `research_data.json`
> (201 faits, 19 sections, 86 sources, chacun avec statut + URL + date).
> L'inventaire critique des sources est dans `research_sources.md`.

---

## 0. Le basculement du 18 novembre

Le point le plus important de cette phase : **l'embargo critiques a été levé aujourd'hui vers 11:00 GMT**,
calé sur le déblocage néo-zélandais. Conséquence : contrairement à ce qu'on pouvait anticiper en S0,
une masse d'informations de **gameplay vérifiables** est désormais disponible via les copies de review
et les previews accréditées (GameSpot, Digital Spy, TrueAchievements, The Independent, TheBigLead…).

| Ce qui est maintenant solide | Ce qui ne l'est toujours pas |
|---|---|
| 5 chapitres, ~100 missions, 50–80 h d'histoire | Noms/synopsis/récompenses de **chaque** mission |
| Système 6 étoiles + indices HUD (visage, tenue, véhicule, compagnon, CCTV) | Comportement détaillé niveau par niveau |
| Carburant, coffre d'armes, limites 2 longues + 2 poings, Focus, poids/fatigue | Statistiques chiffrées de toutes les armes/véhicules |
| 6 stations radio, album 34 titres, score Justice | Playlist complète station par station |
| Metascore 99 (instantané, 146 critiques en fin de journée) | Note définitive + note utilisateurs |
| ~30 activités secondaires | Collectibles, easter eggs in-game, codes de triche, trophées officiels |

Le site sera donc un **guide pré-launch très dense**, avec des pages structurées prêtes à recevoir
les données du 19/11 — pas un guide « complet » fictif.

---

## 1. Fiche technique verrouillée (sources primaires)

| Champ | Valeur | Statut |
|---|---|---|
| Sortie | Jeudi **19 novembre 2026**, minuit heure locale (NZ en premier) | `official` |
| Plateformes natives | PS5, PS5 Pro, Xbox Series X\|S | `official` |
| Xbox One | Via **Xbox Cloud Gaming** uniquement (réglages Series S), + Remote Play | `official` |
| PC | Non annoncé (T1 2027 = rumeur de presse) | `official` / `speculative` |
| Prix | Standard 79,99 $ / 79,99 € · Ultime 99,99 $ / 99,99 € | `official` |
| Précommande | Ouverte le 25/06/2026 ; Pack Vintage Vice City + 1 mois GTA+ | `official` |
| Préchargement | Depuis le 10/11/2026, jusqu'à **212 Go** | `official` |
| Physique | Boîte = code de téléchargement, **aucun disque** | `official` |
| Performance | **30 FPS sur toutes les consoles** ; PS5 Pro = PSSR + ombres ray-tracées, pas de 60 FPS | `official` |
| Mode | **Solo uniquement au lancement** | `official` |
| Moteur / score | RAGE · **Justice** (score adaptative) | `official` / `press_confirmed` |
| ESRB | Mature 17+ | `official` |

**Calendrier Newswire officiel** (à utiliser tel quel pour la page News) : 17/09 The Album · 24/09 Vice City Collection · 08/10 Radio Stations · 15/10 Launch Trailer · 29/10 Original Score by Justice · 03/11 Pre-Load Begins · 05/11 Launch Gallery · 09/11 The Festival (Miami) · 10/11 Pre-Load Now.

---

## 2. Histoire, personnages, carte

* **Cast officiel : 8 profils / 9 personnes** — Jason Duval, Lucia Caminos, Cal Hampton, Boobie Ike, Dre'Quan Priest, Real Dimez (Bae-Luxe & Roxy), Raul Bautista, Brian Heder.
* ⚠ **Découverte majeure** : la longue liste de PNJ du MegaPrompt (Sal Marino, Nadia Okafor, Krystal Kane, Dr Ansel Moreau, Viktor Sokolov, Shérif Clyde Bodine, Valentina…) provient de **leonidaverse.com**, qui présente sa carte comme *« An imagined map ahead of release »* et l'ouvre le 19/11. Ces noms sont **des entrées communautaires imaginées**. Ils iront dans une section « Communauté / non confirmé », jamais dans le cast officiel. Même chose pour la 7e région « Waning Sands ».
* **Carte** : 6 régions officielles (Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga NP). Rob Nelson a bien donné les chiffres 2× GTA V / 3× RDR2 / Vice City 2× Los Santos / banlieues 11× (interview TGG, **août** 2026 — pas juillet), corroborés par EDGE et le NYT. Le prompt avait raison sur le fond ; je passe le statut de `community` à `press_confirmed`.
* **Météo** : le 16/11, The Weather Channel a publié 6 screenshots officiels Rockstar et la déclaration d'Owen Shepherd (VP Art, Light & Rendering) : systèmes « localisés, persistants, dynamiques ». Brouillard marin, orages de marais, pluie dans les Keys. Les **ouragans** sont annoncés par la presse mais pas montrés dans ces 6 visuels.
* ❌ « 62 espèces d'oiseaux », « 5 comtés », « 11 districts de Vice City » : **aucune source primaire trouvée** → ne pas afficher.
* **Cartes communautaires** : GTA VI Mapping / GTADB ≈ 3 300 lieux (Endgame Tools), 2 204 lieux (Leonida Atlas GitHub). Toutes doivent être créditées **CC BY 4.0** et présentées comme reconstructions. Endgame Tools résume parfaitement notre politique : « *before launch, no source for them is worth trusting* » — 5 de ses 9 outils sont « Coming soon ».

---

## 3. Gameplay confirmé (le cœur des futures pages)

**Armes** — 2 armes longues + 2 poings portés, le reste dans le **coffre du véhicule** (logique RDR2) · roue redessinée en 8 emplacements · 4 armes nommées par Rockstar (Moreland 850, Hawk & Little Morgan, Girardi ES9 pour Jason, Klose K17 pour Lucia) · 18 avec preuve first-party selon GTA Intel · personnalisation (silencieux, optiques, chargeurs, teintes, munitions) · PNJ réagissent aux armes dégainées.

**Véhicules** — carburant réel (panne sèche possible, R2/RT ~10 s à la pompe, les stations réparent aussi) · recharge électrique · traceurs GPS sur modèles haut de gamme (retrait payant) · crochetage / clonage de clé · coffre = arsenal + tenues + butin · dégâts = valeur de revente réduite · 6 véhicules officiellement nommés, **aucun chiffre officiel** sur le total (le « 200+ » est un décompte de fans).

**Police (6 étoiles)** — un crime n'est signalé que si un **témoin**, une **alarme** ou une **CCTV** le rapporte. Le HUD suit 5 indices séparés : description physique, tenue, véhicule, compagnon, CCTV. Étoiles blanches = poursuite, clignotantes = recherche, rouges = Heat active dans la zone. Changer de **tenue complète**, abandonner/brûler le véhicule, détruire les images, se séparer du partenaire : chacun efface un indice. À 6 étoiles, la Heat peut couvrir toute la carte.

**Économie** — cash sur soi (perdable) / ATM / solde BuckMe (protégé) · butin physique à **fencer** chez des receleurs spécialisés qui se débloquent · 5 paliers de braquage (supérette → bijouterie → banque → compound → fourgons) · certaines missions d'histoire sont **conditionnées à un capital** · garages achetables, pas de maison (logique de fugitifs) · pas de revenu passif confirmé.

**Relation & corps** — attribut de relation partagé, romance optionnelle, activités de couple, Criminal Profile (réputation), calories/muscle/masse grasse/force, fatigue visible, morphologie encadrée. Bascule de personnage instantanée même en combat véhicule. Focus = ralenti + points faibles.

**Activités** — basket (booste Focus), musculation, MMA, backyard wrestling, mini-golf, billard, pêche, chasse, kayak, plongée, jet-ski, airboat, courses (street / motocross / Gellhorn International Raceway), stand de tir chronométré, skydiving, nightlife, réseaux sociaux in-game, TV, interactions animales.

---

## 4. Astuces, stratégies, techniques, solutions (demande explicite)

Les plus solides viennent des **sessions de review du 18/11** (TheBigLead, 140 h) et des previews accréditées :

1. **Masque avant le crime** > nettoyage après : empêche l'identification faciale.
2. Lire les **icônes sous les étoiles**, pas le seul compteur d'étoiles.
3. **Tenue complète** obligatoire pour effacer l'indice vêtement (chapeau/lunettes = insuffisant) ; stocker des tenues dans le coffre.
4. **Brûler/abandonner** le véhicule repéré : l'icône disparaît, une patrouille peut passer sans reconnaître la nouvelle voiture.
5. **Séparer Jason et Lucia** en poursuite : divise l'attention, peut retirer une étoile.
6. Anticiper le **plein** avant une poursuite ; les stations réparent aussi.
7. **Scan Focus** avant un vol : révèle policiers proches et valeur du véhicule ; tirer dans le moteur immobilise une voiture.
8. **Planifier son loadout** (2+2) et revenir au coffre pour réarmer en mission.
9. **Déposer l'argent** après chaque coup (ATM → BuckMe) sous peine de le perdre à la mort.
10. **Prioriser l'histoire** au début : débloque outils de vol, fences et braquages ; lever les cash gates.
11. Investir dans l'**infrastructure** (outils, véhicule sans traceur, garage, Pay 'n' Spray, barbier) avant les cosmétiques.
12. Ne pas **abîmer** une voiture destinée à la revente.
13. **Focus libre (L3+R3)** : le halo audio circulaire signale une rencontre unique — explorer plutôt que foncer aux marqueurs.
14. **Bâtiments bleu foncé** sur la carte = entrables ; pivoter la carte pour trouver les portes.
15. **Pousser un véhicule** (marcher contre → maintenir Carré) ; **portière** comme arme en voiture, **coup de pied** sur moto.
16. Bascule de personnage en pleine poursuite moto : le partenaire conduit, le joueur tire.
17. Entretenir la relation et la condition physique (sommeil, gym, alimentation).
18. **Éviter** les « money glitch / generator / cheat downloads » pré-lancement : leurres malware.

⚠ Les vidéos YouTube (« 106 Tips » 12/11, « 12 choses Day 1 » 22/10, « Ultimate Pre-Launch Guide » 14/11) et les guides GrandTheft.gg du 18/11 sont **antérieurs à l'accès public** : étiquetés `community`, à re-vérifier après le 19/11. La recherche Reddit ciblée a été peu productive aujourd'hui ; elle sera relancée quand les vrais retours de joueurs existeront.

---

## 5. Musique

* **6 stations prévisualisées** (08/10) : Cocoteo, Back Country, Afro Bank FM, The Chamber, Flash FM, Dirty South Classics, avec leurs DJ.
* **The Album** : 34 titres originaux, Atlantic Records, 19/11/2026 ; 9 titres nommés (Yung Lean/Future/Metro Boomin, Travis Scott, Justice feat. Tame Impala/SZA/King Gizzard, Morgan Wallen, Fuerza Regida, Rauw Alejandro, Cardi B, Keith Richards…).
* **Original Score by Justice** : annonce 29/10, album le 11/12/2026, 30 pistes selon l'annonce / 50 selon le listing Apple Music NZ → divergence à trancher plus tard.
* ⚠ « Flower in a Hurricane » = trailer + album, **pas** une confirmation de diffusion radio.

---

## 6. Online, cheats, trophées, secrets : le mur de J-1

| Sujet | État réel | Décision pour le site |
|---|---|---|
| **GTA VI Online** | Rockstar : jeu **solo** ; aucun mode, nom ou date annoncé. GTA Online (GTA V) continue. Rumeurs 2027 non confirmées. | P14 = hub de statut officiel + rumeurs étiquetées |
| **Codes de triche** | **Aucun** code officiel publié ; toutes les listes en ligne recyclent GTA V ou sont inventées | P11 = page d'état + tableau vide prêt, bouton copier désactivé |
| **Trophées** | Datamine TexFunz2 : **55 configurés** (aucun nom). La liste générique du 08/11 est **fake** (PSNProfiles). PC Gamer / Press-Start publient le 18/11 une liste différente « Vice Got a Price! », plus crédible mais non officielle | P17 = avertissement de conflit + badge « à confirmer via PSN/Xbox » |
| **Collectibles / easter eggs in-game** | N'existent pas encore ; seuls des clins d'œil de trailers sont repérés (Ocean View Hotel, Phil's Ammu-Nation, gecko chemise Vercetti, décor RDR2, Vercetti Estate) | P13/P20 = section « officiel repéré » + zone « découvertes post-launch » vide |
| **Fins** | Rockstar évoque des objectifs optionnels à répercussions narratives, **pas** de fins multiples confirmées | P02d = spoiler toggle + état non confirmé |
| **Missions** | 5 chapitres, ~100 missions, 50–80 h ; pas de liste nominative officielle | P02c = timeline par chapitre, sans inventer de noms |
| **Metascore** | 99 / 146 critiques, 100 % positives, **instantané évolutif** du 18/11 | P18 = chiffre horodaté « au 18/11/2026 » |

---

## 7. Ce que ça change pour la suite du build

* Le **compteur animé** de la homepage peut afficher `6 régions`, `2 protagonistes`, `6 étoiles`, `6 stations radio`, `5 chapitres` — mais **pas** « 200 véhicules » ni « 62 oiseaux » sans badge d'estimation.
* La **carte Leaflet (S5)** utilisera les 6 régions officielles comme couche de base, avec une couche optionnelle « reconstruction communautaire (CC BY 4.0) » clairement désactivable et créditée.
* Chaque page de base de données (armes, véhicules) affichera un **badge de statut** et une mention « chiffres à compléter après le 19/11 ».
* La page **News (P18)** peut être réellement alimentée : calendrier Newswire, météo Weather Channel, firmware PS5, déblocage NZ, embargo et Metascore, Game Awards.
* Les **10 images S2** resteront des illustrations IA originales : les screenshots officiels Rockstar ne sont pas réutilisables tels quels dans un fan guide (et seraient présentés comme officiels à tort). Les visuels seront inspirés de l'esthétique confirmée : néons Vice City, Keys, Grassrivers, météo d'orage, skyline, arsenal, lineup de véhicules.

---

**Checkpoint CP1 validé** → `research_data.json`, `research_sources.md`, `research_findings.md`, `tools/build_research_data.py`.
**Gate :** `CONTINUER` → **S2 — DESIGN_SYSTEM** (4 CSS, 2 JS, 10 JPG haute qualité, 10 MP3).


---

## Amendement S2 — ce que la presse du 18/11 a rendu vérifiable

**283 faits · 20 sections · 114 sources · 14 arbitrages · 12 corrections du prompt.**
`source_url` est désormais attaché à CHAQUE fait ; `s2_press_mission_list` contient les
**93 titres de missions** (22 / 13 / 26 / 25 / 7 par chapitre). Détail : `research_s2_addendum.md`.

| Sujet | Cadrage S1 | Cadrage S2 (après fetch direct) |
|---|---|---|
| Cheats | « aucun test possible avant sortie » | GameSpot a testé une sauvegarde vierge ; listes de presse partielles, prérequis fin d'histoire, L1+R1 + D-pad, **plus de sauvegarde après cheat** |
| Missions | ~100, aucun titre | **93 titres exacts** Press-Start, ~50 h de campagne ; `~100` = arrondi TrueAchievements |
| Trophées | deux listes incompatibles | 55 trophées + Platine `Vice Got A Price!` + `A Long Road` : liste presse vérifiée, toujours non officielle |
| 100 % | indisponible | checklist de presse (100 tâches optionnelles, 300 stunts, 200 véhicules, 100 WAiNK…) masquée jusqu'aux crédits → `SpoilerToggle` |
| Safe codes | absent | **aléatoires** : interdire toute liste statique ; Focus + notes / gardes / écrans |
| Économie | previews génériques | ATM / BuckMe, cash perdu à la mort, cash gates, Scooter Bros Premium 12 500 $, coffres de banque |
| 6 étoiles | HUD + principes | 3★ policier abattu, 5★ zone restreinte, 6★ combat prolongé ; NOOSE, hélicoptères, Hot Areas, Mile Zero |
| Direction artistique | palette MegaPrompt | orange sunsets + néon violet + pastel Art déco + ombres moody → 5 nouveaux tokens CSS |
| Scores | 99 / 109→146 critiques | Metacritic 99 / **146**, OpenCritic **98 / 54**, 100 % recommandent ; ne pas figer |
| Patches | firmware PS5 | patch jeu 1.002.001 : 602,5 Mo PS5 / 1,59 Go Xbox, **aucune note Rockstar** |

**Conséquence S3/S4 :** P01 peut afficher les compteurs vérifiés (6 régions, 2 protagonistes,
6 étoiles, 6 stations, 5 chapitres, 93 missions *badge presse*) ; P11/P12/P17/P20 utilisent des
badges `PRESSE · 18/11` et un spoiler toggle ; P18 est horodatée ; P19 intègre les nouvelles
réponses ; P06/S5 sépare officiel / presse / communauté. Aucune info de presse n'est promue
`official`, aucune donnée post-launch n'est fabriquée.

**Checkpoint CP2 validé** → 4 CSS, 2 JS, 10 JPG, 10 MP3, `design_system.md`, crédits,
amendement de recherche, FSM S2 COMPLETE. **Gate :** `CONTINUER` → **S3 — BUILD_CORE_PAGES**.


---

## Amendement S3 — homepage et passe multi-surfaces

**303 faits · 20 sections · 135 sources · 18 arbitrages · 16 corrections du prompt.**
La passe S3 couvre Rockstar officiel, presse accréditée, forums, YouTube, GitHub,
Reddit et X. Détail et URL : `research_s3_addendum.md` et `research_sources.md`.

| Sujet | Cadrage S2 | Cadrage S3 après intégration |
|---|---|---|
| Codes de coffre | aléatoires GameSpot | Confirmation directe GameSpot ; PlayStationInfo publie trois combinaisons **mission-specific** reprises de PowerPyx → aucune liste universelle, conflit arbitré |
| Scores | Metacritic 99/146, OpenCritic 98/54 | Fetch direct OpenCritic : **98/100, 100 % de recommandation, 63 critiques, 100e percentile** ; ne jamais fusionner avec les snapshots Metacritic |
| Patches | 1.002.001 sans notes | Forbes / Yahoo / VICE : 01.002.000 (~1 Go) puis 01.002.001 (602,5 Mo PS5 / ~1,59 Go Xbox), trois vagues PS5 ; toujours aucune note Rockstar |
| Firmware PS5 | pressenti | 26.07-14.23.00 / 1,267 Go requis avant minuit selon PlayStation Support US relayé par Rockstar et la presse ; post primaire non fetché → `press_confirmed` |
| Embargo | 11:00 GMT | Insider Gaming / ResetEra / métadonnées ; Rockstar n'a pas publié d'horaire → reconstruction `community` |
| Stratégies | GameSpot / Press-Start / Sportskeeda | Ajout des routes 6 étoiles, économie, braquages, Snap Gun, Dye Pack Jammer, cash trucks ; toutes `PRESSE · 18/11` + spoiler |
| Communauté | GitHub / YouTube / leads | `leonida-dispatch`, `gta6-atlas`, MCP, vidéo 106 tips, Reddit stale, X hype : `community`, jamais source de vérité gameplay |

**Conséquence homepage :** compteurs synchronisés avec `research_data.json`,
`data-verify-number` vérifiés par `tools/check_s3.py`, badges sur toutes les
données non officielles, SpoilerToggle sur routes / arbitrages, statut explicite
pour trophées, cheats, checklist, patch notes, PC et GTA VI Online. Le JSON-LD
`VideoGame` ne contient volontairement aucun `aggregateRating` de presse.

**Checkpoint CP3 validé** → `index.html`, `en/index.html`, `main.js`, `search.js`,
`utils.js`, `s3_home.css`, 20 JPG, 12 MP3, SEO, FSM S3 COMPLETE.
**Gate :** `CONTINUER` → **S4 — BUILD_CONTENT_PAGES**.
