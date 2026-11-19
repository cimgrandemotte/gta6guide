# Amendement recherche S4 — BUILD_CONTENT_PAGES

**Date :** 18 novembre 2026 · **État :** S4 · **Groupe :** G1 (Histoire)
**Périmètre :** `pages/histoire/index.html`, `pages/histoire/synopsis.html`, `pages/histoire/missions.html`

## 1. Surfaces interrogées

Recherche multi-surfaces pour le groupe G1 : web généraliste, presse accréditée
post-embargo, forums, YouTube, GitHub, Reddit et réseaux sociaux. Les pages
Rockstar « Only in Leonida » (Jason, Lucia) ont été lues directement et servent
de seule référence `official` avec la page VI et le Store FR déjà enregistrés.

## 2. Ce que l'amendement ajoute

| Élément | Valeur |
|---|---|
| Faits ajoutés | 10 (`MIS-04` → `MIS-14` sauf doublon, `CHA-18` → `CHA-27`) |
| Sources ajoutées | 10 |
| Totaux `research_data.json` | **313 faits / 145 sources / 20 sections** |
| `source_url` | 313 / 313 |
| Répartition | official 60, press_confirmed 183, community 39, post_launch_pending 19, speculative 5, leak_unverified 7 |
| Structure de chapitres | `s4_chapter_structure` — 5 chapitres, **93 missions** |
| Missions de presse conservées | 93 (`s2_press_mission_list`) |

## 3. Structure narrative retenue

| Chapitre | Titre | Missions |
|---|---|---|
| 1 | Just Like Paradise | 22 |
| 2 | Paradise Lost | 13 |
| 3 | Tits Ass Drug Money | 26 |
| 4 | Vice City, Baby | 25 |
| 5 | Top of the World, Ma | 7 |
| **Total** |  | **93** |

Statut : `press_confirmed`. Aucune liste officielle de missions n'a été publiée
par Rockstar. Les listes à **91** missions omettaient deux entrées du chapitre 2
(*Thrillbillies*, *Twist Wrist, Smash, Grab*).

## 4. Sources de référence

- <https://www.talkesport.com/gta-6/all-gta-6-chapters-missions-list/> — décompte 93, titres de chapitres, mentions masquées.
- <https://press-start.com.au/news/2026/11/18/heres-how-many-story-missions-are-in-grand-theft-auto-6/> — liste complète, ~50 h de campagne.
- <https://www.gamespot.com/articles/how-long-to-beat-gta-6/> — 65 h / 90–100 h / 200 h+, ordre souple.
- <https://www.talkesport.com/gta-6/gta-6-replay-missions-manual-save/> — pas de replay, 15 sauvegardes manuelles.
- <https://www.rockstargames.com/VI/only-in-leonida/jason> et `/lucia` — biographies officielles, répliques, Cal Hampton.
- <https://www.gadgets360.com/games/features/gta-6-characters-guide-grand-theft-auto-vi-jason-duval-lucia-caminos-brian-heder-cal-hampton-boobie-ike-more-9826820> — bascule des protagonistes.
- <https://www.gamerbolt.com/gta-6-lucia-caminos/> — contexte Lucia, distribution rapportée.
- <https://gta6gang.com/pages/gta6-jason.html> — hypothèses capacités (marquées `speculative`).
- <https://beebom.com/gta-6-missions-list-walkthrough/> — liste à 91, conservée comme trace de divergence.

## 5. Arbitrages

1. **93 vs 91 missions** → 93 retenu, la différence s'explique par deux missions du chapitre 2.
2. **Fins multiples** → hypothèse communautaire (`speculative`), jamais présentée comme un fait.
3. **Capacités spéciales** → décrites par des guides, non confirmées par Rockstar : `speculative`.
4. **Distribution** → noms de comédiens rapportés : `community`.
5. **Codes de coffre** → l'arbitrage S3 est conservé : aléatoires côté GameSpot, aucune liste universelle.
6. **Durées** → trois mesures concurrentes citées séparément, jamais fusionnées.

## 6. Médias du groupe G1

10 JPG inédits, photoréalistes / cinématographiques, `assets/images/story/*.jpg`,
JPEG q95 progressif (9 × 1920×1080, 1 portrait recadré), voir
`assets/images/CREDITS.md` (IMG021 → IMG030). Aucun PNG, SVG, WebP, AVIF, WAV,
ZIP ni PDF produit. Aucun MP3 consommé pour G1 (quota audio réservé aux groupes
qui en ont besoin).

## 7. Contrôles exécutés

- `node --check` sur les 5 modules JS.
- `node tools/check_links.js` → 5 fichiers HTML, 231 références, **0 cassé**.
- `python3 tools/check_s3.py` → CP3 toujours vert (seuils S3 désormais `>=`).
- `python3 tools/check_s4.py` → CP4 partiel, groupe G1.

**Gate :** `CONTINUER` → groupe G2 (P04 Lucia, P05 secondaires, P05b hub personnages).


---

## G2 — Personnages (clôturé)

Voir `tools/patch_research_s4_g2.py` (+16 faits, +8 sources) et les 3 pages
`pages/personnages/{index,lucia,secondaires}.html`. Hub corrigé après QA :
nœud `Article` ajouté au `@graph` JSON-LD, `SpoilerToggle` ajouté sur les
théories non vérifiées.

**Gate :** `CONTINUER` → groupe G3.

---

## G3 — Carte / Armes / Véhicules

**Pages :** `pages/carte/vice-city.html`, `pages/armes/index.html`, `pages/vehicules/index.html`.
**Faits :** `VCX-01…08` (8), `ARS-01…10` (10), `CAR-01…10` (10) → +27 faits, +12 sources
appliqués par `tools/patch_research_s4_g3.py` (idempotent, 367 faits / 165 sources).

### Recherche et arbitrages

| Sujet | Source | Statut retenu |
|---|---|---|
| 6 quartiers nommés (Peacock Bay, Southside, Tequesta, Tisha-Wocka, Stockyard, Ocean Beach) | panneaux des trailers, captures officielles, copie promo | `official` |
| Waning Sands, comté de Leonard, ville séparée | Trailer 1 | `official` |
| Little Havana, Little Haiti/La Perle, Viceport, Vice Point, Rockridge, Starfish Island | fuites 2022, wikis | `community` (section verrouillée + spoiler) |
| Portage 2 armes longues + 2 armes de poing, coffre-arsenal, arme visible, bouclier humain, combat sous-marin | presse + guides | `press_confirmed` |
| Familles et noms d'armes | listes communautaires agrégées | `press_confirmed` pour les familles, `community` pour la liste complète (spoiler) |
| Équipement (brouilleur, cloneur, attaches, sac de fouille…) | presse | `press_confirmed` |
| 3 paliers de vol, WAINK, traceur, Pay 'n' Spray, garage, RydeMe, Scooter Bros, bus/trains | presse | `press_confirmed` |
| Ultimate Edition (Deviant, Mamba GT, Riata, Kamacho, coupé Sirius) | presse | `press_confirmed` |
| « 300 véhicules », vitesses max, classements de dégâts | rumeurs | **non repris** (aucun chiffre) |

