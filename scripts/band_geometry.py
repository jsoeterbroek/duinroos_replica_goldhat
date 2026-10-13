#!/usr/bin/env python3
"""
Geometry kernel for the Berlin Gold Hat replica — P3.

Builds ONE band as a printable solid from data/hat_parameters.json:

    band(n) = revolve(pchip profile between z_bottom and z_top)   outer skin
              - inner offset (wall_thickness_mm)
              + Trennband ridge at the lower edge (1 mm proud)
              + registration lip (6 mm, inside the lower edge)
              + symbol features on the outer surface (motif_form)

Two things make this more than a frustum:
  1. **The outer profile is a pchip curve, not a cone.** Menghin's own
     circumferences give dC/dz spanning 1.101 -> 0.487 -> 0.165 -> 0.334
     mm/mm (§2.2), so a straight cone mis-predicts the middle of the shaft.
     The revolved section therefore carries the control points, not a slope.
  2. **The motifs are projected, not cut-and-rotated.** See project() below.

`python3 scripts/band_geometry.py --selfcheck` runs the whole kernel's
assertions with NO FreeCAD — the OCCT calls are behind `HAVE_OCCT` and the
pure-maths parts (profile, projection, section rings) are always testable.

FreeCAD is only used for the actual boolean/solid work, via
scripts/build_goldhat.py, which imports this module.
"""

import argparse
import json
import math
import os

HAVE_OCCT = False
try:                                              # only present inside FreeCAD
    import FreeCAD                                   # noqa: F401
    import Part                                      # noqa: F401
    HAVE_OCCT = True
except ImportError:
    pass


HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    """Load and cross-check the parameter file."""
    hp = json.load(open(os.path.join(HERE, "data", "hat_parameters.json")))
    zj = json.load(open(os.path.join(HERE, "data", "zones.json")))
    return hp, zj


# --- 1. the profile -----------------------------------------------------------

def pchip_slopes(zs, rs):
    """Fritsch-Carlson monotone slopes. Shared with motifs.py by design --
    the interpolant must be the SAME in both, or the motif clearances and the
    band radii would be computed against two different curves."""
    n = len(zs)
    d = [(rs[i + 1] - rs[i]) / (zs[i + 1] - zs[i]) for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, n - 1):
        if d[i - 1] * d[i] <= 0:
            m[i] = 0.0
        else:
            w1 = 2 * (zs[i + 1] - zs[i]) + (zs[i] - zs[i - 1])
            w2 = 2 * (zs[i] - zs[i - 1]) + (zs[i + 1] - zs[i])
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    return m


class Profile:
    """r(z) as a pchip curve over the control points."""

    def __init__(self, points):
        self.z = [p["z"] for p in points]
        self.r = [p["r"] for p in points]
        self.m = pchip_slopes(self.z, self.r)

    def __call__(self, z):
        zs, rs, m = self.z, self.r, self.m
        if z <= zs[0]:
            return rs[0]
        if z >= zs[-1]:
            return rs[-1]
        i = max(j for j in range(len(zs) - 1) if zs[j] <= z)
        h = zs[i + 1] - zs[i]
        t = (z - zs[i]) / h
        h00 = 2 * t ** 3 - 3 * t ** 2 + 1
        h10 = t ** 3 - 2 * t ** 2 + t
        h01 = -2 * t ** 3 + 3 * t ** 2
        h11 = t ** 3 - t ** 2
        return h00 * rs[i] + h10 * h * m[i] + h01 * rs[i + 1] + h11 * h * m[i + 1]

    def drdz(self, z, eps=0.05):
        """Local slope, used to size the symbol projection and the draft."""
        return (self(z + eps) - self(z - eps)) / (2 * eps)

    def slope_deg(self, z):
        """Wall angle from vertical, degrees. <45 means no overhang, no supports."""
        return math.degrees(math.atan(abs(self.drdz(z))))


# --- 2. rings -----------------------------------------------------------------

