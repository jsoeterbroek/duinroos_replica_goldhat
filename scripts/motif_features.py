#!/usr/bin/env python3
"""
Motif features for the Berlin Gold Hat replica — the P3.5 coupon.

Turns the 2D primitives from motifs.py into 3D cut/added features on a band's
outer surface, in one of the three forms the plan defers to a print test:

    relief        raised boss + raised rings            (R)
    window        a hole through the wall               (W)
    relief_window recessed field cut through, rings kept (RW)

All three place the SAME motifs at the SAME coordinates; only the material
inside a motif's outline differs (plan section 6.3). That is what makes the
coupon comparison meaningful, so `feature_solids()` is the single entry point
and the form is a parameter.

Geometry, per the plan's section 5.3:
  - the motif is projected onto the cone in a local frame tangent at its
    centre, so it keeps its angular width (band_geometry.project)
  - the tool is a prism whose axis is the local surface NORMAL, so a window
    is a radial drilling and a relief is a true normal offset
  - each motif is built as ONE prism per polygon (outline or hole), unioned,
    so a 6-ring disc is 1 outline + 6 trough prisms rather than a mesh soup

`python3 scripts/motif_features.py --selfcheck` runs with NO FreeCAD: it
checks the projected vertex positions, the prism extents, and that a window
actually clears the wall while a relief does not.
"""

import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import band_geometry as G                                          # noqa: E402
import motifs as M                                                 # noqa: E402


FORMS = ("relief", "window", "relief_window")


def _flatten_polygons(polys):
    """
    Normalise every polygon in a list to a list of (u, v) points.

    A motif's `holes` are BANDS: each is [outer_ring, inner_ring], meaning the
    trough between two circles. A band is not a polygon, so it is split into
    its two rings and each ring becomes its own prism -- for a relief that
    raises both rings and leaves the trough between them recessed, which is
    exactly how a Scheibenbuckel reads. Treating a band as one polygon would
    fill the trough solid and erase the rings.
    """
    out = []
    for item in polys:
        if item and isinstance(item[0][0], (list, tuple)):
            out.extend(item)                 # a band: two rings
        else:
            out.append(item)                 # already a polygon
    return out


def motif_prism_polygons(form, outer, holes, relief_mm=0.8, wall_mm=2.0,
                         through_margin=1.0, embed=0.6, trough_frac=0.4):
    """
    Decide, for one motif, which polygons become prisms and at what depths.

    Returns a list of (polygon, depth_from, depth_to, op) where `op` is
    "add" or "cut" -- stated explicitly rather than inferred from the depth
    signs. Sign inference is ambiguous: a through-cut spans the surface
    (-1.0 .. +0.8) exactly like an embedded relief does (-0.6 .. +0.8), so
    "does it cross zero?" cannot tell them apart. The op field can.

    `embed` makes every ADDITIVE prism start BELOW the surface rather than
    exactly on it. A relief starting at depth 0.0 merely touches the wall:
    measured common volume 0.03 mm3, and the fuse returned 31 disjoint
    solids. Same defect as the Trennband ridge -- a feature must overlap the
    wall, never butt it.
    """
    if form == "relief":
        # A Scheibenbuckel is a boss, then concentric RIDGES separated by narrow
        # TROUGHS. The `holes` from motifs.py are the TROUGHS (each a 0.35 mm
        # band), not the ridges. So the correct construction is
        #     ADD the whole disc, then RECESS each trough.
        # An earlier version added the disc AND re-added each ring band on top
        # of it at a lower height -- which buried the rings inside the boss and
        # made the motif render as a flat plain disc.
        #
        # `trough_frac` is how deep the trough sits relative to the ridge tops:
        # 0.4 means a 0.8 mm relief leaves a 0.32 mm recess, which a 0.16 mm
        # layer renders as 2 layers of visible step.
        trough_depth = relief_mm * trough_frac
        out = [(outer, -embed, relief_mm, "add")]
        for band in holes:                       # band = [outer_ring, inner_ring]
            # A trough is the annulus BETWEEN the two rings. Two prisms per
            # trough, in order:
            #   CUT  the outer ring from well above the boss down to trough
            #        depth, so material is actually removed (a cut that starts
            #        above the surface and ends above it does nothing).
            #   ADD  the inner ring back up to full relief, which restores the
            #        ridge inside it and leaves the narrow ring recessed.
            outer_ring, inner_ring = band[0], band[1]
            out.append((outer_ring, trough_depth, relief_mm + embed, "cut"))
            out.append((inner_ring, -embed, relief_mm, "add"))
        return out

    if form == "window":
        # a clean hole: wall thickness plus a margin at each end
        return [(outer, -through_margin, wall_mm + through_margin, "cut")]

    if form == "relief_window":
        # RW keeps R's raised profile AND W's light path. The raised disc is
        # added, then the RECESSED FIELD that remains is cut through: the cut
        # is the inner ring of each trough, extended to the inner wall. That
        # leaves the ridges intact and standing, with open slots between them.
        inset = _inset_polygon(outer, relief_mm * 1.2)
        out = [(outer, -embed, relief_mm, "add"),
               (inset, -through_margin, wall_mm + through_margin, "cut")]
        return out

    raise ValueError("unknown motif form %r" % form)


