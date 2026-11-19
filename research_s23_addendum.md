# Addendum S23 — veille du 19 novembre et nouveaux chapitres

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **604 → 623 faits**, **313 → 329 sources**. Six sections de contenu ajoutées,
10 illustrations JPG, 0 audio (aucune voix off, décision C3 maintenue).

---

## 1. Ce que la veille a apporté

Deux sujets ont réellement bougé entre le 18 et le 19 novembre, et un troisième méritait
d'être écrit noir sur blanc : ce que les correctifs **ne** changent pas.

### Le firmware PS5 bloque le lancement

Sony a publié la mise à jour système **26.07-14.23.00** le 17 novembre, environ **1,3 Go**
(1,267 Go mesuré), notes réduites à « correctifs de sécurité ». Le support PlayStation US
précise qu'elle est **requise avant de jouer** : sans elle, GTA VI ne démarre pas, même
installé et à jour. Les deux modèles, PS5 et PS5 Pro, sont concernés. La presse y voit une
fermeture de porte avant diffusion d'un binaire, juste après les travaux publics sur le
jailbreak de la version 14.22 — ce n'est pas une explication officielle, et le site le dit
ainsi.

### Les correctifs, sans notes

| Version | Date | PS5 | Xbox Series X\|S | Notes |
|---|---|---|---|---|
| 01.002.000 | 13/11 | ≈ 1,073 Go | ≈ 2,2 Go (rapporté) | aucune |
| 01.002.001 | dès le 16/11 | 602,5 Mo | ≈ 1,59 Go (rapporté) | aucune |

Trois faits tiennent sans note officielle : les tailles, le calendrier de déploiement en
vagues (trois vagues de douze heures sur PS5) et ce que les fichiers ne touchent pas —
l'audio, les cinématiques et les bases de textures sont inchangés, l'installation retombe
même à 209,9 Go. **Aucun mode performance n'est arrivé, et aucun n'est annoncé.**

Point de méthode : Rockstar Support publie ses notes de version une par une, jamais sur le
Newswire. Au 17 novembre, il n'en existait aucune pour GTA VI. Toute liste de correctifs
antérieure à cette publication est une reconstitution — le site l'écrit au lieu de la
recopier.

---

## 2. Nouvelles sections publiées

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| News | `#firmware` | le firmware obligatoire, tableau, échéance, lecture du contexte sécurité | FIX-01, FIX-05 |
| Lancement | `#notes` | ce que les correctifs changent vraiment, et ce qu'ils ne changent pas | FIX-02 → FIX-04 |
| Police | `#reconnaissance` | quatre gestes de préparation : Focus sans mini-carte, balisage des gardes, alarme avant caméras, désescalade | POL-39 → POL-42 |
| Économie | `#receleurs` | les quatre receleurs et leurs spécialités, ordres de grandeur par activité, plafond de liquide, zone spoiler du chapitre 4 | ECO-30 → ECO-34 |
| Tips | `#reflexes` | tenue dans le coffre, portière comme arme, stats qui se perdent, absence de rejeu de mission | TIP-50 → TIP-53 |
| Outils | `#firmware-outil` | liste de vérification du soir de sortie, quatre étapes, sans outil tiers | FIX-01 → FIX-03, TIP-52 |

La FAQ renvoie vers cette liste depuis le bloc « Réglages », et le moteur de recherche gagne
six entrées.

---

## 3. Ce qui a été écarté, et pourquoi

- **Les trois cartes communautaires open source** (gta6map.github.io, Leonida Atlas,
  GTA6mapx) sont documentées dans le corpus sous `OUT-24`, mais **ne sont pas publiées** :
  la décision B4 — retirer le contenu communautaire — prime sur l'intérêt du lien. Elles
  restent traçables pour une réactivation ultérieure.
- **L'économie « farm » à base de cryptomonnaie** est réelle mais narrative : elle est
  publiée dans un bloc `data-spoiler-toggle` fermé par défaut, conformément à la règle
  « tout masqué ».
- **Les notes de version** ne sont pas inventées : le site documente leur absence, datée.
- **Aucune voix off** n'a été produite : la décision C3 reste appliquée, et les 12 MP3
  existants suffisent à la playlist.

---

## 4. Médias

10 JPG 1920×1080, qualité 86, progressif, tous distincts, tous badgés
**ILLUSTRATION IA · NON OFFICIEL** sur la page :

| Fichier | Sujet |
|---|---|
| `fixes/fixes_console_download_night_01.jpg` | console et barre de progression à 23 h 50 |
| `fixes/fixes_firmware_dashboard_dawn_01.jpg` | écran de mise à jour système à l'aube |
| `fixes/fixes_patch_waves_room_01.jpg` | trois écrans, déploiement en vagues |
| `police/police_focus_silhouettes_alley_01.jpg` | silhouettes policières dans une ruelle |
| `police/police_alarm_panel_backroom_01.jpg` | panneau d'alarme en réserve de supérette |
| `economie/economie_fence_garage_dusk_01.jpg` | garage du receleur au couchant |
| `economie/economie_atm_deposit_night_01.jpg` | dépôt de nuit à un distributeur |
| `tips/tips_trunk_outfit_switch_01.jpg` | tenue de rechange dans le coffre |
| `tips/tips_gym_stats_dawn_01.jpg` | salle de sport de quartier à l'aube |
| `tips/tips_manual_save_console_01.jpg` | sauvegarde manuelle, manette et télévision |

**Inventaire publié : 468 JPG distincts, 468 emplacements, 0 réutilisation.**

---

## 5. Contrôles du 19/11/2026

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 623 faits et 329 sources vérifiés dans le HTML
python3 tools/check_s4.py            ✓ CP4 — 29 pages de contenu, 277 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 2 256 références internes, 0 cassée
python3 tools/check_images_unique.py ✓ 468 / 468
python3 tools/build_s6.py            ✓ CSS 100 → 69 Ko, JS 95 → 81 Ko, 8/8 modules
```

Le fichier `assets/js/search.js` a été nettoyé au passage : entrée de la page anglaise
supprimée, quatre entrées pointant vers des ancres disparues retirées (quiz, outils), deux
ancres remplacées par les sections existantes. Aucun lien mort ne subsiste dans l'index de
recherche.
