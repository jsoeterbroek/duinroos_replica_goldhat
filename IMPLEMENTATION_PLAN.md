# Implementation Plan — Berlin Gold Hat Replica

**Status:** 1st draft, for review. Nothing here is built yet. Sections marked **[DECISION]** need an answer before geometry work starts.
**Scope of this plan:** Stage 1 (static, printable replica). Stage 2 (LED + M5 demo) is only planned as far as it constrains Stage-1 geometry (§10).

---

## 1. Goal & deliverables

A 1:1, stylised replica of the Berlin Gold Hat, printed in segments that stack into the full 745 mm object (a waisted **Schaft**, a flared **Kalotte**, and a flat **Krempe** plate at the bottom).

| # | Deliverable | Where |
|---|---|---|
| D1 | Single source of truth for dimensions: `data/hat_parameters.json` | repo |
| D2 | Symbol catalogue + per-zone layout: `data/symbols.json`, `data/zones.json` | repo |
| D3 | Generator: `scripts/build_goldhat.py` (standalone, `freecadcmd`-runnable) | repo |
| D4 | One STL per band: `stl/berlin_goldhat_z01.stl` … `z19.stl`, plus `krempe_a/b/c.stl` for the ⌀301 mm brim plate, which exceeds the print bed (§2.3). **22 files.** | repo |
| D5 | Assembly/stacking doc + registration scheme, incl. the Krempe sector joints | `docs/` |
| D6 | Verification script: `scripts/verify_geometry.py` + `scripts/verify_calendar.py` | repo |

Explicit non-goals for Stage 1: dents, creases, foil-thickness realism, museum-accurate surface irregularity.

---

## 2. What is already established (verified in this draft)

These are cross-checks I ran against the existing docs. They are the numeric anchors the model must satisfy.

### 2.1 Menghin's day-values — **VERIFIED against the primary source** ✅✅
`reference/m5/data/berlin.json` is not a symbol count — it is Menghin's **day-value per zone** (symbols × rings).

Menghin's own text (2010, Ornamentanalyse, `assets/menghin/`) supplies **two independent arithmetic identities** that `berlin.json` satisfies exactly:

| Menghin's sentence (OCR, `assets/menghin/ocr/`) | Arithmetic |
|---|---|
| „…sowie die Zone 5 mit den 38 ‚Sonderzeichen' außer Acht, so sind die **418 Buckelscheiben** (Nr. 8–15) über **18 horizontale Ornamentzonen** verteilt und weisen in der Addition der konzentrischen Ringe gesamt **1701 Kreisringe** auf." | `1783 − zone1(0) − zone2(44) − zone5(38) = **1701**` ✅ |
| same sentence | 21 zones − {1, 2, 5} = **18** zones ✅; Σ bosses over those 18 zones = **420** vs Menghin's 418 (≤1 OCR digit off) ✅ |

So the decode rule is **`day_value(zone) = Σ (count × rings)`**, with zone 1 (8-rayed star) = 0 and zone 5 = 38 *individual* symbols (19 crescents + 19 eye-symbols). Every zone quoted in the text matches:

| Zone | Menghin's words | Check |
|---|---|---|
| 1 | Höhe 6,1 cm, Basisumfang 16,6 cm, achtstrahliger Stern | no countable ring motif → 0 |
| 2 | 0,85 cm; „22 Doppelkreispunzen" | 22 × 2 = **44** ✅ |
| 3 | 1,4 cm; „14 umlaufende Buckelscheiben mit drei konzentrischen Kreisen Nr. 8" | 14 × 3 = **42** ✅ |
| 4 | 2,2 cm; „15 kleine Buckel mit fünf konzentrischen Kreisen Nr. 10" | 15 × 5 = **75** ✅ |
| 5 | 2,45 cm; „19 liegende Mondsicheln … dieselbe Zahl von mandelförmigen Augensymbolen"; Umfang an der Unterkante **27,5 cm** | 19 + 19 = **38** ✅; circumference anchor ✅ |
| 15 | „15 Buckel mit sechs konzentrischen Kreisen Nr. 15" | 15 × 6 = **90** ✅ |
| 16 | „1,9 cm breite Zierfläche … 19 flache Buckelscheiben mit zwei Ringen Nr. 13" | 19 × 2 = **38** ✅ |
| 17 | „1,5 cm breit … 33 kleine Buckel mit zwei Kreisen Nr. 9" | 33 × 2 = **66** ✅ |
| 18 | „Zone 18 jeweils 21 … Buckelscheiben mit sechs Kreisen Nr. 15" | 21 × 6 = **126** ✅ |
| 19 | „Zone 19 je[weils 23] … sechs Kreisen Nr. 15" | 23 × 6 = **138** ✅ |
| 20 | „Zone 20 mit 54 von drei Kreisen gefassten kleinen Buckelscheiben Nr. 8 … identisch mit Zone 3" | 54 × 3 = **162** ✅ |
| 21 | „Zone 21 mit 47 Buckeln mit fünf Kreisen Nr. 14" | 47 × 5 = **235** ✅ |
| 10/12/14 | „aus der gleichen Musterpunze wie … in den Zonen 10, 12 und 14" (= 5-ring Nr. 14) | 19×5=95, 20×5=100, 21×5=**105** ✅ |

**Menghin's zone widths match `dimensions.txt` too:** 0,85 / 1,4 / 2,2 / **2,45** / 3,4 / 1,9 / 1,5 cm ↔ z2=8.5, z3=14, z4=22, z5=24.5, z9=34, z16=19, z17=15 mm — **seven independent hits, including the odd 24.5 mm.** `dimensions.txt`'s **zone heights are Menghin's numbers**; its `tb*` rows are the Kerbwülste/Trennbänder, which Menghin's zone widths do *not* include.

**`berlin.json` is confirmed ground truth for Menghin.**

```
zones 3..21            = 1739   ← matches gold_hat.md exactly
intercalary 5 + 16 + 17 =  142   ← matches gold_hat.md exactly
1739 − 142              = 1597   ← gold_hat.md's 54-synodic-month result
54 × 29.5305            = 1594.65
```
This gives us a hard arithmetic test for any symbol layout we produce (§12).
Also: **24 different punch tools**, of which Nr. 8–15 are the disc bosses; the tool legend on the same page gives punch diameters (Nr. 8 = ⌀12 mm/3 rings, Nr. 9 = ⌀15/2, Nr. 10 = ⌀13/5, Nr. 13 = ⌀15/2, Nr. 14 = ⌀15/5, Nr. 15 = ⌀21/6) — these set the *scale* the motif primitives must have at each cone diameter (§6.2).
(`berlin_meghin.json` is a byte-identical duplicate — one of the two should go.)

### 2.2 The sectioned profile — **derived from Menghin** ✅ *(Q5 resolved by this section)*

Menghin describes the Berlin hat as **four** sections, and — this is the part the earlier draft of this plan did not have — he gives the diameter of **every** transition between them. All figures below were re-read from the page images with the crop recipe in Appendix C, because plain `--psm 1` drops exactly these numbers:

| Transition | Menghin, verbatim | ⌀ | z |
|---|---|---|---|
| Tip (Spitze) base = zone 1 | „eine Höhe von **6,1 cm** und einen Basisumfang von **16,6 cm**" | 52.8 mm | 61 mm |
| Zone 5 lower edge | „Der Kegelumfang beträgt an der Unterkante dieser Zone **27,5 cm**" | 87.5 mm | 160 mm |
| Kerbwulst below zone 12 | „Der am Kerbwulst darunter gemessene Umfang des Schaftes beträgt **37,1 cm**" | 118.1 mm | ≈445 mm |
| **Schaft maximum** | „der annähernd konische **Schaft mit maximal 125 mm Durchmesser**" | **125 mm** | ≈510 mm |
| **Schaftfuß** | „Der untere Teil des Schaftes, der am Fuß einen Durchmesser von **10,8 cm** hat" | **108 mm** | ≈611 mm |
| Schaft→Kalotte cuff | „durch einen **18 mm hohen** vertikal gefältelten Übergang abgesetzt" | — | +18 mm |
| **Kalottenfuß** = Krempenansatz | „Im Falz zwischen Kalotte und Krempe befindet sich ein Bronzeband von ca. **10 mm Höhe und 203 mm × 175 mm Durchmesser**" | **189 mm** (oval) | ≈729 mm |
| **Krempenrand** | „die leicht verformte **horizontale Krempe mit einem Außenmaß von 307 mm × 295 mm**" | **301 mm** (oval) | 745 mm |

Menghin's own summary of the three body sections is „Schaft, Kalotte und [Krempe sind] durch auffällige Trennbänder in drei Abschnitte … gegliedert", and the sections are of very different shape:

| Section | Content | Shape | Half-angle from vertical |
|---|---|---|---|
| **Schaft** | zones 1–16 | long, gently *concave* (waisted) frustum; ⌀ 53 → 125 → 108 | 4–5°, bulging, then **negative** at the foot |
| **Kalotte** | zones 17–19, „100 mm hohe Kalotte" | strongly flared helmet/dome, ⌀ 108 → 189 | **≈20°** |
| **Krempe** | zones 20–21, „52–55 mm schmale **horizontale** Krempe" | near-flat annular brim, ⌀ 189 → 301, seen from above concave | ≈16° (nearly horizontal) |

**Four consequences, each of which changes the plan:**

1. **The object is not a straight cone.** Four circumference anchors are now available and they are *strongly* non-linear: the local diameter growth is 0.351 mm/mm between z=61 and z=160, 0.107 between z=160 and z=445, ≈0.115 up to the max at ≈510, and then **−0.167** (the shaft narrows) down to the Schaftfuß. A straight-line fit through any two anchors mis-predicts everything below the second one. The profile is therefore stored as a **piecewise list of `(z, r)` control points** (§5.1) — never a slope constant. This is now mandatory, not merely prudent.
2. **The widest point is the Krempenrand, ⌀ 301 mm**, and it is a *near-flat annulus* at the very bottom of the object. `dimensions.txt`'s „20 cm **at its widest point**" is 100 mm too small and stays unreliable; but it is at least measuring the right *feature* (the brim is the widest point, not the base of the cone).
3. **The Schaftfuß (⌀108) is narrower than the Schaft maximum (⌀125).** The shaft really is waisted. Part of the 108 mm vs 125 mm gap is certainly Menghin measuring an „annähernd oval" cross-section along different axes (Abb. 18: „dass die Öffnung der Kalotte nicht rund, sondern annähernd oval war"); part is the concave profile. Modelled as a monotone waist of ≈8 mm radius.
4. **Zones 20 and 21 have essentially no stacked height** — they are *concentric rings on a horizontal plate*, not stacked bands. This is what resolves Q2 (below), and it means the Stage-1 deliverable is **19 stackable bands + 1 flat Krempe plate**, not 21 stacked bands.

**Resulting profile** (control points for `data/hat_parameters.json`):

| z (mm) | ⌀ (mm) | radius (mm) | note |
|---|---|---|---|
| 0 | 0 | 0.0 | apex (nominal) |
| 61 | 52.8 | 26.4 | Menghin A |
| 160 | 87.5 | 43.8 | Menghin B |
| 445 | 118.1 | 59.1 | Menghin C |
| 510 | 125.0 | 62.5 | Schaft max |
| 611 | 108.0 | 54.0 | Schaftfuß |
| 629 | 112.0 | 56.0 | top of the cuff = bottom of the Kalotte |
| 729 | 189.0 | 94.5 | Kalottenfuß / bronze band — the Krempe starts here |
| 745 | 301.0 | 150.5 | Krempenrand |

**Height budget — it closes on `745.000` exactly, with no spacers:**

| Section | Source | mm | cumulative z |
|---|---|---|---|
| Spitze + Schaft | `dimensions.txt` z1…z16 + tb1…tb16 | **611** | 611 |
| crimped cuff | Menghin: „**18 mm hoher** vertikal gefältelter Übergang" | **18** | 629 |
| Kalotte | Menghin: „die **100 mm hohe Kalotte**" | **100** | 729 |
| Krempe | residual: 52–55 mm *radial*, risen 16 mm ≈ 16° from horizontal | **16** | **745** |

**Three independent readings agree, which is why this is trustworthy now:**

| Reading | Sum | vs 745 |
|---|---|---|
| Menghin sections (above) | 611 + 18 + 100 + 16 | **745, exact** |
| `dimensions.txt` Kalotte block: z17+z18+z19 (=91) + tb17+tb18 (=18) = 109 | 611 + 18 + 109 = 738 | −7 |
| same, incl. `tb19` = 118 | 611 + 18 + 118 = 747 | +2 |

The table's Kalotten block and Menghin's 100 mm differ by one 9 mm Trennband, and both land within 7 mm of the truth. **The 24 mm "overshoot" that made Q2 look like a table error was the Krempe's radial width being read as a height.** The two `tussenstuk` rows are deleted as unattested. **The measured silhouette (P1) is still required** to fix the intermediate shape of the Schaft between the four anchors, but it no longer has to decide the *topology*.

**Cross-checks that this shape is real, not an OCR artefact:**