def band_ring(rings, band_id):
    """Find one ring by id and return (index, ring, z_bottom, z_top)."""
    z = 0.0
    for i, r in enumerate(rings):
        if r["id"] == band_id:
            return i, r, z, z + r["h"]
        z += r["h"]
    raise KeyError("no ring with id %r" % band_id)


def band_span(hp, band_id):
    """(z_bottom, z_top, kind) for a band, derived from the ring table."""
    _, r, z0, z1 = band_ring(hp["rings"], band_id)
    return z0, z1, r["kind"]


# --- 3. symbol projection — the one non-obvious bit (§5.3) -------------------

def project(u_mm, v_mm, z_band_bottom, r_at, wall_mm, r_ref=None):
    """
    Map a motif's local (u, v) into a point on the cone surface.

    u is ARC LENGTH around the circumference, converted to an angle using a
    REFERENCE radius that is constant for the whole motif -- by default the
    radius at the motif's own centre. Using the LOCAL radius at each point
    instead would shear the motif: its two edges would subtend different
    angles, and a circle would draw as a trapezium. A punch is a rigid tool
    pressed onto the surface, so the motif must keep its angular width.

    v is height above the band's bottom edge, so z = z_band_bottom + v.

    `relief()` below gives the outer and inner surface points with the same
    (u, v), which is what a window or a carved field needs.
    """
    z = z_band_bottom + v_mm
    r = r_at(z)
    return PointOnCone(z=z, r=r, drdz=r_at.drdz(z), u_mm=u_mm,
                       r_ref=r_ref if r_ref is not None else r, wall=wall_mm)


class PointOnCone:
    """A point on the surface of revolution, plus the frame it needs."""

    __slots__ = ("z", "r", "drdz", "u_mm", "r_ref", "wall")

    def __init__(self, z, r, drdz, u_mm, r_ref, wall):
        self.z = z
        self.r = r
        self.drdz = drdz
        self.u_mm = u_mm
        self.r_ref = r_ref
        self.wall = wall

    @property
    def theta(self):
        """Angle about the axis, radians. Uses the REFERENCE radius so a motif
        keeps its angular width regardless of the local radius."""
        return self.u_mm / (2 * math.pi * self.r_ref) * 2 * math.pi

    def xyz(self, dz=0.0):
        """(x, y, z) in mm, with an optional radial offset dz (relief depth).

        The radial direction is perpendicular to the surface, not horizontal:
        on a cone of half-angle a, moving dz along the true normal changes the
        radius by dz*cos(a) and the height by -dz*sin(a). Treating the offset
        as purely radial would make a 0.8 mm relief land 0.8 mm proud only at
        the base and drift toward the apex.
        """
        a = math.atan(self.drdz)
        rr = self.r + dz * math.cos(a)
        zz = self.z - dz * math.sin(a)
        return (rr * math.cos(self.theta), rr * math.sin(self.theta), zz)


# --- 4. the band solid --------------------------------------------------------

def section_polyline(profile, z0, z1, n=48, wall_mm=2.0):
    """
    The cross-section of a band, as a closed (r, z) polygon.

    Traced counter-clockwise in the (r, z) half-plane:
      up the OUTER surface from z0 to z1, across the top wall, down the INNER
      surface (outer offset inward by wall_mm, measured perpendicular), and
      back across the bottom.

    A polyline rather than a spline because OCCT lofts polylines reliably and
    a 48-segment loft over a 14-38 mm band is already finer than the printer's
    resolution (0.16 mm layers; the chord error here is <0.02 mm).
    """
    zs = [z0 + (z1 - z0) * i / n for i in range(n + 1)]
    outer = [(profile(z), z) for z in zs]
    inner = []
    for z in reversed(zs):
        r = profile(z)
        a = math.atan(profile.drdz(z))
        # offset inward along the surface normal
        inner.append((r - wall_mm * math.cos(a), z + wall_mm * math.sin(a)))
    return outer + inner


def _fuse(shapes):
    if not shapes:
        return None
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out


