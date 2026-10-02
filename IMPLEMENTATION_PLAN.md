# Implementation Plan — Berlin Gold Hat Replica

**Status:** 1st draft, for review. Nothing here is built yet. Sections marked **[DECISION]** need an answer before geometry work starts.
**Scope of this plan:** Stage 1 (static, printable replica). Stage 2 (LED + M5 demo) is only planned as far as it constrains Stage-1 geometry (§10).

---

## 1. Goal & deliverables

A 1:1, stylised replica of the Berlin Gold Hat, printed in segments that stack into the full 745 mm cone.

| # | Deliverable | Where |
|---|---|---|
| D1 | Single source of truth for dimensions: `data/hat_parameters.json` | repo |
| D2 | Symbol catalogue + per-zone layout: `data/symbols.json`, `data/zones.json` | repo |
| D3 | Generator: `scripts/build_goldhat.py` (standalone, `freecadcmd`-runnable) | repo |
| D4 | One STL per band: `stl/berlin_goldhat_z01.stl` … `z21.stl` | repo |
| D5 | Assembly/stacking doc + registration scheme | `docs/` |
| D6 | Verification script: `scripts/verify_geometry.py` + `scripts/verify_calendar.py` | repo |

Explicit non-goals for Stage 1: dents, creases, foil-thickness realism, museum-accurate surface irregularity.

---

## 2. What is already established (verified in this draft)

These are cross-checks I ran against the existing docs. They are the numeric anchors the model must satisfy.

### 2.1 Menghin's day-values are internally consistent ✅
`reference/m5/data/berlin.json` is not a symbol count — it is Menghin's **day-value per zone** (symbols × rings).

```
zones 3..21            = 1739   ← matches gold_hat.md exactly
intercalary 5 + 16 + 17 =  142   ← matches gold_hat.md exactly
1739 − 142              = 1597   ← gold_hat.md's 54-synodic-month result
54 × 29.5305            = 1594.65
```
This gives us a hard arithmetic test for any symbol layout we produce (§12). **`berlin.json` = ground truth for Menghin.** (`berlin_meghin.json` is a byte-identical duplicate — one of the two should go.)

### 2.2 The cone geometry is coherent ✅ (with one correction)
Anchors from `dimensions.txt` (zone 1 circumference 166 mm, zone 5 circumference 275 mm) and the prior attempt's diameter table agree:

| Quantity | Value |
|---|---|
| Diameter growth per band (zone *or* Trennband) | **3.86 mm** (1.93 mm radius) |
| Diameter at top of zone 1 | ~53 mm |
| Diameter at bottom of zone 21 (= base) | **~211 mm** ← matches "base diameter of 20 cm" |
| Cone half-angle from vertical | **~6.1°** |
| Slant length / outer surface area | 745 mm / 0.31 m² |
| Filament at 2.0 mm wall, no symbols | ~620 cm³ ≈ 0.62 kg |

So the object is a long, very shallow cone — 6° from vertical, not a "party hat". A uniform straight cone is the working assumption; §12 verifies it against the photo.

### 2.3 Printability ✅
Tallest part = 745 mm. Largest base = 211 mm. BambuLab bed (256 × 256 × 256) fits **one band at a time** (max band ≈ 43 mm tall, ≤ 150 mm dia). Segmentation into bands is therefore mandatory, not just a requirement.

---

## 3. Discrepancies and open questions

### Q1 — `dimensions.md` does not exist **[DECISION / doc fix]**
`AGENTS.md` references `dimensions.md`; the repo has `dimensions.txt`. Rename one or the other. Low cost, do it first so future readers aren't sent to a missing file.

### Q2 — The height table over-sums the total height by 24 mm ⚠️ **blocking**
Summing every zone + Trennband + both `tussenstuk` entries in `dimensions.txt` (z1…z19) gives **769 mm**, not 745 mm. There is **−24 mm left** for z20, tb20 and z21. Something in the table is wrong.

Candidates to check, in order:
1. `z1 = 61 mm` — is that the crown zone, or crown *plus* something already counted?
2. The two `tussenstuk = 20 mm` spacers — real parts, or duplicate/rough notes?
3. Total height — confirm 745 mm against Menghin (2010) plate text and the museum label, not against Wikipedia.

Nothing can be cut until this resolves, because every band's Z-origin depends on it.

### Q3 — Symbol count: 651, 1783, or "over 3000"? **[DECISION]**
Three numbers circulate for the Berlin hat:
- **651** physical motifs — sum of the Schmidt-Kaler per-zone table (17, 19, 29, 33, 34, …).
- **1783** day-value — sum of Menghin's table (651 motifs × varying ring counts + special values).
- **"over 3,000" / ~3,393** — `gold_hat.md`'s comparison table, sourced from Wikipedia.

