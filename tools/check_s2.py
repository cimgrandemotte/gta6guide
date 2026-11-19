#!/usr/bin/env python3
"""
Validation autonome du checkpoint CP2 (S2 — DESIGN_SYSTEM).

Vérifie : 4 CSS + 2 JS, 10 JPG haute qualité (dimensions /format), 10 MP3,
0 format interdit, schéma `source_url` de research_data.json, FSM/state S2,
et la cohérence des 10 chemins audio référencés par components.js.

Usage : python3 tools/check_s2.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CSS = ["design_system.css", "animations.css", "components.css", "responsive.css"]
JS = ["components.js", "animations.js"]
JPG_NAMES = [
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
MP3_NAMES = [
    "ambiances/homepage_ambiance_vicecity_night_01.mp3",
    "ui/homepage_ui_hover_01.mp3",
    "ui/homepage_ui_click_01.mp3",
    "ui/homepage_ui_transition_01.mp3",
    "jingles/characters_jason_theme_01.mp3",
    "jingles/characters_lucia_theme_01.mp3",
    "ambiances/map_leonida_ambiance_01.mp3",
    "ui/weapons_equip_sound_01.mp3",
    "ambiances/vehicles_engine_v8_01.mp3",
    "ui/quiz_correct_answer_01.mp3",
]
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    status = "✓" if condition else "✗"
    print(f"  {status} {message}")
    if not condition:
        errors.append(message)


def main() -> int:
    print("=== CP2 · S2 DESIGN_SYSTEM ===\n--- Fichiers de code ---")
    for name in CSS:
        p = ROOT / "assets" / "css" / name
        check(p.is_file() and p.stat().st_size > 3000, f"assets/css/{name} ({p.stat().st_size if p.exists() else 0} o)")
    for name in JS:
        p = ROOT / "assets" / "js" / name
        check(p.is_file() and p.stat().st_size > 3000, f"assets/js/{name} ({p.stat().st_size if p.exists() else 0} o)")
        if p.exists():
            r = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True)
            check(r.returncode == 0, f"node --check {name}" + ("" if r.returncode == 0 else f" → {r.stderr.strip()[:180]}"))

    print("\n--- Design tokens & effets ---")
    ds = (ROOT / "assets" / "css" / "design_system.css").read_text(encoding="utf-8")
    for token in ["#FF2D78", "#00D4FF", "#FFD700", "#0A0A0F", "#12121C", "#1A1A2E",
                  "#FFFFFF", "#B0B8D4", "#00FF9D", "#FF4444", "--c-sunset", "--c-violet", "--c-pastel"]:
        check(token in ds, f"token {token}")
    anim = (ROOT / "assets" / "css" / "animations.css").read_text(encoding="utf-8")
    for effect in ["GlitchText", "NeonGlow", "ScanLines", "FloatingParticles", "CardHover3D", "LoadingScreen", "CursorCustom"]:
        check(effect in anim, f"effet {effect}")
    resp = (ROOT / "assets" / "css" / "responsive.css").read_text(encoding="utf-8")
    for bp in ["320px", "768px", "1024px", "1440px", "2560px"]:
        check(bp in resp, f"breakpoint {bp}")

    print("\n--- Médias (10 JPG / 10 MP3) ---")
    all_jpg = sorted((ROOT / "assets" / "images").rglob("*.jpg"))
    all_mp3 = sorted((ROOT / "assets" / "audio").rglob("*.mp3"))
    # S3 a ajouté un nouveau lot : CP2 valide désormais la PRÉSENCE du lot S2,
    # pas l'absence d'assets livrés plus tard.
    check(len(all_jpg) >= 10, f"lot S2 présent ({len(all_jpg)} JPG au total, S3 inclus)")
    check(len(all_mp3) >= 10, f"lot S2 présent ({len(all_mp3)} MP3 au total, S3 inclus)")
    for rel in JPG_NAMES:
        p = ROOT / "assets" / "images" / rel
        ok = p.is_file()
        if ok:
            with Image.open(p) as im:
                ok = im.format == "JPEG" and im.size in [(1920, 1080), (1280, 1920)]
        check(ok, f"JPG {rel} → 1920×1080 / 1280×1920")
    for rel in MP3_NAMES:
        p = ROOT / "assets" / "audio" / rel
        head = p.open("rb").read(3) if p.is_file() else b""
        check(p.is_file() and (head.startswith(b"ID3") or (len(head) == 3 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0)), f"MP3 {rel}")

    print("\n--- Formats interdits ---")
    forbidden = []
    for pat in ("*.png", "*.svg", "*.webp", "*.avif", "*.wav", "*.ogg", "*.flac", "*.zip", "*.pdf"):
        forbidden += [str(p.relative_to(ROOT)) for p in ROOT.rglob(pat)]
    check(not forbidden, f"0 PNG/SVG/WebP/AVIF/WAV/ZIP/PDF livré" + (f" → {forbidden[:5]}" if forbidden else ""))

    print("\n--- Cohérence des chemins audio dans components.js ---")
    comp = (ROOT / "assets" / "js" / "components.js").read_text(encoding="utf-8")
    paths = re.findall(r"src: '(assets/audio/[^']+\.mp3)'", comp)
    check(len(paths) == 10, f"{len(paths)} pistes déclarées")
    check(all((ROOT / p).is_file() for p in paths), "tous les MP3 référencés existent")

    print("\n--- research_data.json ---")
    data = json.loads((ROOT / "research_data.json").read_text(encoding="utf-8"))
    flat = [f for section in data["facts"].values() for f in section]
    check(all(
        "source_url" in f and (
            (isinstance(f.get("sources"), list) and f["sources"] and f["source_url"] == f["sources"][0])
            or (isinstance(f.get("sources"), list) and not f["sources"] and bool(f["source_url"]))
            or "sources" not in f
        )
        for f in flat
    ),
          f"source_url sur les {len(flat)} faits")
    check(len(data["facts"]) >= 20, f"{len(data['facts'])} sections")
    check(len(data["sources_registry"]) >= 114, f"registre S2 présent ({len(data['sources_registry'])} sources, S3 inclus)")
    check(data["s2_press_mission_list"]["total"] == 93, "93 missions structurées")
    check("source_url" in data["meta"]["integrity_rule"] or "source_url" in str(data["meta"]["s2_amendment"]),
          "règle d'intégrité S2 tracée")

    print("\n--- FSM ---")
    state = json.loads((ROOT / "state.json").read_text(encoding="utf-8"))
    check(state["current_state"] in {"S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31"} and state["status"] in {"COMPLETE", "IN_PROGRESS"},
          f"state.json = {state['current_state']} {state['status']} (S2 franchi)")
    check(state["gate"].startswith("WAITING_FOR_CONTINUER") or state["gate"] == "FIN",
          f"gate → {state['gate']}")
    try:
        import yaml
        wf = yaml.safe_load((ROOT / "workflow_master.yaml").read_text(encoding="utf-8"))
        fsm = wf["meta"]["fsm"]
        check(fsm["current_state"] in {"S2", "S3", "S4", "S5"} and fsm["status"] in {"COMPLETE", "IN_PROGRESS"},
              f"workflow_master.yaml → {fsm['current_state']} {fsm['status']}")
        check("research_s2" in wf, "section research_s2 présente")
    except ImportError:
        check(False, "PyYAML disponible")

    print("\n--- Résultat ---")
    if errors:
        print(f"✗ {len(errors)} contrôle(s) en échec :")
        for e in errors:
            print(f"   - {e}")
        return 1
    print("✓ CP2 validé : S2 DESIGN_SYSTEM complet, 0 fichier interdit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