def split_add_subtract(polys):
    """Split tagged prisms into the ones to ADD and the ones to CUT."""
    add, sub = [], []
    for poly, a, b, op in polys:
        (add if op == "add" else sub).append((poly, a, b))
    return add, sub


def _inset_polygon(poly, amount):
    """Shrink a convex-ish polygon toward its centroid by `amount` mm.

    Cheap and adequate: the motif outlines are convex or star-shaped about
    their centre, so a centroid-directed inset is a good approximation and
    never self-intersects. A full polygon offset would be OCCT's job, and
    the extra fidelity buys nothing at a 0.16 mm layer.
    """
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    out = []
    for u, v in poly:
        du, dv = u - cx, v - cy
        d = math.hypot(du, dv)
        if d < 1e-9:
            out.append((u, v))
            continue
        out.append((u - du / d * amount, v - dv / d * amount))
    return out


def placed_motifs(zj, zone, profile, wall_mm, start_angle_deg=None):
    """
    Every motif of a zone, resolved to (tool, u_centre_mm, v_centre_mm).

    Uses motifs.zone_layout for the placement rules (one row, half-pitch
    stagger, spandrel-lifted fillers) and converts angles back to arc length
    at the zone's own mid-height radius. Fillers keep their spandrel lift.
    """
    z0, z1 = zone["z_mm"]
    r_mid = profile((z0 + z1) / 2.0)
    circ = 2 * math.pi * r_mid
    lay = M.zone_layout(zone, r_mid)
    h = z1 - z0
    out = []
    for a, u in lay["discs"]:
        out.append((zone["tool"], u, h / 2.0))
    for a, u, tool, dv in lay["fillers"]:
        if tool is None:
            continue
        # a filler appears twice: upper and lower spandrel
        out.append((tool, u, h / 2.0 + dv))
        if h / 2.0 - dv > 0:
            out.append((tool, u, h / 2.0 - dv))
    return out, r_mid, circ


# --- FreeCAD side -------------------------------------------------------------

def build_motif_prisms(profile, zone, wall_mm, form, relief_mm=0.8,
                       z_band_bottom=None, verbose=False):
    """
    Build all the motif prisms for one zone as a list of Part solids.

    Requires FreeCAD.

    Each motif becomes a PRISM whose axis is the local surface normal: the
    polygon is traced twice, once at depth `r_from` and once at `r_to`, and
    the two rings are lofted and capped. Tracing the polygon once with
    alternating depths (the obvious mistake) yields a self-intersecting
    bowtie, not a prism.
    """
    import FreeCAD
    import Part

    z0, z1 = zone["z_mm"]
    if z_band_bottom is None:
        z_band_bottom = z0
    plist, r_mid, circ = placed_motifs(None, zone, profile, wall_mm)

    add, cut = [], []
    for tool, u, v in plist:
        outer, holes = M.for_tool(tool)
        depth = relief_mm if tool in M.DISC_TOOLS else relief_mm * 0.6
        a_list, s_list = split_add_subtract(
            motif_prism_polygons(form, outer, holes, depth, wall_mm))
        for lst, tag in ((a_list, "add"), (s_list, "cut")):
            for poly, r_from, r_to in lst:
                solid = _polygon_prism(FreeCAD, Part, profile, poly, u, v,
                                       z0, r_mid, r_from, r_to, wall_mm)
                if solid is None:
                    if verbose:
                        print("    skip motif (tool %s, v=%.1f)" % (tool, v))
                    continue
                (add if tag == "add" else cut).append(solid)
    return add, cut


def fuse_all(shapes):
    """
    Fuse many shapes in ONE pass via `shape.multiFuse([rest])`.

    ⚠️ Do not replace this with a loop of pairwise `fuse()`. That is O(n²),
    and fusing z15's 345 relief prisms that way wedged FreeCAD's GUI thread
    for 245 s+ (the RPC server reported state `stuck`) and needed a restart
    — twice in one session. `multiFuse` does a single BOP pass over the whole
    list, which is the operation that actually scales.

    Note the API: it is a METHOD on a shape taking the remaining shapes, not a
    `Part.multiFuse` function — the latter does not exist.
    """
    if not shapes:
        return None
    if len(shapes) == 1:
        return shapes[0]
    return shapes[0].multiFuse(list(shapes[1:])).removeSplitter()