### Média

9 JPG (voir `assets/images/CREDITS.md`, lot G3). Génération plafonnée à 10 images
par réponse : la dixième (`weapons_sniper_rooftop_01.jpg`) a échoué puis le quota a
bloqué la relance. Aucune page ne référence ce fichier.

### QA

- 3 pages : breadcrumb, meta SEO + OG/Twitter, JSON-LD `Article` + `BreadcrumbList`,
  alt descriptifs, badges de statut sur chaque section.
- Navigation alignée sur 7 entrées + Stratégies + EN dans les 9 pages de contenu et `en/index.html`.
- `node tools/check_links.js` → 11 fichiers HTML, 502 références, **0 cassé**.
- `optimize_images_s4.py --g3-only` → 9 JPG en 1920×1080, total S4 6 010 Ko.
- `check_s4.py` étendu au groupe G3.

**Gate :** `CONTINUER` → groupe G4.


---

## G4 — Police / Économie / Activités

**Pages :** `pages/police/index.html`, `pages/economie/index.html`, `pages/activites/index.html`.
**Faits :** +31 faits (POL-16…24, ECO-14…24, ACT-12…22) et +17 sources via
`tools/patch_research_s4_g4.py` (marqueur `S4_G4_VERIFIED_FACTS_V2`, idempotent,
renumérotation automatique des identifiants libres par section).
**Totaux :** **398 faits / 20 sections / 182 sources**, `source_url` 398/398.

### Arbitrages

| Sujet | Décision |
|---|---|
| Six étoiles, crime signalé par témoin ou alarme, quatre identifiants | `official` (Rob Nelson, Extended Look 28/08/2026) |
| Couleurs d'étoiles, escalade K-9 / SWAT / militaire, caméras-piétons | `press_confirmed` |
| Six identifiants effaçables (dont vidéosurveillance et équipier) | `press_confirmed` ; « changer de tenue » nuancé : n'efface pas une étoile active à lui seul |
| Trois formes d'argent, dépôt au distributeur uniquement, receleurs spécialisés, coffre vitesse/rendement | `press_confirmed` + `official` pour les formes d'argent |
| Agences et véhicules de police nommés | `community` (aucun guide Rockstar) |
| Entreprises, revenus passifs, braquages à plusieurs millions | **non repris** : `post_launch_pending` / `speculative`, derrière SpoilerToggle |
| Pêche, chasse, mini-golf, MMA, gym, kayak, plongée, courses | `official` pour pêche/chasse, `press_confirmed` sinon ; tennis/zoo/parachute en `community` |

### QA

- 12 pages de contenu, 14 fichiers HTML, **667 références internes, 0 cassée**.
- `check_s4.py` étendu au groupe G4 (10 JPG police/economie/activites).
- `optimize_images_s4.py --g4-only` → 10 JPG 1920×1080, total S4 6 223 Ko.
- Nouveau composant CSS `.s4-steps` (liste d'étapes numérotées) dans `s4_pages.css`.

**Gate :** `CONTINUER` → groupe G5.


---

## G5 — Musique / Online / Codes

**Pages :** `pages/musique/index.html`, `pages/online/index.html`, `pages/codes/index.html`.
**Faits :** +30 faits (MUS-10…24, ONL-12…17, CHE-14…19) et +15 sources via
`tools/patch_research_s4_g5.py` (marqueur `S4_G5_VERIFIED_FACTS`, renumérotation
automatique). **Totaux :** **428 faits / 20 sections / 197 sources**, `source_url` 428/428.

### Arbitrages

| Sujet | Décision |
|---|---|
| Six stations (Flash FM, Cocoteo FM, Back Country Radio, AfroBank FM, The Chamber 106.6, Dirty South Classics), 18 titres | `official` — annonce Rockstar du 08/10/2026 |
| Album 34 titres (19/11) et score Justice 30 pistes (11/12) | `official` |
| Radio à pied au casque + podcasts à la demande | `official` |
| Noms de stations issus de fuites (Kaleidoscope, Emotion 98.3, V-Rock…) | `community`, derrière SpoilerToggle |
| Solo au lancement, GTA Online maintenu, GTA+ offert | `official` |
| Multijoueur 2027 / fenêtre décembre 2026 | `community` — rumeurs nommées avec leur auteur |
| Transfert de progression, cross-play, modèle économique | `post_launch_pending` |
| **Codes de triche** | **aucun code publié** : 0 officiel. Les listes circulantes sont identifiées comme des codes GTA V recyclés, en `speculative`, et reproduites uniquement pour démonter la confusion |

### QA

- 15 pages de contenu, 17 fichiers HTML, **830 références internes, 0 cassée**.
- `check_s4.py` étendu au groupe G5 (10 JPG musique/online/codes).
- `optimize_images_s4.py --g5-only` → 10 JPG 1920×1080, total du lot 5 611 Ko.

**Gate :** `CONTINUER` → groupe G6.


---

## G6 — Trophées / Secrets / Tips

**Pages :** `pages/trophees/index.html`, `pages/secrets/index.html`, `pages/tips/index.html`.
**Faits :** +37 faits (TRO-17…28, SEC-09…21, TIP-38…49) et +13 sources via
`tools/patch_research_s4_g6.py` (marqueur `S4_G6_VERIFIED_FACTS`).
**Totaux :** **465 faits / 20 sections / 210 sources**, `source_url` 465/465.

### Arbitrages

| Sujet | Décision |
|---|---|
| 55 trophées, 28 cachés / 27 visibles, platine « Vice Got a Price! » | `press_confirmed` (listes publiées le 18/11) |
| Six trophées de chapitre + six de mission nommée | `press_confirmed`, noms de chapitres censurés quand les trackers les censurent |
| Checklist 100 % ≈ 60 % du vrai contenu, rien de manquable | `press_confirmed` |
| Seul point manquable : méditation du chapitre 1 | `press_confirmed` |
| Easter eggs relevés dans trailers / cover / Extended Look | `press_confirmed`, avec date et support |
| Coordonnées « OVNI 3 h du matin », « chambre au chainsaw », « Skunk Ape », « manoir Vercetti » | `community`, listées comme non sourcées, théorie derrière SpoilerToggle |
| Tips (Focus détecteur, lunette, silencieux, menu véhicule, natation, carte bleu foncé) | `press_confirmed` |
| Astuces d'ordre de jeu | `community` |

### QA

- 18 pages de contenu, 20 fichiers HTML, **1030 références internes, 0 cassée**.
- `check_s4.py` étendu au groupe G6 (10 JPG trophees/secrets/tips).
- `optimize_images_s4.py --g6-only` → 10 JPG 1920×1080, total du lot 6 204 Ko.

**Gate :** `CONTINUER` → groupe G7.

## Lot G7 — Outils & communauté / Divers / FAQ (dernier groupe, S4 complet)

**Pages :** `pages/outils/index.html`, `pages/divers/index.html`, `pages/faq/index.html`.
**Faits :** +24 faits (OUT-14…21, DIV-06…10, FAQ-01…11) et +15 sources via
`tools/patch_research_s4_g7.py` (marqueur `S4_G7_VERIFIED_FACTS`).
**Totaux :** **489 faits / 20 sections / 225 sources**, `source_url` 489/489.

### Arbitrages

| Sujet | Décision |
|---|---|
| SIXSTAR, rookdex, gta6-companion, Wanted, Companion & Countdown | `community` — aucun n'est officiel, mention explicite en tête de page |
| Chiffres d'abonnés YouTube et répartition par usage | `community` (relevés d'annuaires, datés) |
| Consensus r/GTA6 sur les créateurs et rejet de la « slop » | `community` |
| 1440p interne, ray tracing GI/reflets/ombres, cheveux simulés, HDR > 1 500 nits | `press_confirmed` (Digital Foundry, 18/11) |
| 30 fps partout, pas de mode 60/40, PS5 Pro quasi constant | `official` (Newswire 10/11) + `press_confirmed` (mesures) |
| Chutes à 23 fps (PS5) / 24 fps (Pro) | `press_confirmed`, présentées comme mesures et non comme défauts |
| 79,99 $ / 99,99 $, 212 Go, code en boîte sans disque, pas de PC | `official` |
| Résolution Series S, calendrier PC, mode 60 fps ultérieur, multijoueur | jamais chiffrés : listés en « ce qu'on ignore » (`post_launch_pending`) |

