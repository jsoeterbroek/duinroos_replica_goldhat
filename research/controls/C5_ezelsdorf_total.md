# Control C5 — the Ezelsdorf-Buch total is ≈ 499, not 1739

**What:** the cross-hat test needs the *other* hats' counts. The earlier AI digest
reported Ezelsdorf as "≈ 1,739 symbols in 23 bands" — the same total as Berlin.
That is false and it manufactures independent corroboration that does not exist.

**Expected:**
- Ezelsdorf-Buch: ≈ **499** stamped symbols over ≈ **19** ornament zones
  (Wolfram Kaiser's plate *Übersicht der Ornamentzonen und verwandten
  Hauptmusterpunzen*, 2005, redrawn from Schauer 1986 and Menghin 2000).
- The ≈ 1739 figure is Berlin's **ring-unit** total and must not appear as an
  Ezelsdorf symbol count.

**How to re-find:** the count is transcribed in `theories/menghin_lunisolar.md`
§6, Result 1; the underlying plate is in that file's source list. Primary counts
still need Schauer 1986 (`sources/schauer_1986.md`).

**Result 2026-10-12:** ✔ **primary count obtained.** Menghin 2000, Abb. 27, p. 61
(`assets/menghin/2000/jpg/menghin_page061.jpeg`) gives the Ezelsdorf per-zone table;
its `A` column sums to **499** stamped symbols over zones **2–20** — that is 432
disc symbols (zones 3–20) + 22 eye motifs (Z 15) + 21 wheel motifs (Z 17) + 24 small
bosses (Z 2) — i.e. exactly the ≈ 499 of the secondary plate, now from the primary
source. The rim zone 21 (33 more, a reconstruction) is excluded. Verification:
`scripts/verify_menghin2000.py` (control C6).

**Unit note, now settled:** Ezelsdorf's **rings** total is 1463 (zones 3–20, no rim)
and 1694 (with Menghin's reconstructed rim), and its **Zeichen** total is 1737 with
the reconstructed rim. None of these is 1739 — that is Berlin's. The phantom
digest's "1,739 symbols" remains rejected.

**If missed:** check the unit — a symbol count vs a ring-unit count vs a zone
count. This control exists precisely to catch unit contamination.
