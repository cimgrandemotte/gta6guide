# Addendum S30 — soirée de lancement : réseau, notes, déclaration

Date : 19 novembre 2026 · Site : `https://gta-6.duckdns.org`
Corpus : **671 → 678 faits**, **373 → 380 sources**. Deux sections ajoutées,
9 illustrations JPG, 0 audio.

---

## 1. Le premier obstacle n'était pas Rockstar

Le soir du déblocage, ce qui a bloqué les joueurs est le **PlayStation Network**, pas le jeu —
qui est un jeu solo, sans serveur Rockstar à mettre en cause.

| Élément | Détail daté |
|---|---|
| Panne PSN | ~45 minutes le 18/11 vers 18 h (Royaume-Uni) |
| Pic de signalements | ~10 000 aux États-Unis à 7 h 05 GMT le 19/11 |
| Codes relevés | `WS-116449-5` (« service under maintenance »), « services Sony occupés », « trop de tentatives de connexion » |
| Cause | non communiquée par Sony ; **aucun lien officiel avec le jeu** |

Dépannage utile, dans l'ordre : page d'état PlayStation → firmware PS5 **26.07-14.23.00** →
redémarrage → attente. Côté Xbox, le message « problème réseau temporaire » a laissé un joueur
entrer via l'**option hors ligne** de l'écran.

**Rapports non confirmés, signalés comme tels** : PS5 qui s'éteint quelques secondes après le
lancement, PS5 Pro qui plante dans la mission d'ouverture, pop-in et voitures qui disparaissent,
audio haché sur Series X. Aucune correction officielle ; reconstruire la base de données n'a pas
aidé le joueur qui l'a tenté.

Deux chiffres d'espace disque qui ne concordent pas : **212 Go** (Rockstar) contre **225,3 Go**
(fiche Microsoft).

## 2. Le record de notation, et ce qu'il ne dit pas

- **99 sur Metacritic** (PS5), sur 147 critiques toutes positives, quelques heures après la levée
  de l'embargo le 18/11 à 6 h (heure de l'Est). Seul *Ocarina of Time* (1998) avait atteint 99.
- **Déclaration rare de Sam Houser** (président et cofondateur) à GamesRadar+ : les jeux
  « pouvaient atteindre la même distinction que toutes les autres formes de narration », et
  « nous espérons que vous vous amuserez ».
- **Ce qu'elle ne dit pas** : ni version PC, ni successeur de GTA Online, ni plan de contenu.
  La formule « de nombreuses années » est une intention, pas une feuille de route.
- Audience du soir : **plus de 2,5 millions** de spectateurs Twitch une demi-heure après le
  déblocage, pic rapporté à **3,3 millions** — record pour un jeu solo. Une audience n'est pas
  une preuve de contenu.

## 3. Sections publiées

| Page | Ancre | Contenu | Faits |
|---|---|---|---|
| News | `#soir-de-sortie` | panne PSN datée, table de dépannage, rapports non confirmés, espace disque, audience | REL-36 → 39, CMT-35 |
| Reviews | `#record-99` | 99 Metacritic, déclaration Houser, ce qu'elle ne dit pas, ce qui reste en attente | REV-28, REV-29 |

## 4. Médias

9 JPG 1920×1080 q86 progressif, tous distincts (`soir-lancement/`) : salon bondé, écran
d'erreur, macro de code, manette devant écran noir, bureau de streamer, premières minutes sous
la pluie, file de téléchargement, aube après la nuit, bureau de rédaction.

**Inventaire publié : 537 JPG, 537 emplacements, 0 réutilisation.**

## 5. Contrôles du 19/11/2026 (après S30)

```
python3 tools/check_s2.py            ✓ CP2
python3 tools/check_s3.py            ✓ CP3 — 678 faits / 380 sources
python3 tools/check_s4.py            ✓ CP4 — 29 pages, 346 JPG contrôlés
python3 tools/audit_s6.py            ✓ 33 pages, 0 erreur / 0 avertissement
node tools/check_links.js            ✓ 0 référence interne cassée
python3 tools/check_images_unique.py ✓ 537 / 537
python3 /tmp/nesting.py              ✓ 32 pages, 0 erreur
python3 tools/build_s6.py            ✓ 8/8 modules
```
