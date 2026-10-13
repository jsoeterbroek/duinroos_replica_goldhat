# Berlin Gold Hat — does the ornament encode a calendar?

**Status:** active — 2026-10-13. Source base now includes the full Menghin 2000 and
the full Menghin 2010 monographs.
**Plan item:** #6 (novelty check and write-up) of the CASE plan below, adapted for a
small scholarly corpus (see "Pipeline, adapted" below).

## Question

Does the ornament of the Berlin Gold Hat (Late Bronze Age, c. 1000–800 BC;
no provenance; Neues Museum, Berlin) deliberately encode a calendrical /
astronomical system? And if so, which one — lunisolar (Menghin), Venus
(Schmidt-Kaler), or something else?

**Scoped (doc item #1):**

- **Period:** Late Bronze Age, Urnfield culture, c. 1400–800 BC (the Berlin hat
  itself c. 1000–800 BC per the museum; other hats earlier).
- **Place:** Central Europe. The Berlin hat has no find context; the other three
  gold hats are from Schifferstadt (DE), Ezelsdorf-Buch (DE) and Avanton (FR).
- **What counts as a hit:** a *statistically selective* correspondence between a
  **pre-registered** counting rule applied to the **measured** ornament and a
  calendar/astronomical period, that survives a null model and is corroborated
  by independent data (metrology, find context, iconography, or a second object).
- **What does NOT count:** a block or subset of zones that reaches a round number
  when the block was chosen after seeing the number; a reading that reuses another
  author's measurements; a claim whose free parameter (which zones are
  "intercalary") moves between publications.

## Why it matters

The replica (stages 1–2) must show the calendar theory *or theories* behind the
object with LED bands and an M5 screen. Which theory, and how confident we are,
is a research question. Getting it wrong misleads museum visitors; getting it
right, and showing the uncertainty honestly, is the more interesting exhibit.

## Sources

One recipe per source in `sources/`. Status at 2026-10-10:

**Primary (measured the object):**

| Source | Recipe | Status |
|---|---|---|
| Menghin 2000 (Berlin + the other three hats, Ornamentanalyse) | `sources/menghin_2000_2010.md` | **held — COMPLETE** (83 page images + text, `assets/menghin/2000/`; four per-zone tables transcribed, control C6) |
| Menghin 2010 (book) | `sources/menghin_2000_2010.md` | **held — COMPLETE** (whole book, pp. 1–88, `assets/menghin/2010/full/`; 2026-10-13) |
| Menghin 2003 (Golden Calendar Hats, catalogue) | `sources/menghin_2000_2010.md` | print-only |
| Schauer 1986 (Die Goldblechkegel der Bronzezeit) | `sources/schauer_1986.md` | print-only, not yet obtained |
| Menghin & Schauer 1983 (Ezelsdorf) | `sources/schauer_1986.md` | print-only |
| Fuls 2004 (Goldhüte + Ostfriesland, ORDO ET MENSURA VIII) | `sources/fuls_2004.md` | **held (PDF)** |
| Fuls 2008 (statistical analysis, Nuncius 8) | `sources/fuls_2008.md` | **held (PDF)** |
| Amendola 2021 (Schifferstadt location, JSA 7) | `sources/amendola_2021.md` | abstract held; full text paywalled |
| Lorenz 2010/2011 + Goldhut-Nachtrag (2nd ed.) | `sources/lorenz_2011.md` | **held (PDF)** |

**Reused Menghin's numbers (no new measurement):**

| Source | Recipe | Status |
|---|---|---|
| Schmidt-Kaler 2012 (Venus) | `sources/schmidt_kaler_2012.md` | held (scanned PDF, OCR) |
| Lorenz's popular articles | `sources/lorenz_2011.md` | held |

**Critical / contextual:**

| Source | Recipe | Status |
|---|---|---|
| Schlosser 2003 (Realität bronzezeitlicher Mondkalender, JSMV 86) | `sources/schlosser_2003.md` | **held** (PDF + text in `assets/`) |
| Peter-Röcher 2023 (astronomy & state structures, BUFM 106) | `sources/peter_roecher_2023.md` | **held** (PDF + text in `assets/`) |
| Randsborg 2006 (Calendars, Acta Archaeologica 77) | `sources/randsborg_2006.md` | metadata held; paywalled |
| Hansen & Rink 2008 (Kalender und Finsternisse, Nuncius 8) | `sources/hansen_rink_2008.md` | in the Fuls 2008 proceedings volume; chapter not extracted |
| Wikipedia "Berlin Gold Hat" / "Gold hat" + museum text | `sources/wikipedia_and_museum.md` | held |