### QA

- 20 pages de contenu (21 fichiers HTML avec `synopsis.html`), **1245 références internes, 0 cassée**.
- `check_s4.py` étendu au groupe G7 (10 JPG outils/divers/faq) et à l'assertion 20 pages.
- `optimize_images_s4.py --g7-only` → 10 JPG 1920×1080, total du lot 5 048 Ko.
- Nav +4 entrées (Outils / Divers / FAQ + alignement) sur 21 sous-pages + accueil + `en/index.html`,
  `sitemap.xml` +3, `search.js` +10 entrées.

**Gate :** S4 complet (20 pages) → `CONTINUER` puis S5.

## S5 — INTERACTIVE_FEATURES (carte, collectibles, quiz)

**Pages :** `pages/carte/index.html`, `pages/collectibles/index.html`, `pages/quiz/index.html`.
**Faits :** +18 faits (MAP-16…22, TRO-29…33, OUT-22…23, QIZ-01…04) et +15 sources
via `tools/patch_research_s5.py` (marqueur `S5_VERIFIED_FACTS`).
**Totaux :** **507 faits / 20 sections / 240 sources**, `source_url` 507/507.

### Ce qui a été construit

| Livrable | Détail |
|---|---|
| Carte interactive | `assets/js/map_leonida.js` — schéma SVG maison, 28 lieux, filtres région/type, recherche instantanée, sélection accessible au clavier. Zéro dépendance, zéro réseau. |
| Checklist 100 % | `assets/js/s5_checklist.js` — 16 jalons, filtres par catégorie, barre de progression ARIA, persistance `localStorage`, remise à zéro. |
| Quiz | `assets/js/s5_quiz.js` — 30 questions, 3 niveaux, chronomètre 20 s, score, verdict, rejouer. Chaque correction cite sa référence de fait. |
| Styles | `assets/css/s5_interactive.css` — états `:focus-visible`, `prefers-reduced-motion`, dégradation sans JS. |

### Arbitrages

| Sujet | Décision |
|---|---|
| Carte officielle | **imprimable**, gratuité le 19/11, poster 0,99 $ ensuite — jamais « carte interactive officielle » (`press_confirmed`) |
| Positions des 28 lieux | placements éditoriaux sur schéma, explicitement non officiels (`community`) |
| Base cartographique YANIS / gtadb.org / CC BY 4.0 | `community`, avec attribution |
| 80 challenges, seuils 50 / 70 | `press_confirmed` (PowerPyx, 18/11) |
| 18 séries / 480 cartes, seuils 3 / 15 | `press_confirmed` |
| ≈ 3 000 entrées de progression | `press_confirmed` |
| Quiz : aucune question sur missions/fins/personnages non confirmés | refus explicite, remplacé par calendrier, distribution, géographie, technique |

### QA

- 24 pages contrôlées, **1407 références internes, 0 cassée**, 99 JPG, 12 MP3, 0 format interdit.
- `tools/check_s4.py --group S5` : SEO, breadcrumb, badges, images, liens → ✓.
- Test fonctionnel des trois widgets sous jsdom : 28 pins / 4 après filtre Keys / 1 après recherche « marina » ;
  checklist 2/16 + persistance + filtre + reset ; quiz 30 questions jusqu'au verdict, mode Difficile = 10 questions.

**Gate :** `CONTINUER` → S6 QA_AND_POLISH.

## S6 — QA_AND_POLISH

**Livrables :** `tools/audit_s6.py`, `tools/build_s6.py`, `qa_report_s6.json`,
`pages/qa/index.html`, `assets/images/qa/*.jpg` (5 JPG), `dist/` (build de production).
**Faits :** +6 faits (QA-01…04, REL-19…21) et +6 sources via `tools/patch_research_s6.py`.
**Totaux :** **513 faits / 21 sections / 246 sources**, `source_url` 513/513.

### Résultat de l'audit (reproductible)

| Contrôle | Résultat |
|---|---|
| Pages auditées | 27 (index, en, 25 sous-pages) |
| Erreurs bloquantes | 0 |
| Avertissements | 0 |
| Contrastes calculés | 8 paires, toutes au-dessus du seuil |
| Images | 104 JPG, max 1 021 Ko → ramené sous 900 Ko, total ≈ 63 Mo |
| Liens internes | 1 561 références, 0 cassée |
| Sitemap | 33 URLs, toutes existantes |
| Formats interdits | 0 (y compris dans `dist/`) |
| Core Web Vitals | seuils 2026 cités : LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 |

### Corrections appliquées pendant l'audit

- `en/index.html` : image de hero sans `fetchpriority` → ajouté (LCP).
- `map_regions_terrain_relief_01.jpg` (938 Ko) et `secrets_wall_mural_street_01.jpg` (1 021 Ko)
  recompressés en q88 → 545 Ko et 565 Ko, sans changement de dimensions.
- WCAG 2.2 : `scroll-margin-top` de 96 px sur les ancres (2.4.11), contour de focus 3 px (2.4.13),
  cibles ≥ 32 px (2.5.8), `outline` rétabli sur les points de carte.
- `robots.txt` : `Disallow: /dist/` ; build minifié généré et vérifié (8/8 modules valides).

**Gate :** `CONTINUER` → S7 FINAL_DELIVERY.

## S7 — FINAL_DELIVERY

**Livrables :** `README.md` (réécrit, 8 sections), `pages/final/index.html`,
`assets/images/final/*.jpg` (5 JPG), inventaire complet dans `CREDITS.md`.
**Recherche :** aucun fait ajouté — la livraison ne produit pas de donnée nouvelle ;
le corpus reste à **513 faits / 21 sections / 246 sources**.

### Contenu du récapitulatif

