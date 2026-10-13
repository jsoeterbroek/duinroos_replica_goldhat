#!/usr/bin/env python3
"""
build_goldhat.py — turn the P3 geometry kernel into actual solid geometry.

Run from the repo root, either inside FreeCAD's console or via the MCP server:

    python3 -c "exec(open('scripts/build_goldhat.py').read())"

The heavy lifting (profile, section, projection) is in band_geometry.py and is
testable without FreeCAD. This file only does the OCCT work, so a crash here is
a FreeCAD problem and a crash there is a maths problem.
"""

import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import band_geometry as G                                    # noqa: E402

import FreeCAD                                               # noqa: E402
import Part                                                  # noqa: E402


def make_band_solid(profile, z0, z1, wall_mm, n=48, defl=0.05):
    """
    Revolve a closed (r, z) section into a ring solid.

    The section is a polyline; revolving it about the Z axis gives the wall.

    `n` is the number of segments along the section. 48 over a 14-38 mm band
    is far finer than a 0.16 mm layer: the chord error is r*(1-cos(pi/N)) on
    the revolve and negligible along the short section.

    `defl` caps the triangulation deviation when the shape is meshed/exported.
    OCCT's default circle resolution is what made the first z13 STL 23 MB
    (91,704 facets, ~478 segments around a ⌀123 ring). At a 0.16 mm layer a
    0.05 mm chord deviation is invisible, and it cuts the facet count roughly
    tenfold -- which matters across 22 bands.
    """
    pts = G.section_polyline(profile, z0, z1, n=n, wall_mm=wall_mm)
    vecs = [FreeCAD.Vector(r, 0.0, z) for r, z in pts]
    vecs.append(vecs[0])                                     # close the loop
    wire = Part.makePolygon(vecs)
    face = Part.Face(wire)
    solid = face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360.0)
    return solid, face


def _facets(shape, defl=0.05):
    """A shape's tessellation as absolute point-triples.

    `Mesh.addFacets(shape.tessellate(...))` -- passing the raw
    (vertices, indices) tuple -- is a TRAP: the first call works and every
    later call is silently dropped (verified on FreeCAD 1.1.4: two boxes
    gave 12 facets instead of 24, with a bbox that had grown but no new
    triangles). A single-shape export hides it; a multi-part plate does not.
    It is why stl/test/clearance_ladder.stl contained only ONE part. Expand
    to point-triples and the accumulation is correct.
    """
    v, f = shape.tessellate(defl)
    return [(v[i], v[j], v[k]) for i, j, k in f]


def _edge_key(p):
    """A weldable vertex key: coordinates rounded to 1e-4 mm."""
    return (round(p.x, 4), round(p.y, 4), round(p.z, 4))


def nonmanifold_edges(tris):
    """
    Edges of a triangle soup that are not shared by exactly two faces.

    ⚠️ **A valid OCCT solid can still tessellate to a non-manifold mesh, and
    `Shape.isValid()` will not say so.** The case that bit this project: the
    stacked-joint keyway cutter's face lay exactly ON the hub's bore cylinder
    -- a TANGENT contact, zero volume, invisible to `isValid()` and the
    `len(solids) == 1` check, reported by Bambu Studio as "3 non-manifold
    edges" (one per tile). It is the same failure family as the section
    11.2 rule, applied to a *cut* instead of a boss: **overlap, never
    coincide.** A slicer is the first thing that sees it, so the exporter now
    checks every mesh rather than trusting `isValid()`.
    """
    counts = Counter()
    for tri in tris:
        k = [_edge_key(p) for p in tri]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            counts[tuple(sorted((k[a], k[b])))] += 1
    return [(e, c) for e, c in counts.items() if c != 2]


