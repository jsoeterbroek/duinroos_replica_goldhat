# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Canonical copy:** the tooling sections below are mirrored in `AGENTS.md`
> (`## Tooling (build & verify)`), which is the repo's canonical agent-guidance
> file. Update both together.

## Project Purpose

A 1:1 scale replica of the Berlin Gold Hat — a 745 mm tall cone-shaped Bronze Age artifact with intricate punched decorative patterns. The model is stylized (no dents/creases), not archaeologically exact.

**Three stages (all read `data/*.json` as the single source of truth; restructured 2026-10-14):**
- **Stage 1 (active):** script-generated visual **scenario figures** (PNG/JPG/SVG) per calendar hypothesis, in the Menghin pp. 60–63 idiom — see `IMPLEMENTATION_PLAN.md` §1.5. No FreeCAD, no printer.
- **Stage 2 (draft, gated on Stage 1):** the 22 printable parts — 19 stacked bands + 3 Krempe (base plate) sectors.
- **Stage 3 (planned):** Interactive LED lighting via M5 Core S3 to demonstrate competing lunisolar calendar theories.

## Commands

All verification scripts are stdlib-only and run without FreeCAD. Build scripts require FreeCAD.

**Verify (no FreeCAD needed):**
```bash
python3 scripts/verify_calendar.py          # Menghin's 4 identities (418 discs, 1701 day-values)
python3 scripts/verify_geometry.py          # DATA tier always; STL tier when artifacts exist
python3 scripts/verify_scenarios.py         # Stage-3 lighting zone mapping
python3 scripts/verify_figures.py           # Stage-1 figure set: data-derived + complete
python3 scripts/band_geometry.py --selfcheck  # Pure-math kernel self-test
```

**Stage-1 figures (no FreeCAD):**
```bash
python3 scripts/render_scenarios.py --all   # 16 panels + 16 developments + 4 sheets + comparison + caution -> figures/
python3 scripts/render_scenarios.py --all --pack   # also figures/_pack.pdf
python3 scripts/render_scenarios.py --check-deterministic   # PNG+SVG byte-identical
```
See `docs/stage1_figures.md`.

**Build (requires FreeCAD):**
```bash
freecadcmd scripts/build_goldhat.py z13     # Single band → stl/test/z13_stacked.stl
freecadcmd scripts/build_goldhat.py --all   # All 22 parts
freecadcmd scripts/build_clearance_coupon.py
freecadcmd scripts/build_stacked_joint_coupon.py
```

## Architecture

### Three-tier kernel

**Data layer (`data/`):**
- `hat_parameters.json` — 9 Menghin (2010) documentary constraints; the profile r(z) is PCHIP-interpolated from these
- `zones.json` — 21 decorative zones: symbol counts, ring counts, day-values, tool IDs, z-spans
- `symbols.json` — punch tool definitions (tools 1–17), ring counts, zone assignments
- `scenarios.json` — Stage-3 lighting: 16 time blocks, zone-to-color mappings

**Geometry kernel (`scripts/band_geometry.py`):**
Pure math, testable without FreeCAD. Implements PCHIP interpolation, cone-surface projection of 2D motif coordinates (u=arc length, v=height), band ring/span queries, and clearance checks. The `Profile` object and `pchip_slopes()` must be **identical** between `band_geometry.py` and `motifs.py` — a mismatch breaks clearance validation.

**CAD builder (`scripts/build_goldhat.py`):**
FreeCAD/OCCT integration. Revolves polyline sections into hollow band solids, attaches Trennband ridges, registration lips, P4 flat-stacked hubs+spokes, and motifs. Validates mesh topology (`nonmanifold_edges()`) before export. STL tessellation at 0.05 mm deviation.

**Motifs (`scripts/motifs.py`):**
Primitive punch shapes (`ring_dot`, `double_circle`, `crescent`, `eye`, `star8`). Returns (outer_polygon, [inner_holes]) in 2D (u, v) coordinates. Placement logic avoids radial seams landing on motifs.

### Validation tiers (always run in order)
1. **DATA tier** — JSON arithmetic, bed fit (always runs, no FreeCAD)
2. **STL tier** — 2-manifold, closed, positive volume, bed fit (when artifacts exist)
3. **OCCT tier** — non-manifold edge check, tangent contact check (during build)

## Critical Conventions

**Coordinate system:**
- All dimensions in mm; z=0 at apex, z=745 at Krempe
- Profile r = radius; revolve around Z-axis
- Motif coords: u = arc length (mm, CCW from outside), v = height (mm, +v upward)
- Relief offset is along the cone's **outward normal**, not horizontal

**Data authority — use these, not `dimensions.txt`:**
- `data/hat_parameters.json` + `IMPLEMENTATION_PLAN.md` §2.2 for the profile
- `IMPLEMENTATION_PLAN.md` is the authoritative spec for every derivation, design decision, and photo-residual attribution

**Verified invariants:**
- 9 profile constraints reproduced exactly by construction
- 418 bossed discs across 18 zones (zones 1, 2, 5 excluded) — Menghin's exact count
- 1701 = Σ(count × rings) over disc-bearing zones — verified by `verify_calendar.py`
- Photo residuals: Krempenrand ≤0.3 mm, z=312 ≤1.2 mm, shaft ≤2.5 mm RMS (§12 of IMPLEMENTATION_PLAN.md)

**Known operator decisions:**
- Zone 1 apex star is left plain (not built); it is continuous geometry, not a repeatable motif
- **Apex (z 0–61) is a rounded dome, not a sharp cone** (2026-10-15; see `data/hat_parameters.json` `_profile_apex_note` and plan §11.6). The overhang test is signed, not `|slope|`.
- P4 flat-stacked joint (hub + 4 spokes + keyway) replaced P3 lap lip
- Krempe is split into 3 sectors (a/b/c); seam phasing must land in motif spandrels

## Phase Status

| Phase | Status |
|---|---|
| **Stage 1: scenario figures** | **Active — V0 next (`IMPLEMENTATION_PLAN.md` §1.5)** |
| P1: Profile r(z) | Done |
| P2: Zone data | Done |
| P3: Band geometry | Done |
| P3.5: Motif form (relief vs window) | Deferred pending print test |
| P4: Stacked joint | Done |
| P5: Assembly docs | Next (gated on Stage 1) |
| Stage 3: LED firmware | Planned |

## Key Reference Files

- `IMPLEMENTATION_PLAN.md` — full derivation of every number, every design choice, all photo analysis
- `assets/menghin/` — scanned Menghin 2010 source pages and hand-transcribed text
- `reference/` — earlier abandoned CAD attempt; kept for reference, do not recycle

## Technology Stack

| Component | Tech |
|---|---|
| 3D geometry | FreeCAD + OpenCASCADE (OCC Part) |
| Profile interpolation | Fritsch-Carlson PCHIP (hand-coded, stdlib only) |
| Verification | Python 3 stdlib |
| Output | Binary STL, 0.05 mm tessellation, 22 parts |
| Print target | BambuLabs, 256 mm bed, 0.16 mm layers |
| Stage 3 hardware | ESP32 M5 Core S3 |
| Stage 3 firmware | PlatformIO + C++ (M5Stack SDK) |