| Section | Contenu |
|---|---|
| Le guide en chiffres | 28 HTML, 513 faits, 109 JPG, recomptés sur le disque |
| Les huit états | traçabilité S0 → S7 avec livrables clés |
| Structure | arborescence réelle, rôle de chaque dossier |
| Les 25 sous-pages | index complet cliquable |
| Publier | local, GitHub Pages, Netlify/Vercel, sans build |
| Ce qu'il ne fait pas | cinq refus assumés + trois mises à jour post-lancement derrière SpoilerToggle |

### QA finale

- 28 fichiers HTML, **1670 références internes, 0 cassée**.
- `check_s2` ✓ `check_s3` ✓ `check_s4` ✓ (26 pages de contenu contrôlées) `audit_s6` ✓ (28 pages, 0 erreur).
- `node --check` sur les 8 modules JS ; 0 format interdit ; sitemap 34 URLs toutes existantes.
- Correction trouvée à la livraison : 25 liens de l'index du récapitulatif étaient relatifs
  à la racine alors que la page est en `pages/final/` — réécrits en `../`, puis `localhost`
  retiré du texte d'aide au déploiement (règle « 0 localhost » du projet).

**Gate : FIN — projet livré.**

## S8 — REVIEWS (événement : levée d'embargo du 18/11 à 11:00 UTC)

**Page :** `pages/reviews/index.html`. **Faits :** +14 (REV-17…25, REL-22…26) et +7 sources
via `tools/patch_research_s8.py`. **Totaux : 527 faits / 21 sections / 253 sources.**

### Le basculement

L'embargo presse a été levé le mercredi 18 novembre à 11:00 UTC, la veille du lancement,
au moment où le jeu s'ouvrait en Nouvelle-Zélande. Le corpus change de nature : les
agrégats passent de `post_launch_pending` à `press_confirmed`, avec leur horodatage.

| Élément | Valeur relevée le 18/11 |
|---|---|
| Metacritic PS5 | **99** sur 109 critiques (~80 parfaites, aucune sous 90) |
| Metacritic Xbox | 99, sur beaucoup moins de tests |
| OpenCritic | **98–99** selon l'heure, **100 % de recommandations** |
| Record | égale Ocarina of Time (99 depuis 1998, sur 22 critiques) |
| Meilleur score Rockstar | oui — devant GTA IV (98), GTA V (97), RDR2 (97) |
| Note la plus basse de la vague | 9/10 (TheSixthAxis) |
| Reproche récurrent | le plafond à 30 fps et les chutes en zone dense |

### Corrections éditoriales déclenchées par cette actualité

- `pages/final/index.html` et `pages/quiz/index.html` affirmaient qu'« personne n'y a joué ».
  Faux depuis le 18/11 : la presse accréditée y a joué **et** publié. Reformulé partout.
- Accueil : la section Reviews ne parle plus d'un horaire « reconstruit » (l'heure
  d'embargo est désormais observée et concordante) et pointe vers la nouvelle page.
- La page Reviews garde la règle maison : chaque note porte son agrégateur et son horodatage,
  aucun score n'est moyenné avec un autre.

### QA

- 29 fichiers HTML, **1757 références internes, 0 cassée**.
- `check_s4.py` étendu : groupe S8, 27 pages de contenu contrôlées, 5 JPG reviews (114 au total).
- 5 nouvelles illustrations JPG 1920×1080 (IMG110–IMG114).

**Note :** ce lot ne clôt pas le workflow — il documente un événement majeur à J-1.
Gate maintenu : `FIN`.

---

## Amendement S9 — la nuit de lancement et la technique mesurée (18/11/2026, 13:00 UTC)

Recherche menée pendant que le jeu était déjà ouvert en Nouvelle-Zélande. Trois sujets :
la première nuit côté joueurs, les incidents de préchargement, et les mesures Digital Foundry
sur **versions commerciales** — c'est-à-dire sur les disques et les téléchargements que vous avez,
pas sur les copies de preview.

`S9_LAUNCH_NIGHT_VERIFIED` · +13 faits (`REV-27…31`, `REL-24…27`, `TIP-48…52`), +8 sources.

### Ce que dit la technique, chiffre par chiffre

| Machine | Résolution interne | Cadence | Pire cas observé |
|---|---|---|---|
| PS5 | 1440p | 30 fps (33 ms) | 23 fps, explosions lourdes |
| PS5 Pro | 1440p + PSSR | 30 fps quasi constant | 24 fps ponctuels ; ombres RT exclusives |
| Xbox Series X | ~1440p | 30 fps, VRR 120 Hz | ~20–21 fps en fusillade dense |
| Xbox Series S | ~720p | souvent sous 30 fps | pop-in marqué, reflets dégradés |

- Latence mesurée : **~180 ms**, cohérente avec les autres titres Rockstar à 30 fps.
- Surprise positive : les **cinématiques ne saccadent plus** (correctif moteur RAGE).
- Ray tracing : illumination globale et reflets sur les deux Xbox, **ombres RT réservées à la PS5 Pro**.
- Toujours **aucun mode 60 fps** : le coût CPU par image ne le permet pas sans sacrifier le monde.
- Ces chiffres sont **datés du 18/11** et portent sur les versions 1.002.000/1.002.001 ; les patchs
  de lancement peuvent les déplacer. La page les présente donc avec leur horodatage, pas comme
  une vérité définitive.

### Nuit de lancement : le calendrier réel

| Repère | Heure |
|---|---|
| Nouvelle-Zélande (déjà jouable) | 18/11 · **11:00 UTC** |
| France métropolitaine | 19/11 · **00:00 CET** |
| Côte est des États-Unis (PS5) | 19/11 · **05:00 UTC** |
| Notes utilisateurs Metacritic | **+36 h** après le lancement, soit le 20/11 au plus tôt |
| Fenêtre de spoiler | **~12 h** entre la NZ et votre minuit |

### Communauté : ce qui marche, ce qui casse

- **Astuce néo-zélandaise** : sur Xbox, changer la région de la console suffit (votre version
  continue de fonctionner ; le store NZ peut proposer une installation séparée). Sur PS5, il faut
  un **compte PSN néo-zélandais et un achat sur ce store** — donc payer deux fois.
- **Bug de préchargement Xbox** : l'écran affiche ~200 Go, puis l'installation se termine sur
  ~300 Mo. Supprimer et relancer corrige dans la majorité des cas rapportés ; changer la région
  *avant* d'installer évite le problème.
- **Suspensions de comptes PSN** : rumeurs non confirmées, aucune déclaration de Sony ni de
  Rockstar. Classées `community`, jamais présentées comme un fait.
- **Première heure** : les conseils convergent — régler image/HDR d'abord, marcher avant de rouler,
  rouler sans destination ensuite, trois ou quatre missions, puis seulement explorer. Le seul
  conseil unanime est négatif : ne pas traverser la carte d'emblée.
- **Anti-spoiler** : couper les mots-masqués et les recommandations, éviter les titres YouTube.
  C'est comportemental, pas technique.

### Décisions éditoriales

