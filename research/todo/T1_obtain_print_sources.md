# T1 — obtain the print-only sources

**Why:** the cross-hat test (fix the rule on Berlin, apply it blind to another
hat) is the strongest test available. It is **blocked/only-partly-done** without
the raw per-zone ring counts and zone order for Schifferstadt / Ezelsdorf /
Avanton. Peter-Röcher 2023 now states it *failed* when attempted; we still want the
raw data to test it ourselves.

**Status of the four items (2026-10-11):**

1. **Peter Schauer, *Die Goldblechkegel der Bronzezeit*, Habelt 1986** —
   *to get from Leiden University Library.* Still the single most valuable item:
   it holds the per-zone counts/rings for the non-Berlin hats.
2. **Menghin 2010, *Der Berliner Goldhut*** and **Menghin 2000, *…goldenen
   Kalendarien*** — **in the project author's possession in print.** Digitization
   plan below.
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
Kalendarien der alteuropäischen Bronzezeit", Acta Praehistorica 32, 31–108). Nothing
of it is digitized yet. It should contain the per-zone tables for *all four* hats.
Fuls cites these pages:
- **p. 50** — Schifferstadt per-zone table (rings/symbols).
- **p. 53** — Avanton per-zone table.
- **pp. 74, 77–78** — the numbers/cycles discussion.
- **pp. 88–93** — Berlin and Ezelsdorf, the 1739 / Metonic discussion.

→ Scan the **whole article if feasible**; if not, scan the TOC, the four per-zone
tables (pp. 50, 53, and the Berlin/Ezelsdorf tables), pp. 74–93, and all plates.

**B. Menghin 2010 gaps.** Already held: pages **20–25, 27–31, 47–63**. Missing:
- **pp. 1–19** — front matter, find history, material/technique.
- **p. 26, pp. 32–46** — likely the ornament catalogue / tool legend / measurements.
- **pp. 64–end** — likely the comparative chapters on the other hats, plates,
  bibliography. Highest value for the cross-hat test.
- the **table of contents** (to map the rest).

→ Scan the TOC first, then pp. 32–46 and pp. 64–end (especially any pages with
per-zone tables or the other three hats), then the plates.

**C. Everything else** (full books) — nice to have; do it only if the effort is cheap.

### How the digitization is checked

Re-derive a **known-answer control** from each scanned set: the Berlin counts
(`scripts/verify_calendar.py`, C1) must reproduce from the new 2010 scans, and
Menghin 2000's stated 54-month arithmetic must reproduce from its own page (C2 /
C3). A scan whose numbers cannot be read well enough to pass the control is not
good enough.

---

**Progress:** items 3–4 done and read (2026-10-11). Items 1–2 open.
Owner: project author (has the Menghin prints; Schauer via Leiden).

**Done when:** for Ezelsdorf at least, a per-zone table of rings-per-stamp and the
zone order is transcribed into `data/readings/` with a `_source` field, and the
cross-hat script runs.
