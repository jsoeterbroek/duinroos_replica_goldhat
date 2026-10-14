# The Berlin Gold Hat and the Calendar Hypothesis: An Evidence Review

*Draft — 2026-10-14. Doc item #6 of CASE.md.*
*All results reproduced by script unless noted. Controls: C1–C7 all pass.*

---

## 1. The Object

The Berlin Gold Hat (*Berliner Goldhut*) is a 745 mm tall beaten-gold cone, now in
the Neues Museum, Berlin. It is Urnfield-culture, dated c. 1000–800 BC. Its
provenance is unknown; it surfaced on the art market in 1996. Three related hats
exist: at Schifferstadt (DE), Ezelsdorf-Buch (DE, fragmentary), and Avanton (FR).

The Berlin hat has 21 ornamental zones running from apex to base. Eighteen carry
bossed discs (*Scheibenbuckel*): a central boss surrounded by concentric rings. The
ring counts per disc are 2, 3, 5, or 6 depending on the zone. Zone 5 is a
*Sonderzone* with a crescent and eye motifs; zones 1 and 2 carry a star and plain
ring, respectively. The iconography — sun discs, crescent, wheels, eye, the axial
cone form in a sun-cult context — is unambiguously cosmic. That is not in dispute.

---

## 2. The Question and What Counts as a Hit

**Central question:** Does the ornament deliberately encode a precise astronomical
calendar, and if so, which one?

A correspondence between the ornament's counts and a calendar period is evidence
only when it is *statistically selective* — i.e. it appears with a frequency clearly
above what a blind search over plausible counting combinations would find by chance.
The bar set at the outset of this investigation (`CASE.md`):

> A *statistically selective* correspondence between a **pre-registered** counting
> rule applied to the **measured** ornament and a calendar/astronomical period, that
> survives a null model and is corroborated by independent data (metrology, find
> context, iconography, or a second object).

What does **not** count: a block of zones chosen after seeing the number it reaches;
a reading that reuses another author's measurements to "confirm" those measurements;
a claim whose central free parameter (which zones are intercalary) moves between the
author's own publications.

All three exclusion criteria are satisfied by the claims reviewed here. That is the
frame for everything below.

---

## 3. The Counts (Claim A — solid)

Wilfried Menghin (2000, 2010) measured the ornament in detail. The counts:

| Quantity | Value | Verified by |
|---|---|---|
| Ornament zones | 21 | `verify_calendar.py` |
| Disc-bearing zones | 18 (Z3–Z21, excl. Z5) | `verify_calendar.py` |
| Bossed discs | 418 | `verify_calendar.py` |
| Total concentric rings (Z3–Z21, excl. Z5) | 1701 | `verify_calendar.py` |
| Special signs Z5 | 38 | `verify_calendar.py` |
| System zones 3–21 ring total | **1739 = 1701 + 38** | `verify_calendar.py` |
| Ezelsdorf symbol total | ≈ 499 (not 1739) | `verify_menghin2000.py`, C5 |

These are not controversial. **Claim A is solid.** Every identity reproduces from
the per-zone table without exception, and the 2010 Berlin table (Menghin, Abb. 23)
reproduces the 2000 table (Abb. 14) zone for zone. One small transcription slip
recurs in both editions: zone 8 prints `A = 40` but the body gives a product
consistent with 39; it appears to be a typescript error, not a counting error.

**A note on Ezelsdorf.** An earlier AI-generated digest in this investigation
reported Ezelsdorf-Buch as having ~1739 symbols in 23 bands — the same figure as
Berlin. This is false. The actual count, read from Menghin 2000 Abb. 27 and
confirmed by the per-zone table, is **499 stamped symbols** (432 disc symbols + 24
small bosses + 22 eye + 21 wheel motifs) across zones 2–20, with 1463 rings in
zones 3–20. The phantom figure was a hallucination that manufactured agreement;
it is listed in `sources/phantom_references.md`.