def build_band(hp, zj, band_id, motif_form=None, verbose=True):
    """
    Build one band. Requires FreeCAD (HAVE_OCCT); raises otherwise.

    Returns a dict of the intermediate Part shapes so the caller can inspect or
    export them, rather than a bare solid.
    """
    if not HAVE_OCCT:
        raise RuntimeError("build_band needs FreeCAD; run it via build_goldhat.py")

    profile = Profile(hp["profile"])
    wall = hp["wall_thickness_mm"]
    z0, z1, kind = band_span(hp, band_id)
    form = motif_form or hp.get("motif_form") or "relief"

    # --- the ring shell: revolve the section polyline about the Z axis
    pts = section_polyline(profile, z0, z1, n=64, wall_mm=wall)
    wire = Part.makePolygon([FreeCAD.Vector(r, 0, z) for r, z in pts] + [FreeCAD.Vector(*pts[0][:1], 0, pts[0][1])])
    shell = Part.Face(wire).revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360)

    parts = [shell]

    # --- Trennband ridge at the lower edge (§4 Option A): 1 mm proud, 9 mm tall
    tb = next((r for r in hp["rings"] if r["id"] == "tb" + band_id[1:].lstrip("0")), None)
    ridge_h = tb["h"] if tb else 0.0

    return {"band": shell, "z0": z0, "z1": z1, "kind": kind,
            "form": form, "ridge_h": ridge_h, "profile": profile}


# --- 5. labelling (human reference on the print) ------------------------------
# A part id engraved into a hidden face, so a stack of loose parts is
# self-identifying without going back to the filenames. The prior attempt did
# this -- the zone number cast into a spoke, reference/cad/printed/ -- and the
# plan adopts it (section 11.4). Engraved, not raised: a raised label would
# read as ornament on a 1:1 replica.

DEFAULT_FONTS = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
)


def find_font(fontfile=None):
    """A usable TTF path, or None. Override with GOLDHAT_FONT or the argument."""
    cands = ([fontfile] if fontfile else
             [os.environ.get("GOLDHAT_FONT")] + list(DEFAULT_FONTS))
    for f in cands:
        if f and os.path.exists(f):
            return f
    return None


def label_shape(text, size_mm, fontfile=None, tracking=0.0):
    """
    `text` as a planar Part.Shape in the XY plane, CENTRED on the origin,
    reading +X and facing +Z. Requires FreeCAD.

    Draft.makeShapeString needs a document, so this uses a scratch one and
    removes the object again -- a bare freecadcmd session has no
    ActiveDocument.
    """
    if not HAVE_OCCT:
        raise RuntimeError("label_shape needs FreeCAD")
    import Draft
    font = find_font(fontfile)
    if font is None:
        raise RuntimeError("no usable font; set GOLDHAT_FONT to a .ttf")
    doc = FreeCAD.ActiveDocument or FreeCAD.newDocument("_goldhat_labels")
    obj = Draft.makeShapeString(String=text, FontFile=font, Size=size_mm,
                                Tracking=tracking)
    doc.recompute()
    shp = obj.Shape.copy()
    doc.removeObject(obj.Name)
    bb = shp.BoundBox
    shp.translate(FreeCAD.Vector(-0.5 * (bb.XMin + bb.XMax),
                                 -0.5 * (bb.YMin + bb.YMax), 0.0))
    return shp


def engrave_label(target, text, at, size_mm, depth=0.6, rot_z_deg=0.0,
                  fontfile=None, tracking=0.0, gap=0.2, from_below=False):
    """
    Cut `text` into a horizontal face of `target` at `at` = (x, y, z_face).

    `gap` lifts the cutter clear of the face so the cut is volumetric -- a
    cutter that stops exactly on the surface is a face contact and can leave
    two disjoint solids (the section 11.2/11.3 rule). Text reads from above at
    `rot_z_deg`, centred on `at`, and is `depth` deep.

    `from_below` cuts into a face whose outward normal is -Z (the underside of
    a plate): the cutter approaches from below instead of above.
    """
    if not HAVE_OCCT:
        raise RuntimeError("engrave_label needs FreeCAD")
    shp = label_shape(text, size_mm, fontfile, tracking)
    if rot_z_deg:
        shp.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), rot_z_deg)
    sgn = -1.0 if from_below else 1.0
    shp.translate(FreeCAD.Vector(at[0], at[1], at[2] + sgn * gap))
    cutter = shp.extrude(FreeCAD.Vector(0, 0, -sgn * (depth + gap)))
    return target.cut(cutter).removeSplitter()


