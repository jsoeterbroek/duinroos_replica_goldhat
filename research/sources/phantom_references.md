# Source: the phantom references — NOT FOUND

**Status: rejected / unverified.** Three citations in the project brief and the
earlier AI digest could not be found in any scholarly index, library catalogue or
the open web on 2026-10-10. They are recorded here so a future session does not
re-import them as if they existed.

The earlier digest (`research/gold_hat.md`, now
`theories/secondary_digest_2026-10-08.md`) was explicitly written "using AI
(ChatGPT 4.1.)". All three appear **only** in that digest (and the copies of it
under `reference/m5/`), which is the classic signature of a hallucinated
reference: a citation with no page, no DOI, and no trace outside the summary that
generated it.

## 1. "Spurk, Gebhard, Schauer, et al. — analyses show relationships …"

**Claimed:** a joint study of band/symbol counts and astronomical cycles.

**Search:** OpenAlex, Crossref, Semantic Scholar, DuckDuckGo for the author
triple and for each name with "Goldhut/Goldblechkegel/Nebra".

**Found instead:**
- Peter Schauer, *Die Goldblechkegel der Bronzezeit*, 1986 — real, print-only.
- Rupert Gebhard (LMU Munich) — a real archaeologist, works on the Nebra
  context, no gold-hat counting study with Schauer.
- "Spurk" — no Bronze Age archaeoastronomy author located. The name does not
  attach to the gold hats.

**Verdict:** **no such joint study.** The real ingredients are Schauer 1986 and
Gebhard's Nebra work. Do not cite the triple.

## 2. "Wolfgang Schlosser (2004, 2012)"

**Claimed:** argues for a systematic calendrical interpretation of all hats.

**Found instead:** **Wolfhard Schlosser** (1940–2022), astronomer, Ruhr-Universität
Bochum. Relevant works:
- *Einige Anmerkungen zur Realität bronzezeitlicher Mondkalender*, JSMV 86 (2003).
- *El disco de Nebra, ¿un calendario agrícola?* (2004).
- *Die Himmelsscheibe von Nebra — Sonne, Mond und Sterne* (2005).
- *A Physicist's View — the Disk of Nebra* (2011/2021).
None is about the gold hats, and none is from 2012.

**Verdict:** **name error** (Wolfgang → Wolfhard) plus over-claim. Use
`sources/schlosser_2003.md`.

## 3. "I. Mathieson, *The Golden Hat Calendar* (2010)"

**Claimed:** a PDF offering detailed calculations for several hats.

**Search:** Crossref, OpenAlex, Google Scholar (via reader proxy), DuckDuckGo by
exact title and by author; author not found in archaeoastronomy. No library record.

**Verdict:** **not found.** Treat as unverified. If a real Mathieson text exists it
is not indexed and has left no trace; do not cite it.

## Reproduce the check

```sh
curl -s "https://api.openalex.org/works?search=Spurk%20Gebhard%20Nebra&per-page=5"
curl -s "https://api.openalex.org/authors?search=Wolfhard%20Schlosser"
curl -s "https://api.crossref.org/works?query.bibliographic=Mathieson+golden+hat+calendar&rows=5"
```

## Why this is a "find"

Under the pipeline rules a confirmed *absence* is not a novelty claim, but it is a
useful negative result, because these three citations were load-bearing in the
brief: they were the only "other hats match too" and "all hats are calendars"
support in the repo. Removing them removes the false corroboration. The real,
verifiable support for a calendrical reading is Fuls 2004 (Berlin cycle
arithmetic), Lorenz (Metonic structure), Amendola (Schifferstadt place), with the
sceptical counterweight of Fuls 2008, Schlosser 2003 and Peter-Röcher 2023.