---

## 4. The Calendar Hypotheses (Claim B — assessed)

### 4.1 Menghin: lunisolar / bound calendar (1000–800 BC)

**The claim.** The 16 time blocks formed by grouping the 19 system zones (Z3–Z21)
encode the 19-year Metonic cycle: 235 lunations, 228 solar months, 365-day solar
year, 354-day lunar year. Three zones (Z7, Z16, Z17) serve as intercalary zones
(*Schaltzonen*), subtracted from or added to blocks as needed.

**Strongest point.** Zone 21, the single bottom band, has exactly **47 discs** each
with 5 rings, giving `47 × 5 = 235` — the Metonic lunation count — from one zone,
with no block choice and no intercalary subtraction. This is the cleanest fact in
the corpus. Menghin also notes that 1739 is within 0.2 % of both 1735 d (57 solar
months) and 1742 d (59 lunations), making the grand total a genuine "midpoint".

**Problems:**

1. *Block freedom.* The 16 time blocks are not uniquely forced. The same target
   numbers (365, 354, 235, 228) are reachable from multiple distinct block choices,
   so the system finds the number first and the block second. Two of Menghin's 16
   states (61.2 and 64.4) do not close cleanly on his own terms
   (`verify_scenarios.py` flags both rather than hiding them).

2. *Intercalary drift.* The intercalary set is `{5, 16, 17}` in the 2000 Wikipedia
   summary, `{7, 16, 17}` in the 2010 monograph (pp. 47–63). The parameter that
   makes the arithmetic close is not stable between the author's own publications.
   Menghin (2000, p. 71) acknowledges that the number-hitting requires "nur bei
   flexibler Handhabung der … 'Schaltzonen'" — flexible handling of the intercalary
   zones. Schlosser (2003) quotes this directly and replies that it "demonstrates
   the cleverness of the authors, not the astronomical knowledge of the Bronze Age".

3. *Statistical test.* The day-values of zones 3–21 are not measurably richer in
   calendar numbers than random permutations of the same values (§5 below).

4. *Cross-hat test.* Menghin (2010, p. 65) states the interpretation "lässt sich
   partiell auf seine drei Vergleichsstücke übertragen" — it transfers *only
   partially* — and on Ezelsdorf (p. 68): "keine direkten kalendarische Werte
   ermitteln lassen" — the stamp rule yields no direct calendar values. That is the
   author's own conclusion (§6 below).

**Confidence: 20–30 %.** The astronomical symbolism is secure; the arithmetic
calendar is not demonstrated.

---

### 4.2 Schmidt-Kaler: Venus + Mercury (2012)

**The claim.** The same ornament encodes a Venus calendar (synodic period 584 d)
and a Mercury calendar (synodic period 117 d), using the same measurements as
Menghin.

**Problem.** Schmidt-Kaler reuses Menghin's counts; he makes no new measurement.
His sums reproduce (`verify_venus_hypothesis.py`, control C3), but a reading that
recycles another's data to "confirm" that data is not independent corroboration.
That Menghin's counts support *both* a lunisolar and a Venus+Mercury reading is a
count against both, not for either: the numbers are not selective enough to
distinguish astronomical intentions.

**Confidence: 10–20 %.** The sums reproduce, but the source dependence and the
selectivity failure (§5) both argue against it.

---

### 4.3 Lorenz: Metonic structure (2010/2011)

**The claim.** The hat has **19 line-bands** that divide **12 + 7**, directly
encoding the Metonic cycle: 12 months in an ordinary year, 7 intercalary months
over 19 years, `12 × 12 + 7 × 13 = 235 lunations`.

**What holds.** The **12 + 7 ring-count split** is real and visible. The 19
disc-bearing friezes divide into 7 friezes whose discs carry 5 concentric rings
(the packed, higher-ring discs) and 12 others (smaller discs linked by the little
annulets). This alternating structure is visible in museum photographs. It is a
genuine design feature.