These cannot all describe the same surface. The 3,393 figure does not follow from any per-zone table in the repo and is likely a garbled or differently-defined number.

**Why it matters now, not later:** 651 motifs ⇒ ~651 LEDs in Stage 2 (easy, ~5 A even at full white). 3,393 motifs ⇒ ~3,393 LEDs (~61 A peak, per `gold_hat_scenarios.md`) — an entirely different power and wiring design. Resolve by counting from the Abrollung (§6.1).

**Working assumption:** 651 physical motifs, 1783 day-value. Proceed on that, flag loudly if counting disagrees.

### Q4 — Which scholarly reading drives the demo? **[DECISION]**
Menghin (lunisolar) and Schmidt-Kaler (Venus) use *different* band groupings on the same motifs. Stage 1 geometry is unaffected (motifs are motifs), but the LED *zoning* and the displayed arithmetic differ. Recommendation: build the geometry reading-agnostic, make the interpretation a runtime data file (already how `goldhat_layout.json` vs `berlin.json` are split in the prior attempt).

---

## 4. Architecture of the model

```
                    ┌─────────────────────────────┐
   top of hat  z1   │  zone 21 … zone 1, stacked  │
                    │  + 20 Trennband rings       │
                    └─────────────────────────────┘
        one STL per band, printed axis-vertical, stacked
```

**Decomposition** — 41 distinct decorative parts (21 zones + 20 Trennbands) plus 2 spacers.

**Assembly unit [DECISION]:** the requirement says "each band = one STL". Two readings:

| Option | STL count | Pros | Cons |
|---|---|---|---|
| **A (recommended)** | **21** — one zone with its Trennband fused as a lip at the band's lower edge | fewer joints, fewer files, Trennband is a *relief* not a load-bearing ring, better stacking accuracy | Trennband cannot be swapped/adjusted independently |
| B | 41 — zone and Trennband separate | matches `dimensions.txt` 1:1; Trennband colour/finish can differ | 41 joints × tolerance stack; 41 print jobs |

Recommend **A**. Revisit if the Trennbands must be a different material or colour.

---

## 5. Geometry model

### 5.1 Parameters (one JSON file, `data/hat_parameters.json`)
```jsonc
{
  "height_total_mm": 745.0,
  "base_diameter_mm": 211.0,
  "wall_thickness_mm": 2.0,        // NOT 0.6 — foil thickness is unprintable
  "wall_thickness_tb_mm": 3.0,     // Trennbands read as a thicker ridge
  "symbol_relief_mm": 0.8,         // emboss/engrave depth        (see §6)
  "registration_lip_mm": 6.0,      // inner lap ring for stacking
  "registration_clearance_mm": 0.25,
  "rings": [ { "id":"z01", "kind":"zone", "h":61.0, "d_top":53.0,  "d_bottom":56.9 },
             { "id":"tb1", "kind":"trennband", "h":7.0, "d_top":56.9, "d_bottom":60.7 },
             ... ]
}
```
`d_top` / `d_bottom` are *derived* from the growth rate in §2.2, not hand-typed — the generator computes them from `height_total_mm` + `base_diameter_mm` + the height table, then asserts contiguity. That way Q2 is fixed in one place.

### 5.2 Band as a solid
Each band = `outer_frustum − inner_frustum` (an open conical ring), plus:
- a **registration lip**: a 6 mm tall, wall-thickness ring on the inside of the lower edge, sized to slip into the band below (0.25 mm clearance). Axis-vertical printing makes this support-free.
- a **Trennband ridge** at its lower edge (Option A), 1 mm proud, 9 mm tall — this is the relief that separates zones visually.
- **symbol features** (§6) on the outer surface.

