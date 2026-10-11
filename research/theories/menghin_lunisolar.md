<!-- Consolidated 2026-10-10: moved from research/MENGHIN_HYPOTHESIS.md into
theories/ per research/AGENTS.md. Content unchanged apart from updated
cross-references. Scripts it cites are still at scripts/verify_calendar.py and
scripts/verify_scenarios.py. External corroboration and the Fuls (2004, 2008)
statistical result are now in theories/fuls_correction_cycles.md and
sources/fuls_2008.md. -->

# Is Menghin's calendar reading of the Berlin Gold Hat correct?

**A provisional assessment — a reasoned opinion about a hypothesis, NOT evidence, and NOT a result.**

> ⚠️ **Status: provisional.** This document is an *interpretation of an interpretation*. It
> weighs a published hypothesis (Menghin 2010) using the data we happen to have and two
> quick statistical checks. It proves nothing about the Bronze Age, about Menghin's
> scholarship, or about the object. Treat every "conclusion" below as an *argument to be
> attacked*, not as a finding. Where a number appears, the method that produced it is
> stated so it can be re-run and contradicted.

- **Subject:** the claim that the ornament of the Berlin Gold Hat (Urnfield/Hallstatt,
  c. 1000–800 BC) deliberately encodes a bound lunisolar calendar — specifically the
  19-year Metonic cycle, with 235 lunations and 228 solar months.
- **Source of the claim:** W. Menghin, *Der Berliner Goldhut: Ornamentanalyse* (2010),
  pp. 47–63, in `assets/menghin/2010/text/menghin_pages47-63.txt` and
  `assets/menghin/2010/jpg/menghin_page60..63.jpeg`.
- **Data used here:** `data/zones.json` (per-zone motif and ring counts) and
  `data/scenarios.json` (the 16 time blocks of Figs 61.1–64.4).
- **Date of assessment:** written while the P5 fit-test print was running; cross-hat test
  result added below.

---

## 1. Two claims with very different status

The single most useful move is to separate Menghin's *description* of the object from his
*interpretation* of it.

**Claim A (description):** the counts. The hat has 21 ornamental zones; 418 bossed discs
(Nos. 8–15) over 18 disc-bearing zones carry 1701 concentric rings; zone 5 adds 38
"special signs"; zones 2–21 total 1783 ring-units, and the 19 system zones (3–21) total
1739.

**Claim B (interpretation):** those numbers, read as *days*, encode a lunisolar calendar,
and the zones group into 16 time blocks (4…19 quarter-years / 12…59 lunations) whose
solar and lunar sums reproduce 365, 354, 235, 228, …

**Claim A is solid.** It is not a matter of opinion: we reproduce every total from
independent data, and the identities are cross-validated four ways in
`scripts/verify_calendar.py` (`1739 = 1701 + 38`; `1783 − 44 − 38 = 1701`; `418` and
`1739` from the zone table; totals summing to 745 mm). If Menghin is wrong, he is not
wrong about the counts.

**Claim B is the hypothesis.** It is plausible, argued in good faith, and — as of this
assessment — *not established*. Everything below is about Claim B.

---

## 2. The sceptical test: is the pattern surprising?

The obvious objection to any "the numbers encode a calendar" claim is that with ~19 zone
values, an interpreter can choose contiguous blocks (and optionally add or drop the
three "intercalary" zones) until round calendar numbers appear. That is *numerology*
unless the real arrangement is measurably richer in hits than chance.

**Method.** Zones 3–21 have day-values
`42, 75, 38, 90, 57, 105, 57, 95, 60, 100, 60, 105, 90, 38, 66, 126, 138, 162, 235`.
For every contiguous block, optionally subtracting any subset of the intercalary zones
{7, 16, 17} that lie inside it, count how many sums land within ±tol of
{365, 366, 354, 355, 235, 228, 177}. Then repeat with the same 19 values **shuffled**
into random zone positions (10 000 permutations) and compare.

| test | real hat | random shuffles | P(random ≥ real) |
|---|---|---|---|
| ±2 d, with intercalary subtraction | 12–15 hits | median 9–12, 95th pct 14–18 | **0.12–0.16** |
| ±4 d, no subtraction | 7 hits | median 8 | **0.65** |
| ±4 d, with subtraction | 15 hits | median 15 | **0.38** |

**What this says.** At Menghin's own realistic tolerance (±4 d) the real hat sits **dead
on the median** of random arrangements. The hat's *ordering* is not unusually rich in
calendar numbers — you can find about as many by shuffling the same values. At the tight
±2 d tolerance the result is weakly suggestive (p ≈ 0.12–0.16) but nowhere near
significant (you would need the real hat to beat ~95 % of shuffles).

**What this does *not* say — limits, stated so they can be attacked:**

