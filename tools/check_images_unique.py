#!/usr/bin/env python3
"""Vérifie qu'aucune image n'est utilisée deux fois sur le site.

Règle produit (S10) : une illustration générée ne doit apparaître qu'une seule
fois. Si une page a besoin d'un second visuel, il faut en générer un nouveau —
jamais réutiliser le même fichier.

Sortie : code 0 si toutes les images sont uniques, 1 sinon.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# On compte TOUTES les références visibles à une image : balises <img> et
# arrière-plans CSS (les héros de page utilisent background-image).
IMG_RE = re.compile(r'<img[^>]+src="([^"]+)"')
BG_RE = re.compile(r"background-image:\s*url\(['\"]?([^'\")]+)['\"]?\)")


def main() -> int:
    usage: dict[str, list[str]] = defaultdict(list)
    for page in sorted(ROOT.rglob("*.html")):
        if page.relative_to(ROOT).parts[0] in {"out", "_site", "dist"}:
            continue
        if "dist" in page.parts:
            continue
        html = page.read_text(encoding="utf-8")
        refs = IMG_RE.findall(html) + BG_RE.findall(html)
        for src in refs:
            if src.startswith("data:"):
                continue
            usage[Path(src).name].append(str(page.relative_to(ROOT)))

    dupes = {name: pages for name, pages in usage.items() if len(pages) > 1}
    extras = sum(len(pages) - 1 for pages in dupes.values())
    total = sum(len(pages) for pages in usage.values())

    print(f"Images distinctes utilisées : {len(usage)} · occurrences : {total}")
    if dupes:
        print(f"\n{len(dupes)} image(s) utilisée(s) plusieurs fois ({extras} occurrence(s) en trop) :")
        for name in sorted(dupes):
            pages = sorted(set(dupes[name]))
            print(f"  {len(dupes[name])}x {name}")
            for p in pages:
                print(f"      {p}")
        return 1
    print("Toutes les images sont uniques.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
