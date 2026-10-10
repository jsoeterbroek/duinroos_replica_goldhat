# HANDOFF — research

Start here. Keep this current enough that a fresh session can continue.

## Where we are

2026-10-10. **Doc item #6** (novelty + write-up) of the plan in `CASE.md`.

The three legacy documents have been consolidated into the `AGENTS.md` folder
taxonomy: the two reasoning documents are now `theories/menghin_lunisolar.md` and
`theories/schmidt_kaler_venus.md`; the AI-written digest is
`theories/secondary_digest_2026-10-08.md`, kept as an untrusted secondary source
and corrected. New sources (Fuls 2004/2008, Amendola 2021, Lorenz 2010/2011,
Schlosser 2003, Peter-Röcher 2023, Randsborg 2006, Hansen & Rink 2008) are in
`sources/`, summarised in the theory files and scored in the findings.

## Running now

Nothing. The consolidation round is complete as of this file.

## Next

1. Read `CASE.md` → `catalogues/README.md` → the `findings/` files. Then pick the
   top open item.
2. **Highest value next moves** (see `todo/`):
   - Obtain **Schauer 1986** and **Menghin 2010** (print-only) — they hold the raw
     per-zone ring counts and zone order for Ezelsdorf-Buch, without which the
     cross-hat test stays blocked.
   - Re-run **Fuls's combinatorial null** as a committed script
     (`scripts/`), so the negative result is reproducible here rather than trusted.
   - Extract **Hansen & Rink 2008** from the same Nuncius 8 PDF as Fuls.
   - Get the **Peter-Röcher 2023** PDF (Würzburg repository or interlibrary).
3. Do **not** restart the archaeology; the question and controls are set.

## Gotchas

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
- Heidelberg's JSMV PDF (Schlosser) is behind an Anubis JS challenge; a plain
  `curl` returns an HTML placeholder, not the PDF.
