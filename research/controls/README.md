# controls

Known results the pipeline must re-find. One file per control; per-run recall in
`../runs/`. **A negative result without a control is not a result.**

| Control | What must be re-found | Status |
|---|---|---|
| `C1_menghin_counts.md` | 1739 = 1701 + 38; 418 discs; 745.0 mm | ✔ `verify_calendar.py` |
| `C2_menghin_scenarios.md` | 16 scenario blocks; 61.2 / 64.4 flagged | ✔ `verify_scenarios.py` |
| `C3_schmidt_kaler_sums.md` | 292 = 57+235; 146; 117 | ✔ `verify_venus_hypothesis.py` |
| `C4_fuls_null_result.md` | Berlin ≈ chance; only Schifferstadt significant | ✔ by page image (script pending, `todo/T2`) |
| `C5_ezelsdorf_total.md` | Ezelsdorf ≈ 499 symbols, not 1739 | ✔ unit check |

Recall 2026-10-10: 5/5. The negative controls C4–C5 are the important ones — a
pipeline that only finds positive calendar claims cannot be trusted.