**References named in the earlier digest that could not be verified — see
`sources/phantom_references.md`:**
Spurk/Gebhard/Schauer et al.; "Wolfgang Schlosser" (2004, 2012);
I. Mathieson, *The Golden Hat Calendar* (2010).

## Controls

Known published results the pipeline must re-find before it is trusted. One file
per control in `controls/`.

| # | Control | Where | Re-found? |
|---|---|---|---|
| C1 | Menghin's Berlin counts: 418 discs, 1701 rings, 1739 = 1701 + 38; zones 3–21 | `controls/C1_menghin_counts.md` | yes (`scripts/verify_calendar.py`) |
| C2 | Menghin's 16 scenario blocks and their caveats | `controls/C2_menghin_scenarios.md` | yes (`scripts/verify_scenarios.py`) |
| C3 | Schmidt-Kaler's sums: 57+235=292, 42+38+66=146, 42+75=117 | `controls/C3_schmidt_kaler_sums.md` | yes (`scripts/verify_venus_hypothesis.py`) |
| C4 | Fuls 2008's **negative** result: Berlin's hit-rate ≈ random; only Schifferstadt significant | `controls/C4_fuls_null_result.md` | yes — **reproduced by script** (`scripts/fuls_null.py --check`, 2026-10-13) |
| C5 | The Ezelsdorf-Buch symbol total is ≈ 499, **not** 1739 | `controls/C5_ezelsdorf_total.md` | yes — now from the **primary** per-zone table (Menghin 2000, Abb. 27) |
| C6 | Menghin 2000's four per-zone tables (Berlin, Schifferstadt, Avanton, Ezelsdorf) and their ring identities | `controls/C6_menghin2000_tables.md` | yes (`scripts/verify_menghin2000.py`) |

## Plan

Doc items. Say which one you are on in every update.

1. **Scope.** ✔ done — period, place and hit definition above.
2. **First source.** ✔ done — Menghin 2010; recipes in `sources/`.
3. **Control.** ✔ done — C1–C5 in `controls/`.
4. **Retrieve.** ✔ done for a small corpus — `queries/`; candidates in
   `candidates/CANDIDATES.md`.
5. **Sort, read, verify.** ✔ done for the held sources — `runs/`; findings in
   `findings/`; page images in `evidence/`.
6. **Novelty and write-up.** ◀ **here (this round).** Consolidate the three
   legacy documents into this structure (`theories/`), add the new sources
   (Fuls, Amendola, Lorenz, Schlosser, Peter-Röcher, Randsborg, Hansen & Rink),
   check the phantom references, write the findings and the narrative beat.

**Next after #6:** obtain Schauer 1986 and the Menghin 2003 catalogue chapter
(print-only); extract Hansen & Rink 2008; **re-run Fuls's combinatorial null on the
per-zone data now held for all four hats** (`todo/T2`, no longer blocked). Menghin
2010 is now complete: its "Der Vergleich" chapter (pp. 64–72) records that the author
himself calls the cross-hat transfer only *partial* — see
`findings/FINDING_2026-10-13_menghin-2010-ingested.md`.

## Pipeline, adapted to a small scholarly corpus

Antiquity's loop assumes millions of pages and a GPU embedder. This case has
~15 documents. The adaptation, recorded so the difference is deliberate:

1. **Question + control** — as above; the controls are *published numbers* the
   scripts must reproduce.
2–4. **Retrieve / sort / read** — no embeddings needed. Retrieval is targeted
   search (Crossref/OpenAlex, DuckDuckGo via `r.jina.ai`, publisher sites) and
   regex over the held PDFs (`queries/`). The "judge" classifies each passage
   by *evidence role* (primary measurement / reused number / critique /
   speculation) — see `judges/`. The "reader" extracts the exact numbers.
5. **Verify** — read the **PDF page image**, not the OCR. Page images rendered
   from the held PDFs are in `evidence/`.
6. **Novelty** — check against `catalogues/` (Menghin's numbers, Fuls's database,
   the museum/Wikipedia synthesis) before calling anything new.

## Pipeline rules applied to this case (from `AGENTS.md`)

- Nothing is a "find" before it is read on the page image. Until then, *candidate*.
- Every negative result needs a control; report which controls were missed.
- Record *how* each catalogue was checked (full read vs search-inside).
- Model output is a lead, not a fact. The earlier digest (`gold_hat.md`) was
  written by an AI and contains at least one invented corroboration and three
  unverifiable citations — see `lessons.md`.
- Stay inside the budget in `keys.yml`. This round used no paid model API; all
  work was local scripts + free scholarly APIs (cost $0.00).
