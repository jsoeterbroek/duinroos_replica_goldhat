# Theory: the sceptical reading — ornament, apophenia, or a wide idiom

**Authors:** Wolfhard Schlosser (2003), Andreas Fuls (2008), Heidi Peter-Röcher
(2023), plus the project's own assessments
(`theories/menghin_lunisolar.md`, `theories/schmidt_kaler_venus.md`).
**Sources:** `sources/schlosser_2003.md`, `sources/fuls_2008.md`,
`sources/peter_roecher_2023.md`.

## The claim

The gold hats are certainly **cosmic in iconography** (sun discs, crescent, eye,
wheels, Kivik hat, sun-cult context) and were certainly ritually important. But the
specific claim that their ornament is a **precise numerical calendar** is not
established, because:

1. **The numbers are easy to hit.** With ~19 zone values and free choice of blocks
   (and of "intercalary" zones), round calendar numbers appear at or near the rate
   chance predicts. Fuls 2008 computes this for all four hats: only *Schifferstadt*
   beats the null (synodic month, factor ≈ 2.1). For **Berlin**, the hit-rate tracks
   the random line (tropical year 0 % by contiguous blocks).
2. **The free parameter moves — and Menghin said so.** The intercalary set is
   `{5,7,16,17}` in 2000 and `{7,16,17}` in 2010 (see `theories/menghin_lunisolar.md`
   §6). Menghin 2000, p. 71 admits that plausible number products are to be expected
   "nur bei flexibler Handhabung der … 'Schaltzonen'". Schlosser 2003 quotes this
   and replies that this "demonstrates the cleverness of the authors, not the
   astronomical knowledge of the Bronze Age"; Peter-Röcher 2023 summarises it as
   "gerechnet wird also immer ausgehend vom gewünschten Ergebnis".
3. **The target month is not a constant.** The synodic month averages 29.5306 d, but
   the **lunar year varies by more than 26 hours (> 1 day)** from year to year
   (Schlosser 2003, Table 1967–2003). "Es gibt nicht 'das' Mondjahr schlechthin, und
   die Zahl 354 macht nur im Mittel Sinn — nicht im Einzelfall!" A running calendar
   of 354 marks would be wrong in most individual years. The Metonic rule holds only
   ~2/3 of the time in his sample, so "von 'exakt' kann nicht die Rede sein".
4. **The rule does not transfer.** Schlosser and Peter-Röcher both record that the
   calculation could **not** be applied to the other three hats; Peter-Röcher
   (2023, 135–136): "Auf die anderen drei bekannten Goldblechkegel … ließen sich die
   Rechenoperationen leider nicht übertragen." This is the cross-hat test failing
   in the literature, not just being blocked here.
5. **The unit is not selective.** Counting *plain symbols* lands on the calendar
   targets *more* often than counting rings (project scripts, Menghin §6), so
   "we found 365" is not evidence that rings are the intended unit.
6. **One artefact, many calendars.** Menghin: lunisolar. Schmidt-Kaler: Venus *and*
   Mercury. Lorenz: Metonic structure. When one object supports several unrelated
   systems, confidence in any one drops.
7. **The wider narrative is contested.** Schlosser and Peter-Röcher question the
   leap from "sky symbols" to "state/calendar apparatus"; the "archaeoastronomy
   proves the Bronze Age state" story is a popular construct.

## Status

**This is the best-supported position, and it is a negative one.** It is not
"nothing to see": it is "sky is certainly there; arithmetic is not demonstrated".
Since 2026-10-11 it is backed not only by the project's own null tests but by
Schlosser 2003 (the astronomy of the lunar year), Fuls 2008 (the combinatorial null)
and Peter-Röcher 2023 (the non-transfer to the other hats).

## What would confirm the sceptical reading

- The cross-hat test: apply a pre-registered rule blind to Schifferstadt,
  Ezelsdorf and Avanton and find it fails. The **data is now in hand** (Menghin
  2000's four per-zone tables, `data/readings/menghin2000_zones.json`, control C6),
  so this is a live script job (`todo/T2`) rather than a blocked one. Until it runs,
  Peter-Röcher's one-sentence "ließ sich leider nicht übertragen" is a **reported**
  failure, not a reproduced one.
- A committed re-run of Fuls's null reproducing his Berlin result.
- Showing Lorenz's 19/12+7 structure does not hold on the object.

## What would refute it

- A **pre-registered** counting rule that is selective on Berlin (beats ~95 % of
  shuffles) and that also works on a second hat.
- A demonstration that a correction zone is physically marked (spacing,
  orientation, a distinct tool) *before* the arithmetic is applied.

## Relation to craft-geometry (Soeterbroek/AI, 2026)

The craft-geometry hypothesis (`theories/craft_geometry.md`) extends this sceptical
position by providing a **positive mechanism** for the counts: the disc numbers are
determined by the circumference at each zone divided by the punch tool's
characteristic pitch. On Berlin, this predicts 14/16 shaft counts exactly
(`scripts/verify_craft_geometry.py`). The two positions are complementary: this file
argues "arithmetic not demonstrated"; craft-geometry explains *why* the counts are
what they are without invoking calendar intent.

## What it means for the replica

Show the readings as **readings**, name their authors, and keep the "which is
right?" question open. A museum-grade replica that says "here is one reading, and
here is why it is uncertain" is more honest and more interesting than one that
asserts a calendar. (Unchanged from `theories/menghin_lunisolar.md` §8.)
