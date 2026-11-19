# Addendum S29 — les seuils réels du 100 %, et un chiffre rétrogradé

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **666 → 671 faits**, **368 → 373 sources**. Une section ajoutée,
10 illustrations JPG, 0 audio.

---

## 1. La découverte utile du jour : le 100 % n'exige presque jamais tout

C'est le contresens le plus répandu des guides de complétion. Les seuils publiés au
lendemain de la sortie sont précis, et ils dessinent un itinéraire beaucoup plus court :

| Catégorie | Exigé | Existant |
|---|---|---|
| Séries de cartes | 15 | 18 (480 cartes) |
| Flamants de cocaïne | 100 | 125 |
| Scans WAiNK | 100 | — |
| Cascades | 300 | 397 |
| Défis | 70 | 80 |
| Véhicules de série | 200 | 277 |
| Armes standard | 50 | 66 |
| Espèces étudiées | 100 | 255 |
| Paniers de basket | 90 | 100 |
| Médailles d'or (stand de tir) | 42 | 42 |

Trois astuces qui découlent directement de ces chiffres :

- **Méditations** : 10 sites seulement, mais méditer avec Jason *et* Lucia sur le même site
  compte pour deux → 18 possibles, 15 exigées.
- **Cartes** : vendre une carte à un prêteur ne la retire pas de la collection.
- **Stand de tir** : acheter d'abord l'autorisation à 5 $ au préposé ; les 42 essais de drone
  se répartissent sur 14 sites, le troisième essai s'ouvrant après le par des deux premiers.

Et un piège de planification : **les trophées ne suivent pas le 100 %** — « Cunning Stunts »
demande 250 cascades (le 100 % en exige 300), « One Last Thing » 50 défis sur 80. Faire le
100 % d'abord évite de doubler du contenu déjà validé.

## 2. Un chiffre rétrogradé de « confirmé » à « rapporté »

La taille Xbox du correctif 01.002.000 n'a jamais été relevée à l'écran. Les trackers donnent
1,07 Go sur les deux consoles, d'autres sources 2,18 Go. Seul le poids PS5 (1,07 Go) est
documenté. Le corpus enregistre désormais cette nuance au lieu de trancher arbitrairement :
`REL-35`. C'est la deuxième correction de chiffres en deux étapes — et la règle reste la même :
une valeur non confirmée n'est pas publiée comme un fait.

## 3. Section publiée

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| Collectibles | `#seuils-reels` | tableau des seuils exacts, méditations doublées, stand de tir, drones, écart trophées/100 % | MIS-47 → 50, REL-35 |

## 4. Médias

10 JPG 1920×1080 q86 progressif, tous distincts (`completion/`) : flamant de pelouse, classeur
de cartes, stand de tir, drone, panier de rue, saut de pont, méditation sur ponton, traces de
faune, jumelles, menu de progression nocturne.

**Inventaire publié : 528 JPG, 528 emplacements, 0 réutilisation.**

## 5. Contrôles du 19/11/2026 (après S29)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 671 faits / 373 sources
python3 tools/check_s4.py            ✓ CP4 — 29 pages, 337 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 0 référence interne cassée
python3 tools/check_images_unique.py ✓ 528 / 528
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
```
