# RUN 2026-10-10 — consolidation + source augmentation

Config snapshot, funnel counts, cost. One folder per run.

## What ran

- **Consolidation** of the three legacy documents into the `AGENTS.md` taxonomy.
- **Retrieval** of the sources named in the brief and of new literature:
  targeted search via Crossref, OpenAlex, Semantic Scholar, DuckDuckGo (routed
  through `r.jina.ai`), publisher sites (see `queries/novelty_checks.md`).
- **Reading** of the held PDFs with PyMuPDF (`fitz`) and a local extraction script.
- **Verification** on the rendered page image for every quoted number.
- **Controls** C1–C5 run; C1–C3 via the committed scripts, C4–C5 by page read.

## Funnel

| Stage | Count |
|---|---|
| Candidate sources considered | ~28 |
| Sorted (relevant to the Berlin hat's calendar question) | 14 |
| Read (full text or page range) | 9 |
| Verified on the page image | 5 (Fuls 2004, Fuls 2008, Lorenz, + the two existing assessments) |
| Rejected / not found | 3 phantoms, 3 paywalled-not-held |

## Model roles and cost

| Role | Provider | Used | Cost |
|---|---|---|---|
| judge | — | not invoked (small corpus, human-directed reading) | $0.00 |
| reader | — | not invoked (local PyMuPDF extraction) | $0.00 |
| embedder | — | not needed | $0.00 |
| vision | — | human page-image check of Fuls | $0.00 |

**Total: $0.00**, inside the `keys.yml` caps (`per_run 5`, `per_day 25`).

## Outputs

- `CASE.md`, `HANDOFF.md`, `NARRATIVE.md`, `lessons.md` rewritten.
- `theories/` — 6 theory files + index (2 legacy assessments moved in).
- `sources/` — 13 recipes incl. `phantom_references.md`.
- `controls/` — C1–C5.
- `findings/` — 4 findings.
- `queries/`, `judges/`, `catalogues/`, `candidates/`, `todo/`, `drafts/`.
- `evidence/` — 5 rendered page images from the new PDFs.
- `data/sources/` — 7 source PDFs (gitignored).

## Log / notes

- All control scripts passed (exit 0): `verify_calendar.py`,
  `verify_scenarios.py`, `verify_venus_hypothesis.py`.
- Retrieval trap hit: DuckDuckGo's HTML endpoint returned empty pages under load;
  `r.jina.ai` fixed it (recorded in `lessons.md`). Anubis (Heidelberg) and
  ResearchGate CAPTCHAs blocked two PDFs; recorded, not faked.
- The single most consequential result: **Fuls 2008** independently reproduces the
  project's null result and localises the one significant hat to **Schifferstadt**.