- Nouvelle page `pages/lancement/index.html` (« Nuit de lancement »), pensée pour être lue
  **avant** de jouer : aucun spoiler narratif, un seul bloc masqué par SpoilerToggle.
- Les scores utilisateurs ne sont **pas** affichés : ils n'existent pas encore (règle des 36 h).
- Les chutes de cadence sont présentées comme des **pires cas ponctuels**, pas comme une moyenne.
- Aucune fourchette de prix, aucune spéculation sur un futur patch 60 fps.

### QA

- 30 fichiers HTML, **119 JPG**, 12 MP3, **~1 800 références internes, 0 cassée**.
- `check_s4.py` étendu : groupe S9, **28 pages** de contenu, 5 JPG `lancement_*`.
- 5 nouvelles illustrations JPG 1920×1080 (IMG115–IMG119).

**Note :** ce lot documente une nuit en cours. Gate maintenu : `FIN`.


---

## Amendement S10 — objets réels, cartes réelles, images uniques (18/11/2026)

Trois corrections demandées après la mise en ligne du lot S9. Elles touchent l'intégrité
visuelle du site plus que son contenu éditorial.

### 1. Une image = un seul emplacement

Règle appliquée : **aucune image ne peut apparaître deux fois** sur le site. Les 44 occurrences
en doublon ont été traitées de trois façons :

- **héros de page** convertis en `background-image` CSS (un héros n'est plus un `<img>`, il est
  un fond) — 28 pages concernées ;
- **doublons de contenu** supprimés quand la page gardait assez de visuels ;
- **remplacements** avec des illustrations générées nouvelles quand la page avait besoin d'un
  second visuel (10 JPG 1920×1080 en S10).

Contrôle automatique ajouté : `tools/check_images_unique.py`, qui compte les `<img>` **et** les
arrière-plans CSS et sort en erreur au premier doublon. État actuel : **362 références, 362
images distinctes, 0 doublon**.

### 2. Les vraies cartes

La page Carte ne reposait que sur un schéma SVG éditorial. Elle publie désormais **trois cartes
réelles** de Leonida : le poster officiel (géographie exacte, six régions), une version
quadrillée pour nommer un secteur, et la reconstruction communautaire **YANIS v10** (CC BY 4.0).
Quatre cartes interactives de référence sont liées et datées (gta-6-map.com, sixintelhq,
mapgta6.org, mapheist). Rappel conservé partout : **Rockstar ne propose pas de carte
interactive** ; le poster du 19/11 est un document imprimable.

### 3. Les vraies images des objets

Deux catalogues visuels complets ont été ajoutés, avec un visuel par objet :

| Catalogue | Volume | Source | Page |
|---|---|---|---|
| Armes et équipements | **51 pièces** (8 familles) | fiches GTABase GTA VI | `pages/armes/index.html#v-title` |
| Véhicules | **152 modèles** (12 classes) | fiches GTABase GTA VI | `pages/vehicules/index.html#catalogue` |
| Faune de Leonida | **27 espèces** (5 groupes) | fiches GTABase GTA VI | `pages/collectibles/index.html#faune` |

Chaque fiche porte le nom en jeu, la classe et — pour les armes — le modèle réel d'inspiration
(Beretta 92FS, Glock 17, MP5, M249, RPG-7…). Aucune performance, aucun prix, aucune vitesse
n'est inventé : ces chiffres n'existent pas officiellement.

### Décisions éditoriales

- Les visuels d'objets **ne sont pas générés par IA** : ils proviennent des fiches communautaires
  du jeu et sont crédités dans `assets/images/CREDITS.md`, avec leur statut (communauté, presse,
  officiel).
- Les vignettes d'espèces sont en 320 px : c'est la résolution publiée par la base. Un visuel
  fidèle en petit format vaut mieux qu'une illustration inventée — la limite est écrite sur la page.
- La carte postale officielle est créditée comme document Rockstar, jamais comme capture maison.

### QA

- `check_s4.py` étendu : les catalogues d'objets échappent à la règle 1920×1080 mais gardent
  les contrôles d'alt, de ratio et de chargement paresseux ; comptage des visuels = `<img>` + héros CSS.
- `check_images_unique.py` : nouvelle porte bloquante.
- 0 lien interne cassé, 0 format interdit, audit 30 pages inchangé.

**Note :** lot de correction, pas d'extension du périmètre rédactionnel. Gate maintenu : `FIN`.


---

## Amendement S11 — après l'ouverture : radio réelle et biens confirmés (18/11/2026)

Recherche menée sur les relevés d'écoute des premières heures (Nouvelle-Zélande) et sur les
présentations presse d'août 2026 concernant la propriété.

### La radio est bien plus grande que six stations

Rockstar n'a **nommé** que six stations le 8 octobre : Cocoteo FM, Back Country Radio, AfroBank
FM, The Chamber 106.6, Flash FM, Dirty South Classics. À l'écoute, les joueurs en relèvent **plus
d'une vingtaine** : V-Rock, Vice City FM, Emotion 98.3, Leonida Jazz Radio, Gloriana Blues Radio,
Honey FM, Symphony FM, Radio On-U, Radio La Ola, Kaleidoscope FM, Worldwide FM, Stockyard FM,
CircoLoco Records Radio, VCRR, The Wipe, WKTT.

Décision éditoriale : ces stations sont **entendues**, pas **annoncées**. Elles entrent au corpus
en `community`, dans un tableau séparé, avec un avertissement explicite. Aucun total n'est avancé.
Deux points d'usage vérifiés : la radio s'écoute **à pied** (téléphone + écouteurs) et des
**podcasts à la demande** existent — deux premières dans la série.

### Propriété : les garages, et rien d'autre

La rumeur parle de commerces à racheter et de revenus passifs. Rien de tel n'est confirmé.

| Élément | Statut réel |
|---|---|
| Garages personnels achetables (Shore Court, Paradise Garage) | confirmé (presse, août 2026) |
| Stockage de départ : 3 véhicules | confirmé (presse) |
| Planques achetables | **non** — débloquées par l'histoire |
| Commerces, revenus, prix | **non confirmés** |

Quatre visuels de lieux issus des captures officielles relayées par GTABase sont désormais
publiés dans la section « Les lieux qu'on peut vraiment posséder » de la page Secrets : Leonida
Keys Safehouse, Starlet Motel, Paradise Garage, Shore Court Garage.

### QA

- `research_data.json` : **544 faits / 264 sources**, `source_url` sur 100 % ; bloc `s11_amendment`.
- 10 nouvelles illustrations IA 1920×1080, toutes placées une seule fois.
- `check_images_unique.py` reste vert : **370 images, 370 emplacements**.
- 0 lien cassé, audit 30 pages inchangé.

**Note :** lot d'enrichissement post-ouverture. Gate maintenu : `FIN`.


---

## Amendement S12 — passe de publication (18/11/2026)

Objectif : rendre le site publiable le jour de l'ouverture, sans information manquante sur les
48 dernières heures.

### Corrections techniques (18/11)