- **Circumferences vs. motif counts.** Menghin states the motifs never overlap („es zu keinen Überschneidungen der Scheiben- und Kreismotive"), so every zone needs `circumference ≥ count × tool ⌀`. The flared sections are the *only* place where the tight zones (18/19 on the Kalotte with ⌀21 punches; 20/21 on the Krempe with ⌀12/⌀15 punches, 54 and 47 of them) can physically fit. Details in the table below.
- **Two independent photos** were measured programmatically (`scripts/measure_silhouette.py`, PIL+numpy). Both show a **hard flare in the last ~10 % of the height** — the widest point is at the very bottom — matching „horizontale Krempe mit Außenmaß 307 × 295 mm". The automated segmentation is not yet good enough to quote a profile in mm (interior shadow breaks the naive threshold), so the *numbers* here come from Menghin, and the photos only corroborate the flare. See §14.
- **Mass/foil cross-check.** Menghin: „durchschnittliche Wandstärke 0.06 mm", weight „nur **490 g**". A 0.06 mm shell of 0.284 m² of gold at 19.3 g/cm³ is ≈ 328 g — same order, the rest being the bronze rings and the thicker reinforced edges. So the sectioned profile's surface area (0.284 m²) is consistent with the stated weight; the earlier straight-cone model's 0.35 m² was not.

### 2.3 Printability — **only the Krempe needs splitting**
Tallest band ≈ 38 mm, so height is never a problem. Bed is 256 × 256 mm (a circle does not fit a square bed diagonally: the largest inscribable circle is ⌀256). With the profile from §2.2:

| Section | max ⌀ | fits 256 bed? |
|---|---|---|
| Schaft (zones 1–16) | 125 mm | ✅ with room to spare |
| Kalotte (zones 17–19, after the cuff) | 189 mm | ✅ |
| **Krempe (zones 20–21)** | **301 mm** | ❌ **must be split** |

So the earlier draft's "split the bottom 2–4 stacked bands" is wrong and over-cautious: **every stacked band fits as-is.** Only the flat Krempe plate is too big.

Options for the Krempe, cheapest first:

1. **Split the plate into radial sectors.** A 180° half-annulus has a bounding box of 301 × 150 mm — *still* 301 mm in x, so two halves do **not** fit. **Sectors of ≤ 120° do:** a 120° sector of a ⌀301 annulus spans ≈ **226 × 151 mm**, and a 90° sector ≈ 151 × 151 mm. So **3 sectors (recommended)** or 4. Print each sector **flat, in its own plane**, so the through-windows are vertical drillings (ideal for Stage 2) and the overhang is the plate's own ~16° rise — no support needed. Join with a tongue-and-groove seam and glue. **Take 3 sectors:** bbox ≈ 226 × 151 mm leaves a comfortable 30 mm margin, and 54 motifs divides cleanly into 18 per sector for zone 20 (zone 21's 47 becomes 16/16/15).
2. Print the Krempe as an equivalent *cone* section standing on edge with the rest of the hat — worse: it becomes a large unsupported horizontal annulus. Discard.
3. Scale to 0.85 — violates 1:1. Discard.

Result: **22 STL files** = zones 1–19 (19 files) + `krempe_a/b/c` (3 files). The band schema gains an optional `split` field but no stacked band uses it, so the z13/z14/z15 test print is unaffected.

---

## 3. Discrepancies and open questions

### Q1 — `dimensions.md` does not exist **[DECISION / doc fix]**
`AGENTS.md` references `dimensions.md`; the repo has `dimensions.txt`. Rename one or the other. Low cost, do it first so future readers aren't sent to a missing file.

### Q2 — The height table over-sums the total height by 24 mm — **RESOLVED** ✅
Summing every zone + Trennband + both `tussenstuk` entries in `dimensions.txt` (z1…z19) gives **769 mm**, not 745 mm. There is **−24 mm left** for z20, tb20 and z21. The table itself is not wrong; the *model* of what z20/z21 are was.
**Resolved from Menghin (OCR, primary source):**
1. `z1 = 61 mm` is **correct and is the crown zone alone** — „Die Spitze des Goldhutes hat eine Höhe von **6,1 cm** und einen Basisumfang von **16,6 cm**." Do not add anything.
2. The **zone heights are Menghin's own** numbers (0,85 / 1,4 / 2,2 / **2,45** / 3,4 / 1,9 / 1,5 cm all verify). So the zone column is not the suspect part. Note the OCR trap: the first pass read zone 5 as „2,5 cm" and „i: 5 cm"; the clean crop read gives **2,45 cm**, exactly `dimensions.txt`'s 24.5 mm. Seven independent hits.
3. `tb* = 7…9 mm` are the **Kerbwülste / Trennbänder**; Menghin's zone widths exclude them, so they are genuinely *additional* height — do not delete them. **They are the largest remaining uncertainty**: they set the Z-origin of every band above them, though (now that the base is the flat Krempe, not the cone's foot) they no longer change the *total* height. Measure two or three bead widths off the Abrollung in P1 rather than trusting the table.
4. Menghin counts the canon as „durch **18 Kerbwulstbänder** und fünf Bänder mit Punkten, Punktkreisen, Doppelkreispunkten und Ringkreisen in, ohne die Spitze, **19 Zonen** gegliedert". `dimensions.txt` has 19 `tb` rows, so the count is *close* — but the sentence is garbled and 18 vs 19 does not by itself account for −24 mm.
5. Menghin says nothing about the two `tussenstuk` (spacer) parts. They are **not attested** by any source — prior-attempt invention. Dropping both frees **40 mm**, i.e. more than the deficit.
6. **RESOLVED — see §2.2.** Zones 20–21 sit on the **Krempe**, which Menghin measures as „**52–55 mm schmale horizontale** Krempe" with an outer size of 307 × 295 mm. It is a *horizontal plate*, so zones 20 and 21 consume radial width, not height; their stacked height is ≈0 (the plan carries the 7 mm residual left by the 745 mm budget). That is exactly why `dimensions.txt` lists z20/z21 with no height: they are concentric rings on the brim, not stacked bands.

The height budget therefore closes as **611 (Schaft) + 18 (cuff) + 100 (Kalotte) + 16 (Krempe rise) = 745 mm exactly**, with the two unattested `tussenstuk` rows deleted and nothing else cut (§2.2). Menghin's own section figures sum to 745 on the nose; `dimensions.txt`'s Kalotten block (109 or 118 mm for z17–z19 + Trennbands) agrees to −7 / +2 mm. Q2 is **closed**.

### Q3 — Symbol count: 651, 1783, or "over 3000"? — **RESOLVED** ✅
Four different numbers were circulating. Menghin's text disambiguates all of them; they are four *different* counts of four *different* things:

| Number | What it actually counts | Source |
|---|---|---|
| **418** | disc bosses (Buckelscheiben, tools Nr. 8–15) over 18 zones, excluding the star, zone 2's double-circles and zone 5's special signs | Menghin, verbatim |
| **1701** | concentric rings summed over those 418 bosses | Menghin, verbatim; `= 1783 − 44 − 38` ✅ |
| **1783** | Menghin's **day-value** sum = Σ(count × rings) over all 21 zones | `berlin.json`, verified above |
| **~651** | *all* punched ornaments incl. the small filler punches (Perlpunkte, Punktkreise, Ringkreise) and the radial spandrel patterns | Schmidt-Kaler's per-zone table |
| ~~~3,393~~ | **not a count of anything.** No per-zone table in the repo sums to it and Menghin contradicts it. Treat as garbled. | `gold_hat.md` (Wikipedia-derived) |

**Consequence for Stage 2:** the physical main motifs are ~480 (418 bosses + 22 double-circle punches + 38 special signs + star), reaching ~650 only if every filler punch also gets an LED. Worst case **~650 LEDs ≈ 5 A** at full white, not 3,393 / 61 A. The `gold_hat_scenarios.md` power budget is wrong by ~6× — and it is no longer a constraint on the LED design.

**How many LEDs to actually fit:** the design target is **one light per main motif** (~480), which is also what Menghin's own counting supports. Fillers can be left unlit or lit as a low-current background.

See Appendix C for the zone-by-zone citations.

### Q4 — Which scholarly reading drives the demo? **[DECISION]**
Menghin (lunisolar) and Schmidt-Kaler (Venus) use *different* band groupings on the same motifs. Stage 1 geometry is unaffected (motifs are motifs), but the LED *zoning* and the displayed arithmetic differ. Recommendation: build the geometry reading-agnostic, make the interpretation a runtime data file (already how `goldhat_layout.json` vs `berlin.json` are split in the prior attempt).

