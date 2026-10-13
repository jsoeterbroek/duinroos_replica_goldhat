# RUN 2026-10-13 — ingest Menghin 2010 (the whole book)

## What ran

- The project author supplied the whole of Menghin 2010 as 8 batched scan PDFs
  (`assets/menghin/2010/pdf/2026-10-13_menghin_2010_p*.pdf`), ~226 MB, pp. 1–88 +
  cover/imprint/contents.
- Split into the repo's format **without touching the existing 2010 phone photos**
  (which `IMPLEMENTATION_PLAN.md` still depends on):
  - `assets/menghin/2010/full/jpg/` — 85 page images at native scan resolution
    (`menghin_pageNNN.jpeg`, 3-digit padded; front matter as `front_cover` /
    `imprint` / `toc`).
  - `assets/menghin/2010/full/ocr/` — 85 per-page text files.
  - `assets/menghin/2010/full/text/` — 8 per-batch combined text files.
  - The pre-existing `assets/menghin/2010/jpg/` (28 phone photos, pp. 20–31 and
    47–63) and `ocr/` were left in place.
- Read the new pages the case needs: **"Der Vergleich" pp. 64–72** (p. 65, p. 68,
  p. 30 control, pp. 64, 69–71), and cross-checked against 2000.
- Wrote `findings/FINDING_2026-10-13_menghin-2010-ingested.md`.
- Updated `sources/menghin_2000_2010.md`, `CASE.md`, `HANDOFF.md`,
  `findings/README.md`, `todo/T1_obtain_print_sources.md`, `lessons.md`,
  `NARRATIVE.md`.

## Funnel

| Stage | Count |
|---|---|
| New pages in hand | 85 (pp. 1–88 + front matter) |
| Page images written | 85 |
| Pages read on the image this round | 6 (65, 68, 30, 64, 69–71 by OCR+image) |
| 2000↔2010 zone cross-checks | 2 tables (Berlin 19 zones, Ezelsdorf 18 zones) |
| Flagged, not forced | 4 (partial transfer; moving Ezelsdorf set; Z8 A=40/39; the 432/433 disc-total knock-on) |
| Findings written | 1 |

## Model roles and cost

No model APIs invoked (local PDF split + page-image read + stdlib analysis).
**$0.00.**

## Result

1. **The whole monograph is now in the repo**, complete, in its own `full/` tree so
   the phone photos used by the STL plan are untouched.
2. **Menghin himself calls the cross-hat transfer only partial** (p. 65) and states
   that for **Ezelsdorf the stamp-identity rule yields no direct calendar values**
   (p. 68) — the author's own statement of the failure Peter-Röcher reports.
3. **The Ezelsdorf intercalary set moves between his publications** (`{5,6,19}` in
   2000 → table `{5,6,15,16,17,19}` / text `{5,6,15,17,19}` in 2010; 12 for Fuls),
   and 2010's own table and text disagree. The Berlin set stays `{7,16,17}` + Z5.
4. **The 2000↔2010 tables agree** ring-for-ring for Berlin and Ezelsdorf, and the
   Zone 8 `A=40 / SK=78` slip recurs — it is in the typescript.

## Next

- `todo/T2`: the Fuls null is now reproducible locally from Menghin 2000 data
  (methods A/C/D for Berlin, B for Schifferstadt reproduce his table). Run it for all
  four hats and record the cross-hat result — the thing Menghin himself calls partial.
- Skim **pp. 73–88** (Die goldenen Kalenderhüte, Der Kult, Literatur) for find-context
  and cult arguments; they are in hand but unread.
- Optional: 300–400 dpi re-scan of p. 68 to settle the 6-vs-5 intercalary question.

## Log / notes

- The PDFs carry a scanner text layer; page numbers were assigned from the batch
  ranges (`p16-27` … `p82-88`) and from the printed folios read on the images. The
  first batch (front matter + pp. 7–15) was mapped by hand and is the only place the
  page numbering needed judgement; the low-value pages there are front matter.
- The batches are ~226 MB and, like the 2000 PDFs, are redundant once the page
  images exist; flagged to the project author.
