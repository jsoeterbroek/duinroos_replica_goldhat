# research — the story

The narrative for the write-up, in order, with credits for who had which idea.

## Beats

- **2026-10-08 — case opened.** Question: The Berlin Gold Hat. First pass:
  Menghin's lunisolar reading (2010), Schmidt-Kaler's Venus reading (2012), and an
  AI-written digest (`gold_hat.md`). The digest's *counts* were kept; its *calendar
  reasoning* and several of its citations turned out to be unverified.
- **2026-10-08 — the selectivity problem.** The Menghin assessment
  (`theories/menghin_lunisolar.md`) and its companion
  (`theories/schmidt_kaler_venus.md`) tested both readings against shuffled
  nulls. Result: neither author's key numbers are unusual once you allow the
  interpreter freedom to choose blocks; the counts are solid, the calendar
  reading is unproven. Credit: the *project author* posed the sceptical question;
  the *model* ran the Monte-Carlo.
- **2026-10-10 — consolidation.** The three legacy documents were restructured
  into the Antiquity folder scheme. `gold_hat.md` → a corrected secondary digest;
  the two assessments → `theories/`.
- **2026-10-10 — the missing literature was found, and the phantom literature
  exposed.** Searching the scholarly indexes (OpenAlex/Crossref) rather than
  trusting the digest surfaced:
  - **Andreas Fuls (2004, 2008)** — the quantitative, published version of the
    sceptical test. Fuls builds the full combinatorial null for all four gold
    hats and finds that **almost every astronomical association is what chance
    would give**; only *Schifferstadt* is clearly selective (synodic month).
    Credit: Fuls (the analysis); the *search step* here (finding and reading him).
  - **Luca Amendola (2021)** — shifts the argument from counting to *landscape*:
    the Schifferstadt burial place is astronomically meaningful, independent of
    the ornament.
  - **Thomas Lorenz (2010/2011, 2nd ed.)** — an independent modern *metonic*
    reading of the Berlin hat (19 line-bands, 12 + 7 friezes, 235), and
  - **Wolfhard Schlosser (2003)**, **Heidi Peter-Röcher (2023)** — the critical
    scholarship on Bronze Age lunar calendars and the "archaeoastronomical
    construct".
  At the same time the digest's three load-bearing extra citations —
  "Spurk/Gebhard/Schauer", "Wolfgang Schlosser (2004, 2012)" and
  "I. Mathieson (2010)" — could not be found in any index or library catalogue and
  are recorded as **phantoms** (`sources/phantom_references.md`). The real
  Schlosser is *Wolfhard*, and he wrote about lunar calendars and Nebra, not the
  hats. Credit for the correction: the source-by-source verification step.
- **2026-10-10 — verdict unchanged, evidence base stronger.** Fuls independently
  reaches the same conclusion the project's own scripts did: the Berlin hat's
  numbers are not demonstrably different from chance. The replica therefore shows
  the hypotheses *labelled as hypotheses*.
- **2026-10-11 — the critique arrives from the source floor.** The two critical
  papers that the first round could only see behind paywalls/JS walls were obtained
  and read in full. **Wolfhard Schlosser (2003)** supplies the missing astronomy:
  the synodic lunar year averages 354.37 d but **varies by more than 26 hours**
  year to year, so 354 is a mean and not a per-year count, and the Metonic rule holds
  only ~2/3 of the time. **Heidi Peter-Röcher (2023)** supplies the archaeology:
  the calculation could **not be transferred to the other three hats**, and — quoting
  Menghin's own words — "gerechnet wird also immer ausgehend vom gewünschten
  Ergebnis". The cross-hat test is now recorded as *failing in print*, not merely
  blocked here. Credit: the *project author* obtained both PDFs (T1).
