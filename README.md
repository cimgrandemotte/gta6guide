# GTA VI — The Ultimate Guide

Guide francophone non officiel de **Grand Theft Auto VI** (Rockstar Games), sorti le
**19 novembre 2026** sur PlayStation 5 / PS5 Pro et Xbox Series X|S.

**Site publié : [https://gta-6.duckdns.org](https://gta-6.duckdns.org)** — GitHub Pages, domaine
personnalisé, HTTPS forcé. Site statique complet : **33 fichiers HTML** (30 pages de contenu,
2 pages légales, 1 page 404), **683 faits sourcés**, **386 sources**, **556 illustrations JPG** (546 référencées),
**12 MP3**, zéro dépendance à l'exécution.

> Projet de fan, sans affiliation avec Rockstar Games ou Take-Two Interactive.
> Aucune image officielle n'est reproduite : toutes les illustrations sont générées par IA
> et badgées **ILLUSTRATION IA · NON OFFICIEL** sur les pages qui les affichent.
> © 2026 direct — tous droits réservés.

---

## 1. Ce que contient le guide

| Bloc | Pages | Contenu |
|---|---|---|
| Accueil | `index.html` | compte à rebours, faits officiels, stratégies, galeries, lecteur audio, recherche |
| Histoire & personnages | `pages/histoire/` (3), `pages/personnages/` (3) | synopsis, missions (post-lancement), Lucia, personnages secondaires |
| Monde | `pages/carte/vice-city.html`, `pages/carte/index.html` | Vice City, carte interactive de Leonida (28 lieux, filtres) |
| Gameplay | `pages/armes/`, `pages/vehicules/`, `pages/police/`, `pages/economie/`, `pages/activites/` | armes, véhicules, étoiles de recherche, argent, activités |
| Média & online | `pages/musique/`, `pages/online/`, `pages/codes/` | radio et score, mode en ligne (non annoncé), codes (aucun publié) |
| Complétion | `pages/trophees/`, `pages/secrets/`, `pages/tips/`, `pages/collectibles/` | 55 trophées, easter eggs, astuces, checklist 100 % persistée |
| Divers & service | `pages/outils/`, `pages/divers/`, `pages/faq/`, `pages/quiz/`, `pages/qa/`, `pages/final/` | outils maison, identité visuelle, FAQ, quiz 30 questions, audit QA, livraison |
| Presse | `pages/reviews/index.html` | tests de la presse du 18/11 : Metacritic 99, OpenCritic 98-99 |
| Lancement | `pages/lancement/index.html` | nuit de lancement, ouverture mondiale heure par heure, technique mesurée |
| Juridique | `pages/legal/mentions-legales.html`, `pages/legal/confidentialite.html` | éditeur, hébergeur, propriété intellectuelle, procédure de retrait, zéro collecte |

**Statuts éditoriaux** utilisés partout : `OFFICIEL`, `PRESSE · 18/11`, `VÉRIFICATION`,
`OUTIL DU SITE`, `SPOILER`, `EN ATTENTE · 19/11`, `ESTIMATION`. Le badge `COMMUNAUTÉ`
a été retiré en S22 (voir § 7).

---

## 2. Installation et lancement

Aucune dépendance n'est nécessaire pour consulter le site.

```bash
# 1. servir le site en local (Node ≥ 18, bibliothèque standard uniquement)
node tools/serve.js          # http://0.0.0.0:3000

# 2. ou simplement ouvrir index.html dans un navigateur
```

Vérifications (reproductibles, sans réseau) :

```bash
node tools/check_links.js                 # liens internes : 2 246 références, 0 cassée
python3 tools/check_s2.py                 # design system
python3 tools/check_s3.py                 # pages cœur, 0 format interdit
python3 tools/check_s4.py                 # 29 pages de contenu + médias + formats
python3 tools/audit_s6.py                 # QA : contrastes, a11y statique, budget, sitemap
python3 tools/check_images_unique.py      # 459 images / 459 emplacements
python3 tools/build_s6.py                 # build minifié optionnel dans dist/
```

Les outils Python requis par les scripts d'images et d'audio : `Pillow`, `numpy`,
`lameenc`, `PyYAML`. Ils ne servent **jamais** à l'exécution du site.

---

## 3. Publication sur GitHub Pages

Le site est prêt à être publié, sans build obligatoire : aucun CDN, aucune police distante,
URLs internes strictement relatives, `canonical` / `og:url` / `sitemap` absolus.

**Fichiers de publication à la racine :**

| Fichier | Rôle |
|---|---|
| `CNAME` | contient `gta-6.duckdns.org` — domaine personnalisé GitHub Pages |
| `.nojekyll` | désactive Jekyll (sinon les dossiers commençant par `_` sont filtrés) |
| `sitemap.xml` | 32 URL absolues (30 pages de contenu + 2 pages légales, `404.html` exclu) |
| `robots.txt` | `Sitemap:` absolu, exclusion de `/tools/`, `/dist/`, `/.github/`, blocage des crawlers IA |
| `.github/workflows/deploy.yml` | CI + publication de l'artefact `_site/` |

**Procédure exacte :**

1. Pousser la racine du projet sur la branche `main` d'un dépôt GitHub public.
2. Settings → Pages → *Source* = **GitHub Actions**.
3. Champ *Custom domain* = `gta-6.duckdns.org`, puis cocher **Enforce HTTPS**
   (certificat émis par GitHub après propagation DNS, jusqu'à 24 h).
4. Côté DuckDNS : enregistrements `A` vers `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153` ; `CNAME www` → `<compte>.github.io`.
5. Chaque push sur `main` déclenche `deploy.yml` : contrôle du YAML, des liens internes et de
   la politique d'assets, puis publication.

**Ce qui est publié et ce qui ne l'est pas.** L'étape `Prepare publishable site` du workflow
construit `_site/` avec `rsync` et exclut : `.git`, `.github`, `tools/`, `dist/`, `node_modules`,
`assets/images/_archives/`, `research_data.json`, `research_*.md`, `qa_report_s6.json`,
`state.json`, `workflow_master.yaml`, `design_system.md`, `package.json`, `netlify.toml`,
`vercel.json`. Volumétrie servie : 33 HTML, 7 CSS, 8 JS, 459 JPG, 12 MP3.

Netlify et Vercel restent possibles (`netlify.toml`, `vercel.json` fournis, sans étape de build),
mais le domaine et le `CNAME` ciblent GitHub Pages.

---

## 4. Recherche et données

`research_data.json` est la source de vérité (non publiée) :

- **683 faits** répartis en **21 sections**, **`source_url` sur 683/683** ;
- **386 sources** enregistrées (Rockstar, presse accréditée, forums, GitHub, Reddit, YouTube) ;
- par statut : 107 officiels, 306 presse confirmée, 68 communauté **archivés**, 27 en attente,
  12 estimations, 7 fuites non vérifiées ;
- **92 faits communautaires archivés** en S22 (`meta.archived_community_facts`) : ils restent
  traçables dans le corpus mais ne sont plus affichés sur le site ;
- `meta.publication` et `meta.editorial_policy` documentent les décisions de publication
  (domaine, licence, absence d'analytics, règle spoiler, non-affiliation) ;
- arbitrages documentés (contradictions tranchées, chiffres refusés, rumeurs écartées).

---

## 5. Traçabilité S0 → S22

| État | Objet | Résultat |
|---|---|---|
| S0 | INIT | cadre du projet, FSM, `package.json` |
| S1 | RESEARCH | corpus initial, contradictions arbitrées |
| S2 | DESIGN_SYSTEM | tokens, composants, accueil, 10 JPG / 10 MP3 |
| S3 | BUILD_CORE_PAGES | homepage définitive, recherche, 20 JPG / 12 MP3 |
| S4 | BUILD_CONTENT_PAGES | **20 pages de contenu en 7 groupes** (gate `CONTINUER` après chaque groupe) |
| S5 | INTERACTIVE_FEATURES | carte SVG 28 lieux, checklist `localStorage`, quiz 30 questions |
| S6 | QA_AND_POLISH | audit complet, 0 erreur, contrastes calculés, build minifié |
| S7 | FINAL_DELIVERY | README final, récapitulatif, structure |
| S8 | REVIEWS | levée d'embargo du 18/11 à 11:00 UTC : notes, horaires de déblocage |
| S9 | LAUNCH_NIGHT | nuit de lancement : première heure, anti-spoiler, technique mesurée |
| S10 | REAL_ASSETS | catalogues visuels réels (51 armes, 152 véhicules, 27 espèces), règle « une image = un emplacement » |
| S11 | POST_LAUNCH_RADIO | relevé d'écoute, radio à pied et podcasts, biens achetables |
| S12 | PUBLISH_READY | correctifs 18/11, mesures Digital Foundry, règle des trois poches |
| S13 | FINAL_PUBLISH | page « Le fil du lancement », page 404 réelle, sitemap complet |
| S14 | DEEP_MECHANICS | cinq chapitres et manquables, preuves policières, trophées manquables |
| S15 | PLAYER_FEEDBACK | retours de joueurs du premier jour, meilleures armes par rôle |
| S16 | SAFE_CODES | cinq codes de coffres et de portes, dépannage du soir de sortie |
| S17 | FINAL_POLISH | validation HTML des 32 pages, séquence « minuit », page stockage |
| S18 | SETTINGS | table de réglages console → télévision → jeu, visée et zone morte |
| S19 | DAY_MINUS_ONE | contre-jeu policier, cinq erreurs d'argent, vagues de correctifs |
| S20 | LAUNCH_DAY | ouverture mondiale heure par heure, retours de Nouvelle-Zélande, cloud Xbox One |
| S21 | DAY_ONE_PULSE | dépannage réel du jour J, mesures par machine, ce qui ne se règle pas |
| **S22** | **FINALIZE / PUBLICATION** | **domaine + HTTPS, SEO absolu, pages légales, suppression de l'anglais, purge du contenu communautaire, retrait des prix en euros, `robots.txt` durci** |

Détail horodaté : `state.json`. Définition des étapes : `workflow_master.yaml`.
| **S23** | **DAY_ONE_WATCH** | **veille du jour de sortie : firmware PS5 obligatoire, notes de correctifs, reconnaissance policière, receleurs, réflexes de terrain, liste de vérification** |
| **S24** | **NIGHT_ONE_MEASUREMENTS** | **mesures de la première nuit : résolutions et cadences par console, explication Rockstar du plafond à 30, panne PSN du 18/11, entretien** |
| **S25** | **LAUNCH_DAY_VERIFICATION** | **vérification du jour de sortie : aucun chiffre de ventes officiel, estimation Sensor Tower datée, astuces vérifiées des premières heures, direct 24 h et spoilers** |
| **S26** | **PUBLISH_PACKAGE** | **déplacement sans téléportation, vol de véhicules sans alarme, état vérifié au soir du 19, paquet `out/publish/` prêt à déployer** |
| **S27** | **PRE_LAUNCH_HARDENING** | **firmware PS5 obligatoire, aucun patch de lancement, argent du début et coffre, route de l'argent par chapitre, cartes open source, nettoyage du paquet** |
| **S28** | **PUBLICATION_AUDIT** | **audit SEO complet (canonical, sitemap, og:image, JSON-LD), correction publique des tailles de correctif, trouvailles du jour 1, `out/` exclu du workflow** |
| **S29** | **COMPLETION_TRUTH** | **seuils réels du 100 % (15/18 séries, 100/125 flamants, 300/397 cascades), méditations doublées, stand de tir, drones, écart trophées/100 %** |
| **S30** | **LAUNCH_NIGHT_VERIFICATION** | **panne PSN du soir de lancement et dépannage, 99 Metacritic, déclaration de Sam Houser, audience Twitch record** |
| **S31** | **PERF_AND_SETTINGS** | **mesures Digital Foundry par console, explication Rockstar des 30 fps, réglages (zone morte, HDCP, cache), règles de métier (fourrière, butin, point de contrôle)** |

Récit de la publication : `research_s22_addendum.md`. Veille du 19/11 : `research_s23_addendum.md`. Mesures de la première nuit : `research_s24_addendum.md`. Vérification du jour de sortie : `research_s25_addendum.md`.

---

## 6. Chiffres de la livraison

| | |
|---|---|
| Fichiers HTML | **33** : accueil, 28 sous-pages de contenu, 2 pages légales, page 404 |
| Pages indexables | **32** dans `sitemap.xml` (le 404 est exclu) |
| Faits / sources | 683 / 386, `source_url` 683/683 |
| Images publiées | **556 JPG** (546 utilisés dans les pages) : illustrations IA 1920×1080, visuels d'objets, espèces, cartes, lieux réels — crédits `assets/images/CREDITS.md` |
| Images archivées | 12 JPG dans `assets/images/_archives/`, **non publiés** (voir amendement S22 des crédits) |
| Audio | 12 MP3 originaux (playlist hors ligne, aucune voix off) |
| CSS / JS | 7 feuilles / 8 modules ES, aucun CDN, aucune police distante |
| Liens internes | 2 246 références, **0 cassée** |
| Audit QA | 33 pages, **0 erreur, 0 avertissement** |
| Formats interdits | 0 (aucun PNG, SVG, WebP, AVIF, WAV, ZIP, PDF) |
| Images réutilisées | **0** — contrôle bloquant `tools/check_images_unique.py` |
| Accessibilité | WCAG 2.2 AA : 2.4.11, 2.4.13, 2.5.7, 2.5.8, contrastes calculés |

---

## 7. Décisions de publication (S22)

| Sujet | Décision | Effet |
|---|---|---|
| Analytics | **aucun** | pas de mesure d'audience, pas de bannière de consentement |
| Licence | **tous droits réservés** | mention en pied de page des 33 pages + § Propriété des mentions légales |
| Langue | **français uniquement** | dossier `en/` supprimé, 66 entrées de nav retirées, `hreflang` = `fr` + `x-default` |
| Spoilers | **tout masqué** | blocs `data-spoiler-toggle` fermés par défaut sur chaque page sensible |
| Contenu communautaire | **retiré** | 13 sections supprimées, 24 rebadgées, 92 faits archivés dans le corpus |
| Prix | **euros retirés** | valeurs en USD conservées, marquées `data-verify-number` |
| Voix off | **non** | les 12 MP3 restent une playlist instrumentale |
| Contact | `gta-6@gmail.com` | adresse affichée dans les mentions légales, aucun formulaire |

**Procédure de retrait.** Toute demande de retrait (texte, visuel, marque) adressée à
`gta-6@gmail.com` est traitée sous 7 jours : retrait de la ressource, mise à jour du `sitemap.xml`,
puis republication. La procédure est décrite publiquement dans
`pages/legal/mentions-legales.html#signaler`.

---

## 8. Ce que ce guide refuse de faire

- Inventer des chiffres : nombre de missions, surface officielle de la carte, revenus
  d'entreprise, résolution Series S, mode 60 fps — **rien** de tout cela n'est affiché sans source.
- Publier un code de triche : Rockstar n'en a diffusé aucun au 19/11/2026.
- Présenter une fuite comme un fait : les six comtés, la liste de trophées non recoupée et les
  coordonnées d'easter eggs circulantes sont étiquetés `ESTIMATION` / `VÉRIFICATION` ou exclus.
- Reprendre du contenu communautaire non vérifiable : il a été retiré du site en S22.
- Prétendre qu'un audit automatisé remplace un test manuel avec lecteur d'écran.

---

## 9. Crédits

Illustrations : JPG originaux générés par IA + 4 visuels de lieux réels, inventaire complet dans
[`assets/images/CREDITS.md`](assets/images/CREDITS.md) (amendement S22 inclus).
Audio : MP3 originaux générés localement, libres de droits.
Sources textuelles : listées fait par fait dans `research_data.json` (`sources_registry`).

**Licence :** © 2026 direct — tous droits réservés. *Grand Theft Auto* et *GTA VI* sont des
marques de Take-Two Interactive. Aucune affiliation, aucun partenariat. Le guide est un projet
de fan non commercial ; les illustrations générées par IA ne représentent pas le jeu final.

---

## 10. Publier le site (GitHub Pages)

Le contenu exact à servir est prêt dans **`out/publish/`** (33 HTML, 7 CSS, 8 JS, 546 JPG,
12 MP3, `CNAME`, `.nojekyll`, `sitemap.xml`, `robots.txt`, `manifest.json`, `404.html`,
`SHA256SUMS.txt`). Aucun outil, aucun fichier de travail n'y figure. Procédure détaillée
et checklist de vérification : [`out/PUBLICATION.md`](out/PUBLICATION.md).

1. Pousser le dépôt (le workflow `.github/workflows/deploy.yml` publie déjà `_site/`).
   Variante sans Actions : copier le contenu de `out/publish/` à la racine de la branche publiée.
2. Settings → Pages → Source « GitHub Actions » (ou branche `main` / dossier `/root` en variante manuelle).
3. Domaine personnalisé : `gta-6.duckdns.org` déjà présent dans `CNAME`, cocher « Enforce HTTPS »
   après la propagation. DuckDNS : enregistrement A vers `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`.
4. Vérifier après publication : `/`, `/pages/news/`, `/sitemap.xml`, `/404.html`.

Contrôles avant envoi : `node tools/check_links.js` (0 cassé), `python3 tools/check_images_unique.py`
(510 = 510), `python3 tools/check_s2.py && python3 tools/check_s3.py && python3 tools/check_s4.py`,
`python3 tools/audit_s6.py`. Empreintes du paquet : `out/publish/SHA256SUMS.txt`.
