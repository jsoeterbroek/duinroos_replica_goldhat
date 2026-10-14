# FINDING_2026-10-13_t4-lorenz-structure

**Status:** verified (object images read; counts checked against the canonical
Menghin data)
**Sources / images:** Menghin 2000 Abb. 14 (`assets/menghin/2000/jpg/menghin_page045.jpeg`)
and Menghin 2010 Abb. 23 (`assets/menghin/2010/jpg/menghin_page030.jpeg`);
`data/readings/menghin2000_zones.json`; Lorenz's afterword
(`research/evidence/2020_lorenz_goldhut_metonic_nachtrag_lorenz2nd_p170_full.jpg`);
the object — `assets/Berlín_Goldhut_01.JPG` (upper shaft),
`assets/Berlín_Goldhut_04.JPG` (shaft close-up: packed vs filler friezes),
`assets/Cappello_d'oro_di_berlino,_1000_ac_ca._01.jpg` (whole hat),
`assets/Berlin_Gold_hat_calendar.jpg` (canonical 21-zone diagram),
`assets/berliner_goldhut_abrollung.jpg` (19-band drawing).
**Subject:** T4 — Lorenz's "19 line-bands and 12 + 7 friezes" Metonic reading.

## Lorenz's claim (read on p. 170)

> „So weist dieser insgesamt **19 Linienbänder** auf. Ebenso bilden die großen
> Scheibensymbole **12 Friese (verbunden mit kleinen Scheiben) und 7 Friese (ohne
> weitere Scheiben)**, zusammen also 19 Friese, die als Anzahl von Mondjahren
> (12 kurze, 7 lange) gewertet werden können."

with 12 × 12 + 7 × 13 = 235 lunations, plus the 19 special symbols of zone 5 and
Menghin's 19 × 5 = 235 as reinforcement.

## Result 1 — the canonical count is **21 zones**, not 19

Menghin's measured division (2000 Abb. 14, 2010 Abb. 23) is **21 ornament zones**:
Spitze Z1–Z2, Schaft Z3–Z16, Kalotte Z17–Z19, Krempe Z20–Z21. Of these, **18 carry
Scheibensymbole** (Z3, Z4, Z6–Z21) — Menghin's own count, „418 Scheibenmotive
(Nr. 8–15) über 18 horizontale Ornamentzonen" (2000, p. 81).

Lorenz's **19** is reproducible, but only under a *different definition*: the bands
that carry a stamped symbol, i.e. **Z2–Z21 minus the crescent Sonderzone Z5 = 19**.
So:

| reading | count |
|---|---|
| Menghin, all ornament zones | **21** |
| Menghin, disc-bearing friezes (Scheibensymbole) | **18** |
| disc-bearing bands incl. the apex Z2 (Doppelkreispunkt) | **19** |
| the repo's abrollung drawing, labelled bands | **19** (a drawing, not the object) |

"19 line-bands" is therefore **not the measured zone count**; it is "the bands that
carry stamped symbols", which excludes the apex star Z1 and the crescent zone Z5.
That is a defensible thing to count — but it is a redefinition, and Lorenz presents
it as *the* structure of the hat.

## Result 2 — the "12 + 7" split is real, as a **ring-count** division

The 19 disc-bearing friezes split by the number of concentric rings per disc (`K`),
from the transcribed measurement:

- **7 friezes have 5-ring discs (K = 5): Z4, Z6, Z8, Z10, Z12, Z14, Z21.**
- **12 friezes have other ring counts (K = 2, 3 or 6).**

On the object the K=5 friezes are the **large, tightly packed discs** (no filler), and
the K=3 friezes are smaller discs **linked by the small annulets** (Musterpunzen Nr. 7)
— exactly the visible difference between `Berlín_Goldhut_04.JPG`'s packed and
filler-linked bands, and between the alternating friezes of the abrollung. So
Lorenz's **12 + 7 = 19 is reproduced by the ring-count partition**, provided all the
non-K=5 friezes really do carry small fillers.

**One caveat, not resolved here:** the K=6 friezes (Z15, Z18, Z19) are the largest
discs; whether they are packed (no small discs) or filler-linked decides whether the
"without small discs" class is 7 or 10. At the available resolution this is not
certain, and Lorenz's prose („verbunden mit kleinen Scheiben") does not define the
class precisely. The *ring-count* split is objective; Lorenz's *description* of it is
not quite.

## Result 3 — the Metonic 235 adds nothing

**12 × 12 + 7 × 13 = 235 for any partition of 19 into 12 and 7.** The 235 is
arithmetic, not a measurement: it follows automatically once one has 19 and a 12+7
split, so it cannot be evidence for the Metonic cycle. Lorenz also explicitly reuses
Menghin's 19 × 5 = 235, so the number is not independent.

## Verdict

Lorenz's structural reading is **partially reproducible but not established, and not
independent evidence**:

- the **19** is a redefinition (disc-bearing bands), which conflicts with the measured
  **21**-zone division unless one accepts the narrower definition;
- the **12 + 7** partition is real as the K=5 vs rest ring-count split of the 19
  disc-bearing friezes — this is the strongest part of his claim and it does survive;
- the **235** is arithmetic, so it neither confirms nor refutes anything.

It does **not** refute the calendar hypothesis, and it does **not** provide the
"selective by construction" support the theory note hoped for: his partition is
derived from Menghin's ring counts, not measured independently, and the one element
that would be selective (which friezes lack fillers) is the element his prose leaves
loose.

## Checks

- [x] Read Lorenz on the page image (p. 170)
- [x] Canonical 21 zones from Menghin Abb. 14 / Abb. 23 and `menghin2000_zones.json`
- [x] 18 Scheibenfriese from Menghin's own text (p. 81); 19 = + apex Z2
- [x] K=5 count = 7 verified against the data; 12+7 = 19
- [x] Object read for packed vs filler friezes
      (`Berlín_Goldhut_01/04.JPG`, `Cappello…jpg`, abrollung)
- [x] The 235 shown to be an arithmetic identity of any 12+7 split
- [x] Negative/uncertain states reported (K=6 fillers unresolved; "19" is a definition)

## Evidence

- Object: `assets/Berlín_Goldhut_04.JPG` (packed vs filler friezes),
  `assets/Berlín_Goldhut_01.JPG`, `assets/Cappello_d'oro_di_berlino,_1000_ac_ca._01.jpg`,
  `assets/berliner_goldhut_abrollung.jpg` (19 bands), `assets/Berlin_Gold_hat_calendar.jpg`.
- Canon: `assets/menghin/2000/jpg/menghin_page045.jpeg`,
  `assets/menghin/2010/jpg/menghin_page030.jpeg`.
- Lorenz: `research/evidence/2020_lorenz_goldhut_metonic_nachtrag_lorenz2nd_p170_full.jpg`.

## Open questions

- Do the K=6 friezes (Z15, Z18, Z19) carry the small filler punze? Needs the Menghin
  plates at higher resolution or Schauer 1986 (Leiden). Decides 7 vs 10 for the
  "without small discs" class.
- Is Lorenz's "19 Linienbänder" meant as the disc-bearing bands, or as actual
  horizontal frame lines (Rippen/Wülste)? Only the former matches 19.
