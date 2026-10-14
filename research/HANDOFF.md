# HANDOFF — research

Start here. Keep this current enough that a fresh session can continue.

## Where we are

2026-10-13. **Doc item #6** (novelty + write-up), running.

**Both Menghin monographs are now in the repo, complete and read**, and the
**cross-hat test has been run**. The 2000 article (83 pages + text,
`assets/menghin/2000/`) and the 2010 book (whole book, pp. 1–88,
`assets/menghin/2010/`) are ingested; their per-zone ornament data is on record
(`data/readings/menghin2000_zones.json`, controls C1/C6/C7).

Two results now stand. **(1)** Menghin's own 2010 comparison chapter (pp. 64–72)
calls the transfer *partial* (p. 65) and says the stamp-identity rule gives no direct
values on Ezelsdorf (p. 68). **(2)** Fuls's combinatorial null is re-implemented
(`scripts/fuls_null.py --check` exits 0) and run as the cross-hat test: only
**Schifferstadt, method B, synodic month** is above chance (16.13 % vs 6.77 %);
Berlin, Avanton and Ezelsdorf lie on the chance line. Findings:
`findings/FINDING_2026-10-13_menghin-2010-ingested.md`,
`findings/FINDING_2026-10-13_fuls-null-reproduced.md`.

## Running now

Nothing. The T2 round (Fuls null + cross-hat) is complete as of this file.

## Next

1. Read `CASE.md` → `catalogues/README.md` → the `findings/` files. Then pick the
   top open item.
2. **Open items** (see `todo/`):
   - Skim **Menghin 2010 pp. 73–88** (Kalenderhüte / Der Kult / Literatur) — in hand,
     unread.
   - Count **Lorenz's 19 line-bands and 12+7 friezes** on the object — ✔ **done**
     (`todo/T4`, `findings/FINDING_2026-10-13_t4-lorenz-structure.md`): 19 holds only
     as "disc-bearing bands" (measured: 21 zones); the 12+7 split is real (7 five-ring
     vs 12 other friezes); the 235 is arithmetic.
   - Extract **Hansen & Rink 2008** — abstract held; chapter outstanding (`todo/T3`).
     Obtain ch. 9 (pp. 131 ff.) or the 2014 Tübingen 32/33 paper.
   - Optional: re-transcribe Ezelsdorf Abb. 27's 16 Muster columns (Ezelsdorf B/D
     currently compare only under our 12-group reading).
   - Obtain **Schauer 1986** (Leiden) and **Menghin 2003** catalogue chapter — no
     longer blockers for the counts.
3. Do **not** restart the archaeology; the question and controls are set. The
   Stage-2 exhibit can now show the honest state: counting is real, the calendar
   reading is a *hypothesis*, selective only on Schifferstadt, and not transferable.

## Gotchas

- **Menghin 2010 is complete, in `assets/menghin/2010/`** (jpg/ocr/text, 3-digit
  `pageNNN` names; flattened from `2010/full/` on 2026-10-14). The older
  `assets/menghin/2010/jpg/` phone-photo selection (pp. 20–31 and 47–63) was removed
  in the same reorg — the full scan supersedes it, so use the single tree for everything.
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
