# HANDOFF — research

Start here. Keep this current enough that a fresh session can continue.

## Where we are

2026-10-12. **Doc item #6** (novelty + write-up), running.

**Menghin 2000 is now in the repo, complete and ingested.** The project author
digitised the whole article; 83 page images + text are in `assets/menghin/2000/`,
and its **four per-zone ornament tables (Berlin, Schifferstadt, Avanton, Ezelsdorf)**
are transcribed into `data/readings/menghin2000_zones.json`, verified by control
**C6** (`scripts/verify_menghin2000.py`). This unblocks the cross-hat test for three
of the four hats. The two critical papers (Schlosser 2003, Peter-Röcher 2023) are held
and read. Findings index in `findings/README.md`; the newest beat has the detail:
`findings/FINDING_2026-10-12_menghin-2000-ingested.md`.

## Running now

Nothing. The Menghin 2000 ingest round is complete as of this file.

## Next

1. Read `CASE.md` → `catalogues/README.md` → the `findings/` files. Then pick the
   top open item.
2. **Highest value next moves** (see `todo/`):
   - **Re-run Fuls's combinatorial null** as a committed script (`todo/T2`) — now
     for all four hats, not just Berlin. This is the cross-hat test Peter-Röcher says
     failed in print; the raw data is in hand.
   - Count **Lorenz's 19/12+7 structure** on the object (`todo/T4`).
   - Extract **Hansen & Rink 2008** from the Nuncius 8 PDF (`todo/T3`).
   - Obtain **Schauer 1986** (Leiden) for the plates/tool metrology — no longer a
     blocker for the counts.
   - Fill the **Menghin 2010** gaps (pp. 1–19, 26, 32–46, 64–end).
3. Do **not** restart the archaeology; the question and controls are set.

## Gotchas

- **`assets/menghin/2000/` is now populated** (`pdf/`, `jpg/`, `ocr/`, `text/`).
  `menghin_page106b.jpeg` is a duplicate of p. 106 — nothing is missing. Page names
  are printed page numbers; the front matter is `cover/imprint/toc/plate`.
- **Menghin's counter is rings × symbols, not symbols.** `A`, `K` and `SK` are
  different columns of the same table. Never sum a Menghin `A` with a Menghin `SK`,
  and never sum either with Schmidt-Kaler's plain counts.
- **Menghin's own summary counts do not all close** (418/399, 474/505/462,
  the Avanton 177 row). `scripts/verify_menghin2000.py` prints the deltas as WARN.
  The **ring** sums reproduce everywhere; quote those, flag the symbol totals.
- **Avanton zones 12–14 and Ezelsdorf zone 21 are reconstructions.** Flag or hold
  them out of any cross-hat test.
- The legacy AI digest invented an Ezelsdorf "1739 symbols" corroboration; the
  real figure is **499**, now confirmed from the primary per-zone table (C5/C6).
  Do not re-import it.
- "Wolfgang Schlosser" (2004, 2012), "I. Mathieson 2010" and the joint
  "Spurk/Gebhard/Schauer" study do not appear in any index; see
  `sources/phantom_references.md`. Do not cite them without a page.
- Run the verify scripts before quoting any number: `scripts/verify_calendar.py`,
  `verify_scenarios.py`, `verify_venus_hypothesis.py`, `verify_menghin2000.py`.
  (`verify_venus_hypothesis.py` needs the venv at `scripts/`/project root.)
