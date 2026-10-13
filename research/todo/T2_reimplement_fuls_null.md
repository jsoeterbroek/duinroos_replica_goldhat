# T2 — re-implement Fuls 2008's combinatorial null

**Why:** Fuls's result (only Schifferstadt significant; Berlin ≈ chance) is now a
control (`controls/C4_fuls_null_result.md`), but it is trusted rather than
reproduced here. AGENTS.md's rule is that a negative needs a control *this
pipeline* can re-find.

**Task:** a script (e.g. `scripts/fuls_null.py`) that, for the 19 Berlin zones
3–21:
1. enumerates all non-empty subsets (method A), all same-symbol groups (B),
   all contiguous blocks (C), and contiguous blocks minus switch-zones (D);
2. counts hits within `t_p` of a multiple of the period, for the table of periods
   (sidereal/synodic month, solar month, tropical year, Mercury, Venus, Mars,
   Jupiter, Saturn);
3. computes `h = T/G` and the chance `w = 2·t_p/p`;
4. prints a before/after comparison against Fuls's published rates
   (`catalogues/fuls.md`).

**Progress:** ✔ **DONE 2026-10-13.** `scripts/fuls_null.py` implements methods A–D,
all nine periods and the chance baseline, and `--check` reproduces Fuls's published
tables. Run for all four hats as the cross-hat test. Finding:
`findings/FINDING_2026-10-13_fuls-null-reproduced.md`.

What it found: Berlin ≈ chance for every method/period; **only Schifferstadt,
method B, synodic month** is clearly above chance (16.13 % vs 6.77 %); Avanton and
Ezelsdorf ≈ chance. This reproduces Fuls's negative and Menghin's own "partiell"
admission (2010, p. 65).

Method-D formula recovered (the key to reproducing `G`): a contiguous block minus
*any subset* of the intercalary zones inside it, counting **distinct** zone sets;
Schaltzone = a zone whose stamp occurs only once. Berlin Schalt set
`{Z2,Z5,Z7,Z16,Z17}`; Z5 counted as 19 (K=1).

Remaining, low priority: our Menghin 2000 Abb. 27 transcription gives Ezelsdorf 12
stamp groups vs Fuls's 16, so Ezelsdorf B/D `G` differ; and Berlin Mars differs by
one hit (M=0 edge). Neither changes the conclusion.

**2026-10-12 — no longer blocked, and now extendable.** Menghin 2000's per-zone
tables for *all four* hats are on record (`data/readings/menghin2000_zones.json`,
control C6). So Fuls's null can be reproduced for Berlin *and* run as the real
cross-hat test on Schifferstadt, Avanton and Ezelsdorf — the test Peter-Röcher 2023
reports as having failed in print. Avanton zones 12–14 are reconstructions and
Ezelsdorf zone 21 is a reconstruction; both must be flagged or held out.

**Done when:** the Berlin method-B/D rates reproduce Fuls's within rounding, and
the script is committed. If they do not, one of the two is wrong and must be
found before the negative is used.