def export_stl(shape, path, defl=0.05, check=True):
    """Export with an explicit deviation, instead of OCCT's default.

    `Shape.exportStl` takes no tolerance, so mesh explicitly and write the
    mesh. This is the difference between ~2 MB and ~23 MB per band.

    `shape` may be one shape or a list of them (a coupon plate). Multi-part
    plates are why the accumulation guard below exists. `check` asserts the
    mesh is 2-manifold -- see `nonmanifold_edges` for why `isValid()` is not
    enough.
    """
    import Mesh
    shapes = shape if isinstance(shape, (list, tuple)) else [shape]
    mesh = Mesh.Mesh()
    tris_all = []
    n = 0
    for s in shapes:
        tris = _facets(s, defl)
        mesh.addFacets(tris)
        tris_all.extend(tris)
        n += len(tris)
    assert mesh.CountFacets == n, \
        "mesh lost facets: %d of %d (see _facets)" % (mesh.CountFacets, n)
    if check:
        bad = nonmanifold_edges(tris_all)
        assert not bad, (
            "export_stl: %d non-manifold edge(s) -- the mesh is not 2-manifold "
            "and a slicer will flag it. First: %s. See nonmanifold_edges()."
            % (len(bad), bad[0][0]))
    mesh.write(path)
    return mesh.CountFacets


def _revolve_section(pts):
    """Revolve a closed (r, z) polygon about the Z axis."""
    vecs = [FreeCAD.Vector(r, 0.0, z) for r, z in pts]
    vecs.append(vecs[0])
    face = Part.Face(Part.makePolygon(vecs))
    return face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360.0)


# The Trennband collar's inner face, measured inward from the outer profile.
# It is the surface the registration lip rides against; both this and the lip
# are built as polylines FOLLOWING r(z) so the clearance stays constant all
# the way down a tapering collar (a straight chord would wander by the pchip
# sagitta and eat into the 0.25 mm clearance).
COLLAR_INSET = 0.6


def make_trennband_ridge(profile, z0, h, wall_mm, proud=1.0, embed=COLLAR_INSET,
                         lap=1.0, n=16):
    """
    The Trennband ridge at a band's lower edge: a 1 mm proud collar.

    Built as a separate ring and fused, rather than folded into the section
    polyline, so the ridge stays a swappable design detail (plan section 4
    Option A) and the band section stays a clean two-surface wall.

    `embed` makes the ring overlap the wall radially instead of butting it:
    a collar whose inner face stopped exactly on the outer surface would meet
    the band along a single circle (a LINE contact that OCCT cannot fuse).

    `lap` carries the ring `lap` mm PAST the joint plane and into the band's
    own wall, tapering from `proud` back to the profile so there is no ledge.
    A butt at a single plane is a FACE contact -- two coincident annuli -- and
    OCCT returns it as two disjoint solids even though the faces match (this
    is why the first fit-test trio reported `solids=2`).  The lap gives the
    fuse a real volume and the collar a 1 mm blend into the wall.
    """
    z_join = z0 + h
    z_end = z_join + lap
    zs = [z0 + (h + lap) * i / n for i in range(n + 1)]

    def outer_r(z):
        if z <= z_join:
            return profile(z) + proud
        f = (z - z_join) / lap              # 0 -> 1 across the blend
        return profile(z) + proud * (1.0 - f)

    outer = [(outer_r(z), z) for z in zs]
    inner = [(profile(z) - embed, z) for z in reversed(zs)]
    return _revolve_section(outer + inner)


def make_registration_lip(profile, z_edge, wall_mm, lip_h=6.0, clearance=0.25,
                          collar_inset=COLLAR_INSET, embed=2.0, n=16):
    """
    The registration spigot: a ring on the INSIDE of the band's LOWER edge
    that slips into the Trennband collar of the band below.

    ⚠️ **SUPERSEDED by the flat stack + keyed spine (§11.4)**, which the printed
    coupon confirmed on 2026-10-13. Kept only as the P3 record.

    `z_edge` is the band's LOWER edge -- the larger-z end, i.e. the plane
    where this band meets the band below.  (The zone loop hands `z0` first,
    but z increases DOWNWARD on this object: z0 is the apex side.  The lip
    must be at z1.)

    Sizing is the whole point, and it is NOT "the wall, minus the clearance":

      * the band below carries its own Trennband collar across this joint,
        and that collar's inner face sits `collar_inset` (0.6 mm) inside the
        outer profile -- so the neighbour's bore here is profile(z) - 0.6,
        not profile(z) - wall (2.0).
      * the lip must ride just inside that bore:
            r_outer(z) = profile(z) - collar_inset - clearance
        Because collar_inset < wall, this is FATTER than this band's own bore
        (profile - wall).  That is deliberate and is what makes the lip
        overlap this band's own wall (a real fuse, not a line contact) while
        still clearing the collar of the band below.
      * it follows r(z) rather than being a cylinder, so it cannot wedge on
        the tapering Schaft (r falls ~0.6-1.2 mm across a 9 mm collar).

    The lip starts `embed` mm ABOVE z_edge, inside this band's own wall, and
    runs `lip_h` mm BELOW it, into the neighbour's collar hollow.  `lip_h`
    is kept under the collar height so the lip does not reach the neighbour's
    narrower zone bore.
    """
    zs = [z_edge - embed + (embed + lip_h) * i / n for i in range(n + 1)]
    outer = [(profile(z) - collar_inset - clearance, z) for z in zs]
    inner = [(r - wall_mm, z) for r, z in reversed(outer)]
    return _revolve_section(outer + inner)


