# RUN 2026-10-11 — ingest the two critical sources

## What ran

- **Ingest** of the two PDFs the project author obtained under `todo/T1`:
  Schlosser 2003 (JSMV 86) and Peter-Röcher 2023 (BUFM 106). Extracted to text
  with PyMuPDF and read.
- **Path repair**: the `assets/menghin/` reorg (flat → `2010/{jpg,ocr,text}`)
  broke every reference; 16 files updated to the new layout.
- Wrote `findings/FINDING_2026-10-11_schlosser-peter-roecher-critique.md`; updated
  `sources/schlosser_2003.md`, `sources/peter_roecher_2023.md`,
  `theories/sceptical_ornament.md`, `CASE.md`, `sources/README.md`,
  `findings/README.md`, `candidates/CANDIDATES.md`, `NARRATIVE.md`, `todo/T1`.

## Funnel

| Stage | Count |
|---|---|
| New PDFs in hand | 2 |
| Extracted + read | 2 |
| Findings written | 1 |
| Files path-repaired | 16 |

## Model roles and cost

No model APIs invoked (local extraction + human read). **$0.00.**

## Result

The published critique is now in the record and is stronger than the repo's own
null test alone:
- **Schlosser 2003** — the lunar year varies by **>26 h**; 354 is a mean, not a
  per-year count; the Metonic rule holds ~2/3 of the time.
- **Peter-Röcher 2023** — the calculation **could not be transferred** to the other
  three hats; "gerechnet wird … immer ausgehend vom gewünschten Ergebnis".
- Recorded tension (not flattened): her "wenige verwertbare" for Schifferstadt vs
  Fuls 2008's statistically **significant** Schifferstadt result.

## Next

`todo/T2` (re-implement Fuls's null) and `todo/T4` (count Lorenz's 19/12+7). The
Menghin digitization plan is now written up in `todo/T1` (answer to the author's
question).

## Log / notes

- Tension to watch: Schlosser's variable-lunar-year attack targets the *lunar-year*
  reading, not the *solar/Metonic interval* reading. Keep the two separate.
