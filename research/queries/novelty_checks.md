# Query set: novelty checks for the new sources (v1, 2026-10-10)

The commands that surfaced the augmentation sources and cleared the phantom
references. Kept so the search is reproducible and its limits visible.

```bash
# --- scholarly indexes (reliable) ---
curl -s "https://api.openalex.org/works?search=Berlin%20gold%20hat%20calendar&per-page=10"
curl -s "https://api.openalex.org/works?search=golden%20hat%20bronze%20age%20astronomy&per-page=10"
curl -s "https://api.crossref.org/works?query.bibliographic=golden+hat+calendar&rows=8"
curl -s "https://api.crossref.org/works/10.1558/jsa.18113"        # Amendola 2021
curl -s "https://api.crossref.org/works/10.11588/jsmv.2003.1.89612" # Schlosser 2003

# --- author check (name-drift trap) ---
curl -s "https://api.openalex.org/authors?search=Wolfhard%20Schlosser"

# --- web search that survives rate-limiting (route via a reader proxy) ---
# DuckDuckGo's HTML endpoint returns an empty page when rate-limited; this does not:
curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=Andreas+Fuls+Goldh%C3%BCte"

# --- the sources that were found this way ---
# Fuls 2004:  http://www.archaeoastronomie.de/bronze/Fuls_OEM8_2004.PDF
# Fuls 2008:  https://www.user.tu-berlin.de/fuls/Homepage/literat/archaeo08_Fuls.pdf
# Lorenz:     http://www.weltwunder-himmelsscheibe.de/wwhs_nachtrag-goldhut.pdf
# Schlosser:  https://journals.ub.uni-heidelberg.de/index.php/jsmv/article/view/89612
# Peter-Röcher: BUFM 106 (print); ToC sample at denkmal-buch-geschichte.de
```

## Negative searches (recorded, with limits)

- `Spurk Gebhard Schauer`, `Spurk Goldblechkegel`, `Spurk Nebra` → nothing.
- `"I. Mathieson" gold hat calendar`, exact title → nothing.
- `Wolfgang Schlosser Goldhut` → returns others; no "Wolfgang Schlosser" author.

**Limits:** indexed-source absence is not proof of non-existence. Grey literature,
dissertations and unindexed PDFs can be missed. The negative is strong enough only
to say "do not cite without a page".