def build(band_id="z13", out_dir=None, verbose=True):
    """
    The P3 LAP band: shell + Trennband ridge + registration lip.

    ⚠️ **Superseded** by `build_stacked` (the flat stack, §11.4) once the
    stacked-joint coupon was printed and judged (2026-10-13). Kept as the P3
    record and because `build_coupons.py` still uses it for the z13/z14/z15
    fit trio; new work uses `build_stacked`.
    """
    hp, zj = G.load()
    profile = G.Profile(hp["profile"])
    wall = hp["wall_thickness_mm"]
    z0, z1, kind = G.band_span(hp, band_id)

    if verbose:
        print("building %s: z %.1f .. %.1f (%s), wall %.1f mm"
              % (band_id, z0, z1, kind, wall))

    solid, face = make_band_solid(profile, z0, z1, wall)
    # --- Trennband ridge: the tb immediately BELOW this zone
    idx = int(band_id[1:])
    tb = next((r for r in hp["rings"]
               if r["id"] == "tb%d" % (idx - 1) and r["kind"] == "trennband"), None)
    parts = [solid]
    if tb is not None:
        zb = z0 - tb["h"]
        ridge = make_trennband_ridge(profile, zb, tb["h"], wall, proud=1.0)
        parts.append(ridge)
        if verbose:
            print("  + Trennband ridge tb%d: z %.1f .. %.1f, 1.0 mm proud (1 mm lap)"
                  % (idx - 1, zb, zb + tb["h"] + 1.0))

    # --- registration lip, inside the LOWER edge (z1 -- see make_registration_lip)
    if idx > 1 and tb is not None:
        lip = make_registration_lip(profile, z1, wall,
                                   lip_h=hp["registration_lip_mm"],
                                   clearance=hp["registration_clearance_mm"])
        parts.append(lip)
        if verbose:
            r_out = profile(z1) - COLLAR_INSET - hp["registration_clearance_mm"]
            print("  + registration lip: z %.1f..%.1f, outer r %.3f (d %.2f), "
                  "%s clearance into tb%d"
                  % (z1 - 2.0, z1 + hp["registration_lip_mm"], r_out, 2 * r_out,
                     hp["registration_clearance_mm"], idx))

    band = parts[0]
    for p in parts[1:]:
        band = band.fuse(p)
    band = band.removeSplitter()

    if verbose:
        bb = band.BoundBox
        print("  solid: volume %.1f mm3, bbox %.1f x %.1f x %.1f"
              % (band.Volume, bb.XLength, bb.YLength, bb.ZLength))
        print("  watertight: %s" % band.isValid())

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "%s.stl" % band_id)
        facets = export_stl(band, path)
        if verbose:
            print("  wrote %s  (%d facets, %.1f MB)"
                  % (path, facets, os.path.getsize(path) / 1e6))

    return band


# --- P4: the flat-stacked band ------------------------------------------------
# seat (flat) + outer wall + 4-arm spider + hub bore/keyway, driven entirely by
# data/hat_parameters.json -> "joint". The coupon (scripts/
# build_stacked_joint_coupon.py) validates the JOINT mechanics at ~1:1 before
# this is used for the 22 parts; this function is the real profile's version.
# The wall/seat section is HORIZONTALLY offset (flat top and bottom), unlike
# the lap band's normal offset, because a flat seat is the whole point of the
# design: it stacks on a bed-flat face instead of on a protruding lip.

def _box(l, w, h, x, y, z):
    return Part.makeBox(l, w, h, FreeCAD.Vector(x, y, z))


