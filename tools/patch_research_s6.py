#!/usr/bin/env python3
"""Amendement recherche S6 — QA_AND_POLISH.

Marqueur `s6_amendment.marker == "S6_VERIFIED_FACTS"`. Idempotent.

Deux surfaces :
  • les seuils publics utilisés par l'audit (Core Web Vitals 2026, WCAG 2.2 AA) ;
  • l'état réel du jeu la veille du lancement (patchs 01.002.000 et 01.002.001),
    utile pour la page QA et pour la FAQ technique déjà publiée.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research_data.json"
MARKER = "S6_VERIFIED_FACTS"

SOURCES = {
    "webdev_cwv": {
        "title": "Core Web Vitals thresholds — LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1",
        "publisher": "web.dev (Google), synthèses 2026",
        "url": "https://web.dev/articles/vitals",
        "date": "2026-10-01",
        "kind": "référentiel public",
        "status": "official",
    },
    "wcag22_quickref": {
        "title": "WCAG 2.2 — Understanding SC 2.4.11, 2.4.13, 2.5.7, 2.5.8",
        "publisher": "W3C / WebAIM",
        "url": "https://webaim.org/blog/wcag-2-2-overview-and-feedback/",
        "date": "2026-08-31",
        "kind": "référentiel public",
        "status": "official",
    },
    "reddit_patch_1002": {
        "title": "GTA VI — Update Version 1.002 available (1 GB) (r/PS5)",
        "publisher": "Reddit · r/PS5",
        "url": "https://www.reddit.com/r/PS5/comments/1xv60mc/gta_vi_update_version_1002_available_1_gb/",
        "date": "2026-11-13",
        "kind": "forum",
        "status": "community",
    },
    "reddit_patch_1002001": {
        "title": "GTA 6 — Update 01.002.001 available, 602 MB, trois vagues (r/PS5)",
        "publisher": "Reddit · r/PS5",
        "url": "https://www.reddit.com/r/PS5/comments/1xxlyc2/gta_6_update_01002001_available_33_of_users_now/",
        "date": "2026-11-16",
        "kind": "forum",
        "status": "community",
    },
    "playstationlifestyle_patch": {
        "title": "GTA 6 Is Already Receiving PS5 Patches Ahead of Its Big Launch",
        "publisher": "PlayStation LifeStyle",
        "url": "https://www.playstationlifestyle.net/2026/11/13/gta-6-ps5-patches-before-launch",
        "date": "2026-11-13",
        "kind": "presse",
        "status": "press_confirmed",
    },
    "ign_day_one_patch": {
        "title": "GTA 6 Gets Another Day One Patch, and It's 1GB Bigger on Xbox",
        "publisher": "IGN",
        "url": "https://za.ign.com/grand-theft-auto-vi/245644/gta-6-gets-another-day-one-patch-and-its-1gb-bigger-on-xbox",
        "date": "2026-11-16",
        "kind": "presse",
        "status": "press_confirmed",
    },
}

FACTS = {
    "press_reviews": [
        {
            "id": "QA-XX",
            "status": "official",
            "text": "Seuils Core Web Vitals 2026 : LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1, évalués au 75e percentile des visites réelles, séparément sur mobile et sur ordinateur. Une page « passe » si les trois métriques sont au vert pour 75 % des visites.",
            "source_url": "https://web.dev/articles/vitals",
            "source_label": "web.dev (Google)",
        },
        {
            "id": "QA-XX",
            "status": "official",
            "text": "WCAG 2.2 AA ajoute quatre critères structurants pour ce projet : 2.4.11 (l'élément focalisé ne doit pas être masqué par un en-tête collant), 2.4.13 (indicateur de focus d'au moins 2 px avec contraste 3:1), 2.5.7 (toute action par glissement doit avoir une alternative au clic) et 2.5.8 (cible tactile ≥ 24 × 24 px CSS).",
            "source_url": "https://webaim.org/blog/wcag-2-2-overview-and-feedback/",
            "source_label": "W3C / WebAIM",
        },
        {
            "id": "QA-XX",
            "status": "official",
            "text": "Contraste minimal AA : 4,5:1 pour le texte normal, 3:1 pour le grand texte (≥ 24 px, ou ≥ 18,66 px en gras) et pour les éléments d'interface non textuels.",
            "source_url": "https://webaim.org/blog/wcag-2-2-overview-and-feedback/",
            "source_label": "W3C / WebAIM",
        },
    ],
    "release_and_platforms": [
        {
            "id": "REL-XX",
            "status": "press_confirmed",
            "text": "Deux mises à jour sont sorties avant même le lancement : 01.002.000 (≈ 1 Go) le 13 novembre, puis 01.002.001 le 16 novembre (602,5 Mo sur PS5, environ 1,59 Go sur Xbox Series X|S selon des relevés non confirmés par Rockstar). Aucune note de patch n'a été publiée.",
            "source_url": "https://za.ign.com/grand-theft-auto-vi/245644/gta-6-gets-another-day-one-patch-and-its-1gb-bigger-on-xbox",
            "source_label": "IGN / PlayStation LifeStyle",
        },
        {
            "id": "REL-XX",
            "status": "community",
            "text": "Le déploiement du patch 01.002.001 s'est fait par vagues : environ un tiers des joueurs d'abord, le reste douze heures plus tard, puis l'ensemble en vingt-quatre heures. Conséquence pratique : deux joueurs avec la même version de préchargement peuvent ne pas avoir le même numéro de build.",
            "source_url": "https://www.reddit.com/r/PS5/comments/1xxlyc2/gta_6_update_01002001_available_33_of_users_now/",
            "source_label": "Reddit r/PS5 (relevés de déploiement)",
        },
        {
            "id": "REL-XX",
            "status": "press_confirmed",
            "text": "Aucun changement de fréquence d'images n'est attaché à ces patchs : la cible reste 30 fps sur toutes les consoles. Les messages communautaires qui annoncent « le patch 60 fps » sont des plaisanteries de forum, pas des informations.",
            "source_url": "https://www.playstationlifestyle.net/2026/11/13/gta-6-ps5-patches-before-launch",
            "source_label": "PlayStation LifeStyle",
        },
    ],
}


def _renumber(data: dict) -> None:
    facts = data.get("facts", {})
    prefix = {"press_reviews": "QA", "release_and_platforms": "REL"}
    for section, items in FACTS.items():
        used = set()
        for f in facts.get(section, []):
            m = re.match(r"^([A-Z]+)-(\d+)$", str(f.get("id", "")))
            if m:
                used.add(int(m.group(2)))
        nxt = max(used) + 1 if used else 1
        for item in items:
            item["id"] = f"{prefix[section]}-{nxt:02d}"
            nxt += 1


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("s6_amendment", {}).get("marker") == MARKER:
        print("research_data.json : déjà patché en S6 — aucune duplication.")
        return

    _renumber(data)
    sources = data.setdefault("sources_registry", {})
    added_src = 0
    for k, v in SOURCES.items():
        if k not in sources:
            sources[k] = v
            added_src += 1

    facts = data.setdefault("facts", {})
    added = 0
    for section, items in FACTS.items():
        bucket = facts.setdefault(section, [])
        ids = {f.get("id") for f in bucket}
        for item in items:
            if item["id"] in ids:
                continue
            bucket.append({
                "id": item["id"],
                "status": item["status"],
                "fact": item["text"],
                "source_url": item["source_url"],
                "source_label": item["source_label"],
                "added_in": "S6",
            })
            added += 1

    data["s6_amendment"] = {
        "marker": MARKER,
        "at": "2026-11-18",
        "facts_added": added,
        "sources_added": added_src,
        "ids": {s: [f["id"] for f in items] for s, items in FACTS.items()},
        "targets": {
            "lcp_s": 2.5,
            "inp_ms": 200,
            "cls": 0.1,
            "contrast_text": 4.5,
            "target_size_px": 24,
        },
    }
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in facts.values())
    print(f"Amendement S6 appliqué : +{added} faits, +{added_src} sources, {total} faits, {len(sources)} sources.")


if __name__ == "__main__":
    main()