- **2026-10-12 — the comparative source arrives, and the cross-hat test unblocks in
  three quarters.** The project author digitised the whole of **Menghin 2000**, *Der
  Berliner Goldhut und die goldenen Kalendarien der alteuropäischen Bronzezeit*
  (Acta Praehistorica et Archaeologica 32, 31–108) — the study that measured *all
  four* hats, not just Berlin. Until today the case held only Berlin, through the
  2010 book, and the strongest available test (fix the rule on Berlin, apply it
  blind to another hat) was blocked. Its four per-zone tables — Berlin (Abb. 14),
  Schifferstadt (Abb. 17), Avanton (Abb. 20), Ezelsdorf (Abb. 27) — are now
  transcribed from the page images into `data/readings/menghin2000_zones.json` and
  pinned by a new control, **C6**. Credit: **the project author** for the scans; the
  transcription, the verification script and the reading are this round's work.
  Three things follow.
  *First*, the **Ezelsdorf count is now primary**: 499 stamped symbols, with 432
  disc symbols and 1463 rings in zones 3–20 (1694 with Menghin's rebuilt rim). C5's
  secondary figure was right; the phantom digest's "1739 symbols" stays dead.
  *Second*, Fuls's combinatorial null can now be re-run here **for all four hats**,
  instead of trusting Peter-Röcher's one-line report that the rule "ließ sich leider
  nicht übertragen" — the cross-hat test finally becomes ours to run (`todo/T2`).
  *Third*, reading the primary source on the page caught errors that no summary
  would have shown: Menghin 2000 prints **418** discs on p. 81 and **399** on
  pp. 83/91 for the same 1701 rings; his Ezelsdorf symbol totals come out 475/508/465
  from his own table where the text prints 474/505/462; and the Avanton six-lunation
  row divides 177 by 6 while saying the intercalary zone was dropped. The ring sums
  are exact everywhere; the flagged symbol deltas are themselves evidence for the
  critics' point that the method is applied selectively, and they belong on the
  Stage-2 "how sure are we" screen. One correction to *our own* record: the earlier
  trap note claiming Menghin 2000 used a different intercalary set (`{5,7,16,17}`)
  than 2010 is wrong — 2000 uses `{7,16,17}` too, with zone 5 as a *Sonderzone*
  added for solar cycles; only the bookkeeping of 1597 differs. `lessons.md` and
  `sources/menghin_2000_2010.md` are corrected.
- **2026-10-13 — the monograph arrives whole, and the author himself calls the
  transfer partial.** The project author supplied the rest of **Menghin 2010**, *Der
  Berliner Goldhut — Macht, Magie und Mathematik in der Bronzezeit*: the whole book,
  pp. 1–88 + front matter, 85 page images and text, now in
  `assets/menghin/2010/full/` (the older phone-photo selection used by the STL plan
  is left untouched). The chapter the case needed is **"Der Vergleich" (pp. 64–72)**,
  where Menghin applies his Berlin reading to the three other hats. It is decisive,
  and it is the author's own conclusion.
  *First*, the opening sentence of p. 65: the lunisolar / "bound calendar"
  interpretation „**lässt sich partiell** auf seine drei Vergleichsstücke übertragen"
  — it transfers only *partially*. For Schifferstadt he gets "wenige kalendarisch
  annähernd verwertbare Zahlen wie 355, 266 und 272"; for Avanton likewise only a few
  (364, 182, 355, 268, 177). *Second*, and stronger, p. 68 on Ezelsdorf-Buch: „Umso
  erstaunlicher ist es, dass sich etwa aus der Addition identischer Stempel oder
  deren zonenweiser rhythmischer Abfolge … **keine direkten kalendarische Werte
  ermitteln lassen**." That is the stamp-identity rule the Berlin reading actually
  rests on — and Menghin states it fails on Ezelsdorf. He then falls back to
  *contiguous zone-block sums*, i.e. to the post-hoc block selection the case's hit
  definition excludes. Peter-Röcher's one-sentence report ("ließ sich leider nicht
  übertragen") is thereby corroborated from the primary author's pen, and the
  critique no longer rests on a secondary source.
  *Third*, a genuine moving target: the **Ezelsdorf intercalary set changes between
  Menghin's own publications** — `{5,6,19}` in the 2000 article (with Z15 and Z17 as
  *Sonderzonen*), six green rows `{5,6,15,16,17,19}` in the 2010 table (Abb. 69),
  five in the 2010 *text* (Z16 omitted), and 12 under Fuls's "unique symbol type"
  rule. Berlin's `{7,16,17}` + zone 5 stays put; *Ezelsdorf* is where "which zones
  are intercalary" is under-specified. That is the concrete form of the
  free-parameter objection, now documented on the page.
  *Fourth*, the control that passed: Menghin 2010's Berlin table (Abb. 23, p. 30)
  reproduces the 2000 table (Abb. 14, p. 45) zone for zone and ring for ring, and the
  2010 Ezelsdorf table (Abb. 69, p. 68) reproduces the 2000 one — including the
  **Zone 8 `A=40` with `SK=78`** slip, which therefore lives in Menghin's typescript
  and is not a scanning artefact. Credit: **the project author** for the full-book
  scan; the split, the cross-check and the writing-up are this round's work. Finding:
  `findings/FINDING_2026-10-13_menghin-2010-ingested.md`.
