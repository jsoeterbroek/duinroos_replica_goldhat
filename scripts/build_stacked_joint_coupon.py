#!/usr/bin/env python3
"""
build_stacked_joint_coupon.py — the stacked-joint trial: keyed spine vs flat stack.

Run HEADLESS (see the note in build_coupons.py for why not the MCP bridge):

    freecadcmd scripts/build_stacked_joint_coupon.py

What this decides
-----------------
The P3 plan joined the bands with a 6 mm LAP lip that nests into the collar of
the band below (scripts/build_goldhat.py `make_registration_lip`).  Its own P5
pre-flight found three defects in that one feature and a first print that did
not fit, and a lap gives no rotational constraint at all.  The operator prefers
a FLAT STACK with connectors that prevent horizontal misalignment, so this
coupon tests the replacement:

    structure / height   -> a flat annular seat          (determinate, +-1 layer)
    lateral alignment    -> a central keyed SPINE         (one straight part,
                                                           so no tolerance stack)
    anti-rotation        -> a KEYWAY in the hub bore       (also clocks the wire
                                                           bus and the ornament
                                                           seam)

The coupon is a SCALED FEATURE TEST, like stl/test/clearance_ladder.stl: the
fit depends on the clearances (0.25 mm), not on the absolute diameter, so the
ring is scaled to ~d70 and the tiles are 12 mm tall.  The taper is the real
local slope at the z14/z15 joint (dr/dz = -0.0707) so the seat is not a
special case.

What is deliberately NOT in this coupon
---------------------------------------
* The LED cavity (the hollow annulus behind the decorated skin).  The prior
  prints (reference/cad/printed/) already prove it prints, and it does not
  change the JOINT mechanics.  Add it back in the P4 band, behind a 2 mm
  structural wall -- the 1 mm skin in those prints is too thin for the 0.8 mm
  relief and for the P3.5 fin judgement.
* The outer-rim light rebate.  A flat seam leaks and every lit-band scenario in
  data/scenarios.json depends on it not leaking; the rebate is a SEPARATE,
  loose feature from the structural seat and is judged by the torch test, not
  modelled here.

Judgements to run on the print (plan IMPLEMENTATION PLAN section 11.4)
---------------------------------------------------------------------
  1. stack 3 tiles with NO spine     -> measure the lateral drift (the control)
  2. stack 3 tiles with the spine    -> drift should be < the spine clearance
  3. twist the stack                 -> the key must stop rotation
  4. phone torch inside the top tile -> is the seam light-tight?  (expect: no,
                                         this is what motivates the rebate)
  5. is the 3-tile stack straight?   -> measure top-tile concentricity
"""

import math
import os
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import band_geometry as G            # noqa: E402
import build_goldhat as B            # noqa: E402  (_revolve_section, export_stl)

import FreeCAD                       # noqa: E402  (only inside FreeCAD)
import Part                          # noqa: E402

OUT = os.path.join(HERE, "stl", "test")

# --- coupon geometry (mm) -----------------------------------------------------
# The JOINT features are read from data/hat_parameters.json so the coupon and the
# model cannot drift; only the coupon's own scale is set here (it is a feature
# test, like the clearance ladder -- the fit depends on the clearances, not the
# diameter).
R0 = 35.0            # outer radius at the seat (d70)
H = 12.0             # tile height (a compact zone)
WALL = 2.0           # structural wall (plan section 6.4 / 11.4)
TAPER = 0.0707       # real local dr/dz at the z14/z15 joint (z=527)

_J = G.load()[0]["joint"]
assert _J["type"] == "stacked_spine", "hat_parameters.joint is not stacked_spine"
BORE_R = _J["hub_bore_mm"] / 2.0          # the spine passes through this
HUB_R = BORE_R + _J["hub_wall_mm"]        # hub outer radius
SPOKES = _J["spokes"]                     # arms (the "interior ribs" section 6.4 asks for)
SPOKE_W = _J["spoke_w_mm"]                # arm width
KEY_W = _J["keyway_w_mm"]                 # keyway width
KEY_D = _J["keyway_depth_mm"]             # keyway depth, INTO the hub wall
CLEAR = _J["spine_clearance_mm"]          # radial clearance

SPOKE_EMBED = 2.0    # overlap into the hub and the wall -- NEVER butt (section 11.2)
KEY_ANGLE_DEG = 45.0  # between two spokes, so the cut cannot graze an arm
# The keyway cutter must start INSIDE the bore void, not on the bore cylinder.
# A cutter face flush with the bore is TANGENT to it: zero-volume contact,
# `isValid()` still True, and one non-manifold edge per tile in the slicer
# (Bambu Studio). Overlap, never coincide -- the section 11.2 rule for cuts.
KEY_EMBED = 1.0

