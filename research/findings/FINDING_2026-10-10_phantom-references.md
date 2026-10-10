# FINDING_2026-10-10_phantom-references

**Status:** rejected (negative result with controls)
**Source:** the earlier AI digest `gold_hat.md` (now
`theories/secondary_digest_2026-10-08.md`) and the project brief `AGENTS.md`.
**Subject:** three citations that do not exist

## What was claimed

1. "Spurk, Gebhard, Schauer, et al.: analyses show relationships between
   band/symbol counts and astronomical cycles."
2. "Wolfgang Schlosser (2004, 2012): argues for a systematic calendrical
   interpretation for all hats."
3. "I. Mathieson, *The Golden Hat Calendar* (2010): PDF — detailed calculations for
   several hats."

## What was found

| Claim | Searched | Result |
|---|---|---|
| Spurk/Gebhard/Schauer | OpenAlex, Crossref, Semantic Scholar, DDG | **no such joint study**; real parts are Schauer 1986 + Gebhard (Nebra), no "Spurk" in this field |
| Wolfgang Schlosser | OpenAlex author search, Wikipedia | **name error**: Wolfhard Schlosser (1940–2022); works on lunar calendars/Nebra, **not** the hats, and no 2012 gold-hat paper |
| I. Mathieson 2010 | Crossref, OpenAlex, Google Scholar, DDG | **not found**; author absent from archaeoastronomy; likely hallucinated |

## Checks

- [x] Searched three index APIs and a web search, exact titles and author names
- [x] Author-name variants checked (Wolfgang/Wolfhard; Spurck/Spurk)
- [x] Traced all three to a single origin: the AI-written digest, which labels
      itself "using AI (ChatGPT 4.1.)"
- [x] Catalogues checked: `catalogues/wikipedia_and_museum.md` (search-inside)

## Evidence

`sources/phantom_references.md` (the full search record); `research/lessons.md`
(trap rows). Control: the *positive* controls C1–C3 still pass, so the search
methodology is not simply broken.

## Why it matters

These three were the only "the other hats match too / all hats are calendars"
support in the repo. With them removed, the calendrical case rests on Menghin
(measurement + hypothesis), Fuls (construction + null), Lorenz (structure) and
Amendola (place) — and is properly contested by Fuls 2008, Schlosser 2003 and
Peter-Röcher 2023.

## Open questions

- Is there an obscure grey-literature "Mathieson" PDF offline? If a human finds
  one, this finding must be re-opened. Absence in indexed sources is not proof of
  non-existence, only that it must not be cited without a page.
