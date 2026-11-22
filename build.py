#!/usr/bin/env python3
"""Build a ready-to-send complaint form from a config file.

Usage:
    python build.py config/example.config.json            -> docs/index.html (public demo)
    python build.py config/<yourcompany>.config.json      -> dist/<key>-complaint-form.html

The output is ONE self-contained HTML file (logo, products and complaint types embedded).
Send it to customers by e-mail / WhatsApp, or host it (e.g. GitHub Pages).
"""
import base64, json, mimetypes, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_type_library(path):
    sets, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or (line.startswith("#") and not line.startswith("##")):
            continue
        if line.startswith("##"):
            cur = line[2:].strip()
            sets[cur] = []
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5 or cur is None:
            continue
        tid, en, tr, ru, kw = parts[:5]
        sets[cur].append({"id": tid, "label": {"en": en, "tr": tr, "ru": ru},
                          "kw": [k.strip() for k in kw.split(",") if k.strip()]})
    return sets


def data_uri(path):
    if not path:
        return ""
    p = (ROOT / path)
    if not p.exists():
        print(f"  ! logo not found: {path}")
        return ""
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def main():
    cfg_path = Path(sys.argv[1] if len(sys.argv) > 1 else "config/example.config.json")
    cfg = json.loads((ROOT / cfg_path).read_text(encoding="utf-8"))

    sets = load_type_library(ROOT / cfg.get("typeLibrary", "taxonomy/type-library.tsv"))
    groups = json.loads((ROOT / cfg.get("groups", "taxonomy/default.groups.json")).read_text(encoding="utf-8"))
    for g in groups:
        g["kind"] = g.get("set", "")          # paint / decorative / grout … (drives pack sizes & base column)
        g["types"] = sets.get(g.pop("set", ""), [])
        g.setdefault("products", [])
    taxonomy = {"common": sets.get("common", []), "groups": groups}

    brand = dict(cfg.get("brand", {}))
    brand["logo"] = data_uri(brand.get("logo"))
    out_cfg = {
        "key": cfg.get("key", "pcf"),
        "brand": brand,
        "prefix": cfg.get("prefix", "PCF"),
        "languages": cfg.get("languages", ["en", "tr", "ru"]),
        "defaultLang": cfg.get("defaultLang", "en"),
        "recipients": cfg.get("recipients", []),
        "allowCustomize": cfg.get("allowCustomize", False),
        "ocr": cfg.get("ocr", {}),
        "taxonomy": taxonomy,
    }

    html = (ROOT / "src/form.html").read_text(encoding="utf-8")
    payload = json.dumps(out_cfg, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__CONFIG__", payload)

    out = ROOT / cfg.get("output", f"dist/{out_cfg['key']}-complaint-form.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    n_types = len(taxonomy["common"]) + sum(len(g["types"]) for g in groups)
    n_prod = sum(len(g["products"]) for g in groups)
    print(f"Built {out.relative_to(ROOT)}  |  {len(groups)} groups, {n_types} complaint types, {n_prod} products")


if __name__ == "__main__":
    main()
