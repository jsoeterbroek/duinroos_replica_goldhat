# Implementation Plan — Berlin Gold Hat Replica

**Status:** nothing here is built yet. **One item remains, and it is a choice, not an unknown:** the **motif form** is deliberately deferred to a print (P3.5, §6.3). The profile `r(z)` — previously the only *unknown* — is now **settled** (P1, §6.1, §12): it is Menghin's **9 documentary constraints** with `pchip` between them, and the photo check has been performed, quantified, and its limits recorded.

| Was | Now |
|---|---|
| Q1 doc rename | ✅ fixed |
| Q2 height reconciliation | ✅ exact 745 mm, §2.2 |
| Q3 motif arithmetic | ✅ 418 / 1701 ×2 / 1783 derived, §2.1 |
| Q5 Kalotte/Krempe geometry | ✅ resolved, §2.2 |
| Assembly unit (22 vs 40+ files) | ✅ **Option A, 22 files** |
| **P1 profile `r(z)`** | ✅ **settled — 9 documentary constraints + `pchip`**, photo-checked, §6.1 / §12 |
| **Motif physical form (R / W / RW)** | ⏸ deferred to a 3-coupon print test at P3.5, §6.3 |
| Q4 which scholarly reading drives the demo | open, Stage 2 only — does not block geometry, §3 |

**P1, the profile — closed:**

| Item | Result |
|---|---|
| Menghin's four circumference anchors (A 166 mm @ 61, B 275 mm @ 160, D 349 mm @ 312, C 371 mm @ 445) + five section diameters (⌀125, ⌀108, ⌀127, ⌀189, ⌀301) | ✅ **9 hard constraints**; reproduced exactly by construction |
| the shape *between* them | ✅ `pchip` — monotone to the ⌀125 max at z=510, then decreasing to z=611, no overshoot; **asserted**, not eyeballed |
| photo corroboration | ✅ the **⌀301 Krempenrand to 0.3 mm**, the mid-shaft z=312 to **1.2 mm**, the shaft to **1.6–2.5 mm RMS** in radius; worst residuals localised and **attributed**, §12 |
| the *original* ±2 mm-at-10-heights criterion | ❌ **withdrawn as unachievable** — one photo cannot separate a profile error from a segmentation error at that scale, and that is now *demonstrated*, not asserted (§6.1) |
| one region left explicitly unresolved | ⚠️ the **cuff / Kalotte base, z≈600–640**: Menghin's ⌀108 Schaftfuß and ⌀127 Kalotte base and the photo's ~⌀119 silhouette disagree by ~5 mm. A **cuff-shape** question for P3, not an `r(z)` question; the documentary values are kept |

Everything else is a choice or a print. Exit criterion (§11 P1, restated in full in §12): `r(z)` reproduces all 9 documentary constraints with **zero** error; the photo's *tilted projection* of `r(z)` agrees to **≤2 mm radius at the ⌀301 Krempenrand and at z=312**, and **≤5 mm radius per shaft section**, with every larger residual attributed to a named cause. The ⌀189 Kalottenfuß and the cuff are **not** photo-checkable from this view and are held to Menghin alone. Run with `python3 scripts/measure_silhouette.py "<photo>" --project` (`cv2` is not installed and must not be added — PIL + numpy only).
**Scope of this plan:** Stage 1 (static, printable replica). Stage 2 (LED + M5 demo) is only planned as far as it constrains Stage-1 geometry (§10).

---

## 1. Goal & deliverables

A 1:1, stylised replica of the Berlin Gold Hat, printed in segments that stack into the full 745 mm object (a long conical **Schaft** that widens to ⌀125 mm then tucks in to ⌀108 mm at the foot, an 18 mm pleated cuff, a flared **Kalotte**, and a flat **Krempe** plate at the bottom).

| # | Deliverable | Where |
|---|---|---|
| D1 | Single source of truth for dimensions: `data/hat_parameters.json` | repo |
| D2 | Symbol catalogue + per-zone layout: `data/symbols.json`, `data/zones.json` | repo |
| D3 | Generator: `scripts/build_goldhat.py` (standalone, `freecadcmd`-runnable) | repo |
| D4 | One STL per band: `stl/berlin_goldhat_z01.stl` … `z19.stl`, plus `krempe_a/b/c.stl` for the ⌀301 mm brim plate, which exceeds the print bed (§2.3). **22 files.** | repo |
| D5 | Assembly/stacking doc + registration scheme, incl. the Krempe sector joints | `docs/` |
| D6 | Verification scripts: `scripts/verify_calendar.py` ✅ (created, passing) + `scripts/verify_scenarios.py` ✅ (Stage-2 colouring + day values) + `scripts/verify_geometry.py` (P3, needs geometry) | repo |
| D7 | **Motif-form test coupons** — 3 single-band STLs, one per candidate motif form (§6.3), for the deferred print-and-look decision. Not part of the object. | `stl/test/` |

Explicit non-goals for Stage 1: dents, creases, foil-thickness realism, museum-accurate surface irregularity.

---

## 2. What is already established (verified in this draft)

These are cross-checks I ran against the existing docs. They are the numeric anchors the model must satisfy.

### 2.1 Menghin's day-values — **VERIFIED against the primary source** ✅✅
`reference/m5/data/berlin.json` is not a symbol count — it is Menghin's **day-value per zone** (symbols × rings).

Menghin's own text (2010, Ornamentanalyse, `assets/menghin/text/`) supplies **four independent arithmetic identities** that `berlin.json` satisfies exactly:

| Menghin's sentence (`text/menghin_page31.txt`) | Arithmetic |
|---|---|
| „If one disregards the apex (Zone 2) … as well as Zone 5 with its 38 ‚special symbols' …" | 21 zones − {1, 2, 5} = **18 disc-bearing zones** ✅ |
| „…the **418 bossed discs** (Nos. 8–15) are distributed across 18 horizontal ornamental zones …" | Σ counts over those 18 zones = **418 exactly** ✅ |
| „…and comprise a total of **1,701 concentric rings**." | Σ (count × rings) over those 18 zones = **1701 exactly** ✅ |
| „…If one disregards the apex (Zone 2) … as well as Zone 5 with its 38 ‚special symbols' …" | `1783 − zone1(0) − zone2(44) − zone5(38) = **1701**` ✅ |

The third and fourth rows are two *different routes* to the same 1701 — subtracting zone-2 and zone-5 from the total ring count, versus multiplying out the 18 remaining zones — and they agree.

**418 and 1701 are not merely *asserted* by Menghin — they are *derivable* from his own per-zone counts.** Take his count and tool number for each of the 21 zones, look up the tool's ring count in his Fig. 21 legend, multiply:

| Zone | Menghin's sentence (`text/menghin_page*.txt`) | count | tool | rings | × = |
|---|---|---|---|---|---|
| 1 | „an eight-rayed star set against a dotted background" | — | — | 0 | **0** |
| 2 | „a 0.85 cm wide band … contains **22** circular punches featuring **two** rings (No. 6)" | 22 | 6 | 2 | **44** |
| 3 | „a 1.4 cm wide band … featuring **14** encircling bossed discs, each with **three** concentric circles (No. 8)" | 14 | 8 | 3 | **42** |
| 4 | „Zone 4—2.2 cm wide … featuring **15** small bosses with **five** concentric circles (No. 10)" | 15 | 10 | 5 | **75** |
| 5 | „**19** horizontal crescent shapes with a central dot (No. 16), and beneath them, an equal number of almond-shaped eye symbols (No. 17)" | 19+19 | 16, 17 | 1 | **38** |
| 6 | „Zone 6 is [**2.5**] cm wide and decorated with **18** bossed discs featuring **five** rings (No. 10)" | 18 | 10 | 5 | **90** |
| 7 | „a continuous series of **19** discs with **three** circles (No. 11)" | 19 | 11 | 3 | **57** |
| 8 | „It shows **21** small bumps with **five** circles (No. 10)" | 21 | 10 | 5 | **105** |
| 9 | „The main pattern consists of **19** large bumps with **three** circles (No. 12)" | 19 | 12 | 3 | **57** |
| 10 | „The repeating pattern consists of **19** bosses with **five** circles (No. 14)" | 19 | 14 | 5 | **95** |
| 11 | „a band of equal width containing **20** correspondingly large bosses with **three** circles (No. 12)" | 20 | 12 | 3 | **60** |
| 12 | „its main pattern … consists of **20** bossed discs featuring **five** circles (No. 14)" | 20 | 14 | 5 | **100** |
| 13 | „**20** large discs with **three** concentric rings (No. 12)" | 20 | 12 | 3 | **60** |
| 14 | „**21** bosses framed by **five** circles (No. 14)" | 21 | 14 | 5 | **105** |
| 15 | „the main ornament consists of **15** bosses featuring **six** concentric circles (No. 15)" | 15 | 15 | 6 | **90** |
| 16 | „displays **19** shallow boss-discs featuring **two** rings (No. 13)" | 19 | 13 | 2 | **38** |
| 17 | „displays **33** small bosses featuring **two** circles (No. 9)" | 33 | 9 | 2 | **66** |
| 18 | „zone 18 contains **21** … embossed discs featuring **six** circles (No. 15)" | 21 | 15 | 6 | **126** |
| 19 | „zone 19 contains **23** embossed discs featuring **six** circles (No. 15)" | 23 | 15 | 6 | **138** |
| 20 | „zone 20, containing **54** small embossed discs (No. 8) framed by **three** circles" | 54 | 8 | 3 | **162** |
| 21 | „zone 21 follows with **47** bosses featuring **five** circles (No. 14)" | 47 | 14 | 5 | **235** |
| | | | | **total** | **1783** ✅ |

Derived totals, computed from the 21 rows above (asserted in §12):

```
Σ discs, all 21 zones                        = 440
Σ discs, zones {3,4,6..21}  (excl. 2 and 5)  = 440 − 22 = 418   ← Menghin's "418"
Σ rings, all 21 zones                        = 1783          ← berlin.json total
Σ rings over those 418 discs                 = 1783 − 44 − 38 = 1701  ← Menghin's "1701"
Σ day-values zones 3..21                     = 1739          ← gold_hat.md
```

So `berlin.json` **reproduces exactly** from Menghin's prose, zone by zone, with no fitting: `[0,44,42,75,38,90,57,105,57,95,60,100,60,105,90,38,66,126,138,162,235]`. **This is the strongest single piece of evidence in the plan** — a decode rule (`Σ count × rings`) confirmed on 21 out of 21 zones by four arithmetic identities that were never fitted to each other.

So the decode rule is **`day_value(zone) = Σ (count × rings)`**, with zone 1 (8-rayed star) = 0 and zone 5 = 38 *individual* symbols (19 crescents + 19 eye-symbols). Every zone quoted in the text matches:

| Zone | Menghin's words | Check |
|---|---|---|
| 1 | Höhe 6,1 cm, Basisumfang 16,6 cm, achtstrahliger Stern | no countable ring motif → 0 |
| 2 | 0,85 cm; „**22** circular punches featuring **two** rings (No. 6)" | 22 × 2 = **44** ✅ |
| 3 | 1,4 cm; „**14** encircling bossed discs, each with **three** concentric circles (No. 8)" | 14 × 3 = **42** ✅ |
| 4 | 2,2 cm; „**15** small bosses with **five** concentric circles (No. 10)" | 15 × 5 = **75** ✅ |
| 5 | 2,45 cm; „**19** horizontal crescent shapes with a central dot (No. 16), and beneath them, an equal number of almond-shaped eye symbols (No. 17)"; lower-edge circumference **27.5 cm** | 19 + 19 = **38** ✅; circumference anchor ✅ |
| 6 | „**18** bossed discs featuring **five** rings (No. 10)" | 18 × 5 = **90** ✅ |
| 7 | „**19** discs with **three** circles (No. 11)" | 19 × 3 = **57** ✅ |
| 8 | „**21** small bumps with **five** circles (No. 10), identical to those in Zones 4 and 6" | 21 × 5 = **105** ✅ |
| 9 | „**19** large bumps with **three** circles (No. 12)"; circumference **34,9 cm** | 19 × 3 = **57** ✅; circumference anchor ✅ |
| 15 | „**15** bosses featuring **six** concentric circles (No. 15)" | 15 × 6 = **90** ✅ |
| 16 | „1,9 cm … **19** shallow boss-discs featuring **two** rings (No. 13)" | 19 × 2 = **38** ✅ |
| 17 | „1,5 cm wide … **33** small bosses featuring **two** circles (No. 9)" | 33 × 2 = **66** ✅ |
| 18 | „zone 18 contains **21** … embossed discs featuring **six** circles (No. 15)" | 21 × 6 = **126** ✅ |
| 19 | „zone 19 contains **23** … embossed discs featuring **six** circles (No. 15)" | 23 × 6 = **138** ✅ |
| 20 | „zone 20, containing **54** small embossed discs (No. 8) framed by **three** circles … identical to the one found at the top of the shaft in zone 3" | 54 × 3 = **162** ✅ |
| 21 | „zone 21 follows with **47** bosses featuring **five** circles (No. 14) … the same pattern punch as those in zones 10, 12, and 14" | 47 × 5 = **235** ✅ |
| 10/12/14 | „identical to those found in Zones 9 and 11" / „identical to that of Zones 10 and 12" (= 5-ring No. 14) | 19×5=95, 20×5=100, 21×5=**105** ✅ |
| 11/13 | „identical to those found in Zones 9 and 11" (= 3-ring No. 12) | 20×3=60, 20×3=**60** ✅ |

