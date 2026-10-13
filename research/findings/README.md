# findings

`FINDING_<date>_<slug>.md`, from `templates/FINDING.md`. Status candidate until read
on the page image.

| Finding | Status | One line |
|---|---|---|
| `FINDING_2026-10-10_berlin-counts-solid.md` | verified | Menghin's counts (1739 = 1701 + 38) reproduce |
| `FINDING_2026-10-10_fuls-statistics.md` | verified | Fuls 2008: only Schifferstadt is statistically selective; Berlin ≈ chance |
| `FINDING_2026-10-10_ezelsdorf-total-correction.md` | verified | Ezelsdorf has ≈ 499 symbols, not Berlin's 1739 |
| `FINDING_2026-10-11_schlosser-peter-roecher-critique.md` | verified | Schlosser: the lunar year varies >1 day; Peter-Röcher: the rule does not transfer to the other hats |
| `FINDING_2026-10-10_phantom-references.md` | rejected (negative) | three brief citations do not exist |
| `FINDING_2026-10-12_menghin-2000-ingested.md` | verified | Menghin 2000 read complete: the four per-zone tables are on record; Ezelsdorf = 499 symbols from the primary source; three of his own totals flagged |
| `FINDING_2026-10-13_menghin-2010-ingested.md` | verified | Whole Menghin 2010 ingested; he calls the cross-hat transfer only *partial* and says the stamp rule gives no direct values on Ezelsdorf; the Ezelsdorf intercalary set moves between his publications |
| `FINDING_2026-10-13_fuls-null-reproduced.md` | verified | Fuls's combinatorial null re-implemented (`scripts/fuls_null.py --check` exits 0); run as the cross-hat test, only Schifferstadt method B × synodic month exceeds chance; Berlin/Avanton/Ezelsdorf ≈ chance |
| `FINDING_2026-10-13_hansen-rink-abstract.md` | abstract held | T3: the Fuls PDF is Fuls-only, Hansen & Rink ch. 9 (p. 131 ff.) is not held; their 2013 abstract confirms the eclipse/Metonic line includes the Berlin hat, but the per-zone 32/33 check is outstanding |

Controls behind these: `../controls/`. Runs: `../runs/RUN_2026-10-10_consolidation.md`,
`../runs/RUN_2026-10-11_ingest_critique.md`, `../runs/RUN_2026-10-12_ingest_menghin2000.md`,
`../runs/RUN_2026-10-13_ingest_menghin2010.md`, `../runs/RUN_2026-10-13_fuls_null.md`.
