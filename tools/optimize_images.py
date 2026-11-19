#!/usr/bin/env python3
"""
Post-traitement des 10 JPG générés en S2.

- Upscale Lanczos vers 1920×1080 (paysage 16:9) ou 1280×1920 (portrait 2:3)
- Ré-encodage JPEG qualité 95, subsampling 0 (4:4:4), progressif, optimisé
- Aucune conversion vers un autre format : entrée JPG → sortie JPG
- Aucun SVG / PNG / WebP / AVIF n'est produit

Rappel d'honnêteté : ces visuels sont des illustrations ORIGINALES générées par IA,
inspirées de l'esthétique néon Vice City. Ce ne sont PAS des captures officielles
Rockstar Games. Voir assets/images/CREDITS.md.

Usage : python3 tools/optimize_images.py
"""
from __future__ import annotations

import glob
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_ROOT = os.path.join(ROOT, "assets", "images")

LANDSCAPE = (1920, 1080)
PORTRAIT = (1280, 1920)


def target_for(size: tuple[int, int]) -> tuple[int, int]:
    w, h = size
    return PORTRAIT if h > w else LANDSCAPE


def main() -> None:
    files = sorted(glob.glob(os.path.join(IMG_ROOT, "**", "*.jpg"), recursive=True))
    print(f"Optimisation de {len(files)} fichiers JPG…")
    for path in files:
        with Image.open(path) as src:
            assert src.format == "JPEG", f"{path} : format inattendu {src.format}"
            src = src.convert("RGB")
            original = src.size
            target = target_for(original)
            # Rééchantillonnage Lanczos : meilleure conservation des détails fins.
            out = src.resize(target, Image.Resampling.LANCZOS)
            out.save(
                path,
                format="JPEG",
                quality=95,
                subsampling=0,      # 4:4:4 : pas de sous-échantillonnage couleur
                optimize=True,
                progressive=True,
            )
        rel = os.path.relpath(path, ROOT)
        print(f"  ✓ {rel:64s} {original[0]}x{original[1]} → {target[0]}x{target[1]}  "
              f"{os.path.getsize(path) // 1024} Ko")
    print("Terminé — 10 JPG haute qualité, 0 fichier SVG/PNG.")


if __name__ == "__main__":
    main()