### 5.3 Symbol projection — the one non-obvious bit
Do **not** try to bend a flat pattern onto the cone (the prior attempt's unrolled-frustum SVG route, `reference/cad/svg/z04_strip.svg` — an annular sector 795 mm across, which cannot be mapped back onto a cone in FreeCAD without a bend feature).

Instead: for each motif, build a prism in a local frame tangent to the cone at the motif's (θ, z), and boolean it radially. The visible shape on the outer skin is then the correct radial projection — which is exactly what you want for an LED light window anyway. Chord error for a 25 mm motif on a 100 mm radius is 0.8 mm; acceptable for a stylised model, and it shrinks toward the top.

Placement maths: `r(z)` linear; motif angular pitch `Δθ = 360° / n_zone`; local frame rotated by the cone half-angle (6.06°) so the prism is normal to the surface.

---

## 6. Symbol system

### 6.1 Getting the layout — the Abrollung
`assets/berliner_goldhut_abrollung.jpg` (648×800) is the unrolled surface view and is the **primary geometric source**. Method:

1. Determine whether it is a photographic true development (width ∝ circumference, 2πr) or an orthographic silhouette (width ∝ 2r). Both are linear in r; the difference is a constant factor.
2. Calibrate with two anchors: total height = 745 mm, base diameter ≈ 211 mm.
3. Extract `r(z)` by measuring image width at each of the ~41 band boundaries → replaces hand-typed diameters and simultaneously answers Q2.
4. Cross-check the profile against `assets/Berlín_Goldhut_01.JPG` (800×1873, front-on) to confirm the straight-cone assumption. A straight cone is expected; if it bows, fit a piecewise cone.

Then transcribe, band by band, the motif type + count into `data/zones.json` (21 rows — a manual job with a magnifier, not CV). CV/contour tracing is a fallback, not a plan.

### 6.2 Motif primitives — parameterised, not traced
The prior attempt has SVG/bitmap traces (`symbol12_bitmap_traced.svg` etc.). Do **not** recycle them: they are hand-fitted circles, and the requirement is explicitly stylised. Define a small set of primitives:

| Primitive | Params | Covers |
|---|---|---|
| `ring` | r, count | concentric-circle motifs — symbol 12/13/14 (3/4/5 rings) |
| `disc` | r | plain punched dot |
| `ring_dot` | r_outer, count, r_dot | disc inside N concentric rings (the classic "sun" of symbols 12–14) |
| `circle_row` | r_dot, n | rows of small dots |
| `zigzag` | teeth, amplitude | Trennband motifs |
| `oval` / `crescent` | a, b, rotation | sparse special motifs |

Each is a handful of `Part.makeCircle` / `makePolygon` calls. No SVG import path, no bitmap tracing, no 17 hand-made files.

### 6.3 Physical form of a motif — **[DECISION]**
This is the single decision that ties Stage 1 to Stage 2.

| Option | Stage 1 look | Stage 2 | Verdict |
|---|---|---|---|
| **C (recommended)** — motif is a **through-window** in the band wall | motif reads as a crisp silhouette; held to a light it already glows | literally satisfies "LED behind the outer surface behind the symbols"; one LED per window | smallest geometry, one print per band |
| B — motif embossed/engraved on a solid wall | closest to repoussé relief | needs re-cutting every band to add windows | rejects the second stage for the first |
| A — opaque outer skin + inner translucent diffuser sleeve | best looking | needs per-symbol baffles or light bleeds across the whole zone | twice the printing, alignment risk, deferred |

Recommend **C**. Add an optional inner diffuser sleeve later (Stage 2) without touching the bands — that is the "A" benefit at no Stage-1 cost. Note the structural consequence: at 651 motifs on 0.31 m², windows occupy a small fraction of the shell; keep a minimum 3 mm ligature between neighbouring windows, and add interior ribs if any zone's windows exceed ~40 % of its surface.

---

## 7. Data files

| File | Contents | Status |
|---|---|---|
| `data/hat_parameters.json` | heights, diameters, wall/relief/registration params | to create |
| `data/symbols.json` | motif catalogue: id, primitive, params, ring count | to create |
| `data/zones.json` | per zone: ordered motif placement (type, count, counted/ornament, start angle), Trennband motif | to create — **the real research work** |
| `data/readings/menghin.json` | day-value per zone (verified, §2.1) | copy from `reference/m5/data/berlin.json` |
| `data/readings/schmidt_kaler.json` | motif count per zone | copy from `reference/m5/data/goldhat_layout.json` |

Note the schema in `data/zones.json` must carry **both** the motif count and the ring multiplier per motif, because Menghin's day-value = Σ(count × rings). The prior attempt's schema (`{zone, count, multiplier, special_value}`) is a lossy summary — it collapses a whole zone to one multiplier, which cannot represent zone 12 (20 × symbol-14 with 5 rings **plus** ornament motifs between them). One level deeper is needed.

---

## 8. Toolchain & pipeline

```
data/*.json  ──►  scripts/build_goldhat.py  ──►  stl/*.stl
                        │
                        └─ freecadcmd (headless, via FreeCAD MCP `execute_code_headless`)
```

- **Source of truth is the Python + JSON in `scripts/` and `data/`.** FreeCAD is the geometry kernel, not the editor. The whole model must be reproducible from a clean checkout with one command: `freecadcmd scripts/build_goldhat.py`.
- **Heavy generation runs headless** (`execute_code_headless` → separate `freecadcmd` process). Boolean cuts against 30–80 motif prisms per band are exactly the kind of OCCT work that can wedge the GUI thread; a crash there should not take the running FreeCAD session with it.
- **MCP `execute_code` + screenshots used for interactive QA only** — open one band, look at it, adjust a parameter. Not for the batch run.
- No new dependencies. `Part` (OCCT) via FreeCAD's bundled Python is sufficient; do not add build123d/cadquery.

---

## 9. Print strategy

| Parameter | Value | Rationale |
|---|---|---|
| Orientation | axis vertical, band lying flat | 6° wall ⇒ zero overhang, zero supports, registration lip prints inside-free |
| Layer height | 0.16 mm | 0.62 kg of filament; don't throw resolution away for nothing |
| Walls | 3 loops ≈ 1.6 mm + top/bottom | 2.0 mm nominal wall; symbol windows cut through |
| Material (Stage 1) | matte PLA, bronze/gold silk | reads as gold without paint; **not** silk for fit-test coupons (silk hides dimensional error) |
| Per-band print | 1 at a time | largest band ≤ 150 mm dia, 43 mm tall |
| Tolerance | 0.25 mm radial clearance on the lap joint | verify with a 3-band fit test before committing to 21 prints |
| Total | ~21 prints, ~0.7 kg incl. windows | |

**Fit test first:** print z13 + z14 + z15 (a plain repeating stretch) 1:1 and check that the stack is straight and the lap joint doesn't wobble. Only then print the rest. The top zone (z1) and the base (z21) print last — they are the least forgiving parts and benefit from a calibrated machine.

---

## 10. Stage-2 constraints this plan must respect

Nothing below is implemented now; these are the interfaces Stage 1 must leave open.

1. **Window per motif** (§6.3, Option C) — each motif is a light channel.
2. **Interior cavity**: the lap joint leaves a natural annular gap; keep ≥ 8 mm of clear radial depth behind a band so an LED PCB can be slipped in, and leave a **20 × 6 mm cable notch** in each lap lip at a common clock angle (recommend θ = 0°, i.e. the hat's "front"), so a single wiring spine runs up the inside.
3. **Modular Z-addressability**: zones are already separate parts, so per-zone LED segments need no extra geometry.
4. **LED budget** is contingent on Q3 (§3): 651 (assumed) vs 3,393 motifs. Do not design the power stage before counting.
5. **M5 Core S3 + display** sits outside the hat; plan a base plinth/cradle (a separate later model) that hides the electronics and holds the cone upright.

---

## 11. Phases & milestones

| Phase | Work | Exit criterion |
|---|---|---|
| **P0 — resolve blockers** | Q1 doc rename; Q2 height reconciliation vs Menghin; confirm 745 mm | height table sums to the declared total; `dimensions.md` exists |
| **P1 — profile extraction** | Abrollung calibration → `r(z)` for all 41 boundaries → `hat_parameters.json`; validate against photo silhouette | `r(z)` within ±1 mm of the photo at 10 sample heights |
| **P2 — motif catalogue** | Count and classify motifs from the Abrollung → `symbols.json` + `zones.json`; implement primitives | `verify_calendar.py` reproduces every Menghin zone value (1783 total, 1739, 142, 1597) |
| **P3 — geometry kernel** | `build_goldhat.py`; one band end-to-end (start with z13) | an STL that visually matches the Abrollung strip for that zone |
| **P4 — full generation** | all 21 bands → `stl/` | 21 STLs, watertight, `verify_geometry.py` passes |
| **P5 — print & fit** | 3-band fit test, then full print, assembly | stacked cone is straight, 745 mm ± 3 mm, joints tight |
| **P6 — (later) Stage 2** | LEDs, M5 firmware | out of scope here |

P0 and P1 are cheap and de-risk everything. P2 is the long pole and the only real research effort.

---

## 12. Verification plan

Runnable, no frameworks, assert-based.

**`scripts/verify_calendar.py`** — the layout must reproduce the source arithmetic:
```
sum(day_value[3..21])                       == 1739
day_value[5] + day_value[16] + day_value[17] ==  142
…                                            == 1597  (54 synodic months)
sum(day_value[1..21])                        == 1783
sum(motif_count[1..21])                      ==  651
```
If Q3 is resolved differently, these last two change — which is precisely why they are assertions and not comments.

**`scripts/verify_geometry.py`** — on the exported STLs:
```
bounding box height of the full stack == 745 ± 3 mm
outer diameter at each boundary       == r(z) target ± 0.5 mm
each solid                            watertight, volume > 0, no self-intersection
Σ band heights                        == 745 mm   (catches the Q2 class of error)
```

**`scripts/verify_calendar.py` on the STL (Stage 2 prep only)** — count through-windows per band and assert it equals the motif count in `zones.json`. Cheap sanity check that geometry and data did not drift apart.

**Visual** — screenshot each band overlaid on its Abrollung strip crop; a human eyeballs 21 pairs once.

---

## 13. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Q2 height discrepancy is a real measurement error in Menghin | every Z coordinate shifts | resolve in P0 before any cutting |
| Q3 motif count is wrong by 5× | Stage 1 unaffected; Stage 2 power/wiring design invalidated | count in P2; keep the LED design out of Stage 1 |
| Manual motif transcription errors | a zone's day-value assertion fails | the P2 assertion catches it immediately — build P2 data with the test running |
| 21-part tolerance stack drifts over 745 mm | hat leans or joints open | lap joint + 3-band fit test at P5; add a removable internal mandrel as a fallback |
| FreeCAD/OCCT boolean failures on dense motif clusters | band won't build | headless generation isolates crashes; fall back to `fuse`-then-single-`cut` (fuse all motif prisms first — a single boolean against the heavy shell) |
| Abrollung is distorted (a photo, not a true development) | wrong profile | calibrate on two known anchors and reject the source if residuals exceed tolerance |

---

## 14. Immediate next actions

1. Fix the `dimensions.md` reference (Q1) — 1 minute.
2. Open `assets/berliner_goldhut_abrollung.jpg` and `assets/Berlín_Goldhut_01.JPG` side by side with the height table; resolve Q2 (does z1 really include 61 mm? do the spacers exist?).
3. Decide Q3 (count from the Abrollung) and Q4 (which reading the demo shows).
4. Confirm Option **A** for the STL decomposition (§4) and Option **C** for the motif form (§6.3).
5. Then start P1.

---

## Appendix A — inventory of what exists

| Path | What it is | Use |
|---|---|---|
| `gold_hat.md` | Menghin + Schmidt-Kaler + Wikipedia digest | **primary theory source** |
| `dimensions.txt` | prior attempt's height table; circumference anchors | **primary dimension source** (with Q2 caveat) |
| `sources.md` | 3 physical books | bibliographic verification for P0 |
| `assets/berliner_goldhut_abrollung.jpg` | unrolled surface view | **primary motif + profile source** |
| `assets/Berlín_Goldhut_01.JPG` (800×1873) | front-on photo | silhouette profile validation |
| `assets/Berlín_Goldhut_04.JPG` | detail photo | motif cross-check |
| `assets/Berlin_Gold_hat_calendar.jpg` | Menghin's calendar diagram | zone grouping / intercalary confirmation |
| `assets/tb_detail.jpg` (88×83) | Trennband detail | Trennband motif design |
| `assets/berlin_golden_hat-paper-replika.com.pdf` | paper-replica build | practical assembly reference |
| `reference/cad/*` | abandoned attempt: FCStd, 3MF, 38 STLs, unrolled-frustum SVGs | **reference only — do not recycle** (`AGENTS.md`) |
| `reference/m5/*` | abandoned attempt: ESP32 firmware + scenario doc | **Stage-2 reference only** |
| `scripts/analyze_cone.py` | OpenCV cone-measurement script (from prior attempt) | candidate tool for P1 profile extraction |

## Appendix B — numbers used in this plan, and where they come from

| Number | Value | Source / derivation |
|---|---|---|
| Total height | 745 mm | `dimensions.txt`; to be confirmed against Menghin (Q2) |
| Base diameter | ~211 mm | derived from circumference anchors + 41 band steps (§2.2); agrees with "20 cm" |
| Zone/Trennband diameter step | 3.86 mm | (275 − 166)/π ÷ 9 steps |
| Cone half-angle | 6.06° from vertical | atan(79.2 / 745) |
| Outer surface area | 0.31 m² | π(r_top+r_bot)·slant |
| Filament @ 2.0 mm wall | ~620 cm³ | area × thickness |
| Days, zones 3–21 | 1739 | Menghin, per `berlin.json` |
| Days, zones 5+16+17 | 142 | Menghin |
| Days, 54 synodic months | 1597 (≈1594.65) | Menghin |
| Physical motifs | 651 **(unconfirmed)** | Schmidt-Kaler table, §3 Q3 |
| Day-value total | 1783 | Menghin table |
| Printed parts | 21 (Option A) or 41 (Option B) | §4 |