- My target list is my choice. A different list changes every p-value.
- The null permutes values among zones, which also destroys the ornamental structure.
  So it tests whether the *ordering* carries information (it does not), not whether the
  numbers are meaningless. A proponent can reply that the encoding is in the *structure*
  (which disc type sits where), not the order — but then the shuffled cases hitting just
  as often remains bad news, because it shows these magnitudes are *easy to hit*.
- I model "search all blocks" rather than Menghin's intended quarter-year rhythm. That
  makes **the sceptical case stronger than it should be**; a fairer test would restrict
  the block set. I flag this as a bias *against* Menghin.
- Two of the sixteen states (61.2, 64.4) do not close cleanly even on his own terms
  (`scripts/verify_scenarios.py` prints this rather than hiding it).

**Degeneracy.** With subtraction allowed, 365 is reachable by block 4–8 *and* 7–11; 354 by
12–15 *and* 16–19; 235 by 14–16 *and* 21–21. The specific blocks Menghin reports are
therefore underdetermined: the system finds the number first and the block second.

---

## 3. Where Menghin has genuine merit

1. **235 = 47 × 5 in zone 21, exactly the Metonic lunation count.** One zone, no free
   parameter, no subtraction. `47` is prime and an unusual count. This is the single
   strongest fact and the one a defence should be built on.
2. **The total 1739 sits within 0.2 % of both 1735 d (57 solar months) and 1742 d
   (59 lunations)** — a genuine "middle ground", exactly as he argues.
3. **The ornament is unambiguously cosmic.** Sun discs, moon crescent, eye motifs, wheels,
   on a beaten-gold ritual cone from a sun-cult context. *Some* astronomical content is
   close to certain; the disagreement is about precision and intent, not about whether
   the sky is in the design.
4. **The structure is systematic, not random.** The alternation of 3-, 5-, 2- and 6-ring
   discs, the three once-only stamps, the clean zone hierarchy — these are real design
   decisions. Menghin's counts are careful and internally consistent.

---

## 4. Where he could be mistaken

1. **Too many degrees of freedom.** Block choice *and* which intercalary zones to include
   are both free, yet the system still needs ±2–4 d and leaves two states unresolved. A
   designed calculating device should be exact; a mnemonic that "roughly reminds" is a
   weaker (and still interesting) claim.
2. **The key parameter moved.** The intercalary zone set changed from the earlier summary
   reading {5, 16, 17} to {7, 16, 17} in pp. 47–63. A hypothesis whose central knob is
   negotiable between its own statements is fragile.
3. **Competing readings of the same object.** Schmidt-Kaler reads a Venus calendar
   (584 d) into the same ornament (a full treatment and side-by-side comparison is in
   `theories/schmidt_kaler_venus.md`); others read pure ritual/decoration. When one artefact
   supports several numerological systems, confidence in any single one drops.
4. **Anachronism risk.** 235 lunations ≈ 19 years is a true astronomical fact, but the
   *precise intercalation rule* is a 5th-century-BC Greek/Babylonian construct. The hat is
   ~1000 BC. Menghin's bridge (oral Druidic transmission, per Caesar) is an argument from
   possibility, not evidence.
5. **No independent corroboration.** No text, no legend, and — the decisive gap — no
   demonstration that the *same rule* decodes the other gold hats.

---

## 5. The test that would actually move the needle: cross-hat validation

Fix the counting rule on the Berlin hat (which Menghin had in front of him), then apply it
**blind** to the other gold hats (Schifferstadt, Ezelsdorf-Buch, Avanton). If a system with
different zone/disc counts independently yields 365/354/235 by the same procedure, that is
strong evidence of design. If it only works on Berlin, the hypothesis is probably
overfitted.

A second, weaker test: **pre-register** the rule and targets, then check whether the
reported blocks are forced (unique) rather than one of many. §2 already shows they are not.

**Result:** see §6, appended after the test was run.

---

## 6. Cross-hat test — attempt and result

**Goal.** Fix the rule on Berlin, then apply it *blind* to another hat. If a system
with different zone/disc counts independently yields 365/354/235, that is evidence of
design.

**What I obtained.** An independent per-zone dataset for the **Ezelsdorf-Buch** hat: the
Commons plate *„Übersicht der Ornamentzonen und verwandten Hauptmusterpunzen“* (Wolfram
Kaiser, 2005, redrawn from Schauer 1986 and Menghin 2000). It gives ~19 ornament zones with
these stamped-symbol counts:

```
left:  19x Nr.11  27x Nr.9  28x Nr.11  39x Nr.10  32x Nr.13  19x Nr.16  22x Nr.20  21x Nr.19  14x Nr.18  22x Nr.18
right: 24x Nr.6   27x Nr.15 22x Nr.12  30x Nr.15  20x Nr.17  45x Nr.8   17x Nr.21  19x Nr.14  52x Nr.7
apex:  10-ray star (no count)
total: 499 stamped symbols across ~19 zones
```

