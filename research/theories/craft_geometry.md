# Theory: craft-geometry — disc counts determined by circumference / tool pitch

**Authors / date:** Soeterbroek/AI, 2026.
**Sources:** `scripts/verify_craft_geometry.py`; Berlin profile
`data/hat_parameters.json`; all four hats' per-zone tables
`data/readings/menghin2000_zones.json`.

## The claim

The disc counts in each zone are **not calendar encodings** but are determined by a
simple craft constraint: the goldsmith placed each punch tool at a characteristic
centre-to-centre spacing (the *pitch*), and the number of discs in a zone is how many
fit around the circumference at that height of the cone:

> count ≈ round(circumference(z) / pitch(tool))

The "day-values" (count × rings) that modern interpreters sum to calendar-adjacent
numbers are therefore epiphenomenal — they arise from the geometry of a cone
decorated with fixed-pitch punches, and a blind search over block combinations finds
them because the number space is dense enough that calendar targets are easy to hit
(as Fuls 2008 demonstrated independently).

The hat's genuine design content is **structural and iconographic**: the cone form
(axis mundi), the iconographic sequence (star → sun discs → crescent/eye → sun
discs → brim), the 12+7 alternation of packed and filler-linked disc types, and the
3×7 ornamental partition. None of these require numerical day-value encoding.

## Evidence

### 1. Pitch constancy on Berlin (quantitative)

For every tool used in multiple zones on the Berlin hat, the centre-to-centre
pitch is constant to within ~1 mm (4.5–8.1 % of the mean):

| Tool | N zones | Mean pitch (mm) | Range (mm) | % variation |
|---|---|---|---|---|
| 10 (13/5) | 3 | 15.42 | 0.69 | 4.5 % |
| 12 (15/3) | 3 | 18.29 | 0.98 | 5.4 % |
| 14 (15/5) | 4 | 18.33 | 1.05 | 5.7 % |
| 15 (21/6) | 3 | 23.86 | 1.94 | 8.1 % |

On a hand-beaten Bronze Age gold sheet, ~1 mm consistency is remarkable and
indicates a fixed working practice, not a numerical encoding.

### 2. Count prediction on Berlin (quantitative)

Using `round(circumference / mean_pitch)` to predict the disc count:

- **Shaft zones (Z3–Z16, excl. Z5): 14 of 16 exact, max |residual| = 1.**
- Krempe zones (Z20, Z21) are packed 5–12 % tighter than the shaft — the goldsmith
  filled the available ring on the flat brim plate. This packing difference explains
  the residuals of +4 (Z20) and +2 (Z21) when using the overall mean pitch.

### 3. Within-tool monotonicity across all four hats (structural)

On a cone that widens from apex to base, zones sharing a tool should show
non-decreasing disc counts (wider = more discs at the same pitch):

| Hat | Multi-zone tools | All monotonic? |
|---|---|---|
| Berlin | 5 | **Yes** |
| Schifferstadt | 3 | **Yes** |
| Avanton | 3 | **Yes** |
| Ezelsdorf | 6 | 4 of 6 |

Berlin, Schifferstadt and Avanton show **perfect** monotonicity. Ezelsdorf's two
violations (tools 11 and 15) may reflect a non-monotonic profile (the cone narrows
mid-shaft) or uncertain tool assignments on this fragmentary hat.

### 4. Zone 21's 235 is geometrically determined

Zone 21 (outer Krempe ring) has 47 discs × 5 rings = 235, the Metonic lunation
count and the single strongest numerical fact in the corpus. But the outer Krempe
ring has circumference ≈ 829 mm, and tool 14's Krempe pitch is ≈ 17.65 mm (5 %
tighter than the shaft's 18.56 mm), giving `round(829 / 17.65) = 47`. The number
47 is determined by the brim diameter and the punch spacing. That `47 × 5 = 235`
is a consequence of the hat's dimensions, not a deliberate encoding.

### 5. The cross-hat failure is predicted, not awkward

Under the calendar hypothesis, the cross-hat failure is devastating: if the hats are
calculators built to the same rule, the rule should work on all four. Under the craft
hypothesis, the failure is **expected**: each hat has a different profile, different
punches, and different circumferences at each zone height. The counts are
geometry-specific, not rule-specific. The structural *similarities* across hats
(all cones, all gold, all sun discs) reflect a shared cosmographic tradition; the
numerical *differences* reflect different geometries and toolkits.

## Status

**Candidate — 55–65 %.** The pitch constancy and count prediction are quantitative
and reproducible (`scripts/verify_craft_geometry.py`). The hypothesis has not been
peer-reviewed and is new to this investigation; it extends rather than contradicts
the sceptical position (cosmic yes, arithmetic no) by providing a *mechanism* for
why the counts are what they are.

## What would confirm

- **Cross-hat pitch test.** Obtain profile measurements for Schifferstadt, Avanton,
  and Ezelsdorf and verify that `round(circ / pitch)` predicts their counts as well
  as Berlin's. The per-zone tables are in hand (`menghin2000_zones.json`); only the
  profile geometries are missing.
- **Punch footprint measurement.** If the actual punch tool diameters (held by the
  museums) match the computed pitches minus a plausible inter-disc gap, the
  hypothesis is confirmed mechanically.
- **Residual analysis.** If every zone's count is fully explained by geometry, there
  is no room for calendar encoding. Any zone where the residual is large (the
  goldsmith broke the pitch rule) would be a candidate for deliberate numerical
  choice — and *that* zone, not the whole hat, would carry the burden of proof.

## What would refute

- A Berlin shaft zone where the count deviates by ≥ 3 from the geometric prediction
  and the deviation matches a calendar period. (Currently the max shaft residual is 1.)
- Profile data for Schifferstadt or Avanton showing that within-tool monotonicity
  fails when the circumference is known (rather than inferred from the count).
- Evidence that the goldsmith could have chosen a different pitch for a specific zone
  to reach a round number, but did not — i.e. the pitch was *not* the constraint.

## Relation to the other theories

This hypothesis **extends the sceptical position** (`theories/sceptical_ornament.md`)
by providing a positive explanation for the counts, rather than merely arguing that
the calendar readings are not selective. It is **complementary**, not contradictory:
"cosmic yes, arithmetic no, and here is *why* the counts are what they are."

It is **incompatible with the strong form** of Menghin's lunisolar reading, Schmidt-
Kaler's Venus reading, and any hypothesis that requires the disc counts to be
deliberately chosen to encode day-values. It does not contest that the hat is
cosmically symbolic, systematically structured, or ritually significant.

## What it means for the replica

The Stage-2 LED display could include a **"craft" mode**: zones light up coloured by
tool type, showing the 12+7 alternation as a design grammar and the counts as
following the circumference. This is the most honest reading: the hat is a model of
the cosmos, built by a goldsmith whose punch counts followed the geometry of the
cone, and the calendar numbers a modern scholar can find in the sums are a
consequence of that geometry.