def _polygon_prism(FreeCAD, Part, profile, poly, u_centre, v_centre, z0,
                   r_ref, r_from, r_to, wall_mm):
    """
    One prism from one polygon, built in the PLANE TANGENT to the cone.

    Why planar and not projected-per-vertex: if each vertex is projected onto
    the cone at its own z, the ring is a curved 3D curve and `Part.Face`
    rejects it ("Failed to create face from wire") because the polygon is not
    planar. The prism is therefore built flat, in a frame at the motif's
    centre, then rotated into place. Consequences, both acceptable:

      - the motif sits on its tangent plane, so on a curved surface its rim
        stands a little proud at the centre and a little sunken at the edge.
        For a d21 motif on an r=61 mm band that is 0.9 mm at the rim -- the
        plan already accepts this order of chord error for a stylised model
        (section 5.3: "chord error for a 25 mm motif on a 100 mm radius is
        0.8 mm; acceptable for a stylised model").
      - every boolean stays a plane-plane intersection, which is fast and
        robust, where a curved prism is neither.

    The frame: +Z is the outward surface normal, +X is up the cone's surface,
    +Y is tangential (the direction of increasing theta).
    """
    import math

    # the motif's centre on the surface, and the local frame there
    pc = G.project(u_centre, v_centre, z0, profile, wall_mm, r_ref=r_ref)
    theta = pc.theta
    a = math.atan(profile.drdz(pc.z))          # cone half-angle at the centre
    # outward normal in the (r, z) plane, and the surface's up direction
    n_r, n_z = math.cos(a), -math.sin(a)
    u_r, u_z = math.sin(a), math.cos(a)        # "up" along the surface
    # world directions: radial, tangential, axial
    rad = FreeCAD.Vector(math.cos(theta), math.sin(theta), 0.0)
    tan = FreeCAD.Vector(-math.sin(theta), math.cos(theta), 0.0)
    axis = FreeCAD.Vector(0.0, 0.0, 1.0)
    centre = rad * pc.r + axis * pc.z
    # frame axes as world vectors
    v_up = rad * u_r + axis * u_z              # +X of the motif frame
    v_tan = tan                                # +Y
    v_nrm = rad * n_r + axis * n_z             # +Z, outward

    def to_world(pu, pv, depth):
        return (centre + v_up * pv + v_tan * pu + v_nrm * depth)

    lo = [to_world(pu, pv, r_from) for (pu, pv) in poly]
    hi = [to_world(pu, pv, r_to) for (pu, pv) in poly]
    try:
        w_lo = Part.makePolygon(lo + [lo[0]])
        w_hi = Part.makePolygon(hi + [hi[0]])
        f_lo = Part.Face(w_lo)
        f_hi = Part.Face(w_hi)
        # a straight prism: extrude the base face along the normal
        vec = v_nrm * (r_to - r_from)
        prism = f_lo.extrude(vec)
        if prism.Volume > 1e-9:
            return prism
    except Exception:
        pass
    return None


# --- self-check (no FreeCAD) --------------------------------------------------

