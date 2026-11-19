# Addendum S24 — mesures de la première nuit

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **623 → 631 faits**, **329 → 337 sources**. Cinq sections de contenu ajoutées,
10 illustrations JPG, 0 audio (aucune voix off, décision C3 maintenue).

---

## 1. Ce que la nuit a réellement appris

Trois sujets, tous documentés par des mesures ou des déclarations datées, remplacent enfin
les « on verra bien » de la veille : la tenue des cadences, la raison technique du plafond à
30 images par seconde, et une panne réseau qui a gâché l'attente de milliers de joueurs.

### Résolutions et cadences mesurées

| Console | Rendu interne | Mise à l'échelle | Cadence observée |
|---|---|---|---|
| PS5 Pro | 2560×1440 | PSSR → 4K + ombres tracées | quasi verrouillée à 30, 24 dans les pires explosions |
| PS5 | 2560×1440 | TAA maison → 4K | 30 avec descentes dans la vingtaine haute |
| Xbox Series X | 2560×1440 | TAA maison → 4K | 30 avec descentes, plancher à 22 |
| Xbox Series S | 720p | AMD FSR 4 → 1080p | ≈27 en jeu, 25 en fusillade, 20 en scène intense, 18-19 en explosion |

La Series S est la **première jeu commercial** à utiliser FSR 4 sur la console. Elle conserve
les cheveux simulés par mèches, l'illumination globale et les reflets tracés par rayons ;
elle perd les ombres tracées, réservées à la PS5 Pro.

### Pourquoi 30 et pas 40

Rockstar a répondu à TechRadar le 18 novembre. Jonathon Ashcroft (vice-président technologie) :
« la complexité à simuler et rendre notre monde […] demande d'équilibrer soigneusement chaque
milliseconde du processeur et du processeur graphique », avec « seulement 33 ms pour le faire ».
Marc Chambers (production technique) ajoute que le processeur de la PS5 Pro n'est que
légèrement supérieur à celui de la PS5 — insuffisant pour accélérer la simulation. La
technologie est entièrement maison. Ce ne sont donc pas des options graphiques qui manquent,
c'est du temps de calcul.

### La panne PlayStation du 18 novembre

Signalements en hausse à partir de 19 h (Paris), environ 876 puis plus de 4 000 sur
Downdetector, page d'état Sony en panne sur « Gaming and Social », retour au vert vers 21 h,
sans explication de cause. Le dépannage utile est publié tel quel : page d'état d'abord,
redémarrages ensuite, reconnexion au compte en dernier.

---

## 2. Nouvelles sections publiées

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| News | `#mesures` | tableau résolutions/cadences, ce que la Series S garde et perd, explication Rockstar, réglages utiles | DFF-01 → 04, PRF-02 |
| News | `#reseau` | chronologie de la panne PSN et dépannage ordonné | PRF-03, PRF-04 |
| Lancement | `#cadences` | qui tient 30 fps, ventilateur comme réglage de performance, ce qui ne changera pas | PRF-01, PRF-02, DFF-02 |
| Divers | `#upscaling` | 1440p, trois suréchantillonneurs, deux résultats perçus | DFF-01 → 03 |
| FAQ | `#entretien` | tableau symptôme → cause → geste, et le point de méthode sur les impressions contradictoires | PRF-01 |

Le moteur de recherche gagne cinq entrées, toutes vérifiées (ancre existante, vignette
existante).

---

## 3. Médias

10 JPG 1920×1080, qualité 86, progressif, tous distincts, tous badgés
**ILLUSTRATION IA · NON OFFICIEL** :

| Fichier | Sujet |
|---|---|
| `perf/perf_pro_console_living_room_01.jpg` | console posée dans un salon, écran allumé |
| `perf/perf_small_console_shelf_01.jpg` | petite console sur une étagère encombrée |
| `perf/perf_frame_analysis_desk_01.jpg` | bureau d'analyse, courbes et carte thermique |
| `perf/perf_thermal_probe_bench_01.jpg` | sonde thermique sur une grille d'échappement |
| `perf/perf_signin_error_screen_01.jpg` | échec de connexion sur grand écran, pièce sombre |
| `perf/perf_router_reboot_hands_01.jpg` | mains rebranchant un routeur |
| `perf/perf_upscaler_comparison_wall_01.jpg` | deux tirages, l'un plus doux |
| `perf/perf_vrr_tv_settings_01.jpg` | réglages d'image sur un téléviseur |
| `perf/perf_fan_dust_closeup_01.jpg` | ventilateur encrassé en macro |
| `perf/perf_night_drive_rig_01.jpg` | dispositif de capture en voiture, la nuit |

**Inventaire publié : 478 JPG distincts, 478 emplacements, 0 réutilisation.**

---

## 4. Ce qui est refusé

- **Aucune capture officielle** n'est reproduite : les illustrations restent générées par IA
  et badgées comme telles, y compris quand elles montrent une console ou une télévision.
- **Aucun chiffre inventé** : les cadences et résolutions publiées sont celles mesurées par
  Digital Foundry sur versions commerciales ; les valeurs de la Series S sont données en
  fourchettes observées, jamais en moyenne fabriquée.
- **Aucune promesse de correctif** : le site dit ce que Rockstar a dit, y compris que rien
  n'indique qu'un mode 40 ou 60 images arrivera un jour.
- **Aucune voix off** n'a été produite (décision C3).

---

## 5. Contrôles du 19/11/2026 (après S24)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 631 faits / 337 sources vérifiés dans le HTML
python3 tools/check_s4.py            ✓ CP4 — 29 pages de contenu, 287 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 2 266 références internes, 0 cassée
python3 tools/check_images_unique.py ✓ 478 / 478
python3 tools/build_s6.py            ✓ CSS 100 → 69 Ko, JS 96 → 82 Ko, 8/8 modules
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
```
