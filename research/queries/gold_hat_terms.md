# Query set: the gold-hat corpus (v1, 2026-10-10)

For a small scholarly corpus, retrieval is targeted search + regex over the held
PDFs. No embeddings are needed (see `CASE.md` "Pipeline, adapted").

## Sources to search

`research/data/sources/*.pdf`, `assets/menghin/2010/text/*.txt`, and the `theories/`
files (as a secondary corpus to be checked, never trusted).

## Keyword regex (tolerant of OCR errors)

```
(?i)(gold(ener)? ?(hut|kegel|blechkegel)|golden hat|gold hat|cone d'?avanton|
     ezelsdorf|schifferstadt|berliner goldhut)
(?i)(meton|metonic|luni[- ]?sol|synodisch|synodic|mondzyklus|lunar|schaltzone|
     intercalary|schaltjahr|embolismic)
(?i)((1[0-9]{3}|[0-9]{3})\s*(kreise|symbol|ringe|tage|d))   # counts with units
```

## Named quantities to search for

`1739`, `1701`, `1783`, `418`, `235`, `19`, `292`, `584`, `365`, `354`, `945`,
`44414`, `32660`, `1461`, `266`, `355`, `59`, `60`, `146`, `117`,
`29.530588`, `29.530585`, `365.2422`.

## Unit disambiguation (mandatory)

Every hit must be tagged with its unit before it is counted:

| Unit | Author | Meaning |
|---|---|---|
| `rings` | Menghin, Fuls | concentric rings per disc × number of discs = "days" |
| `ornaments` | Schmidt-Kaler | every punched ornament incl. fillers — **not days** |
| `symbols` | Menghin (zones 3–21) | stamped symbols per zone |
| `bands/lines/friezes` | Lorenz | structural counts (19, 12+7) |

**Never sum across units.** A regex hit for `235` is meaningless without the unit.

## Known traps to exclude / flag

- `Wolfgang Schlosser`, `Mathieson`, `Spurk` → secondary web summaries or
  hallucinations, not primary sources (`lessons.md`).
- `sources.md` (project `AGENTS.md`) → does not exist in the repo.
- Numbers quoted from `theories/secondary_digest_2026-10-08.md` or
  `reference/m5/` → secondary; re-check against a primary.
- `~3,393`, `1739 Eselsdorf`, `{5,7,16,17}` (as *the* intercalary set) → known-bad.

## Semantic queries (for a future embedder, if the corpus grows)

- "the author proposes that the number of symbols encodes a calendar"
- "the counting unit is defined as X, not Y"
- "the association is what would be expected by chance"
- "the same group of zones is treated as intercalary in one work and solar in another"
