# Is Schmidt-Kaler's Venus reading of the Berlin Gold Hat correct?

**A provisional assessment of the Schmidt-Kaler (2012) hypothesis, and a side-by-side
comparison with Menghin (2010). A reasoned opinion about a hypothesis, NOT evidence,
and NOT a result.**

> ⚠️ **Status: provisional.** This is the companion to `MENGHIN_HYPOTHESIS.md`. That
> document weighs Menghin's lunisolar reading; this one weighs Theodor Schmidt-Kaler's
> alternative Venus reading and asks which of the two is more likely. It proves nothing
> about the Bronze Age or about either scholar. Treat every "conclusion" below as an
> *argument to be attacked*. Where a number appears, the method that produced it is
> stated so it can be re-run and contradicted.
>
> **Primary source used here:** T. Schmidt-Kaler, *Ein Venus-Kalender auf dem Berliner
> Goldhut — Zur Entstehung und Entwicklung der Goldhüte als Kalender-Gerät* (2012),
> `https://www.quantenbit.physik.uni-mainz.de/files/2020/03/Goldhut-TSchmidtKaler-2012.pdf`.
> The PDF is a **scan with no text layer**; the quotations and zone numbers below come
> from a machine OCR (tesseract, `deu`) of that scan, so wording and a few digits may be
> imperfect. The file also binds a second, separate article on the Schifferstadt hat
> (Schmidt/Schmidt-Kaler/Theuerkauf) after Schmidt-Kaler's Venus paper; only the Venus
> paper is assessed here.
>
> **Data used here:** the same `data/readings/menghin.json` and
> `data/readings/schmidt_kaler.json` as the Menghin assessment, via
> `scripts/verify_venus_hypothesis.py` (new, committed with this document).
>
> **Date of assessment:** written after re-running the Menghin arithmetic with the
> Schmidt-Kaler targets added.

---

## 1. What Schmidt-Kaler actually argues

The essay is much broader than the hat: it opens with a long cultural-astronomical
argument (Venus pentagram, Babylonian *Ammizaduga* texts, Homeric hymns, the Genesis
"two camps" of Jacob, the Salzmünde stone axes) and only turns to the Berlin hat on
about its thirteenth page. The hat-specific claims are these.

**Claim A (description).** The object's ornaments and the counts *per zone*. Schmidt-Kaler
does **not** recount the hat. He adopts Menghin's own day-values explicitly — the paper
says the sums are "gemäß Menghin" ("according to Menghin") — and reuses them:

- zone 7 = 19 discs × 3 rings = **57**
- zone 21 = 47 discs × 5 rings = **235**
- zone 3 = 14 × 3 = **42**, zone 4 = 15 × 5 = **75**, zone 5 = 38, zone 17 = 33 × 2 = **66**

**Claim B (interpretation).** That those values encode a running **Venus calendar**
(and a Mercury calendar), not (only) a lunisolar one:

1. **Iconography.** The apex ends in an **eight-rayed star**, which he reads as the
   symbol of Venus — the 8:5 octaeteris: 8 solar years = 5 Venus synodic periods
   (8 × 365 = 2920 = 5 × 584).
2. **The 19s.** Zone 5 has 19 crescent-and-dot motifs above 19 almond/eye motifs. He
   reads both as Venus and credits the count 19 to Menghin's lunisolar starting point.
3. **Venus half-cycle.** zone 7 + zone 21 = 57 + 235 = **292** = ½ × 584, the duration
   of one morning-star or evening-star apparition. He himself records the errors of
   this first solution as −13/70 ≈ **−19 %** (57 vs the ~70-day segment) and +6 %
   (235 vs ~222 days).
4. **A "better" second Venus solution.** zone 3 + zone 5 + zone 17 = 42 + 38 + 66 = **146**,
   then ×2 = **292** and ×4 = **584**, arranged as a mirror structure for the morning and
   evening star, with errors −6 %, +0.5 %, averaging ≈5 %. He asks in the paper itself:
   *"Welche der beiden Lösungen ist die bessere?"* — which of the two solutions is better?
5. **Mercury.** zones 3 + 4 = 42 + 75 = **117** ≈ Mercury's 115.88-day synodic period;
   and 5 × 117 = **585** ≈ 584 (the Venus period). Zone 3's 42 also matches the ~42-day
   visibility of Mercury.

**What he does *not* claim.** He does not say Menghin is wrong. He writes that the
punches Menghin studied "perhaps *also* contain a Venus calendar" and treats the
lunisolar numbers (19, 235) as already present. The Venus reading is offered as an
**additional layer**, not as a refutation.

---

## 2. Where the astronomy is right

This part should be said plainly, because a fair assessment cannot pretend it is all
numerology.