### Q5 — Kalotte + Krempe: is the Berlin hat a plain cone? — **RESOLVED** ✅ *(answer: no, and Menghin gives the dimensions)*
Menghin describes the body as **four** parts, not one cone, and every section has a stated diameter:

> „**Die Spitze, der annähernd konische Schaft mit maximal 125 mm Durchmesser, die 100 mm hohe Kalotte** und die **52–55 mm schmale horizontale Krempe** [sind] gegliedert."
> „Der untere Teil des Schaftes, der **am Fuß einen Durchmesser von 10,8 cm** hat, ist … mit Zierzonen zwischen … gefassten Kerbwülsten strukturiert." (Abb. 17 caption)
> „Im Falz zwischen Kalotte und Krempe befindet sich ein Bronzeband von ca. **10 mm Höhe und 203 mm × 175 mm Durchmesser**."
> „Der Umbruch zur leicht verformten **horizontalen Krempe mit einem Außenmaß von 307 mm × 295 mm**, auf der die Ziermuster von oben konkav erscheinen, ist durch eine Fältelung des Goldblechs markiert."
> „Der Schaft wird durch **16** stark [ausgeprägte] Treibwülste horizontal strukturiert und ist von der Kalotte durch einen **18 mm hohen** vertikal gefältelten Übergang abgesetzt."

The plate captions localise the zones: Abb. 17 = „Unterer Teil des Schaftes, **Kalotte und Krempe**"; Abb. 18 = „**Unteransicht der Krempe** … der Spannungsriss in der Krempe", and it records that „die Öffnung der Kalotte nicht rund, sondern annähernd oval war". Zone 17 is the topmost zone *on the Kalotte* — „b. **Auf der Kalotte** … Den obersten Fries (**Zone 17**) bilden kleine Buckelscheiben mit 2 Ringen" — so zones 17–19 are the Kalotte and 20–21 the Krempe. A „Falz mit innen liegendem Bronzereif" joins them.

**Everything Q5 was blocking is now answered in §2.2**, including the exact numbers. The geometry model changes from "one linear frustum" to "piecewise `(z, r)` profile + a flat annular Krempe plate"; the deliverable changes from 21 stacked bands to **19 stacked bands + a split Krempe plate**; and the print-bed problem shrinks to the Krempe alone (§2.3).

**Residual uncertainty (not blocking):** the *shape* of the Schaft between the four circumference anchors, and whether the 108 mm Schaftfuß vs 125 mm Schaft maximum is a real waist or an oval-cross-section measurement artefact. Both are P1 measurements, neither changes any topology.

