# Annotation schema

Each page is a pair of files that share an id:

    <subset>/<split>/<industry>/<doctype>/<id>.webp   page image, RGB, 1700 x 2200 px (US Letter at 200 DPI)
    <subset>/<split>/<industry>/<doctype>/<id>.json   ground truth

## JSON fields

| field | type | description |
|---|---|---|
| `id` | string | Page id, unique across the whole dataset. |
| `industry` | string | One of the 9 industries. |
| `doctype` | string | Document type within the industry. |
| `lang` | `"en"` \| `"fr"` | Main language of the page. French pages use Canadian French (fr-CA). Some English pages carry bilingual labels. |
| `seed` | string | Seed of the page. Equal to `id`. |
| `preset` | string | Degradation preset applied to the page (see README). |
| `bbox_approx` | bool | `true` when the preset warps the page locally (for example `crumpled`). Boxes are then approximate by a few pixels. |
| `styled` | bool | Only in the `charts` and `styles` subsets. `true` when the page uses a varied visual theme. |
| `homography` | 3x3 array or `null` | Projective transform from the clean render to the degraded image, in pixels. `null` when the preset has no geometric change. |
| `width`, `height` | int | Image size in pixels (1700 x 2200). |
| `page_md` | string | Full-page markdown: all regions in reading order, joined by blank lines. Tables are GitHub markdown. |
| `layout_1036` | array | Layout boxes `{bbox: [x1, y1, x2, y2], cat}` normalized to a 1036 x 1036 space, in reading order. |
| `regions` | array | Regions in reading order: `{id, cat, bbox_px: [x1, y1, x2, y2], md}`. Table regions also have `otsl` and `html`. |
| `tables` | array | Tables on the page: `{id, otsl, html, markdown}`. The `id` matches the table's region id. |

## Coordinates

- `bbox_px` is in image pixels (origin top-left).
- `layout_1036` is the same box scaled to 1036 x 1036: `x * 1036 / width`, `y * 1036 / height`.
- On pages with a homography (skew, phone photo, perspective), each box is the axis-aligned bound of the warped quad. Boxes are therefore a little larger on rotated pages.

## Region categories

`title`, `section_header`, `text`, `list_item`, `page_header`, `page_footer`, `caption`, `footnote`,
`table`, `table_caption`, `table_footnote`, `image`, `image_caption`, `chart`, `formula`, `code`.

## Reading order

- Regions in the normal page flow come in document order.
- Margin notes slot in by their top edge.
- `page_header` regions come first and `page_footer` regions come last.
- Empty regions (spacers, blank ruled lines) are not included.

## Tables (OTSL)

Each table is given in three formats: OTSL, HTML and GitHub markdown. OTSL tokens:

| token | meaning |
|---|---|
| `<fcel>text` | cell with content |
| `<ecel>` | empty cell |
| `<lcel>` | continuation of a colspan (merged with the cell on the left) |
| `<ucel>` | continuation of a rowspan (merged with the cell above) |
| `<xcel>` | continuation of both a colspan and a rowspan |
| `<nl>` | end of row |

## Known limits

- Checkbox state is not in the markdown. The ground truth has the checkbox label only. Handwritten marks inside table cells are in the ground truth.
- `chart` and `image` regions have a box but no transcription of the graphic content.
- All names, addresses, phone numbers, account numbers and other identifiers are synthetic. They look like Canadian data (provinces, postal codes, area codes) but they do not refer to real people or organizations.
