#!/usr/bin/env python3
"""Validation S4 — BUILD_CONTENT_PAGES (par groupe).

Contrôle les pages produites, groupe par groupe, avec les mêmes exigences que
CP3 : HTML valide, SEO complet, fil d'Ariane statique, images JPG avec
alt/width/height/loading, badges de statut, SpoilerToggle, liens internes,
absence de réseau externe et chiffres conformes à research_data.json.

Usage :
    python3 tools/check_s4.py            # tous les groupes disponibles
    python3 tools/check_s4.py --group G1 # groupe précis
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = (".png", ".svg", ".webp", ".avif", ".wav", ".ogg", ".flac", ".zip", ".pdf")

GROUPS = {
    "G1": [
        "pages/histoire/index.html",
        "pages/histoire/synopsis.html",
        "pages/histoire/missions.html",
    ],
    "G2": [
        "pages/personnages/index.html",
        "pages/personnages/lucia.html",
        "pages/personnages/secondaires.html",
    ],
    "G3": [
        "pages/carte/vice-city.html",
        "pages/armes/index.html",
        "pages/vehicules/index.html",
    ],
    "G4": [
        "pages/police/index.html",
        "pages/economie/index.html",
        "pages/activites/index.html",
    ],
    "G5": [
        "pages/musique/index.html",
        "pages/online/index.html",
        "pages/codes/index.html",
    ],
    "G6": [
        "pages/trophees/index.html",
        "pages/secrets/index.html",
        "pages/tips/index.html",
    ],
    "G7": [
        "pages/outils/index.html",
        "pages/divers/index.html",
        "pages/faq/index.html",
    ],
    "S5": [
        "pages/carte/index.html",
        "pages/collectibles/index.html",
        "pages/quiz/index.html",
    ],
    "S6": [
        "pages/qa/index.html",
    ],
    "S7": [
        "pages/final/index.html",
    ],
    "S8": [
        "pages/reviews/index.html",
    ],
    "S9": [
        "pages/lancement/index.html",
    ],
    "S12": [
        "pages/news/index.html",
    ],
    # S22 : les deux pages légales sont de la publication, pas du contenu éditorial —
    # elles n'ont ni badges de statut ni galerie, on ne les soumet donc pas à check_page().
    "S22_LEGAL": [
        "pages/legal/mentions-legales.html",
        "pages/legal/confidentialite.html",
    ],
}

errors: list[str] = []


def check(cond: bool, message: str) -> None:
    print(f"  {'✓' if cond else '✗'} {message}")
    if not cond:
        errors.append(message)


class Doc(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append({"tag": tag, "attrs": {k: (v or "") for k, v in attrs}})

    handle_startendtag = handle_starttag

    def get(self, tag: str) -> list[dict]:
        return [t for t in self.tags if t["tag"] == tag]


def data_facts() -> tuple[list[dict], dict]:
    data = json.loads((ROOT / "research_data.json").read_text(encoding="utf-8"))
    return [f for sec in data["facts"].values() for f in sec], data


def check_page(rel: str, raw_numbers: set[str], ids: set[str]) -> None:
    path = ROOT / rel
    print(f"\n--- {rel} ---")
    check(path.exists(), f"{rel} existe")
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    doc = Doc()
    doc.feed(html)
    depth = len(Path(rel).parents) - 1  # pages/histoire/x.html → 2

    # SEO
    check(len(doc.get("title")) == 1, "un seul <title>")
    desc = [m for m in doc.get("meta") if m["attrs"].get("name") == "description"]
    check(bool(desc) and len(desc[0]["attrs"]["content"]) >= 110, "meta description ≥ 110 caractères")
    check(any(l["attrs"].get("rel") == "canonical" for l in doc.get("link")), "canonical")
    hl = {l["attrs"].get("hreflang") for l in doc.get("link") if l["attrs"].get("hreflang")}
    check({"fr", "x-default"} <= hl, "hreflang fr / x-default")
    og = {m["attrs"].get("property") for m in doc.get("meta") if m["attrs"].get("property")}
    check({"og:title", "og:description", "og:image", "og:type"} <= og, "Open Graph complet")
    tw = {m["attrs"].get("name") for m in doc.get("meta") if m["attrs"].get("name")}
    check({"twitter:card", "twitter:title", "twitter:image"} <= tw, "Twitter Card")
    ld = [s for s in doc.get("script") if s["attrs"].get("type") == "application/ld+json"]
    ok_ld = False
    for block in ld:
        try:
            parsed = json.loads(html.split("</script>")[0]) if False else None
        except Exception:
            parsed = None
    if ld:
        try:
            start = html.find('<script type="application/ld+json">') + len('<script type="application/ld+json">')
            end = html.find("</script>", start)
            parsed = json.loads(html[start:end])
            ok_ld = "Article" in json.dumps(parsed) and "BreadcrumbList" in json.dumps(parsed)
        except Exception:
            ok_ld = False
    check(ok_ld, "JSON-LD Article + BreadcrumbList valide")

    # Structure & accessibilité
    check(len(doc.get("h1")) == 1, "un seul <h1>")
    check(any("s4-skip" in t["attrs"].get("class", "") for t in doc.get("a")), "lien d'évitement clavier")
    bc = [n for n in doc.get("nav") if n["attrs"].get("data-breadcrumbs")]
    check(bool(bc) and bc[0]["attrs"].get("data-breadcrumbs") == "static", "fil d'Ariane statique")
    check(any("aria-current" in t["attrs"] for t in doc.get("span")) or any("aria-current" in t["attrs"] for t in doc.get("a")), "page courante marquée aria-current")
    check(bool([n for n in doc.get("nav") if n["attrs"].get("aria-label")]), "navigation étiquetée")
    check('data-search' in html and 'data-search-panel' in html, "moteur de recherche présent")
    check("data-spoiler-toggle" in html and 'aria-controls="spoiler' in html, "SpoilerToggle + aria-controls")
    check(bool(doc.get("style")), "CSS critique inline")

    # Réseau externe
    ext_css = [l for l in doc.get("link") if l["attrs"].get("rel") == "stylesheet" and l["attrs"].get("href", "").startswith(("http", "//"))]
    ext_js = [s for s in doc.get("script") if s["attrs"].get("src", "").startswith(("http", "//"))]
    local_css = [l for l in doc.get("link") if l["attrs"].get("rel") == "stylesheet"]
    check(not ext_css and not ext_js, "0 ressource distante")
    check(len(local_css) >= 2 and all((path.parent / l["attrs"]["href"]).resolve().exists() for l in local_css), "feuilles CSS locales résolues")
    code = re.sub(r"/\*.*?\*/", "", html, flags=re.S)
    check("googleapis" not in code and "localhost" not in code and "127.0.0.1" not in code, "0 CDN / 0 localhost")

    # Badges
    status_badges = re.findall(r'data-status="([a-z_]+)"[^>]*data-badge="([^"]+)"', html)
    check(len(status_badges) >= 3, f"{len(status_badges)} blocs avec data-status + data-badge")
    check(all(f'>{badge}<' in html or badge in html for _, badge in status_badges), "chaque bloc porte son libellé de badge")
    check(html.count("badge badge--") >= 10, f"{html.count('badge badge--')} badges visibles dans le corps de page")

    # Images
    imgs = [t for t in doc.get("img")]
    # On compte les visuels réellement affichés : balises <img> + héros en background-image.
    bg_visuals = re.findall(r"background-image:\s*url\(['\"]?[^'\")]+['\"]?\)", html)
    check(len(imgs) + len(bg_visuals) >= 3, f"{len(imgs)} <img> + {len(bg_visuals)} héros = {len(imgs) + len(bg_visuals)} visuels")
    for img in imgs:
        src = img["attrs"].get("src", "")
        target = (path.parent / src).resolve()
        if not target.exists():
            check(False, f"image existante : {src}")
            continue
        alt = img["attrs"].get("alt", "")
        decorative = img["attrs"].get("aria-hidden") == "true" or "alt=\"\"" in ""
        check(src.lower().endswith(".jpg"), f"JPG : {Path(src).name}")
        check(bool(alt.strip()) or img["attrs"].get("aria-hidden") == "true", f"alt présent : {Path(src).name}")
        check(bool(img["attrs"].get("width")) and bool(img["attrs"].get("height")), f"width/height : {Path(src).name}")
        if not img["attrs"].get("fetchpriority"):
            check(img["attrs"].get("loading") == "lazy", f"loading lazy : {Path(src).name}")
        with Image.open(target) as im:
            # Les visuels d'objets (armes, véhicules) proviennent de fiches tierces et
            # gardent leur ratio d'origine : on vérifie le ratio déclaré, pas la taille exacte.
            if "objets" in Path(src).parts:
                declared = int(img["attrs"]["width"]) / int(img["attrs"]["height"])
                check(abs(declared - im.size[0] / im.size[1]) < 0.02,
                      f"ratio HTML = fichier : {Path(src).name} → {im.size}")
            else:
                check((int(img["attrs"]["width"]), int(img["attrs"]["height"])) == im.size,
                      f"dimensions HTML = fichier : {Path(src).name} → {im.size}")

    # Chiffres affichés
    shown = set(re.findall(r'data-verify-number="([^"]+)"', html))
    unknown = sorted(n for n in shown if n not in raw_numbers)
    check(not unknown, f"{len(shown)} chiffres affichés, tous traçables dans research_data.json" + (f" — inconnus : {unknown}" if unknown else ""))

    # Identifiants de faits cités
    cited = set(re.findall(r"\b(?:MIS|CHA|ECN|MAP|POL|WPN|VHC)\-\d{2}\b", html))
    orphans = sorted(c for c in cited if c not in ids)
    check(not orphans, f"{len(cited)} identifiants de faits cités, tous présents dans research_data.json" + (f" — orphelins : {orphans}" if orphans else ""))

    # Liens internes
    broken = []
    for a in doc.get("a"):
        href = a["attrs"].get("href", "")
        if not href or href.startswith(("http", "mailto:", "tel:", "//")):
            continue
        target = href.split("#")[0]
        if not target:
            continue
        resolved = (ROOT / target.lstrip("/")) if target.startswith("/") else (path.parent / target).resolve()
        if not resolved.exists():
            broken.append(href)
    check(not broken, f"0 lien interne cassé ({len(doc.get('a'))} liens)" + (f" — {broken}" if broken else ""))


def main() -> int:
    wanted = None
    if "--group" in sys.argv:
        wanted = sys.argv[sys.argv.index("--group") + 1]

    print("=== CP4 · S4 BUILD_CONTENT_PAGES ===")
    facts, data = data_facts()
    ids = {f["id"] for f in facts}
    raw_numbers: set[str] = set()
    blob = json.dumps(data, ensure_ascii=False)
    for match in re.findall(r"\d[\d  ]{0,20}(?:missions|faits|sources|heures|emplacements|chapitres|régions|Go|FPS|titres|stations|€|%)?", blob):
        raw_numbers.add(match.strip())
    for n in re.findall(r"\d+", blob):
        raw_numbers.add(n)

    total = 0
    for group, pages in GROUPS.items():
        if wanted and group != wanted:
            continue
        print(f"\n===== Groupe {group} : {len(pages)} pages =====")
        if group == "S22_LEGAL":
            for rel in pages:
                check((ROOT / rel).exists(), f"{rel} existe")
            continue
        total += len(pages)
        for rel in pages:
            check_page(rel, raw_numbers, ids)

    print("\n--- Médias et formats ---")
    jpgs = sorted((ROOT / "assets/images").rglob("*.jpg"))
    # S10 : les visuels d'objets (armes, véhicules) ont des formats hétérogènes
    # — on ne les traite pas comme les illustrations 1920x1080 du reste du site.
    jpgs = [p for p in jpgs if "objets" not in p.parts]
    mp3s = sorted((ROOT / "assets/audio").rglob("*.mp3"))
    story = [p for p in jpgs if "story" in p.parts and not p.name.startswith(("story_motel_pool", "story_roadside_bar", "story_timeline_corkboard", "story_chapter_calendar", "story_motel_room_cash"))]
    check(len(story) == 10, f"10 JPG G1 dans assets/images/story ({len(story)})")
    g2 = [p for p in jpgs if "characters" in p.parts and p.name.startswith(("lucia_", "cal_", "brian_", "boobie_", "drequan_", "raul_", "cast_")) and not p.name.startswith(("cast_crew_alley", "characters_crew_alley", "cast_two_figures"))]
    check(len(g2) == 10, f"10 JPG G2 dans assets/images/characters ({len(g2)})")
    g3_names = {"vicecity_ocean_drive_pastel_01.jpg", "vicecity_downtown_neon_dusk_01.jpg",
                "vicecity_little_havana_street_01.jpg", "weapons_armory_trunk_01.jpg",
                "weapons_pistol_closeup_01.jpg", "vehicles_supercar_causeway_01.jpg",
                "vehicles_speedboat_keys_01.jpg", "vehicles_muscle_pay_n_spray_01.jpg",
                "vehicles_police_interceptor_night_01.jpg"}
    g3 = [p for p in jpgs if p.name in g3_names]
    g4_names = {"police_roadblock_night_01.jpg", "police_helicopter_searchlight_01.jpg",
                "police_k9_tracking_swamp_01.jpg", "police_swat_armored_01.jpg",
                "economie_bank_vault_duffel_01.jpg", "economie_fence_pawnshop_01.jpg",
                "economie_atm_cash_night_01.jpg", "activites_airboat_everglades_01.jpg",
                "activites_minigolf_neon_01.jpg", "activites_cage_fight_01.jpg"}
    g4 = [p for p in jpgs if p.name in g4_names]
    check(len(g4) == 10, f"10 JPG G4 dans police/economie/activites ({len(g4)})")
    g5_names = {"musique_radio_studio_neon_01.jpg", "musique_dj_booth_crowd_01.jpg",
                "musique_car_radio_sunset_01.jpg", "musique_vinyl_wall_shop_01.jpg",
                "online_crew_garage_meet_01.jpg", "online_server_room_01.jpg",
                "online_console_living_room_01.jpg", "codes_phone_dialpad_night_01.jpg",
                "codes_notebook_handwritten_01.jpg", "codes_arcade_cabinet_01.jpg"}
    g5 = [p for p in jpgs if p.name in g5_names]
    check(len(g5) == 10, f"10 JPG G5 dans musique/online/codes ({len(g5)})")
    g6_names = {"trophees_trophy_shelf_neon_01.jpg", "trophees_checklist_notebook_01.jpg",
                "trophees_medal_city_dusk_01.jpg", "secrets_ufo_swamp_night_01.jpg",
                "secrets_underwater_wreck_01.jpg", "secrets_motel_neon_door_01.jpg",
                "secrets_wall_mural_street_01.jpg", "tips_focus_mode_alley_01.jpg",
                "tips_safe_cracking_01.jpg", "tips_map_glovebox_01.jpg"}
    g6 = [p for p in jpgs if p.name in g6_names]
    check(len(g6) == 10, f"10 JPG G6 dans trophees/secrets/tips ({len(g6)})")
    g7_names = {"outils_dual_screen_setup_01.jpg", "outils_interactive_map_wall_01.jpg",
                "outils_discord_room_glow_01.jpg", "divers_leonida_road_trip_dawn_01.jpg",
                "divers_marina_boats_golden_01.jpg", "divers_storm_palms_skyline_01.jpg",
                "faq_console_disc_box_01.jpg", "faq_install_progress_screen_01.jpg",
                "faq_versions_stack_01.jpg", "faq_question_notes_wall_01.jpg"}
    g7 = [p for p in jpgs if p.name in g7_names]
    check(len(g7) == 10, f"10 JPG G7 dans outils/divers/faq ({len(g7)})")
    s5_names = {"map_leonida_atlas_desk_01.jpg", "map_vicecity_neon_grid_01.jpg",
                "map_regions_terrain_relief_01.jpg", "map_highway_causeway_air_01.jpg",
                "collec_cards_flamingo_flatlay_01.jpg", "collec_shells_jar_01.jpg",
                "collec_checklist_clipboard_01.jpg", "quiz_neon_trivia_board_01.jpg",
                "quiz_pub_trivia_night_01.jpg", "quiz_arcade_scoreboard_01.jpg"}
    s5 = [p for p in jpgs if p.name in s5_names]
    check(len(s5) == 10, f"10 JPG S5 dans map/collectibles/quiz ({len(s5)})")
    # S6 : audit QA — 5 nouvelles illustrations (le lot S6 est volontairement
    # réduit : la QA ne produit pas d'images de contenu, seulement 5 visuels de dossier).
    s6_names = {"qa_accessibility_keyboard_01.jpg", "qa_responsive_devices_lineup_01.jpg",
                "qa_performance_graph_monitor_01.jpg", "qa_contrast_cards_macro_01.jpg",
                "qa_lighthouse_lcp_metaphor_01.jpg"}
    s6_names_full = s6_names | {"final_sunrise_causeway_wide_01.jpg", "final_guide_desk_stack_01.jpg",
                "final_archive_server_corridor_01.jpg", "final_palms_departure_road_01.jpg",
                "final_vicecity_dawn_rooftop_01.jpg"}
    s6 = [p for p in jpgs if p.name in s6_names]
    check(len(s6) == 5, f"5 JPG S6 dans qa ({len(s6)})")
    s7 = [p for p in jpgs if p.name.startswith("final_")]
    check(len(s7) == 5, f"5 JPG S7 dans final ({len(s7)})")
    s8 = [p for p in jpgs if p.name.startswith("review_") and p.name not in ("review_frame_pacing_graph_01.jpg", "review_players_couch_night_01.jpg", "review_motion_settings_tv_01.jpg")]
    check(len(s8) == 5, f"5 JPG S8 dans reviews ({len(s8)})")
    # S9 : nuit de lancement — 5 illustrations dédiées.
    s9 = [p for p in jpgs if p.name.startswith("lancement_") and p.name not in ("lancement_preload_progress_console_01.jpg", "lancement_status_phone_sofa_01.jpg", "lancement_midnight_kitchen_01.jpg", "lancement_ssd_toolkit_night_01.jpg", "lancement_quick_resume_sofa_01.jpg", "lancement_midnight_balcony_city_01.jpg", "lancement_frame_dip_bench_01.jpg")]
    check(len(s9) == 5, f"5 JPG S9 dans lancement ({len(s9)})")
    check(len(g3) == 9, f"9 JPG G3 dans vicecity/weapons/vehicles ({len(g3)})")
    for p in story + g2 + g3 + g4 + g5 + g6 + g7 + s5 + s6 + s7 + s8 + s9:
        with Image.open(p) as im:
            check(im.format == "JPEG" and max(im.size) >= 1920, f"{p.name} JPEG {im.size}")
    all_files = [p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    forbidden = [str(p.relative_to(ROOT)) for p in all_files if p.suffix.lower() in FORBIDDEN]
    check(not forbidden, "0 fichier au format interdit" + (f" — {forbidden}" if forbidden else ""))
    check(len(mp3s) == 12, f"playlist inchangée : {len(mp3s)} MP3")

    print("\n--- JS et liens ---")
    for js in ["main.js", "search.js", "utils.js", "components.js", "animations.js"]:
        rc = subprocess.run(["node", "--check", f"assets/js/{js}"], cwd=ROOT, capture_output=True).returncode
        check(rc == 0, f"node --check assets/js/{js}")
    rc = subprocess.run(["node", "tools/check_links.js"], cwd=ROOT, capture_output=True, text=True)
    check(rc.returncode == 0 and "0 lien interne cassé" in rc.stdout, "node tools/check_links.js → 0 cassé")

    print("\n--- Résultat ---")
    if errors:
        print(f"✗ {len(errors)} contrôle(s) en échec :")
        for e in errors:
            print(f"   - {e}")
        return 1
    if wanted is None:
        check(total == 29, f"29 pages = 21 S4 + 3 interactives S5 + QA S6 + livraison S7 + reviews S8 + lancement S9 + news S12 ({total})")
    print(f"✓ CP4 validé : {total} pages (S4 complet + 3 interactives S5 + rapport QA S6), 7 lots de 10 JPG (G2 à G7) + 9 JPG G3, "
          f"{len(jpgs)} JPG au total, {len(mp3s)} MP3, 0 lien cassé, 0 format interdit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