### Do the motif counts fit the sectioned profile?
Menghin states the motifs never overlap („es zu keinen Überschneidungen der Scheiben- und Kreismotive") and gives each tool's outer ⌀ (§6.2). So for any zone: `circumference ≥ count × ⌀`. Checking the zones against the §2.2 profile:

| Zone | Section | count × ⌀ | required circumference | profile gives | verdict |
|---|---|---|---|---|---|
| 14 | Schaft, z≈493–527 | 20 × 15 mm | ≥ 300 mm | 393 mm (max ⌀125) | ✅ |
| 15 | Schaft, z≈536–574 | 15 × 21 mm | ≥ 315 mm | 381 mm | ✅ |
| 16 | Schaft, z≈583–602 | 19 × 15 mm | ≥ 285 mm | 351 mm | ✅ |
| 17 | Kalotte top, z≈629–644 | 33 × 15 mm | ≥ 495 mm | ~380 mm | ⚠️ tight |
| 18 | Kalotte, z≈662–700 | 21 × 21 mm | ≥ 441 mm | 465 mm | ✅ |
| 19 | Kalotte, near foot | 23 × 21 mm | ≥ 483 mm | ~560–594 mm | ✅ |
| 20 | Krempe, inner ring | 54 × 12 mm | ≥ 648 mm | 594–770 mm | ✅ |
| 21 | Krempe, outer ring | 47 × 15 mm | ≥ 705 mm | 770–946 mm | ✅ |

Zone 17 is the only marginal one, and it is marginal by construction: it is the 1,5 cm zone at the very top of the Kalotte, where the Kalotte is still narrow. Menghin's own note that zone 17's motifs are the **smallest** of the eight types (Nr. 9, ⌀15, 2 rings) is consistent — it is the zone where the surface was tightest. Two readings of this: either the Kalotte's top is a little wider than ⌀108, or zone 17's 33 motifs are packed tighter than the pitch rule allows. **This is the one motif-layout question P1's Abrollung scan must settle**, and it is a data field (`count`) change, not a geometry change.

Note that the earlier draft's alarming "zone 21 is 6 % short on a straight cone" was an artefact of the too-narrow 211 mm model, and the later "every zone passes on the corrected 293 mm cone" was a coincidence of a wrong profile. On the *sectioned* profile the flare is what makes zones 18–21 fit, and the pitch rule is a genuine argument *for* the Kalotte/Krempe reading, not merely neutral.

**Interim decision (unchanged):** build and print **z13 + z14 + z15** (§11 P3) regardless — all three are unambiguously mid-Schaft, so no part of this discussion can affect them.

---

## 4. Architecture of the model

```
                    ┌─────────────────────────────┐
   top of hat  z1   │  zone 21 … zone 1, stacked  │
                    │  + 20 Trennband rings       │
                    └─────────────────────────────┘
        one STL per band, printed axis-vertical, stacked
```

**Decomposition** — 21 decorative zones. Of these, **zones 1–19 are stacked bands** (each carrying its Trennband as a fused lip) and **zones 20–21 are two concentric motif rings on the single flat Krempe plate**. 19 Trennbands are fused as lips; the `tb19` row is dropped along with the two unattested spacers (§3 Q2).

**Assembly unit [DECISION]:** the requirement says "each band = one STL". Two readings:

| Option | STL count | Pros | Cons |
|---|---|---|---|
| **A (recommended)** | **22** — 19 stacked bands (z01…z19, each with its Trennband fused as a lip at the band's lower edge) + 3 Krempe sectors | fewest joints, fewest files, Trennband is a *relief* not a load-bearing ring, better stacking accuracy; the Krempe is a genuinely separate plate anyway (§2.3) | Trennband cannot be swapped/adjusted independently; 2 glued Krempe seams |
| B | 40+ — zone and Trennband separate | matches `dimensions.txt` 1:1; Trennband colour/finish can differ | 40 joints × tolerance stack; 40 print jobs |

Recommend **A**. Revisit if the Trennbands must be a different material or colour.

---

## 5. Geometry model

### 5.1 Parameters (one JSON file, `data/hat_parameters.json`)
```jsonc
{
  "height_total_mm": 745.0,
  // The profile is PIECEWISE, from Menghin's four circumference anchors plus the
  // section diameters (§2.2). A single slope constant is now known to be wrong.
  "profile": [ { "z":   0.0, "r":   0.0 },   // apex (nominal)
               { "z":  61.0, "r":  26.4 },   // Menghin A: tip height 61 mm, base circ 166 mm
               { "z": 160.0, "r":  43.8 },   // Menghin B: zone 5 lower edge, circ 275 mm
               { "z": 445.0, "r":  59.1 },   // Menghin C: circ 371 mm below zone 12
               { "z": 510.0, "r":  62.5 },   // Schaft maximum, 125 mm
               { "z": 611.0, "r":  54.0 },   // Schaftfuss, 108 mm  <- waisted
               { "z": 629.0, "r":  56.0 },   // 18 mm crimped cuff -> bottom of the Kalotte
               { "z": 729.0, "r":  94.5 },   // Kalottenfuss / bronze band, 189 mm
               { "z": 745.0, "r": 150.5 } ], // Krempenrand, 301 mm  <- widest point
  "profile_interp": "pchip",       // monotone piecewise-cubic; NEVER a slope constant
  "wall_thickness_mm": 2.0,        // NOT 0.06 — the real foil is unprintable
  "wall_thickness_tb_mm": 3.0,     // Trennbands read as a thicker ridge
  "symbol_relief_mm": 0.8,         // emboss/engrave depth        (see §6)
  "registration_lip_mm": 6.0,      // inner lap ring for stacking
  "registration_clearance_mm": 0.25,
  "krempe": { "r_inner_mm": 94.5, "r_outer_mm": 150.5, "z_inner_mm": 729.0,
               "z_outer_mm": 745.0, "sectors": 3 },
  "rings": [ { "id":"z01", "kind":"zone", "h":61.0 },
             { "id":"tb1", "kind":"trennband", "h":7.0 },
             ... ]
}
```
Each ring stores only `id`, `kind` and `h`; the generator derives `r_top`/`r_bottom` by evaluating the profile, then asserts contiguity (`z_bottom[i] == z_top[i+1]`). That way Q2 is fixed in one place and a profile revision is a data edit.

Expected derived values, asserted by `verify_geometry.py`: surface area ≈ **0.284 m²** (vs 0.385 m² for the old straight cone), filament at 2.0 mm ≈ **0.57 L ≈ 0.7 kg** before subtracting the windows, and mass consistency with Menghin's stated **490 g** at 0.06 mm gold foil (≈328 g of gold alone, the balance being the bronze rings and reinforced edges).

### 5.2 Band as a solid
Each *stacked* band (zones 1–19, TBs fused as lips) = `outer_frustum/frustum-band − inner offset` (an open ring with a non-linear outer profile), plus:
- a **registration lip**: a 6 mm tall, wall-thickness ring on the inside of the lower edge, sized to slip into the band below (0.25 mm clearance). Axis-vertical printing makes this support-free.
- a **Trennband ridge** at its lower edge (Option A), 1 mm proud, 9 mm tall — the relief that separates zones visually.
- **symbol features** (§6) on the outer surface.

The **Krempe** is a different primitive: `annular_disc(r_inner=94.5, r_outer=150.5, z=729→745)`, with zones 20 and 21 as **concentric** motif rings rather than stacked ones, split into **3 radial sectors** (§2.3). Its two motif rings are placed at the mid-radius of each radial half: zone 20 at r ≈ 94.5–122, zone 21 at r ≈ 122–150.5.

### 5.3 Symbol projection — the one non-obvious bit
Do **not** try to bend a flat pattern onto the cone (the prior attempt's unrolled-frustum SVG route, `reference/cad/svg/z04_strip.svg` — an annular sector 795 mm across, which cannot be mapped back onto a cone in FreeCAD without a bend feature).

Instead: for each motif, build a prism in a local frame tangent to the cone at the motif's (θ, z), and boolean it radially. The visible shape on the outer skin is then the correct radial projection — which is exactly what you want for an LED light window anyway. Chord error for a 25 mm motif on a 100 mm radius is 0.8 mm; acceptable for a stylised model, and it shrinks toward the top. **The local frame's tilt is evaluated from the profile's local slope**, which varies from 4° (Schaft) to 20° (Kalotte) — so the tilt must be per-motif, not a global constant.

Placement maths: `r(z)` from the piecewise profile; motif angular pitch `Δθ = 360° / n_zone`. For the Krempe, motifs are placed on *concentric circles in a horizontal plane* instead — the prism axis is vertical, i.e. the light windows become drillings, which is the easiest possible LED geometry and a bonus for Stage 2.

---

## 6. Symbol system

### 6.1 Getting the layout — the Abrollung
`assets/berliner_goldhut_abrollung.jpg` (648×800) is the unrolled surface view and is the **primary geometric source**. Method:

1. Determine whether it is a photographic true development (width ∝ circumference, 2πr) or an orthographic silhouette (width ∝ 2r). Both are linear in r; the difference is a constant factor.
2. Calibrate with two anchors: total height = 745 mm, and the **Krempenrand ⌀ 301 mm** (§2.2 — *not* 211 mm, and not the shaft's 125 mm either; the widest *feature* is the brim, and the width is now known from Menghin regardless of what the photo yields).
3. Extract `r(z)` by measuring image width at each of the band boundaries → **replace the interpolated profile** between the four Menghin anchors, and settle the two open shape questions (Schaft concavity; whether the 108 mm Schaftfuß is a real waist or an oval-measurement artefact).
4. Cross-check against `assets/Berlín_Goldhut_01.JPG` (800×1873, front-on). The topology is already settled by §2.2; what P1 adds here is the *intermediate* shape.

⚠️ The obvious automatic route does not work yet: naive thresholding fails because a large part of the gold surface is *darker* than the background in these photos (interior shadow), so per-row extents pick up background instead of the object. `scripts/measure_silhouette.py` (PIL + numpy — **`cv2` is not installed and must not be added as a dependency**) is a working helper that already recovers the *outline* and the bottom flare, but it must be tuned per image (background subtraction, or manual landmark clicking) before it can report a profile in mm. Budget half a day for this, not an hour.

Then transcribe, band by band, the motif type + count into `data/zones.json` (21 rows — a manual job with a magnifier, not CV). CV/contour tracing is a fallback, not a plan.

### 6.2 Motif primitives — parameterised, not traced
The prior attempt has SVG/bitmap traces (`symbol12_bitmap_traced.svg` etc.). Do **not** recycle them: they are hand-fitted circles, and the requirement is explicitly stylised. Define a small set of primitives:

| Primitive | Params | Covers |
|---|---|---|
| `ring` | r, count | concentric-circle motifs — **`count ∈ {2, 3, 5, 6}` only** |
| `disc` | r | plain punched dot |
| `ring_dot` | r_outer, count, r_dot | disc inside N concentric rings (the classic "sun" of the Scheibenbuckel) |
| `circle_row` | r_dot, n | rows of small dots (Perlpunktbänder, Punktkreise) |
| `zigzag` | teeth, amplitude | Trennband / Kerbwulst motifs |
| `oval` / `crescent` | a, b, rotation | sparse special motifs (Mondsicheln, Augensymbole) |
| `star8` | r, points | the tip's eight-rayed star (zone 1) — a one-off on the crown |

Each is a handful of `Part.makeCircle` / `makePolygon` calls. No SVG import path, no bitmap tracing, no 17 hand-made files.

**Ring counts are 2, 3, 5 or 6 — never 4.** Menghin: „Hauptzierelemente sind acht verschiedene Scheibenbuckel unterschiedlicher Größe mit **zwei, drei, fünf oder sechs** konzentrischen Ringen." The prior attempt's "symbol 13 = 4 rings" is not attested. Menghin's tool legend gives the diameters the primitives must hit:

| Tool | Rings | ⌀ (from legend) | Zones Menghin attributes explicitly |
|---|---|---|---|
| Nr. 8 | 3 | 12 mm | 3 (14×), 20 (54×) — „Derselbe Ornamentstempel kommt sonst nur noch in Zone 20 auf der Krempe vor" |
| Nr. 9 | 2 | 15 mm | 17 (33×) |
| Nr. 10 | 5 | 13 mm | 4 (15×) |
| Nr. 11 | 3 | — | — (filler Scheiben) |
| Nr. 12 | 3 | — | 9 (19×) |
| Nr. 13 | 2 | 15 mm | 16 (19×) |
| Nr. 14 | 5 | 15 mm | 10 (19×), 12 (20×), 14 (21×), 21 (47×) — same punch throughout |
| Nr. 15 | 6 | 21 mm | 15 (15×), 18 (21×), 19 (23×) |
| Nr. 4–7 | — | — | Perlpunkt-, Kreisring-, Punktkreis-, Doppelkreispunkt fillers + radial spandrels |

These ⌀ values against the local cone circumference give the motif pitch (≈ `πD / count`), which is a free second check on every per-zone count.

### 6.3 Physical form of a motif — **[DECISION]**
This is the single decision that ties Stage 1 to Stage 2.

| Option | Stage 1 look | Stage 2 | Verdict |
|---|---|---|---|
| **C (recommended)** — motif is a **through-window** in the band wall | motif reads as a crisp silhouette; held to a light it already glows | literally satisfies "LED behind the outer surface behind the symbols"; one LED per window | smallest geometry, one print per band |
| B — motif embossed/engraved on a solid wall | closest to repoussé relief | needs re-cutting every band to add windows | rejects the second stage for the first |
| A — opaque outer skin + inner translucent diffuser sleeve | best looking | needs per-symbol baffles or light bleeds across the whole zone | twice the printing, alignment risk, deferred |

Recommend **C**. Add an optional inner diffuser sleeve later (Stage 2) without touching the bands — that is the "A" benefit at no Stage-1 cost. Note the structural consequence: at ~480 main motifs on 0.284 m² (§2.2) — about **1 window per 6 cm²** — windows occupy a small fraction of the shell; keep a minimum 3 mm ligature between neighbouring windows, and add interior ribs if any zone's windows exceed ~40 % of its surface. The 418-boss figure (§3 Q3) plus each boss's Menghin punch diameter (⌀12–21 mm) fixes the per-zone window count and size directly — no counting from scratch needed.

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
| Orientation | axis vertical, band lying flat; **Krempe flat in its own plane** | 4–20° wall ⇒ under 45°, so zero overhang and zero supports either way; the registration lip prints inside-free |
| Layer height | 0.16 mm | ~0.6 kg of filament; don't throw resolution away for nothing |
| Walls | 3 loops ≈ 1.6 mm + top/bottom | 2.0 mm nominal wall; symbol windows cut through |
| Material (Stage 1) | matte PLA, bronze/gold silk | reads as gold without paint; **not** silk for fit-test coupons (silk hides dimensional error) |
| Per-band print | 1 at a time; 3 for the Krempe sectors | largest stacked band ⌀189 mm × 38 mm tall; Krempe sector ≈ 226 × 151 mm flat |
| Tolerance | 0.25 mm radial clearance on the lap joint | verify with a 3-band fit test before committing to 19 prints |
| Total | 22 prints, ~0.6 kg incl. windows | |

**Fit test first:** print z13 + z14 + z15 (a plain repeating stretch) 1:1 and check that the stack is straight and the lap joint doesn't wobble. Only then print the rest. The top zone (z1) and the Krempe print last — they are the least forgiving parts and benefit from a calibrated machine.

---

## 10. Stage-2 constraints this plan must respect

Nothing below is implemented now; these are the interfaces Stage 1 must leave open.

1. **Window per motif** (§6.3, Option C) — each motif is a light channel.
2. **Interior cavity**: the lap joint leaves a natural annular gap; keep ≥ 8 mm of clear radial depth behind a band so an LED PCB can be slipped in, and leave a **20 × 6 mm cable notch** in each lap lip at a common clock angle (recommend θ = 0°, i.e. the hat's "front"), so a single wiring spine runs up the inside.
3. **Modular Z-addressability**: zones are already separate parts, so per-zone LED segments need no extra geometry.
4. **LED budget** is now **~480 main motifs** (≈5 A), not 3,393 (≈61 A) — §3 Q3 is closed. The `gold_hat_scenarios.md` power budget is wrong by ~6× and must be rewritten, not just revised.
5. **Kalotte/Krempe (Q5) — RESOLVED** (§2.2, §3 Q5). Zones 17–19 are the Kalotte (⌀108→189, ~20° half-angle) and 20–21 the near-horizontal Krempe (⌀189→301, 16 mm rise). Both are *easy* for Stage 2: the Kalotte's windows still face radially outward, and the Krempe's windows become vertical drillings in a horizontal plate, so an LED strip can be laid underneath it — that zone pair (54 + 47 motifs) is actually the simplest to light in the whole model.
6. **M5 Core S3 + display** sits outside the hat; plan a base plinth/cradle (a separate later model) that hides the electronics and holds the cone upright. **New constraint from §2.2:** the hat does *not* stand on its own — its contact ring is the Krempenrand at ⌀301 mm, with a hollow interior of ⌀189 behind it (and ⌀108 further up). The cradle must therefore support the Krempe from below, which is convenient: the space under the brim is exactly where the M5, the PSU and the wiring spine can live, invisible from outside.

---

## 11. Phases & milestones

| Phase | Work | Exit criterion |
|---|---|---|
| **P0 — resolve blockers** | Q1 doc rename; Q5 geometry (done — see §2.2); Q2 height reconciliation | height table sums to 745 mm; sectioned profile in `hat_parameters.json` |
| **P1 — profile extraction** | Abrollung calibration → refine `r(z)` between Menghin's four anchors; validate against photo silhouette | `r(z)` within ±2 mm of the photo at 10 sample heights |
| **P2 — motif catalogue** | Count and classify motifs from the Abrollung → `symbols.json` + `zones.json`; implement primitives | `verify_calendar.py` reproduces every Menghin zone value (1783 total, 1739, 142, 1597, 1701×2) |
| **P3 — geometry kernel** | `build_goldhat.py`; one band end-to-end (start with z13) | an STL that visually matches the Abrollung strip for that zone |
| **P4 — full generation** | zones 1–19 + the Krempe plate split into 3 sectors → `stl/` | all 22 STLs watertight, `verify_geometry.py` passes |
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
sum(day_value[3..21]) - day_value[5]
  - day_value[16] - day_value[17]            == 1701   ← Menghin's stated circle-ring total
sum(day_value[3..21])
  - day_value[2] - day_value[5]              == 1701   ← same identity, reached the other way
sum(bosses[zones excluding 1,2,5])            ==  418   ← Menghin's stated boss count
zone_count                                   ==   21
```
The two `1701` lines are the strongest check available: they are Menghin's own two independent statements, and they agree only if the per-zone counts *and* the ring multipliers are both right. See §2.1.

**`scripts/verify_geometry.py`** — on the exported STLs:
```
bounding box height of the full stack == 745 ± 3 mm
outer diameter at each boundary       == r(z) target ± 0.5 mm
Schaft maximum diameter               == 125 ± 3 mm   (Menghin)
Schaftfuss diameter                   == 108 ± 3 mm   (Menghin)
Kalottenfuss / bronze-band diameter   == 189 ± 5 mm   (Menghin, oval 203 x 175)
Krempenrand outer diameter            == 301 ± 5 mm   (Menghin, oval 307 x 295)
Krempe radial width                   ==  52..55 mm   (Menghin)
each solid                            watertight, volume > 0, no self-intersection
every solid's bbox fits 256 x 256 x 256 mm   <-- the printability assertion (§2.3)
Σ band heights                        == 745 mm   (catches the Q2 class of error)
```

**`scripts/verify_calendar.py` on the STL (Stage 2 prep only)** — count through-windows per band and assert it equals the motif count in `zones.json`. Cheap sanity check that geometry and data did not drift apart.

**Visual** — screenshot each band overlaid on its Abrollung strip crop; a human eyeballs 21 pairs once.

---

## 13. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| ~~Q2 height discrepancy~~ **RESOLVED** — the Krempe is a horizontal plate with ~0 stacked height, so summing z1…z19 overshoots by exactly that (§2.2, §3 Q2). The two `tussenstuk` rows are unattested and get deleted | — | — |
| ~~Q5 Kalotte/Krempe unknown~~ **RESOLVED** (§2.2, §3 Q5) | — | residual: the Schaft's intermediate curvature between the four anchors, and whether the 108/125 mm pair is a real waist — both P1 |
| Q3 motif count wrong | ~~Stage 1 unaffected~~ **RESOLVED** — 418 bosses / 1701 rings / 1783 days all three agree (§3 Q3). Residual risk: individual per-zone counts read off the Abrollung may differ from Menghin's by a few percent (he gives only 5 zones explicitly) | re-read the OCR against the image before typing any count |
| Manual motif transcription errors | a zone's day-value assertion fails | the P2 assertion catches it immediately — build P2 data with the test running |
| 22-part tolerance stack drifts over 745 mm | hat leans or joints open | lap joint + 3-band fit test at P5; add a removable internal mandrel as a fallback |
| FreeCAD/OCCT boolean failures on dense motif clusters | band won't build | headless generation isolates crashes; fall back to `fuse`-then-single-`cut` (fuse all motif prisms first — a single boolean against the heavy shell) |
| Abrollung is distorted (a photo, not a true development) | wrong profile | calibrate on two known anchors and reject the source if residuals exceed tolerance |

---

## 14. Immediate next actions

1. Fix the `dimensions.md` reference (Q1) — 1 minute. Delete the two unattested `tussenstuk` rows from the height table.
2. **Refine the profile** — `scripts/measure_silhouette.py` already exists (PIL+numpy; `cv2` is not installed and must not be added). It needs per-image tuning before it can report `r(z)` in mm; do that, then refine the interpolated Schaft curve between Menghin's four anchors. Budget half a day. Menghin supplies all four `(z, ⌀)` anchors, so this step only affects the *intermediate* Schaft curvature — it is no longer a blocker for anything.
3. **Measure one Kerbwulst width** from the Abrollung. It is the last free parameter in the ~41-band height chain, and it shifts individual band Z-origins by up to ±15 mm even though it no longer moves the total.
4. **Verify the four new Menghin diameters by crop re-read** if any of them is going to be load-bearing (§Appendix C recipe): 125 / 108 / 203×175 / 307×295. Two independent crops already agree on all four, so this is a cheap belt-and-braces step, not a blocker.
5. Confirm Option **A** for the STL decomposition (§4), Option **C** for the motif form (§6.3), and the **Krempe 3-sector split** (§2.3 — note 2 sectors do *not* fit: the bbox is still 301 mm wide).
6. Then start P2 (motif catalogue), which is the long pole.

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
| `scripts/analyze_cone.py` | OpenCV cone-measurement script (from prior attempt) | **not runnable — `cv2` is not installed and will not be added.** Superseded by `scripts/measure_silhouette.py` (PIL+numpy) |
| `scripts/measure_silhouette.py` | PIL+numpy silhouette/profiler written for this plan | working helper; recovers outline + bottom flare, needs per-image tuning before it can report mm |
| `assets/menghin/menghin_page{20..25,27..31}.jpeg` | 11 photos of Menghin (2010) pp. 18–29 (page 26 missing; pages 21/22/28 are pure plates, 30 is Abb. 23) | **primary source for Q2/Q3 — now OCR'd** |
| `assets/menghin/ocr/page*.txt` | German OCR of the above (tesseract 5.5.3, `deu`+`osd`, `--psm 1`) | citable text: `page27.txt` = the 21-zone analysis, `page31.txt` = the 1701/418 sentence, `page30.txt` = Abb. 23 legend |
| `reference/m5/data/berlin.json` | Menghin's per-zone day-values | **ground truth**, verified §2.1 |

## Appendix B — numbers used in this plan, and where they come from

| Number | Value | Source / derivation |
|---|---|---|
| Total height | 745 mm | `dimensions.txt`, and closes exactly: 611 (Schaft) + 18 (cuff) + 100 (Kalotte) + 16 (Krempe) ✅ |
| Zone 1 (Spitze) height | 6,1 cm | **Menghin, verbatim ✅** |
| Zone 1 base circumference | 16,6 cm | **Menghin, verbatim ✅** |
| Zone 5 lower-edge circumference | 27,5 cm | **Menghin, verbatim ✅** |
| Shaft circumference (lower) | 37,1 cm | Menghin, verbatim ✅ |
| **Schaft maximum diameter** | **125 mm** | **Menghin, verbatim** (crop re-read ×2) ✅ |
| **Schaftfuß diameter** | **108 mm** | **Menghin, Abb. 17 caption** ✅ |
| **Kalotte height** | **100 mm** | **Menghin, verbatim** ✅ |
| **Schaft→Kalotte cuff** | **18 mm**, vertically crimped | **Menghin, verbatim** ✅ |
| **Bronze band in the Kalotte/Krempe Falz** | **203 × 175 mm, 10 mm tall** (mean ⌀189) | **Menghin, verbatim** ✅ |
| **Krempenrand (widest point)** | **307 × 295 mm** (mean ⌀301) | **Menghin, verbatim** ✅ |
| **Krempe radial width** | **52–55 mm**, horizontal | **Menghin, verbatim** ✅ |
| Wall thickness (real) | 0,06 mm | Menghin; weight 490 g consistent with 0,286 m² of gold |
| Outer surface area | 0.284 m² | integration of the piecewise profile (§2.2) |
| Filament @ 2.0 mm wall | ~570 cm³ ≈ 0.6–0.7 kg | area × thickness, before the windows |
| ~~Old straight-cone figure: 293 mm base, 9.94°, 0.385 m²~~ | **superseded** | two-anchor fit (166 mm @ z=61, 275 mm @ z=160) — valid only as a check on the upper Schaft |
| Punch tool diameters | Nr. 8 ⌀12/3 rings, Nr. 10 ⌀13/5, Nr. 9 & 13 ⌀15/2, Nr. 14 ⌀15/5, Nr. 15 ⌀21/6 | **Menghin tool legend ✅** |
| Disc bosses (Nr. 8–15) | 418 over 18 zones | **Menghin, verbatim ✅** (plan's recount: 420) |
| Concentric rings total | 1701 | **Menghin, verbatim ✅** = 1783 − 44 − 38 |
| Days, zones 3–21 | 1739 | Menghin, per `berlin.json` |
| Days, zones 5+16+17 | 142 | Menghin |
| Days, 54 synodic months | 1597 (≈1594.65) | Menghin |
| Physical main motifs | ~480 (418 + 22 + 38 + star) | derived, §3 Q3 |
| Physical ornaments incl. fillers | ~651 | Schmidt-Kaler table, §3 Q3 |
| Day-value total | 1783 | Menghin table |
| Printed parts | 22 (Option A: 19 bands + 3 Krempe sectors) or 40+ (Option B) | §4 |

---

## Appendix C — Menghin (2010) OCR: provenance and reproduction

### Source
`assets/menghin/menghin_page{20,21,22,23,24,25,27,28,29,30,31}.jpeg` — 11 phone photos of Menghin 2010, book pp. 18–29 (page 26 never photographed). Page images are 4032×3024, EXIF orientation 6.

Pages 21, 22 and 28 are **pure plates** (OCR yields ~0 text) — that is expected, not an OCR failure. `page30` is the Abb. 23 symbol-distribution figure plus its legend.

### Reproduction recipe
Tesseract bundles only `eng`; `deu` was not installed and `sudo` was unavailable, so the models live in a user prefix. No package install is needed:

```bash
T=~/.local/share/tessdata && mkdir -p $T
curl -fsSL -o $T/deu.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/main/deu.traineddata
curl -fsSL -o $T/osd.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/main/osd.traineddata
# osd.traineddata is REQUIRED: --psm 1 (auto page segmentation) fails silently without it
# and returns 180°-rotated garbage, because the page photos have no usable EXIF rotation applied.
export TESSDATA_PREFIX=$T
ls assets/menghin/*.jpeg | sed 's|.*/menghin_||; s|\.jpeg||' | xargs -P 4 -I{} sh -c \
  "TESSDATA_PREFIX=$T tesseract assets/menghin/menghin_{}.jpeg assets/menghin/ocr/{} -l deu --psm 1"
```

Output: `assets/menghin/ocr/page*.txt` (~22 kB total).

**⚠️ Known failure mode — psm 1 silently drops numbers.** On `page27.txt` the sentence reads „Die Spitze des Goldhutes hat eine Höhe **an** und einen Basisumfang von 16,6 cm" — the `von 6,1 cm` is *gone*, and even `2,45 cm` came out as `2,5 cm`. Body prose is reliable; **any digit, decimal or number-in-a-table must be re-read from the image** before it is used. The failure is worse on `page25.txt`, where the entire section-diameter sentence (125 / 108 / 203×175 / 307×295) is garbled in the psm-1 text and only appears on a crop re-read. Cheap verification recipe (grayscale + normalize + 150 % + `--psm 6` recovers the two-column text cleanly on a crop):

```bash
# single column, top 55 % — recovers the tip dimensions
magick assets/menghin/menghin_page27.jpeg -auto-orient -crop 100%x55%+0+0 +repage \
        -colorspace Gray -normalize -resize 150% /tmp/p27.png
tesseract /tmp/p27.png stdout -l deu --psm 6 | grep -A2 "Goldhutes"
# → „Die Spitze des Goldhutes hat eine Höhe von 6,1 cm und einen Basisumfang von 16,6 cm."
# → „Die Zone 5 ist 2,45 cm breit"

# page 25, top 30 % — recovers ALL FOUR section diameters (§2.2)
# (this is the only way to see them; they are absent from ocr/page25.txt)
for y in 0 25 50; do
  magick assets/menghin/menghin_page25.jpeg -auto-orient -crop 100%x30%+0+${y}% +repage \
          -colorspace Gray -normalize -resize 150% /tmp/p25_$y.png
  tesseract /tmp/p25_$y.png stdout -l deu --psm 6 | grep -nE "307|295|203|175|125|108|Krempe|Schaft|Kalotte"
done
# → „Schaft mit maximal 125 mm Durchmesser, die 100 mm hohe Kalotte"  (2 of 3 crops agree; 1 reads 127)
# → „Bronzeband von ca. 10 mm Höhe und 203 mm x 175 mm Durchmesser"
# → „Außenmaß von 307 mm x 295 mm"
# → „52-55 mm schmale horizontale Krempe"
```

Every number asserted in §2.1 and §2.2 has been re-read this way. `scripts/measure_silhouette.py` cannot help with printed text — this recipe is the only route.

### Where each claim comes from

| Claim | File | How to find it |
|---|---|---|
| 6,1 cm / 16,6 cm tip; 21 zones; 24 punch tools; tool catalogue + diameters | `ocr/page27.txt` | `grep -n "Spitze des Goldhutes" page27.txt` |
| Zone 2 = 0,85 cm / 22 Doppelkreispunzen; zone 3 = 1,4 cm / 14 × 3 rings; zone 4 = 2,2 cm / 15 × 5; zone 5 = 2,5 cm / 38 signs / 27,5 cm circumference | `ocr/page27.txt` | second half of the file |
| Kalotte + Krempe structure; Abb. 16/17/18 captions; **Schaftfuß ⌀10,8 cm**; 22 Doppelkreispunzen zone 2 | `ocr/page23.txt` | `grep -n "Kalotte\|Krempe" page23.txt` |
| **All four section diameters**: 125 (Schaft max), 100 mm Kalotte, 18 mm cuff, 203×175 bronze band, 307×295 Krempe, 52–55 mm horizontal, 0,06 mm wall, 490 g, 16 Treibwülste | `ocr/page25.txt` | `grep -n "307\|203\|125\|Krempe" page25.txt` — **then crop-re-read, because psm 1 garbles these digits** |
| **418 Buckelscheiben / 1701 Kreisringe / 18 zones / 38 Sonderzeichen**; zone 21 = 47 × 5; zone 20 = 54 × 3; zones 18/19 = 21 & 23 × 6; zone 16 = 1,9 cm / 19 × 2; zone 17 = 1,5 cm / 33 × 2; zone 15 = 15 × 6 | `ocr/page31.txt` | `grep -n "1701" page31.txt` |
| Zone 7/8/9 arrangement; 3,4 cm zone 9 | `ocr/page29.txt` | `grep -n "3,4 cm" page29.txt` |
| Abb. 23 legend (Punktkreispunzen, Ringpunzen, Scheibensymbole colours) | `ocr/page30.txt` | whole file |
| Comparative chapter (Ezelsdorf-Buch etc. — 18 zones, 8-pointed star) — **not the Berlin hat**, do not conflate | `ocr/page20.txt`, `ocr/page25.txt` | `grep -n "Ezelsdorf"` |

⚠️ Pages 20–25 mix the Berlin hat with the comparative hats (Schifferstadt, Avanton, Ezelsdorf-Buch). Zone counts of **18** and the „hybrider Kegelhut" belong to the *comparison* objects, not to Berlin (21 zones).
