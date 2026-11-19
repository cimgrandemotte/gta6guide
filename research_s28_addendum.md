# Addendum S28 — vérification, correction de chiffres, trouvailles du jour 1

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **662 → 666 faits**, **362 → 368 sources**. Deux sections ajoutées,
10 illustrations JPG, 0 audio (décision C3 maintenue), **aucune archive ZIP**.

---

## 1. Une erreur de notre propre corpus, corrigée publiquement

La taille du premier correctif était arrondie du mauvais côté. Deux relevés indépendants
donnent :

| Version | Date | PS5 | Xbox Series X\|S |
|---|---|---|---|
| 01.002.000 | 13/11 | ≈ 1,07 Go | ≈ 2,18 Go |
| 01.002.001 | 16/11 | 602,5 Mo | ≈ 1,59 Go |

Une édition antérieure affirmait « ≈ 2,2 Go sur les deux consoles ». C'est faux, et la
correction est visible sur `pages/news#correctif-tailles` : le site dit ce qu'il avait écrit
de travers, au lieu de réécrire l'histoire en silence. Quatre endroits du HTML ont été corrigés
(page Lancement ×2, page News ×2).

Rappel maintenu : **aucune note de version publiée par Rockstar**, ni pour l'une ni pour l'autre.

## 2. Trouvailles des premières 24 heures (statut « trouvailles de joueurs »)

| Découverte | Détail | Source |
|---|---|---|
| L'oeuf de Pâques au sens propre | au sommet d'une tour de communications, ~7 min d'escalade ; un nid d'oeufs peints ; en lancer un déclenche une cinématique | IBTimes, Gamemapa |
| Bigfoot | silhouette près du lac Cottonmouth ; il faut courir vers elle et ouvrir le mode Photo | Gamemapa, VGTimes |
| Le crabe géant et le chien en jet-ski | deux clins d'oeil absurdes de la même journée | Gamemapa |
| La maison de Belville | identique à celle de la remasterisation de San Andreas (2021), plantes comprises : premier aperçu du jeu, deux ans avant | VGC |
| Deux casinos, un zoo, un cimetière | présents dans les fichiers, **non ouverts** : emplacements réservés, pas des secrets à débloquer | VGTimes |

Aucune de ces entrées n'est classée `official` : Rockstar n'a rien confirmé.

## 3. Vérifications techniques de publication (S28)

Contrôles qui n'existaient pas encore dans la batterie :

- **Canonical / og:url strictement égaux à l'URL publique** pour les 33 pages
  (l'accueil pointait vers `/index.html` au lieu de `/` — corrigé dans le HTML, le sitemap,
  les `hreflang` et le `@graph` JSON-LD, y compris les 30 fils d'Ariane qui désignaient la
  mauvaise URL d'accueil).
- **Sitemap = 32 URL, exactement l'ensemble des pages indexables** (ensemble identique, pas
  seulement un compte).
- **og:image : chaque URL absolue correspond à un fichier existant** — 0 manquante.
- **JSON-LD parsé sur les 33 pages** — 0 erreur.
- **479 balises `<img>` : 0 sans `alt`, 0 sans `width`/`height`, 0 dont les dimensions déclarées
  diffèrent du fichier ; 3 en `eager` pour le LCP, le reste en `lazy`.**
- **0 identifiant dupliqué, 0 `href="#"`, un seul `<h1>` par page.**
- **`out/` exclu du workflow GitHub Actions** : sans cette ligne, la CI aurait publié `_site/`
  *et* le paquet `out/publish/` en double (120 Mo dupliqués).
- **Aucun ZIP nulle part**, conforme à la consigne.

## 4. Sections publiées

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| Secrets | `#premieres-trouvailles` | oeuf de la tour, Bigfoot, crabe, chien, Belville, lieux fermés | SEC-33 → 35, FAQ-11 |
| News | `#correctif-tailles` | tailles réelles des deux correctifs + aveu de la correction | REL-34 |

## 5. Médias

10 JPG 1920×1080 q86 progressif, tous distincts, badgés **ILLUSTRATION IA** (dossier `jour1/`) :
ascension de la tour, nid d'oeufs peints, silhouette au bord du lac, crabe géant, chien en
jet-ski, maison de Belville, immeuble au bord de la baie, casino fermé, photographe dans les
herbes, lendemain de nuit blanche.

**Inventaire publié : 518 JPG, 518 emplacements, 0 réutilisation.**

## 6. Contrôles du 19/11/2026 (après S28)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 666 faits / 368 sources
python3 tools/check_s4.py            ✓ CP4 — 29 pages, 327 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 2 269 références internes, 0 cassée
python3 tools/check_images_unique.py ✓ 518 / 518
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
python3 tools/build_s6.py            ✓ CSS 100 → 69 Ko, JS 97 → 83 Ko, 8/8 modules
paquet out/publish                   ✓ 613 fichiers, 0 lien cassé, 0 ancre morte, 0 format interdit
```

## 7. Procédure de publication

Inchangée, décrite dans `out/PUBLICATION.md` : dépôt → GitHub Actions → `_site/` → domaine
`gta-6.duckdns.org` → HTTPS. **Aucune archive à décompresser** : soit le workflow publie depuis
le dépôt, soit on copie `out/publish/` tel quel.