N_TILES = 3
SPINE_LEN = N_TILES * H + 20.0

# derived
R_TOP = R0 - TAPER * H
SPINE_R = BORE_R - CLEAR
SPINE_RIDGE_OUT = BORE_R + KEY_D - CLEAR
SPINE_RIDGE_W = KEY_W - 2 * CLEAR
SPOKE_X0 = HUB_R - SPOKE_EMBED
SPOKE_X1 = R_TOP - 0.5           # inside the wall at the top, overlaps it at the seat


def _box(l, w, h, x, y, z):
    return Part.makeBox(l, w, h, FreeCAD.Vector(x, y, z))


def tile_section():
    """The tile's outer ring, as a closed (r, z) polygon. z is UP from the seat."""
    n = 24
    zs = [H * i / n for i in range(n + 1)]
    outer = [(R0 - TAPER * z, z) for z in zs]
    inner = [(R0 - TAPER * z - WALL, z) for z in reversed(zs)]
    return outer + inner


def build_tile():
    """One tile: outer ring + hub + spider, with a keyway in the hub bore."""
    ring = B._revolve_section(tile_section())
    hub = B._revolve_section([(BORE_R, 0.0), (HUB_R, 0.0),
                              (HUB_R, H), (BORE_R, H)])
    parts = [ring, hub]
    for k in range(SPOKES):
        b = _box(SPOKE_X1 - SPOKE_X0, SPOKE_W, H, SPOKE_X0, -SPOKE_W / 2.0, 0.0)
        b.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1),
                 360.0 * k / SPOKES)
        parts.append(b)

    tile = parts[0]
    for p in parts[1:]:
        tile = tile.fuse(p)
    tile = tile.removeSplitter()

    # keyway: a slot in the hub bore, at an angle between two spokes. It starts
    # KEY_EMBED inside the bore so its face is not tangent to the cylinder.
    key = _box(KEY_D + KEY_EMBED, KEY_W, H + 2.0, BORE_R - KEY_EMBED,
               -KEY_W / 2.0, -1.0)
    key.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), KEY_ANGLE_DEG)
    tile = tile.cut(key).removeSplitter()
    return tile


def build_spine():
    """The keyed spine: a rod that centres every tile, plus the key ridge."""
    rod = Part.makeCylinder(SPINE_R, SPINE_LEN)
    ridge = _box(SPINE_RIDGE_OUT - (SPINE_R - 1.0), SPINE_RIDGE_W, SPINE_LEN,
                 SPINE_R - 1.0, -SPINE_RIDGE_W / 2.0, 0.0)
    return rod.fuse(ridge).removeSplitter()


def selfcheck():
    """The clearances are the whole point, so assert them before building."""
    assert abs((SPINE_R + CLEAR) - BORE_R) < 1e-9, "spine does not fit the bore"
    assert abs((SPINE_RIDGE_OUT + CLEAR) - (BORE_R + KEY_D)) < 1e-9, \
        "key ridge does not fit the keyway depth"
    assert abs((SPINE_RIDGE_W + 2 * CLEAR) - KEY_W) < 1e-9, \
        "key ridge does not fit the keyway width"
    assert SPINE_LEN > N_TILES * H, "spine is shorter than the stack it must align"
    # overlaps, never butts (the section 11.2/11.3 rule)
    assert SPOKE_X0 < HUB_R, "spoke does not overlap the hub"
    assert SPOKE_X1 > R_TOP - WALL and SPOKE_X1 < R0, \
        "spoke must overlap the wall without protruding through it"
    # the keyway must leave hub material and must not graze a spoke
    assert KEY_D < HUB_R - BORE_R, "keyway cuts through the hub"
    assert KEY_EMBED > 0.0, "keyway must start inside the bore, not on it (non-manifold)"
    for k in range(SPOKES):
        d = abs((KEY_ANGLE_DEG - 360.0 * k / SPOKES + 180.0) % 360.0 - 180.0)
        assert d > math.degrees(math.atan2(SPOKE_W / 2.0, HUB_R)) + 5.0, \
            "keyway is too close to a spoke"
    # the stack of tiles must reach past the spine's straight section
    print("stacked-joint self-check: all passed")
    print("  spine d%.2f in bore d%.2f  (%.2f mm radial clearance)"
          % (2 * SPINE_R, 2 * BORE_R, CLEAR))
    print("  key %.1f x %.1f in keyway %.1f x %.1f  (%.2f mm all round)"
          % (SPINE_RIDGE_W, SPINE_RIDGE_OUT - (SPINE_R - 1.0), KEY_W, KEY_D, CLEAR))
    print("  tile d%.1f x %.1f mm, taper %+.4f;  stack of %d = %.1f mm"
          % (2 * R0, H, TAPER, N_TILES, N_TILES * H))