1. **The periods are correct.** Venus's synodic period is 583.92 d; 584 and its half
   292 are the standard calendar numbers. 5 × 584 = 2920 = 8 × 365. Mercury's synodic
   period is 115.88 d. None of this is in dispute.
2. **The eight-pointed star is a real Venus symbol.** In Mesopotamian religion the
   eight-pointed star is the star of Inanna/Ishtar, the Venus goddess. So the apex motif
   reading has genuine iconographic precedent, not just wishful shape-matching. This is
   the single best thing in the paper.
3. **His prior argument has force.** He argues that a *Venus* calendar is much easier to
   build than a *lunisolar* one (the ratio 8/5 is good to 0.08 %; 12 lunar months against
   a solar year is off by 3.1 %), so if a Bronze Age people encoded a calendar, Venus is
   the more tractable target. That is a legitimate reason to take a Venus encoding
   seriously in principle. Note, though, that it argues against the *precision* of
   Menghin's Metonic calculator, not against lunisolar symbolism.
4. **Chronology is on his side, not Menghin's.** The 8-year octaeteris is attested far
   earlier (Babylonian *Ammizaduga* material, ~16th c. BC) than a formal 19-year
   intercalation rule (cuneiform hints only after ~1100 BC; the Greek/Babylonian
   19-year cycle is 5th–4th c. BC). The hat is c. 1000 BC.

---

## 3. The arithmetic, tested

`scripts/verify_venus_hypothesis.py` reproduces every sum Schmidt-Kaler states, then
measures how much information each number carries. The point of the second step is the
same as in `MENGHIN_HYPOTHESIS.md` §2: with ~19 zone values, a number that can be hit
in many ways is weak evidence of design; a number that can be hit in one way is strong.

**Reproduced exactly** (all assert-passing):

```
57 + 235            = 292
42 + 38 + 66        = 146   ->  x2 = 292,  x4 = 584
42 + 75             = 117   ->  x5 = 585
```

**How many ways?** Subsets of the 19 day-values (zones 3–21) summing *exactly* to each
target, and whether any *contiguous* block does:

| target | subsets | contiguous blocks | comment |
|---|---|---|---|
| 42 | 1 | 1 | just zone 3 itself (trivial: it is a value, not a sum) |
| 117 (Mercury) | 5 | 1 (zones 3–4) | 4 other pairs also give 117 (7+11, 7+13, 9+11, 9+13) |
| 235 (Metonic) | 11 | 1 (zone 21) | but zone 21 alone is also Menghin's 235 |
| **292 (Venus ½)** | **27** | **0** | zones 7+21 and 9+21 are the only pairs; 25 larger subsets also hit it |
| **584 (Venus)** | **450** | **0** | reachable in hundreds of ways; never as one contiguous span |
| 585 | 476 | 1 | |

Two consequences follow immediately.

- **The Venus numbers are easy to find, and not by a reading rule.** 292 has 27 exact
  subset representations and 584 has 450. Neither is reachable by any *contiguous* block.
  So Schmidt-Kaler's method is not "read the ornament in sequence" — it is "choose a
  scattered group of zones until the target appears." That is a much larger search space
  than Menghin's contiguous-block rule, and a correspondingly weaker constraint.
- **The number he rests on is Menghin's number.** 235 is not an independent Venus datum:
  it is exactly the 47 × 5 = 235 that Menghin reads as the Metonic lunation count, and
  57 is 3 × 19. His headline Venus half-cycle is *235 (lunisolar Metonic) + 57
  (3 × 19 lunisolar)*. If zone 21 is meaningful, it is at least as naturally the
  Metonic number as the Venus one.

