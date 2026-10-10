# FINDING_2026-10-10_fuls-statistics

**Status:** verified
**Source:** Andreas Fuls, *Astronomisch-statistische Analyse von Kreissymbolen
bronzezeitlicher Goldhüte*, Nuncius Hamburgensis 8 (2008), 113–129; and
*Archäoastronomische Anmerkungen …*, ORDO ET MENSURA VIII (2004), 39–57.
**Subject:** the statistical significance of the gold-hat calendar readings

## Verbatim (translated from the page image)

> "Der Vergleich der Ergebnisse zeigt, dass in fast allen Fällen die relative
> Häufigkeit der Treffer genau der Wahrscheinlichkeit einer zufälligen Auswahl
> entspricht, d. h. h ≈ w. Nur in wenigen Fällen ergibt sich eine signifikant
> höhere Häufigkeit."
>
> "Nur für den Goldhut von Schifferstadt lassen sich bezüglich des synodischen
> Monats (Methode B) und des Sonnenmonats (Methode C und D) eine signifikant über
> der Zufälligkeit liegende Trefferquote nachweisen."

## What it says

- Fuls builds the full combinatorial null for all four hats under four grouping
  methods (arbitrary subsets; same-symbol groups; contiguous blocks; contiguous
  blocks minus switch-zones). Berlin's search space runs from 210 to 1 048 575
  combinations.
- **Berlin's hit-rate tracks the random line** for the synodic month and the
  tropical year. **Only Schifferstadt** clearly beats chance (synodic month,
  factor ≈ 2.1 at a tolerance of ≈ 0.3 d), and that is confirmed by Schifferstadt's
  metrology (height ratio 3:9, diameter ratio 9:15).
- He also warns the other way: with G up to 65 535 a real, sparse encoding could
  be drowned out. His conclusion is "not demonstrated", not "disproved".

This independently reproduces — in a peer-reviewed proceedings volume — the same
conclusion as the project's own Monte-Carlo in `theories/menghin_lunisolar.md` §2
and `theories/schmidt_kaler_venus.md` §3.

## Checks

- [x] Read on the page image:
      `evidence/2008_wurzburg_fuls_goldhats_stats_conclusions_fuls2008_p123_full.jpg`,
      `…_stats_tables_fuls2008_p121_full.jpg`
- [x] Author's own caveat quoted (the result is not a disproof)
- [x] Unit: Fuls uses Menghin's rings×symbols; the planetary re-test covers
      Schmidt-Kaler's Venus/Mercury and finds no Berlin selectivity
- [x] Novelty: this result was *not* in the project before 2026-10-10; it is a
      genuine addition. Checked against `catalogues/` — not previously cited.

## Evidence

`research/data/sources/fuls_2008_nuncius8.pdf` (pp. 113–129);
`research/data/sources/fuls_2004_ordo8.pdf`; the two page images above.
Controls: `controls/C4_fuls_null_result.md`, `controls/C3_schmidt_kaler_sums.md`.

## Open questions

- Can the null be re-implemented here? (open `todo/`.)
- Does the pattern-type grouping of Fuls 2004 survive on Ezelsdorf once Schauer
  1986 is available?
- Why is Schifferstadt selective and Berlin not? Age? Simpler ornament? Or is the
  Berlin reading simply over-fitted?