- **2026-10-13 — the null is reproduced, and the cross-hat test is run.** With the
  Menghin monographs in hand, the case closed its last trust-without-reproduce
  control. `scripts/fuls_null.py` re-implements Fuls's four combination methods
  (arbitrary subsets; same-stamp groups; contiguous blocks; contiguous blocks minus
  the intercalary zones inside them), his nine periods and tolerances, and his chance
  baseline `w = 2·t_p/p`. `--check` re-finds his published Tables 8.2–8.5 from the
  Menghin 2000 counters: Berlin A/C/D and Schifferstadt/Avanton A–D reproduce
  exactly, and the one Berlin cell that did not is explained — Fuls's Mars count
  includes the single zone-5 sum `19 d` as within ±20 d of *zero* periods, whereas
  formula 8.1 requires a multiple `M ≥ 1`. The method-D rule had to be recovered (a
  contiguous block minus any subset of its intercalary zones, counting *distinct*
  zone sets); with it, Berlin's `G = 699` falls out exactly. On the way, one
  transcription error surfaced: Schifferstadt's zones 3 and 4 are Musterpunze 5, not
  3 (Abb. 17), now fixed and control C6 re-run clean. Credit: the recovery and the
  script are this round's work; the method is Fuls's.
  The payoff is the **cross-hat test** the case has wanted since day one: apply the
  Berlin reading blind to every hat and compare the hit rate with chance. The result
  is a clean reproduction of Fuls's negative. **Only Schifferstadt, method B, for the
  synodic month is clearly above chance** — 5 hits in 31 combinations against 2.1
  expected (16.13 % vs 6.77 %), and there it is the *metrology* (the 3:9 and 9:15
  proportions), not the Berlin rule, that corroborates it. Berlin, Avanton and
  Ezelsdorf sit on the chance line, and on Berlin the tropical-year rate is *below*
  chance. So the strong form of the calendar hypothesis is now not merely
  unproven — it fails Fuls's selectivity test on Berlin, it fails Menghin's own
  transfer test on the other hats (finding of the previous beat), and the single
  positive signal in the corpus belongs to the one hat whose interpretation has an
  independent check. Finding: `findings/FINDING_2026-10-13_fuls-null-reproduced.md`.
- **2026-10-13 — T3: a recipe corrected, and an independent model confirmed to
  include Berlin.** T3 set out to extract Hansen & Rink's Nuncius 8 chapter on
  calendars and eclipses and to test whether its Pleiades/32-33 mechanism touches a
  Berlin zone value. It does not get that far: the recipe's claim that the whole
  volume sits inside `fuls_2008_nuncius8.pdf` turned out to be false — that PDF is a
  Fuls-only chapter extract (19 pages, pp. 113–129; zero occurrences of
  Hansen/Rink/Finsternis/Plejad), and the chapter is actually **ch. 9, p. 131 ff.**,
  not "pp. 401–431". Rather than leave a false "held" line standing, the recipe and
  T3 are corrected, and the failure mode is added to `lessons.md`: verify a held
  source with a page count and a keyword grep, not the recipe's word. What *could* be
  obtained is the authors' open 2013 abstract, and it is informative: their line runs
  „von der Himmelsscheibe von Nebra über den Sonnenwagen von Trundholm **bis zu dem
  Berliner Goldhut**", via lunar eclipses, the Saros cycle and the derived Metonic
  intercalation cycle. So the eclipse/32-33 model is a genuine *independent
  explanation* that explicitly claims the Berlin hat — but its per-zone arithmetic is
  not in hand. Per the project author's decision, T3 is recorded as **abstract
  obtained, chapter outstanding**. Finding:
  `findings/FINDING_2026-10-13_hansen-rink-abstract.md`.