| Sujet | Contenu retenu | Statut |
|---|---|---|
| Mises à jour avant lancement | 1.002 (13/11, ≈1 Go PS5 / ≈2,2 Go Xbox) puis 01.002.001 (16/11, ≈602 Mo / ≈1,6 Go) ; aucune note publiée par Rockstar | presse |
| PS5 | firmware système 26.07-14.23.00 (≈1,2 Go) **obligatoire** pour lancer le jeu | presse |
| Ouverture | minuit local par fuseau ; Nouvelle-Zélande 11:00 UTC le 18 ; France minuit dans la nuit du 18 au 19 | presse |
| Préchargement | ouvert le 10/11 (annonce du 3/11), jusqu'à 212 Go | officiel |
| Performance | 30 fps partout, pas de mode 60 ; 1440p reconstruit ; PS5 Pro quasi verrouillée, PS5 jusqu'à 23 fps, Series X ~20 fps, Series S sous 30 fps | Digital Foundry |

### Corrections de fond

- **Argent liquide** : solde bancaire / espèces portées / butin en sac. Les espèces sont perdues en cas de mort ou d'arrestation (Rob Nelson). L'argent est aussi une condition de progression.
- **Identification** : caméras, témoins, plaques ; le masque empêche l'identification, pas l'alerte.
- **Solo à l'ouverture** : aucun mode en ligne, aucun co-op, aucun abonnement ; GTA Online (GTA V) continue.
- **Discographie** : *The Album* 34 titres (Atlantic), album de score 30 titres + bonus le 11/12/2026.

### Nouvelles sections publiées

`#verifications` (lancement), `#technique` (reviews), `#cash-sur-soi` (économie), `#identifier`
(police), `#lecture-carte` (carte), `#platine` (trophées), `#solo-ferme` (online), `#fiabilite`
(FAQ), `#album-suite` (musique), `#chronologie` (histoire).

### QA de publication

- 38 références d'images cassées (`assets/images/<cat>/<cat>/…`) corrigées : **0 référence manquante**.
- Entrée de nav dupliquée retirée (lancement), `id` dupliqué corrigé (missions), ancre de sommaire orpheline supprimée.
- `sitemap.xml` reconstruit : **34 URLs relatives**, sans nom d'hôte inventé.
- 10 nouvelles illustrations IA 1920×1080, une occurrence chacune.
- `research_data.json` : **554 faits / 270 sources** ; bloc `s12_amendment`.
- Batterie verte : CP2, CP3, CP4, audit 30 pages 0/0, 0 lien cassé, 0 image dupliquée, 8/8 JS valides.


---

## Amendement S13 — publication finale (18/11/2026, 22 h 40)

Dernière passe avant livraison. Objectif : qu'un visiteur arrivant le soir de l'ouverture trouve
une page d'actualité à jour, et qu'un lien mort ne renvoie jamais une erreur brute.

### Nouveautés

- **31ᵉ page : `pages/news/index.html` — « Le fil du lancement »**, liée depuis toutes les navigations
  (31 pages + `404.html`), depuis le bandeau de l'accueil, le sitemap et le moteur de recherche.
  Contenu : état du jour en six lignes, vérifications avant lancement, argent de la première heure
  (confirmé vs rapporté), performance mesurée, stations relevées, et un tableau « ce qui est faux »
  (codes de triche, revenus de commerces, date PC).
- **`404.html`** réelle, avec 200 status servi par GitHub Pages et redirections 404 déclarées pour
  Netlify (`[[redirects]]`) et Vercel (`routes`). La 404 propose six entrées utiles et la recherche.
- **10 nouvelles illustrations IA** 1920×1080, une occurrence chacune (total **394**).
- **Nouvelles boucles de revenus** documentées dans Tips (commerce, véhicules, repaires) avec
  séparation stricte entre ce qui est confirmé et ce qui est rapporté.
- **Plan de chasse aux trophées** (Trophées), refonte des pieds de page (mention légale corrigée et
  cohérente sur les 32 pages HTML), `state.json` et `workflow_master.yaml` en S13.

### Recherche du jour (sources ajoutées)

Vice City Hustle (guide argent du 14/09 et checklist du 20/10), AlcastHQ (18/11), U7Buy (18/11),
CULTR (relevé de stations). Les chiffres de paiement (10 000 $, 30 000 $, 205 000 $) et le faux code
« 250 000 $ » ont été explicitement écartés et signalés comme tels.

### QA finale

- `check_s4` : **29 pages de contenu** validées (les 2 pages racine et la 404 sont hors groupe).
- `audit_s6` : **32 pages, 0 erreur, 0 avertissement** — référencements, contrastes, poids, a11y.
- `check_links` : **2 159 références internes, 0 cassée** ; `check_images_unique` : **394 / 394**.
- 8/8 modules JS valides, `yaml.safe_load` OK, 0 PNG/SVG/WebP/AVIF dans l'arbre du site.


---

## Amendement S14 — mécaniques de fond (18/11/2026, 23 h 55)

Après la publication, la recherche a porté sur ce qui change vraiment une partie, plutôt que sur
l'actualité : structure de la campagne, système de preuves policières, braquage en duo, manquables.

### Cinq chapitres, aucune rejouabilité

GTA VI n'a **pas de menu de rejouabilité de mission**. Les guides de lancement (LFCarry, PowerPyx)
recommandent une sauvegarde manuelle au début et à la fin de chaque chapitre. Les quêtes marquées
manquables — deux courses de Shirley au chapitre 1, une course limitée dans le temps au chapitre 3 —
ne comptent ni pour les trophées ni pour la complétion. Nouvelle section `#chapitres-missions`.

### Six preuves, pas six étoiles

La police poursuit ce qu'elle peut prouver : **caméra, témoin, vêtements, visage, arme, véhicule**.
Chaque preuve s'annule d'une manière précise (masque, changement de tenue, véhicule banal, arme
rangée). Le **Focus Mode** met en évidence les agents à travers les murs, les icônes de
reconnaissance s'affichent en poursuite, et les voitures de valeur embarquent des traceurs GPS.
Nouvelle section `#six-preuves`, avec deux colonnes « ce qui marche / ce qui ne marche pas ».

### Braquage en duo

Sécurité moyenne ou élevée : duo obligatoire, un personnage tient la salle, l'autre vide caisse et
coffre. Les sacs se passent, et le personnage non contrôlé peut revendre le butin pendant la fuite.
Les billets marqués explosent sans neutralisateur (chapitre 3+). Silencieux = temps de butin
supplémentaire. La visée distingue tuer (tête/cœur) et blesser (articulations). Section `#duo-braquage`.

### Trophées réellement manquables

18 points de méditation sur 10 lieux, dont **un seul** dépend du chapitre 1 (maison de Jason).
La complétion est indulgente : la plupart des collectibles et quêtes annexes ne sont pas exigés et
tout reste faisable après l'histoire. Section `#manquables-reels`.

### QA

`check_s4` ✓ (29 pages de contenu) · `audit_s6` ✓ (32 pages, 0/0) · `check_links` ✓ (0 cassé) ·
`check_images_unique` ✓ (**403 / 403**) · 563 faits / 277 sources · 9 illustrations IA S14.


