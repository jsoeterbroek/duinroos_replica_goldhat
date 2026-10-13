# RUN 2026-10-13 — T2, Fuls's combinatorial null reproduced and run as cross-hat

## What ran

- Wrote `scripts/fuls_null.py`: Fuls's methods A–D over the Menghin 2000 per-zone
  counters, the nine periods/tolerances of his Table 8.1, and the chance baseline
  `w = 2·t_p/p` (formula 8.7). `--check` compares our T/G with Tables 8.2–8.5.
- Recovered the method-D combinatorics: a contiguous block minus any subset of the
  intercalary zones inside it, counting **distinct** zone sets; Schaltzone = a zone
  whose stamp occurs once. `G` = 699 (Berlin), 69 (Schifferstadt), 111 (Avanton).
- Ran it for all four hats (cross-hat test) and read off h vs w.
- Fixed one transcription error found on the way: Schifferstadt Z3/Z4 are
  **Musterpunze 5**, not 3 (`data/readings/menghin2000_zones.json`; Abb. 17, p. 50).
- Re-ran control C6 (`verify_menghin2000.py`) — still clean.
- Wrote `findings/FINDING_2026-10-13_fuls-null-reproduced.md`; updated control C4,
  catalogues/fuls, todo/T2, findings/README, controls/README, CASE, HANDOFF.

## Funnel

| Stage | Count |
|---|---|
| Methods implemented | 4 (A–D) |
| Periods tested | 9 |
| Hats tested | 4 |
| Published cells compared | 16 (4 methods × 4 hats) |
| Exact reproductions | 12 |
| Documented deviations | 2 + 2 cells (Berlin Mars M=0; Ezelsdorf B/D typology) |
| Transcription errors found and fixed | 1 (Schifferstadt Z3/Z4 stamp) |

## Model roles and cost

No model APIs invoked (local Python + page-image read). **$0.00.**

## Result

1. **Control C4 is now reproduced by script, not taken on trust.** `--check` exits 0.
   Berlin A/C/D and Schifferstadt/Avanton A–D reproduce; Berlin A/B differ by one
   Mars hit, explained (the zone-5 sum `19 d` inside the ±20 d tolerance of `M = 0`,
   which formula 8.1 forbids).
2. **The cross-hat test confirms the negative.** Only Schifferstadt method B ×
   synodic month is clearly above chance (16.13 % vs 6.77 %); Berlin, Avanton and
   Ezelsdorf lie on the chance line. The rule does not selectively transfer.
3. **Method B for Berlin reproduces** once multiplicities are weighted by
   combination count — an earlier failure was a bug in the exploratory script, not
   in Fuls's table.

## Next

- Optional: re-transcribe Ezelsdorf Abb. 27's 16 Muster columns so method B/D compare
  cell-for-cell (does not change the conclusion).
- Optional: re-run with Avanton Z12–14 and Ezelsdorf Z21 held out as reconstructions.
- `todo/T4` (Lorenz 19 / 12+7) and `todo/T3` (Hansen & Rink 2008) remain open.