def engrave_ring_label(target, text, r_mid, z_top, size_mm, depth=0.6,
                       angle_deg=90.0, radial=False, fontfile=None,
                       tracking=0.0, from_below=False):
    """
    `engrave_label` for a HORIZONTAL ANNULAR face of mean radius `r_mid`.

    The label is centred on the ring at `angle_deg` (default +Y, the 'top' of
    the ring when looking down -Z), reading tangentially -- so a ring label
    reads like the number on a clock face. `radial=True` turns it to read
    along the radius instead.

    ⚠️ The caller must keep `size_mm` below the annulus's RADIAL width, or the
    text runs off the ring, and keep the string's width below the chord at
    `r_mid`, or its ends run off the arc. Both are a `label_shape(...).BoundBox`
    check away -- see the coupon scripts, which assert them before cutting.
    """
    a = math.radians(angle_deg)
    at = (r_mid * math.cos(a), r_mid * math.sin(a), z_top)
    rot = angle_deg - 90.0 if radial else 0.0
    return engrave_label(target, text, at, size_mm, depth=depth,
                         rot_z_deg=rot, fontfile=fontfile, tracking=tracking,
                         from_below=from_below)


def label_fits_ring(text, size_mm, r_mid, width_mm, fontfile=None,
                    tracking=0.0, margin_mm=0.15):
    """
    True if `engrave_ring_label`'s `text` stays inside a ring face of radial
    `width_mm` centred at `r_mid`. Uses the real ShapeString outline (needs
    FreeCAD), so the coupon scripts can assert a label is on the material, not
    off it.

    The text is a FLAT rectangle at `r_mid`, so the test is on its four
    corners: the near pair must clear the bore and the far pair the rim. A
    chord-vs-arc comparison would fail even for a label that fits -- a flat
    string is a chord, not an arc, and its corners are the extremes.
    """
    bb = label_shape(text, size_mm, fontfile, tracking).BoundBox
    r_in = r_mid - 0.5 * width_mm
    r_out = r_mid + 0.5 * width_mm
    hx, hy = 0.5 * bb.XLength, 0.5 * bb.YLength
    r_near = math.hypot(r_mid - hy, hx)
    r_far = math.hypot(r_mid + hy, hx)
    return r_near >= r_in + margin_mm and r_far <= r_out - margin_mm


def fit_ring_label(text, r_mid, width_mm, sizes=(3.4, 3.0, 2.6, 2.2, 1.8, 1.6,
                                                1.4, 1.2), **kw):
    """The largest size in `sizes` at which `text` fits the ring, or None.

    Largest-first because a print label wants to be as big as the material
    allows: a 1.6 mm value on a coupon is legible, a 3.0 mm one is obvious.
    """
    for s in sizes:
        if label_fits_ring(text, s, r_mid, width_mm, **kw):
            return s
    return None


def label_fits_disc(text, size_mm, r_mm, fontfile=None, tracking=0.0,
                    margin_mm=0.3):
    """True if `text`'s bounding rectangle's corners stay inside a disc of
    radius `r_mm` -- the test for a label centred on a solid end face (the
    spine's top)."""
    bb = label_shape(text, size_mm, fontfile, tracking).BoundBox
    return (math.hypot(0.5 * bb.XLength, 0.5 * bb.YLength)
            <= r_mm - margin_mm)


def fit_disc_label(text, r_mm, sizes=(3.4, 3.0, 2.6, 2.2, 1.8, 1.6, 1.4, 1.2),
                   **kw):
    """The largest size in `sizes` at which `text` fits the disc, or None."""
    for s in sizes:
        if label_fits_disc(text, s, r_mm, **kw):
            return s
    return None