def make_spoke(profile, z0, z1, hub_r, wall, spoke_w, embed_hub=1.0,
               embed_wall=1.0, n=12):
    """
    One radial rib, as a planar-faced solid of constant tangential width.

    The rib's OUTER EDGE follows r(z), at `profile(z) - wall + embed_wall`: past
    the wall's inner face (so it overlaps and fuses) but always short of the
    outer surface (so it can never break through). A straight box cannot do
    that on a tapering band -- it misses the wall at one end and pokes through
    it at the other. Built flat in the XZ plane and rotated into place, so every
    boolean is a plane/cylinder intersection (the section 11.2 trick).
    """
    r_out = lambda z: profile(z) - wall + embed_wall          # noqa: E731
    pts = [FreeCAD.Vector(hub_r - embed_hub, 0.0, z1),
           FreeCAD.Vector(hub_r - embed_hub, 0.0, z0)]
    for i in range(n + 1):
        z = z0 + (z1 - z0) * i / n
        pts.append(FreeCAD.Vector(r_out(z), 0.0, z))
    face = Part.Face(Part.makePolygon(pts + [pts[0]]))
    solid = face.extrude(FreeCAD.Vector(0.0, spoke_w, 0.0))
    solid.translate(FreeCAD.Vector(0.0, -spoke_w / 2.0, 0.0))
    return solid


# Fig. 21 tool numbers motifs.py can build (for_tool supports exactly these).
_SUPPORTED_TOOLS = frozenset({4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})


def _special_ops(profile, zone, wall, form, relief):
    """
    Motif operations for a zone whose ornament is a LIST of specials rather
    than one Fig.21 disc -- today only zone 5 (19 crescent + 19 eye), placed
    alternately around the zone (Menghin's crescent + eye pairing).

    Same tier batching and order discipline as motif_features.build_motif_ops,
    so an RW trough/ring interleave still holds. Requires FreeCAD.
    """
    import motifs as MM
    import motif_features as F
    z0, z1 = zone["z_mm"]
    h = z1 - z0
    r_mid = profile(0.5 * (z0 + z1))
    tools = []
    for m in zone["motifs"]:
        tools += [m["tool"]] * m["count"]
    n = len(tools)
    tiers = []
    for j, tool in enumerate(tools):
        u = (j + 0.5) * 2.0 * math.pi * r_mid / n
        outer, holes = MM.for_tool(tool)
        polys = F.motif_prism_polygons(form, outer, holes, relief * 0.6, wall)
        for k, (poly, r_from, r_to, op) in enumerate(polys):
            while len(tiers) <= k:
                tiers.append({"add": [], "cut": []})
            s = F._polygon_prism(FreeCAD, Part, profile, poly, u, h / 2.0,
                                 z0, r_mid, r_from, r_to, wall)
            if s is not None:
                tiers[k][op].append(s)
    ops = []
    for tier in tiers:
        if tier["cut"]:
            ops.append(("cut", F.fuse_all(tier["cut"])))
        if tier["add"]:
            ops.append(("add", F.fuse_all(tier["add"])))
    return ops


def part_span(hp, band_id):
    """
    The z-span and rings of PART `band_id`.

    Operator rule (2026-10-13): the Trennband fuses to the band's **UPPER**
    edge. z increases downward, so "upper" is the smaller-z side, and part N
    runs from the end of zone N-1 down to the end of zone N. That includes
    tb(N-1), any intercalary ring in between (the 18 mm cuff before z17), and
    zone N -- and leaves zone 1 as the bare apex cone (no Trennband above it).
    """
    idx = int(band_id[1:])
    ends, z = {}, 0.0
    for r in hp["rings"]:
        z += r["h"]
        if r["id"].startswith("z") and r["id"] != "z":
            ends[r["id"]] = z
    zB = ends["z%02d" % idx]
    zA = 0.0 if idx == 1 else ends["z%02d" % (idx - 1)]
    rings, z = [], 0.0
    for r in hp["rings"]:
        lo, hi = z, z + r["h"]
        z = hi
        if lo >= zA - 1e-9 and hi <= zB + 1e-9:
            rings.append(r)
    return zA, zB, rings


