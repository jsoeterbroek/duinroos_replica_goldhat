# Control C2 — Menghin's 16 scenario blocks must reproduce

**What:** Menghin's own interpretive arithmetic, transcribed from pp. 60–63 /
Figs 61.1–64.4. This is the set the Stage-2 LEDs display.

**Expected:** the 30 stated zone-sums reproduce; two states (61.2, 64.4) do **not**
close cleanly and must be flagged, not forced. The green/intercalary zones in the
2010 figures are `{7,16,17}`.

**How to re-find:**

```sh
python3 scripts/verify_scenarios.py
```

**Result 2026-10-10:** ✔ reproduces; the two caveats print rather than being
hidden. `data/scenarios.json` is a faithful transcription, not a reconstruction.

**If missed:** the transcription of the figures is wrong. Do not "fix" the two
caveat states — Menghin's own text leaves them open.
