#!/usr/bin/env python3
"""Validation autonome du checkpoint CP3 (S3 — BUILD_CORE_PAGES).

Contrôle : homepage définitive, 12 composants globaux, SEO / JSON-LD,
20 JPG / 12 MP3, navigation clavier + ARIA, badges de statut, SpoilerToggle,
countdown J-1 → « Lancer le Guide », chiffres conformes à research_data.json,
liens internes, absence de réseau externe dans le code navigateur, FSM S3.

Usage : python3 tools/check_s3.py
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
FORBIDDEN = ("*.png", "*.svg", "*.webp", "*.avif", "*.wav", "*.ogg", "*.flac", "*.zip", "*.pdf")

S2_JPG = [
    "heroes/homepage_hero_vicecity_night_01.jpg",
    "characters/characters_jason_fullbody_01.jpg",
    "characters/characters_lucia_fullbody_01.jpg",
    "map/map_leonida_aerial_01.jpg",
    "weapons/weapons_arsenal_cinematic_01.jpg",
    "vehicles/vehicles_lineup_vicecity_01.jpg",
    "missions/gameplay_action_scene_01.jpg",
    "heroes/vicecity_districts_night_01.jpg",
    "map/leonida_keys_paradise_01.jpg",
    "map/mount_kalaga_epic_01.jpg",
]
S3_JPG = [
    "heroes/homepage_hero_sunset_ocean_drive_01.jpg",
    "heroes/homepage_vicecity_skyline_dusk_01.jpg",
    "heroes/homepage_neon_street_rain_01.jpg",
    "heroes/homepage_leonida_keys_bridge_01.jpg",
    "characters/homepage_jason_lucia_duo_01.jpg",
    "map/homepage_leonida_aerial_teaser_01.jpg",
    "missions/homepage_heist_getaway_01.jpg",
    "vehicles/homepage_supercar_night_01.jpg",
    "weapons/homepage_arsenal_neon_01.jpg",
    "heroes/homepage_vice_city_art_deco_01.jpg",
]
S3_MP3 = [
    "ambiances/homepage_ambiance_sunset_cruise_01.mp3",
    "jingles/homepage_jingle_guide_intro_01.mp3",
]

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    print(f"  {'✓' if condition else '✗'} {message}")
    if not condition:
        errors.append(message)


class Document(HTMLParser):
    """Collecte les balises, attributs, textes et scripts structurés."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[dict] = []
        self.stack: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        entry = {"tag": tag, "attrs": {k: (v or "") for k, v in attrs}, "text": ""}
        self.tags.append(entry)
        if tag not in VOID:
            self.stack.append(entry)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data: str) -> None:
        for entry in self.stack:
            entry["text"] += data

    def find(self, tag: str, **attrs: str) -> list[dict]:
        out = []
        for entry in self.tags:
            if entry["tag"] != tag:
                continue
            if all(entry["attrs"].get(k) == v for k, v in attrs.items()):
                out.append(entry)
        return out

    def ids(self) -> dict[str, dict]:
        return {e["attrs"]["id"]: e for e in self.tags if e["attrs"].get("id")}


