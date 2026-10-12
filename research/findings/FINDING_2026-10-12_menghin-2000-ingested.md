# FINDING_2026-10-12_menghin-2000-ingested

**Status:** verified (read on the page images; controls C1, C5 and C6 reproduce)
**Source:** W. Menghin, *Der Berliner Goldhut und die goldenen Kalendarien der
alteuropäischen Bronzezeit*, Acta Praehistorica et Archaeologica 32 (2000), 31–108.
Page images `assets/menghin/2000/jpg/menghin_pageNNN.jpeg`, text layer
`assets/menghin/2000/ocr/`, batch text `assets/menghin/2000/text/`. Digitised by the
project author, 2026-10-12.
**Subject:** the comparative study — the per-zone ornament data for **all four**
gold hats, on the page, from the primary print.

## What changed

Until today the case held Menghin's Berlin measurement only through the 2010 book,
and the whole cross-hat test (apply the rule to a *second* hat) was **blocked**: the
per-zone counts for Schifferstadt, Avanton and Ezelsdorf were print-only
(`todo/T1`). The 2000 article is now on disk, complete (pp. 31–108 + front matter,
83 page images) and readable, and its four per-zone tables are transcribed.

This is doc item #6 (write-up) being unblocked, not a new interpretation. Nothing in
the finding changes the *question* or the *hit definition* in `CASE.md`.

## The four tables, as read on the page

Menghin's unit is the **counter** (Zähler): `A` stamped symbols × `K` concentric
rings per symbol = `SK` rings per zone. `SK` is a day-count. This is not
Schmidt-Kaler's plain symbol count and not a zone count.

| Hat | Figure, page | Zones | Rings (`SK`) | Symbols (`A`) |
|---|---|---|---|---|
| Berlin | Abb. 14, p. 45 | 1–21 (`{7,16,17}` Schalt, Z5 Sonder) | 1701 in 18 zones (3–21); 1466 (3–20) | 418 discs in 18 friezes; 437 incl. Z5 once |
| Schifferstadt | Abb. 17, p. 50 | 1–11 (`{2,9}` Schalt) | 557 (2–11); 355 (2–9) | 310 (2–11); 266 in 8 zones (2, 5–11) |
| Avanton | Abb. 20, p. 53 | 1–14 (`{12}` Schalt) | 583 (2–14); 537 (3–14) | 269 (2–14) |
| Ezelsdorf | Abb. 27, p. 61 | 1–21, Z21 rebuilt (`{5,6,19}` Schalt) | 1463 (3–20); 1694 (3–21) | **499** (2–20); 432 discs (3–20) |

Data: `data/readings/menghin2000_zones.json`. Verified by
`scripts/verify_menghin2000.py` (control **C6**): `SK = A × K` in every disc-bearing
zone, and every ring total Menghin states in his running text reproduces. The
Berlin 2000 table agrees zone by zone with the 2010-derived `data/zones.json`, and
the 18 rows of the master calculation table (Abb. 43,1, p. 88) reproduce.

## Three results that matter to the case

1. **The Ezelsdorf primary count is obtained: 499 symbols.** Independent of the
   secondary plate used by C5. The phantom digest's "1,739 symbols" is dead; the
   Ezelsdorf ring total is 1463 (no rim) / 1694 (with Menghin's rebuilt rim) and its
   "Zeichen" total 1737 — none of them 1739. See `controls/C5_ezelsdorf_total.md`.

2. **The cross-hat test is no longer blocked for three of four hats.** Schifferstadt,
   Avanton and Ezelsdorf now have raw per-zone `A`/`K`/`SK` on record, so Fuls's
   combinatorial null can be re-run *here* rather than relying on Peter-Röcher's
   one-sentence report that the rule "ließ sich leider nicht übertragen"
   (`todo/T2`). That is a materially better position than 2026-10-11.

3. **Menghin 2000's own summary symbol counts do not all close, and the script says
   so instead of hiding it.** Ezelsdorf zones 3–20 sum to 475 / 508 / 465 where the
   text prints 474 / 505 / 462; the Berlin disc count is 418 on p. 81 but 399 on
   pp. 83 and 91 (the 2010 text at p. 31 confirms 418); and the Avanton six-lunation
   row on p. 79 divides 177 by 6 while stating that Schaltzone 12 was dropped
   (177 includes it; without it the sum is 135 and `135/6 = 22.5`). The **ring** sums
   are exact everywhere. These flagged deltas are themselves evidence for
   Schlosser's and Peter-Röcher's point — a rule applied selectively — and belong in
   the Stage-2 "how sure are we" screen, not under the carpet.

## One correction to our own source recipe

`sources/menghin_2000_2010.md` listed as a trap that "the intercalary ('Schalt') zone
set moves: Menghin 2000 uses `{5,7,16,17}` … the 2010 figures colour only
`{7,16,17}`". Having now read the 2000 pages, that is not right. In 2000 the Berlin
Schaltzonen are `{7,16,17}` throughout (pp. 45, 71, 73, 81–83, 89); zone 5 is a
*Sonderzone*, drawn in the same grey, and is *added* (38) for solar cycles — as in
2010. The two publications differ only in bookkeeping: 2000 gets 1597 as
`1701 − (38+66)`, Wikipedia/2010 get the same 1597 as `1739 − (38+38+66)`. The recipe
has been corrected. The *real* free parameter — which zone blocks get added — stands,
and the critique of it stands with it.

## Checks

- [x] Read on the page image (not the OCR) for every transcribed number
- [x] `SK = A × K` in every disc-bearing zone of all four hats
- [x] All published ring totals reproduce (C6); Abb. 43,1 reproduces
- [x] Cross-source: Menghin 2000 p. 45 == Menghin 2010-derived `data/zones.json`
- [x] Units: Menghin`s counter (rings × symbols) kept separate from Schmidt-Kaler's
      plain counts; `data/readings/` flags both
- [x] Negative/flagged states reported, not forced (three deltas; the Avanton row)
- [x] Novelty: the 2000 article was not in the repo before 2026-10-12; the Ezelsdorf
      primary count is new to the case; the recipe correction is new

## Evidence

- Page images: `assets/menghin/2000/jpg/menghin_page045.jpeg` (Abb. 14),
  `…050.jpeg` (Abb. 17), `…053.jpeg` (Abb. 20), `…061.jpeg` (Abb. 27),
  `…088.jpeg` (Abb. 43,1), `…036.jpeg` (Abb. 2), `…072.jpeg` (Abb. 33).
- Transcription: `data/readings/menghin2000_zones.json`.
- Controls: `controls/C6_menghin2000_tables.md` (new), C1, C5 (both updated).

## Open questions

- Ezelsdorf: why do the table's symbol columns give 475 / 508 / 465 where the text
  gives 474 / 505 / 462? A scanning artefact in the 2000 graphic, or a genuine slip
  in Menghin's typescript? A 300–400 dpi scan of p. 61 (and of the tool legend,
  p. 59) would settle it.
- Which of the four hats does Fuls 2004/2008 actually test, and with which zone
  partition? Needed before `todo/T2` can re-run the null on the new data.
- Menghin 2010 pp. 32–46 and 64–end are still missing; they may hold the other three
  hats' 2010 figures, which would let the 2000 and 2010 readings of Ezelsdorf be
  compared the way Berlin's just were.