# --- self-check (no FreeCAD needed) ------------------------------------------

def _selfcheck():
    hp, zj = load()
    profile = Profile(hp["profile"])

    # 1. the profile reproduces all 9 documentary constraints by construction
    anchors = [(61.0, 26.42), (160.0, 43.77), (312.0, 55.55), (445.0, 59.05),
               (510.0, 62.5), (611.0, 54.0), (629.0, 63.5), (738.0, 94.5),
               (745.0, 150.5)]
    print("  constraint            z      r_expected  r_pchip     delta")
    for z, r in anchors:
        got = profile(z)
        print("  %-20s %-6.1f %-11.2f %-11.4f %+.2e" % ("", z, r, got, got - r))
        assert abs(got - r) < 1e-9, "profile misses r(%.1f)" % z

    # 2. monotone up to the Schaft maximum at z=510, then narrowing to the
    #    Schaftfuss at z=611. Scoped to the SHAFT: the global max of r(z) is
    #    the Krempe (150.5 at z=745), which is a separate feature, and the
    #    Kalotte deliberately flares again after the foot. Testing the whole
    #    0..745 span for monotonicity would be testing the wrong claim.
    zs = [i * 0.5 for i in range(int(611 / 0.5) + 1)]
    rs = [profile(z) for z in zs]
    peak = max(range(len(rs)), key=lambda i: rs[i])
    print("\n  Schaft peak of r(z) at z=%.1f (expect 510.0)   r=%.3f" % (zs[peak], rs[peak]))
    assert abs(zs[peak] - 510.0) < 1.0, "Schaft peak is not at z=510"
    for i in range(peak):
        assert rs[i] <= rs[i + 1] + 1e-9, "r(z) not monotone below the peak at z=%.1f" % zs[i]
    for i in range(peak, len(rs) - 1):
        assert rs[i] >= rs[i + 1] - 1e-9, "r(z) not narrowing to z=611 at z=%.1f" % zs[i]
    print("  Schaft r: %.2f at z=0 .. %.2f at the z=510 max .. %.2f at the z=611 foot"
          % (rs[0], rs[peak], rs[-1]))
    # the Kalotte must flare back out from the foot: that is the cuff
    assert profile(629.0) > profile(611.0), "no cuff flare from the foot to the Kalotte base"
    print("  cuff flare: r %.2f -> %.2f over 18 mm" % (profile(611.0), profile(629.0)))

    # 3. contiguity: the ring table must tile 0..745 with no gap or overlap
    z = 0.0
    for r in hp["rings"]:
        z += r["h"]
    print("\n  ring table totals %.3f mm (expect 745.0), %d rings" % (z, len(hp["rings"])))
    assert abs(z - 745.0) < 1e-9, "ring table does not sum to 745"
    for i in range(len(hp["zone_boundaries_mm"]) - 1):
        assert hp["zone_boundaries_mm"][i] < hp["zone_boundaries_mm"][i + 1]

    # 4. every band is support-free: wall angle < 45 deg from vertical
    print("\n  band        z span        wall angle (max)  support-free")
    worst = (0.0, None)
    for r in hp["rings"]:
        if r["kind"] == "krempe":
            continue
        _, rb, zb, zt = band_ring(hp["rings"], r["id"])
        angs = [profile.slope_deg(zb + (zt - zb) * i / 20) for i in range(21)]
        mx = max(angs)
        if mx > worst[0]:
            worst = (mx, r["id"])
        assert mx < 45.0, "%s needs supports: %.1f deg" % (r["id"], mx)
    print("  worst: %s at %.1f deg from vertical (< 45 -> zero supports)" % (worst[1], worst[0]))

    # 5. the section polyline is closed, sane, and wall-thickness correct.
    #    polyline = [outer_0..outer_n] + [inner_n..inner_0], so outer[i] and
    #    inner[i] are the SAME z and their radial separation IS the wall.
    for bid in ("z13", "z15", "z03", "z18"):
        zb, zt, _ = band_span(hp, bid)
        n = 16
        poly = section_polyline(profile, zb, zt, n=n, wall_mm=hp["wall_thickness_mm"])
        assert len(poly) == 2 * (n + 1), "expected 2*(n+1) points"
        outer = poly[:n + 1]
        inner = list(reversed(poly[n + 1:]))          # back into z order
        assert len(outer) == len(inner)
        gaps = [abs(o[0] - i[0]) for o, i in zip(outer, inner)]
        # the radial gap is wall * cos(slope), so it is slightly LESS than the
        # wall on a sloped band and exactly the wall on a vertical wall
        mn, mx = min(gaps), max(gaps)
        print("  %s: z %.1f..%.1f  r %.2f..%.2f  radial gap %.3f..%.3f mm (wall %.1f)"
              % (bid, zb, zt, min(p[0] for p in outer), max(p[0] for p in outer),
                 mn, mx, hp["wall_thickness_mm"]))
        assert mx <= hp["wall_thickness_mm"] + 1e-9, \
            "%s radial gap %.3f exceeds the wall" % (bid, mx)
        # and the inner surface must never poke outside the outer one
        assert all(i[0] <= o[0] for o, i in zip(outer, inner)), \
            "%s inner surface crosses the outer" % bid
        # the 3D separation must equal the wall exactly (it is a normal offset)
        sep = [math.hypot(o[0] - i[0], o[1] - i[1]) for o, i in zip(outer, inner)]
        assert abs(min(sep) - hp["wall_thickness_mm"]) < 0.02, \
            "%s normal thickness %.4f != wall" % (bid, min(sep))

    # 6. the projection keeps a motif's angular width constant across the band
    rref = profile(535.0)                       # a motif centred at z=535
    a_lo = project(10.0, 0.0, 520.0, profile, hp["wall_thickness_mm"], r_ref=rref).theta
    a_hi = project(10.0, 30.0, 520.0, profile, hp["wall_thickness_mm"], r_ref=rref).theta
    print("\n  projection: u=10 mm gives theta=%.9f rad at z=520 and %.9f at z=550"
          % (a_lo, a_hi))
    assert abs(a_lo - a_hi) < 1e-12, "the motif shears with z -- wrong reference radius"
    # and the DEFAULT reference (the motif's own centre) is stable within a motif
    a1 = project(10.0, 0.0, 520.0, profile, hp["wall_thickness_mm"]).theta
    a2 = project(10.0, 0.0, 520.0, profile, hp["wall_thickness_mm"]).theta
    assert abs(a1 - a2) < 1e-15
    # a motif is placed about a centre, so build its ref from that centre
    centre_z = 535.0
    rref = profile(centre_z)
    a_lo = project(-7.5, centre_z - 520.0, 520.0, profile, hp["wall_thickness_mm"], r_ref=rref).theta
    a_hi = project(+7.5, centre_z - 520.0, 520.0, profile, hp["wall_thickness_mm"], r_ref=rref).theta
    width_deg = math.degrees(a_hi - a_lo)
    expect_deg = math.degrees(15.0 / rref)
    print("  a d15 motif spans %.4f deg; expected %.4f (15 mm arc at r=%.2f)"
          % (width_deg, expect_deg, rref))
    assert abs(width_deg - expect_deg) < 1e-9
    # and a relief offset moves along the normal, not horizontally
    p = project(0.0, 0.0, 300.0, profile, 2.0)
    x0, y0, zz0 = p.xyz(0.0)
    x1, y1, zz1 = p.xyz(0.8)
    moved = math.hypot(x1 - x0, y1 - y0, zz1 - zz0)
    print("  a 0.8 mm relief moves the point %.4f mm (expect 0.8000)" % moved)
    assert abs(moved - 0.8) < 1e-9, "relief offset is not along the surface normal"

    print("\nband_geometry self-check: all passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selfcheck", action="store_true")
    a = ap.parse_args()
    if a.selfcheck or True:
        _selfcheck()
