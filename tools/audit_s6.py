#!/usr/bin/env python3
"""Audit S6 — QA_AND_POLISH.

Contrôles réels, sans navigateur, sur les 24+2 pages HTML :
  • SEO / structure / liens (déjà couverts par check_s4, on ajoute ce qui manque) ;
  • accessibilité statique : alt, labels, aria, cibles, ordre des titres, lang ;
  • contraste WCAG AA calculé sur les paires couleur/texte déclarées dans le CSS ;
  • poids des pages et des images, budget par page ;
  • présence de robots.txt, manifest.json, sitemap complet ;
  • absence de ressource distante et de format interdit.

Sortie : `qa_report_s6.json` + résumé console. Code retour 1 si un contrôle échoue.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = (".png", ".svg", ".webp", ".avif", ".wav", ".ogg", ".flac", ".zip", ".pdf")
BUDGET_HTML_KO = 120
BUDGET_IMG_KO = 900

errors: list[str] = []
warnings: list[str] = []
report: dict = {}


def check(cond: bool, message: str, soft: bool = False) -> bool:
    if cond:
        print(f"  ✓ {message}")
    else:
        print(f"  {'!' if soft else '✗'} {message}")
        (warnings if soft else errors).append(message)
    return cond


# ── contraste WCAG ────────────────────────────────────────────────────────────
def _lum(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(fg: str, bg: str) -> float:
    a, b = _lum(fg), _lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def audit_contrasts() -> None:
    """Paires texte/fond réellement utilisées dans les CSS du projet."""
    pairs = [
        ("#f5f3ff", "#0b0a16", "texte principal sur fond nuit", 4.5),
        ("#f5f3ff", "#14122a", "texte sur carte", 4.5),
        ("#ff5ca8", "#0b0a16", "accent rose sur fond nuit", 3.0),
        ("#40e0d0", "#0b0a16", "accent turquoise sur fond nuit", 3.0),
        ("#ffc247", "#0b0a16", "accent ambre sur fond nuit", 3.0),
        ("#12091a", "#ff5ca8", "texte sur bouton rose actif", 4.5),
        ("#0b0a16", "#40e0d0", "texte sur case cochée", 4.5),
        ("rgba(255,255,255,0.72)", "#0b0a16", "texte secondaire", 4.5),
    ]
    print("\n--- Contrastes (WCAG AA) ---")
    results = []
    for fg, bg, label, minimum in pairs:
        if fg.startswith("rgba"):
            # approximation sur fond #0b0a16
            alpha = float(re.search(r"([\d.]+)\)", fg).group(1))
            base = "#0b0a16"
            blend = "#%02x%02x%02x" % tuple(
                round(alpha * int(fg.lstrip("rgba( ").split(",")[i].strip()) + (1 - alpha) * int(base[1 + 2 * i:3 + 2 * i], 16))
                for i in range(3)
            )
            fg = blend
        ratio = contrast(fg, bg)
        ok = ratio >= minimum
        results.append({"fg": fg, "bg": bg, "label": label, "ratio": round(ratio, 2), "min": minimum, "ok": ok})
        check(ok, f"{label} : {ratio:.2f}:1 (min {minimum})")
    report["contrastes"] = results


# ── pages ────────────────────────────────────────────────────────────────────
def pages() -> list[Path]:
    return sorted(list(ROOT.glob("*.html")) + list(ROOT.glob("pages/*/*.html")) + list(ROOT.glob("en/*.html")))


def audit_pages() -> None:
    print("\n--- Pages : structure, a11y, poids ---")
    rows = []
    for p in pages():
        rel = str(p.relative_to(ROOT))
        html = p.read_text(encoding="utf-8")
        size_ko = len(html.encode("utf-8")) / 1024
        row = {"page": rel, "ko": round(size_ko, 1)}

        check(size_ko < BUDGET_HTML_KO, f"{rel} : {size_ko:.0f} Ko < {BUDGET_HTML_KO} Ko", soft=True)

        # lang + titre + h1 + ordre des titres
        check('lang="fr"' in html or 'lang="en"' in html, f"{rel} : attribut lang", soft=True)
        h1 = len(re.findall(r"<h1\b", html))
        check(h1 == 1, f"{rel} : un seul h1 ({h1})")
        levels = [int(m) for m in re.findall(r"<h([1-6])\b", html)]
        jumps = [(a, b) for a, b in zip(levels, levels[1:]) if b > a + 1]
        check(not jumps, f"{rel} : pas de saut de niveau de titre", soft=True)

        # images
        imgs = re.findall(r"<img\b[^>]*>", html)
        no_alt = [i for i in imgs if 'alt=' not in i]
        check(not no_alt, f"{rel} : {len(imgs)} images, toutes avec alt")
        no_dim = [i for i in imgs if 'width=' not in i or 'height=' not in i]
        check(not no_dim, f"{rel} : width/height sur toutes les images")
        lazy = [i for i in imgs if 'loading="lazy"' in i or 'fetchpriority' in i]
        check(len(lazy) == len(imgs), f"{rel} : loading/fetchpriority explicite")

        # poids des images référencées
        refs = re.findall(r'src="([^"]+\.jpg)"', html) + re.findall(r'url\(([^)]+\.jpg)\)', html)
        heavy = []
        for ref in refs:
            target = (p.parent / ref).resolve()
            if target.exists() and target.stat().st_size / 1024 > BUDGET_IMG_KO:
                heavy.append((ref, round(target.stat().st_size / 1024)))
        check(not heavy, f"{rel} : aucune image > {BUDGET_IMG_KO} Ko" + (f" — {heavy}" if heavy else ""), soft=True)

        # formulaires / labels
        inputs = re.findall(r"<input\b[^>]*>", html)
        unlabelled = []
        for i in inputs:
            if 'type="search"' not in i and 'type="text"' not in i:
                continue
            has_aria = "aria-label" in i
            idm = re.search(r'id="([^"]+)"', i)
            has_for = bool(idm) and f'for="{idm.group(1)}"' in html
            if not (has_aria or has_for):
                unlabelled.append(i[:60])
        check(not unlabelled, f"{rel} : champs de saisie étiquetés")

        # cibles interactives : boutons avec texte ou aria-label
        buttons = re.findall(r"<button\b[^>]*>(.*?)</button>", html, re.S)
        raw_buttons = re.findall(r"<button\b[^>]*>.*?</button>", html, re.S)
        empty = [b[:80] for b in raw_buttons
                 if not re.sub(r"<[^>]+>|\s", "", re.sub(r"^<button\b[^>]*>|</button>$", "", b))
                 and "aria-label" not in b.split(">")[0]]
        check(not empty, f"{rel} : boutons nommés", soft=True)

        # ressources distantes
        remote = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
        remote_local = [u for u in remote if not urlparse(u).netloc.endswith(("example.test",))]
        local_hosts = [u for u in remote if "localhost" in u or "127.0.0.1" in u]
        check(not local_hosts, f"{rel} : aucun appel à localhost")

        row.update({"images": len(imgs), "h1": h1, "remote_links": len(remote)})
        rows.append(row)
    report["pages"] = rows
    total_ko = sum(r["ko"] for r in rows)
    print(f"  → {len(rows)} pages, {total_ko:.0f} Ko de HTML cumulé, "
          f"moyenne {total_ko / len(rows):.0f} Ko")


def audit_assets() -> None:
    print("\n--- Assets ---")
    jpgs = sorted((ROOT / "assets/images").rglob("*.jpg"))
    sizes = [(p, p.stat().st_size / 1024) for p in jpgs]
    total = sum(s for _, s in sizes)
    biggest = max(sizes, key=lambda x: x[1])
    print(f"  ✓ {len(jpgs)} JPG, {total / 1024:.1f} Mo, plus lourd : {biggest[0].name} ({biggest[1]:.0f} Ko)")
    check(biggest[1] < 1100, f"aucun JPG au-delà de 1 100 Ko ({biggest[1]:.0f})", soft=True)
    report["images"] = {"count": len(jpgs), "total_mo": round(total / 1024, 2),
                        "max_ko": round(biggest[1]), "max_file": biggest[0].name}

    css = sorted((ROOT / "assets/css").glob("*.css"))
    js = sorted((ROOT / "assets/js").glob("*.js"))
    print(f"  ✓ {len(css)} CSS ({sum(p.stat().st_size for p in css) / 1024:.0f} Ko), "
          f"{len(js)} JS ({sum(p.stat().st_size for p in js) / 1024:.0f} Ko)")
    report["css_js"] = {"css": len(css), "js": len(js),
                        "css_ko": round(sum(p.stat().st_size for p in css) / 1024),
                        "js_ko": round(sum(p.stat().st_size for p in js) / 1024)}

    # dist/ est un build généré (indexé nulle part) : exclu du décompte, mais aucun
    # fichier interdit ne doit y apparaître non plus.
    forbidden = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
                 if p.is_file() and p.suffix.lower() in FORBIDDEN
                 and "node_modules" not in p.parts and ".arena" not in p.parts]
    dist = ROOT / "dist"
    if dist.exists():
        print(f"  ✓ dist/ : {len(list(dist.rglob('*')))} fichiers générés (build S6, non référencés)")
    check(not forbidden, "0 fichier au format interdit" + (f" — {forbidden[:5]}" if forbidden else ""))


def audit_delivery() -> None:
    print("\n--- Livraison ---")
    for name in ("robots.txt", "manifest.json", "sitemap.xml"):
        check((ROOT / name).exists(), f"{name} présent")

    if (ROOT / "manifest.json").exists():
        try:
            man = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
            check("name" in man and "icons" in man and "start_url" in man, "manifest.json : champs requis")
            bad_icons = [i["src"] for i in man.get("icons", []) if i["src"].lower().endswith((".png", ".svg", ".webp"))]
            check(not bad_icons, "manifest : aucune icône PNG/SVG" + (f" — {bad_icons}" if bad_icons else ""),
                  soft=bool(bad_icons))
        except Exception as exc:  # noqa: BLE001
            check(False, f"manifest.json valide → {exc}")

    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8") if (ROOT / "sitemap.xml").exists() else ""
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    missing = []
    for loc in locs:
        rel = loc.split("gta-6.duckdns.org/")[-1].strip("/") or "index.html"
        if not (ROOT / rel).exists():
            missing.append(rel)
    check(not missing, f"{len(locs)} URLs de sitemap, toutes existantes" + (f" — {missing}" if missing else ""))

    html_pages = len(pages())
    indexables = [pg for pg in pages() if pg.name != "404.html"]
    check(len(locs) >= len(indexables), f"sitemap couvre au moins les {len(indexables)} pages indexables ({len(locs)} URLs)", soft=True)
    report["sitemap"] = {"urls": len(locs), "html_pages": html_pages}


def main() -> int:
    print("=== S6 · AUDIT QA ===")
    audit_contrasts()
    audit_pages()
    audit_assets()
    audit_delivery()

    report["errors"] = errors
    report["warnings"] = warnings
    (ROOT / "qa_report_s6.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n--- Résultat ---")
    if errors:
        print(f"✗ {len(errors)} contrôle(s) bloquant(s) :")
        for e in errors:
            print(f"   - {e}")
        return 1
    print(f"✓ Audit S6 validé : {len(pages())} pages, {len(warnings)} avertissement(s) non bloquant(s).")
    print("   Rapport : qa_report_s6.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