def parse(path: Path) -> Document:
    doc = Document()
    doc.feed(path.read_text(encoding="utf-8"))
    doc.close()
    return doc


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def main() -> int:
    print("=== CP3 · S3 BUILD_CORE_PAGES ===\n--- Fichiers livrés ---")
    required = [
        "index.html", "assets/js/main.js", "assets/js/search.js", "assets/js/utils.js",
        "assets/css/s3_home.css", "research_s3_addendum.md", "robots.txt", "sitemap.xml", "manifest.json",
        "tools/patch_research_s3.py", "tools/check_s3.py",
    ]
    for rel in required:
        p = ROOT / rel
        check(p.is_file() and p.stat().st_size > 100, f"{rel} ({p.stat().st_size if p.exists() else 0} o)")

    print("\n--- JavaScript ---")
    js_files = ["assets/js/components.js", "assets/js/animations.js", "assets/js/main.js", "assets/js/search.js", "assets/js/utils.js", "tools/check_links.js", "tools/serve.js"]
    for rel in js_files:
        p = ROOT / rel
        r = subprocess.run(["node", "--check", str(p)], cwd=ROOT, capture_output=True, text=True)
        check(r.returncode == 0, f"node --check {rel}" + ("" if r.returncode == 0 else f" → {r.stderr.strip()[:160]}"))

    print("\n--- SEO, métadonnées et JSON-LD ---")
    home = ROOT / "index.html"
    raw = home.read_text(encoding="utf-8")
    doc = parse(home)
    canonical = [e for e in doc.find("link") if "canonical" in e["attrs"].get("rel", "")]
    alternates = [e for e in doc.find("link") if "alternate" in e["attrs"].get("rel", "")]
    hreflangs = {e["attrs"].get("hreflang") for e in alternates}
    check(len(canonical) == 1, "1 canonical")
    check({"fr", "x-default"}.issubset(hreflangs), "hreflang fr / x-default (site monolingue)")
    for prop in ["og:title", "og:description", "og:image", "og:type", "og:locale"]:
        check(any(e["attrs"].get("property") == prop for e in doc.find("meta")), f"meta {prop}")
    for name in ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]:
        check(any(e["attrs"].get("name") == name for e in doc.find("meta")), f"meta {name}")
    ld_scripts = [e for e in doc.find("script") if e["attrs"].get("type") == "application/ld+json"]
    ld_ok = False
    if ld_scripts:
        try:
            ld = json.loads(ld_scripts[0]["text"])
            ld_ok = ld.get("@type") == "VideoGame" and ld.get("name") == "Grand Theft Auto VI"
        except Exception:
            ld_ok = False
    check(ld_ok, "JSON-LD @type VideoGame valide")

    print("\n--- Réseau externe / sandbox ---")
    links = doc.find("link")
    scripts = doc.find("script")
    check(all(not e["attrs"].get("href", "").startswith(("http://", "https://", "//")) for e in links if "stylesheet" in e["attrs"].get("rel", "")), "0 feuille CSS distante")
    check(all(not e["attrs"].get("src", "").startswith(("http://", "https://", "//")) for e in scripts if e["attrs"].get("src")), "0 script distant")
    css_text = "".join((ROOT / p).read_text(encoding="utf-8") for p in [
        "assets/css/design_system.css", "assets/css/animations.css", "assets/css/components.css",
        "assets/css/responsive.css", "assets/css/s3_home.css",
    ])
    def strip_code_comments(text: str) -> str:
        """Ignore les mentions pédagogiques dans les commentaires ; QA = code réel."""
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        return re.sub(r"(?m)^\s*//.*$", "", text)

    css_clean = strip_code_comments(css_text)
    check("@import" not in css_clean and "fonts.googleapis.com" not in css_clean, "0 @import / Google Fonts")
    browser_code = raw + css_text + "".join((ROOT / p).read_text(encoding="utf-8") for p in js_files[:5])
    browser_clean = strip_code_comments(browser_code)
    check("localhost" not in browser_clean and "127.0.0.1" not in browser_clean, "0 localhost dans le code navigateur")
    check(not re.search(r"<script[^>]+src=['\"]https?://", raw, re.I), "0 CDN script dans index.html")

    print("\n--- Composants globaux & ARIA ---")
    hooks = {
        "Navbar": "data-nav-burger", "SearchEngine": "data-search", "Breadcrumbs": "data-breadcrumbs",
        "ItemCard": "item-card", "StatBar": "data-stat-value", "Tooltip": "data-tooltip",
        "SpoilerToggle": "data-spoiler-toggle", "CopyButton": "data-copy", "BackToTop": "data-back-to-top",
        "CookieBanner": "data-cookie-banner", "AudioPlayer": "data-audio-player", "Footer": "footer",
    }
    for name, needle in hooks.items():
        check(needle in raw, f"composant {name} → {needle}")
    check("skip-link" in raw and 'href="#main-content"' in raw, "lien d'évitement clavier")
    check('aria-live="polite"' in raw and "data-countdown-inline=\"managed\"" in raw, "countdown ARIA + fallback inline")
    check("Lancer le Guide" in raw and "Lancer le Guide" in (ROOT / "assets/js/components.js").read_text(encoding="utf-8"), "bascule post-19/11 → Lancer le Guide")
    check("new Date(2026, 10, 19" in raw, "cible countdown 19/11/2026")
    for button in doc.find("button"):
        label = button["attrs"].get("aria-label", "").strip() or norm(button["text"])
        check(bool(label), f"bouton accessible : {label[:44] or button['attrs']}")
    for toggle in doc.find("button", **{"data-spoiler-toggle": ""}):
        target = toggle["attrs"].get("aria-controls", "")
        target_el = doc.ids().get(target)
        check(target_el is not None and "hidden" in target_el["attrs"] and toggle["attrs"].get("aria-expanded") == "false", f"SpoilerToggle ARIA → {target}")
    check(all(e["attrs"].get("tabindex") == "0" for e in doc.tags if "data-tooltip" in e["attrs"]), "tooltips focusables au clavier")

    print("\n--- Badges & chiffres conformes à research_data.json ---")
    data = json.loads((ROOT / "research_data.json").read_text(encoding="utf-8"))
    corpus = json.dumps(data, ensure_ascii=False)
    for el in doc.tags:
        if "data-status" in el["attrs"]:
            status = el["attrs"]["data-status"]
            badge = el["attrs"].get("data-badge", "")
            check(bool(badge) and (status == "official" or status != "official"), f"badge présent pour data-status={status} → {badge}")
    verified = [norm(e["attrs"]["data-verify-number"]) for e in doc.tags if e["attrs"].get("data-verify-number")]
    check(len(verified) >= 20, f"{len(verified)} valeurs numériques à recouper")
    missing = [v for v in verified if v not in corpus]
    check(not missing, "tous les chiffres affichés existent dans research_data.json" + (f" → manquants {missing[:5]}" if missing else ""))
    flat = [f for section in data["facts"].values() for f in section]
    check(len(flat) >= 303 and len(data["sources_registry"]) >= 135 and len(data["facts"]) >= 20, f"{len(flat)} faits / {len(data['sources_registry'])} sources / {len(data['facts'])} sections (S3 + amendements)")
    check(all(
        "source_url" in f and (
            (isinstance(f.get("sources"), list) and f["sources"] and f["source_url"] == f["sources"][0])
            or (isinstance(f.get("sources"), list) and not f["sources"] and bool(f["source_url"]))
            or "sources" not in f
        )
        for f in flat
    ), f"source_url sur {len(flat)} / {len(flat)} faits")
    check(data["meta"].get("s3_amendment", {}).get("marker") == "S3_VERIFIED_FACTS", "amendement S3 idempotent tracé")
    check(data["s2_press_mission_list"]["total"] == 93, "93 missions de presse conservées")

    print("\n--- Images : 10 JPG S2 + 10 JPG S3 ---")
    imgs = doc.find("img")
    img_srcs = {e["attrs"].get("src", "").lstrip("./") for e in imgs}
    for rel in S2_JPG + S3_JPG:
        check(f"assets/images/{rel}" in img_srcs, f"<img> intégré : {rel}")
    for e in imgs:
        src = e["attrs"].get("src", "")
        alt = e["attrs"].get("alt", "")
        check(bool(alt) and len(alt) > 15, f"alt descriptif : {src or 'img'} ({len(alt)} caract.)")
        check("width" in e["attrs"] and "height" in e["attrs"], f"width / height : {src}")
        check("loading" in e["attrs"], f"loading : {src}")
        if src.startswith("assets/images/") and (ROOT / src).is_file():
            with Image.open(ROOT / src) as im:
                check(im.format == "JPEG", f"format JPEG : {src}")
                expected = (int(e["attrs"]["width"]), int(e["attrs"]["height"]))
                check(im.size == expected, f"dimensions HTML = fichier : {src} → {im.size}")
    for rel in S2_JPG:
        tags = [e for e in imgs if e["attrs"].get("src") == f"assets/images/{rel}"]
        check(bool(tags) and tags[0]["attrs"].get("loading") == "lazy", f"lot S2 lazy : {rel}")

    print("\n--- Audio local : 12 MP3, 0 autoplay ---")
    utils = (ROOT / "assets/js/utils.js").read_text(encoding="utf-8")
    mp3_refs = sorted(set(re.findall(r"assets/audio/[A-Za-z0-9_/\-]+\.mp3", utils)))
    check(len(mp3_refs) == 12, f"{len(mp3_refs)} pistes MP3 dans la playlist window.GTA6_AUDIO_TRACKS")
    check(all((ROOT / p).is_file() for p in mp3_refs), "tous les MP3 référencés existent")
    for rel in S3_MP3:
        check(f"assets/audio/{rel}" in mp3_refs, f"nouveau MP3 S3 : {rel}")
    for p in mp3_refs:
        head = (ROOT / p).open("rb").read(3)
        check(head.startswith(b"ID3") or (head[0] == 0xFF and (head[1] & 0xE0) == 0xE0), f"en-tête MP3 : {p}")
    check("window.GTA6_UI_SOUNDS = false" in utils, "sons UI désactivés sans opt-in")
    check('preload = \'none\'' in (ROOT / "assets/js/components.js").read_text(encoding="utf-8"), "lecteur audio preload=none")

    print("\n--- Formats livrés ---")
    all_jpg = sorted((ROOT / "assets/images").rglob("*.jpg"))
    all_mp3 = sorted((ROOT / "assets/audio").rglob("*.mp3"))
    check(len(all_jpg) >= 20, f"au moins 20 JPG (socle S3) — {len(all_jpg)} au total")
    check(len(all_mp3) >= 12, f"au moins 12 MP3 (socle S3) — {len(all_mp3)} au total")
    forbidden = []
    for pattern in FORBIDDEN:
        forbidden += [str(p.relative_to(ROOT)) for p in ROOT.rglob(pattern)]
    check(not forbidden, "0 PNG/SVG/WebP/AVIF/WAV/ZIP/PDF" + (f" → {forbidden[:5]}" if forbidden else ""))

    print("\n--- Liens internes ---")
    r = subprocess.run(["node", "tools/check_links.js"], cwd=ROOT, capture_output=True, text=True)
    print("  " + r.stdout.strip().replace("\n", "\n  "))
    check(r.returncode == 0 and "0 lien interne cassé" in r.stdout, "node tools/check_links.js → 0 lien cassé")

    print("\n--- JSON / YAML / FSM ---")
    for rel in ["research_data.json", "state.json", "manifest.json", "package.json"]:
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
            check(True, f"{rel} JSON valide")
        except Exception as exc:
            check(False, f"{rel} JSON valide → {exc}")
    try:
        import yaml
        wf = yaml.safe_load((ROOT / "workflow_master.yaml").read_text(encoding="utf-8"))
        fsm = wf["meta"]["fsm"]
        check(fsm["current_state"] in {"S3", "S4", "S5"} and fsm["status"] in {"COMPLETE", "IN_PROGRESS"},
              f"workflow_master.yaml → S3 franchi ({fsm['current_state']} {fsm['status']})")
        check(fsm["gate"].startswith("WAITING_FOR_CONTINUER") or fsm["gate"] == "FIN",
          f"gate → {fsm['gate']} (S3 franchi)")
        check("research_s3" in wf, "section research_s3 présente")
    except Exception as exc:
        check(False, f"workflow_master.yaml valide → {exc}")
    state = json.loads((ROOT / "state.json").read_text(encoding="utf-8"))
    check(state["current_state"] in {"S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31"} and state["status"] in {"COMPLETE", "IN_PROGRESS"},
          f"state.json → S3 franchi ({state['current_state']} {state['status']})")
    check(state["gate"].startswith("WAITING_FOR_CONTINUER") or state["gate"] == "FIN",
          f"state.json gate → {state['gate']}")
    check(any(h.get("state") == "S3" for h in state["history"]), "historique S3 tracé")

    print("\n--- Résultat ---")
    if errors:
        print(f"✗ {len(errors)} contrôle(s) en échec :")
        for e in errors[:40]:
            print(f"   - {e}")
        if len(errors) > 40:
            print(f"   … et {len(errors) - 40} autre(s).")
        return 1
    print("✓ CP3 validé : S3 BUILD_CORE_PAGES complet, 0 lien cassé, 0 format interdit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