def _ridge_outer(profile, zA, ridge_h, proud=1.0, blend=1.0):
    """The outer radius with a 1 mm Trennband ridge over the part's upper
    `ridge_h` mm, eased back to the profile over `blend` mm (a knife-edge step
    would be a stress riser and a slicer artefact)."""
    def r_out(z):
        if ridge_h <= 0.0:
            return profile(z)
        d = z - zA
        if d <= ridge_h:
            return profile(z) + proud
        if d <= ridge_h + blend:
            return profile(z) + proud * (1.0 - (d - ridge_h) / blend)
        return profile(z)
    return r_out


def build_stacked(band_id="z13", out_dir=None, verbose=True, motifs=True):
    """
    One P4 PART: the zone + its Trennband (upper edge) + any intercalary ring,
    as outer wall + hub + spider + keyway, with the motif form applied.

    The wall/seat section is HORIZONTALLY offset (flat top and bottom), so the
    seat is bed-flat: that is the point of the flat stack. The Trennband ridge
    is an outward bump only -- the inner surface stays at profile(z) - wall, so
    the ridge reads as a thicker band and the LED cavity does not narrow.

    Motif form comes from data (motif_form); zones whose ornament is a SPECIAL
    (1 and 5 -- star and crescent/eye) are handled: zone 5 via its motif list,
    zone 2 via tool 6; only zone 1's continuous eight-rayed star is still plain.
    """
    hp, zj = G.load()
    profile = G.Profile(hp["profile"])
    wall = hp["wall_thickness_mm"]
    zA, zB, rings = part_span(hp, band_id)
    ridge_h = rings[0]["h"] if rings and rings[0]["kind"] == "trennband" else 0.0
    r_out = _ridge_outer(profile, zA, ridge_h)
    zone = next((z for z in zj["zones"] if z["zone"] == int(band_id[1:])), None)
    form = hp.get("motif_form") or "relief"
    relief = hp["symbol_relief_mm"]
    jt = hp["joint"]
    assert jt["type"] == "stacked_spine", "hat_parameters.joint is not stacked_spine"
    bore_r = jt["hub_bore_mm"] / 2.0
    hub_r = bore_r + jt["hub_wall_mm"]
    n_spokes, spoke_w = jt["spokes"], jt["spoke_w_mm"]
    kd, kw = jt["keyway_depth_mm"], jt["keyway_w_mm"]

    if verbose:
        print("building %s: z %.1f .. %.1f (%s), wall %.1f mm, ridge %.1f mm"
              % (band_id, zA, zB, "+ ".join(r["id"] for r in rings), wall, ridge_h))

    # --- outer wall, flat top and bottom (the seat). Zone 1 is a cone from
    # r=0, so its ring would vanish (inner radius negative) near the tip: build
    # the apex parts as a SOLID cone with a blind bore for the spine, which is
    # the plan's "solid or rim-only" apex (section 11.4).
    zs = [zA + (zB - zA) * i / 64 for i in range(65)]
    z_hub = next((z for z in zs if profile(z) >= bore_r + 2.0), None)
    solid_apex = z_hub is None or min(profile(z) for z in zs) - wall < hub_r + 1.0

    if solid_apex:
        # revolved solid: tip point -> outer profile -> axis at zB
        sec = [(0.0, zA)] + [(r_out(z), z) for z in zs[1:]] + [(0.0, zB)]
        parts = [_revolve_section(sec)]
    else:
        wall_sec = ([(r_out(z), z) for z in zs] +
                    [(max(profile(z) - wall, 0.0), z) for z in reversed(zs)])
        parts = [_revolve_section(wall_sec)]
        # hub (a tube, so the spine passes through and the wire can too)
        parts.append(_revolve_section([(bore_r, zA), (hub_r, zA),
                                       (hub_r, zB), (bore_r, zB)]))
        # spider: ribs from hub to wall. Between them is the LED cavity.
        for k in range(n_spokes):
            s = make_spoke(profile, zA, zB, hub_r, wall, spoke_w)
            s.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1),
                     360.0 * k / n_spokes)
            parts.append(s)

    band = parts[0]
    for p in parts[1:]:
        band = band.fuse(p)
    band = band.removeSplitter()

    # --- motifs (RW etc.), in the order motif_features emits them: the trough
    # cut / ring add interleaving is load-bearing (section 11.2).
    if motifs and zone and zone.get("motifs"):
        ops = _special_ops(profile, zone, wall, form, relief)
    elif motifs and zone and zone.get("tool") in _SUPPORTED_TOOLS:
        import motif_features as F
        ops = F.build_motif_ops(profile, zone, wall, form, relief)
    else:
        ops = []
        if verbose:
            why = ("zone not in zones.json" if not zone else
                   "continuous %s -- no repeatable motifs" % zone.get("primitive"))
            print("  motifs: skipped (%s)" % why)
    for tag, shape in ops:
        band = (band.fuse(shape) if tag == "add" else band.cut(shape))
        band = band.removeSplitter()

    # --- keyway: a slot in the hub bore, between two spokes. It starts 1 mm
    # inside the bore void -- a cutter face flush with the bore cylinder is
    # TANGENT to it and leaves non-manifold edges (section 11.4).
    kz0 = z_hub if solid_apex else zA
    if solid_apex:
        bore = Part.makeCylinder(bore_r, zB + 1.0 - kz0,
                                 FreeCAD.Vector(0.0, 0.0, kz0))
        band = band.cut(bore).removeSplitter()
    key = _box(kd + 1.0, kw, (zB - kz0) + 2.0, bore_r - 1.0, -kw / 2.0, kz0 - 1.0)
    key.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1),
               180.0 / n_spokes)
    band = band.cut(key).removeSplitter()

    # --- label on the hidden seat annulus (wider on a solid apex: bore..rim)
    if solid_apex:
        r_mid = 0.5 * (bore_r + profile(zB))
        width = profile(zB) - bore_r
    else:
        r_mid, width = profile(zB) - wall / 2.0, wall
    size = G.fit_ring_label(band_id, r_mid, width)
    if size:
        band = G.engrave_ring_label(band, band_id, r_mid, zB, size)
    elif verbose:
        print("  NOTE: %s does not fit the %.1f mm seat annulus -- unlabelled"
              % (band_id, wall))

    if verbose:
        bb = band.BoundBox
        print("  solid: volume %.1f mm3, solids=%d, bbox %.1f x %.1f x %.1f"
              % (band.Volume, len(band.Solids), bb.XLength, bb.YLength, bb.ZLength))
        print("  watertight: %s, %s"
              % (band.isValid(),
                 ("SOLID apex, bore d%.1f, keyway %.1f x %.1f, no spider"
                  % (2 * bore_r, kw, kd)) if solid_apex else
                 ("hub bore d%.1f, keyway %.1f x %.1f, %d spokes, form %s"
                  % (2 * bore_r, kw, kd, n_spokes, form))))

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "%s_stacked.stl" % band_id)
        facets = export_stl(band, path)          # asserts 2-manifold
        if verbose:
            print("  wrote %s  (%d facets, %.1f MB)"
                  % (path, facets, os.path.getsize(path) / 1e6))
    return band


