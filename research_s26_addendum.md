# Addendum S26 — astuces de déplacement, vol de véhicules, état à J+0

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **646 → 653 faits**, **347 → 351 sources**. Trois sections ajoutées,
10 illustrations JPG, 0 audio (décision C3 maintenue).

---

## 1. Le sujet le plus utile de la journée : on ne se téléporte pas

C'est la première surprise du jeu et elle coûte cher à qui l'ignore : **aucun clic sur la
carte ne téléporte**. Trois méthodes existent, documentées et vérifiées :

| Méthode | Coût | Limite |
|---|---|---|
| Changer de personnage | gratuit | la plus rapide ; l'autre personnage attend près du refuge en cours |
| Bus et trains | quasi gratuit | soumis à des horaires, réseau dense dans Vice City |
| RydeMe / Paradise Taxi | course + 100 $ pour sauter le trajet | l'app arrive au chapitre 2, le taxi dès la première mission |

Deux compléments : l'**autopilote** (croix directionnelle vers le bas, caméra cinématique)
respecte le code à la lettre et s'arrête net dans les embouteillages ; le **pourboire de 5 $**,
jusqu'à deux fois, fait accélérer le chauffeur. Et le moment de la journée change la réaction
policière — une rue calme la nuit rend un braquage plus simple qu'un après-midi de Vice City.

## 2. Voler une voiture sans se faire repérer

Ordre des gestes : **scanner (WAiNK)** → comprendre le traceur → choisir une cible adaptée à sa
progression → charger. Traceur standard : pas de modification sans immatriculation. Traceur
avancé : il prévient la police si la voiture s'éloigne trop de son point d'origine, et rouler
vite est la seule façon d'empêcher le signalement. Les modèles sans clé exigent un **cloneur
de clé** qui n'arrive que plus tard — une limite de progression, pas un bug. SUV pour le
chargement, camion pour certains braquages. Revenu d'appoint sans receleur : les **conteneurs
maritimes** (argent, armes, parfois un véhicule léger).

## 3. Notes de version : toujours rien

Vérification refaite après l'ouverture : **Rockstar n'a publié aucune note** ni pour 1.002.000
ni pour 1.002.001. Les seuls éléments confirmés restent les versions, les tailles et les vagues
de déploiement (50 % puis 11 h plus tard pour la première, 33 % / 22 h GMT / 17 à 10 h GMT pour
la seconde). Le site le dit au lieu de résumer en « corrections de bugs ».

## 4. Sections publiées

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| Tips | `#se-deplacer` | tableau des trois méthodes, autopilote, pourboire, aide contextuelle | TIP-58 → 60, MEC-31 |
| Véhicules | `#voler` | scanner, traceurs, cloneur de clé, chargement, conteneurs | VEH-41 → 43 |
| News | `#etat-j2` | état vérifié au soir du 19 : notes, ventes, mode performance, online | FIX-06 |

## 5. Médias

10 JPG 1920×1080 q86 progressif, tous distincts, badgés **ILLUSTRATION IA** (dossier
`deplacement/`) : course de nuit au trottoir, autopilote sous la pluie, quai de train au
crépuscule, coffre de SUV, parc à conteneurs, scan de véhicule au téléphone, établi du
cloneur de clé, rue déserte à 2 h, aide contextuelle, refuge à l'aube.

**Inventaire du site : 510 JPG distincts, 498 emplacements dans le HTML, 0 réutilisation.**
Les 12 visuels restants servent d'images d'aperçu social (`og:image`) et de favicons JPEG,
ce qui explique l'écart entre le nombre de fichiers et le nombre d'images insérées.

## 6. Paquet de publication

`out/publish/` contient exactement ce qui doit être servi : **605 fichiers** — 33 HTML, 7 CSS,
8 JS, 510 JPG, 12 MP3, `CNAME`, `.nojekyll`, `sitemap.xml`, `robots.txt`, `manifest.json`,
`404.html`, crédits, plus `SHA256SUMS.txt` (605 empreintes). Aucun `tools/`, `dist/`,
`research_data.json`, `state.json`, `.md` de travail, ni archive.

Deux défauts trouvés en construisant le paquet et corrigés dans les pages sources :

1. **34 liens vers `research_data.json`** (corpus non publié) et 8 liens vers des documents de
   travail (`README.md`, `state.json`, `workflow_master.yaml`, `design_system.md`,
   `research_*.md`) : remplacés par des destinations réelles du site (Newswire, page News,
   FAQ « chiffres », mentions légales, sitemap).
2. **Liens de crédits en chemin relatif faux** (`../../assets/...` depuis `pages/<dossier>/`) :
   passés en chemin absolu `/assets/images/CREDITS.md` et `/assets/audio/CREDITS.md`.
   Plus **2 ancres mortes** dans la page News (`reviews#joueurs`, `codes#coffres`) repointées
   vers `#verdict` et `#zero`.

Contrôle final du paquet : **2 249 références internes, 0 cassée, 0 ancre morte**.

## 7. Contrôles du 19/11/2026 (après S26)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 653 faits / 351 sources vérifiés dans le HTML
python3 tools/check_s4.py            ✓ CP4 — 29 pages de contenu, 307 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 2 286 références internes, 0 cassée
python3 tools/check_images_unique.py ✓ 498 / 498
python3 tools/build_s6.py            ✓ CSS 100 → 69 Ko, JS 97 → 84 Ko, 8/8 modules
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
```
