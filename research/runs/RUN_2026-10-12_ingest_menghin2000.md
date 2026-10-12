# RUN 2026-10-12 — ingest Menghin 2000 (the comparative study)

## What ran

- The project author digitised the whole of Menghin 2000, *Der Berliner Goldhut und
  die goldenen Kalendarien der alteuropäischen Bronzezeit* (Acta Praehistorica et
  Archaeologica 32, 31–108), into `assets/menghin/2000/pdf/` (9 scan PDFs, 83 pages
  including the front matter).
- **Readability check, then split** into the repo's format: 83 page images
  (`assets/menghin/2000/jpg/menghin_pageNNN.jpeg`), 83 per-page text files
  (`assets/menghin/2000/ocr/pageNNN.txt`) and a combined text per scan batch
  (`assets/menghin/2000/text/`). Pages mapped by printed page number; the one
  duplicate (p. 106) is kept as `menghin_page106b.jpeg`.
- **Transcription of the four per-zone ornament tables from the page images** (not
  the OCR): Berlin Abb. 14 p. 45, Schifferstadt Abb. 17 p. 50, Avanton Abb. 20 p. 53,
  Ezelsdorf Abb. 27 p. 61 → `data/readings/menghin2000_zones.json`.
- New control **C6** and `scripts/verify_menghin2000.py`.
- Wrote `findings/FINDING_2026-10-12_menghin-2000-ingested.md`.
- Corrected a trap in `sources/menghin_2000_2010.md` and `lessons.md` (the
  intercalary-zone set does *not* move between Menghin's two publications).
- Updated C1, C5, `controls/README.md`, `sources/README.md`, `findings/README.md`,
  `CASE.md`, `HANDOFF.md`, `todo/T1`, `NARRATIVE.md`.

## Funnel

| Stage | Count |
|---|---|
| New pages in hand | 83 (pp. 31–108 + cover/imprint/contents/plate) |
| Data tables on the pages | 6 + 4 figure-legend tables (Abb. 14, 17, 20, 27, 39, 42,1, 43,1) |
| Tables transcribed as data | 4 (the per-zone tables) |
| Ring identities verified | 40+ (all reproduce) |
| Flagged, not forced | 4 (3 Ezelsdorf symbol totals, 1 Avanton row) |
| Findings written | 1 |

## Model roles and cost

No model APIs invoked (local extraction + human/page-image read + stdlib script).
**$0.00.**

## Result

1. **Readable and workable.** ≈180 dpi page images; body text and every count table
   legible at 1:1, tables unambiguous at 2–3× crop. The OCR layer is good for grep
   and useless for numbers. Full assessment in `sources/menghin_2000_2010.md`.
2. **The case's central blocker is cleared for three of four hats.** Schifferstadt,
   Avanton and Ezelsdorf now have raw per-zone `A`/`K`/`SK` on record, so Fuls's
   combinatorial null can be re-run locally (`todo/T2`).
3. **Ezelsdorf = 499 symbols from the primary source** (control C5 upgraded).
4. **Three of Menghin's own summary totals do not reproduce from his own tables**;
   the script prints the deltas rather than hiding them.

## Next

- `todo/T2`: re-run Fuls's null on the newly held per-zone data (Schifferstadt,
  Avanton, Ezelsdorf) — the cross-hat test can now be done here.
- Optional: a 300–400 dpi re-scan of pp. 59 and 61 would settle the Ezelsdorf
  symbol-count deltas.
- Menghin 2010 pp. 1–19, 26, 32–46, 64–end still missing (same plan, `todo/T1`).

## Log / notes

- The delivered PDFs carry an OCR text layer from the scanning app. It is *not*
  citable and was not used for any number; every figure in `menghin2000_zones.json`
  was read on the page image.
- `assets/menghin/2000/pdf/` is ~100 MB of scanned PDFs. The page JPEGs (93 MB) are
  the working copy. Flagged to the project author: the PDFs are redundant now and
  may be worth keeping out of git history.