def main():
    selfcheck()
    os.makedirs(OUT, exist_ok=True)

    print("\n=== stacked-joint coupon ===")
    t = time.time()
    tile = build_tile()
    print("  tile      %8.1f mm3  solids=%d valid=%s"
          % (tile.Volume, len(tile.Solids), tile.isValid()))
    spine = build_spine()
    print("  spine     %8.1f mm3  solids=%d valid=%s"
          % (spine.Volume, len(spine.Solids), spine.isValid()))

    # --- lay the parts out on one plate (d70 tiles spaced 75 mm, spine below)
    # Each tile's hub top is engraved with its index: the three tiles are
    # identical, so without a mark their order (and the stack they came from)
    # is lost as soon as they leave the plate. The spine end face carries the
    # coupon tag and the clearance it was cut at -- "SJ" for stacked-joint.
    hub_rmid = HUB_R - _J["hub_wall_mm"] / 2.0
    tag = "SJ%.2f" % CLEAR
    spine_size = G.fit_disc_label(tag, SPINE_R)
    assert spine_size, "spine end face too small for %r" % tag
    spine = G.engrave_label(spine, tag, (0.0, 0.0, SPINE_LEN), spine_size)
    assert len(spine.Solids) == 1 and spine.isValid(), "engraving broke the spine"

    shapes = []
    for i in range(N_TILES):
        s = tile.copy()
        size = G.fit_ring_label(str(i + 1), hub_rmid, _J["hub_wall_mm"])
        assert size, "hub face too small for tile index %d" % (i + 1)
        s = G.engrave_ring_label(s, str(i + 1), hub_rmid, H, size)
        assert len(s.Solids) == 1 and s.isValid(), \
            "engraving tile %d broke it" % (i + 1)
        s.translate(FreeCAD.Vector((i - (N_TILES - 1) / 2.0) * 75.0, 0.0, 0.0))
        shapes.append(s)
    spine.translate(FreeCAD.Vector(0.0, 80.0, 0.0))
    shapes.append(spine)

    # ⚠️ B.export_stl, not a local `mesh.addFacets(s.tessellate())` loop: the
    # tuple form silently keeps only the FIRST shape (build_goldhat._facets),
    # which is how the earlier clearance ladder shipped as a single part.
    path = os.path.join(OUT, "stacked_joint.stl")
    facets = B.export_stl(shapes, path)
    vol = sum(s.Volume for s in shapes)
    xspan = [s.BoundBox for s in shapes]
    print("\nwrote %s" % path)
    print("  %d facets, %.1f g PLA" % (facets, vol * 1.24 / 1000.0))
    print("  plate spans x %.0f..%.0f, y %.0f..%.0f"
          % (min(b.XMin for b in xspan), max(b.XMax for b in xspan),
             min(b.YMin for b in xspan), max(b.YMax for b in xspan)))
    print("  %.0fs total" % (time.time() - t))

    rep = os.path.join(OUT, "stacked_joint_report.txt")
    with open(rep, "w") as f:
        f.write("stacked-joint coupon (keyed spine vs flat stack)\n")
        f.write("built %s\n\n" % time.strftime("%Y-%m-%d %H:%M"))
        f.write("tiles: %d x (d%.1f, h%.1f, wall %.1f, %d spokes, bore d%.1f, "
                "keyway %.1f x %.1f)\n"
                % (N_TILES, 2 * R0, H, WALL, SPOKES, 2 * BORE_R, KEY_W, KEY_D))
        f.write("taper: %+.4f (real dr/dz at the z14/z15 joint)\n" % TAPER)
        f.write("spine: d%.2f x %.1f mm, key ridge %.1f x %.1f, clearance %.2f mm\n"
                % (2 * SPINE_R, SPINE_LEN, SPINE_RIDGE_W,
                   SPINE_RIDGE_OUT - (SPINE_R - 1.0), CLEAR))
        f.write("labels: tiles 1..%d engraved on the hub, spine '%s' on its end\n"
                % (N_TILES, tag))
        f.write("mesh: 2-manifold (export_stl asserts 0 non-manifold edges; the\n"
                "      first build's keyway was tangent to the bore -- see section 11.4)\n")
        f.write("\nprint one job. Judgements 1-5 are in "
                "IMPLEMENTATION_PLAN.md section 11.4.\n")
        f.write("Use matte PLA, not silk.\n")
    print("wrote %s" % rep)


if __name__ == "__main__" or __name__ == os.path.splitext(
        os.path.basename(__file__))[0]:
    # freecadcmd sets __name__ to the script's BASENAME, not "__main__"; a plain
    # guard silently does nothing and still exits 0. Accept both (build_coupons.py).
    main()