# --- P4: the Krempe plate (zones 20/21) ---------------------------------------

def _krempe_z(hp, r):
    """
    The Krempe's TOP surface at radius r.

    The brim SITS ON the Kalottenfuss: its underside is flush with z19's top
    (z=738) at the inner edge and rises to 745-thickness at the outer edge, so
    the top runs 740 -> 745 and the plate never dips below 738. (Making the top
    run 738 -> 745 with the thickness below it put the underside at 736, 2 mm
    into z19 -- a real clash when stacked.)
    """
    k, t = hp["krempe"], hp["wall_thickness_mm"]
    return (k["z_inner_mm"] + t + (r - k["r_inner_mm"])
            / (k["r_outer_mm"] - k["r_inner_mm"])
            * (k["z_outer_mm"] - k["z_inner_mm"] - t))


def _revolve_section_angle(pts, angle_deg, n=64):
    """Revolve a closed (r, z) polygon about Z by `angle_deg` (a wedge)."""
    vecs = [FreeCAD.Vector(r, 0.0, z) for r, z in pts]
    vecs.append(vecs[0])
    return Part.Face(Part.makePolygon(vecs)).revolve(
        FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), angle_deg)


def _plate_prism(poly, r_c, phi_rad, r_from, r_to, hp):
    """
    One motif prism on the Krempe's nearly-flat top face.

    Same construction as motif_features._polygon_prism (build flat in a local
    frame, extrude along the local normal, keep every boolean plane/plane), but
    the frame is a PLATE frame, not the side-cone frame: the Krempe is not on
    r(z), so G.project does not apply.
    """
    k = hp["krempe"]
    beta = math.atan((_krempe_z(hp, k["r_outer_mm"]) - _krempe_z(hp, k["r_inner_mm"]))
                     / (k["r_outer_mm"] - k["r_inner_mm"]))
    rad = FreeCAD.Vector(math.cos(phi_rad), math.sin(phi_rad), 0.0)
    tan = FreeCAD.Vector(-math.sin(phi_rad), math.cos(phi_rad), 0.0)
    up = rad * math.cos(beta) + FreeCAD.Vector(0.0, 0.0, math.sin(beta))
    nrm = rad * (-math.sin(beta)) + FreeCAD.Vector(0.0, 0.0, math.cos(beta))
    centre = rad * r_c + FreeCAD.Vector(0.0, 0.0, _krempe_z(hp, r_c))
    lo = [centre + up * pv + tan * pu + nrm * r_from for (pu, pv) in poly]
    try:
        prism = Part.Face(Part.makePolygon(lo + [lo[0]])).extrude(
            nrm * (r_to - r_from))
    except Exception:
        return None
    return prism if prism.Volume > 1e-9 else None