**The same test on the other counting unit.** Re-running the finder on the plain
ornament counts (Schmidt-Kaler's own 651-unit table, zones 3–21) makes things worse for
selectivity, not better:

```
292 under rings-as-days:      27 subsets, 0 contiguous
292 under plain ornaments:  3984 subsets, 1 contiguous  (zones 3-11)
```

So "we can find 292" is not evidence that rings are the encoded unit — the number
surfaces far more easily if you ignore rings. This is the same non-selectivity result
the Menghin assessment found for 365/354/235 (its §6, Result 3), reproduced here for the
Venus targets.

**Ordering is not special.** Shuffling the 19 day-values among the zones:

| target set | real contiguous hits | P(random ≥ real) |
|---|---|---|
| Venus 292/584/117, exact | 1 | 0.65 |
| Venus 292/584/117, ±2 d | 5 | 0.087 |
| Menghin 365/354/235/228/177, ±2 d | 5 | 0.58 |

The Venus ordering is *not* significant (the ±2 d case is weakly suggestive at best), and
neither is Menghin's. Neither the ordering nor the value-set is measurably richer in
calendar numbers than a random shuffle.

---

## 4. Where the Venus claim is weak

1. **It is parasitic on Menghin, not independent of him.** Every number comes from
   Menghin's day-value table ("gemäß Menghin"). It adds no new measurement of the object.
   Consequence: if the "ring = day" premise is wrong, both readings collapse together;
   and Schmidt-Kaler's reading *cannot* be better evidenced than the data it borrows.
2. **The search space is looser, so the fit means less.** Menghin at least fixes a rule
   (contiguous blocks, named intercalary zones). Schmidt-Kaler allows scattered zones,
   repeated zones, doubling and quadrupling, and then picks between two candidate
   solutions *after* seeing which fits better ("which of the two is better?"). The first
   solution carries a self-reported **19 % error** on one segment — poor for something
   meant to be a calendar, and a sign that the groupings are being fitted to the targets.
3. **The strongest number is Menghin's Metonic number.** As above: 292 = 235 + 57 is
   built from the lunisolar numbers. A Venus reading that needs the Metonic 235 to work
   is not an alternative to the lunisolar reading; it is downstream of it.
4. **It ignores the spatial structure that would be the real evidence.** 7 + 21 joins a
   shaft zone to a brim zone across the whole object; 3 + 5 + 17 likewise. A real encoded
   rule should be readable from the arrangement (as Menghin's zones and alternation at
   least attempt to be). Schmidt-Kaler's core arithmetic is essentially arrangement-free.
5. **It repurposes Menghin's "skipped" zones.** Zones 5, 7, 16, 17 are precisely the
   zones Menghin calls intercalary / not part of the solar-lunar sums. Schmidt-Kaler
   makes 5, 7, and 17 carry the Venus numbers. The two readings assign opposite roles to
   the same zones; at most one can be following the designer's intent, and this is
   another sign of fitting rather than reading.
6. **One object, three calendars.** The paper also extracts a **Mercury** calendar from
   zones 3 + 4. Menghin: lunisolar. Schmidt-Kaler: Venus *and* Mercury. When the same
   ornaments support several unrelated systems, the probability that any one of them is
   *the* intended system falls (the old "competing readings" objection, now with a second
   competitor added by the same author).
7. **The external corroboration is itself speculative.** The load-bearing external
   evidence is the Salzmünde "calendar axes" (Wegwitz), read as recording the 16:10 =
   8:5 Venus equation around 3400 BC. That reading is a contested hypothesis by the same
   author, not an independently accepted result, so it cannot carry the hat.
8. **The essay's habit of finding the same numbers everywhere weakens it.** Genesis
   animal totals (=580), Homeric hymn line counts (293, 580), Roman ten-month years,
   Jacob's 16 persons — all read as Venus/Mercury numbers. A method that decodes
   Scripture, epic poetry and a gold hat identically is a method with a very high false
   positive rate.

---

## 5. Side by side

| | **Menghin (2000/2010)** | **Schmidt-Kaler (2012)** |
|---|---|---|
| Claim | bound **lunisolar** calendar: 365/354/235/228, quarter-year states, Metonic | running **Venus** (584/292) and **Mercury** (117) calendar |
| Counting unit | rings: day_value = discs × concentric rings | the *same* rings/days, adopted **"gemäß Menghin"** |
| Independent measurement of the object? | yes — his own ornament analysis | no — reuses Menghin's table |
| Decoding rule | contiguous zone blocks, named intercalary zones subtracted | scattered/repeated zone sums, ×2 and ×4 |
| Uses the arrangement/ordering? | yes (which zone, 3/5-ring alternation, intercalary placement) | mostly no (7+21, 3+5+17 are non-adjacent) |
| Representations of the key number(s) | 365: 98 subsets; 354/228 by subtraction | 292: 27 subsets; 584: 450 subsets |
| Reachable by a contiguous span? | **yes** (365 = zones 4–8; 354 by subtraction; 235 = zone 21) | **no** for 292 and 584 |
| Ordering vs shuffle | not significant | not significant |
| Selectivity under the other unit | fails (Menghin doc §6) | fails worse (292: 3 984 subsets in the ornament unit) |
| Corroboration on other hats | cross-hat test attempted, **blocked/negative** | none; points to contested Salzmünde axes |
| Iconographic support | sun discs, crescent, eye, wheels | **eight-pointed Venus star** (real Ishtar symbol) |
| Chronological fit | Metonic rule is ~700 yr *later* than the hat | octaeteris is ~600 yr *earlier*; fits better |
| Scholarly status | museum monograph; basis of the Wikipedia "calendrical function" section | minority essay on a physics-department page; not in the archaeological reception stream |

---

## 6. Which of the two is more likely?

**Short answer: Menghin's lunisolar reading is the more likely of the two to reflect a
deliberate numerical encoding — but both are probably over-readings, and the margin is
not large.**

The reasoning, in order of weight:

1. **Neither is established.** Both are interpretations laid on the same ornament. The
   Monte-Carlo and subset counts say the same thing for both: their key numbers are easy
   to hit, and their orderings do not beat chance. So "more likely" is about which is the
   *better-supported reading*, not about certainty.
2. **Schmidt-Kaler's reading cannot outrank the data it borrows.** Its numbers are
   Menghin's numbers. It adds an interpretation, not evidence. All else equal, an
   interpretation that reuses another hypothesis's measurements is conditional on that
   hypothesis; it does not get an independent evidential boost.
3. **Its headline number is the lunisolar number.** 292 = 235 (Metonic lunations) + 57.
   The Venus half-cycle is assembled from the Metonic count. This makes the Venus reading
   look like a re-labelling of the stronger lunisolar facts, not a competitor to them.
4. **Menghin's rule is more constrained and more falsifiable.** A contiguous-block rule
   with named intercalary zones can fail; Schmidt-Kaler's free grouping, repetition and
   scaling can almost always succeed (27 resp. 450 representations of 292/584). A
   hypothesis that can always succeed is weaker evidence when it does.
5. **But Schmidt-Kaler wins two points that matter.** The eight-pointed Venus star is a
   genuine, well-attested symbol, and the 8-year octaeteris really is both easier and
   *earlier* than a 19-year lunisolar cycle. Those facts support a broader conclusion:
   the hat probably carries **layered astronomical symbolism** (sun, moon, and plausibly
   Venus) rather than a single precise calculator, and the strong, precise **Metonic
   calculator** reading is the one most at risk.

**Confidence estimates** (argued, not measured — attack them):

- that the hat carries **some** deliberate astronomical symbolism: **high (> 85 %)**, as
  in the Menghin assessment;
- that **Menghin's strong lunisolar-system claim** is essentially right: **low–moderate
  (20–30 %)**;
- that **Schmidt-Kaler's Venus-encoding claim** is essentially right as the *intended*
  system: **low (10–20 %)**; its iconographic and chronological points raise the odds
  that Venus is *present*, but the numerical encoding itself is weaker than Menghin's;
- **best guess at the truth:** a structured symbolic/mnemonic object carrying a few key
  astronomical numbers (19, 235, 365, ~354, plausibly 292/584), whose precise arithmetic
  — lunisolar *or* Venusian — is substantially the interpreter's reconstruction.

In one line: **Menghin is the better bet, Schmidt-Kaler is the better corrective.** The
Venus reading is unlikely to be *the* system, but it is a useful reminder that a single
object can carry more than one astronomical referent, and that the Metonic calculator
story is the part most likely to be wrong.

---

## 7. What would change this verdict

- **A blind, pre-registered rule.** Fix the Venus grouping rule *before* looking at the
  other hats, then apply it to Schifferstadt / Ezelsdorf-Buch / Avanton. If a hat with
  different zone counts independently yields 292/584 by the same rule, the Venus case
  rises sharply. This is the same cross-hat test that is still blocked for Menghin
  (`MENGHIN_HYPOTHESIS.md` §6): the raw per-zone ring counts and zone order for the other
  hats are not available in the accessible sources.
- **Independent per-zone counts.** Any dataset that counts the Berlin rings without
  going through Menghin would let the Venus and lunisolar readings be tested against each
  other on equal footing. Currently every number both authors use is the same number.
- **A demonstration that the arrangement encodes the Venus grouping.** If the zones
  Schmidt-Kaler selects (7+21, or 3+5+17) were shown to be marked on the object — by
  spacing, orientation, or punch type — the "ignores ordering" objection would fall.
- **Disproof of the ring-count premise.** If the concentric rings are not a counting unit
  (the "ornament only" reading), then both hypotheses lose together, and this comparison
  becomes moot.

---

## Appendix — how to reproduce the checks in this document

```bash
# Menghin's counts and identities (unchanged)
python3 scripts/verify_calendar.py

# Schmidt-Kaler's Venus/Mercury arithmetic, the subset counts, the
# non-selectivity check and the shuffle test
python3 scripts/verify_venus_hypothesis.py
```

The subset and contiguous counts are exhaustive over the 19 system zones (zones 3–21) of
`data/readings/menghin.json`; the shuffle test uses 20 000 random permutations of the 19
day-values (seed 1, so it is repeatable). The primary-source quotations and zone values
are from a machine OCR of the scanned 2012 PDF and should be checked against the scan
(`assets/` or the source URL) before being quoted as exact.

**Cross-references.** `MENGHIN_HYPOTHESIS.md` §2 (Menghin selectivity), §4.3 (competing
readings), §6 (cross-hat test, blocked / non-selective); `AGENTS.md` and `README.md`
Schmidt-Kaler digest; `data/readings/schmidt_kaler.json` (the 651 ornament table, flagged
*not a day count*); `IMPLEMENTATION_PLAN.md` §10 (why the two readings must stay separate).
