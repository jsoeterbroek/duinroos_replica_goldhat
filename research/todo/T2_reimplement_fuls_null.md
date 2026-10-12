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

**Progress:** not started. Small job — a day.

**2026-10-12 — no longer blocked, and now extendable.** Menghin 2000's per-zone
tables for *all four* hats are on record (`data/readings/menghin2000_zones.json`,
control C6). So Fuls's null can be reproduced for Berlin *and* run as the real
cross-hat test on Schifferstadt, Avanton and Ezelsdorf — the test Peter-Röcher 2023
reports as having failed in print. Avanton zones 12–14 are reconstructions and
Ezelsdorf zone 21 is a reconstruction; both must be flagged or held out.

**Done when:** the Berlin method-B/D rates reproduce Fuls's within rounding, and
the script is committed. If they do not, one of the two is wrong and must be
found before the negative is used.
