# Control C1 — Menghin's Berlin counts must re-derive

**What:** the hard, non-interpretive numbers of the Berlin Gold Hat. If the
pipeline cannot re-find these, it is not allowed to reason about the calendar.

**Expected (Menghin 2010, pp. 47–63):**
- 21 ornamental zones; zones 3–21 are the 19 "system" zones.
- 418 bossed discs (stamps 8–15) over 18 disc-bearing zones carry **1701**
  concentric rings.
- Zone 5 adds **38** special signs (19 crescent+dot over 19 eye/almond).
- Total ring-units zones 2–21 = **1783**; the 19 system zones = **1739**.
- Identity: `1739 = 1701 + 38`.
- The ring-height table sums to **745.0 mm**.

**How to re-find:**

```sh
python3 scripts/verify_calendar.py
```

**Result 2026-10-10:** ✔ all identities reproduce. Source of truth for the
numbers is `assets/menghin/text/`; the derived tables are `data/zones.json` and
`data/readings/menghin.json`.

**If missed:** the zone transcription or the tool/ring table is wrong; fix the
data before continuing. A negative result about the *calendar* is worthless until
this control passes.
