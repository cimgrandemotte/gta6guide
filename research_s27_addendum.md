# Addendum S27 — avant minuit, argent du début, cartes ouvertes

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **653 → 662 faits**, **351 → 362 sources**. Quatre sections ajoutées,
10 illustrations JPG, 0 audio (décision C3 maintenue).

---

## 1. Ce qui a bloqué les joueurs n'était pas le serveur

Deux téléchargements, et un seul est officiellement documenté comme obligatoire :

| Élément | Version | Poids | Statut |
|---|---|---|---|
| Firmware PS5 (Sony) | 26.07-14.23.00 | — | **obligatoire**, publié le 17/11, notes = « correctifs de sécurité » |
| Mise à jour du jeu | 01.002.000 | 1,07 Go | 13/11, obligatoire, PS5 + Xbox rapporté |
| Mise à jour du jeu | 01.002.001 | 602,5 Mo PS5 / ~1,59 Go Xbox | 16/11, trois vagues sur PS5 |
| Patch de lancement | — | — | **aucun confirmé par Rockstar** au soir du 19 |

Conséquence pratique retenue par la presse : garder plusieurs gigaoctets libres au-delà des
212 Go installés, et vérifier manuellement « Check for Update » sur la vignette du jeu.
Un préchargement interrompu signifie retélécharger jusqu'à 212 Go, soit près de cinq heures à
100 Mbps. Toujours **aucune note de version** : le site ne résume donc pas ces correctifs.

## 2. Les trois habitudes du début (statut communauté)

Retours de joueurs des premières vingt-quatre heures, publiés sur r/GTA6 et repris par les
guides du jour — donc étiquetés `community`, jamais `official` :

- **S'entraîner chaque jour** : gratuit, augmente santé maximale et endurance, avec un plafond
  quotidien ; les barres protéinées rendent les gains temporaires et raccourcissent l'attente.
- **Ne pas mourir riche** : à la mort ou à l'arrestation, le liquide et les armes non achetées
  sont perdus ; environ 1 000 $ sur soi, le reste au refuge puis à la banque.
- **Furtivité d'abord** : munitions rares, police nettement plus dure que dans les épisodes
  précédents, et bonus non létal comptabilisé dans le profil criminel.

## 3. La route de l'argent, chapitre par chapitre

Chiffres de guides publiés au lancement, présentés comme des ordres de grandeur :

| Chapitre | Source | Ordre de grandeur |
|---|---|---|
| 1 | supérettes, plongées de Kenton | petits montants, puis dizaines de milliers au total |
| 2 | véhicules volés vendus à Moses | 1 000 $ à plus de 10 000 $ par contrat |
| 3 | bijouteries, puis Randy après le cloneur de clé | 10 000–25 000 $ ; plus de 30 000 $ |
| fin 4 | gros coffres de banque | jusqu'à ~205 000 $ |

## 4. Cartes et checklists open source

Aucune carte interactive officielle au 19/11. Trois projets de fans, libres et hors ligne :

- **ViceRoute** (lociAI, MIT) — 100 points, tri par proximité, export JSON, vérification à 10 joueurs.
- **Leonida Atlas** (navanem, AGPL-3.0) — 2 204 lieux dérivés de GTADB (CC BY 4.0), notes privées, sans compte.
- **GTA6 Atlas** (jerrysf) — checklist de complétion avec export/import JSON, étiquettes de vérification honnêtes.
- **awesome-gta-6** (devtoship) — liste maintenue séparant sources officielles et outils de fans.

Le site les cite comme **outils**, avec licence et statut, sans reprendre aucune coordonnée
communautaire comme un fait.

## 5. Nettoyage de publication (S27)

- **7 entrées mortes retirées de l'index de recherche** (`research_data.json`, addendas,
  `design_system.md`, `workflow_master.yaml`, `state.json`, `README.md`).
- `search.js` ne fait **plus aucune requête** vers le corpus : l'index local est la seule
  source, ce qui rend le moteur de recherche identique en local et en ligne.
- **12 JPG archivés** (`assets/images/_archives/`, doublons de la génération S2) sortis du
  paquet : chaque image publiée est désormais référencée par une page.

## 6. Sections publiées

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| Lancement | `#avant-minuit` | firmware PS5 obligatoire, patch non confirmé, coût d'un oubli | REL-32, REL-33, FIX-06 |
| Tips | `#argent-et-coffre` | perte à la mort, coffre du véhicule, entraînement quotidien | TIP-61 → 63 |
| Économie | `#route-argent` | rentabilité par chapitre, plafonds et accélérateurs | ECO-39, ECO-40 |
| Outils | `#cartes-communautaires` | ViceRoute, Leonida Atlas, GTA6 Atlas, awesome-gta-6 | CMT-33, CMT-34 |

## 7. Médias

10 JPG 1920×1080 q86 progressif, tous distincts, badgés **ILLUSTRATION IA** (dossier
`depart/`) : mise à jour système de la console, préchargement interrompu, tiroir-caisse du
refuge, coffre de voiture américaine, plongée au trésor, repaire de nuit, vitrine de
bijouterie, chambre forte, salle de sport à l'aube, poste de cartographie.

**Inventaire publié : 508 JPG référencés, 508 emplacements, 0 réutilisation.**

## 8. Contrôles du 19/11/2026 (après S27)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 662 faits / 362 sources
python3 tools/check_s4.py            ✓ CP4 — 29 pages, 317 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 2 259 références internes, 0 cassée
python3 tools/check_images_unique.py ✓ 508 / 508
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
paquet out/publish                   ✓ 603 fichiers, 0 lien cassé, 0 ancre morte
```
Badges des nouvelles sections renommés « RETOURS DE JOUEURS » et « OUTILS DE FANS »
(aucune mention « COMMUNAUTÉ » nulle part dans le HTML), et l'édition affichée passe à
**S27** dans les 33 pages avec les compteurs 662 / 362.