**Result 1 — the repo's own earlier “corroboration” is false.** `theories/secondary_digest_2026-10-08.md`'s comparison
table asserted Ezelsdorf-Buch has **“~1,739 symbols in 23 bands”** — the *same* 1739 as
Berlin. The real figure is **~499 symbols in ~19 zones**. That was not independent evidence;
it looks like a summary that copied Berlin's total onto the other hat. A caution about the
source material, and a reason to distrust any “the other hats match too” claim that is not
backed by raw per-zone data.

**Result 2 — the full replication is blocked, not passed and not failed.** Menghin's unit is
the *ring*, and both the per-stamp **ring counts** and the **zone order** for Ezelsdorf are in
print-only sources (`Schauer 1986`, `Menghin 2000`, Acta Praehistorica 32). The plate shows
the symbol counts but neither the rings per stamp reliably nor the zone sequence. Without
both, the day-value block sums cannot be rebuilt. **Honest status: not runnable from
accessible data.** The experiment stays open; absence of corroboration is not refutation.

**Result 3 — the method is not selective, and that is worse than a failed replication.**
Running the *identical* finder on Berlin with three different “counting units”:

| unit | hits (±2 d) | random-shuffle median | P(random ≥ real) |
|---|---|---|---|
| rings × symbols (Menghin's unit) | 12 | 9 | 0.13 |
| **symbol counts only** | **43** | 37 | 0.14 |
| rings per symbol only | 0 | 0 | – |

Counting **plain symbols** lands on the calendar targets *more* often than counting rings.
So “we can find 365/354/235 in the sums” is **not** evidence that rings are the encoded unit:
the numbers surface under either reading, and the real arrangement never beats the shuffled
null. The corollary is serious — **a positive result on another hat would not be
corroboration either**, unless the rule is pre-registered and shown to be selective first.

**Result 4 — the intercalary set is not stable across Menghin's own publications.** The
transcript of Menghin (2000) carried on Wikipedia gives the 54-month example as
`1739 − (zones 5+16+17 = 142) = 1597` and calls zones **{5, 7, 16, 17}** the *Schaltzonen*.
The 2010 figures (pp. 60–63) colour only **{7, 16, 17}** green. The one parameter that makes
the arithmetic close moves between the two statements.

**Net effect on the verdict.** The cross-hat test did not corroborate the hypothesis; and,
more damagingly, the finder it would have to use is not selective enough to corroborate
anything. This nudges confidence in the strong claim **down** (see §7).

---

## 7. Provisional verdict (subject to §6)

- **Confidence that the hat carries solar/lunar/astronomical symbolism: high (> 85 %).**
  The iconography and context are not seriously in doubt.
- **Confidence that the strong Menghin claim — a deliberately encoded, self-consistent
  lunisolar calculator at the level of the 16 states — is essentially right: low
  (20–30 %).** (Reduced from 25–35 % after §6: the cross-hat test did not corroborate it and
  the method proved non-selective.)
- **Best guess at the truth:** closer to "a structured mnemonic encoding a few key numbers
  (235, 365, ~354) and a felt rhythm, with the precise arithmetic largely reconstructed by
  the interpreter" than to "a precise 19-year calculator".

Menghin is not a crank: his measurements are careful and his question is legitimate. But
*careful scholar with a plausible pattern* is not the same as *proven*, and the burden of
proof here has not been met. "Could he be mistaken?" — yes, and the most likely error is
not fabrication but apophenia: reading a designed system into numbers that were designed,
but designed as ornament.

---

## 8. What this means for the replica (unchanged)

None of the above changes what to build. The practical rule:

- Present the 16 scenarios as **Menghin's hypothesis**, labelled as such on the M5 screen.
- Keep `data/scenarios.json` as a *faithful transcription* (exactly what it is), with
  `scripts/verify_scenarios.py` showing which parts are Menghin's arithmetic (30 stated
  zone-sums reproduce) and which are his caveats (61.2, 64.4 flagged, not forced).
- Do not let the demo imply the question is settled. A museum-grade replica that says
  "here is one reading, and here is why it is uncertain" is both more honest and more
  interesting than one that asserts a calendar.

---

## Appendix — how to reproduce the checks in this document

```bash
# the zone counts and identities (Claim A)
python3 scripts/verify_calendar.py

# the 16 scenario blocks, Menghin's own zone arithmetic, and its caveats
python3 scripts/verify_scenarios.py
```

The Monte-Carlo figures in §2 were produced with the day-values of zones 3–21 and
10 000 random permutations; the script is not committed (it is a few lines) but is
reproducible from the description in §2 and the values printed there.