---

## Amendement S15 — retours de joueurs du premier jour (19/11/2026, 0 h 20)

Douze heures après l'ouverture néo-zélandaise, les retours de joueurs sont exploitables. Ils
nuancent sensiblement les tests de presse sur trois points.

### Ce que les joueurs disent (et que les tests disent moins)

| Sujet | Retour dominant | Section publiée |
|---|---|---|
| 30 fps | Peu gênant à la manette, visible en action dense | `reviews#joueurs` |
| Rythme | Premier chapitre très lent, proche d'une simulation de vie | `reviews#joueurs` |
| Conduite | Plus lourde, plus réaliste ; nette amélioration avec un bon véhicule | `vehicules#toucher` |
| Dialogues | Mixage parfois trop bas, sous-titres indispensables | `divers#confort` |
| Image | Bloom et profondeur de champ peu réglables selon la version | `divers#confort` |
| Lancement | Téléchargements longs, cas isolés de plantages après changement de région | `lancement#jour-un` |

### Deux apports de mécanique

- **Limite de port** : deux armes de poing dissimulées et deux armes longues visibles — le reste
  voyage dans le coffre. Nouvelle section dans Tips, avec deux visuels dédiés.
- **Meilleures armes par rôle** : Duke 556, Girardi ES9 / Klose K17, Hawk & Little Morgan,
  Moreland 850. Aucun prix confirmé ; l'achat le plus rentable reste le silencieux. Section
  `armes#trio`.

### QA

`check_s4` ✓ (29 pages) · `audit_s6` ✓ (32 pages, 0/0) · `check_links` ✓ · `check_images_unique` ✓
(**411 / 411**) · **568 faits / 282 sources** · 9 illustrations IA S15 · aucune image réutilisée.


---

## Amendement S16 — codes de coffres et dépannage (19/11/2026, 1 h 05)

Correction importante : la page Codes affirmait qu'aucun code n'existe. C'est vrai pour les **codes de
triche**, faux pour les **codes de coffres et de portes**.

### Cinq combinaisons publiées le 18/11

| Lieu | Code | Ouverture |
|---|---|---|
| Mission « Lab Fees » — porte | 0420 | Accès au local |
| Cagibi de Brian | 7700 | Local marqué en vert |
| Casa de Empeno | 1680 | Collier à tête de bison |
| Richardson Jewelry | 6815 | Bague de diamant |
| Donovan Banks & Co. | 0104 | Collier en améthyste (zéro initial significatif) |

