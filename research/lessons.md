# Lessons — research

Traps found in *this* case's sources. Add one the moment you hit one, then feed
it back into `queries/` and `judges/`.

| Trap | Source | What it looked like | What it actually was |
|---|---|---|---|
| **Author-name drift** | earlier digest `gold_hat.md`; project `AGENTS.md` | "Wolfgang Schlosser (2004, 2012)" | The archaeoastronomer is **Wolfhard Schlosser** (Bochum, 1940–2022). There is no "Wolfgang Schlosser" in this field. His relevant works are on *lunar calendars* and the Nebra disc, not the gold hats. |
| **Invented citation / phantom reference** | earlier digest `gold_hat.md` | "I. Mathieson, *The Golden Hat Calendar* (2010)" | No trace in Crossref, OpenAlex, library catalogues or the open web. Likely hallucinated by the summarising model. |
| **Garbled composite citation** | earlier digest `gold_hat.md` | "Spurk, Gebhard, Schauer, et al.: analyses show relationships …" | No such joint study exists. The real ingredients are Schauer 1986 (the gold-hat monograph) and R. Gebhard (Nebra). "Spurk" attaches to neither in this context. |
| **Copied corroboration** | earlier digest `gold_hat.md` | Ezelsdorf-Buch "≈ 1,739 symbols in 23 bands", the *same* 1739 as Berlin | Ezelsdorf has ≈ **499** symbols. The summary copied Berlin's total onto the other hat to manufacture agreement. This is the "no independent corroboration" trap in miniature. |
| **Secondary-source number drift** | Wikipedia calendar section vs Menghin 2000 vs Menghin 2010 | the 54-month example `1739 − 142 = 1597` and the intercalary set `{5,7,16,17}` | Corrected 2026-10-12 after reading Menghin 2000 itself: the 2000 Schaltzonen are `{7,16,17}` too, and zone 5 is a *Sonderzone* added for solar cycles — the same roles as 2010. Only the bookkeeping of 1597 differs (`1701−(38+66)` vs `1739−(38+38+66)`). The genuinely free parameter is *which zone blocks are added*, not which zones are intercalary. Do not repeat the older, wrong version of this trap. |
| **The source's own summary contradicts its own table** | Menghin 2000, pp. 45 / 81 / 83 / 91 | one disc count and one symbol total per hat, stated three times | The Berlin table sums to 418 discs; p. 81 says 418, pp. 83+91 say 399 (2010, p. 31 confirms 418). Ezelsdorf zones 3–20 sum to 475/508/465 where the text prints 474/505/462. And p. 79 divides 177 by 6 while saying Schaltzone 12 was dropped. **Transcribe the table, verify every identity, print the deltas.** A summary sentence in a primary source is still a claim, not the measurement. |
| **The free parameter moves between the author's own publications** | Menghin 2000 Abb. 27 vs Menghin 2010 Abb. 69 / p. 68 text | the Ezelsdorf-Buch "Schaltzonen" | **Ezelsdorf:** `{5,6,19}` in the 2000 article (Z15, Z17 being *Sonderzonen*); the **2010 table marks six** green rows `{5,6,15,16,17,19}`, while the **2010 text lists five** (omits Z16); Fuls 2008 uses **12**. Berlin's `{7,16,17}` + Z5 is stable, so *Ezelsdorf* is where "which zones are intercalary" is under-specified. A reading that depends on the intercalary set is not pre-registered. |
| **The author's own summary of the transfer is negative, and was there all along** | Menghin 2010, pp. 65, 68 | "lässt sich **partiell** auf seine drei Vergleichsstücke übertragen"; for Ezelsdorf "aus der Addition identischer Stempel … **keine direkten kalendarische Werte**" | Not a later sceptic's gloss — Menghin states it in the comparison chapter. Quote it (Peter-Röcher 2023 is corroboration, not the source). |
| **A count silently redefines its own unit** | Lorenz, *Nachtrag 2. Auflage*, p. 170 (`theories/lorenz_metonic.md`, `todo/T4`) | "19 Linienbänder" and "19 Friese (12+7)" presented as the hat's structure | The measured division is **21 zones** (Menghin); 19 works only as "disc-bearing bands" (Z2–Z21 minus Z5). A number is only comparable once its unit is stated; "19" here is a definition, not the measured structure. Related: the Metonic 235 = 12×12+7×13 is true for *any* 12+7 split, so it is arithmetic, not evidence. |
| **A held PDF is a chapter extract, not the volume the recipe claims** | `sources/hansen_rink_2008.md` vs `research/data/sources/fuls_2008_nuncius8.pdf` | "the whole Nuncius 8 volume is inside" the Fuls PDF; the chapter "pp. 401–431" | The PDF is **Fuls only** (19 pp., pp. 113–129; **0** text occurrences of Hansen/Rink/Finsternis/Plejad). The chapter is **ch. 9, p. 131 ff.** Verify a "held" claim with `fitz` page count + keyword grep, not the recipe's word; pagination in a recipe is a lead, not a fact. |
| **Search-engine false negatives** | DuckDuckGo HTML endpoint | queries returning zero results | The endpoint silently rate-limits/blocks and returns an empty page. Route through `https://r.jina.ai/<search-url>` or use Crossref/OpenAlex; never read an empty result set as "this does not exist". |
| **Anubis JS wall** | Heidelberg JSMV (`journals.ub.uni-heidelberg.de`) | `curl` of a PDF returns a 2-page HTML "Making sure you're not a bot!" | Not the article. A proof-of-work gate. Try the OJS landing page for metadata, or an archive, or ask a human. |
| **ResearchGate CAPTCHA** | `researchgate.net/.../*.pdf` | a small HTML page titled "ResearchGate - Temporarily Unavailable" | Not the PDF. Do not record the download as "held". |
| **Counting-unit collision** | `data/readings/*.json` | Menghin's day-values vs Schmidt-Kaler's ornament counts | Two different units. Never sum them; the JSON `_unit` fields warn but a careless reader will still add 1739 + 651. |

## How these feed the pipeline

- Add `Wolfgang Schlosser`, `Mathieson`, `Spurk` to `queries/` as **trap terms**:
  when they appear, the passage is probably a secondary web summary, not a
  primary source.
- Add to `judges/`: "is the measurement new here, or reused from Menghin?" — the
  phantom citations all came from text that reused other people's numbers.
- Keep the rule in `CASE.md`: no page image, no find.
