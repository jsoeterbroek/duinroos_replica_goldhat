# Judge question: calendrical claim + unit  (v1)

Provider-neutral form.

**Type:** two answers — (a) yes/no, (b) choice{rings, ornaments, symbols, bands, none}
**Input:** one paragraph from any source about a gold hat.
**Question (a):** Does the passage claim that the ornament encodes a calendar or
astronomical cycle? **Question (b):** If it states a counting unit, which one?

## Decision rules

- A passage that only says the iconography is "cosmic"/"solar" is **no** for (a).
  The sceptical position also accepts cosmic iconography; the dispute is about
  arithmetic.
- A passage that reports a number without saying what is counted is (b) = `none` —
  send it to the reader, do not silently assume "days".
- "gemäß Menghin", "nach Menghin", "adopted from" → still (a), but the reader must
  tag the value `reused_number`.

## Examples

| Passage (abridged) | (a) | (b) |
|---|---|---|
| "Each symbol, or each ring of a symbol, represents a single day." | yes | rings |
| "19 discs × 5 rings = 235" | yes | rings |
| "The 651 punched ornaments per zone…" | no | ornaments |
| "the hat served as insignia of a sun cult" | no | none |
| "h ≈ w: the hits equal chance" | no (it is a negative test) | rings |

## Changelog

- v1 — 2026-10-10 — created.
