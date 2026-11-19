# Crédits audio — lot AUD001–AUD010 (S2)

**10 fichiers, 10 MP3, 0 WAV / 0 OGG / 0 FLAC / 0 ZIP / 0 PDF.**
Signaux **100 % originaux**, synthétisés en Python (NumPy + `lameenc`) par
`tools/make_audio.py` : nappes, impulsions, bruit filtré, enveloppes ADSR. **Aucun sample sous
licence, aucune musique de GTA, aucune piste Rockstar, aucun enregistrement de moteur réel,
aucun fichier audio officiel.** Ce ne sont pas des thèmes officiels de Jason / Lucia ni la bande-son
de GTA VI : ce sont des ambiances de fan guide non officiel.

| # | Fichier | Durée / type | Usage prévu |
|---|---|---|---|
| 01 | `ambiances/homepage_ambiance_vicecity_night_01.mp3` | nappe longue | Ambiance d'accueil, lecture via le lecteur flottant (jamais en autoplay imposé). |
| 02 | `ui/homepage_ui_hover_01.mp3` | impulsion courte | Survol des boutons / cartes (armé après 1re interaction). |
| 03 | `ui/homepage_ui_click_01.mp3` | clic sec | Validation, navigation, CTA. |
| 04 | `ui/homepage_ui_transition_01.mp3` | whoosh | Changement de section / ouverture de drawer. |
| 05 | `jingles/characters_jason_theme_01.mp3` | motif synthétique | Fiche Jason — **jingles originaux, pas un thème officiel**. |
| 06 | `jingles/characters_lucia_theme_01.mp3` | motif synthétique | Fiche Lucia — **jingles originaux, pas un thème officiel**. |
| 07 | `ambiances/map_leonida_ambiance_01.mp3` | nappe longue | Page Carte / Leonida, S5 Leaflet. |
| 08 | `ui/weapons_equip_sound_01.mp3` | mécanisme synthétique | Filtres / fiches armes. |
| 09 | `ambiances/vehicles_engine_v8_01.mp3` | grondement filtré | Fiches véhicules — **simulation sonore, pas un moteur enregistré**. |
| 10 | `ui/quiz_correct_answer_01.mp3` | arpège court | Bonne réponse au quiz (P19 / S5). |

**Intégration :** `assets/js/components.js → initAudioPlayer()` référence exactement ces 10 MP3,
avec `preload="none"`, contrôle explicite de lecture, volume, playlist et respect de la politique
autoplay des navigateurs. `GTA6_UI_SOUNDS` doit être activé explicitement en S3 ; les sons UI ne
démarrent jamais sans interaction utilisateur.

**Légal :** fan guide non officiel, aucune affiliation Rockstar Games / Take-Two Interactive.
Les vraies informations soundtrack/radio (Justice, 6 stations, album 34 titres) sont dans
`research_data.json` avec leurs sources ; elles ne sont PAS reproduites dans ces fichiers audio.


---

## LOT S3 — AUD011–AUD012

**2 nouveaux fichiers, 2 MP3, 0 WAV / 0 OGG / 0 FLAC / 0 ZIP / 0 PDF.**
Signaux **100 % originaux** synthétisés par `tools/make_audio_s3.py` (NumPy + `lameenc`),
qui réutilise les générateurs de `tools/make_audio.py`. Aucun sample sous licence, aucune
musique de GTA, aucune piste Rockstar, aucun enregistrement réel.

| # | Fichier | Type | Usage |
|---|---|---|---|
| 011 | `ambiances/homepage_ambiance_sunset_cruise_01.mp3` | nappe chaude | Première piste du lecteur flottant S3, ambiance de croisière au coucher de soleil. |
| 012 | `jingles/homepage_jingle_guide_intro_01.mp3` | court jingle | Ouverture optionnelle du guide, jamais en autoplay. |

**Intégration S3 :** `assets/js/utils.js → window.GTA6_AUDIO_TRACKS` expose les 12 MP3
locaux (lot S2 + lot S3) avec des URL relatives compatibles `index.html` et
`en/index.html`. `components.js → initAudioPlayer()` garde `preload="none"`, une
playlist clavier, un volume ARIA et l'absence de lecture automatique.
