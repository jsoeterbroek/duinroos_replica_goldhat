# controls

Known results the pipeline must re-find. One file per control; per-run recall in
`../runs/`. **A negative result without a control is not a result.**

| Control | What must be re-found | Status |
|---|---|---|
| `C1_menghin_counts.md` | 1739 = 1701 + 38; 418 discs; 745.0 mm | ✔ `verify_calendar.py` |
| `C2_menghin_scenarios.md` | 16 scenario blocks; 61.2 / 64.4 flagged | ✔ `verify_scenarios.py` |
| `C3_schmidt_kaler_sums.md` | 292 = 57+235; 146; 117 | ✔ `verify_venus_hypothesis.py` |
| `C4_fuls_null_result.md` | Berlin ≈ chance; only Schifferstadt significant | ✔ by page image (script pending, `todo/T2`) |
| `C5_ezelsdorf_total.md` | Ezelsdorf ≈ 499 symbols, not 1739 | ✔ unit check; **primary count now held** (C6) |
| `C6_menghin2000_tables.md` | the four per-zone tables (Berlin / Schifferstadt / Avanton / Ezelsdorf) | ✔ `verify_menghin2000.py` |
| `C7_menghin2010_cross.md` | Menghin 2010's Berlin (Abb. 23) and Ezelsdorf (Abb. 69) tables == the 2000 tables | ✔ by page image (2026-10-13) |

Recall 2026-10-10: 5/5. Recall 2026-10-12: 6/6 (C6 added). Recall 2026-10-13:
7/7 (C7 added). The negative controls C4–C5 are the important ones — a pipeline that
only finds positive calendar claims cannot be trusted.
