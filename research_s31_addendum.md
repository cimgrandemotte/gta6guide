# Addendum S31 — 30 fps expliqués, réglages, règles de métier

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **678 → 683 faits**, **380 → 386 sources**. Deux sections ajoutées,
9 illustrations JPG, 0 audio.

---

## 1. Les 30 fps ne sont pas un choix commercial, mais une limite de processeur

| Machine | Mesure rapportée | Détail |
|---|---|---|
| PS5 Pro | **30 fps quasi parfait** | plus de 50 h sans une seule chute ; ombres tracées + PSSR en plus |
| PS5 | 30 fps avec de petites chutes | « peine à tenir 30 plus souvent que prévu » |
| Series X\|S | selon les relevés | la Series S est la plus en difficulté |

Explication officielle : **Marc Chambers** (directeur de production technologique, Rockstar)
précise que la présentation de base utilise déjà réflexions et illumination globale en ray
tracing, et que la PS5 Pro ajoute les ombres tracées et le PSSR. « Le processeur de la PS5 Pro
n'est pas assez puissant pour faire tourner la simulation à des fréquences plus élevées. »
Un mode 60 fps est donc improbable sur cette génération — **ce n'est pas une question de
réglages à baisser**, et le site le dit ainsi plutôt que d'entretenir l'espoir d'un patch.

## 2. Réglages : effet réel et contrepartie

| Réglage | Effet | Contrepartie |
|---|---|---|
| Zone morte des sticks | réponse plus précoce, lourdeur atténuée | micro-mouvements involontaires |
| Flou de mouvement | netteté en mouvement | sur OLED, certains préfèrent le garder |
| Vider le cache (PS5 base) | moins de saccades selon plusieurs joueurs | aucune |
| Couper le HDCP | saccades réduites selon un joueur | **plus de Blu-ray ni de streaming** |

Les trois derniers sont des retours de joueurs ; seul le premier est un réglage de confort
largement confirmé. Le site étiquette chaque ligne.

## 3. Règles de métier (le vrai gain)

- **Jamais de crime avec son propre véhicule** : identifié, il part à la fourrière ; voler une
  voiture jetable et l'abandonner coûte moins cher.
- **Donner le butin au partenaire** : il le revend ; un peu moins d'argent, beaucoup de trajets
  en moins. Plus tard, les receleurs vident les sacs des garages possédés.
- **Point de contrôle : dedans oui, dehors non** — « reprendre au dernier point de contrôle »
  est gratuit en mission, sans effet en monde ouvert.
- **Focus mode** : presser les deux sticks fait apparaître un halo autour des sources de bruit
  (signal d'une rencontre unique) ; on peut pousser un véhicule à la main ; n'importe quelle
  explosion ouvre un coffre.

## 4. Sections publiées

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| Tips | `#reglages-et-metier` | table des réglages avec contreparties, quatre règles de métier, Focus mode | TIP-64 → 66 |
| Reviews | `#30-fps-explique` | mesures par console, explication Rockstar, ce que cela exclut | REV-30, REV-31 |

## 5. Médias

9 JPG 1920×1080 q86 progressif (`reglages/`) : réglage de zone morte, téléviseur OLED, halo de
bruit, fourrière, passage du sac, chambre de motel, cache de console, rue calme, ray tracing.

**Inventaire publié : 546 JPG, 546 emplacements, 0 réutilisation.**

## 6. Contrôles du 19/11/2026 (après S31)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 683 faits / 386 sources
python3 tools/check_s4.py            ✓ CP4 — 29 pages, 355 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 0 référence interne cassée
python3 tools/check_images_unique.py ✓ 546 / 546
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
python3 tools/build_s6.py            ✓ 8/8 modules
```