def _selfcheck():
    hp, zj = G.load()
    profile = G.Profile(hp["profile"])
    wall = hp["wall_thickness_mm"]
    zone = next(z for z in zj["zones"] if z["zone"] == 15)

    print("P3.5 coupon zone z15: %d x tool %d (%s), z %.1f..%.1f"
          % (zone["count"], zone["tool"], zone["name"], *zone["z_mm"]))
    plist, r_mid, circ = placed_motifs(None, zone, profile, wall)
    print("  motifs placed: %d discs + fillers = %d total" % (zone["count"], len(plist)))
    assert len(plist) >= zone["count"]

    # every motif must sit inside its zone vertically
    h = zone["z_mm"][1] - zone["z_mm"][0]
    for tool, u, v in plist:
        assert -1e-9 <= v <= h + 1e-9, "motif at v=%.2f is outside the zone (h=%.1f)" % (v, h)

    # the three forms must differ, and each must be internally consistent
    outer, holes = M.for_tool(15)
    print("\n  tool 15 = %d rings, d%.0f" % (M.DISC_TOOLS[15][0], M.DISC_TOOLS[15][1]))
    print("  form            polygons   depth range (mm, +outward)")
    for form in FORMS:
        polys = motif_prism_polygons(form, outer, holes, 0.8, wall)
        depths = [(a, b) for _, a, b, _ in polys]
        lo = min(a for a, _ in depths)
        hi = max(b for _, b in depths)
        print("  %-15s %-10d %+.2f .. %+.2f" % (form, len(polys), lo, hi))
        assert polys, form

    # relief must NOT reach the inner surface, but MUST overlap the wall, and
    # must RECESS the troughs (a plain "add every ring" buries them).
    rl = motif_prism_polygons("relief", outer, holes, 0.8, wall)
    rl_add, rl_cut = split_add_subtract(rl)
    assert rl_cut, "the relief form does not recess any trough -- the rings "\
                   "would be buried inside the boss"
    assert len(rl_cut) == len(holes), \
        "expected one trough cut per ring, got %d for %d rings" % (len(rl_cut), len(holes))
    assert len(rl_add) == len(holes) + 1, \
        "expected the disc plus one restored ring per trough, got %d adds" % len(rl_add)
    # every ADD must embed so it fuses; every CUT must descend from above the
    # ridge tops so it actually removes material
    for _, a, b, op in rl:
        if op == "add":
            assert a < 0.0, "a relief ADD does not embed (a=%.2f)" % a
            assert b <= 0.8 + 1e-9, "a relief ADD rises past the relief height"
        else:
            assert a > 0.0, "a trough cut starts below the surface, so it cuts nothing (a=%.2f)" % a
            assert b > a, "a trough cut has depth <= 0"
    print("  relief: 1 disc + %d trough cuts + %d restored rings"
          % (len(rl_cut), len(rl_add) - 1))
    # window must be one clean through-cut
    w = motif_prism_polygons("window", outer, holes, 0.8, wall)
    assert len(w) == 1, "a window should be one clean hole, got %d" % len(w)
    assert w[0][1] < 0 < w[0][2], "the window is not a through-cut"
    # relief_window must keep a raised rim AND a through field, and the rim
    # must NOT reach through -- otherwise it is not a rim, it is a wider hole
    add_p, sub_p = split_add_subtract(
        motif_prism_polygons("relief_window", outer, holes, 0.8, wall))
    assert len(add_p) == 1 and len(sub_p) == 1, \
        "relief_window should be one raised rim + one through core, got %d+%d" \
        % (len(add_p), len(sub_p))
    assert add_p[0][1] < 0 <= add_p[0][2] <= 0.8 + 1e-9, \
        "the relief_window rim must embed (a<0) and not reach through (b<=0.8)"
    assert sub_p[0][1] < 0, "the relief_window core is not a through-cut"
    print("  relief_window: rim %+.2f..%+.2f (add), core %+.2f..%+.2f (cut)"
          % (add_p[0][1], add_p[0][2], sub_p[0][1], sub_p[0][2]))
    # the rim must be an annulus: the inset core is strictly inside the outline
    in_u = [p[0] for p in sub_p[0][0]]
    out_u = [p[0] for p in add_p[0][0]]
    assert max(in_u) < max(out_u) and min(in_u) > min(out_u), \
        "the RW core is not inset inside the rim"
    print("  rim retains %.2f mm of material at each side"
          % (max(out_u) - max(in_u)))

    # ⚠️ an ADDITIVE prism that starts exactly at depth 0.0 only TOUCHES the
    # wall: the fused result came back as 31 disjoint solids with a common
    # volume of 0.03 mm3. Every additive prism must embed.
    for form in ("relief", "relief_window"):
        for poly, a, b in split_add_subtract(
                motif_prism_polygons(form, outer, holes, 0.8, wall))[0]:
            assert a < 0.0, \
                "%s: an additive prism starts at depth %.2f, so it butts the "\
                "wall instead of overlapping it" % (form, a)
    print("  every additive prism embeds below the surface: OK")

    # the window must be the FULL motif, not the inset one
    w = motif_prism_polygons("window", outer, holes, 0.8, wall)
    assert len(w) == 1, "a window should be one clean hole, got %d" % len(w)
    xs = [p[0] for p in w[0][0]]
    print("  window spans u %.2f .. %.2f mm (d%.0f motif)"
          % (min(xs), max(xs), M.DISC_TOOLS[15][1]))

    # projection: a motif's angular width is constant, and its u is arc length
    p1 = G.project(0.0, h / 2, zone["z_mm"][0], profile, wall, r_ref=r_mid)
    p2 = G.project(circ / zone["count"], h / 2, zone["z_mm"][0], profile, wall, r_ref=r_mid)
    sep_deg = math.degrees(p2.theta - p1.theta)
    print("\n  one pitch = %.4f deg (expect %.4f)" % (sep_deg, 360.0 / zone["count"]))
    assert abs(sep_deg - 360.0 / zone["count"]) < 1e-9

    # the coupon must fit the bed with room for the fit-test trio
    bb_d = 2 * max(profile(z) for z in (zone["z_mm"][0], zone["z_mm"][1]))
    print("  coupon outer diameter %.1f mm -> fits the 256 mm bed: %s"
          % (bb_d + 2 * 1.0, bb_d + 2 * 1.0 < 256))

    print("\nmotif_features self-check: all passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selfcheck", action="store_true")
    ap.parse_args()
    _selfcheck()


