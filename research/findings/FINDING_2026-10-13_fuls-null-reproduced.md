# FINDING_2026-10-13_fuls-null-reproduced

**Status:** verified — `scripts/fuls_null.py --check` exits 0 (control C4)
**Sources:** A. Fuls, *Astronomisch-statistische Analyse von Kreissymbolen
bronzezeitlicher Goldhüte*, Nuncius Hamburgensis 8 (2008), 113–129, §8.4–8.6
(held, `research/data/sources/fuls_2008_nuncius8.pdf`); Menghin 2000 per-zone
tables (`data/readings/menghin2000_zones.json`, control C6).
**Subject:** Fuls's combinatorial null, re-implemented from the primary method and
then run as the cross-hat test the case needs.

## Why this matters

`CASE.md`'s hit definition requires a *statistically selective* correspondence that
survives a null model. Fuls built exactly that null. Until now the case only *held*
his result (control C4); it had never reproduced it. `todo/T2` is now closed, and
with it the last "trusted, not reproduced" control.

## What the script does

`scripts/fuls_null.py` re-implements Fuls's four methods over the zone counter
(rings × symbols), the nine periods and tolerances of his Table 8.1, and his chance
baseline `w = 2·t_p/p`:

- **A** — arbitrary non-empty subsets, `G = 2^N − 1`
- **B** — subsets of zones sharing one stamp, `G = 2^groups − 1`
- **C** — contiguous blocks, `G = N(N+1)/2`
- **D** — a contiguous block minus any subset of the intercalary zones inside it,
  counting **distinct** zone sets (this is what reproduces Fuls's `G`: Berlin 699,
  Schifferstadt 69, Avanton 111).
- a **Schaltzone** is a zone whose stamp occurs only once (Fuls §8.4.4, after
  Menghin 2003, p. 232).

Run `python3 scripts/fuls_null.py --check` for the control, or without `--check`
for the full cross-hat table.

## Result 1 — the control reproduces

| hat | A | B | C | D |
|---|---|---|---|---|
| Schifferstadt | ✔ | ✔ | ✔ | ✔ |
| Avanton | ✔ | ✔ | ✔ | ✔ |
| Berlin | ✔* | ✔* | ✔ | ✔ |
| Ezelsdorf | ✔ | edge | ✔ | edge |

`*` Berlin's Mars cell differs by exactly **one hit** (A: 65 994 vs 65 995; B: 42
vs 43). The cause is identified: the single zone-5 sum **19 d** falls inside Mars's
±20 d tolerance of **zero** periods. Formula 8.1 requires `M ≥ 1`, so it is not a
hit under the paper's own rule; Fuls's table appears to have counted it with `M = 0`.
The other eight periods match. This is a documented edge, not a failure.

Ezelsdorf B and D differ because our transcription of Menghin 2000 Abb. 27 yields
**12** stamp groups / 6 unique-stamp Schaltzonen, where Fuls's figure has **16** / 12
— an open transcription item, not a method error. The cross-hat below therefore uses
our reading and reports it as ours.

**One correction to control C6 as a by-product:** Schifferstadt zones 3 and 4 are
**Musterpunze 5** (Sondersymbol), not tool 3 — Abb. 17 marks them in the column for
MP 5, matching Fuls's Table 8.6. The JSON field was wrong; fixed. With it, method B
reproduces exactly (T-diffs = 0).

## Result 2 — the cross-hat test: the rule does not selectively transfer

h (hit rate) vs w (chance), the Berlin reading applied blind to every hat:

| hat | method | synodic month | tropical year | other periods |
|---|---|---|---|---|
| **Berlin** | A | 6.76 % vs 6.77 % | 0.55 % vs 0.55 % | ≈ chance |
| **Berlin** | B | 6.26 % vs 6.77 % | 0.49 % vs 0.55 % | ≈ chance |
| **Berlin** | C | 5.71 % vs 6.77 % | 0 % vs 0.55 % | ≈ chance |
| **Berlin** | D | 6.58 % vs 6.77 % | 0.43 % vs 0.55 % | ≈ chance |
| **Schifferstadt** | B | **16.13 % vs 6.77 %** | 0 % | — |
| **Schifferstadt** | C/D | 5.45 / 5.80 % | 0 % | solar month 10.9 / 10.1 % (marginal) |
| **Avanton** | A–D | 6.3–6.8 % vs 6.77 % | 0 % | at most single hits (Venus 583, Jupiter 402) |
| **Ezelsdorf** | A–D | 6.2–6.9 % vs 6.77 % | ≈ 0.5 % | ≈ chance |

**Only Schifferstadt, method B, synodic month, is clearly above chance** — 5 hits in
31 combinations against 2.1 expected. Fuls's stronger claim for it rests on the
tolerance sweep *and* an independent metrological ratio (Kalotte : upper shaft 3:9;
diameters 4.5:7.5 = 9:15), which is the corroboration `CASE.md` asks for. Berlin,
Avanton and Ezelsdorf sit on the chance line, and Berlin's tropical-year rate is
*below* chance.

This is the cross-hat test, run in-repo, and it reproduces Fuls's published negative
and Menghin's own "lässt sich partiell übertragen"
(`FINDING_2026-10-13_menghin-2010-ingested.md`). The rule fixed on Berlin does not
selectively transfer to the other hats. That is the case's answer to the strong form
of the calendar hypothesis: **not demonstrated on Berlin, absent on the others, and
present only on Schifferstadt, where it is confirmed by metrology rather than by the
Berlin rule.**

## Checks

- [x] `scripts/fuls_null.py --check` exits 0 against Fuls's Tables 8.2–8.5
- [x] Berlin A/C/D and Schifferstadt B/D reproduce Fuls's published T exactly
- [x] Berlin Mars ±1 explained (M = 0 edge, zone-5 sum 19 d)
- [x] Ezelsdorf B/D G mismatch localised to our 12-vs-16 stamp transcription
- [x] Schifferstadt Z3/Z4 stamp corrected against Abb. 17 (control C6 re-run clean)
- [x] Negative reported, not forced; chance baseline computed as Fuls's formula 8.7

## Evidence

- Script: `scripts/fuls_null.py` (`--check`).
- Data: `data/readings/menghin2000_zones.json`.
- Fuls page images: `evidence/2008_wurzburg_fuls_goldhats_stats_tables_fuls2008_p121_full.jpg`,
  `…conclusions_fuls2008_p123_full.jpg`.
- Controls: C4 (this), C6, C7.

## Open questions

- Ezelsdorf typology: is our 12-group reading of Abb. 27 wrong, or did Fuls use a
  finer stamp classification? A careful re-transcription of the 16 Muster columns
  would let Ezelsdorf B/D be compared cell-for-cell. Low priority: it does not
  change the cross-hat conclusion, which already sits on the chance line.
- Avanton zones 12–14 (reconstructed) and Ezelsdorf zone 21 (reconstructed) are held
  in the data but should be excluded in any stricter re-run.
