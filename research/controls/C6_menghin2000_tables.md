# Control C6 — Menghin 2000's four per-zone tables must reproduce

**What:** the raw measured ornament of all four surviving European gold hats, on
Menghin's own counter (`A` symbols, `K` concentric rings per symbol,
`SK = A × K` rings per zone). This is the primary data the cross-hat test needs;
until now only Berlin was held, via the 2010 book.

**Expected (transcribed 2026-10-12 from the page images, not the OCR):**

| Hat | Figure | rings | symbols | identity |
|---|---|---|---|---|
| Berlin | Abb. 14, p. 45 | 1701 (Z 3–21) | 418 (18 friezes) | `1739 = 1701 + 38`; `Z 3–21` = 437 with Z5 once |
| Schifferstadt | Abb. 17, p. 50 | 557 (Z 2–11) | 266 in 8 zones (2, 5–11) | `311 + 44 = 355`; `355 + 202 = 557` |
| Avanton | Abb. 20, p. 53 | 583 (Z 2–14) | 269 (Z 2–14) | `537 = 583 − 46`; `Z 3–11` = 360 |
| Ezelsdorf | Abb. 27, p. 61 | 1463 (Z 3–20) | 432 (Z 3–20) | `1737 = 1463 + 21 + 22 + 231`; `1694 = 1463 + 231` |

**How to re-find:**

```sh
python3 scripts/verify_menghin2000.py
```

Data: `data/readings/menghin2000_zones.json`.

**Result 2026-10-12:** ✔ every **ring** identity reproduces: `SK = A × K` in all
four hats; Berlin 1701 / 1466 / 1739 / 1682 / 1644 / 1597 / 1461; Schifferstadt 266 /
310 / 311 / 355 / 557 / 202; Avanton 269 / 583 / 537 / 360 / 182 / 355 / 271 / 364 /
177; Ezelsdorf 1463 / 1694 / 1737 / 1502 / 1448 / 1411 / 1506 / 432. The 18 rows of
the master calculation table (Abb. 43,1, p. 88) reproduce. The 2000 table for Berlin
agrees zone by zone with the 2010-derived `data/zones.json`.

**Flagged, not forced** (the script prints these as WARN):

- Ezelsdorf symbol totals: the table gives 475 / 508 / 465 where Menghin prints
  474 / 505 / 462 (deltas 1 / 3 / 3). The ring sums are unaffected but exact.
- Avanton, 6 lunations (p. 79): `177 ÷ 6` is used while the text says Schaltzone 12
  was dropped; 177 is zones 12–14 with zone 12 included, and `135 ÷ 6 = 22.5`.
- Berlin disc count: the 2000 article prints 418 on p. 81 but 399 on pp. 83 and 91.
  The 2010 text (p. 31) independently says 418 and the table sums to 418 → **418**.

**If missed:** the transcription is wrong. Do not "fix" the flagged states — the
article leaves them open, and they are evidence for the critical literature's point
about a rule that is applied selectively (`theories/sceptical_ornament.md`).

**Effect on the case:** the cross-hat test is no longer blocked for three of the
four hats. The raw data for Schifferstadt, Avanton and Ezelsdorf is now on record,
so *we* can apply Fuls's null ourselves instead of relying on Peter-Röcher's
one-sentence report that the rule "could not be transferred" (`todo/T2`).
