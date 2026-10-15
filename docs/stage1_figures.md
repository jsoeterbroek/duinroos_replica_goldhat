# Stage 1 — scenario figures

Stage 1 turns the Berlin Gold Hat's `data/*.json` into **deterministic, stylised
figures** that show each calendar hypothesis band-by-band, in the visual idiom of
Menghin (2010), *Der Berliner Goldhut*, pp. 60–63 (Abb. 61.1–64.4). They are the
project's article/documentation/demo assets, and they are generated — not drawn —
so they can never drift from the data that will also drive the 3D model (Stage 2)
and the LED demo (Stage 3).

> **The figures are not proof.** The ornament counts are solid; the *calendar
> reading* is a hypothesis. The `caution` figure (below) states this on the
> figures themselves.

## Regenerating

Everything is reproducible with one command (plain `python3`, no FreeCAD):

```bash
python3 scripts/render_scenarios.py --all          # 16 panels + 16 developments + 4 sheets + comparison + caution
python3 scripts/render_scenarios.py --all --pack   # also figures/_pack.pdf (18 pages)
python3 scripts/render_scenarios.py --state 61.1   # a single panel
python3 scripts/render_scenarios.py --check-deterministic   # asserts PNG+SVG reproduce byte-for-byte
```

Verification (stdlib only, no matplotlib):

```bash
python3 scripts/verify_figures.py                  # data-derived + complete figure set
python3 scripts/figure_geometry.py --selfcheck     # the figure kernel's own checks
```

The renderer needs only **matplotlib** (Agg backend, no display). Nothing in
Stage 2 (`freecadcmd`) imports it.

## What is drawn, and from what

| Figure | File(s) | Shows | Data |
|---|---|---|---|
| **F1 panel** | `figures/menghin/<id>.png` | the sectioned hat silhouette, 21 zone bands coloured for one state, zone numbers, `SZ` marks, sun/crescent glyphs, the arithmetic caption | `data/hat_parameters.json`, `data/zones.json`, `data/scenarios.json` |
| **F2 development** | `figures/menghin/development_<id>.png` | the unrolled ornament (Abrollung): each zone at its own circumference, the real motifs drawn, coloured for the state | `data/symbols.json` (via `scripts/motifs.py`), same three files |
| **F3 sheet** | `figures/menghin/sheet_6x.png` | four F1 panels in the source's page layout | F1 |
| **F4 legend** | the key on every figure | red = solar block · blue = lunar block · green = intercalary zone (`SZ`) · grey = not part of this block | — |
| **F5 comparison** | `figures/compare/hypotheses.png` | the five readings side by side: unit, total, target periods, confidence, and a hat coloured by what each reads | `data/hypotheses.json` |
| **F6 caution** | `figures/caution/null_model.png` | Fuls (2008) null model: only Schifferstadt beats the chance line | `data/readings/fuls_null.json` |
| **pack** | `figures/_pack.pdf` | every F1 panel, then F5 and F6, as one 18-page PDF | all of the above |

The 16 `id`s are Menghin's blocks: `61.1 … 61.4`, `62.1 … 62.4`, `63.1 … 63.4`,
`64.1 … 64.4` — the four source pages, four panels each.

## Legend

| colour | meaning | Stage-3 LED |
|---|---|---|
| **red** | solar block | warm red |
| **blue** | lunar block | blue |
| **green** | intercalary ("Schalt") zone, marked `SZ` | the zones to add/remove from a block |
| grey | not part of this block | dark |

The intercalary zones are the zones whose disc stamp occurs exactly once in the
canon: **{7, 16, 17}** (tools Nr. 11, 13, 9). Zone 5 is the 38 special signs and is
never counted as a disc.

## How it is built (three tiers, mirroring Stage 2)

```
data/*.json  ─►  scripts/figure_geometry.py  ─►  scripts/render_scenarios.py  ─►  figures/*
                  (pure maths, stdlib)            (matplotlib, Agg)
```

- **`scripts/figure_geometry.py`** — the figure kernel. Silhouette, zone bands, the
  Krempe radial split, the colour classes, and the **re-derived captions**. It holds
  no day value: `rederive(state, side, day)` re-sums every stated solar/lunar value
  from `data/zones.json`, and `--selfcheck` asserts all 30 of them.
- **`scripts/motifs.py`** — the 2D punch primitives and `placed_zone_motifs()`, the
  single placement routine shared by the SVG development and F2.
- **`scripts/render_scenarios.py`** — the only file that touches a plotting library.

## Honesty rules (enforced)

- **No hard-coded numbers.** `verify_figures.py` fails if the renderer contains a
  day value, and checks every caption value is the re-derived one.
- **No invented state data.** Only Menghin has a full state model
  (`data/scenarios.json`). The other readings in `data/hypotheses.json` declare
  their unit and targets but are rendered with a plain hat and an explicit
  "no zone grouping in this reading" where they define none.
- **The null result is on the figures.** F6 carries Fuls's cross-hat result:
  Berlin's reading sits on the chance line and does not transfer to the other hats.
- **Deterministic.** `--check-deterministic` renders a panel twice and asserts the
  PNG and SVG are byte-identical. (PDF stamps a creation date, so only its pixels
  reproduce; that is documented in `_savefig`.)

## Notes

- `figures/` is **tracked** in git (operator decision) — the PNGs are the
  deliverable, like the STL parts.
- The figures share the profile `r(z)` with Stage 2, so a profile change (e.g. the
  rounded apex, `IMPLEMENTATION_PLAN.md` §11.6) moves both together: rerun
  `render_scenarios.py --all` after any `data/` edit.
- Sources and the full derivation of every number: `IMPLEMENTATION_PLAN.md` §1.5
  and §2; the competing readings: `research/theories/`.