**Menghin's zone widths match `dimensions.txt` too:** 0,85 / 1,4 / 2,2 / **2,45** / **2,5** / 2,9 / 3,4 / 1,9 / 1,5 / 3,8 cm ↔ z2=8.5, z3=14, z4=22, z5=24.5, z6=25, z7=29, z9=34, z16=19, z17=15, z15=38 mm — **ten independent hits, including the odd 24.5 mm.** `dimensions.txt`'s **zone heights are a transcription of Menghin's own numbers**; its `tb*` rows are the Kerbwülste/Trennbänder, which Menghin's zone widths do *not* include (as his own closing sentence says: the canon is organised „by 18 bands of notched ridges **and** five bands featuring dots").

**`berlin.json` is confirmed ground truth for Menghin.**

```
zones 3..21             = 1739   ← 418 discs' 1701 rings + zone 5's 38 special signs
intercalary 7 + 16 + 17 =  161   ← the three once-only DISC stamps (Nr. 11/13/9)
```

⚠️ **Correction — Menghin pp. 47–63 (added later) supersede the intercalary reading above.** An earlier draft here carried `intercalary 5 + 16 + 17 = 142 → 1597`, taken from `gold_hat.md`. That is wrong on the **zone set**: the intercalary ("Schalt") zones are the zones whose *disc* stamp occurs exactly once in the canon — Nr. 11 in zone 7, Nr. 13 in zone 16, Nr. 9 in zone 17 (independently asserted by `verify_calendar.check_tools_used_once`). **Zone 5 is not a single-use *disc* stamp**: it carries the 38 *special signs* (recumbent crescent + eye, tools Nr. 16/17, 2 × 19) that are counted separately and never enter the 418/1701 disc totals. ⚠️ Its status is itself unstable in Menghin's own corpus: pp. 47's running text and the earlier Menghin (2000, *Acta Praehistorica* 32 — see the Wikipedia transcript) group it with the *Schaltzonen* (`{5,7,16,17}`, giving the 54-month example `1739 − 142 = 1597`), while the 2010 Figs 61.1–64.4 colour only **{7,16,17}** green and place zone 5 inside the red solar blocks. See `MENGHIN_HYPOTHESIS.md` §6, Result 4. This is not a bookkeeping detail: the intercalary set is the free parameter that makes the arithmetic close, so its instability is a real weakness of the hypothesis. The `1597`/54-lunation example came from the earlier `gold_hat.md` summary and does **not** occur in pp. 47–63, which instead read the 19 zones as **1739 ≈ 1735 d** (57 solar months / 19 quarter-years) or **1742 d** (59 lunations); §10.1. The plan keeps the *derived* identity `1739 = 1701 + 38` as the hard test, not the interpretive period.

**Tool catalogue — all 24 punches.** Menghin's Fig. 21 legend (`text/menghin_page27.txt`) gives the full set; the eight disc bosses (Nos. 8–15) are the ones that carry the calendar arithmetic, and the legend fixes their size, which is what the motif primitives must scale to (§6.2):

| No. | Motif | Rings | ⌀ | Used in |
|---|---|---|---|---|
| 4 | beaded dot (Perlpunkt) | — | — | filler bands throughout |
| 5 | dot-in-circle (Punktkreis) | — | — | filler, cap top |
| 6 | dot-in-double-circle (Doppelkreispunkt) | 2 | — | z2 (22), and interstices of z15, z18, z19 |
| 7 | annulet / ring-within-circle (Ringkreis) | — | — | interstices z9–14, z16; bands at z9-bottom, z10-top, z11, z21 |
| **8** | 3 circles | 3 | **12 mm** | z3 (14), z20 (54) |
| **9** | 2 circles | 2 | **12 mm** | z17 (33) |
| **10** | 5 circles | 5 | **13 mm** | z4 (15), z6 (18), z8 (21) |
| **11** | 3 circles | 3 | **14 mm** | z7 (19) |
| **12** | 3 circles | 3 | **15 mm** | z9 (19), z11 (20), z13 (20) |
| **13** | 2 circles | 2 | **15 mm** | z16 (19) |
| **14** | 5 circles | 5 | **15 mm** | z10 (19), z12 (20), z14 (21), z21 (47) |
| **15** | 6 circles | 6 | **21 mm** | z15 (15), z18 (21), z19 (23) |
| 16 | horizontal crescent + central dot | — | 11 mm long | z5 (19) |
| 17 | eye / almond | — | 11 mm long | z5 (19) |
| — | 8-rayed star on dotted triangles | — | — | z1 |

Ring counts are **{2, 3, 5, 6} — never 4**, exactly as Menghin says („featuring two, three, five, or six concentric rings"). Nos. 9, 11 and 13 appear in exactly **one** zone each — which is what Menghin's Fig. 23 key means by „Disc symbols appearing **only once** in the ornamental canon: Green" (`text/menghin_page30.txt`), a third independent check on the per-zone table above.
Its byte-identical duplicate `berlin_meghin.json` has been deleted (it was referenced nowhere).

### 2.2 The sectioned profile — **derived from Menghin** ✅ *(Q5 resolved by this section)*

Menghin describes the Berlin hat as **four** sections — „the apex, the conical shaft, the helmet-like cap, and the brim" (`text/menghin_page27.txt`) — and — this is the part the earlier draft of this plan did not have — he gives the diameter of **every** transition between them. All figures below are quoted from the **human transcription** `assets/menghin/text/menghin_page*.txt` (Appendix C), which is authoritative over the machine OCR;

| Transition | Menghin, verbatim | ⌀ | z |
|---|---|---|---|
| Tip (Spitze) base = zone 1 | „The apex … measures **6.1 cm** in height and has a basal circumference of **16.6 cm**" | 52.8 mm | 61 mm |
| Zone 5 lower edge | „The circumference of the cone at the lower edge of this zone is **27.5 cm**" | 87.5 mm | 160 mm |
| Zone 9 (mid-shaft) | „…arranged on the shaft and has a circumference of **34.9 cm**" | 111.1 mm | ≈312 mm |
| Notched collar below zone 12 | „The circumference of the shaft, measured at the notched collar below, is **37.1 cm**" | 118.1 mm | ≈445 mm |
| **Schaft maximum** | „the roughly conical **shaft (with a maximum diameter of 125 mm)**" | **125 mm** | ≈510 mm |
| **Schaftfuß** | „The lower section of the shaft—which has a diameter of **10.8 cm** at the base" | **108 mm** | 611 mm |
| cuff, bottom → top | „separated from the crown by an **18 mm high, vertically pleated** transition zone" | 108 → **127 mm** | 611 → 629 |
| **Kalottenfuß** = Krempenansatz | „A bronze band—approximately **10 mm high and measuring 203 mm by 175 mm in diameter**—is located in the fold between the base of the crown and the brim." | **189 mm** (oval) | 738 mm |
| **Krempenrand** | „the slightly deformed **horizontal brim (outer dimensions 307 mm by 295 mm)**" | **301 mm** (oval) | 745 mm |

The four circumference anchors (A z=61, B z=160, D z=312, C z=445) are *independent measurements of the same profile*; A–B–C were known before, **D is new** and it lands within 2 mm of the curve A–B–C already implied at z=312 (predicts 111.6 mm, measures 111.1 mm). That is four-for-four on a profile nothing was fitted to.

Menghin's own summary of the three body sections is „Schaft, Kalotte und [Krempe sind] durch auffällige Trennbänder in drei Abschnitte … gegliedert", and the sections are of very different shape:

| Section | Content | Shape | Half-angle from vertical |
|---|---|---|---|
| **Schaft** | zones 1–16 | long, gently *concave* frustum — ⌀ 53 → 125 → 108; the ⌀108 foot is *not* a mid-shaft waist, it is a tuck-in over the last 100 mm | **+23.4°** at the apex → **+9.9°** → **+4.4°** → **+1.5°** (z≈375, flattest) → **+3.0°** → **−4.8°** at the foot |
| **cuff** | 18 mm, between z16 and z17 | **strongly flared**, `vertikal gefältelt`; ⌀ 108 → 127 | **≈27.8°** *as a chord* (611→629) — see the correction below |
| **Kalotte** | zones 17–19, „100 mm hohe Kalotte" | flared helmet/dome, ⌀ 127 → 189 | **≈15.9°** *as a chord* (629→738) |
| **Krempe** | zones 20–21, „52–55 mm schmale **horizontale** Krempe" | near-flat annular brim, ⌀ 189 → 301, seen from above concave | **7.1°** from horizontal |

The **18 mm cuff is the key to the whole upper profile**: Menghin calls it `vertikal gefältelt` (vertically pleated) precisely *because* pleating is how a ⌀108 neck opens into a ⌀189 dome in 18 mm of height. It is not a decorative ring — it is the flare. §"Do the motif counts fit" below shows that this flare is not merely plausible but *forced* by Menghin's own motif counts.

**⚠️ Menghin's „three sections of seven zones" is a *different* partition from his four physical sections.** Both are real and both must be modelled as data, because they are offset from each other:

| Partition | Groups |
|---|---|
| **physical** (§2.2) | apex 1–2 · Schaft 3–16 · Kalotte 17–19 · Krempe 20–21 |
| **ornamental** – „divided into three sections—each comprising seven zones—by distinctive bands" | 1–7 · 8–14 · **15–21** |

The third ornamental group straddles the boundary: „the two zones at the base of the shaft (above the cap) overlap with the five zones located on the brim and the cap itself" — i.e. z15+z16 (shaft) + z17–z21 (cap+brim) = 7. Menghin's closing remark is the point of the whole object: the canon „only partially aligns with the formal structural division of the object as a whole" (`text/menghin_page31.txt`). **Stage-2 consequence:** the two partitions are two different, equally defensible lighting scenarios (§10) — the physical one for the form, the ornamental 7+7+7 one for the counting system. Do not hard-code either.

**Four consequences, each of which changes the plan:**

1. **The object is not a straight cone.** Four circumference anchors are now available and they are *strongly* non-linear: the local diameter growth is **+0.351** mm/mm between z=61 and z=160, **+0.155** between z=160 and z=312, **+0.053** between z=312 and z=445, up to the maximum at ≈510, and then **−0.167** (the shaft narrows) down to the Schaftfuß. A straight-line fit through any two anchors mis-predicts everything below the second one. The profile is therefore stored as a **piecewise list of `(z, r)` control points** (§5.1) — never a slope constant. This is now mandatory, not merely prudent.
   *Honest caveat:* the new zone-9 anchor (34.9 cm) makes the middle of the shaft very nearly straight and puts the curvature change at z≈312. A ±2 mm reading error on 34.9 cm would remove most of that kink, so the z=312 control point carries that reading error. It does not affect any zone boundary. **P1 update:** the photo's tilted projection puts z=312 within **1.2 mm** of the planned value, so the kink is corroborated rather than merely assumed — see §6.1.
2. **The widest point is the Krempenrand, ⌀ 301 mm**, and it is a *near-flat annulus* at the very bottom of the object. `dimensions.txt`'s „20 cm **at its widest point**" is 100 mm too small and stays unreliable; but it is at least measuring the right *feature* (the brim is the widest point, not the base of the cone).
3. **The Schaftfuß (⌀108) is narrower than the Schaft maximum (⌀125).** The profile widens monotonically from the apex all the way to ⌀125 at z≈510, then tucks in by 8.5 mm of radius over the last 100 mm of shaft. Part of the 108 mm vs 125 mm gap is certainly Menghin measuring an „annähernd oval" cross-section along different axes (Abb. 18: „dass die Öffnung der Kalotte nicht rund, sondern annähernd oval war"); part is the concave profile. Modelled as a **monotone narrowing**, not a hump: the plan does *not* claim a mid-shaft waist, which nothing in Menghin supports.
4. **Zones 20 and 21 have essentially no stacked height** — they are *concentric rings on a horizontal plate*, not stacked bands. This is what resolves Q2 (below), and it means the Stage-1 deliverable is **19 stackable bands + 1 flat Krempe plate**, not 21 stacked bands.

**Resulting profile** (control points for `data/hat_parameters.json`):

| z (mm) | ⌀ (mm) | radius (mm) | note |
|---|---|---|---|
| 0 | 0 | 0.0 | apex (nominal) |
| 61 | 52.8 | 26.42 | Menghin A |
| 160 | 87.5 | 43.77 | Menghin B |
| 312 | 111.1 | 55.55 | **Menghin D (zone 9), 34.9 cm** |
| 445 | 118.1 | 59.05 | Menghin C, 37.1 cm |
| 510 | 125.0 | 62.50 | Schaft max — widest point of the shaft |
| 611 | 108.0 | 54.00 | Schaftfuß |
| 629 | 127.0 | 63.50 | top of the cuff = bottom of the Kalotte. **Set by the motif load, see below** |
| 738 | 189.0 | 94.50 | Kalottenfuß / bronze band — the Krempe starts here |
| 745 | 301.0 | 150.50 | Krempenrand — widest point of the object |

Note `r(629) = 63.5` rather than the 56.0 a naive read of „Schaftfuß 108 mm → Kalotte 189 mm" would give: the cuff's *top* diameter is not stated by Menghin, and it is over-determined by the zone-17 motif pitch (next section). 63.5 mm is the value the ornament requires.

**Height budget — it closes on `745.000` exactly, with no spacers:**

The zone widths and the section heights are now *over-determined*, so the Kalotte/Krempe split is decided by which reading honours Menghin's **stated zone widths**:

| Section | Source | mm | cumulative z |
|---|---|---|---|
| Spitze + Schaft | `dimensions.txt` z1…z16 + tb1…tb16 — and **every** zone width is independently confirmed by Menghin's own cm values (0,85 / 1,4 / 2,2 / 2,45 / 2,9 / 3,4 / 1,9 / 1,5 / 3,8 cm) | **611** | 611 |
| pleated cuff | Menghin: „an **18 mm high**, vertically pleated transition zone" | **18** | 629 |
| Kalotte | Menghin's zone widths: z17 (1,5) + tb (0,9) + z18 (3,8) + tb (0,9) + z19 (3,8) = **109** | **109** | 738 |
| Krempe | residual: 56 mm *radial* (52–55 mm plate + rim), risen 7 mm ⇒ **7,1°** from horizontal | **7** | **745** |

Two readings of Menghin's own numbers give the **same 116 mm** for Kalotte + Krempe but split it differently:

| Reading | Split | Sum | vs 745 |
|---|---|---|---|
| **adopted** — his stated *zone widths* (15 / 38 / 38 mm) + two 9 mm separator bands | 109 (Kalotte) + 7 (Krempe) | 611+18+109+7 | **745, exact** |
| his *rounded* section figure „the **100 mm high** crown" | 100 + 16 | 611+18+100+16 | 745, exact |

They agree because `109 + 7 = 100 + 16 = 116`. The first is adopted because the 109 mm comes from Menghin's own per-zone widths, whereas „100 mm" is a round number that is 9 mm — exactly one separator band — short of them.

**And the whole table closes in one line**, which is the cleanest proof that the 745 mm is not being adjusted to fit:

```
dimensions.txt grand total        = 769 mm   (z1..z19 + tb1..tb19 + 2 x tussenstuk(20))
- 2 x tussenstuk (unattested)     = -40 mm
- tb19       (Krempe starts at 738, no band there)  = -9 mm
+ the 18 mm pleated cuff (Menghin)                  = +18 mm
+ the 7 mm Krempe rise (residual)                   = +7 mm
------------------------------------------------------------
                                    = 745 mm  exact
```

Note also that `z1..z19 + tb1..tb19` alone is **729 mm** — which is exactly the number an earlier draft mistook for the Kalotte foot after subtracting a spurious 16 mm. There is no 16 mm anywhere in Menghin; the 729 is simply the pre-cuff total, and the cuff is what turns it into 745. Either way **`Σ band heights == 745 mm` holds exactly and no `tussenstuk` is needed**; the two spacer rows in `dimensions.txt` are deleted as unattested by any source. `dimensions.txt` is therefore not an independent witness but a *transcription of Menghin's own figures in mm*, which is why every one of its zone widths matches to 0.05 cm.

**The measured silhouette (P1) is no longer required** — it has been run. It cannot supply `r(z)` (the view is tilted: see §6.1) but it does corroborate the documentary curve, so the profile stands on Menghin's nine numbers alone. It never had to decide the *topology* or the total height.

**Cross-checks that this shape is real, not an OCR artefact:**

- **Circumferences vs. motif counts — this is the strongest evidence in the plan.** Menghin states the motifs never overlap („The arrangement ensures there is no overlap between the disc and circular motifs"), so every zone needs `circumference ≥ count × tool ⌀`. Running all 19 disc zones against the profile above: **every one fits**, and the two tightest (z17 and z18, at the top of the cap) come out at **+3.0 mm and +0.9 mm** margin. That is not a coincidence to be admired, it is a *constraint that fixes the profile*: given Menghin's zone-17 count (33 × ⌀12) and zone-18 count (21 × ⌀21), the cuff **must** flare to ⌀127 by z=629, and it must do so within 18 mm. So the ⌀127 adopted above is not a guess — it is the value Menghin's ornament demands, and it independently corroborates both the 18 mm cuff and the „⌀108 → ⌀189" jump. Details in the table below.
- **Two independent photos** were measured programmatically (`scripts/measure_silhouette.py`, PIL+numpy). Both show a **hard flare in the last ~10 % of the height** — the widest point is at the very bottom — matching „horizontale Krempe mit Außenmaß 307 × 295 mm". The photos were then taken further than that: see §6.1 for the tilt-recovered *forward check*, which puts the ⌀301 Krempenrand within 0.3 mm and the mid-shaft z=312 within 1.2 mm, and which is also what proves neither image can be used as a *source* for `r(z)`.
- **Mass/foil cross-check.** Menghin: „The average wall thickness is **0.06 mm**", weight „only **490 g**". A 0.06 mm shell of 0.292 m² of gold at 19.3 g/cm³ is ≈ **338 g** — same order, the remaining 150 g being the bronze hoop in the Falz, the twisted rim wire, and the thicker reinforced edges. So the sectioned profile's surface area is consistent with the stated weight; the earlier straight-cone model's 0.35 m² was not.

### 2.3 Printability — **only the Krempe needs splitting**
Tallest band ≈ 38 mm, so height is never a problem. Bed is 256 × 256 mm (a circle does not fit a square bed diagonally: the largest inscribable circle is ⌀256). With the profile from §2.2:

| Section | max ⌀ | fits 256 bed? |
|---|---|---|
| Schaft (zones 1–16) | 125 mm | ✅ with room to spare |
| Kalotte (zones 17–19, after the cuff) | 189 mm | ✅ |
| **Krempe (zones 20–21)** | **301 mm** | ❌ **must be split** |

So the earlier draft's "split the bottom 2–4 stacked bands" is wrong and over-cautious: **every stacked band fits as-is.** Only the flat Krempe plate is too big.

Options for the Krempe, cheapest first:

1. **Split the plate into radial sectors.** A 180° half-annulus has a bounding box of 301 × 150 mm — *still* 301 mm in x, so two halves do **not** fit. **Sectors of ≤ 120° do:** a 120° sector of a ⌀301 annulus spans ≈ **226 × 151 mm**, and a 90° sector ≈ 151 × 151 mm. So **3 sectors (recommended)** or 4. Print each sector **flat, in its own plane**, so the through-windows are vertical drillings (ideal for Stage 2) and the overhang is the plate's own **7.1°** rise — no support needed. Join with a tongue-and-groove seam and glue. **Take 3 sectors:** bbox ≈ 226 × 151 mm leaves a comfortable 30 mm margin, and 54 motifs divides cleanly into 18 per sector for zone 20 (zone 21's 47 becomes 16/16/15).
2. Print the Krempe as an equivalent *cone* section standing on edge with the rest of the hat — worse: it becomes a large unsupported horizontal annulus. Discard.
3. Scale to 0.85 — violates 1:1. Discard.

Result: **22 STL files** = zones 1–19 (19 files) + `krempe_a/b/c` (3 files). The band schema gains an optional `split` field but no stacked band uses it, so the z13/z14/z15 test print is unaffected.

---

## 3. Discrepancies and open questions

### Q1 — `dimensions.md` does not exist — ✅ **FIXED** (doc fix)
`AGENTS.md` references `dimensions.md`; the repo has `dimensions.txt`. Rename one or the other. Low cost, do it first so future readers aren't sent to a missing file.

### Q2 — The height table over-sums the total height by 24 mm — **RESOLVED** ✅
Summing every zone + Trennband + both `tussenstuk` entries in `dimensions.txt` (z1…z19) gives **769 mm**, not 745 mm. There is **−24 mm left** for z20, tb20 and z21. The table itself is not wrong; the *model* of what z20/z21 are was.
**Resolved from Menghin (primary source — human transcription, Appendix C):**
1. `z1 = 61 mm` is **correct and is the crown zone alone** — „Die Spitze des Goldhutes hat eine Höhe von **6,1 cm** und einen Basisumfang von **16,6 cm**." Do not add anything.
2. The **zone heights are Menghin's own** numbers (0,85 / 1,4 / 2,2 / **2,45** / **2,5** / 2,9 / 3,4 / 1,9 / 1,5 / **3,8** cm all verify). So the zone column is not the suspect part. Note the OCR trap: the first pass read zone 5 as „2,5 cm" and „i: 5 cm"; the clean crop read gives **2,45 cm**, exactly `dimensions.txt`'s 24.5 mm. **Ten independent hits**, including the odd 24.5 mm.
3. `tb* = 7…9 mm` are the **Kerbwülste / Trennbänder**; Menghin's zone widths exclude them, so they are genuinely *additional* height — do not delete them. Menghin confirms their existence and rough size in his closing sentence („18 bands of notched ridges and five bands featuring dots, dotted circles, double-circle dots, and ring-and-dot motifs", `text/menghin_page31.txt`). They set the Z-origin of every band above them, but they no longer change the *total* height — the 745 budget absorbs all sixteen of them (§2.2); earlier drafts treated them as free parameters, which was the mistake.
4. Menghin's „**19 zones (excluding the tip)**" is now fully resolved and is **not** a 19-vs-18 discrepancy: the „tip" is zones **1 + 2** together („Zone 2 … is also considered part of the apex"), leaving zones **3–21** = **19 zones**. And his other count, „**18 horizontal zones**" (`text/menghin_page25.txt`), is the **18 disc-bearing** zones — 21 total minus {1 star, 2 double-circles, 5 specials} = 18, which is exactly what he says in the closing sentence of p31. **Both numbers are right; they count different things.** The plan's earlier flag of this as a source inconsistency was wrong.
5. Menghin says nothing about the two `tussenstuk` (spacer) parts. They are **not attested** by any source — prior-attempt invention. Dropping both frees **40 mm**, i.e. more than the deficit.
6. **RESOLVED — see §2.2.** Zones 20–21 sit on the **Krempe**, which Menghin measures as „**52–55 mm schmale horizontale** Krempe" with an outer size of 307 × 295 mm. It is a *horizontal plate*, so zones 20 and 21 consume radial width, not height; their stacked height is ≈0 (the plan carries the 7 mm residual left by the 745 mm budget). That is exactly why `dimensions.txt` lists z20/z21 with no height: they are concentric rings on the brim, not stacked bands.

The height budget therefore closes as **611 (Schaft) + 18 (pleated cuff) + 109 (Kalotte, from Menghin's own zone widths 15+38+38 and two 9 mm bands) + 7 (Krempe rise) = 745 mm exactly**, with the two unattested `tussenstuk` rows deleted and nothing else cut (§2.2). Menghin's rounded section figures give the same 745 with a `100 + 16` split; the two agree because `109 + 7 = 100 + 16 = 116`. Q2 is **closed** — and it is closed by *Menghin's numbers*, not by adjusting the table.

### Q3 — Symbol count: 651, 1783, or "over 3000"? — **RESOLVED** ✅
Four different numbers were circulating. Menghin's text disambiguates all of them; they are four *different* counts of four *different* things:

| Number | What it actually counts | Source |
|---|---|---|
| **418** | disc bosses (Buckelscheiben, tools Nr. 8–15) over the 18 disc-bearing zones, excluding the star, zone 2's double-circles and zone 5's special signs | Menghin; **fully derived zone-by-zone in §2.1** ✅ |
| **1701** | concentric rings summed over those 418 bosses | Menghin; **fully derived in §2.1**: `1783 − 44 − 38` ✅ |
| **1783** | Menghin's **day-value** sum = Σ(count × rings) over all 21 zones | derived from Menghin's prose (§2.1), and independently matched by `reference/m5/data/berlin.json` |
| **~651** | *all* punched ornaments incl. the small filler punches (Perlpunkte, Punktkreise, Ringkreise) and the radial spandrel patterns | Schmidt-Kaler's per-zone table |
| ~~~3,393~~ | **not a count of anything.** No per-zone table in the repo sums to it and Menghin contradicts it. Treat as garbled. | `gold_hat.md` (Wikipedia-derived) |

**Consequence for Stage 2:** the physical main motifs are ~480 (418 bosses + 22 double-circle punches + 38 special signs + star), reaching ~650 only if every filler punch also gets an LED. Worst case **~650 LEDs ≈ 5 A** at full white, not 3,393 / 61 A. The `gold_hat_scenarios.md` power budget is wrong by ~6× — and it is no longer a constraint on the LED design.

**How many LEDs to actually fit:** the design target is **one light per main motif** (~480), which is also what Menghin's own counting supports. Fillers can be left unlit or lit as a low-current background.

See Appendix C for the zone-by-zone citations.

### Q4 — Which scholarly reading drives the demo? — **[Stage 2 — open, does not block geometry]**
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

**Residual uncertainty (not blocking):** the *intermediate* shape of the Schaft between the four circumference anchors — that is, the `pchip` segments themselves, which are interpolations and not measurements. **P1 (see §6.1) sized this error**: the photo's tilted projection agrees with the curve to **1.6–2.5 mm RMS in radius** through the shaft, i.e. the interpolation is not doing anything the photo contradicts. The topology, all four circumference anchors, all five section diameters, the cuff flare and the 745 mm total are **all fixed by Menghin**. The 108-vs-125 question is answered: „10.8 cm at the base" (p22) is the **foot**, „maximum 125 mm" (p25) is at ≈z=510 — two different heights, not a contradiction. **One local disagreement remains, deliberately kept unfixed:** the cuff / Kalotte base at z≈600–640, where the photo reads ~⌀119 against the documented ⌀108 → ⌀127. That is a cuff-*shape* question for P3, not an `r(z)` question, and the documentary numbers win until the cuff is modelled.

### Do the motif counts fit the sectioned profile?
Menghin states the motifs never overlap („The arrangement ensures there is no overlap between the disc and circular motifs") and gives each tool's outer ⌀ (§6.2). So for any zone: `circumference ≥ count × ⌀`.

**All 19 disc zones pass; the two tightest land on exact tangency.** Using the §2.2 profile (so the cuff now flares 108 → 127 mm):

| Zone | z range (mm, from apex) | count × ⌀ | need ≥ | min circumference in zone | margin |
|---|---|---|---|---|---|
| 3 | 83.5 – 97.5 | 14 × 12 | 168 | 190.8 | +22.8 |
| 4 | 105.5 – 127.5 | 15 × 13 | 195 | 215.0 | +20.0 |
| 5 | 135.5 – 160.0 | 19 × 11 ×2 rows | 209 | 248.1 | +39.1 |
| 6 | 168.0 – 193.0 | 18 × 13 | 234 | 278.9 | +44.9 |
| 7 | 202.0 – 231.0 | 19 × 14 | 266 | 295.5 | +29.5 |
| 8 | 240.0 – 269.0 | 21 × 13 | 273 | 314.0 | +41.0 |
| 9 | 278.0 – 312.0 | 19 × 15 | 285 | 332.5 | +47.5 |
| 10 | 321.0 – 355.0 | 19 × 15 | 285 | 350.5 | +65.5 |
| 11 | 364.0 – 398.0 | 20 × 15 | 300 | 357.6 | +57.6 |
| 12 | 407.0 – 441.0 | 20 × 15 | 300 | 364.7 | +64.7 |
| 13 | 450.0 – 484.0 | 20 × 15 | 300 | 372.7 | +72.7 |
| 14 | 493.0 – 527.0 | 21 × 15 | 315 | 383.7 | +68.7 |
| 15 | 536.0 – 574.0 | 15 × 21 | 315 | 358.9 | +43.9 |
| 16 | 583.0 – 602.0 | 19 × 15 | 285 | 344.1 | +59.1 |
| **17** | 629.0 – 644.0 | 33 × 12 | **396** | **399.0** | **+3.0 → tangent** |
| **18** | 653.0 – 691.0 | 21 × 21 | **441** | **441.9** | **+0.9 → tangent** |
| 19 | 700.0 – 738.0 | 23 × 21 | 483 | 525.9 | +42.9 |
| 20 (Krempe, inner ring, r≈107) | 738 → 745 | 54 × 12 | 648 | 672.3 | +24.3 |
| 21 (Krempe, outer ring, r≈132) | 738 → 745 | 47 × 15 | 705 | 829.4 | +124.4 |
| rim bead + plate edge | r 144.5 – 150.5 | — | — | 56 mm radial (25+25+6) | ✓ matches „52–55 mm" |

**Zones 17 and 18 landing on near-exact tangency is a strong cross-validation, not a problem.** Menghin's motif counts and Menghin's diameters were measured independently — one by counting punches, the other with callipers — and they meet at **+3.0 mm and +0.9 mm**. A profile that was too narrow at the cuff would leave zone 18 impossible (21 bosses of ⌀21 mm need 441 mm of circumference and there is nowhere else to put them); a profile that was too wide would contradict the „52–55 mm" brim and the 307 × 295 mm outer measure. **The flare Menghin's motif counts require is exactly the flare his diameters give.** Menghin himself states the correlation as a design principle: „The width of the decorative bands and the number and size of the disc symbols are clearly correlated with the shaft's circumference at any given point" (`text/menghin_page31.txt`) — the pitch check is therefore a *test of our reading of his numbers*, and it passes.

The earlier draft's ⚠️ on zone 17 („33 × 15 mm — tight, needs ≥495 mm") was itself an error: Fig. 21 gives **Nr. 9 = 2 circles, ⌀12 mm** — not ⌀15. Re-reading the tool legend off `text/` (rather than the OCR, which had merged No. 9 with No. 13) turns a 20 % shortfall into a 1 % margin. **This is exactly the class of error the human transcription tier exists to kill** — see Appendix C.

The „alternating 3-and-5-ring rhythm, strictly maintained up to Zone 14" (Menghin, p31) is visible in the table above as the ring-count column **3, 5, 5, 3, 5, 3, 5, 3, 5, 3, 5** over zones 3–14 — alternating from zone 7 onward — with the jump to **six** rings at zone 15 ending it. That is his correlation rule operating as a design constraint, and it is why the tool ⌀ grows monotonically (12 → 13 → 14 → 15 mm) before the ⌀21 jump.

**Interim decision (unchanged):** build and print **z13 + z14 + z15** (§11 P3) regardless — all three are unambiguously mid-Schaft, so no part of this discussion can affect them.

---

## 4. Architecture of the model

```
                    ┌──────────────────────────────┐
   top of hat  z1   │  zone 19 … zone 1, stacked       │
                    │  + 18 Trennband lips + 1 cuff    │
                    │  + the flat Krempe (3 sectors)   │
                    └──────────────────────────────┘
        one STL per band, printed axis-vertical, stacked
```

**Decomposition** — 21 decorative zones. Of these, **zones 1–19 are stacked bands** (each carrying its Trennband as a fused lip) and **zones 20–21 are two concentric motif rings on the single flat Krempe plate**. The 18 Trennbands of `dimensions.txt` (`tb1`…`tb18`) are fused as lips; the `tb19` row and the two unattested spacers are dropped (§3 Q2) — and the 745 mm budget confirms that `tb17` and `tb18` *are* needed while `tb19` is *not*, since zone 19 ends exactly where the Krempe begins.

**Assembly unit — ✅ CONFIRMED: Option A, 22 files.** The requirement says "each band = one STL"; the two candidate readings were:

| Option | STL count | Pros | Cons |
|---|---|---|---|
| **A — ✅ CHOSEN** | **22** — 19 stacked bands (z01…z19, each with its Trennband fused as a lip at the band's lower edge) + 3 Krempe sectors | fewest joints, fewest files, Trennband is a *relief* not a load-bearing ring, better stacking accuracy; the Krempe is a genuinely separate plate anyway (§2.3) | Trennband cannot be swapped/adjusted independently; 2 glued Krempe seams |
| B — rejected | 40+ — zone and Trennband separate | matches `dimensions.txt` 1:1; Trennband colour/finish can differ | 40 joints × tolerance stack; 40 print jobs |

Re-open only if the Trennbands turn out to need a different colour or material — and even then the cheapest fix is to print the *lip* in a second filament on the same machine, not to split the parts.

---

## 5. Geometry model

### 5.1 Parameters (one JSON file, `data/hat_parameters.json`)
```jsonc
{
  "height_total_mm": 745.0,
  // The profile is PIECEWISE, from Menghin's four circumference anchors (A z=61,
  // B z=160, D z=312, C z=445) plus the four stated section diameters. A single
  // slope constant is known to be wrong: the growth rate varies 6x along the shaft.
  "profile": [ { "z":   0.0, "r":   0.0 },   // apex (nominal)
               { "z":  61.0, "r":  26.4 },   // Menghin A: tip 61 mm high, base circ 166 mm
               { "z": 160.0, "r":  43.8 },   // Menghin B: zone 5 lower edge, circ 275 mm
               { "z": 312.0, "r":  55.6 },   // Menghin D: zone 9, circ 349 mm  (photo-checked to 1.2 mm, P1)
               { "z": 445.0, "r":  59.1 },   // Menghin C: circ 371 mm below zone 12
               { "z": 510.0, "r":  62.5 },   // Schaft maximum, 125 mm
               { "z": 611.0, "r":  54.0 },   // Schaftfuss, 108 mm  <- tuck-in over the last 100 mm
               { "z": 629.0, "r":  63.5 },   // 18 mm vertically pleated cuff -> bottom of the Kalotte.
                                             //   NOT a guess: forced by zone 17's 33 x 12 mm
                                             //   and zone 18's 21 x 21 mm pitch (see "Do the
                                             //   motif counts fit"); the plate gives 127 mm here.
               { "z": 738.0, "r":  94.5 },   // Kalottenfuss / bronze band, 189 mm
               { "z": 745.0, "r": 150.5 } ], // Krempenrand, 301 mm  <- widest point
  "profile_interp": "pchip",       // monotone piecewise-cubic; NEVER a slope constant
  "zone_boundaries_mm": [ 0, 61, 68, 76.5, 83.5, 97.5, 105.5, 127.5, 135.5, 160, 168,
                          193, 202, 231, 240, 269, 278, 312, 321, 355, 364, 398, 407,
                          441, 450, 484, 493, 527, 536, 574, 583, 602, 611, 629, 644,
                          653, 691, 700, 738, 745 ],
  // 40 boundaries -> 39 intervals = 19 zones + 18 Trennbaender + the 18 mm cuff
  // + the Krempe plate. Derivation in §2.2; `sum(ring heights) == 745.0` is
  // asserted, not assumed.
  "wall_thickness_mm": 2.0,        // NOT 0.06 — the real foil is unprintable
  "wall_thickness_tb_mm": 3.0,     // Trennbands read as a thicker ridge
  "symbol_relief_mm": 0.8,         // emboss/engrave depth        (see §6)
  "motif_form": "TBD",            // "relief" | "window" | "relief_window"
                                    //   NOT a guess and NOT a default: the generator must
                                    //   accept all three from day one, because the choice is
                                    //   deliberately deferred to a physical test (§6.3).
  "registration_lip_mm": 6.0,      // inner lap ring for stacking
  "registration_clearance_mm": 0.25,
  "krempe": { "r_inner_mm": 94.5, "r_outer_mm": 150.5, "z_inner_mm": 738.0,
               "z_outer_mm": 745.0, "sectors": 3,
               "rings": [ { "zone": 20, "r_mid_mm": 107.0 },
                          { "zone": 21, "r_mid_mm": 132.0 } ],
               "rim_bead_r_mm": [ 144.5, 150.5 ] },   // twisted bronze wire, 6 mm
  "rings": [ { "id":"z01", "kind":"zone", "h":61.0 },
             { "id":"tb1", "kind":"trennband", "h":7.0 },
             ... ]
}
```
Each ring stores only `id`, `kind` and `h`; the generator derives `r_top`/`r_bottom` by evaluating the profile, then asserts contiguity (`z_bottom[i] == z_top[i+1]`). That way Q2 is fixed in one place and a profile revision is a data edit.

Expected derived values, asserted by `verify_geometry.py`: surface area ≈ **0.292 m²** (vs 0.385 m² for the superseded straight cone), filament at 2.0 mm ≈ **0.58 L ≈ 0.72 kg** of PLA before subtracting the light windows, and mass consistency with Menghin's stated **490 g** at 0.06 mm gold foil (≈ **338 g** of gold alone, the balance being the bronze hoop, the rim wire, and the reinforced edges).

### 5.2 Band as a solid
Each *stacked* band (zones 1–19, TBs fused as lips) = `outer_frustum/frustum-band − inner offset` (an open ring with a non-linear outer profile), plus:
- a **registration lip**: a 6 mm tall, wall-thickness ring on the inside of the lower edge, sized to slip into the band below (0.25 mm clearance). Axis-vertical printing makes this support-free.
- a **Trennband ridge** at its lower edge (§4 Option A), 1 mm proud, 9 mm tall — the relief that separates zones visually.
- **symbol features** (§6) on the outer surface.

The **Krempe** is a different primitive: `annular_disc(r_inner=94.5, r_outer=150.5, z=738→745)` — a 56 mm radial ribbon rising only 7 mm (7.1°), so it prints flat in its own plane with no supports — with zones 20 and 21 as **concentric** motif rings rather than stacked ones, split into **3 radial sectors** (§2.3). Its two motif rings sit at r ≈ 107 mm (zone 20, 54 × ⌀12 mm, circumference 672 mm) and r ≈ 132 mm (zone 21, 47 × ⌀15 mm, circumference 829 mm), with the twisted bronze rim wire occupying r 144.5–150.5 mm.

### 5.3 Symbol projection — the one non-obvious bit
Do **not** try to bend a flat pattern onto the cone (the prior attempt's unrolled-frustum SVG route, `reference/cad/svg/z04_strip.svg` — an annular sector 795 mm across, which cannot be mapped back onto a cone in FreeCAD without a bend feature).

⚠️ **Correction, measured by `scripts/band_geometry.py` — the steepest wall is NOT the cuff.** The angles in that table are **chords between control points** (dr/dz over a whole segment), and a chord *understates* a locally steep curve. The kernel measures the **local `pchip` derivative**, which is what actually governs overhang, and it disagrees in two places:

| Where | chord (table above) | **local max** | why |
|---|---|---|---|
| cuff, 611–629 | 27.8° | **35.5°** (z≈622) | the curve must leave the ⌀108 foot *and* turn into the Kalotte, so it steepens mid-segment |
| **Kalotte bottom, z→738** | 15.9° | **38.9°** (at z=738) | the pchip must reach ⌀189 *while* the profile is about to turn 83° into the Krempe, so it steepens right at the joint |

**38.9° at z=738 is the steepest wall in the object, and it is not an artefact**: r(z) is monotone to the last control point (max 150.14 at z=744.96, no overshoot), and the 82.9° direction change at z=738 is physical — that is where the Krempe attaches. Consequences: (a) „the cuff is steepest, still 17° under the limit" was **optimistic** — the real margin at z19 is **6.1°**, not 17°; (b) **z18 and z19 are the bands to watch at P5**, not only the cuff; (c) if a future profile revision deepens that corner, z19 is the first band to exceed 45° and need supports. All 39 rings still pass `< 45°`, so the print strategy is unchanged — but the margin is thin and now known rather than assumed.

Instead: for each motif, build a prism in a local frame tangent to the cone at the motif's (θ, z), and boolean it radially. The visible shape on the outer skin is then the correct radial projection — which is exactly what you want for an LED light window anyway. Chord error for a 25 mm motif on a 100 mm radius is 0.8 mm; acceptable for a stylised model, and it shrinks toward the top. Motif placement maths: `r(z)` from the piecewise profile; motif angular pitch `Δθ = 360° / n_zone`. **The tilt must be per-motif, not a global constant**: it runs **+23.4°** at the apex, flattens to **+1.5°** in mid-shaft, turns to **−4.8°** at the foot (the wall leans *inward* there), then jumps to **+27.8°** across the 18 mm cuff and relaxes to **+15.9°** down the Kalotte. A single tilt constant would visibly shear the windows in the apex, the foot, and the cuff — three of the twenty-one zones. For the Krempe, motifs are placed on *concentric circles in a horizontal plane* instead — the prism axis is vertical, i.e. the light windows become drillings, which is the easiest possible LED geometry and a bonus for Stage 2.

---

## 6. Symbol system

### 6.1 Getting the layout — and why neither image is a geometric source (the P1 result)

**P1 is closed.** The profile is Menghin's **nine documentary constraints** with `pchip` between them. Both candidate image routes were measured programmatically (`scripts/measure_silhouette.py`, PIL + numpy) and **both are disqualified as sources for `r(z)`**:

1. **`assets/berliner_goldhut_abrollung.jpg` (648×800) is not a development.** Its foreground width is **constant at 382 px** across the whole shaft (rows 219–655). Over that same span the documentary circumference grows **275 → 392 mm, ×1.43** — and a true development's width *is* the circumference, so it would have to grow ×1.43. It grows ×1.00. It is not an orthographic silhouette either: its width is non-monotone (a dip at rows 136–156, then flat for 400 rows), which no body of revolution with this profile produces. `assets/cone_debug.png` is the *same* 648×800 drawing, so this pair is the prior attempt's debug render, not a scan of the object. **Not used for geometry.**
2. **The museum photo is a 15–16° tilted view, not a front-on elevation.** For a body of revolution a ring of radius `r` at height `z` projects to an *ellipse*, not a row, so the outline at a given row is `max over z of r(z)·sqrt(1 − ((v − z·cos t)/(r(z)·sin t))²)`. Reading `r(z)` straight off it is wrong by up to `r·sin t` ≈ 40 px of vertical smear. The tilt *is* recoverable from the brim alone — the brim half-width fixes the scale (`s = 0.5199 mm/px` at ⌀301) and the apex row to the widest row fixes `t = 15.4°` — and doing so **predicts the brim's lower silhouette edge at row 1507, where the image's foreground genuinely ends** (below it: 1–16 px specks). That out-of-sample hit is what makes the forward check meaningful.

So the photo is used as a **forward check**, never as a source: project the planned `r(z)` through the tilt model and compare with the actual outline. Residual, in **radius** (mm RMS), and at the control heights:

| section | z span | RMS radius |
|---|---|---|
| apex z1 | 0–68 | 3.8 |
| shaft z2–5 | 68–160 | 2.0 |
| shaft z6–9 | 160–312 | **1.6** |
| shaft z10–12 | 312–445 | **2.5** |
| shaft z13–16 | 445–611 | 3.7 |
| cuff / Kalotte base | 611–629 | 3.2 |
| Kalotte z17–19 | 629–738 | 5.2–7.8 (the two resolutions of the same photo disagree by this much) |

and at the control heights, Δ = photo − planned, in **radius**: z=61 **−2.3**, z=160 −1.9, **z=312 −1.2**, z=445 +0.2, z=510 −3.0, z=611 +4.7, z=629 −5.2, z=745 **−0.3**. The scale is not a free parameter — it *is* the ⌀301 calibration (widest row 1430 = 579 px × 0.5199 = 301.0 mm), so the agreement at the brim is by construction and the agreement at z=312 is not.

**Two things this photo cannot check, and the plan does not pretend otherwise:** at z=738 the tool reports a *silhouette* radius of 148.3, not the ⌀189 Kalottenfuß's 94.5 — the brim's ellipse masks the cap base completely from this 15.4° view, so the Kalottenfuß is **not** photo-validated and rests on Menghin alone. Likewise the cuff is a step that a full-ring projection cannot represent at all, which is exactly why its ~5 mm disagreement is a *modelling* item for P3 rather than a profile error.

The remaining disagreements are **attributed, not unexplained**:

- **The cuff, z≈600–640.** Menghin's ⌀108 Schaftfuß and ⌀127 Kalotte base against the photo's ~⌀119 silhouette — ~5 mm. A **cuff-shape** question (a stepped/fluted cuff whose documented diameters may be taken across different features). Deferred to P3, where the cuff is modelled. **The documentary values are kept** rather than bent to a segmentation-limited measurement.
- **The apparent ~2 mm narrowing in the upper shaft is not real.** The *same* photograph at 250×494 (`assets/goldhat.jpg`) gives 2.5 / 4.5 / 3.5 mm over the sections where the 800×1581 version gives 2.0 / 1.6 / 2.5 mm. Two resolutions of one image disagreeing by as much as the image disagrees with the profile means **the residual is at the method's noise floor, not the curve's error**. Perspective was tested as the cause and **rejected by the fit** — a 2-parameter `(tilt, camera distance)` fit chose an infinite camera distance.

⚠️ **±2 mm from a photograph is not achievable, and this plan no longer claims it** (the withdrawn criterion is recorded in §12). What the profile needs is the *topology* and the *nine documented numbers*, and those come from Menghin. The photo's job was to catch a gross error; it found none. Do **not** go hunting for a better photograph: `cv2` is not installed and must not be added, and no photograph of a *deformed foil* object will out-resolve Menghin's own caliper readings.

Then read the per-zone motif type + count into `data/zones.json`. **This part is already done** — §2.1 derives all 21 zones' tool, count and ring count from Menghin's own sentences, and `scripts/verify_calendar.py` reproduces his 418 / 1701 / 1783 from them. **Placement is now also done** (`scripts/motifs.py`, `zone_layout()` + `placement self-check`) — and it turned up two things that were not obvious:

**1. There is no „correct" angular phase, and that is now proved rather than assumed.** The shaft disc counts are 14, 15, 18, 19, 21, 19, 19, 20, 20, 20, 21, 15, 19, 33, 21, 23 and **`gcd(...) = 1`**. No rotation makes all zones align, so no phase is privileged — the question the earlier draft left open („start angle per zone and the ornament-group offset") has the answer *it is a declared choice with no geometric content*. The check asserts `gcd == 1`, so if a future count edit ever made all zones commensurate, the plan would be told. The single appearance rule worth encoding is the **stagger**: the Fig. 22 plates show z13 and z14 offset rather than stacked, so each odd zone is shifted by half of its *own* pitch (half a pitch is not a constant angle — it is 12.0° in z15 and 7.8° in z19).

**2. The interstice filler cannot sit on the disc centreline — it has to be lifted into the spandrel.** This was a real geometric finding, not a styling choice. At the discs' mid-height the gap between neighbours is only `pitch − disc ⌀`: in **z9 that is 18.12 − 15 = 3.12 mm**, while the Nr. 7 annulet is **⌀4.85 mm**. It physically does not fit there. The first render made the error obvious — the fillers drew straight through the discs. The fix is `spandrel_offset()`, which solves for the height at which the filler clears both neighbours: with the disc centres `p` apart, a point on the bisector at height `y` is `√((p/2)² + y²)` from either centre, so the filler clears once `y ≥ √((R + r_f)² − (p/2)²)`. That gives a **lift of 2.95 mm (z13) to 9.59 mm (z18)**, and the check asserts the resulting clearance. A close reading of `menghin_page29.jpeg` (Z13) then confirmed the *count* too: it is **two annulets per gap, one above and one below**, in the upper and lower spandrels.

This is a good example of the plan's own rule working: the numbers came from the transcription, the *shape* came from the plate, and the arithmetic that reconciles them is an `assert` in the script rather than a sentence in this document. The Abrollung was not needed for any of it.

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

**Implemented and verified — `scripts/motifs.py` (P2, first half).** All 8 boss discs, the 4 fillers (Nos. 4–7) and the 4 specials (Fig. 21 Nos. 16/17, the eye, the tip star, the notched ridge) are built as **2D (arc-length, height) polygons**, deliberately FreeCAD-free so they are testable and so the same code serves both the band generator and an unrolled development render. `python3 scripts/motifs.py` runs the self-check:

- **the ring rule** — every tool's ring count ∈ {2, 3, 5, 6}; a 4 would fail the assert;
- **every tool the zones use is buildable** — `for_tool()` raises on an unattributed number, so a `zones.json` edit that introduces tool 23 fails loudly rather than silently drawing nothing;
- **the built diameter equals Menghin's stated diameter** for all 8 discs (exact to 1e-6 mm), and the built ring count equals the legend's;
- **printability of the smallest feature.** This one caught a real defect: Nr. 10 packs **5 rings into a ⌀13 disc**, and a fixed 0.45 mm ridge left only a **0.36 mm** trough between rings — below what a 0.4 mm nozzle resolves. The ridge width is now `min(0.45, 0.30 × ring pitch)`, which puts every trough at **0.575–1.912 mm**. ⚠️ This is a **stylisation choice, not a measurement**: the Fig. 22 photo cannot resolve a sub-half-millimetre ridge (an autocorrelation of a phone photo of a printed page returns the ridge repeat and the disc repeat at comparable strength and cannot separate them). The trough width is therefore set by the **printer**, which is the honest constraint, not by a number we cannot read.
- **NO OVERLAP** — Menghin's own stated constraint („The arrangement ensures there is no overlap between the disc and circular motifs"), evaluated on the **pchip** profile rather than a straight cone. **All 19 disc zones clear**, tightest at **z17 +0.6 mm** and **z21 +0.5 mm**.

**The disc-to-pitch ratio is the useful number this produces**, and it is not uniform:

| zones | ratio | reading |
|---|---|---|
| shaft, z3–z16 | **0.79–0.86** | comfortable, ~2.3–4.0 mm gaps |
| z17 (33 × ⌀12) | **0.95** | 0.59 mm gap — saturated |
| z18 (21 × ⌀21) | **0.97** | 0.75 mm gap — saturated |
| z19 (23 × ⌀21) | 0.92 | 1.76 mm gap |
| z20/z21 (brim) | — | 729.9 mm circumference, +1.5 / +0.5 mm |

That saturation at z17/z18 is exactly what §2.2 predicted from the other direction ("the two tightest come out at +3.0 mm and +0.9 mm margin"), and it is why the cuff **must** flare to ⌀127 within 18 mm: Menghin's own ornament counts leave almost no room. The profile and the motif counts constrain each other, which is a far stronger statement than either alone.

**Ring counts are 2, 3, 5 or 6 — never 4.** Menghin: „Hauptzierelemente sind acht verschiedene Scheibenbuckel unterschiedlicher Größe mit **zwei, drei, fünf oder sechs** konzentrischen Ringen." The prior attempt's "symbol 13 = 4 rings" is not attested. Menghin's tool legend gives the diameters the primitives must hit:

| Tool | Rings | ⌀ (Fig. 21 legend) | Zones Menghin attributes explicitly |
|---|---|---|---|
| Nr. 8 | 3 | **12 mm** | 3 (14×), 20 (54×) — „This same decorative stamp appears elsewhere only in Zone 20, on the brim" |
| Nr. 9 | 2 | **12 mm** | 17 (33×) — „this motif appears only once in the decorative repertoire" |
| Nr. 10 | 5 | **13 mm** | 4 (15×), 6 (18×), 8 (21×) — „identical to those in Zones 4 and 6" |
| Nr. 11 | 3 | **14 mm** | 7 (19×) — „a motif found only in this zone" |
| Nr. 12 | 3 | **15 mm** | 9 (19×), 11 (20×), 13 (20×) — „identical to those found in Zones 9 and 11" |
| Nr. 13 | 2 | **15 mm** | 16 (19×) — „a motif that appears only in this zone" |
| Nr. 14 | 5 | **15 mm** | 10 (19×), 12 (20×), 14 (21×), 21 (47×) — „the same pattern punch" |
| Nr. 15 | 6 | **21 mm** | 15 (15×), 18 (21×), 19 (23×) |
| Nr. 4–7 | — | — | Perlpunkt-, Punktkreis-, Doppelkreispunkt-, Ringkreis fillers + radial spandrel patterns |

**All eight diameters are now known** (they were only partly legible in the machine OCR; the transcription supplies the full legend), so the primitives are fully parameterised without any hand measurement: `⌀12/3, ⌀12/2, ⌀13/5, ⌀14/3, ⌀15/3, ⌀15/2, ⌀15/5, ⌀21/6`.

These ⌀ values against the local cone circumference give the motif pitch (≈ `πD / count`), which is a free second check on every per-zone count — and it passes for all 19 zones (see §3, "Do the motif counts fit"). Note also which tools appear in **only one** zone: **Nr. 9 (z17), Nr. 11 (z7), Nr. 13 (z16)** — exactly the three Menghin's Fig. 23 key flags as „Disc symbols appearing **only once** in the ornamental canon: Green". A third independent confirmation of the layout.

### 6.3 Physical form of a motif — **DEFERRED to a physical test**

This is the single decision that ties Stage 1 to Stage 2, and it is the one thing that cannot be settled from the sources. **Decision (operator, this round): do not decide from text — 3D-print one band in each candidate form and look at it.** Leaning **R**, because the requirement is that the symbols are *physically present on the outside and visible with the LEDs off*.

The options are named **R / W / RW** rather than A / B / C, because §4 already uses "Option A/B" for the assembly unit and one namespace collision in a plan is one too many.

| Form | Stage 1 — what you see, LEDs off | Stage 2 — light path | Cost |
|---|---|---|---|
| **R — relief** (`relief`) | closest to the real repoussé: raised discs, raised rings, shadow lines in raking light | **none.** A solid wall has no window; Stage 2 would have to re-cut every band | cheapest possible |
| **W — window** (`window`) | crisp flat silhouette; a hole, not a feature. Reads as a stencil | one LED per window, exactly "LED behind the outer surface behind the symbols" | cheapest possible |
| **RW — relief-carved light channel** (`relief_window`) | **R's look**: the raised profile is still there — what is *cut through* is the recessed field *inside* the motif, so the raised rings and rims stay intact and cast shadow | **W's light path**: the light exits through the motif's own recessed field; the raised parts of the motif become the light *modulators* | same as W. ⚠️ leaves a thin fin where a raised ring borders an open slot — must be measured on the coupon |

**R and W are not two points on a spectrum; they are the two ends of one axis, and RW is the whole reason the axis exists.** RW is what the real object does: a boss is pressed out from *behind*, so the outward relief and the light path are the same feature seen from two sides. Judge RW first.

> On the previous draft's "A = opaque skin + inner translucent diffuser sleeve": that is **not** a Stage-1 form. It is W (or RW) plus a Stage-2 sleeve, and the sleeve can be slipped in later **without reprinting a single band**. It was mis-sorted as a third alternative; a diffuser is an accessory, not a form.

**The test, to be run at P3.5 — exactly three coupons, one band each.**

- **Band: `z15`.** Chosen because it is the worst case for R and the best case for judging: 15 × **tool 15 = ⌀21 mm with 6 rings**, the largest and most layered motif on the object, with tool 7 annulets and tool 6 fillers in the interstices — so **two motif scales** are judged on one coupon at once. The ⌀21 / 6-ring disc is also the family that dominates the object (zones 8–19 are all disc zones), so this tests the typical case, not a corner case. And z15 is already in the P5 fit-test trio, so it prints on a known-good setup with no supports.
- **Three STLs, identical except for the motif form:** `stl/test/z15_relief.stl`, `z15_window.stl`, `z15_relief_window.stl`. Same profile, same placement, same wall — **only the motif form may differ**, or the comparison is worthless.
- **Print them together in one job, in matte PLA (not silk — silk hides exactly the dimensional differences being judged), and the fit-test trio in the same session.** ~10 g each.

**Judge each coupon on these five, in this order.** 1 and 2 are why R is leading; 3 is the fact that decides whether R survives at all.

| # | Question | How | Pass looks like |
|---|---|---|---|
| 1 | Does the motif read with the LEDs off? | daylight, 1 m, and again at 3 m | R and RW: yes. W: a stencil, not a symbol |
| 2 | Does it read *as gold* rather than as a hole? | raking light along the wall, and a finger | R and RW show a profile; W has none |
| 3 | **Does each motif light individually, without bleeding into its neighbours?** | phone torch held *inside* the band, dark room | W and RW: 15 separate lit motifs, dark wall between. **R: nothing lights. This is the one that can eliminate R.** |
| 4 | Is RW's thin fin (raised ring next to an open slot) sound? | flex the coupon; then measure the fin with calipers | no crackling, fin ≥ 0.8 mm, wall still stiff enough to stack |
| 5 | What does it cost? | slicer estimate | recorded, not a tiebreaker |

**Then write the winner into `data/hat_parameters.json` as `motif_form` and delete the two losing coupons.** The generator carries all three forms behind one switch (§5.1) so this costs a data edit, not a code change — and so that the *same* band can be regenerated if the sleeve or the LED layout later argues for a different form.

The 418-boss figure (§3 Q3) plus each boss's Menghin punch diameter (⌀12–21 mm) fixes the per-zone window count and size directly — no counting from scratch needed, and it is form-independent: R, W and RW all place the same motifs at the same coordinates; only the material inside the motif's outline differs.

### 6.4 Are there enough motifs to matter, and enough wall to hold them?

Worth stating before anyone prints a coupon, because it bounds how much this decision can even matter. At ~480 main motifs on ≈0.292 m² of shell (§2.2) that is about **one motif per 6 cm²** — motifs occupy a small fraction of the surface, and the wall between them dominates. Two consequences, both live for W and RW and irrelevant for R:

- keep a **minimum 3 mm ligature** between neighbouring windows, or the wall delaminates at the thinnest point when the band is squeezed onto the one below. This is asserted by `verify_geometry.py` (§12) and is the constraint most likely to force a motif smaller than Menghin's punch diameter — in which case shrink the *window*, not the relief.
- if any single zone's windows exceed ~**40 %** of its own surface, that zone needs **interior ribs** to stop the band ovalising under the lap joint. Zones 10, 12 and 14 (19–21 motifs at ⌀13–15 mm) are the ones to check first; zones 17–19 on the Kalotte are the other candidates, since they add the cuff and bronze-band curvature.
- for **RW**, the raised ring bordering an open slot *is* the ligature in the radial direction, so RW is not automatically weaker than W — but its thinnest section is a fin, not a wall, and that is judgement #4 on the coupon.

---

## 7. Data files

| File | Contents | Status |
|---|---|---|
| `data/hat_parameters.json` | heights, diameters, wall/relief/registration params | ✅ **created** — profile, 40 zone boundaries, 39 rings, the Krempe block. `sum(ring h) == 745.0` asserted |
| `data/symbols.json` | motif catalogue: 8 primitives + 24 tools (Nos. 8–15 = the 8 disc diameters) | ✅ **created** — complete for Nos. 4–17; Nos. 1–3 and 18–24 are marked `unattributed`, not invented |
| `data/zones.json` | per zone: which tool, how many, how many rings, `day_value`, attested `fillers` | ✅ **created** — counts/rings/day-values **derived, not transcribed**; `placement` (start angle, ornament offset) is the still-open part |
| `data/readings/menghin.json` | day-value per zone (verified, §2.1) | ✅ **created** — reproduces `reference/m5/data/berlin.json` exactly |
| `data/readings/schmidt_kaler.json` | ornament count per zone | ✅ **created** — marked *not a day count*, must never be summed with Menghin's |
| `data/scenarios.json` | the 16 Stage-2 lighting blocks (Figs 61.1–64.4): per state, the red/blue/green zone colouring and Menghin's stated solar/lunar day values | ✅ **created** — transcription of Menghin pp. 47–63; see §10.1 |
| `scripts/verify_calendar.py` | asserts every identity above | ✅ **created & passing** — `python3 scripts/verify_calendar.py`, stdlib only, no FreeCAD |
| `scripts/verify_scenarios.py` | checks the scenario colouring + 30 stated zone-sums | ✅ **created & passing** — `python3 scripts/verify_scenarios.py`, stdlib only |

The JSON is the source of truth; this plan's §5.1 block is only its *spec* and is deliberately left as pseudo-JSON (it ends in `... ]`). Edit the files, not the plan, and let `verify_calendar.py` tell you if you broke something.

Note the schema in `data/zones.json` carries **both** the motif count and the ring multiplier per motif, because Menghin's day-value = Σ(count × rings). The prior attempt's schema (`{zone, count, multiplier, special_value}`) is a lossy summary — it collapses a whole zone to one multiplier, which cannot represent zone 12 (20 × symbol-14 with 5 rings **plus** Ringkreis-Nr.‑7 motifs interleaved between them). One level deeper is needed, and that is what `fillers` is for. `data/readings/menghin.json` is a *copy of the derived day-values*, not the input — the input is `zones.json`, and `verify_calendar.py` proves the two agree.

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
| Orientation | axis vertical, band lying flat; **Krempe flat in its own plane** | steepest wall is the 18 mm cuff at **27.8° from vertical** (+23.4° at the apex, −4.8° at the foot, 15.9° down the Kalotte, 7.1° on the Krempe plate) ⇒ all under 45°, so zero overhang and zero supports either way; the registration lip prints inside-free |
| Layer height | 0.16 mm | ~0.6 kg of filament; don't throw resolution away for nothing |
| Walls | 3 loops ≈ 1.6 mm + top/bottom | 2.0 mm nominal wall; symbol windows cut through |
| Material (Stage 1) | matte PLA, bronze/gold silk | reads as gold without paint; **not** silk for fit-test coupons (silk hides dimensional error) |
| Per-band print | 1 at a time; 3 for the Krempe sectors | largest stacked band ⌀189 mm × 38 mm tall; Krempe sector ≈ 226 × 151 mm flat |
| Tolerance | 0.25 mm radial clearance on the lap joint | verify with a 3-band fit test before committing to 19 prints |
| Total | 22 prints, ~0.6 kg incl. windows | |

**Fit test first:** print z13 + z14 + z15 (a plain repeating stretch) 1:1 and check that the stack is straight and the lap joint doesn't wobble. Only then print the rest. The top zone (z1) and the Krempe print last — they are the least forgiving parts and benefit from a calibrated machine.

**Print the motif-form coupons in the same session** (§6.3, P3.5): z15 in all three of `relief` / `window` / `relief_window`, matte PLA, ~10 g each. The fit test and the coupon test are two different asks — one for tolerance, one for looks — but they need the same calibrated machine, so do them together and keep the silk out of both. The coupon verdict is a prerequisite for P4: generating 22 bands before the form is chosen means regenerating them all.

---

## 10. Stage-2 constraints this plan must respect

Nothing below is implemented now; these are the interfaces Stage 1 must leave open.

1. **One light channel per motif** (§6.3) — the motif's recessed field is the channel. **The form (R / W / RW) is deliberately still open**, and `motif_form` in `data/hat_parameters.json` is the single switch. ⚠️ If the coupon test selects **R**, Stage 2 stops working as literally specified ("LED behind the outer surface behind the symbols") — there is no light path at all. R therefore cannot be the answer on its own; if R's *look* wins, the answer is **RW**, and if only R's look plus W's light path are wanted, that is what RW already is.
2. **Interior cavity**: the lap joint leaves a natural annular gap; keep ≥ 8 mm of clear radial depth behind a band so an LED PCB can be slipped in, and leave a **20 × 6 mm cable notch** in each lap lip at a common clock angle (recommend θ = 0°, i.e. the hat's "front"), so a single wiring spine runs up the inside.
3. **Modular Z-addressability**: zones are already separate parts, so per-zone LED segments need no extra geometry.
4. **LED budget** is now **~480 main motifs** (≈5 A), not 3,393 (≈61 A) — §3 Q3 is closed. The `gold_hat_scenarios.md` power budget is wrong by ~6× and must be rewritten, not just revised.
5. **Kalotte/Krempe (Q5) — RESOLVED** (§2.2, §3 Q5). Zones 17–19 are the Kalotte (⌀127→189, 15.9° half-angle) and 20–21 the near-horizontal Krempe (⌀189→301, **7 mm** rise over 56 mm radial, i.e. 7.1°). Both are *easy* for Stage 2: the Kalotte's windows still face radially outward, and the Krempe's windows become vertical drillings in a horizontal plate, so an LED strip can be laid underneath it — that zone pair (54 + 47 motifs) is actually the simplest to light in the whole model.
6. **M5 Core S3 + display** sits outside the hat; plan a base plinth/cradle (a separate later model) that hides the electronics and holds the cone upright. **New constraint from §2.2:** the hat does *not* stand on its own — its contact ring is the Krempenrand at ⌀301 mm, with a hollow interior of ⌀189 behind it (and ⌀108 further up). The cradle must therefore support the Krempe from below, which is convenient: the space under the brim is exactly where the M5, the PSU and the wiring spine can live, invisible from outside.

### 10.1 Stage-2 lighting scenarios are now data (Menghin pp. 47–63)

The scenario system the LEDs will run comes from Menghin (2010) *Zahlensymbolik und Rechensystem*, pp. 47–63, Figs 61.1–64.4 (`assets/menghin/menghin_page60..63.jpeg`). For each of **16 time blocks** (4…19 quarter-years / 12…59 lunations) the figures colour the hat:

| colour | meaning | LED meaning |
|---|---|---|
| **red** | solar block | light these zones in warm red |
| **blue** | lunar block | light these zones in blue |
| **green** | intercalary zone (`SZ`) | the zones to add/remove from a block |
| off | not part of this time block | dark |

The three green zones are always **{7, 16, 17}** — the once-only disc stamps (Nr. 11/13/9), the same set `verify_calendar.py` derives independently. Zone 5 is not coloured green by the figures (it is the 38 special signs), though Menghin's earlier 2000 work also treats it as intercalary — the set is unstable across his publications, see §2.1 and `MENGHIN_HYPOTHESIS.md` §6. This colouring **is** the LED command set, so it is transcribed into `data/scenarios.json` and checked by `scripts/verify_scenarios.py`:

- all 16 states present; every referenced zone ∈ 3…21;
- every green zone is within {7,16,17} = the single-use disc stamps;
- **30** of Menghin's stated solar/lunar zone-sums reproduce from `data/zones.json` (his arithmetic, re-run on our data);
- `|solar − lunar|` equals each state's stated day difference;
- anchors run monotonically 4…19 QY / 12…59 L and the full cycle closes on **1739**.

**Kept honest, not papered over:** 61.2 has only a calendar target (the source gives no zone arithmetic for it), and 64.4's lunar block is stated as 1739 although green zone 7 lies inside it — both are flagged in the data and printed by the verifier rather than forced to balance.

⚠️ The prior attempt's `reference/m5/gold_hat_scenarios.md` is **superseded**: it assumes ~3,400 individually-lit LEDs, a `zone→count` table that is Schmidt-Kaler's ornament tally (651) rather than Menghin's day-values, and the old `5,16,17` intercalary set. Stage 2 reads `data/scenarios.json`, not that file.

**Is the hypothesis actually true?** The full reasoning — the counting-unit selectivity test, the Monte-Carlo null, the cross-hat attempt against Ezelsdorf-Buch, and the confidence levels — is in **`MENGHIN_HYPOTHESIS.md`**. Short version: the *counts* are solid, the *calendar reading* is a legitimate but unproven hypothesis (provisional confidence in the strong claim ≈ 20–30 %), and the demo must label it as such.

---

## 11. Phases & milestones

| Phase | Work | Exit criterion |
|---|---|---|
| **P0 — resolve blockers** | Q1 doc rename; **Q2 height reconciliation (done — exact 745, §2.2)**; **Q3 motif arithmetic (done — 418/1701 derived, §2.1)**; Q5 geometry (done — §2.2) | height table sums to 745 mm; sectioned profile in `hat_parameters.json` |
| **P1 — profile extraction** | Abrollung calibration → refine `r(z)` between Menghin's **four** anchors (A 166 mm @ 61, B 275 mm @ 160, **D 349 mm @ 312**, C 371 mm @ 445); validate against photo silhouette | ✅ **CLOSED.** The Abrollung route is **disproved** (not a development, §6.1); the profile is the **9 documentary constraints + `pchip`**, and the photo only corroborates it. Criterion restated in §12 |
| **P2 — motif catalogue** | Count and classify motifs from the Abrollung → `symbols.json` + `zones.json`; implement primitives. **Menghin's per-zone tool-and-count table (§2.1) and the Fig. 22.1–22.4 per-zone plate set (`text/menghin_page28/29.txt`) have already given the *counting* half** — `data/symbols.json` and `data/zones.json` exist and verify. What is left is (a) the 8 primitives as code, (b) per-zone **placement** (start angle, ornament offset), with the Abrollung only confirming positions within a zone | `verify_calendar.py` reproduces every Menghin zone value (1783 total, 1739, 1701×2, 418, 21 zones, 745) |
| **P3 — geometry kernel** | `build_goldhat.py`; one band end-to-end (start with z13) | ✅ **CLOSED.** `scripts/band_geometry.py` (profile, section, projection — no FreeCAD needed, self-checking) + `scripts/build_goldhat.py` (OCCT). **z13 builds as one valid closed solid**: vol 33,429 mm³, ⌀123.0 × 43.1 mm, and every section radius matches `r(z)` to 0.01 mm. Two bugs found and fixed on the way — see below |
| **P3.5 — motif-form test** | emit the same band three ways (`relief` / `window` / `relief_window`), print all three, **look at them** (§6.3). ⚠️ **Do not wait for the full P3 catalogue to do this** — the coupon needs exactly one primitive (tool 15, the ⌀21 / 6-ring disc) and one zone's placement. Build those two things first and the coupons exist while the other 23 tools are still unwritten. | motif form chosen; `data/hat_parameters.json` ✅ **COUPONS BUILT, print verdict pending.** `scripts/motif_features.py` + `scripts/build_coupons.py` emit `stl/test/z15_{relief,window,relief_window}.stl` plus the fit-test trio, all three single valid solids and measurably different (§11.2). What remains is the **physical print and the five judgements** in §6.3. |
| **P4 — full generation** | zones 1–19 + the Krempe plate split into 3 sectors → `stl/` | all 22 STLs watertight, `verify_geometry.py` passes |
| **P5 — print & fit** | 3-band fit test, then full print, assembly | stacked cone is straight, 745 mm ± 3 mm, joints tight |
| **P6 — (later) Stage 2** | LEDs, M5 firmware | out of scope here |

P0 and P1 are cheap and de-risk everything. P2 is the long pole and the only real research effort.

### 11.1 P3 results — three things the first band changed

**1. The steepest wall is not the cuff — it is the Kalotte's bottom edge (38.9° at z=738).** Measured by the kernel's local-derivative check (see the §2.2 correction). The print strategy previously said the cuff was steepest at 27.8° with „17° of margin“; the real margin is **6.1°**, and it is at **z19**, not the cuff. Still support-free — but now known rather than assumed, and **z18/z19 become the bands to watch at P5**.

**2. A 1 mm-proud Trennband ridge cannot simply butt against the wall.** The first build produced **two disjoint solids**. A collar whose inner end stops exactly on the outer surface meets the band along a **single circle** — a line contact, which OCCT cannot fuse into one solid and which would be a knife-edge joint on the print regardless. Fix: `embed=0.6` mm carries the ring *into* the wall so the fuse sees a real overlapping face. The registration lip had the identical defect for the identical reason (its outer face sits only 0.25 mm inside the wall), and the same fix.

> **Reusable rule for the whole generator: every added feature must OVERLAP the wall, never butt it.** A butt joint is a line contact, and OCCT will silently return a multi-solid shape that `isValid()` still calls valid.

**3. The first STL was 23 MB for one band — ~500 MB across 22.** Two causes: the section was 96 segments, and `Shape.exportStl()` takes no tolerance argument, so OCCT fell back to its default circle resolution (≈478 segments around a ⌀123 ring). Now `n=48` plus an explicit `tessellate(0.05)`: **91,704 → 24,754 facets and 23 MB → 1.2 MB**, with the volume unchanged to 0.001 % (33,429.2 vs 33,429.0 mm³), so no geometry was lost. At a 0.16 mm layer a 0.05 mm chord deviation is invisible. `stl/` is **gitignored** — the data files already describe the geometry, so committed binaries would be churn, not provenance.

### 11.2 P3.5 results — the coupons exist, and four bugs died on the way

`scripts/motif_features.py` (the three forms, placement → prisms) and `scripts/build_coupons.py` (the headless build) produce the three z15 coupons and the fit-test trio. All three coupons are **single valid closed solids** and are genuinely, measurably different:

| coupon | volume | vs bare shell | relief depth measured on the surface |
|---|---|---|---|
| **`relief`** | 33,709.4 | **+5,874.0** | 1.136 mm — raised rim **with recessed ring troughs** |
| **`window`** | 22,439.6 | **−5,395.9** | 0.930 mm — an open field, rim only |
| **`relief_window`** | 24,608.1 | **−3,227.3** | **2.618 mm** — raised rim *and* a through field |

The measured radial profile across one motif (`.`=low, `@`=high, ` `=no material) is the proof the forms differ in *kind*, not just in volume:

```
relief          [ #@%##*++=======++*##%@# ]   stepped rings, symmetric
window          [@%*+=-:..       ..:-=+*%@]   flat open field
relief_window   [+@:...             ...:@+]   widest open span, rim retained
```

**Four bugs found, and three were the same bug wearing different hats:**

1. **A feature that BUTTS the wall does not fuse.** The relief prisms started at depth 0.0 — exactly on the surface — so the common volume was **0.03 mm³** and the fuse returned **31 disjoint solids** that `isValid()` still called valid. This is the *identical* defect as the Trennband ridge and the registration lip (§11.1). All three are now fixed by embedding (`embed=0.6` mm). **The rule has earned its place: every added feature must overlap the wall, never butt it.**
2. **"Add the rings" buries the rings.** `motifs.py` returns the **troughs** (six 0.35 mm bands), not the ridges. Adding the disc and then re-adding each band *inside* it put the rings under the boss, so the first relief coupon rendered as a **flat plain disc**. The correct construction is **add the disc, then recess each trough, then restore the inner ring** — 1 add + 6 cuts + 6 adds per motif, and the order is load-bearing.
3. **Sign inference cannot separate an add from a cut.** A through-cut spans `−1.0..+0.8` and an embedded relief spans `−0.6..+0.8` — "does it cross zero?" gives the same answer for both, so `split_add_subtract` mis-classified RW's core. Fixed by **tagging each prism with `op`** instead of inferring it.
4. **A per-vertex projected polygon is not planar.** `Part.Face` rejects it: *"Failed to create face from wire"*. The whole ring is a curve on the cone. Fixed by building each prism flat in the **tangent plane** at the motif centre and rotating it into place, which also keeps every boolean a plane-plane intersection.

**Performance and process, both learned the hard way.** Fusing z15's 345 prisms by looping pairwise `fuse()` is O(n²) and wedged FreeCAD's GUI thread for **245 s+** (the RPC server reported state `stuck`) — twice in one session, each needing a restart. Two fixes: `shape.multiFuse([...])` (note: a **method on a shape**, not `Part.multiFuse`), and batching by **operation tier** rather than per motif. Relief went **1256 s → 218 s**.

⚠️ **Use `freecadcmd`, not the MCP bridge, for anything non-interactive.** The MCP bridge enforces a ~90 s transport limit; real OCCT boolean work exceeds it, and every timeout wedges the session. `freecadcmd scripts/build_coupons.py` has no GUI thread and no such limit, and it is now the documented route for P4. Two traps in that route, both hit: (a) a script passed as a **file argument** gets `__name__` set to its **basename**, not `"__main__"`, so a plain guard silently does nothing **and freecadcmd still exits 0** — a failure that looks like success; (b) FreeCADCmd prints a `(0 %) … (99 %)` progress bar per export that must be filtered out of any pipe.

⚠️ **Operating note — an OCCT call can wedge FreeCAD without crashing it.** A `makeShapeFromMesh` on that 23 MB mesh left FreeCAD's MCP RPC thread blocked: the socket accepted connections and never answered, while the process stayed alive with no coredump and no journal entry. Recovery was `kill` + relaunch, and it was safe only because nothing unsaved was open (verified first — no `.FCStd` written for 6 h). Diagnosis, if it happens again: `ss -ltnp | grep 9875` tells “process gone” from “RPC thread busy”. The kernel returns a `Part.Shape`, so screenshots and checks need **no STL round-trip at all** — that was the mistake.

### 11.3 P5 pre-flight — the registration lip never engaged (and two fuse bugs fell out)

**The first printed fit trio did not fit.** The hand measurements matched the model (⌀123.7 / ⌀119.7 at z14's lower edge, ⌀125.7 / ⌀122.5 at z15's upper edge, 2.0 mm wall), so the profile and the printer were both fine — the *joint* was broken. Slicing the STLs showed the registration lip at z 533–542 on `z15`, i.e. six millimetres **below** the z=527 joint plane and entirely inside `z15`'s own wall: it never reached `z14`. The two bands only met on a **0.60 mm-wide annulus** and had zero registration.

**Root cause — three defects, all in the lip:**

1. **Wrong end.** `z` increases *downward* on this object (z=0 apex, z=745 brim), so `z0` handed out by `band_span` is the band's **upper** edge. The lip was built at `z0`; it must be at `z1` (the lower edge, where the band meets the one below).
2. **Wrong reference surface.** `r_outer = profile(z0) − clearance` is the band's own **outer** profile. The neighbour's mating surface is its **Trennband collar bore**, `profile(z) − COLLAR_INSET` (0.6), so the lip was ~2 mm too fat.
3. **Cylindrical on a tapering shaft.** A straight lip gains ~0.6–1.2 mm of interference across a 9 mm collar on the narrowing Schaft.

The fix (`make_registration_lip`) sizes the lip to the collar it enters and follows `r(z)`:

```
r_outer(z) = profile(z) − COLLAR_INSET(0.6) − clearance(0.25)
```

Because `COLLAR_INSET (0.6) < wall (2.0)`, this radius is *fatter* than the band's own bore (`profile − wall`). That is the point: it **overlaps the band's own wall** (so the fuse is volumetric and solid) while still clearing the collar of the band below by exactly the clearance. The lip starts `embed=2` mm above `z1` inside the wall and runs `lip_h=6` mm below it, staying inside the 7–9 mm collar.

**Two more fuse defects surfaced while regenerating:**

- **The Trennband collar still butted the wall at a single plane** (face contact, two coincident annuli). OCCT returned it as **two disjoint solids** — the original code had the same failure; it was masked by a butt that OCCT happened to glue. `make_trennband_ridge` now **laps 1 mm past the joint** into the wall and tapers `proud → profile`, so the fuse has real volume. This strengthens the §11.2 rule: it is not only *line* contacts that fail — a shared **face with identical coincident boundaries** can too. **Overlap in a third dimension.**
- The lip's own fuse into the wall is now measurable: **≈830–910 mm³** of overlap per band.

**Verification.** z13/z14/z15 each build as **one valid solid**; re-sliced from the exported STLs the joint gap is a **0.238 mm radial** (diametral 0.476 mm) — nominal 0.25, the 0.01 mm being tessellation. Files: `stl/test/{z13,z14,z15}_fit.stl`.

⚠️ **Before the next print, calibrate the clearance.** 0.25 mm radial is optimistic for FDM and is currently *believed*, not measured. Rather than print 400 g of trio at three clearances, `scripts/build_clearance_coupon.py` emits `stl/test/clearance_ladder.stl` — a ~16 g plate of three independent socket/spigot pairs at **0.15 / 0.25 / 0.35 mm**, each reproducing the joint's *local taper* (`dr/dz = −0.0707` at z=527) rather than a straight cylinder. Row order left→right is 0.15, 0.25, 0.35. It deliberately does **not** put three clearances on three arcs of one band: the lip enters a uniform collar axially, so the tightest arc alone decides whether the band enters — the sectors would not be independent. Keep the loosest pair that still holds, set `registration_clearance_mm` from it, and rebuild.

**Still open at this end:** the same lip logic must be re-checked at the cuff (611–629) and the Kalottenfuß, where the profile turns and `drdz` swings sign — the profile-following form handles it, but the `z1`-adjacency of those rings should be asserted by `verify_geometry.py` before P4.

---

## 12. Verification plan

Runnable, no frameworks, assert-based.

**`scripts/verify_calendar.py`** — ✅ **exists and passes** (`python3 scripts/verify_calendar.py`, stdlib only, no FreeCAD), 11 checks. It reads `data/*.json` and `dimensions.txt` and runs these. These are **derivations from Menghin's own per-zone counts × ring counts**, not fits:
```
zone_count                                    ==   21
zones are exactly 1..21, in order, non-empty z-ranges        [check_zone_count]
disc_bearing_zone_count                       ==   18   <-- 21 - {1,2,5}
disc_bearing_zone_set                         ==   set(1..21) - {1,2,5}
day_value[zone] == count[zone] * rings[zone]  for all 21 zones    [check_day_values]
sum(day_value)                                == 1783
derived day-values == data/readings/menghin.json   (no drift from the copy)
ring_counts subset of {2,3,5,6}                (never 4)          [check_ring_counts]
zone's ring count == its tool's ring count in symbols.json
sum(bosses[zones excluding 1,2,5])            ==  418   <-- derived   [check_menghin_identities]
sum(day_value[zones excluding 1,2,5])         == 1701   <-- derived, route A
1783 - day_value[2] - day_value[5]            == 1701   <-- route B, same number
sum(day_value[3..21])                        == 1739
tool_used_once == [9, 11, 13]                <-- matches Fig. 23's green key  [check_tools_used_once]
zone_height_sum                              ==  745              [check_height_budget]
769 - 40(2 x tussenstuk) - 9(tb19) + 18(cuff) + 7(rise) == 745
len(zone_boundaries_mm) == len(rings) + 1 and boundaries contiguous
611+18+109+7 == 611+18+100+16 == 745   (Menghin's two readings of the top 116 mm)
every tool's zone list in symbols.json == zones.json's attribution  [check_all_zones_covered]
all 21 zones inside the right one of the 5 physical sections     [check_zone_attribution]
2*pi*r(anchor) == anchor circumference +- 3 mm  for A, B, C and D  [check_profile]
profile_interp == "pchip"  (never a slope constant)
max(r) == r(745) == 150.5     (the Krempenrand is the widest point)
Schmidt-Kaler's 651 != Menghin's 1783 and is flagged 'NOT a day count'
dimensions.txt z/tb heights == data/hat_parameters.json, tb1..tb19 all present
```
The two `1701` routes, the `418`, and the `1739` are the strongest check available: they are Menghin's own statements, and they agree only if the per-zone counts *and* the ring multipliers are both right — and **none of the five was fitted to make them agree**. See §2.1.

⚠️ An earlier draft of this section listed `sum(day_value[3..21]) - day_value[5] - day_value[16] - day_value[17] == 1701`. That is **wrong** — it evaluates to 1739 − 38 − 38 − 66 = **1597**, which is a *different* Menghin claim (his figure for 54 synodic months, cross-checked against 54 × 29.53059 = 1594.65, 0.15 % off). Keep the two apart: **1597 is a lunisolar period count and is not a sum over the 21 zones.**

**`scripts/measure_silhouette.py --project`** — the **P1 profile check**, and the evidence behind §6.1. PIL + numpy only. Run it against any of `assets/*.jpg`:
```
python3 scripts/measure_silhouette.py "assets/Cappello_d'oro_di_berlino,_1000_ac_ca._01.jpg" --project

segmentation         foreground = far from the *border median* (not Otsu: on a flat
                     black border Otsu returns thr=1 and then inverts, which is why an
                     earlier version reported the whole canvas as the object)
                     row extent = envelope of runs, not longest run (the gold surface
                     fragments into up to 30 runs per row; dark seams fall below tol)
                     single-row dropouts despiked from the surrounding rows
scale                s = (301/2) / (brim half-width in px)   -> 0.5199 mm/px
                     <-- the Krempenrand is the calibration, from Menghin, not from the image
tilt                 t = acos((widest_row - apex_row) * s / 745)  -> 15.4 deg
out-of-sample check  the tilt model predicts the brim's lower silhouette edge at row 1507;
                     the foreground genuinely ends there (below: 1-16 px specks)
forward check        project r(z) through the ellipse model, compare with the outline,
                     report RMS in *radius* per section and delta at every control height
assert  r(z) reproduces all 9 documentary constraints with 0 error   (by construction)
assert  r(z) is non-decreasing to the max at z=510, then non-increasing to z=611
assert  no control point is overshot (pchip, monotone)               <-- catches a bad interpolant
assert  |photo - projected| <= 2 mm radius at the Krempenrand (z=745) and z=312
assert  |photo - projected| <= 5 mm radius per shaft section
assert  the Kalottenfuss is NOT reported as photo-validated  (the brim's ellipse
       masks it: at z=738 the silhouette reads 148.3, not r(738)=94.5)
assert  every residual over 2 mm carries a named cause in the report
```
**P1 exit criterion, restated (the original ±2 mm-at-10-heights is withdrawn):** the profile reproduces all nine documentary constraints exactly; it is monotone to the maximum at z=510; the photo's *tilted projection* of it agrees within **±2 mm radius** at the ⌀301 Krempenrand and at the mid-shaft z=312, and within **±5 mm radius** per shaft section — and **every** larger residual is attributed to a named cause. **Two features are explicitly outside the photo's reach** and are checked against Menghin alone: the ⌀189 Kalottenfuß (masked by the brim's ellipse in this tilted view) and the cuff transition (a step a full-ring projection cannot represent). An unexplained residual is a failure; a residual with a named cause and a named owner (here: P3's cuff model) is a finding.

⚠️ What the criterion deliberately no longer asks for: a number in mm *per sample height read off the image*. That is not achievable and the earlier draft's version of this check was unachievable for three separate reasons, all now demonstrated rather than assumed — the view is tilted (so the outline is a smear, not `r(z)`), the hat's own shadowed gold is nearly as dark as the black background (so the extreme edges are segmentation-limited, and the tolerance that keeps the lower shaft carves holes in the upper one), and the *same* photograph at two resolutions disagrees with itself by 2–3 mm. A check that cannot fail for the right reason is not a check.

**`scripts/verify_geometry.py`** — on the exported STLs:
```
bounding box height of the full stack == 745 ± 3 mm
outer diameter at each boundary       == r(z) target ± 0.5 mm
r(61)  ==  52.8 ± 2 mm   (anchor A)
r(160) ==  87.5 ± 2 mm   (anchor B)
r(312) == 111.1 ± 2 mm   (anchor D)
r(445) == 118.1 ± 2 mm   (anchor C)
Schaft maximum diameter               == 125 ± 3 mm   (Menghin)
Schaftfuss diameter                   == 108 ± 3 mm   (Menghin)
Kalottenfuss / bronze-band diameter   == 189 ± 5 mm   (Menghin, oval 203 x 175)
Krempenrand outer diameter            == 301 ± 5 mm   (Menghin, oval 307 x 295)
Krempe radial width                   ==  52..55 mm   (Menghin)
Krempe rise                           ==   7 mm      (745 budget residual)
minimum ligature between windows      >=   3 mm
for each zone: sum(motif pitch) <= min circumference in zone   <-- the P2 pitch check
  (this is the check that forces r(629) = 63.5: zone 17 needs 396 mm of 33 x 12 mm
   and zone 18 needs 441 mm of 21 x 21 mm, against 399.0 and 441.9 available)
each solid                            watertight, volume > 0, no self-intersection
every solid's bbox fits 256 x 256 x 256 mm   <-- the printability assertion (§2.3)
Sum band heights                     == 745 mm   (catches the Q2 class of error)
dimensions.txt grand total 769 - 40 (2 x tussenstuk) - 9 (tb19)
  + 18 (cuff) + 7 (Krempe rise)      == 745 mm   (the one-line budget closure, §2.2)
```

**`scripts/verify_calendar.py` on the STL (Stage 2 prep only)** — count through-windows per band and assert it equals the motif count in `zones.json`. Cheap sanity check that geometry and data did not drift apart.

**Visual** — screenshot each band overlaid on its Abrollung strip crop; a human eyeballs 21 pairs once.

---

## 13. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| ~~Q2 height discrepancy~~ **RESOLVED** — the Krempe is a horizontal plate with ~0 stacked height, so summing z1…z19 overshoots by exactly that (§2.2, §3 Q2). The two `tussenstuk` rows are unattested and get deleted | — | — |
| ~~Q5 Kalotte/Krempe unknown~~ **RESOLVED** (§2.2, §3 Q5) | — | residual: the Schaft's intermediate curvature between the anchors, **sized by P1** at 1.6–2.5 mm RMS in radius; the 108/125 mm pair is answered (foot vs maximum, two different heights) |
| ~~Q3 motif count wrong~~ **RESOLVED from the primary source** — 418 bosses / 1701 rings / 1783 days / 440 discs all derive from Menghin's own per-zone table (§2.1). Residual risk: 16 of the 21 per-zone counts are read from the **translation**, not the German; the machine OCR cannot confirm them | — | the P2 assertion catches any transcription slip immediately, because one wrong count breaks the 1701 identity in **both** directions at once — build P2 data with the test running |
| Manual motif **position** errors within a zone (what is left of P2) | a band's motifs are offset or miss the Abrollung strip | Fig. 22.1–22.4 are per-zone photographic plates; visual overlay check (§12) is one human eyeball pass over 21 pairs |
| 22-part tolerance stack drifts over 745 mm | hat leans or joints open | lap joint + 3-band fit test at P5; add a removable internal mandrel as a fallback |
| FreeCAD/OCCT boolean failures on dense motif clusters | band won't build | headless generation isolates crashes; fall back to `fuse`-then-single-`cut` (fuse all motif prisms first — a single boolean against the heavy shell) |
| Abrollung is distorted (a photo, not a true development) | wrong profile | calibrate on two known anchors and reject the source if residuals exceed tolerance |

---

## 14. Immediate next actions

1. ~~Fix the `dimensions.txt` reference (Q1).~~ ✅ **Done.** The two `tussenstuk` rows are dropped from the model — they are unattested and the 745 mm budget reconciles without them (§2.2). They **stay in `dimensions.txt`**, which is the primary source and is not edited.
2. ~~**Refine the profile**~~ ✅ **Done — P1 is closed (§6.1).** `scripts/measure_silhouette.py` was finished and run; it recovered the scale from the Krempenrand and the tilt from the brim, and its forward check puts the ⌀301 Krempenrand within 0.3 mm and the mid-shaft within 1.2 mm. The outcome is a *negative* result on the source question and a *positive* one on the curve: the Abrollung is **not a development** (constant 382 px where ×1.43 is required), a photo cannot yield `r(z)` (15.4° tilt), and the profile therefore stands on **Menghin's nine documented numbers** with `pchip` between them. Residual between the anchors: 1.6–2.5 mm RMS in radius versus the photo. Re-run with `--project`, not by hand.

   ⚠️ Do **not** reach for the prior attempt's per-zone diameters as a cross-check. `reference/cad/calculate_bands_dimensions.py` carries ⌀60/64, 68/72, 76/80, 84/88, 92/96, 100/104, 108/112 mm for z03–z09 — a **synthetic +4 mm arithmetic ladder**, not measurements (Appendix A.4). Our own numbers already disagree with it at z05's top (⌀87.5 from anchor B vs its ⌀80).
3. ~~**Implement `verify_calendar.py` first** (§12) — it needs no geometry and it locks 418/1701/1739/1783/745 in place before a single line of `build_goldhat.py` exists.~~ ✅ **Done** — it exists, it is stdlib-only, and it passes. Run it before starting P3, and re-run it after every data edit.
4. **Settle the two residual data questions** (non-blocking): (a) does `tb19` exist? — zone 19 ends at 738 and the Krempe begins there, so the 109 mm reading uses `tb17`+`tb18` only and `tb19` is **not** needed; (b) is zone 9's 34.9 cm measured at its lower edge? — assumed yes, z = 312; anchor D is consistent with the A–B–C curve either way.
5. Confirm Option **A** for the STL decomposition (§4), Option **C** for the motif form (§6.3), and the **Krempe 3-sector split** (§2.3 — note 2 sectors do *not* fit: the bbox is still 301 mm wide).
6. Then start P2 (motif catalogue): the 8 primitives as code, then per-zone placement. The **counting** half of P2 is already done (`data/zones.json`, verified); the long pole is now the primitives plus placement, not the research.

---

## Appendix A — inventory of what exists

### A.1 This project's own files

| Path | What it is | Status |
|---|---|---|
| `IMPLEMENTATION_PLAN.md` | this document | 1st draft, for review |
| `AGENTS.md`, `README.md` | project instructions; repo readme | — |
| `open_questions.md` | the Q1–Q5 questions and the user's answers | **authoritative for scope** — Q2/Q3 are now closed from the primary source, see the note below |
| `gold_hat.md` | Menghin + Schmidt-Kaler + Wikipedia digest | **secondary** — superseded by `assets/menghin/text/` for every number |
| `dimensions.txt` | the prior attempt's height table, **but only its z/tb height section is Menghin** — confirmed to *be* Menghin's own per-zone table (§2.2); the two unattested `tussenstuk` rows are dropped from the model but stay in the file | ⚠️ **three known-bad lines elsewhere in the file, all the prior attempt's, none of them to be imported:** `base diameter of 20 cm at its widest point` (Menghin: 307 × 295 mm); `thickness = 0.6 mm` (unprintable — the plan uses 2.0 mm); and `symbol 13 - 4 rings = value 4` (**Menghin: Nr. 13 has two rings**, and a ring count of 4 occurs in no zone at all — a 4-ring Nr. 13 would give zone 16 = 19 × 4 = 76 instead of 38 and the total 1821 instead of 1783). `verify_calendar.py` reads **only** the z/tb heights, and asserts them against `data/hat_parameters.json` |
| `sources.md` | 3 physical books | bibliographic verification for P0 |
| `data/hat_parameters.json` | profile, 40 zone boundaries, 39 rings, cuff, Krempe | ✅ **created** |
| `data/symbols.json` | 8 primitives + the 24-tool catalogue | ✅ **created** |
| `data/zones.json` | 21 zones × (tool, count, rings, day_value, fillers) | ✅ **created** |
| `data/readings/menghin.json` | day-value per zone | ✅ **created**, verified |
| `data/readings/schmidt_kaler.json` | ornament count per zone | ✅ **created**, explicitly *not* a day count |
| `scripts/verify_calendar.py` | 11 assertions over the above, stdlib only | ✅ **created, passing** |
| `scripts/build_goldhat.py` | the FreeCAD geometry kernel | to create (P3) |
| `scripts/verify_geometry.py` | STL-level assertions | to create (P3) |
| `stl/berlin_goldhat_{z01..z19,krempe_a..c}.stl` | 22 printed parts | to create (P4) |

⚠️ `open_questions.md` Q2 asked for ~20 mm spacers between Z9–Z10 and Z16–Z17. **The resolved 745 mm budget says they do not exist** (§2.2): they belong to the prior attempt's table, not to Menghin. The file is left as written because it records what was asked.

### A.2 Assets

| Path | What it is | Use |
|---|---|---|
| `assets/menghin/text/menghin_page{20..31}.txt` | **hand transcription / English translation, 12 files, 16,904 B** (page 26 is a 16-byte "page skipped" stub — the book has no such page) | **THE authoritative text tier.** Wins on every conflict. Supplies the four circumference anchors, all 21 zone widths, the Fig. 21 tool legend, the Fig. 22 plate captions, the Fig. 23 key and the alloy analyses |
| `assets/menghin/ocr/menghin_page*.txt` | German OCR of the above (tesseract 5.5.3, `deu`+`osd`, `--psm 1`), 11 files, 21,847 B | the German verbatim quoted in §2.1/§2.2 **and** the witness that exposed the psm-1 digit-dropping failure. **Never the route for a number** |
| `assets/menghin/menghin_page{20..25,27..31}.jpeg` | 11 phone photos of pp. 18–29 (pp. 21–24 and 28 are plates; p. 30 is Fig. 23) | the source itself; **all 11 are rotated 90°** (OSD `Orientation=270`) |
| `assets/berliner_goldhut_abrollung.jpg` (648×800) | **not** an unrolled surface view — it is the prior attempt's debug render, and it is the same drawing as `cone_debug.png` (verified: 800×648 both, mean abs difference 0.93/255, i.e. JPEG noise and nothing else) | ❌ **measured and disqualified.** Its width is constant at 382 px across the shaft, where a development must grow ×1.43 (275 → 392 mm). Not used for geometry or for placement, §6.1 |
| `assets/Berlín_Goldhut_01.JPG` (800×1873) | the earlier draft's "front-on photo" | ❌ **measured and unusable**: mid-grey background (border median 102, tol 42), a second object merges into the left flank, and the brim is cut off at the bottom edge. Only the 250×494 + 800×1581 pair carries a usable silhouette |
| `assets/Berlín_Goldhut_04.JPG` (800×1200) | detail photo | ⚠️ yields **no foreground at all** under border-median segmentation (bg 129, large MAD). Usable by eye only, not programmatically |
| `assets/Berlin_Gold_hat_calendar.jpg` (1008×626) | Menghin's calendar diagram | zone grouping / intercalary confirmation |
| `assets/tb_detail.jpg` (88×83) | Trennband detail | Trennband lip design |
| `assets/berlin_golden_hat-paper-replika.com.pdf` | paper-replica build report | practical assembly reference |
| `assets/cone_debug.png` (648×800) | the prior attempt's cone-fit render — **the same drawing as `berliner_goldhut_abrollung.jpg`** (mean abs difference 0.93/255) | **superseded**, but kept as the provenance that settles the "is it an Abrollung?" question (it is not) |
| `assets/Cappello_d'oro_di_berlino,_1000_ac_ca._01.jpg` (800×1581) | Wikimedia, pure-black background | ✅ **the P1 check photo** — the 15.4° tilt is recovered from the brim and the profile is forward-checked against it, §6.1 |
| `assets/goldhat.jpg` (250×494) | the **same** photograph at a lower resolution | not too small to measure after all — it is the evidence that the residual is at the method's noise floor (2.5/4.5/3.5 mm here vs 2.0/1.6/2.5 mm at 800×1581), §6.1 |
| `assets/cover_issue_5778_de_DE.jpg` (300×453) | journal cover | provenance colour |

Total `assets/` ≈ **40 MB** in git. Flagged rather than acted on: the plan needs the 11 page photos, but the nine other images and the PDF are convenience copies that could move to a release asset or LFS if repo size matters.

### A.3 Scripts

| Path | What it is | Status |
|---|---|---|
| ~~`scripts/analyze_cone.py`~~ | OpenCV cone-measurement script, from the prior attempt | ✅ **deleted when P1 closed** — `cv2` is not installed and will not be added; `measure_silhouette.py` replaced it |
| `scripts/measure_silhouette.py` | PIL + numpy silhouette profiler — **the P1 tool** | ✅ **working and finished.** Border-median segmentation, per-row envelope with despiking, `--dump` (ASCII mask, for a model that cannot accept image content), `--project` (tilt-recovered forward check). See §12 |
| `scripts/verify_calendar.py` | the data-layer assertions | ✅ passing |
| `scripts/motif_features.py` | **the three motif forms** (`relief` / `window` / `relief_window`) as ordered prism operations on the cone; `placed_motifs`, `motif_prism_polygons`, `build_motif_ops`, `fuse_all` | ✅ new, self-checking without FreeCAD |
| `scripts/build_coupons.py` | the P3.5 coupon build — **run under `freecadcmd`**, not the MCP bridge | ✅ emits the 3 coupons + fit-test trio |
| `scripts/build_clearance_coupon.py` | the lap-joint radial-clearance ladder (⌀35 mm, real joint taper, 0.15/0.25/0.35 mm) | ✅ emits `stl/test/clearance_ladder.stl` (~16 g); see §11.3 |
| `scripts/motifs.py` | **the P2 motif primitives and placement** — 2D (u,v) polygons for all 8 boss discs, the Nos. 4–7 fillers and the specials; `for_tool()`, `build()`, `clearance()`, `zone_layout()`, `spandrel_offset()`, `development_svg()` | ✅ **new, self-checking.** `python3 scripts/motifs.py` runs two suites: the primitive checks (ring rule, diameters, nozzle clearance, Menghin's no-overlap constraint) and the **placement checks** (one disc row per zone, one interstice filler per gap at exactly half a pitch, the spandrel lift clearing both neighbours, and `gcd(counts)=1` proving the phase is unconstrained). No FreeCAD, no PIL, no scipy — it runs anywhere |

### A.4 `reference/` — the abandoned attempt (94 MB, **do not recycle**, `AGENTS.md`)

| Path | What it is | Note |
|---|---|---|
| `reference/cad/*.FCStd` | 15 FreeCAD files: the assembly, the zone set, the symbol set, `berlin_goldhut_bands` and per-zone `z01`…`z09` | |
| `reference/cad/freecad_export/` | 38 STLs (16 × `zNN`, 9 × `tbN`, 7 × `bandNN`, 5 × `symbol*`, 1 test) | the prior attempt's **printing split, not its geometry** |
| `reference/cad/3mf/` | 28 3MF files | |
| `reference/cad/svg/` | 18 SVGs — flat unrolled-frustum strips (`zNN_strip.svg`) and traced/rebuilt symbols | papercraft output |
| `reference/cad/freecad_import/` | import staging | |
| `reference/cad/calculate_bands_dimensions.py` | the script that generated those SVGs. **Kept for provenance; not used.** | ⚠️ Its per-zone diameters (⌀60/64, 68/72, 76/80, 84/88, 92/96, 100/104, 108/112 mm for z03–z09) are a **synthetic arithmetic ladder, +4 mm per zone**, not measurements — do *not* use them as an independent check on the P1 profile |
| `reference/m5/` | abandoned ESP32 firmware + `gold_hat_scenarios.md` + `VERIFY_README.md` | Stage-2 reference only |
| `reference/m5/include/led_mapper.h` | `struct zone_t {zone, count, start_index, end_index, multiplier, special_value}` + `load_goldhat_layout()`, `zone_value()`, `map_zone_range_to_led_ranges()` | **the Stage-2 interface to beat.** Its schema is lossy: one `multiplier` per zone cannot express zone 12's Ringkreis-Nr.‑7 interleaved between the Nr.‑14 discs — `data/zones.json` carries a `fillers` list instead |
| `reference/m5/include/goldhat_layout.h` | the same table embedded as a C string, as SPIFFS fallback | |
| `reference/m5/data/berlin.json` | Menghin's per-zone day-values | **now fully re-derived** from Menghin's prose (§2.1); it agrees exactly, so it is a *check*, not an input |
| `reference/m5/data/goldhat_layout.json` | Schmidt-Kaler's per-zone ornament counts (651) | the name is misleading — it is a count table, not a layout. `VERIFY_README.md` uploads it to SPIFFS under that name, so the name stays |
| `reference/m5/data/flag_{de,uk}.png` | UI flags | Stage 2 |
**Three byte-identical duplicates were deleted** in this round: `reference/m5/data/berlin_meghin.json` (≡ `berlin.json`), `reference/m5/data/berlin_schmidtkaler.json` (≡ `goldhat_layout.json`) and `scripts/calculate_bands_dimensions.py` (≡ `reference/cad/calculate_bands_dimensions.py`). In each pair the surviving copy is the one something actually references.


## Appendix B — numbers used in this plan, and where they come from

| Number | Value | Source / derivation |
|---|---|---|
| Total height | **745 mm** | Menghin, verbatim (p20); **closes exactly, three ways**: 611 + 18 + **109** + 7 ✅, 611 + 18 + **100** + 16 ✅ (=745, since 109+7 = 100+16 = 116), and 769 − 40 − 9 + 18 + 7 ✅ (the `dimensions.txt` table reconciled) |
| Zone 1 (Spitze) height | 6.1 cm | **Menghin, verbatim ✅** (p27) |
| Zone 1 base circumference **= anchor A** | 16.6 cm → ⌀52.8 mm | **Menghin, verbatim ✅** (p27) |
| Zone 5 lower edge circumference **= anchor B** | 27.5 cm → ⌀87.5 mm | **Menghin, verbatim ✅** (p27) |
| Zone 9 circumference **= anchor D (NEW)** | 34.9 cm → ⌀111.1 mm | **Menghin, verbatim ✅** (p31); lands within 2 mm of the A–B–C curve |
| Shaft circumference below zone 12 **= anchor C** | 37.1 cm → ⌀118.1 mm | **Menghin, verbatim ✅** (p31) |
| Every zone width | z2 0.85 · z3 1.4 · z4 2.2 · z5 2.45 · z6 2.5 · z7 2.9 · z9 3.4 · z15 3.8 · z16 1.9 · z17 1.5 cm | **Menghin, verbatim ✅** — all **ten** match `dimensions.txt` to 0.05 cm |
| **Schaft maximum diameter** | **125 mm** | **Menghin, verbatim** (p25) ✅ |
| **Schaftfuß diameter** | **108 mm** | **Menghin, verbatim** (p22 caption) ✅ |
| **Kalotte height** | **100 mm** | **Menghin, verbatim** ✅ (rounded; the zone widths give 109) |
| **Schaft→Kalotte cuff** | **18 mm**, vertically pleated, ⌀108 → **127 mm** | **Menghin, verbatim** ✅ (p25); the 127 mm top is *derived* from the zone-17/18 motif pitch |
| **Bronze band in the Kalotte/Krempe Falz** | **203 × 175 mm, 10 mm tall** (mean ⌀189) | **Menghin, verbatim** ✅ (p25) |
| **Krempenrand (widest point)** | **307 × 295 mm** (mean ⌀301) | **Menghin, verbatim** ✅ (p25) |
| **Krempe radial width** | **52–55 mm**, horizontal | **Menghin, verbatim** ✅ (p25) |
| Krempe rise | 7 mm over 56 mm (7.1°) | residual of the 745 budget — **not** stated by Menghin |
| Wall thickness (real) | 0.06 mm | **Menghin, verbatim ✅** (p25) |
| Weight (real, incl. bronze) | 490 g | **Menghin, verbatim ✅** (p25) |
| Gold alloy | 9.8 % Ag / 0.4 % Cu / 0.11 % Sn (1998 microprobe, TU Berlin, Riederer); BAM 2008 synchrotron: apex 90.68 Au / 8.69 Ag / 0.37 Cu / 0.16 Sn, mid-shaft 91.82 / 7.81 / 0.23 / 0.10 | **Menghin, verbatim ✅** (p25) — **not needed for Stage 1**, recorded for Stage 2 provenance labelling |
| Outer surface area | **0.292 m²** | integration of the piecewise profile (§2.2) |
| Filament @ 2.0 mm wall | ~584 cm³ ≈ 0.72 kg PLA | area × thickness, before the windows |
| Gold mass implied by the profile | ≈ **338 g** | 0.292 m² × 0.06 mm × 19.3 g/cm³ — consistent with the stated 490 g incl. bronze |
| ~~Old straight-cone figure: 293 mm base, 9.94°, 0.385 m²~~ | **superseded** | two-anchor fit (166 mm @ z=61, 275 mm @ z=160) — valid only as a check on the upper Schaft |
| Punch tools | **24 in total**; the eight disc bosses Nr. 8–15 are ⌀12/3, ⌀12/2, ⌀13/5, ⌀14/3, ⌀15/3, ⌀15/2, ⌀15/5, ⌀21/6 rings | **Menghin, Fig. 21 legend ✅** (`text/menghin_page27.txt`) |
| Disc bosses (Nr. 8–15) | **418** over the 18 disc-bearing zones | **derived zone-by-zone from Menghin's counts, §2.1** ✅ — no longer merely "verbatim" |
| Concentric rings total | **1701** | **derived, §2.1** ✅ = 1783 − 44 − 38 |
| Discs, all 21 zones | 440 | derived, §2.1 |
| Days, zones 3–21 | 1739 | derived from the same table |
| Days, zones 5+16+17 | 142 | Menghin |
| Days, 54 synodic months | 1597 (≈1594.65) | Menghin |
| Physical main motifs | ~480 (418 + 22 + 38 + star) | derived, §3 Q3 |
| Physical ornaments incl. fillers | ~651 | Schmidt-Kaler table, §3 Q3 |
| Day-value total | **1783** | **derived from Menghin's prose, all 21 zones, §2.1** ✅ |
| Ornamental partition | 3 sections × 7 zones (1–7, 8–14, **15–21**) — offset from the 4 physical sections | **Menghin, verbatim ✅** (p25) |
| Printed parts | **22, confirmed** (19 bands + 3 Krempe sectors) | §4 ✅ |
| Motif physical form | **deferred to a 3-coupon print test** | §6.3 |
| Data layer | `data/hat_parameters.json`, `symbols.json`, `zones.json`, `readings/{menghin,schmidt_kaler}.json` — **all created** | §§5.1, 7 |
| Verification | `scripts/verify_calendar.py` — 11 checks, stdlib only, passing | §12 |

---

## Appendix C — Menghin (2010) OCR: provenance and reproduction

### Source — **two tiers, and the human one wins**

`assets/menghin/menghin_page{20,21,22,23,24,25,27,28,29,30,31}.jpeg` — 11 phone photos of Menghin 2010, book pp. 18–29. Page images are 4032×3024, EXIF orientation 6. **All 11 pages are rotated 90°** (confirmed by `tesseract --psm 0`: every page reports `Orientation in degrees=270 / Rotate=90`); `-auto-orient` handles it.

| Tier | Path | Status |
|---|---|---|
| **1 — transcription (authoritative)** | `assets/menghin/text/menghin_page{20..31}.txt` — 12 files, 16,904 B | **Hand-transcribed English translation of Menghin. Wins on every conflict.** |
| 2 — machine OCR | `assets/menghin/ocr/menghin_page{20,21,22,23,24,25,27,28,29,30,31}.txt` — 11 files, 21,847 B | `tesseract -l deu --psm 1`. Kept: it supplies the **German verbatim** quoted throughout this plan, and it is the independent witness that caught the psm-1 number-dropping failure. |
| 2 — the human transcriptions | `assets/menghin/text/menghin_page{20..31}.txt` (12 files, 16,904 B; **page 26 does not exist** — the book skips it) | **THE authoritative tier.** Where it and the OCR disagree, this wins. All numbers in this plan come from here |
| 3 — the photos | `assets/menghin/*.jpeg` | ground truth for *shapes and layouts*, not for text. **P2 has now used them** — read directly as images (see the note below), which is what confirmed the primitive forms and caught the Fig. 21 legend's `diam. 15 mm` omission for Nr. 13. **P1 used and closed** — and the one believed to be an Abrollung turned out not to be (§6.1). |
| 4 — the derived data | `data/*.json` + `scripts/verify_calendar.py` + `scripts/motifs.py` | **created** — the machine-readable form of tier 2, with tier 2's arithmetic *and* its geometry as runnable assertions. If tier 2 is ever re-transcribed, re-run both; they will tell you which zone or which tool broke |

**⚠️ Tier 3 note — the plate pages are now readable as images.** `menghin_page28/29.jpeg` (Fig. 22's ornament photographs) and `menghin_page30.jpeg` (Fig. 23's combination table) are **rotated 90°**; rotating by **−90°** puts them right way up. Read this way they are directly informative **about shape**: Fig. 22's close-ups showed the disc structure (central boss + N concentric ridges, with the small annulets No. 7 between discs) that `motifs.py` implements, and Fig. 23's table makes the alternating **three-and-five-circle structure of the shaft** visually obvious — which is the pattern §2.1 derives numerically and `verify_calendar.py` asserts.

**But the numbers still come from tier 1, and this was tested rather than assumed.** Reading Fig. 23's „K / A" columns off the image and comparing them against `data/zones.json` gave a **row-for-row disagreement**, and on inspection my reading of the plate was off by one row — i.e. the error was in **reading the image**, not in the data. Fig. 23 is a printed table photographed at an angle: its rows are legible as *structure* and unreliable as *values*. So the tier-3 role is **confirmatory for shape and topology only**. A number must come from tier 1, and `verify_calendar.py` is what proves it.

**Second caveat, also learned the hard way:** a model reading these images **mis-identified the object** as the *Golden Hat of Schifferstadt* — a different object in the same family of four. Vision is useful here, and needs the same discipline as OCR: it proposes, the transcription disposes.

`assets/menghin/text/menghin_page26.txt` is a single line, „Page 26 skipped" — page 26 was not photographed. Pages 21, 22 and 28 are **pure plates** (OCR yields ~0 text) — expected, not an OCR failure. `page23` is the Fig. 18 bottom-view plate, `page24` is the Fig. 19 vertical-half plate (`text/`: „Vertical half. Blue: Spandrel pattern. Green: Switch zones"), and `page30` is the Fig. 23 combination-table legend.

**⚠️ Two source typos found in the transcription**, recorded so nobody re-“fixes” them in the wrong direction:
1. `text/menghin_page27.txt`: „Zone 6 is **25.0 cm** wide" — must read **2.5 cm**. Confirmed by (a) `dimensions.txt` z6 = 25 mm, (b) the zone order (2.45 cm zone 5 then 2.9 cm zone 7), (c) 25 cm would not fit in a 100 mm cap.
2. `text/menghin_page27.txt`, Fig. 21 legend: „– No. 16, eye pattern, length 11 mm" — must read **No. 17**; No. 16 is the crescent, as the immediately preceding line says.

**⚠️ The transcription is an English translation.** German strings are retained in this plan where the OCR tier supplied them, because they are now corroborated by the translation.

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

Output: `assets/menghin/ocr/menghin_page*.txt` (~22 kB total). Note the page number is repeated in the filename — `ocr/menghin_page27.txt`, not `ocr/page27.txt`.

⚠️ **Known failure mode — psm 1 silently drops numbers.** On `menghin_page27.txt` the sentence reads „Die Spitze des Goldhutes hat eine Höhe **an** und einen Basisumfang von 16,6 cm" — the `von 6,1 cm` is *gone*, and even `2,45 cm` came out as `2,5 cm`. Body prose is reliable; **any digit, decimal or number-in-a-table must be re-read from the image** before it is used. The failure is worse on `menghin_page25.txt`, where the entire section-diameter sentence (125 / 108 / 203×175 / 307×295) is garbled in the psm-1 text and only appears on a crop re-read. Cheap verification recipe (grayscale + normalize + 150 % + `--psm 6` recovers the two-column text cleanly on a crop):

```bash
# single column, top 55 % — recovers the tip dimensions
magick assets/menghin/menghin_page27.jpeg -auto-orient -crop 100%x55%+0+0 +repage \
        -colorspace Gray -normalize -resize 150% /tmp/p27.png
tesseract /tmp/p27.png stdout -l deu --psm 6 | grep -A2 "Goldhutes"
# → „Die Spitze des Goldhutes hat eine Höhe von 6,1 cm und einen Basisumfang von 16,6 cm."
# → „Die Zone 5 ist 2,45 cm breit"

# page 25, top 30 % — recovers ALL FOUR section diameters (§2.2)
# (this is the only way to see them; they are absent from ocr/menghin_page25.txt)
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

Every number asserted in §2.1 and §2.2 has been re-read this way. **Since the transcription tier arrived, this recipe is no longer the primary route for *numbers*** — use `text/` — but it remains the only way to recover Menghin's **German wording**, and it is what proved the psm-1 failure mode in the first place. `scripts/measure_silhouette.py` cannot help with printed text.

### Where each claim comes from

`text/` = human transcription (first choice); `ocr/` = machine OCR (German verbatim + cross-check).

| Claim | Primary (text) | Cross-check / German (ocr) |
|---|---|---|
| 745 mm hollow body, one piece, provenance 1996 | `page20` | — |
| 6.1 cm / 16.6 cm tip; 21 zones; **24 punch tools**; full Fig. 21 tool catalogue + all 8 disc diameters | `page27` | `page27` — but psm 1 **drops the digits** here |
| Zone 2 = 0.85 cm / 22 × 2 rings (No. 6); zone 3 = 1.4 cm / 14 × No. 8; zone 4 = 2.2 cm / 15 × No. 10; zone 5 = 2.45 cm / 19 crescent + 19 eye / 27.5 cm circumference; zone 6 = 2.5 cm / 18 × No. 10; zone 7 = 2.9 cm / 19 × No. 11 | `page27` | second half of `page27` |
| Fig. 16 caption: apex 8-rayed star + 22 double-circles; zones 4–9 separated by notched ridges + beaded bands; alternating 3-and-5 ring rhythm; dot-circles in interstices from zone 7 | `page21` | — |
| Fig. 17 caption: **Schaftfuß ⌀10.8 cm**; zone 16 = 2-ring frieze; zone 15 = first 6-ring band; zone 17 = small 2-ring discs; **brim rim = twisted square-section bronze wire, gold folded up around it**; cap–brim fold contains a bronze hoop + pleating band | `page22` | — |
| Fig. 18: **bottom view** plate | `page23` | `page23` (plate) |
| Fig. 19: **vertical half; Blue = spandrel pattern, Green = switch zones** | `page24` | `page24` (plate) |
| **All four section diameters**: 125 (Schaft max), 100 mm Kalotte, 18 mm pleated transition, 203×175 bronze band, 307×295 Krempe, 52–55 mm horizontal, 0.06 mm wall, 490 g, 16 embossed ridges; **alloy composition (Riederer 1998 + BAM 2008)**; „18 horizontal zones"; the 3 × 7 ornamental division | `page25` | `page25` — **psm 1 garbles every one of these digits**; requires the 3-crop recipe above |
| Page 26 | *not photographed* | — |
| Fig. 22.1–22.4 plate captions (= the **per-zone photographic reference set** for P2): 1–2 / 3–6, 7–8 / 9–11, 13–15 / 16–19, 16–21 | `page28`, `page29` | plates |
| Zone 8 = 21 × No. 10 (same as 4 and 6); zone 9 = 3.4 cm, 19 × No. 12 + No. 7 interstices, **34.9 cm circumference** | `page29` | `page29` |
| Fig. 23 combination-table key: yellow = dividing bands, blue = bead, yellow = dot-and-circle, dark yellow = ring, light blue = double-circle, red = symbol punches, **green = disc symbols appearing only once**, K = circle count, A = symbols per zone | `page30` | `page30` (whole file) |
| Zones 10–21 zone-by-zone (counts, tools, widths, 37.1 cm anchor); zone 16 = last shaft zone, collar of three notched beads; zone 17 = first cap zone; zone 20 negative relief pressed from below; **the 418 / 1701 / 18-zone closing summary**; the 3-and-5 alternating rhythm "strictly maintained up to Zone 14"; the circumference-correlation design principle; the ornamental canon "only partially aligns with the formal structural division" | `page31` | `page31` — `grep -n "1701"` |

⚠️ **Pages 20–25 sit in a chapter that compares the Berlin hat with other gold hats** (Schifferstadt, Avanton, Ezelsdorf-Buch). Two cautions previously recorded in this plan were **wrong** and are withdrawn: the zone count **18** is Menghin's own count of the **disc-bearing** zones of Berlin's 21 (not a comparison object's total), and **„hybrider Kegelhut" is Menghin's type name for the Berlin hat itself** (`page20`: „the fourth of its kind … of the Schifferstadt type"). Every number above is nevertheless traceable to a specific page, which is why the two are distinguishable.

⚠️ **The `text/` transcripts are an English translation of Menghin.** Where this plan quotes German verbatim, the German came from a crop-re-read of the OCR tier and is retained because it is corroborated by the translation; English quotes are the translation itself.

⚠️ **Pages 20–25 mix the Berlin hat with the comparative hats** (Schifferstadt, Avanton, Ezelsdorf-Buch) in the surrounding chapters. But two earlier cautions in this plan were **wrong** and are withdrawn: (a) the zone count **18** is *not* a comparison object's total — it is Menghin's own count of the **18 disc-bearing zones of the Berlin hat's 21**; (b) **„hybrider Kegelhut" is Menghin's type name for the Berlin hat itself** (it is „the fourth of its kind … of the Schifferstadt type", p20), not a comparison object. The only genuine mixing risk is the *adjacent* chapters on the 18-zone comparison hats, which is why every number above is traceable to a specific page.