def _fuse_shapes(shapes):
    if len(shapes) == 1:
        return shapes[0]
    return shapes[0].multiFuse(shapes[1:])


def _orient_for_bed(shape, step_deg=3.0):
    """
    Rotate a shape about Z to its smallest footprint.

    A 120-degree sector of this annulus is congruent at every 120 degrees, but
    its axis-aligned bbox is not: exported in place, sector b measured
    103 x 261 mm -- 5 mm past the 256 mm bed -- while a and c measured
    226 x 151. Rotating all three to the same relative minimum fixes it, and
    is what a slicer's auto-arrange would do anyway. Rotating about Z keeps
    the plate flat for printing.
    """
    best = None
    d = 0.0
    while d < 360.0:
        s = shape.copy()
        s.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), d)
        bb = s.BoundBox
        m = max(bb.XLength, bb.YLength)
        if best is None or m < best[0]:
            best = (m, s)
        d += step_deg
    return best[1]


def build_krempe(out_dir=None, verbose=True):
    """
    The Krempe plate: zone 20 (54 x d12 @ r107) and zone 21 (47 x d15 @ r132)
    as concentric RW motif rings on one shallow annular plate (r 94.5->150.5,
    z 738->745), then SPLIT into `krempe.sectors` radial sectors.

    Operator decision (2026-10-13): a seam is allowed to cut a motif -- the two
    halves meet when the sectors are assembled. No phase avoids all seams at
    once (47 x d15 on an 829 mm ring leaves 2.6 mm gaps, 1.15 deg), so option
    (a) is the honest one. Returns the list of sector shapes.
    """
    import motifs as MM
    import motif_features as F
    hp, zj = G.load()
    k = hp["krempe"]
    sectors = k["sectors"]
    thickness = hp["wall_thickness_mm"]
    form = hp.get("motif_form") or "relief"
    relief = hp["symbol_relief_mm"]

    # --- the full plate (top surface + vertical thickness below)
    n = 96
    rs = [k["r_inner_mm"] + (k["r_outer_mm"] - k["r_inner_mm"]) * i / n
          for i in range(n + 1)]
    sec = ([(r, _krempe_z(hp, r)) for r in rs] +
           [(r, _krempe_z(hp, r) - thickness) for r in reversed(rs)])
    plate = _revolve_section(sec)

    # --- motifs, batched by operation (adds first, then the through-cuts; for
    # RW the inset only touches its own disc, so the order is equivalent and
    # 200 individual booleans become a handful)
    adds, cuts = [], []
    for ring in k["rings"]:
        zone = next(z for z in zj["zones"] if z["zone"] == ring["zone"])
        tool, cnt, r_c = zone["tool"], zone["count"], ring["r_mid_mm"]
        outer, holes = MM.for_tool(tool)
        depth = relief if tool in MM.DISC_TOOLS else relief * 0.6
        polys = F.motif_prism_polygons(form, outer, holes, depth, thickness)
        for j in range(cnt):
            phi = 2.0 * math.pi * j / cnt
            for poly, r_from, r_to, op in polys:
                pr = _plate_prism(poly, r_c, phi, r_from, r_to, hp)
                if pr is not None:
                    (adds if op == "add" else cuts).append(pr)
        if verbose:
            print("  ring z%d: %d x tool %d at r=%.1f mm"
                  % (ring["zone"], cnt, tool, r_c))
    if adds:
        plate = plate.multiFuse(adds)
    if cuts:
        plate = plate.cut(_fuse_shapes(cuts))
    plate = plate.removeSplitter()

    # --- split into sectors by intersecting with a wedge
    rbig, z0 = k["r_outer_mm"] + 20.0, k["z_inner_mm"] - 30.0
    z1 = k["z_outer_mm"] + 30.0
    wsec = [(0.0, z0), (rbig, z0), (rbig, z1), (0.0, z1)]
    out = []
    label_r = 0.5 * (k["r_inner_mm"] + k["r_outer_mm"])
    label_z = _krempe_z(hp, label_r) - thickness
    for s in range(sectors):
        a0 = 360.0 * s / sectors
        wedge = _revolve_section_angle(wsec, 360.0 / sectors)
        wedge.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), a0)
        part = plate.common(wedge).removeSplitter()
        name = ("krempe_%s" % "abc"[s]) if sectors == 3 else "krempe_%d" % (s + 1)
        size = G.fit_ring_label(name, label_r, 12.0)
        if size:
            part = G.engrave_ring_label(part, name, label_r, label_z, size,
                                        angle_deg=a0 + 180.0 / sectors,
                                        from_below=True)
        part = _orient_for_bed(part)
        if verbose:
            bb = part.BoundBox
            print("  %s: vol %.1f mm3, solids=%d valid=%s, bbox %.1f x %.1f x %.1f, label %s"
                  % (name, part.Volume, len(part.Solids), part.isValid(),
                     bb.XLength, bb.YLength, bb.ZLength, size))
        out.append((name, part))

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        for name, part in out:
            path = os.path.join(out_dir, "%s.stl" % name)
            facets = export_stl(part, path)
            if verbose:
                print("  wrote %s  (%d facets, %.1f MB)"
                      % (path, facets, os.path.getsize(path) / 1e6))
    return out


