# T1 — obtain the print-only sources

**Why:** the cross-hat test (fix the rule on Berlin, apply it blind to another
hat) is the strongest test available. It is **blocked/only-partly-done** without
the raw per-zone ring counts and zone order for Schifferstadt / Ezelsdorf /
Avanton. Peter-Röcher 2023 now states it *failed* when attempted; we still want the
raw data to test it ourselves.

**Status of the four items (2026-10-13):**

1. **Peter Schauer, *Die Goldblechkegel der Bronzezeit*, Habelt 1986** —
   *to get from Leiden University Library.* Wanted for the plates and the tool
   measurements; **no longer the blocker for the counts** (Menghin 2000 reproduces
   Schauer's per-zone data in Abb. 17, 20 and 27).
2. **Menghin 2000, *…goldenen Kalendarien*** — ✔ **held COMPLETE** since
   2026-10-12 (83 page images + text, pp. 31–108 plus front matter, in
   `assets/menghin/2000/`; four per-zone tables transcribed, control C6).
   The cross-hat data sits on four figure pages, now on disk and read:
   **Abb. 14, p. 45** (Berlin), **Abb. 17, p. 50** (Schifferstadt),
   **Abb. 20, p. 53** (Avanton), **Abb. 27, p. 61** (Ezelsdorf-Buch); each figure
   carries its own stamp/numbering legend, and the Ezelsdorf ornament patterns are
   itemised in Abb. 25, p. 59 (numbering after M. Fecht).
2b. **Menghin 2010, *Der Berliner Goldhut*** — ✔ **held COMPLETE** since
   2026-10-13 (whole book, pp. 1–88 + front matter, in `assets/menghin/2010/`;
   a lower-resolution phone-photo selection was removed in the 2026-10-14 reorg).
   Finding: `findings/FINDING_2026-10-13_menghin-2010-ingested.md`.
3. **Wolfhard Schlosser, JSMV 86 (2003)** — ✔ **held**:
   `assets/89612-Artikeltext-237706-1-10-20220629.pdf` (+ text
   `assets/schlosser_2003_jsmv86.txt`). Read → `findings/FINDING_2026-10-11_…`.
4. **Heidi Peter-Röcher, BUFM 106 (2023)** — ✔ **held**:
   `assets/Peter-Roecher_2023_Astronomische_Forschungen.pdf` (+ text
   `assets/peter_roecher_2023_bufm106.txt`). Read → same finding.

---

## Digitization plan for Menghin 2000 / 2010

**Format of record: page images.** The pipeline rule is "nothing is a find before
it is read on the original page image"; OCR alone is not citable. Text extracted
from images is a convenience for searching, not the source.

- **Preferred output:** a single multi-page **PDF per book**, 300 dpi, greyscale
  (colour only where it aids the plates). If scanning to PDF is not possible,
  **per-page JPG at 300–400 dpi**, 600 dpi for any table or plate page.
- **File names:** by *printed* page number, in the existing convention:
  - `assets/menghin/2000/jpg/menghin_page050.jpeg`
  - `assets/menghin/2010/jpg/menghin_page032.jpeg`
  - OCR text into `assets/menghin/<year>/ocr/pageNN.txt` and a combined
    `assets/menghin/<year>/text/menghin_pagesXX-YY.txt` (as already done for 2010).
- **Quality:** flat, straight, even diffuse light. Avoid phone photos with
  perspective/keystone or shadow — the small concentric rings and the table digits
  are the whole point. A phone scanning app with perspective correction is
  acceptable for text pages but not for the count tables.
- **Also capture:** title page + verso (for citation), the **table of contents**,
  and every **figure legend** (the legends define which stamp/ring type a zone
  carries — that is the data the cross-hat test needs).

### Priority order

**A. Menghin 2000 first — it is the comparative study** ("und die goldenen
Kalendarien der alteuropäischen Bronzezeit", Acta Praehistorica 32, 31–108).
**✔ digitised complete 2026-10-12.** It does contain the per-zone tables for *all
four* hats, as expected: the four figure pages are Abb. 14 (Berlin, p. 45),
Abb. 17 (Schifferstadt, p. 50), Abb. 20 (Avanton, p. 53) and Abb. 27
(Ezelsdorf-Buch, p. 61). Fuls cites these pages:
- **p. 50** — Schifferstadt per-zone table (rings/symbols).
- **p. 53** — Avanton per-zone table.
- **pp. 74, 77–78** — the numbers/cycles discussion.
- **pp. 88–93** — Berlin and Ezelsdorf, the 1739 / Metonic discussion.

→ **Done.** The whole article is digitised (83 page images, pp. 31–108 + front
matter); the per-zone tables (Abb. 14, 17, 20, 27) are transcribed into
`data/readings/menghin2000_zones.json`. No further scan of 2000 is needed.

**B. Menghin 2010 — ✔ digitised complete 2026-10-13.** The whole book (pp. 1–88 +
front matter) is held in `assets/menghin/2010/` (jpg/ocr/text, 3-digit padded
names, flattened out of `2010/full/` on 2026-10-14) from the author's 8-batch PDF. The comparison chapter (pp. 64–72) is read:
Menghin calls the cross-hat transfer *partial* (p. 65) and says the stamp-identity
rule gives no direct values on Ezelsdorf (p. 68). No further scan of 2010 is needed;
a 300–400 dpi re-scan of p. 68 would only settle the 6-vs-5 intercalary question.

**C. Everything else** (full books) — nice to have; do it only if the effort is cheap.

### How the digitization is checked

Re-derive a **known-answer control** from each scanned set. Done for Menghin 2000:
the Berlin counts (`scripts/verify_calendar.py`, C1) reproduce from the 2000 pages,
and the per-zone tables plus the 54-month arithmetic reproduce zone by zone
(`scripts/verify_menghin2000.py`, C6). A scan whose numbers cannot be read well
enough to pass the control is not good enough.

---

**Progress (updated 2026-10-13):**

- **Menghin 2000 — ✔ DONE, complete.** The author digitised the whole article.
  83 page images + text are in `assets/menghin/2000/`; the four per-zone tables are
transcribed into `data/readings/menghin2000_zones.json` and verified by control C6
(`scripts/verify_menghin2000.py`). Readability verdict and page map:
`sources/menghin_2000_2010.md`. Finding:
`findings/FINDING_2026-10-12_menghin-2000-ingested.md`. Run:
`runs/RUN_2026-10-12_ingest_menghin2000.md`.
- **Menghin 2010 — ✔ DONE, complete.** Whole book pp. 1–88 + front matter in
  `assets/menghin/2010/` (85 page images + text, 8-batch PDF). The Vergleich
  chapter is read and written up: `findings/FINDING_2026-10-13_menghin-2010-ingested.md`;
  run `runs/RUN_2026-10-13_ingest_menghin2010.md`.
- **Item 1 (Schauer 1986)** and the **2003 catalogue chapter** remain open. Schauer is
  now a *nice to have*, not the blocker: Menghin 2000 reproduces Schauer's per-zone
  data for the other three hats (his Abb. 17, 20, 27 are drawn from Schauer's plates).
- Items 3–4 (Schlosser 2003, Peter-Röcher 2023) done and read on 2026-10-11.

---

## Status of the digitization plan

**A. Menghin 2000 — ✔ complete.** **B. Menghin 2010 — ✔ complete.** The two
monographs are fully in the repo; the remaining print-only items are Schauer 1986
and the Menghin 2003 catalogue chapter, neither of which blocks the cross-hat test.

**Done when:** for Ezelsdorf at least, a per-zone table of rings-per-stamp and the
zone order is transcribed into `data/readings/` with a `_source` field, and the
cross-hat script runs.

**Status 2026-10-13:** the first half is **DONE** — four per-zone tables, all four
hats, in `data/readings/menghin2000_zones.json`, cross-checked against Menghin 2010.
The second half (the cross-hat script) is `todo/T2`, which is no longer blocked.
