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


def export_stl(shape, path, defl=0.05):
    """Export with an explicit deviation, instead of OCCT's default.

    `Shape.exportStl` takes no tolerance, so mesh explicitly and write the
    mesh. This is the difference between ~2 MB and ~23 MB per band.
    """
    import Mesh
    mesh = Mesh.Mesh()
    mesh.addFacets(shape.tessellate(defl))
    mesh.write(path)
    return mesh.CountFacets


def make_trennband_ridge(profile, z0, h, wall_mm, proud=1.0, embed=0.6):
    """
    The Trennband ridge at a band's lower edge: a 1 mm proud collar.

    Built as a separate ring and fused, rather than folded into the section
    polyline, so the ridge stays a swappable design detail (plan section 4
    Option A) and the band section stays a clean two-surface wall.

    `embed` makes the ring overlap the wall instead of butting against it.
    A collar that ends exactly on the outer surface touches the band along a
    single circle -- a LINE contact, which OCCT cannot fuse into one solid
    (it returns two disjoint solids) and which is also a knife-edge joint on
    the print. Carrying the ring `embed` mm inward into the wall gives a
    real overlapping face, so the fuse is solid and the joint is printable.
    """
    r_outer = profile(z0) + proud
    r_outer_hi = profile(z0 + h) + proud
    r_embed = profile(z0) - embed
    r_embed_hi = profile(z0 + h) - embed
    pts = [(r_embed, z0),
           (r_outer, z0),
           (r_outer_hi, z0 + h),
           (r_embed_hi, z0 + h)]
    vecs = [FreeCAD.Vector(r, 0.0, z) for r, z in pts]
    vecs.append(vecs[0])
    face = Part.Face(Part.makePolygon(vecs))
    return face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360.0)


def make_registration_lip(profile, z0, wall_mm, lip_h=6.0, clearance=0.25):
    """
    A ring on the INSIDE of the lower edge that slips into the band below.

    Sized to the OUTER radius at z0 minus the clearance, so it enters the band
    below's bore. It grows inward-and-down from the band's own wall.

    Like the Trennband ridge this OVERLAPS the wall rather than butting it:
    the lip's outer face is only `clearance` inside the wall's own surface, so
    it would otherwise meet the shell along a line and fail to fuse.
    """
    r_outer = profile(z0) - clearance          # sits just inside the band below
    r_inner = r_outer - wall_mm
    # start the lip ABOVE z0 so it is truly embedded in the shell, and run it
    # down past z0 so it protrudes below where it must mate
    z_top = z0 + lip_h
    z_bot = z0 - lip_h / 2.0
    pts = [(r_outer, z_bot), (r_outer, z_top),
           (r_inner, z_top), (r_inner, z_bot)]
    vecs = [FreeCAD.Vector(r, 0.0, z) for r, z in pts]
    vecs.append(vecs[0])
    face = Part.Face(Part.makePolygon(vecs))
    return face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360.0)


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
            print("  + Trennband ridge tb%d: z %.1f .. %.1f, 1.0 mm proud"
                  % (idx - 1, zb, z0))

    # --- registration lip, inside the lower edge
    if idx > 1:
        lip = make_registration_lip(profile, z0, wall,
                                   lip_h=hp["registration_lip_mm"],
                                   clearance=hp["registration_clearance_mm"])
        parts.append(lip)
        if verbose:
            print("  + registration lip: %s, %s clearance"
                  % (hp["registration_lip_mm"], hp["registration_clearance_mm"]))

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
