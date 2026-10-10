# Control C3 — Schmidt-Kaler's sums must reproduce

**What:** the arithmetic the Venus reading rests on, so the comparison with
Menghin is fair.

**Expected (exact):**
- `57 + 235 = 292` (½ Venus synodic period)
- `42 + 38 + 66 = 146` → ×2 = 292, ×4 = 584
- `42 + 75 = 117` → ×5 = 585 (Mercury)

**How to re-find:**

```sh
python3 scripts/verify_venus_hypothesis.py
```

**Result 2026-10-10:** ✔ all sums reproduce; the script also reports the subset
counts (292 has 27 exact subset representations, 584 has 450, neither reachable as
a contiguous block).

**If missed:** `data/readings/menghin.json` or `schmidt_kaler.json` has drifted.

**Note:** this control only checks that the *arithmetic* is as published; it does
not confirm the interpretation. That is C4's job.