**What does not hold:**

1. *The 19 is a redefinition.* The hat has **21** measured ornament zones. Lorenz
   reaches 19 by counting only the disc-bearing zones and excluding Z2 (plain rings)
   and Z5 (crescent/*Sonderzone*), which he never states explicitly. The "19 bands"
   is not the measured structure; it is a redefinition constructed to match the
   Metonic number.

2. *The arithmetic is trivial.* `12 × 12 + 7 × 13 = 235` for **any** 12+7 split
   of groups averaging 12 and 13. It is not evidence; it is arithmetic. Lorenz also
   reuses Menghin's `19 × 5 = 235` alongside it.

**Loose end.** Whether the three 6-ring friezes (Z15, Z18, Z19) carry fillers
decides the split as 7 vs. 10; this requires the high-resolution plates or Schauer
1986 (print-only, not yet held).

**Confidence: 25–35 %.** The 12+7 ring-count split is a genuine structure; the
19-band headline and the Metonic payoff are not demonstrated.

---

### 4.4 Hansen & Rink: eclipse / Saros / Metonic (2008)

**The claim.** A separate independent model, connecting the Nebra Sky Disc,
Trundholm Sun Chariot and the Berlin Gold Hat via lunar eclipses, the Saros cycle,
and the derived Metonic intercalation cycle.

**Status: abstract only.** The 2013 abstract confirms explicitly that the Berlin hat
is included in the model: "von der Himmelsscheibe von Nebra über den Sonnenwagen von
Trundholm **bis zu dem Berliner Goldhut**". The chapter itself (Nuncius Hamburgensis
8, ch. 9, p. 131 ff.) is not yet held; the per-zone arithmetic is not available to
assess. This is a genuine independent explanation that deserves a full reading.
It is recorded as outstanding (`todo/T3`, low priority).

**Confidence: unassessable from the abstract alone.** Noted as candidate.

---

### 4.5 Craft-geometry — counts determined by circumference / tool pitch (2026)

**The claim.** The disc counts per zone are not calendar encodings but are
determined by a craft constraint: each punch tool was placed at a characteristic
centre-to-centre spacing (the *pitch*), and the count in a zone is simply how many
fit around the circumference at that height. The hat's genuine design content is
structural and iconographic (axis mundi cone form, 12+7 alternation, 3×7 partition),
not numerical.

**Evidence (quantitative, reproduced by `scripts/verify_craft_geometry.py`):**

1. *Pitch constancy.* For every tool used in multiple Berlin zones, the pitch is
   constant to within ~1 mm (4.5–8.1 % of mean). On a hand-beaten Bronze Age gold
   sheet, this indicates a fixed working practice.

2. *Count prediction.* `round(circumference / mean_pitch)` predicts the disc count
   for **14 of 16 shaft zones exactly** (max |residual| = 1). The two Krempe zones
   are packed 5–12 % tighter — the goldsmith filled the brim ring — explaining their
   larger residuals.

3. *Cross-hat monotonicity.* If the pitch is constant, zones sharing a tool should
   show non-decreasing counts from apex to base (wider cone = more discs). This
   holds **perfectly** for Berlin, Schifferstadt, and Avanton (11 of 11 multi-zone
   tools); Ezelsdorf shows 4 of 6 (the fragmentary hat with uncertain tool
   assignments).

4. *Zone 21's 235 is geometric.* The outer Krempe ring circumference (~829 mm)
   divided by tool 14's Krempe pitch (~17.65 mm) gives `round(47) = 47`. That
   `47 × 5 = 235` is a consequence of the brim diameter and punch spacing, not a
   deliberate Metonic encoding.

5. *The cross-hat failure is predicted.* Each hat has a different profile and
   different punches. The counts are geometry-specific, not rule-specific.
   Structural similarities (all cones, all gold, all sun discs) reflect a shared
   cosmographic tradition; numerical differences reflect different geometries.

**Confidence: 55–65 %.** The pitch constancy and count prediction are quantitative
and reproducible. The hypothesis extends the sceptical position by providing a
*mechanism* for the counts rather than merely arguing that the calendar readings are
not selective. It has not been peer-reviewed.

---

## 5. The Statistical Test: Fuls's Combinatorial Null (Reproduced)

Andreas Fuls (2008) built the published quantitative null for the calendar
hypothesis. His method: for each of four combination rules (arbitrary non-empty
subsets, A; same-stamp-group subsets, B; contiguous blocks, C; contiguous blocks
minus intercalary subsets, D), count how many zone-value combinations fall within a
tolerance of each of nine astronomical periods, and compare with the chance baseline
`w = 2·t_p/p` (the fraction of the number line a period occupies at its tolerance).

This investigation re-implemented Fuls's method in `scripts/fuls_null.py` and ran
`--check` against his published Tables 8.2–8.5 (control C4). All cells reproduce,
with one documented edge case: Berlin's Mars count differs by one hit because Fuls
appears to have counted a zone-5 sum of 19 d as a zero-multiple hit of Mars, whereas
his own formula 8.1 requires `M ≥ 1`. The method-D rule (contiguous block minus any
subset of its intercalary zones, counting distinct zone sets) had to be recovered
from the text; it gives Berlin `G = 699` exactly.

**Results for Berlin:**

| Method | Synodic month h/w | Tropical year h/w | Verdict |
|---|---|---|---|
| A | 6.76 % / 6.77 % | 0.55 % / 0.55 % | ≈ chance |
| B | 6.26 % / 6.77 % | 0.49 % / 0.55 % | ≈ chance |
| C | 5.71 % / 6.77 % | 0.00 % / 0.55 % | below chance |
| D | 6.58 % / 6.77 % | 0.43 % / 0.55 % | ≈ chance |

The Berlin hat's ring sums are **not measurably richer in calendar numbers than
chance**. The tropical-year rate is *below* chance under contiguous-block methods.
The system finds approximately the expected number of hits regardless of whether the
zones are in their measured order or shuffled.

---

## 6. The Cross-Hat Test (Decisive)

The decisive test is: fix the counting rule on Berlin (where it was developed) and
apply it blind to the other three gold hats. If the hat was designed as a calendar
tool, the same rule should yield calendar numbers on a second, independently
ornamented hat. If it lands on the chance line, the rule is overfitted to Berlin.

This test became runnable when Menghin 2000's four per-zone tables were transcribed
from the page images into `data/readings/menghin2000_zones.json` (control C6,
2026-10-12). The cross-hat run of `scripts/fuls_null.py` gives:

| Hat | Method | Synodic month | Verdict |
|---|---|---|---|
| Berlin | A–D | ≈ chance (see §5) | baseline |
| **Schifferstadt** | **B** | **16.13 % vs 6.77 %** (5 hits / 31 combos) | **above chance** |
| Schifferstadt | C/D | 5.45 / 5.80 % | marginal (solar month only) |
| Avanton | A–D | 6.3–6.8 % | ≈ chance |
| Ezelsdorf | A–D | 6.2–6.9 % | ≈ chance |

**Only Schifferstadt, method B, synodic month is clearly above chance** — by a
factor of approximately 2.1. Schifferstadt is also the hat with independent
metrological corroboration: its proportions (Kalotte : upper shaft = 3:9; diameters
4.5:7.5 = 9:15) are consistent with the synodic month being a design unit. That is
the corroboration the hit definition asks for — and it belongs to Schifferstadt, not
Berlin.

**Menghin said so himself.** Menghin (2010, p. 65): the interpretation "lässt sich
partiell auf seine drei Vergleichsstücke übertragen" — transfers *only partially*.
On Ezelsdorf (p. 68): the stamp-identity rule "lässt sich … keine direkten
kalendarische Werte ermitteln" — yields no direct calendar values. He then falls
back to post-hoc contiguous block sums, which is exactly the block-choice freedom
the hit definition excludes.

**Peter-Röcher confirmed it** (2023, pp. 135–136): the calculation "ließ sich leider
nicht übertragen" — could not be transferred to the other three hats — and "gerechnet
wird also immer ausgehend vom gewünschten Ergebnis" — calculation proceeds from
the desired result.

The cross-hat failure is not merely our negative; it is documented in the primary
source and in a peer-reviewed critique, and it is now also reproduced in-repository.

---

## 7. The Sceptical Position (Best-Supported)

The sceptical reading — *cosmic yes, precise arithmetic no* — is backed by four
independent lines of evidence:

1. **The astronomical argument (Schlosser 2003).** The synodic lunar year averages
   354.37 d but varies by more than 26 hours from year to year. "Es gibt nicht 'das'
   Mondjahr schlechthin, und die Zahl 354 macht nur im Mittel Sinn — nicht im
   Einzelfall!" A running calendar of 354 marks would be wrong in most individual
   years. The Metonic rule holds only ~2/3 of the time in Schlosser's 1967–2003
   sample. Precision arithmetic breaks on the variability of the object being counted.

2. **The statistical argument (Fuls 2008, reproduced here).** Berlin sits on the
   chance line under all four methods (§5). The tropical-year rate is below chance
   under contiguous-block methods. The numbers are easy to hit, and the real hat is
   no better than a shuffled one.

3. **The transfer argument (Menghin 2010, Peter-Röcher 2023, reproduced here).**
   The rule fails on the other three hats. If it were a designed tool, it should not
   fail (§6).

4. **The free-parameter argument.** With block choice and intercalary zone choice
   both free, the system has enough degrees of freedom to "find" a calendar in almost
   any structured set of numbers. Menghin himself acknowledged this ("flexibler
   Handhabung der Schaltzonen"). A good calendar device does not need two free
   parameters and ±2–4 d tolerance to reach its targets.

None of this says the ornament is meaningless. It says:

- The **cosmic symbolism is real** (sun discs, crescent, eye, cone form, sun-cult
  context — certainty > 85 %).
- The **ornament is systematically structured** (alternating disc types, three
  unique-stamp zones, clean zone hierarchy — not random).
- **Zone 21's 47 × 5 = 235** is the single strongest numerical fact; it is
  remarkable even if the broader arithmetic is not demonstrated.
- The ornament may be a **mnemonic or symbol system** — encoding a few key numbers
  and a felt rhythm — without being a precise 19-year calculator.

---

## 8. Summary: Confidence Table

| Reading | Central claim | Confidence | Limiting factor |
|---|---|---|---|
| Cosmic symbolism | Sky is in the design | > 85 % | Not in dispute |
| Menghin lunisolar | 19-year Metonic calculator | 20–30 % | Selectivity failure; cross-hat failure; free parameter drift |
| Schmidt-Kaler Venus | Venus + Mercury encoding | 10–20 % | Reuses Menghin's numbers; not selective |
| Lorenz 12+7 structure | 19-band Metonic structure | 25–35 % | "19" is a redefinition; arithmetic is trivial |
| Hansen & Rink eclipse | Saros/Metonic via eclipses | unassessable | Chapter not yet held |
| Schifferstadt synodic | Synodic month on Schifferstadt | ~50 % | Method B selective; metrological corroboration |
| **Craft-geometry** | **Counts = circumference / tool pitch** | **55–65 %** | **Quantitative; predicts cross-hat failure; not yet peer-reviewed** |
| Sceptical position | Cosmic yes, arithmetic no | ~70 % | Best-supported by held sources |

---

## 9. What Remains Open

**Low priority (does not change the conclusion):**

- **Hansen & Rink chapter** (Nuncius 8, ch. 9, p. 131 ff.) — abstract confirms
  Berlin is included in the eclipse/Metonic model; per-zone arithmetic outstanding.
  Would provide an independent mechanistic account; would not overturn the Fuls null
  unless it pre-registers a selective rule.
- **Ezelsdorf stamp transcription** — our 12-group reading of Menghin 2000 Abb. 27
  vs. Fuls's 16; does not change the cross-hat conclusion (Ezelsdorf sits at chance
  under both readings).
- **Z15/Z18/Z19 filler question** — decides the 12+7 split as 7 or 10; needs
  high-res plates or Schauer 1986.

**Medium priority:**

- **Schauer 1986** (*Die Goldblechkegel der Bronzezeit*) — the foundational
  typological monograph; print-only, not yet obtained. Provides the original gold-hat
  typology and the Ezelsdorf stamp classification that Fuls used.
- **Menghin 2003 catalogue chapter** — print-only; gives the Schaltzone definition
  (`§8.4.4`, cited in Fuls) and may resolve the Berlin intercalary drift.

---

## 10. Implications for the Replica (Stage 2)

The Stage-2 LED display and M5 screen should present the readings as **plural and
explicitly uncertain**. The research supports:

- Showing **all six readings** (Menghin, Schmidt-Kaler, Lorenz, Hansen & Rink,
  craft-geometry, and the sceptical position) labelled by author
  and confidence.
- A "how sure are we?" mode that displays the statistical basis: the Fuls null
  result, the cross-hat result, the Menghin transfer admission.
- **Schifferstadt** as the hat with the strongest calendar signal — it is a better
  candidate than Berlin for the synodic month story.
- **Zone 21** as the strongest single fact on Berlin: `47 × 5 = 235 lunations` from
  one band, no free parameters — though the craft-geometry analysis shows that 47 is
  also the geometric prediction for the Krempe circumference and tool pitch.
- A **"craft" mode**: zones light up by tool type, showing the
  counts as following the circumference and the 12+7 alternation as a design grammar.

The honest exhibit is: *here are the theories, here is the evidence, here is why the
question is still open*. This is more interesting, and more accurate, than asserting
a calendar.

---

## 11. Sources Held

| Source | Role | Notes |
|---|---|---|
| Menghin 2000 (Acta Praehistorica et Archaeologica 32) | Primary measurement — all 4 hats | Complete; per-zone tables transcribed (C6) |
| Menghin 2010 (*Der Berliner Goldhut*) | Primary monograph — Berlin | Complete; "Der Vergleich" chapter (pp. 64–72) read |
| Fuls 2004 (ORDO ET MENSURA VIII) | Statistical analysis — early version | Held |
| Fuls 2008 (Nuncius Hamburgensis 8, 113–129) | Statistical null — main result | Held; reproduced in `scripts/fuls_null.py` (C4) |
| Schlosser 2003 (JSMV 86) | Astronomical critique | Held |
| Peter-Röcher 2023 (BUFM 106) | Archaeological critique | Held |
| Schmidt-Kaler 2012 | Venus/Mercury hypothesis | Held (scanned PDF) |
| Lorenz 2010/2011 + 2nd ed. | Metonic structure hypothesis | Held |
| Hansen & Rink 2008 (Nuncius 8, ch. 9) | Eclipse/Saros/Metonic model | Abstract only; chapter outstanding |
| Amendola 2021 (JSA 7) | Schifferstadt landscape hypothesis | Abstract only; paywalled |
| Schauer 1986 | Typological monograph | Print-only; outstanding |
| Phantom references (3) | Hallucinated citations | Documented in `sources/phantom_references.md` |

---

*Controls recalled: 7/7 (C1–C7). Cost: $0.00 (no paid model API; stdlib scripts +
free scholarly APIs). Scripts: `verify_calendar.py`, `verify_scenarios.py`,
`verify_venus_hypothesis.py`, `verify_menghin2000.py`, `fuls_null.py`.*
