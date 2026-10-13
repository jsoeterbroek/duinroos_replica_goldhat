# `reference/cad/printed/` — proof-of-concept prints of the abandoned attempt

**These are evidence, not assets.** They come from the **abandoned earlier attempt**
(`AGENTS.md`: use `reference/` for reference, do **not** recycle its files or code).
They are kept so the current plan can cite what was physically proven to print, and
they are read as *design evidence* in `IMPLEMENTATION_PLAN.md` §11.4.

## What is shown

Proof-of-concept prints of **zones 4 and 8**, three views each:

| File | View |
|---|---|
| `z04_z08_top.jpeg` | looking down into the cavity — the 4-arm spider, the central hub, the hub connector slot |
| `z04_z08_side.jpeg` | the decorated outer skin and its ring symbols, with the inner structural ring recessed |
| `z04_z08_bottom.jpeg` | the underside — spider, hub, and the zone number cast into a spoke (`z04`, `z08`) |

**One zone per print**, each with: a thin (~1 mm) decorated outer skin; a hollow
annulus directly behind the symbols (the **LED cavity**); an inner structural ring;
a **4-arm spider** to a central hub; and a slot/nub connector at the hub. The layer
lines run around the circumference — printed axis-vertical.

## They match the models in this folder

- `berlin_goldhut_z04.FCStd` — Body007 = 33,406 mm³, bbox **70 × 24 × 70 mm**, plus a
  separate 9 mm Trennband body (Body008, Ø74).
- `berlin_goldhut_z08.FCStd` — Body007 = 72,622 mm³, **102 × 31 × 102 mm**
  (Trennband Ø106).

## Why they matter

They establish that the **spider + cavity + skin** shape prints, and it is exactly the
Stage-2 light path the project needs. §11.4 **adopts the shape** but **changes the
joint**: the P3 lap lip is replaced by a flat stacked seat plus a keyed central spine
(anti-misalignment) and a keyway (anti-rotation). Two caveats recorded in §11.4: the
~1 mm skin is too thin (keep the 2.0 mm structural wall), and the apex zones z01–z02
have no room for a spider.

The replacement is tested by `scripts/build_stacked_joint_coupon.py`
(`stl/test/stacked_joint.stl`).

## Size

The photos are downscaled to **1600 px longest edge, JPEG q80** (~0.3 MB each,
down from 2.3–2.8 MB) to keep the repo small; full resolution is not needed to read
the spider, cavity and skin. Full-resolution re-encoding alone barely helps (the
phone JPEGs are already well encoded) — the saving is the downscale.

`assets/menghin/*/jpg/` (~96 MB of book-page phone photos) is the larger offender and
is deliberately **not** touched here: those are OCR/primary-source evidence, and the
plan depends on them as images (all 11 are stored rotated 90°, OSD `Orientation=270`).
