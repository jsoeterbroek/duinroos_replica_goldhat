# T4 — count Lorenz's 19 line-bands and 12 + 7 friezes on the object

**Why:** Lorenz's Metonic reading (`theories/lorenz_metonic.md`) is the most
**falsifiable** positive claim in the case: either the hat has 19 counting
line-bands and the disc friezes partition 12 + 7, or it does not. Unlike the
block-sum readings, it cannot be reached by choosing subsets — so it is worth
testing first.

**Task:**
1. Count the horizontal line-bands on `assets/berliner_goldhut_abrollung.jpg`
   (the unrolled view) and on the Museum photos.
2. Classify the disc friezes: large discs *with* small discs vs *without*. Does the
   count come to 12 and 7?
3. Compare against `data/zones.json` (21 zones) — do 19 line-bands even correspond
   to the zones, or are they frame lines?
4. Record the result as a finding either way (a clean negative is a finding).

**Progress:** ✔ **DONE 2026-10-13.** Finding:
`findings/FINDING_2026-10-13_t4-lorenz-structure.md`.

Results:
1. **Canonical count = 21 zones** (Menghin Abb. 14 / Abb. 23), of which **18** carry
   Scheibensymbole (Menghin p. 81). Lorenz's **19** is reproducible only as "the
   disc-bearing bands" (Z2–Z21 minus the crescent zone Z5), not as the measured zone
   count; the repo's abrollung drawing also labels 19 bands.
2. **12 + 7 is real as a ring-count split**: the 7 friezes with 5-ring discs (K=5:
   Z4, Z6, Z8, Z10, Z12, Z14, Z21) vs the 12 others. On the object the K=5 friezes
   are the packed discs and the K=3 ones the filler-linked friezes
   (`assets/Berlín_Goldhut_04.JPG`).
3. **The 235 is arithmetic** (12×12 + 7×13 for *any* 12+7 split), so it is not
   evidence; Lorenz also reuses Menghin's 19×5 = 235.

Verdict: partially reproducible, **not independent evidence**; the "19" conflicts
with the 21-zone canon unless redefined, and the one potentially selective element
(which friezes lack small fillers) is left loose by Lorenz's prose. Open: do the K=6
friezes (Z15, Z18, Z19) carry fillers? (decides 7 vs 10).

**Done when:** a number for line-bands and for each frieze class, with the images
named, and a finding note.

**Status 2026-10-13:** done — see above and the finding. The claim is not refuted
(the 12+7 split survives) but it is not the independent, selective test the theory
note hoped for.
