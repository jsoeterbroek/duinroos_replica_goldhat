# Catalogue: Menghin's numbers (how they were checked)

**What it is:** the reference set of Menghin's own counts — now for **all four**
hats — so that any "new" number can be checked against it before being called a find.

**How checked:**
- **2010, pp. 47–63:** full read of `assets/menghin/2010/text/menghin_pages47-63.txt`
  and the derived `data/zones.json` / `data/readings/menghin.json`, re-verified by
  `scripts/verify_calendar.py` and `scripts/verify_scenarios.py`.
- **2000, pp. 31–108:** full read of the page images `assets/menghin/2000/jpg/` (the
  OCR text was used for grep only), transcribed to
  `data/readings/menghin2000_zones.json`, re-verified by
  `scripts/verify_menghin2000.py` (control C6). Added 2026-10-12.

## The catalogue

| Quantity | Value | Note |
|---|---|---|
| **Berlin** ring-units, zones 3–21 | 1739 | = 1701 + 38 (Z5 counted twice) |
| Berlin ring-units, zones 2–21 | 1783 | |
| Berlin concentric rings, zones 3–21 | 1701 | on 418 discs in 18 friezes |
| Berlin concentric rings, zones 3–20 | 1466 | |
| Berlin "Zeichen", zones 3–21 | 437 | = 418 + 19 (Z5 counted once) |
| Berlin special signs, zone 5 | 38 | 19 crescent+dot + 19 eye |
| Berlin zone day-values | 42,75,38,90,57,105,57,95,60,100,60,105,90,38,66,126,138,162,235 | zones 3–21 |
| Berlin intercalary set | {7,16,17} | **2000 and 2010 both**; Z5 is a Sonderzone added for solar cycles |
| Berlin height total | 745.0 mm | |
| **Schifferstadt** rings, zones 2–11 | 557 | |
| Schifferstadt disc symbols, 8 zones (2, 5–11) | 266 | |
| Schifferstadt all symbols, zones 2–11 | 310 | |
| Schifferstadt rings, zones 2–9 | 355 | = 311 + 44 Sondermuster |
| Schifferstadt intercalary set | {2, 9} | |
| **Avanton** rings, zones 2–14 | 583 | |
| Avanton disc symbols, zones 2–14 | 269 | |
| Avanton rings, shaft zones 3–14 | 537 | = 583 − 46 |
| Avanton intercalary zone | {12} | zones 12–14 are reconstructions |
| **Ezelsdorf** stamped symbols, zones 2–20 | 499 | primary count, 2026-10-12 |
| Ezelsdorf disc symbols, zones 3–20 | 432 | |
| Ezelsdorf rings, zones 3–20 | 1463 | no rim |
| Ezelsdorf rings, zones 3–21 | 1694 | with Menghin's rebuilt rim |
| Ezelsdorf "Zeichen", zones 3–21 | 1737 | with the rebuilt rim |
| Ezelsdorf intercalary set | {5, 6, 19} | Sonderzeichen zones 15, 17 |

Data: `data/readings/menghin2000_zones.json`, `data/zones.json`,
`data/readings/menghin.json`.

## Corrections to this catalogue (2026-10-12)

- The earlier row "intercalary set … 2000 text: {5,7,16,17}" was **wrong**. Reading
  Menghin 2000 itself: the Berlin Schaltzonen are `{7,16,17}` throughout; zone 5 is a
  *Sonderzone* drawn in the same grey and *added* (38) for solar cycles, exactly as in
  2010. Only the bookkeeping of the 54-month value differs: 2000 uses
  `1701 − (38 + 66) = 1597`, Wikipedia/2010 use `1739 − (38 + 38 + 66) = 1597`.
- Berlin's disc count: 418 (pp. 81, and 2010 p. 31, and the table) — **not** the 399
  printed twice in the 2000 running text (pp. 83, 91).

## What is *not* in it

- `~3,393` "symbols" (garbled; no zone table sums to it).
- `1739` as an Ezelsdorf symbol count (that is Berlin's ring total).
- any plain-ornament count (`651` etc.) — that is Schmidt-Kaler's unit.
- the three flagged deltas (Ezelsdorf 475/508/465 vs 474/505/462; the Avanton
  177 row). They are transcription-vs-text mismatches, not Menghin values.

## Use

Before writing a new finding: does the number already appear here? If yes, the
finding is a *re-finding* (still useful as a control) and not novel.
