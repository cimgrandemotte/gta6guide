#!/usr/bin/env python3
"""Optimisation des JPG du groupe S4 / G1 (pages Histoire).

Ne traite QUE les fichiers listés ci-dessous : les JPG S2/S3 déjà livrés ne
sont jamais réencodés. Sortie JPEG q95, progressive, 1920×1080 ou
1280×1920, format .jpg exclusivement (aucun PNG/SVG/WebP).

Usage : python3 tools/optimize_images_s4.py [--dry-run]
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images"

TARGETS = [
    "story/story_prologue_prison_corridor_01.jpg",
    "story/story_leonida_keys_airboat_swamp_01.jpg",
    "story/story_heist_planning_table_01.jpg",
    "story/story_vice_city_night_chase_01.jpg",
    "story/story_cartel_warehouse_heist_01.jpg",
    "story/story_finale_highway_sunrise_01.jpg",
    "story/story_jason_portrait_neon_01.jpg",
    "story/story_jason_swamp_stalk_01.jpg",
    "story/story_lucia_release_gate_01.jpg",
    "story/story_duo_motel_doorway_01.jpg",
]

S9_TARGETS = [
    "lancement/lancement_controller_dawn_01.jpg",
    "lancement/lancement_first_drive_dash_01.jpg",
    "lancement/lancement_spoiler_shield_phone_01.jpg",
    "lancement/lancement_map_on_lap_01.jpg",
    "lancement/lancement_corner_store_3am_01.jpg",
]

S8_TARGETS = [
    "reviews/review_neon_scorecard_01.jpg",
    "reviews/review_critics_notes_desk_01.jpg",
    "reviews/review_screening_room_01.jpg",
    "reviews/review_midnight_launch_queue_01.jpg",
    "reviews/review_printing_press_pages_01.jpg",
]

S7_TARGETS = [
    "final/final_sunrise_causeway_wide_01.jpg",
    "final/final_guide_desk_stack_01.jpg",
    "final/final_archive_server_corridor_01.jpg",
    "final/final_palms_departure_road_01.jpg",
    "final/final_vicecity_dawn_rooftop_01.jpg",
]

S6_TARGETS = [
    "qa/qa_accessibility_keyboard_01.jpg",
    "qa/qa_responsive_devices_lineup_01.jpg",
    "qa/qa_performance_graph_monitor_01.jpg",
    "qa/qa_contrast_cards_macro_01.jpg",
    "qa/qa_lighthouse_lcp_metaphor_01.jpg",
]

S5_TARGETS = [
    "map/map_leonida_atlas_desk_01.jpg",
    "map/map_vicecity_neon_grid_01.jpg",
    "map/map_regions_terrain_relief_01.jpg",
    "map/map_highway_causeway_air_01.jpg",
    "collectibles/collec_cards_flamingo_flatlay_01.jpg",
    "collectibles/collec_shells_jar_01.jpg",
    "collectibles/collec_checklist_clipboard_01.jpg",
    "quiz/quiz_neon_trivia_board_01.jpg",
    "quiz/quiz_pub_trivia_night_01.jpg",
    "quiz/quiz_arcade_scoreboard_01.jpg",
]

G7_TARGETS = [
    "outils/outils_dual_screen_setup_01.jpg",
    "outils/outils_interactive_map_wall_01.jpg",
    "outils/outils_discord_room_glow_01.jpg",
    "divers/divers_leonida_road_trip_dawn_01.jpg",
    "divers/divers_marina_boats_golden_01.jpg",
    "divers/divers_storm_palms_skyline_01.jpg",
    "faq/faq_console_disc_box_01.jpg",
    "faq/faq_install_progress_screen_01.jpg",
    "faq/faq_versions_stack_01.jpg",
    "faq/faq_question_notes_wall_01.jpg",
]

G6_TARGETS = [
    "trophees/trophees_trophy_shelf_neon_01.jpg",
    "trophees/trophees_checklist_notebook_01.jpg",
    "trophees/trophees_medal_city_dusk_01.jpg",
    "secrets/secrets_ufo_swamp_night_01.jpg",
    "secrets/secrets_underwater_wreck_01.jpg",
    "secrets/secrets_motel_neon_door_01.jpg",
    "secrets/secrets_wall_mural_street_01.jpg",
    "tips/tips_focus_mode_alley_01.jpg",
    "tips/tips_safe_cracking_01.jpg",
    "tips/tips_map_glovebox_01.jpg",
]

G5_TARGETS = [
    "musique/musique_radio_studio_neon_01.jpg",
    "musique/musique_dj_booth_crowd_01.jpg",
    "musique/musique_car_radio_sunset_01.jpg",
    "musique/musique_vinyl_wall_shop_01.jpg",
    "online/online_crew_garage_meet_01.jpg",
    "online/online_server_room_01.jpg",
    "online/online_console_living_room_01.jpg",
    "codes/codes_phone_dialpad_night_01.jpg",
    "codes/codes_notebook_handwritten_01.jpg",
    "codes/codes_arcade_cabinet_01.jpg",
]

G4_TARGETS = [
    "police/police_roadblock_night_01.jpg",
    "police/police_helicopter_searchlight_01.jpg",
    "police/police_k9_tracking_swamp_01.jpg",
    "police/police_swat_armored_01.jpg",
    "economie/economie_bank_vault_duffel_01.jpg",
    "economie/economie_fence_pawnshop_01.jpg",
    "economie/economie_atm_cash_night_01.jpg",
    "activites/activites_airboat_everglades_01.jpg",
    "activites/activites_minigolf_neon_01.jpg",
    "activites/activites_cage_fight_01.jpg",
]

# Note : la 10e image G3 (sniper sur toit) n'a pas pu être générée pendant la
# réponse (quota de 10 images atteint) ; elle sera produite en G4 si utile.
G3_TARGETS = [
    "vicecity/vicecity_ocean_drive_pastel_01.jpg",
    "vicecity/vicecity_downtown_neon_dusk_01.jpg",
    "vicecity/vicecity_little_havana_street_01.jpg",
    "weapons/weapons_pistol_closeup_01.jpg",
    "weapons/weapons_armory_trunk_01.jpg",
    "vehicles/vehicles_supercar_causeway_01.jpg",
    "vehicles/vehicles_speedboat_keys_01.jpg",
    "vehicles/vehicles_muscle_pay_n_spray_01.jpg",
    "vehicles/vehicles_police_interceptor_night_01.jpg",
]

G2_TARGETS = [
    "characters/lucia_boxing_gym_01.jpg",
    "characters/lucia_getaway_driver_01.jpg",
    "characters/lucia_neon_portrait_01.jpg",
    "characters/lucia_parole_street_01.jpg",
    "characters/cal_hampton_radio_room_01.jpg",
    "characters/brian_heder_dock_01.jpg",
    "characters/boobie_ike_club_01.jpg",
    "characters/drequan_priest_street_01.jpg",
    "characters/cast_duo_wanted_poster_01.jpg",
    "characters/raul_bautista_garage_01.jpg",
]


def target_size(width: int, height: int) -> tuple[int, int]:
    """Paysage → 1920×1080, portrait → 1280×1920, ratio conservé par crop."""
    if height > width:
        return 1280, 1920
    return 1920, 1080


def cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    ratio = max(tw / image.width, th / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.LANCZOS)
    left = (resized.width - tw) // 2
    top = (resized.height - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def main() -> int:
    dry = "--dry-run" in sys.argv
    targets = TARGETS + ([] if "--g1-only" in sys.argv else G2_TARGETS)
    if "--g3-only" in sys.argv:
        targets = G3_TARGETS
    if "--g4-only" in sys.argv:
        targets = G4_TARGETS
    if "--g5-only" in sys.argv:
        targets = G5_TARGETS
    if "--g6-only" in sys.argv:
        targets = G6_TARGETS
    if "--g7-only" in sys.argv:
        targets = G7_TARGETS
    if "--s5-only" in sys.argv:
        targets = S5_TARGETS
    if "--s6-only" in sys.argv:
        targets = S6_TARGETS
    if "--s7-only" in sys.argv:
        targets = S7_TARGETS
    if "--s8-only" in sys.argv:
        targets = S8_TARGETS
    if "--s9-only" in sys.argv:
        targets = S9_TARGETS
    missing = [t for t in targets if not (IMG / t).exists()]
    if missing:
        print("Fichiers absents :", *missing, sep="\n  ")
        return 1

    total_before = total_after = 0
    for rel in targets:
        path = IMG / rel
        before = path.stat().st_size
        total_before += before
        with Image.open(path) as im:
            im = im.convert("RGB")
            size = target_size(im.width, im.height)
            out = cover_crop(im, size)
        if dry:
            print(f"[dry] {rel} → {size[0]}×{size[1]} ({before // 1024} Ko)")
            continue
        out.save(path, "JPEG", quality=95, optimize=True, progressive=True, subsampling=0)
        after = path.stat().st_size
        total_after += after
        print(f"{rel} → {size[0]}×{size[1]} · {after // 1024} Ko (avant {before // 1024} Ko)")

    if not dry:
        print(f"Total S4 : {total_after // 1024} Ko (avant {total_before // 1024} Ko) · {len(targets)} JPG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
