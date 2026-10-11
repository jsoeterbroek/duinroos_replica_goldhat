# HANDOFF — research

Start here. Keep this current enough that a fresh session can continue.

## Where we are

2026-10-11. **Doc item #6** (novelty + write-up), running.

The three legacy documents have been consolidated into the `AGENTS.md` folder
taxonomy, and the source base has been augmented. As of 2026-10-11 the two
critical papers (Schlosser 2003, Peter-Röcher 2023) are held and read; the
published critique is now on record 
(`findings/FINDING_2026-10-11_schlosser-peter-roecher-critique.md`). The
`assets/menghin/` reorg paths have been repaired across the repo.

## Running now

Nothing. The consolidation round is complete as of this file.

## Next

1. Read `CASE.md` → `catalogues/README.md` → the `findings/` files. Then pick the
   top open item.
2. **Highest value next moves** (see `todo/`):
   - **Digitize Menghin 2000 and the 2010 gaps** — the author has both in print;
     the detailed priority/format plan is in `todo/T1_obtain_print_sources.md`.
     Menghin 2000 (the comparative study) is the priority for the cross-hat test.
   - Obtain **Schauer 1986** (Leiden University Library) — the raw non-Berlin data.
   - Re-run **Fuls's combinatorial null** as a committed script (`todo/T2`).
   - Count **Lorenz's 19/12+7 structure** on the object (`todo/T4`).
   - Extract **Hansen & Rink 2008** from the Nuncius 8 PDF (`todo/T3`).
3. Do **not** restart the archaeology; the question and controls are set.

## Gotchas

- **`assets/menghin/` was reorganised** (2026-10-11) into `<year>/{jpg,ocr,text}`;
  references were repaired to `assets/menghin/2010/...`. The `2000/` folders are
  empty placeholders awaiting digitization.
- The legacy AI digest invented an Ezelsdorf "1739 symbols" corroboration; the
  real figure is ≈ 499. Do not re-import it.
- "Wolfgang Schlosser" (2004, 2012), "I. Mathieson 2010" and the joint
  "Spurk/Gebhard/Schauer" study do not appear in any index; see
  `sources/phantom_references.md`. Do not cite them without a page.
- Two different counting units live in this case: **rings × symbols (day-values,
  Menghin)** and **plain ornament counts (Schmidt-Kaler)**. They must never be
  summed together — `data/readings/` flags both.
- `verify_venus_hypothesis.py` needs the venv at `scripts/`/project root; run the
  three verify scripts before quoting any number.
