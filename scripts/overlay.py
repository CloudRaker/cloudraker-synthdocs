"""Draw the ground-truth region boxes on a page.

    pip install pillow
    python scripts/overlay.py samples/core_legal_nda_*.json -o overlay.png
"""
import argparse, json, pathlib
from PIL import Image, ImageDraw

COLORS = {
    "title": "#d62728", "section_header": "#ff7f0e", "text": "#1f77b4", "list_item": "#17becf",
    "table": "#2ca02c", "table_caption": "#98df8a", "table_footnote": "#98df8a",
    "page_header": "#9467bd", "page_footer": "#9467bd", "caption": "#8c564b", "footnote": "#8c564b",
    "image": "#e377c2", "image_caption": "#e377c2", "chart": "#bcbd22", "formula": "#7f7f7f", "code": "#7f7f7f",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", type=pathlib.Path)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=pathlib.Path("overlay.png"))
    a = ap.parse_args()
    page = json.loads(a.json.read_text())
    img = Image.open(a.json.with_suffix(".webp")).convert("RGB")
    draw = ImageDraw.Draw(img)
    for i, r in enumerate(page["regions"]):
        c = COLORS.get(r["cat"], "#000000")
        draw.rectangle(r["bbox_px"], outline=c, width=3)
        draw.text((r["bbox_px"][0] + 4, r["bbox_px"][1] + 2), f'{i} {r["cat"]}', fill=c)
    img.save(a.out)
    print(f"{a.out}: {len(page['regions'])} regions, {len(page['tables'])} tables, preset={page['preset']}")


if __name__ == "__main__":
    main()
