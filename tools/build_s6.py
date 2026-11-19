#!/usr/bin/env python3
"""Build de production S6 — minification conservatrice.

Le site publié n'utilise PAS ce build : les pages chargent directement
assets/css/*.css et assets/js/*.js, ce qui garantit un fonctionnement sans
étape de compilation (et dans l'aperçu sandbox). Ce script produit une variante
allégée dans dist/ pour un hébergement réel.

Règles :
  • CSS : commentaires supprimés, espaces compactés, accolades équilibrées vérifiées.
  • JS  : commentaires supprimés seulement — aucun renommage, aucune concaténation,
          le graphe d'imports ES reste intact et chaque fichier passe `node --check`.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
(DIST / "js").mkdir(exist_ok=True)

CSS_ORDER = ["design_system.css", "animations.css", "components.css",
             "responsive.css", "s3_home.css", "s4_pages.css", "s5_interactive.css"]


def strip_block_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def minify_css(text: str) -> str:
    text = strip_block_comments(text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{}:;,>~+])\s*", r"\1", text)
    return text.replace(";}", "}").strip()


def minify_js(text: str) -> str:
    text = strip_block_comments(text)
    lines = [ln.rstrip() for ln in text.splitlines() if not ln.strip().startswith("//")]
    return "\n".join(ln for ln in lines if ln.strip()) + "\n"


def main() -> int:
    css_src = [ROOT / "assets/css" / name for name in CSS_ORDER if (ROOT / "assets/css" / name).exists()]
    css_out = "".join(minify_css(p.read_text(encoding="utf-8")) for p in css_src)
    (DIST / "app.min.css").write_text(css_out, encoding="utf-8")
    balanced = css_out.count("{") == css_out.count("}")
    print(f"CSS : {sum(p.stat().st_size for p in css_src) // 1024} Ko → "
          f"{(DIST / 'app.min.css').stat().st_size // 1024} Ko ({len(css_src)} feuilles) · accolades {'OK' if balanced else 'DÉSÉQUILIBRÉES'}")

    ok = 0
    js_src = [p for p in sorted((ROOT / "assets/js").glob("*.js")) if ".min." not in p.name]
    for p in js_src:
        target = DIST / "js" / p.name.replace(".js", ".min.js")
        target.write_text(minify_js(p.read_text(encoding="utf-8")), encoding="utf-8")
        rc = subprocess.run(["node", "--check", str(target)], capture_output=True).returncode
        ok += rc == 0
        if rc:
            print(f"  ✗ {p.name}")
    print(f"JS  : {sum(p.stat().st_size for p in js_src) // 1024} Ko → "
          f"{sum(p.stat().st_size for p in (DIST / 'js').glob('*.min.js')) // 1024} Ko · "
          f"{ok}/{len(js_src)} modules valides")

    (DIST / "README.md").write_text(
        "# dist/ — build de production (S6)\n\n"
        "Généré par `tools/build_s6.py`. Rien ici n'est référencé par les pages : le site\n"
        "fonctionne sans étape de build.\n\n"
        "- `app.min.css` : concaténation minifiée des 7 feuilles, ordre à conserver\n"
        "  (design_system → animations → components → responsive → s3_home → s4_pages → s5_interactive).\n"
        "- `js/*.min.js` : 8 modules ES, commentaires retirés, graphe d'imports préservé.\n\n"
        "Pour publier en production : remplacer les `<link rel=\"stylesheet\">` par une seule\n"
        "référence à `dist/app.min.css`, puis servir `dist/js/main.min.js` en ajustant les\n"
        "chemins relatifs des imports (`./search.js` → `./search.min.js`).\n",
        encoding="utf-8")
    return 0 if balanced and ok == len(js_src) else 1


if __name__ == "__main__":
    raise SystemExit(main())
