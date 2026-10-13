# HANDOFF — research

Start here. Keep this current enough that a fresh session can continue.

## Where we are

2026-10-13. **Doc item #6** (novelty + write-up), running.

**Both Menghin monographs are now in the repo, complete and read.** The 2000
article (83 pages + text, `assets/menghin/2000/`) and the 2010 book (whole book,
pp. 1–88, `assets/menghin/2010/full/`) are ingested; their per-zone ornament data
is on record (`data/readings/menghin2000_zones.json`, controls C1/C6). The 2010
book's **"Der Vergleich"** chapter (pp. 64–72) is the important new material: on
p. 65 Menghin calls the cross-hat transfer only **partial**, and on p. 68 he states
that for **Ezelsdorf the stamp-identity rule yields no direct calendar values**.
The Ezelsdorf intercalary set also **moves between his own publications**
(`{5,6,19}` in 2000 → six green rows `{5,6,15,16,17,19}` in the 2010 table, five in
the 2010 text; 12 for Fuls). See
`findings/FINDING_2026-10-13_menghin-2010-ingested.md`.

## Running now

Nothing. The Menghin 2010 ingest round is complete as of this file.

## Next

1. Read `CASE.md` → `catalogues/README.md` → the `findings/` files. Then pick the
   top open item.
2. **Highest value next move** (see `todo/`):
   - **Re-run Fuls's combinatorial null locally** (`todo/T2`). It is now reproducible
     from Menghin 2000 data — methods A/C/D for Berlin and B for Schifferstadt land
     on Fuls's published table (method D reproduces all nine periods exactly, with
     Z5 counted as 19). Run it as the cross-hat test on all four hats. This is the
     test Menghin himself calls partial (p. 65) and Peter-Röcher says failed.
   - Skim **Menghin 2010 pp. 73–88** (Kalenderhüte / Der Kult / Literatur) — now in
     hand, unread.
   - Count **Lorenz's 19/12+7 structure** on the object (`todo/T4`).
   - Extract **Hansen & Rink 2008** from the Nuncius 8 PDF (`todo/T3`).
   - Obtain **Schauer 1986** (Leiden) and **Menghin 2003** catalogue chapter — no
     longer blockers for the counts.
3. Do **not** restart the archaeology; the question and controls are set.

## Gotchas

- **Menghin 2010 is complete, in `assets/menghin/2010/full/`** (jpg/ocr/text, 3-digit
  `pageNNN` names). The older `assets/menghin/2010/jpg/` (28 phone photos, pp. 20–31
  and 47–63) is kept because `IMPLEMENTATION_PLAN.md` reads it; **use `full/` for the
  research case.**
- **Menghin's counter is rings × symbols, not symbols.** `A`, `K` and `SK` are
  different columns of the same table. Never sum a Menghin `A` with a Menghin `SK`,
  and never sum either with Schmidt-Kaler's plain counts.
- **Menghin's own summary counts do not all close.** Berlin 418 vs 399 discs; the
  Ezelsdorf symbol totals; the Avanton 177 row; and the 2010 Z8 `A=40` print, which
  shifts the Ezelsdorf disc total from 432 (2000) to 433 (2010) while the ring sum
  stays 78. The **ring** sums reproduce everywhere; quote those, flag the symbol
  totals.
- **The Ezelsdorf intercalary set is not stable across Menghin's publications**
  (see above), and 2010's own table and text disagree. Berlin's `{7,16,17}` + Z5 is
  stable. Treat a cross-hat reading that depends on which zones are "Schalt" as
  under-specified until resolved.
- **Avanton zones 12–14 and Ezelsdorf zone 21 are reconstructions.** Flag or hold
  them out of any cross-hat test.
- The legacy AI digest invented an Ezelsdorf "1739 symbols" corroboration; the
  real figure is **499**, confirmed from the primary per-zone table (C5/C6). Do not
  re-import it.
- "Wolfgang Schlosser" (2004, 2012), "I. Mathieson 2010" and the joint
  "Spurk/Gebhard/Schauer" study do not appear in any index; see
  `sources/phantom_references.md`. Do not cite them without a page.
- Run the verify scripts before quoting any number: `scripts/verify_calendar.py`,
  `verify_scenarios.py`, `verify_venus_hypothesis.py`, `verify_menghin2000.py`.
  (`verify_venus_hypothesis.py` needs the venv at `scripts/`/project root.)
