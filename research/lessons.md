# Lessons — research

Traps found in *this* case's sources. Add one the moment you hit one, then feed
it back into `queries/` and `judges/`.

| Trap | Source | What it looked like | What it actually was |
|---|---|---|---|
| **Author-name drift** | earlier digest `gold_hat.md`; project `AGENTS.md` | "Wolfgang Schlosser (2004, 2012)" | The archaeoastronomer is **Wolfhard Schlosser** (Bochum, 1940–2022). There is no "Wolfgang Schlosser" in this field. His relevant works are on *lunar calendars* and the Nebra disc, not the gold hats. |
| **Invented citation / phantom reference** | earlier digest `gold_hat.md` | "I. Mathieson, *The Golden Hat Calendar* (2010)" | No trace in Crossref, OpenAlex, library catalogues or the open web. Likely hallucinated by the summarising model. |
| **Garbled composite citation** | earlier digest `gold_hat.md` | "Spurk, Gebhard, Schauer, et al.: analyses show relationships …" | No such joint study exists. The real ingredients are Schauer 1986 (the gold-hat monograph) and R. Gebhard (Nebra). "Spurk" attaches to neither in this context. |
| **Copied corroboration** | earlier digest `gold_hat.md` | Ezelsdorf-Buch "≈ 1,739 symbols in 23 bands", the *same* 1739 as Berlin | Ezelsdorf has ≈ **499** symbols. The summary copied Berlin's total onto the other hat to manufacture agreement. This is the "no independent corroboration" trap in miniature. |
| **Secondary-source number drift** | Wikipedia calendar section vs Menghin 2000 vs Menghin 2010 | the 54-month example `1739 − 142 = 1597` and the intercalary set `{5,7,16,17}` | The 2010 figures use `{7,16,17}`; zone 5 is *inside* the solar blocks there. The free parameter moves between the author's own publications. |
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
