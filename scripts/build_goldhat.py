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


def export_stl(shape, path, defl=0.05):
    """Export with an explicit deviation, instead of OCCT's default.

    `Shape.exportStl` takes no tolerance, so mesh explicitly and write the
    mesh. This is the difference between ~2 MB and ~23 MB per band.

    `shape` may be one shape or a list of them (a coupon plate). Multi-part
    plates are why the accumulation guard below exists.
    """
    import Mesh
    shapes = shape if isinstance(shape, (list, tuple)) else [shape]
    mesh = Mesh.Mesh()
    n = 0
    for s in shapes:
        tris = _facets(s, defl)
        mesh.addFacets(tris)
        n += len(tris)
    assert mesh.CountFacets == n, \
        "mesh lost facets: %d of %d (see _facets)" % (mesh.CountFacets, n)
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


if __name__ == "__main__":
    out = os.path.join(HERE, "stl", "test")
    build("z13", out_dir=out)
