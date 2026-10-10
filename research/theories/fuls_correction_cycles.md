# Theory: Fuls — correction-cycle arithmetic on the gold hats

**Author / date:** Andreas Fuls (TU Berlin), 2004 (extended 2008).
**Sources:** `sources/fuls_2004.md`, `sources/fuls_2008.md`.

## The claim

Menghin's basic move — read a zone's concentric rings × its symbols as days — is
right, but the **grouping must follow the ornament**: a legitimate cycle sums only
zones that share a decoration type. Under that constraint the four hats encode
lunar and solar cycles *plus explicit correction cycles*:

- Schifferstadt: 266 d ≈ 9 months (zones 3–8), 355 d ≈ 12 months (zones 2–9);
  corrections `92 × 266 − 22 = 24 450 d` (828 months) and
  `110 × 266 − 24 = 29 236 d` (990 months).
- Avanton: 177 d ≈ 6 months (zones 12–14); `46 × 104 = 4784 d` = 162 months.
- Berlin: the rounded double month (59 and 60: zones 9/11/13 and 10/12/14),
  the solar year 75+94+57+105+38 = 365, a **945-day** cycle `15 × 59 + 60`, and its
  47-fold correction `47 × 945` with one 944-day substitute — giving a mean month
  of 29.530 585 d, which Fuls himself calls **"unglaublich" and doubts**.
- Ezelsdorf: most cycles "ungenau"/"fragwürdig"; only 1461 d (4 yr, zones 6–21)
  and 1418 d (48 months) are "genau".

## Status

**Candidate — not a find.** The arithmetic is real and reproducible, and Fuls's
pattern-type constraint is a genuine improvement on Menghin. But in the very same
research programme Fuls (2008) ran the full combinatorial null and found that for
**Berlin the hit-rate is indistinguishable from chance**; only **Schifferstadt**
is statistically selective. Fuls 2004 is therefore best read as *the strongest
construction the arithmetic admits*, not as confirmation that it was intended.

## What would confirm

- Reproduce the Berlin 945-day and 47-fold cycles from `data/readings/menghin.json`
  (a scriptable check; not yet done).
- Show the correction zones are marked on the object by spacing or orientation.
- Find the same structure on Schifferstadt, where it *is* selective, and show the
  two objects are contemporary or directly related.

## What would refute

- Fuls 2008's own null: hit frequency ≈ chance for Berlin (already found).
- The fact that the "correction" zones and the 944/945 substitution are chosen
  from a set of possibilities — the same degrees of freedom Menghin is accused of.

## Relation to the other theories

It is a *steelman* of the lunisolar reading: same unit and object, stricter
grouping, and self-doubt at the crucial step. See `theories/menghin_lunisolar.md`
(§6 is the same null test) and `theories/schmidt_kaler_venus.md`.