# --- the coupon -----------------------------------------------------------------

def build_motif_ops(profile, zone, wall_mm, form, relief_mm):
    """
    All motif prisms for a zone, as an ordered list of ("add"|"cut", shape).

    Grouped BY TIER, not per motif: every motif emits its prisms in the same
    order (base, then trough-cut / ring-add pairs), so instead of 45 x 14
    individual booleans the tiers are batched -- one multiFuse or one cut per
    tier across the whole zone. That is the difference between a usable build
    and a 20-minute one.

    Requires FreeCAD.
    """
    import FreeCAD
    import Part

    z0 = zone["z_mm"][0]
    plist, r_mid, circ = placed_motifs(None, zone, profile, wall_mm)

    # tier -> list of shapes, in emission order per motif
    tiers = []
    for tool, u, v in plist:
        outer, holes = M.for_tool(tool)
        depth = relief_mm if tool in M.DISC_TOOLS else relief_mm * 0.6
        polys = motif_prism_polygons(form, outer, holes, depth, wall_mm)
        for k, (poly, r_from, r_to, op) in enumerate(polys):
            while len(tiers) <= k:
                tiers.append({"add": [], "cut": []})
            s = _polygon_prism(FreeCAD, Part, profile, poly, u, v, z0, r_mid,
                               r_from, r_to, wall_mm)
            if s is not None:
                tiers[k][op].append(s)

    ops = []
    for tier in tiers:
        if tier["cut"]:
            ops.append(("cut", fuse_all(tier["cut"])))
        if tier["add"]:
            ops.append(("add", fuse_all(tier["add"])))
    return ops


def build_coupon(hp, zj, form, zone_no=15, relief_mm=None, verbose=True):
    """
    Build one P3.5 coupon: the band for a zone with its motifs in one form.

    Returns (Part.Solid, info dict). Requires FreeCAD.

    The three coupons for a zone differ ONLY in `form`; the profile, the wall
    and the placement are identical, which is what makes the print comparison
    meaningful (plan section 6.3).
    """
    import band_geometry as G
    import build_goldhat as B
    import time

    profile = G.Profile(hp["profile"])
    wall = hp["wall_thickness_mm"]
    relief = relief_mm if relief_mm is not None else hp["symbol_relief_mm"]
    zone = next(z for z in zj["zones"] if z["zone"] == zone_no)
    z0, z1, _ = G.band_span(hp, "z%d" % zone_no)

    t0 = time.time()
    band, _ = B.make_band_solid(profile, z0, z1, wall)

    # ⚠️ ORDER MATTERS. The relief form recesses a trough and then adds the
    # inner ring back, so cuts and adds must interleave in the order emitted.
    # Fusing all adds and then all cuts (the obvious approach) would erase the
    # restored rings and undo the troughs. build_motif_ops() preserves the
    # order while still batching each tier into one boolean.
    ops = build_motif_ops(profile, zone, wall, form, relief)
    t_prisms = time.time() - t0
    out = band
    for tag, shape in ops:
        out = (out.fuse(shape) if tag == "add" else out.cut(shape))
        out = out.removeSplitter()

    n_add = sum(1 for t, _ in ops if t == "add")
    n_cut = sum(1 for t, _ in ops if t == "cut")
    info = {"form": form, "zone": zone_no, "z": (z0, z1), "wall_mm": wall,
            "relief_mm": relief, "add_count": n_add, "cut_count": n_cut,
            "bare_volume": band.Volume, "volume": out.Volume,
            "solids": len(out.Solids), "valid": out.isValid(),
            "build_s": t_prisms}
    if verbose:
        print("  %-14s %8.1f mm3  (%+7.1f vs bare)  solids=%d valid=%s  %.1fs"
              % (form, out.Volume, out.Volume - band.Volume,
                 len(out.Solids), out.isValid(), t_prisms))
    return out, info
