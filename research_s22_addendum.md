# Addendum S22 — FINALIZE / publication

Date : 19 novembre 2026 · Domaine : `https://gta-6.duckdns.org` · Hébergement : GitHub Pages

Aucun fait éditorial nouveau n'est ajouté en S22 : **604 faits / 313 sources** inchangés.
Cette étape ne touche qu'à la mise en publication (technique, juridique, indexation).

---

## 1. Décisions issues des réponses du formulaire

| Question | Réponse retenue | Conséquence dans le code |
|---|---|---|
| URL | `https://gta-6.duckdns.org` | `CNAME`, canonical/`og:url`/JSON-LD/sitemap absolus |
| Hébergement | GitHub Pages | `.nojekyll`, `deploy.yml` avec étape `Prepare publishable site` |
| Éditeur / contact | `direct` · `gta-6@gmail.com` | page Mentions légales, § Éditeur |
| Analytics | non | aucun script de mesure, aucune balise de consentement |
| Licence | tous droits réservés | mention de pied de page sur les 33 pages + § Propriété |
| Nom affiché | `direct` (on ne renomme rien) | marque conservée telle quelle partout |
| Version anglaise | supprimer | dossier `en/` supprimé, 66 entrées de nav retirées |
| Spoilers | tout masqué | chaque page sensible garde un bloc `data-spoiler-toggle` fermé par défaut |
| Communauté | retirer | 13 sections supprimées, 24 sections rebadgées PRESSE / OFFICIEL / VÉRIFICATION / OUTIL DU SITE |
| Prix en euros | retirer | plus aucun `€` ; valeurs en USD marquées `data-verify-number` |
| Visuels de lieux réels | conserver | 4 visuels `lieux/` conservés avec mention d'origine |
| Voix off | non | 12 MP3 restent une playlist musicale, aucune narration |

---

## 2. Ce qui a été modifié dans le site

### Indexation
- `canonical`, `og:url`, `twitter:image`, `og:image` en URL **absolues** sur les 33 pages.
- JSON-LD (`Article` + `BreadcrumbList`) réécrit avec des URL absolues sur 30 pages.
- `hreflang` : `fr` + `x-default` uniquement (plus de paire `fr`/`en`).
- `sitemap.xml` : **32 URL** = 30 pages de contenu + 2 pages légales ; `404.html` exclu
  (une page d'erreur ne s'indexe pas) ; `lastmod` 2026-11-19.
- `robots.txt` : `Sitemap:` absolu, exclusion de `/tools/`, `/dist/`, `/.github/`,
  et blocage explicite des robots d'entraînement (GPTBot, CCBot, Google-Extended,
  anthropic-ai, ClaudeBot, PerplexityBot).

### Juridique
- `pages/legal/mentions-legales.html` : éditeur, hébergeur (GitHub Pages + GitHub Inc.),
  propriété intellectuelle et marques, non-affiliation Rockstar / Take-Two, statut des
  illustrations générées par IA, avertissement sur l'exactitude, procédure de retrait.
- `pages/legal/confidentialite.html` : aucune collecte, aucun cookie, aucun analytics ;
  tableau des stockages locaux (`localStorage` : checklist, thème ; recherche en mémoire) ;
  journaux de connexion GitHub Pages ; droits et saisine CNIL ; date de révision.
- Pied de page « Mentions légales · Confidentialité · Contact » + « © 2026 direct — tous
  droits réservés » sur les 33 pages.

### Contenu
- **13 sections supprimées** (contenu communautaire, fuites non vérifiées, retours de joueurs) :
  `codes#coffres`, `vice-city#fuites`, `musique#fuites`, `musique#apres-lancement`,
  `secrets#nonverifie`, `online#rumeurs`, `police#agences`, `reviews#joueurs`,
  `reviews#lancement-notes`, `economie#erreurs`, `faq#depannage-jour-j`,
  `lancement#jour-un`, `quiz#culture`.
- **24 sections rebadgées** vers `PRESSE · 18/11`, `OFFICIEL`, `VÉRIFICATION`,
  `OUTIL DU SITE`. Plus aucune occurrence du badge `COMMUNAUTÉ` dans le HTML.
- `pages/outils/index.html` réécrite : plus aucune recension d'outils tiers, seulement les
  quatre outils maison (carte 28 lieux, checklist 80 défis, quiz 30 questions, recherche `/`).
- Prix en euros retirés ; les quatre éditions restent décrites en USD avec leur contenu.
- 92 faits communautaires archivés dans `research_data.json` (`meta.archived_community_facts`),
  jamais supprimés du corpus : ils restent traçables mais ne sont plus affichés.

---

## 3. Contrôles avant publication (tous verts au 19/11/2026)

```
python3 tools/check_s2.py            ✓ CP2 — design system
python3 tools/check_s3.py            ✓ CP3 — pages cœur, 0 format interdit
python3 tools/check_s4.py            ✓ CP4 — 29 pages de contenu, 268 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 2 246 références internes, 0 cassée
python3 tools/check_images_unique.py ✓ 459 images distinctes / 459 emplacements
python3 tools/build_s6.py            ✓ CSS 100 → 69 Ko, JS 94 → 81 Ko, 8/8 modules
node --check assets/js/*.js          ✓ 8/8
python3 -c "yaml.safe_load(...)"     ✓ workflow_master.yaml et deploy.yml valides
curl pages/legal/*.html              ✓ 200 / 200
grep COMMUNAUTÉ --include=*.html     ✓ 0 occurrence
grep <loc> sitemap.xml               ✓ 32
```

Les deux pages légales sont volontairement exemptées du contrôle `check_s4.py` (groupe
`S22_LEGAL`) : ce sont des pages de service, sans badges de statut ni galerie.

---

## 4. Mise en ligne — procédure exacte

1. **Dépôt** : pousser la racine du projet sur la branche `main` d'un dépôt GitHub public.
2. **Pages** : Settings → Pages → *Source* = **GitHub Actions**.
3. **Domaine** : champ *Custom domain* = `gta-6.duckdns.org`, puis cocher **Enforce HTTPS**
   (le certificat est émis par GitHub après propagation DNS, compter jusqu'à 24 h).
4. **DNS chez DuckDNS** : enregistrements `A` vers `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153` ; `CNAME www` → `<compte>.github.io`.
5. **`.nojekyll`** déjà présent : sans lui, GitHub filtrerait les dossiers commençant par `_`.
6. **Publication** : chaque push sur `main` déclenche `deploy.yml`, qui vérifie le YAML,
   les liens internes et la politique d'assets (JPG/MP3 uniquement), construit `_site/`
   (sans `tools/`, `dist/`, `research_data.json`, `state.json`, ni `assets/images/_archives/`)
   puis publie cet artefact.

**Volumétrie publiée** : 33 pages HTML, 7 CSS, 8 JS, 459 JPG, 12 MP3 — soit environ 120 Mo,
sous le plafond de 1 Go de GitHub Pages.

---

## 5. Ce qui reste volontairement ouvert

- **Aucun analytics** : la fréquentation n'est pas mesurable, c'est le prix de la décision A4.
- **Aucun formulaire de contact** : le seul canal est l'adresse `gta-6@gmail.com`, affichée
  dans les mentions légales (choix assumé, pas d'anti-spam côté site).
- **Spoilers** : la règle « tout masqué » est portée par les blocs `data-spoiler-toggle`
  des pages sensibles, pas par un mur d'avertissement global.
- **Mission 30 fps** : les valeurs de visée restent indicatives, badgées `PRESSE · 18/11`,
  en attendant un correctif ou une confirmation officielle.
