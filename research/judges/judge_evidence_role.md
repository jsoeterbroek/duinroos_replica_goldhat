# Judge question: what is the evidential role?  (v1)

Provider-neutral form. Compile to the judge provider's API at run time.

**Type:** choice{primary_measurement, reused_number, construction, critique, speculation, other}
**Input:** one paragraph or table row from a source, with its heading.
**Question:** In this passage, does the author report a **new measurement of the
object**, reuse another author's number, **construct** a new grouping of numbers,
**criticise** a claim, or **speculate**?

## Definitions

- `primary_measurement` — a count, ring number, dimension or find context measured
  by *this* author.
- `reused_number` — a value explicitly taken from another work (e.g. "gemäß
  Menghin").
- `construction` — a new sum/group/rule applied to existing numbers.
- `critique` — a claim that a previous interpretation is unsound, or a null test.
- `speculation` — a wider cultural/historical argument not tied to a measurement.

## Examples

| Passage (abridged) | Expected |
|---|---|
| "Zone 3 = 14 × 3 = 42; zone 4 = 15 × 5 = 75" | primary_measurement |
| "die Summen sind gemäß Menghin" | reused_number |
| "zones 7 + 21 = 57 + 235 = 292" | construction |
| "in fast allen Fällen entspricht die Häufigkeit der einer zufälligen Auswahl" | critique |
| "the hat was probably worn by a priestly caste" | speculation |

## Why it matters

The phantom citations all came from `reused_number`/`speculation` text that a
summariser promoted to "analyses show". The judge keeps the roles apart before the
reader extracts numbers.

## Changelog

- v1 — 2026-10-10 — created for the consolidation round.
