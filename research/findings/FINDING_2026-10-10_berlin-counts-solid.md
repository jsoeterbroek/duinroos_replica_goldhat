# FINDING_2026-10-10_berlin-counts-solid

**Status:** verified
**Source:** Menghin 2010, pp. 47–63 (`assets/menghin/2010/text/`, scans
`assets/menghin/2010/jpg/menghin_page47..63.jpeg`)
**Subject:** the non-interpretive counts of the Berlin Gold Hat

## Verbatim / numbers

- 21 ornamental zones; 418 bossed discs carry **1701** concentric rings.
- Zone 5 adds **38** special signs (19 crescent+dot, 19 eye/almond).
- Zones 2–21 total **1783** ring-units; zones 3–21 total **1739**.
- `1739 = 1701 + 38`; the ring heights sum to **745.0 mm**.

## Checks

- [x] Read on the source pages (project author, 2026-10-08; scans in `assets/`)
- [x] Reproduced independently by `scripts/verify_calendar.py` (all identities)
- [x] Unit stated: concentric rings × discs ("day-value"), not plain symbols
- [x] Catalogues checked: `catalogues/menghin_numbers.md` — full read

## Evidence

`data/zones.json`, `data/readings/menghin.json`, `data/hat_parameters.json`;
`assets/menghin/2010/jpg/*.jpeg`. Control: `controls/C1_menghin_counts.md`.

## Open questions

- The 2000 vs 2010 intercalary-zone set discrepancy (`{5,7,16,17}` vs `{7,16,17}`).
- Whether the two caveat states (61.2, 64.4) are resolvable from a better scan.
