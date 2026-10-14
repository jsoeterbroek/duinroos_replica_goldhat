# Control C7 — Menghin 2010 tables must reproduce the 2000 tables

**What:** the whole of Menghin 2010 is now held (pp. 1–88, `assets/menghin/2010/`).
Its two published per-zone tables must reproduce the 2000 article's tables, zone by
zone and ring by ring — otherwise the new scan, the page mapping or the 2000
transcription is wrong. This is the scan's known-answer control.

**Expected:**

- **Berlin** — 2010 Abb. 23 (p. 30) == 2000 Abb. 14 (p. 45): Z3 3/14, Z4 5/15,
  Z5 19/19, Z6 5/18, Z7 3/19, Z8 5/21, Z9 3/19, Z10 5/19, Z11 3/20, Z12 5/20,
  Z13 3/20, Z14 5/21, Z15 6/15, Z16 2/19, Z17 2/33, Z18 6/21, Z19 6/23, Z20 3/54,
  Z21 5/47 (K/A).
- **Ezelsdorf** — 2010 Abb. 69 (p. 68) == 2000 Abb. 27 (p. 61), ring for ring:
  Z5 54, Z6 84, Z7 66, Z9 150, Z10 96, Z11 95, Z12 140, Z13 45, Z14 102, Z16 57,
  Z18 98, Z19 52, Z20 154; totals 1506 (Z3–20) and 1737 (with the rebuilt rim).

**How to re-find:** read the page images
`assets/menghin/2010/jpg/menghin_page030.jpeg` and `…page068.jpeg`, and compare
against `data/readings/menghin2000_zones.json` (control C6).

**Result 2026-10-13:** both reproduce. The only discrepancy is the already-known
**Zone 8 `A=40` with `SK=78`** slip, which appears in *both* publications — so it is
in Menghin's typescript, not the scan. This also confirms the 2010 page map.

**If missed:** the 2010 split/page map is wrong, or the 2000 transcription is wrong.
