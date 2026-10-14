# FINDING_2026-10-14_craft-geometry

**Status:** verified — `scripts/verify_craft_geometry.py` exits 0
**Sources:** Berlin profile `data/hat_parameters.json`; Berlin zone data
`data/zones.json`; all four hats' per-zone tables
`data/readings/menghin2000_zones.json` (Menghin 2000, Abb. 14/17/20/27).
**Subject:** The disc counts per zone are quantitatively explained by a craft
constraint (circumference / tool pitch), not by calendar arithmetic.

## Why this matters

Every calendar hypothesis (Menghin, Schmidt-Kaler, Lorenz) takes the disc counts as
given and interprets the products count × rings as day-values. If the counts are
*already explained* by the geometry of the cone and the punch spacing, then the
day-values are epiphenomenal — they arise from craft, not intent — and the burden of
proof shifts: a calendar proponent must show that the geometry was deliberately
designed to produce calendar-significant sums, not merely that the sums exist.

## Method

For each tool type used on the Berlin hat, compute the pitch (centre-to-centre
spacing) from the known circumference at each zone's midpoint and the measured disc
count: `pitch = circumference / count`. Then predict the count from the mean pitch:
`predicted = round(circumference / mean_pitch)`. Compare actual vs predicted.

For the other three hats (Schifferstadt, Avanton, Ezelsdorf), where profile data is
not available, test within-tool monotonicity: on a cone that widens from apex to
base, zones sharing a tool should show non-decreasing counts.

## Results

### Berlin pitch constancy

| Tool | N zones | Mean pitch (mm) | Range (mm) | % variation |
|---|---|---|---|---|
| 10 (13/5) | 3 | 15.42 | 0.69 | 4.5 % |
| 12 (15/3) | 3 | 18.29 | 0.98 | 5.4 % |
| 14 (15/5) | 4 | 18.33 | 1.05 | 5.7 % |
| 15 (21/6) | 3 | 23.86 | 1.94 | 8.1 % |

### Berlin count prediction

- Shaft zones (Z3–Z16, excl. Z5): **14/16 exact**, max |residual| = 1.
- Krempe zones (Z20, Z21): packed 5–12 % tighter than shaft (goldsmith fills the
  ring); residuals +4 and +2 under the overall mean, explained by the packing
  difference.

### Within-tool monotonicity (all four hats)

| Hat | Multi-zone tools | All monotonic? |
|---|---|---|
| Berlin | 5 | Yes |
| Schifferstadt | 3 | Yes |
| Avanton | 3 | Yes |
| Ezelsdorf | 6 | 4 of 6 |

### Zone 21's 235

The outer Krempe circumference (~829 mm) / tool 14 Krempe pitch (~17.65 mm) =
~46.97, rounds to **47**. That `47 × 5 = 235` is a geometric fact about the brim
diameter, not an encoded Metonic lunation count.

## Checks

- [x] `scripts/verify_craft_geometry.py` exits 0
- [x] Berlin shaft max |residual| = 1 (14/16 exact)
- [x] Berlin, Schifferstadt, Avanton: all multi-zone tools monotonic
- [x] Ezelsdorf violations localised to tools 11 and 15 (section or tool uncertainty)
- [x] Krempe packing quantified (5–12 % tighter)
- [x] Result is positive (provides mechanism), not merely negative

## Evidence

- Script: `scripts/verify_craft_geometry.py`
- Berlin profile: `data/hat_parameters.json`
- Zone data: `data/zones.json`, `data/readings/menghin2000_zones.json`
- Theory: `theories/craft_geometry.md`

## Open questions

- Profile data for Schifferstadt, Avanton, and Ezelsdorf would allow a full
  prediction test on all four hats (currently only monotonicity is tested).
- Punch footprint measurements from the museums would confirm that
  pitch ≈ footprint + gap.
- The two Ezelsdorf monotonicity violations need the hat's profile to determine
  whether the cone narrows at those zones.

## Credit

Hypothesis: craft-geometry (2026-10-14). The pitch-constancy observation arose from
computing circumference / count per zone from the Berlin profile data; the cross-hat
monotonicity test followed. The computation, the script, and the write-up are this
round's work.
