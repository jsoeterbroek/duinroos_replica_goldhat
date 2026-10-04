#!/usr/bin/env python3
"""
build_clearance_coupon.py — a compact radial-clearance ladder for the lap joint.

Run inside FreeCAD (MCP `execute_code` or `freecadcmd`):

    freecadcmd scripts/build_clearance_coupon.py

Why this exists
---------------
The P5 fit test needs a radial clearance, and 0.25 mm (data/hat_parameters.json)
is an assumption, not a measurement.  Printing the whole fit-test trio at three
clearances costs ~400 g; this coupon is ~20 g and answers the same question.

Why NOT "three lip arcs at three clearances on the z14 band"
------------------------------------------------------------
That was the first idea and it does not work: the lip is inserted axially into a
uniform collar, so the TIGHTEST arc alone decides whether the band enters at
all.  The three sectors would not be independent.

Design
------
Three independent socket/spigot pairs, side by side, each a short ring that
reproduces the joint's LOCAL TAPER exactly (`dr/dz` of the real profile at the
z14/z15 mating plane, z=527).  The socket is the Trennband collar's bore
(`profile - COLLAR_INSET`); the spigot is the registration lip
(`profile - COLLAR_INSET - clearance`).  The absolute diameter is not 1:1 — the
fit depends on the taper and the clearance, not on the diameter — so the whole
coupon is scaled to ~⌀35 mm.

Row order on the plate is left -> right = 0.15, 0.25, 0.35 mm.  Print it flat,
drop each spigot into its socket, and keep the loosest pair that still holds.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import band_geometry as G            # noqa: E402
import build_goldhat as B            # noqa: E402

import FreeCAD                        # noqa: E402  (only inside FreeCAD)
import Part                          # noqa: E402

OUT = os.path.join(HERE, "stl", "test")

CLEARANCES = [0.15, 0.25, 0.35]      # row order, left to right
R0 = 15.0                            # coupon "profile" radius (mm)
INSET = 0.6                          # collar inner face, as in build_goldhat
JOINT_Z = 527.0                      # the z14/z15 mating plane


def _slope_at(z):
    """The real local taper at the joint (dr/dz of the pchip profile)."""
    hp, _ = G.load()
    return G.Profile(hp["profile"]).drdz(z)


def socket_section(slope, h=12.0, wall=2.5, inset=INSET, cham=1.0, n=24):
    """The collar bore, with a 1 mm lead-in chamfer at the mouth."""
    zs = [h * i / n for i in range(n + 1)]
    outer = [(R0 - inset + slope * z + wall, z) for z in zs]
    inner = [(R0 - inset + slope * z, z) for z in reversed(zs)]
    inner[-1] = (R0 - inset + cham, 0.0)          # widen the mouth (z=0)
    return outer + inner


def spigot_section(slope, clearance, h=10.0, wall=2.0, inset=INSET, cham=1.0,
                   n=24):
    """The registration lip, with a 1 mm lead-in chamfer at its nose."""
    zs = [h * i / n for i in range(n + 1)]

    def ro(z):
        return R0 - inset - clearance + slope * z

    outer = [(ro(z), z) for z in zs]
    outer[-1] = (ro(h) - cham, h)
    inner = [(ro(z) - wall, z) for z in reversed(zs)]
    return outer + inner


def main():
    slope = _slope_at(JOINT_Z)
    os.makedirs(OUT, exist_ok=True)
    print("lap clearance ladder — real joint taper dr/dz = %+.5f at z=%.0f"
          % (slope, JOINT_Z))
    print("row order left->right: " + ", ".join("%.2f mm" % c for c in CLEARANCES))
    print()

    shapes = []
    for i, c in enumerate(CLEARANCES):
        x = (i - (len(CLEARANCES) - 1) / 2.0) * 60.0
        socket = B._revolve_section(socket_section(slope))
        spigot = B._revolve_section(spigot_section(slope, c))
        socket.translate(FreeCAD.Vector(x, 0.0, 0.0))
        spigot.translate(FreeCAD.Vector(x, 60.0, 0.0))
        shapes += [socket, spigot]
        print("  %.2f mm: socket vol %6.0f mm3  spigot vol %6.0f mm3  "
              "radial gap %.2f mm" % (c, socket.Volume, spigot.Volume, c))

    import Mesh
    mesh = Mesh.Mesh()
    for s in shapes:
        mesh.addFacets(s.tessellate(0.05))
    path = os.path.join(OUT, "clearance_ladder.stl")
    mesh.write(path)
    total = sum(s.Volume for s in shapes)
    print("\nwrote %s  (%d facets, %.1f g PLA)"
          % (path, mesh.CountFacets, total * 1.24 / 1000.0))


if __name__ == "__main__" or __name__ == os.path.splitext(
        os.path.basename(__file__))[0]:
    main()
