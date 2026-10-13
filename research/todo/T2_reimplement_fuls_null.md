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

**Progress:** not started as a committed script.

**2026-10-13 — the method is recovered, and three of four methods reproduce.**
Working from Menghin 2000's Berlin table (Z5 counted as **19**, not 38) and Fuls's
Schaltzone rule (a zone whose symbol type occurs only once):
- **Method A** (all subsets, G=1048575): Berlin T matches Fuls on 8 of 9 periods
  (Mars off by one hit, a tolerance-edge artefact).
- **Method C** (contiguous blocks, G=210): exact.
- **Method D** (contiguous blocks minus any subset of the Schaltzonen, counting
  *distinct* zone sets; G=699 with Schaltzonen `{Z2,Z5,Z7,Z16,Z17}`): **exact on all
  nine periods** (sid 58, syn 46, son 34, trop 3, Mercury 13, Venus 15, Mars 27,
  Jupiter 12, Saturn 1).
- **Method B** (subsets of same-symbol-type groups): exact for **Schifferstadt**
  (the published 16.13 % vs 6.77 % synodic-month result re-finds), but **not** for
  Berlin — the published Berlin method-B row (87/64/64…, G=1023) does not follow
  from the 10 Berlin type groups, so Fuls's Berlin method-B grouping/values are
  still unexplained. Do **not** quote the Berlin method-B row until this is resolved.

So the script is a small job now: encode the four methods, print the before/after
against `catalogues/fuls.md`, and settle the Berlin method-B gap. Method D is the
one that matches Menghin's own "geordnete Zonen mit Schaltzonen" procedure and is the
cleanest cross-hat instrument.

**2026-10-12 — no longer blocked, and now extendable.** Menghin 2000's per-zone
tables for *all four* hats are on record (`data/readings/menghin2000_zones.json`,
control C6). So Fuls's null can be reproduced for Berlin *and* run as the real
cross-hat test on Schifferstadt, Avanton and Ezelsdorf — the test Peter-Röcher 2023
reports as having failed in print. Avanton zones 12–14 are reconstructions and
Ezelsdorf zone 21 is a reconstruction; both must be flagged or held out.

**Done when:** the Berlin method-B/D rates reproduce Fuls's within rounding, and
the script is committed. If they do not, one of the two is wrong and must be
found before the negative is used.