def build_all(out_dir=None, only=None, verbose=True):
    """
    Generate the 19 stacked bands (z01..z19) into `out_dir` (default stl/).

    The Krempe plate (zones 20/21) is NOT here: it is a flat annular sector,
    not a band, and the 3-sector split needs its own decision -- 47 motifs of
    15 mm on an 829 mm ring leave only 2.6 mm gaps, so a radial seam lands on a
    motif unless it is phased into one. That is a design choice, not code.
    """
    out = out_dir or os.path.join(HERE, "stl")
    ids = only or ["z%02d" % i for i in range(1, 20)]
    built = []
    for bid in ids:
        built.append(build_stacked(bid, out_dir=out, verbose=verbose))
    if not only:
        built += [p for _, p in build_krempe(out_dir=out, verbose=verbose)]
    if verbose:
        print("\n%d parts written to %s" % (len(built), out))
    return built


if __name__ == "__main__" or __name__ == os.path.splitext(
        os.path.basename(__file__))[0]:
    # freecadcmd sets __name__ to the script's BASENAME, not "__main__"; a plain
    # guard silently does nothing AND freecadcmd still exits 0 (section 11.2).
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("band", nargs="?", default="z13")
    ap.add_argument("--all", action="store_true",
                    help="build all 19 stacked bands into stl/")
    ap.add_argument("--lap", action="store_true",
                    help="build the SUPERSEDED P3 lap band (registration lip) "
                         "instead of the P4 flat-stacked band")
    ap.add_argument("--out", default=os.path.join(HERE, "stl", "test"))
    a = ap.parse_args([x for x in sys.argv[1:] if not x.endswith(".py")])
    # freecadcmd leaves the script's own path in sys.argv, so a bare positional
    # would be read as the band id; drop *.py before parsing.
    if a.all:
        build_all(a.out)
    elif a.lap:
        build(a.band, out_dir=a.out)
    else:
        build_stacked(a.band, out_dir=a.out)