Nuance publiée : les codes **de mission** sont fixes, les coffres de **monde libre** peuvent être
randomisés (garde fouillé, note proche, Focus Mode, ou ouverture à l'explosif). Nouvelle section
`codes#coffres`, avec deux visuels dédiés.

### Dépannage du soir de sortie

Nouvelle section `lancement#depannage` : cinq causes réelles (déblocage à minuit local, préchargement
bloqué, espace insuffisant jusqu'à 212 Go, précommande non honorée, code de boîte d'une autre région)
et un avertissement explicite sur les fausses listes de correctifs publiées avant la sortie.

### QA

`check_s4` ✓ (29 pages) · `audit_s6` ✓ (32 pages, 0/0) · `check_links` ✓ · `check_images_unique` ✓
(**421 / 421**) · **571 faits / 285 sources** · 10 illustrations IA S16, une occurrence chacune.


---

## Amendement S17 — finition de publication (19/11/2026, 2 h 05)

### Un vrai défaut de validité corrigé

Un contrôle de structure HTML sur les **32 pages** a révélé que `404.html` contenait une balise
`</head>` dupliquée (héritage de la génération du fichier). Corrigé. Contrôle désormais automatisable :
aucune page du site n'a d'erreur de nesting.

### Deux sections utiles ajoutées

- `lancement#minuit` : la séquence exacte avant 23 h 45 puis à minuit (espace, firmware, correctifs,
  sous-titres, sauvegarde manuelle) et le piège le plus courant : croire le jeu cassé parce qu'il ne
  se lance pas avant minuit local.
- `faq#stockage` : les trois chiffres réels (212 Go demandés par Rockstar, ~225 Go pour le paquet
  Xbox, ~213 Go constatés après correctifs) et le conseil de garder 10 à 15 Go de marge.

### Actualité du 13 au 18/11

Un patch d'environ **1,07 Go** a été déployé sur PS5 avant l'ouverture (textures, cadence, mémoire,
stabilité), en plus des correctifs 1.002 et 01.002.001, toujours sans notes officielles. La mise à
jour système PS5 est confirmée comme **obligatoire**, à installer avant minuit.

### QA

`check_s4` ✓ (29 pages) · `audit_s6` ✓ (32 pages, 0/0) · `check_links` ✓ · `check_images_unique` ✓
(**431 / 431**) · nesting HTML : **0 erreur sur 32 pages** · **574 faits / 287 sources** ·
10 illustrations IA S17 réparties une seule fois chacune.


---

## Amendement S18 — réglages : console, télévision, jeu (19/11/2026, 3 h 00)

Le site expliquait la performance, pas comment en tirer le meilleur sur son matériel. Nouvelle
section `faq#reglages`, construite sur une règle d'ordre : régler la **console**, puis la
**télévision**, puis le **jeu**.

| Couche | Réglage | Valeur |
|---|---|---|
| Console | Résolution | Automatique / 4K si compatible |
| Console | HDR | Activé **puis calibré** (trois mires, HGiG si disponible) |
| Console | VRR / ALLM / 120 Hz | Automatique si l'écran le permet |
| Télévision | Mode image | **Jeu** |
| Télévision | Interpolation de mouvement | **Désactivée** (TruMotion, MotionFlow, Auto Motion Plus) |
| Jeu | Flou de mouvement | Faible ou coupé |
| Jeu | Grain, aberration chromatique | Coupés |
| Jeu | Mini-carte | **Classique** |
| Jeu | Caméra cinématique d'accident | Désactivée |

Deux idées fausses sont nommées : le 120 Hz ne débloque pas plus de 30 images, et copier des
valeurs HDR trouvées en ligne ne sert à rien puisqu'elles dépendent de l'écran.

Complément dans `outils` : sensibilité de caméra, sensibilité de visée, zone morte, aide à la visée
modérée. La PS5 Pro ajoute le PSSR et les ombres par ray tracing (« Enhanced Fidelity »).

### QA

`check_s4` ✓ (29 pages) · `audit_s6` ✓ (32 pages, 0/0) · `check_links` ✓ · `check_images_unique` ✓
(**441 / 441**) · nesting HTML 0 erreur · **577 faits / 292 sources** · 10 illustrations IA S18.

## Amendement S19 — day-minus-one (19/11/2026)

Passe finale avant publication : ce qui change concrètement la première session, côté joueur.

### Ce que chaque geste efface (POL-36/37/38)

Coiffeur = signalement physique ; tenue complète = identifiant vêtements (une casquette ne suffit
pas) ; masque porté **pendant** le crime = le visage n'entre jamais dans la fiche ; abandon du
véhicule = identifiant véhicule (repeindre ne change que l'apparence) ; séparation du duo = brouille
l'identifiant « couple » ; rester dans le quartier = n'efface rien, les zones chaudes persistent.
Ralentir ou bloquer un agent vaut mieux que l'abattre : le profil criminel juge la méthode.

### Argent (ECN-28/29)

Cinq erreurs : acheter avant d'avoir une source de revenus, viser la propriété la plus chère,
répéter la méthode familière, oublier les frais qui courent, courir après les failles. Le garde-fou
reste le dépôt du liquide (ECN-27, Rob Nelson).

### Correctifs (LAU-36/37)

01.002.000 (13/11, ≈ 1 Go PS5 / ≈ 2,2 Go Xbox) déployé sur environ la moitié des consoles puis
11 h plus tard ; 01.002.001 (16/11, 602,5 Mo PS5 / ≈ 1,59 Go Xbox non confirmé) en trois vagues
d'environ 12 h. Aucune note Rockstar, aucun « day one patch » confirmé : garder plusieurs Go libres
au-delà des 212 Go (un re-téléchargement à 100 Mbps = ≈ 4 h 43).

### Pause, veille, Quick Resume (FAQ-12/13)

Options (PS5) / Menu (Xbox) arrête le temps du jeu, cinématiques comprises. Le mode repos suspend
une partie ; le Quick Resume Xbox restaure l'état mémoire exact sans recharger la sauvegarde, y
compris des états laissés actifs — d'où le réflexe « quitter le jeu » avant une session sérieuse.

### Première heure (TIP-53/54/55)

Terminer l'introduction (carte + téléphone), essayer voiture / moto / bateau, entrer dans un
commerce, tester le Focus à faible enjeu, repérer caméras et témoins, ne pas sprinter la campagne.
Un braquage se prépare : issues, caméras, alarme, véhicule de fuite.

### SEO et intégrité

32 pages : **0 titre > 70 caractères**, **0 description > 165**, **0 `&` brut**, 0 ancre cassée.
`en/index.html` reçoit enfin sa figure et la feuille `s4_pages.css`. Deux fichiers image jamais
référencés ont été rebranchés (studio radio → quiz, ruelle en plongée → personnages secondaires),
deux autres supprimés du disque (orphelins définitifs).

### QA

`check_s2` ✓ · `check_s3` ✓ · `check_s4` ✓ (29 pages, « 248 JPG ») · `audit_s6` ✓ (32 pages, 0/0) ·
`check_links` ✓ · `check_images_unique` ✓ (**451 / 451**) · nesting 0 erreur · 8/8 JS · YAML ✓.
**590 faits / 302 sources / 451 JPG / 32 pages.**

## Amendement S20 — jour d'ouverture (19/11/2026)

### La vague, pas l'instant (LAU-38)

Nouvelle-Zélande 11:00 UTC le 18/11 → Paris 23:00 UTC → Royaume-Uni 00:00 UTC → US East 05:00 UTC →
US West 08:00 UTC. Vingt et une heures entre le premier et le dernier grand marché. Retours NZ :
graphismes, fluidité, écriture profonde, systèmes météo locaux (« la tempête enveloppe la carte »),
aucune panne majeure signalée dans les heures suivant l'ouverture.

### Plateformes (LAU-39/40)

Xbox One : **cloud uniquement**, Xbox Cloud Gaming dès 1 h ET, rendu au préréglage Series S, 30 fps,
achat séparé, quota mensuel 15 h (Ultimate) / 10 h (Premium) / 5 h (Essential), heures achetables et,
depuis le 11/11, temps de cloud vendu sans abonnement. Aucun streaming PC : Microsoft a démenti le
droit exclusif et la diffusion vers PC.

### Ampleur (LAU-41) et notes (REV-27)

≈ 17,07 M d'unités précommandées / ≈ 1,65 Md$ (Sensor Tower, non audité), 75 % PS5 ; ≈ 2,46 M de
spectateurs Twitch simultanés le 18/11 (≈ 66 % de la plateforme). Le « 99 Metacritic » viral du soir
d'ouverture était non vérifié à l'instant T : nos chiffres viennent des agrégateurs consultés le 18/11.

### Terrain (TIP-56/57/58/59)

Boutiques hors banque en sécurité faible dans la zone de départ, une seule protagoniste souvent
suffisante ; silencieux = temps de fouille ; marqueur **rouge** = mort, **jaune** = blessé hors combat,
tête/cœur létal contre articulations invalidantes ; la simulation (salle de sport) fait partie des
habitudes qui changent une partie.

### QA

`check_s2` ✓ · `check_s3` ✓ · `check_s4` ✓ (29 pages, « 258 JPG ») · `audit_s6` ✓ (32 pages 0/0) ·
`check_links` ✓ (2 306 réf.) · `check_images_unique` ✓ (**461 / 461**) · nesting 0 erreur ·
0 titre > 70 · 0 description > 165 · 0 `&` brut · 0 ancre cassée.
**599 faits / 309 sources / 461 JPG / 32 pages.**

## Amendement S21 — pouls du jour J (19/11/2026)

Aucun correctif officiel n'était publié au moment d'écrire ces lignes. Tout ce qui suit est badgé
**COMMUNAUTÉ** : ce sont des remontées de joueurs et des mesures relayées, pas des notes Rockstar.

| Symptôme | Détail | Remède essayé |
|---|---|---|
| Coupures audio | 1 à 5 s de son haché, surtout en roulant vite en circulation dense | Stéréo non compressée, vibrations réduites, redémarrage complet |
| Pop-in | Décor et textures en retard, flou par moments | Espace libre SSD, vitesse modérée en ville |
| Chutes de fps | Zones denses, fusillades ; plus marqué sur Series S | Quitter complètement le jeu, fermer les téléchargements |
| Image floue | Rendu jugé doux sur certaines dalles | Changer d'entrée HDMI ou de mode image TV |
| Plantages | Prologue surtout, quelques extinctions de console | Correctifs à jour, reconstruction de la base de données |

**Frame rate par machine (mesures relayées)** : PS5 Pro stable à 30 avec PSSR et RT ; Series X proche
de 30 hors scènes intenses ; PS5 de base entre 30 et la fin de la vingtaine ; Series S la plus
instable, longues portions dans la vingtaine. Plancher documenté : ≈ 24 fps sur une destruction de
véhicules au lance-grenades.

**Options** : vignette en haut d'écran non désactivable ; flou de mouvement réglable ; conduite plus
lourde (entre GTA IV et GTA V) ; visée assistée jugée généreuse et souvent baissée.

**Sauvegarde** : plusieurs cas de progression perdue malgré la sauvegarde automatique — vérifier le
réglage et quitter proprement le jeu (la veille n'est pas une sauvegarde).

### QA

CP2 ✓ · CP3 ✓ · CP4 ✓ (29 pages, « 268 JPG ») · audit 32 pages 0/0 · **471 / 471** images uniques ·
0 lien cassé · 0 ancre cassée · 0 titre > 70 · 0 `&` brut.
**604 faits / 313 sources / 471 JPG / 32 pages.**
