# Addendum S25 — le jour de la sortie : ce qui est vérifié, ce qui ne l'est pas

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **631 → 646 faits**, **337 → 347 sources**. Cinq sections ajoutées,
10 illustrations JPG, 0 audio (décision C3 maintenue).

---

## 1. Le chiffre du jour est faux — et c'est le sujet

Toute la presse reprend « **17,07 millions de copies et 1,65 milliard de dollars en 24 heures** ».
Vérification faite : **ni Rockstar ni Take-Two n'ont publié le moindre chiffre de ventes,
de précommandes ou de revenus** au 19 novembre 2026. Les 17,07 M viennent d'une estimation
de **Sensor Tower arrêtée au 18 novembre**, soit la veille de la sortie — donc avant que le
jeu ne soit jouable nulle part. Elle a ensuite été recopiée comme un résultat du premier jour.

Ce qui est réellement sur le registre :

| Chiffre | Nature | Portée |
|---|---|---|
| ventes / précommandes / revenus | **aucun** | Take-Two et Rockstar, au 19/11 |
| 17,07 M · 1,65 Md$ | estimation Sensor Tower | précommandes numériques, arrêtées au 18/11 |
| 3,35 à 3,5 Md$ de réservations nettes | prévision Take-Two | trimestre clos le 31/12/2026 |
| 11,21 M · 815,7 M$ en 24 h | record officiel GTA V (2013) | la référence à battre |

Le site publie cette distinction en tête de section, avec un encadré d'avertissement. Il ne
« corrige » pas les autres médias : il explique la différence entre officiel, estimé et
projeté, et donne le réflexe utile — **chercher la date du chiffre avant son auteur**.

Signal de marché, ajouté pour être complet : l'action Take-Two avait perdu près de 10 % sur
les deux séances précédant la sortie, avant de reprendre environ 7,7 %.

---

## 2. Astuces du jour de sortie, vérifiées

| Ancre | Contenu | Faits |
|---|---|---|
| `economie#keys` | les quatre paquets des Keys (~900 $ chacun) après « Clean Up After Donnie » ; vendre immédiatement ; le piège de la boutique de Shirley ; cartes à collectionner et chapeaux conservés | ECO-35 → 38 |
| `tips#premier-jour` | la cache sous le plancher, **Dolores** et le bonus de Focus, portes blanches/rouges, bonnes actions et routine, péage des Keys à 5 $ et point de non-retour de Key Lento | TIP-54 → 57 |
| `lancement#direct` | le direct de 24 h sur YouTube : ce qu'il n'apporte pas, et le risque de spoilers pour qui joue en décalé | REL-31 |
| `news#chiffres` | le tableau officiel / estimé / projeté, et ce que le site fera quand un chiffre sortira | SAL-01 → 04 |
| `faq#chiffres-faq` | la même distinction, en trois lignes, pour les lecteurs pressés | SAL-01 |

Complément technique : RockstarINTEL documente le déploiement du second correctif par vagues
(33 %, puis 22 h GMT, puis le 17 à 10 h GMT), la version **1.0.2.1** côté Xbox et une
installation à 211,9 Go. **Toujours aucune note de version publiée** au 19 novembre. (`FIX-06`, `FIX-07`)

---

## 3. Ce qui n'a pas été publié, volontairement

- **Aucun chiffre de ventes inventé ou extrapolé.** Le site dit « aucun chiffre officiel », ce
  qui est exactement ce que disent les registres de Take-Two au 19/11.
- **Aucune reprise du direct YouTube** ni de capture de flux : la section explique le direct,
  elle ne le relaie pas.
- **Aucune solution de triche** : les codes d'argent circulant pour GTA VI restent non vérifiés
  et ne sont pas relayés (règle déjà en place depuis S4).
- **Aucune voix off** (décision C3) : 12 MP3 existants, aucun ajout audio.

---

## 4. Médias

10 JPG 1920×1080, qualité 86, progressif, tous distincts, badgés **ILLUSTRATION IA** :

| Fichier | Sujet |
|---|---|
| `sales/sales_tally_board_night_01.jpg` | salle de rédaction, mur d'écrans et graphique |
| `sales/sales_stock_ticker_window_01.jpg` | fenêtre pluvieuse, ordinateur et cours boursier |
| `sales/sales_press_conference_podium_01.jpg` | podium vide sous un projecteur |
| `tips/tips_floorboards_cash_stash_01.jpg` | lames de parquet soulevées, billets et photos |
| `tips/tips_snake_feed_focus_01.jpg` | serpent dans son terrarium, nourrissage |
| `tips/tips_keys_backroom_door_01.jpg` | porte d'arrière-boutique, enseigne lumineuse |
| `economie/economie_keys_boat_packages_01.jpg` | bateau au mouillage dans les Keys |
| `economie/economie_pawnshop_cards_counter_01.jpg` | comptoir de prêteur sur gages, cartes |
| `news/news_livestream_watch_party_night_01.jpg` | salon, trois silhouettes devant un direct |
| `news/news_correction_desk_lamp_01.jpg` | lampe, pages imprimées, stylo rouge |

**Inventaire publié : 488 JPG distincts, 488 emplacements, 0 réutilisation.**

---

## 5. Contrôles du 19/11/2026 (après S25)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 646 faits / 347 sources vérifiés dans le HTML
python3 tools/check_s4.py            ✓ CP4 — 29 pages de contenu, 297 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 2 276 références internes, 0 cassée
python3 tools/check_images_unique.py ✓ 488 / 488
python3 tools/build_s6.py            ✓ CSS 100 → 69 Ko, JS 97 → 83 Ko, 8/8 modules
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
```
