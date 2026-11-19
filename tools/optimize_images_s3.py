#!/usr/bin/env python3
"""Post-traitement des 10 JPG générés en S3 (lot IMG011–IMG020).

- Upscale Lanczos vers 1920×1080 (paysage) ou 1280×1920 (portrait)
- Ré-encodage JPEG q95, 4:4:4, progressif, optimisé
- N'altère PAS les 10 JPG déjà validés en S2
- Aucun SVG / PNG / WebP / AVIF n'est produit
"""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
S3_FILES = [
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
LANDSCAPE = (1920, 1080)
PORTRAIT = (1280, 1920)


def main() -> None:
    print("Optimisation des 10 JPG S3 (IMG011–IMG020)…")
    for rel in S3_FILES:
        path = ROOT / "assets" / "images" / rel
        with Image.open(path) as src:
            assert src.format == "JPEG", f"{path}: format inattendu {src.format}"
            original = src.size
            target = PORTRAIT if original[1] > original[0] else LANDSCAPE
            Image.Image.resize(
                src.convert("RGB"), target, Image.Resampling.LANCZOS
            ).save(
                path,
                format="JPEG",
                quality=95,
                subsampling=0,
                optimize=True,
                progressive=True,
            )
        print(f"  ✓ {rel:62s} {original[0]}×{original[1]} → {target[0]}×{target[1]}  {path.stat().st_size // 1024} Ko")
    print("Terminé — 10 JPG S3 haute qualité, 0 fichier interdit.")


if __name__ == "__main__":
    main()
