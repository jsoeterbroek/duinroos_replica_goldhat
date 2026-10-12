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
