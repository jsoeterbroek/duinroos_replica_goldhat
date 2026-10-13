# Catalogue: Fuls's statistical results (how they were checked)

**What it is:** the published null-model results, so that a new statistical claim
can be checked against a prior one rather than re-invented.

**How checked:** **full read** of Fuls 2008 §8.4–8.6 on the page images
(`evidence/2008_wurzburg_fuls_goldhats_stats_conclusions_fuls2008_p123_full.jpg`,
`…_tables_fuls2008_p121_full.jpg`), and Fuls 2004 Tables 3–12.

## The catalogue (Fuls 2008, hit-rate `h` vs chance `w`)

| Hat | method | period | h | w | significant? |
|---|---|---|---|---|---|
| Schifferstadt | B | synodic month | 16.13 % | 6.77 % | **yes** (×2.1) |
| Schifferstadt | C/D | solar month | 10.14 % | 4.60 % | marginal; no systematics |
| Berlin | D | synodic month | 6.58 % | 6.77 % | no |
| Berlin | D | tropical year | 0.43 % | 0.55 % | no |
| Berlin | C | tropical year | 0 % | 0.55 % | no |
| Avanton | B | Venus | 1 hit (583 d) | — | inconclusive (incomplete hat) |
| Avanton | B | Jupiter | 402 d | ±4 d | inconclusive |

Search-space sizes (Berlin): method A = 1 048 575, B = 1023, C = 210, D = 699.

## What is *not* in it

- No confirmation that Berlin encodes a calendar; the opposite.
- No proof that it does not — Fuls's own caveat: a sparse true encoding could be
  hidden by the large search space.

## Reproduced locally (2026-10-13)

`scripts/fuls_null.py` re-implements methods A–D, the nine periods and formula 8.7,
and `--check` re-finds this table from the Menghin 2000 per-zone data (control C4).
Exact cells: Schifferstadt and Avanton A–D, Berlin C/D, Schifferstadt B/D. Two
documented deviations: Berlin's Mars cell is one hit high in Fuls (his table counts
the zone-5 sum `19 d` against `M = 0`, which formula 8.1 excludes), and Ezelsdorf
B/D `G` differ because our Abb. 27 transcription yields 12 stamp groups against
Fuls's 16. The cross-hat extension (same four methods on all four hats) confirms the
headline: only Schifferstadt method B × synodic month is above chance. See
`findings/FINDING_2026-10-13_fuls-null-reproduced.md`.

## Use

Any future "we found number X on the Berlin hat" claim must either (a) be
selective under a pre-registered rule, or (b) explain why it escapes Fuls's null.
A hit that merely matches `h ≈ w` is not a find.
