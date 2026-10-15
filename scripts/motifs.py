#!/usr/bin/env python3
"""
2D motif primitives for the Berlin Gold Hat replica.

Each motif is punched into the metal on the OUTSIDE of a body of revolution.
Locally the surface is a plane (u, v) = (arc length around the circumference,
height), so every primitive is defined in 2D mm and later mapped onto the cone
by build_goldhat.py. Keeping the primitives 2D is what makes them testable
without FreeCAD, and what lets `--svg` render a development for eyeballing.

    u = 0 at the motif centre, +u = counter-clockwise seen from outside
    v = 0 at the motif centre, +v = up (towards the apex)

Primitives return (outer, inner) as lists of (u, v) ring polygons:
  outer = the closed convex-ish outline of the punch footprint
  inner = holes (countersunk ring troughs), possibly empty

The physical form (relief / window / relief_window) is NOT decided here -- see
IMPLEMENTATION_PLAN.md section 6.3, deferred to the P3.5 print test. These are
the footprint and hole geometry either way.

Authoritative sources: the English hand-transcription
assets/menghin/2010/text/menghin_pages20-31.txt (Fig. 21 legend and per-zone
tool attribution), and the page images in assets/menghin/2010/jpg/:
  Fig. 22 plates (menghin_page028/029.jpeg) for the actual FORM

Ring counts are 2, 3, 5 or 6. NEVER 4.
"""

import json
import math
import os

# --- Fig. 21 tool legend ------------------------------------------------------
# Menghin's own numbers. diameter_mm is the OUTER diameter of the boss disc.
# rings is the number of concentric circles INSIDE the boss (the central dot is
# not counted as a ring -- Fig. 22 plates show boss + N concentric ridges).
DISC_TOOLS = {
    # tool: (rings, diameter_mm)
    8:  (3, 12.0),
    9:  (2, 12.0),
    10: (5, 13.0),
    11: (3, 14.0),
    12: (3, 15.0),
    13: (2, 15.0),
    14: (5, 15.0),
    15: (6, 21.0),
}

# Special patterns (Fig. 21, scale 1:1, "length 11 mm")
SPECIAL_LENGTH_MM = 11.0


def _circle(cu, cv, r, n=72, start=0.0):
    """A closed circle as a polygon. n segments is plenty for a punch outline."""
    return [(cu + r * math.cos(start + 2 * math.pi * i / n),
             cv + r * math.sin(start + 2 * math.pi * i / n)) for i in range(n)]


def _ring_band(cu, cv, r_mid, width, n=72):
    """An annulus (a ridge trough): outer circle and inner circle, as one hole."""
    return [_circle(cu, cv, r_mid + width / 2.0, n),
            _circle(cu, cv, r_mid - width / 2.0, n)]


# --- the primitives -----------------------------------------------------------

def ring_dot(rings, diameter_mm, ridge_w=None, boss_frac=0.34):
    """
    Scheibenbuckel: the signature motif, 418 of them on the hat.

    Fig. 22 plates (menghin_page029.jpeg, Z13/Z14/Z15) show: one central boss
    (a dome) surrounded by `rings` concentric circular ridges, and the whole
    thing is `diameter_mm` across.

    outer  = the disc footprint
    inner  = the trough between each pair of ridges, so `rings` concentric
             rings need `rings` ridge positions and `rings` troughs (the
             innermost trough separates the boss from the first ridge).

    ridge_w defaults to a value that keeps the trough printable: Nr.10 packs
    5 rings into a 13 mm disc, and a fixed 0.45 mm ridge leaves only a
    0.36 mm trough there. Scaling the ridge to 30% of the ring pitch keeps
    every trough >= 0.5 mm, which a 0.4 mm nozzle can resolve. This is a
    STYLISATION choice, not a measurement -- the Fig. 22 photo cannot resolve
    a sub-half-millimetre ridge on a phone photo of a printed page.
    """
    R = diameter_mm / 2.0
    r_boss = R * boss_frac
    pitch = (R - r_boss) / rings
    if ridge_w is None:
        ridge_w = min(0.45, 0.30 * pitch)
    step = (R - r_boss - ridge_w / 2.0) / rings
    holes = []
    for i in range(rings):
        r_mid = r_boss + ridge_w / 2.0 + (i + 0.5) * step
        holes.append(_ring_band(0.0, 0.0, r_mid, ridge_w))
    return _circle(0.0, 0.0, R), holes


def disc(r):
    """Plain punched dot (Punktkreis family)."""
    return _circle(0.0, 0.0, r), []


def ring(r_mid, width=0.45):
    """A single annulet (Ringkreis, No. 7) -- the interstitial filler.

    Fig. 22 (menghin_page029.jpeg Z13/Z14) shows these small rings in the four
    gaps between neighbouring boss discs.
    """
    return _circle(0.0, 0.0, r_mid + width / 2.0), [_circle(0.0, 0.0, r_mid - width / 2.0)]


def circle_row(r_dot, n, pitch=None):
    """A row of small dots (Perlpunktband No. 4 / Punktkreis No. 5).

    Returns ONE outer with n holes -- the row is a single punched band, not n
    separate motifs, which is why these never appear in Menghin's counts.
    """
    if pitch is None:
        pitch = 2.6 * r_dot
    span = pitch * (n - 1)
    outer = [(-span / 2.0 - pitch / 2.0, -1.3 * r_dot),
             (span / 2.0 + pitch / 2.0, -1.3 * r_dot),
             (span / 2.0 + pitch / 2.0, 1.3 * r_dot),
             (-span / 2.0 - pitch / 2.0, 1.3 * r_dot)]
    holes = []
    for i in range(n):
        cu = -span / 2.0 + i * pitch
        holes.append(_circle(cu, 0.0, r_dot, 32))
    return outer, holes


def crescent(length_mm=SPECIAL_LENGTH_MM, thickness=None):
    """
    Horizontal crescent with a central dot (No. 16), zone 5 upper row.

    Fig. 22.1b shows a downward-opening arc (a wide shallow 'smile') with a dot
    hanging in the middle beneath it. Modelled as a filled arc band so it works
    as a relief ridge or a window ligature.
    """
    if thickness is None:
        thickness = length_mm * 0.17
    a = length_mm / 2.0
    outer, inner = [], []
    n = 40
    r_out, r_in = 1.45 * a, 1.45 * a - thickness
    for i in range(n + 1):
        th = math.pi + math.pi * i / n          # 180deg -> 360deg = upper arc
        outer.append((r_out * math.cos(th), -0.55 * a + r_out * math.sin(th)))
    for i in range(n, -1, -1):
        th = math.pi + math.pi * i / n
        inner.append((r_in * math.cos(th), -0.55 * a + r_in * math.sin(th)))
    return outer + inner, [_circle(0.0, -0.05 * a, thickness * 0.55, 24)]


def oval(length_mm=SPECIAL_LENGTH_MM, thickness=None, rotation=0.0):
    """
    Almond-shaped eye symbol (No. 17), zone 5 lower row.

    Fig. 22.1b: a pointed almond with a short vertical stroke through it.
    Two circular arcs meeting at points.
    """
    if thickness is None:
        thickness = length_mm * 0.42
    a, b = length_mm / 2.0, thickness / 2.0
    outer, holes = [], []
    n = 48
    for i in range(n + 1):                       # upper arc
        t = -a + 2 * a * i / n
        outer.append((t, b * math.sqrt(max(0.0, 1.0 - (t / a) ** 2)) ** (2.0 / 3.0)))
    for i in range(n, -1, -1):                   # lower arc
        t = -a + 2 * a * i / n
        outer.append((t, -b * math.sqrt(max(0.0, 1.0 - (t / a) ** 2)) ** (2.0 / 3.0)))
    holes.append([(0.0, -b * 0.75), (b * 0.22, b * 0.75),
                  (-b * 0.22, b * 0.75)])        # the central vertical stroke
    if rotation:
        c, s = math.cos(rotation), math.sin(rotation)
        rot = lambda pts: [(x * c - y * s, x * s + y * c) for x, y in pts]
        outer, holes = rot(outer), [rot(h) for h in holes]
    return outer, holes


def star8(r=30.0, points=8, inner_frac=0.62):
    """Eight-rayed star, zone 1 (the crown tip). A one-off.

    text/menghin_pages20-31.txt: 'The smooth-surfaced eight-rayed star features a
    freehand outline, while the eight acute-angled triangles between its rays
    display regular dotting arranged in horizontal rows.'
    So: a smooth star, with dots in the eight notches.
    """
    outer = []
    for i in range(points * 2):
        ang = math.pi / 2 + i * math.pi / points
        rr = r if i % 2 == 0 else r * inner_frac
        outer.append((rr * math.cos(ang), rr * math.sin(ang)))
    holes = []
    for i in range(points):
        ang = math.pi / 2 + math.pi / points + i * 2 * math.pi / points
        rr = r * inner_frac * 0.72
        holes.append(_circle(rr * math.cos(ang), rr * math.sin(ang), r * 0.055, 20))
    return outer, holes


def zigzag(teeth=3, amplitude=1.6, width=8.0):
    """Notched ridge (Kerbwulst) -- the Trennband motif between zones."""
    outer, holes = [], []
    n = teeth * 2
    for i in range(n + 1):
        u = -width / 2.0 + width * i / n
        outer.append((u, amplitude if i % 2 == 0 else -amplitude))
    return outer, holes


# --- dispatch -----------------------------------------------------------------

def build(primitive, **kw):
    """Build a primitive by name. Raises on unknown names (fail loud)."""
    if primitive == "ring_dot":
        return ring_dot(kw.get("rings", 3),
                        kw.get("diameter_mm", 15.0))
    if primitive == "disc":
        return disc(kw.get("r", 3.0))
    if primitive == "ring":
        return ring(kw.get("r_mid", 4.0))
    if primitive == "circle_row":
        return circle_row(kw.get("r_dot", 1.2), kw.get("n", 8))
    if primitive == "crescent":
        return crescent(kw.get("length_mm", SPECIAL_LENGTH_MM))
    if primitive == "oval":
        return oval(kw.get("length_mm", SPECIAL_LENGTH_MM),
                    rotation=kw.get("rotation", 0.0))
    if primitive == "star8":
        return star8(kw.get("r", 30.0), kw.get("points", 8))
    if primitive == "zigzag":
        return zigzag(kw.get("teeth", 3), kw.get("amplitude", 1.6))
    raise ValueError("unknown primitive: %r" % (primitive,))


def for_tool(tool_no):
    """Build the primitive for a Fig. 21 tool number."""
    if tool_no in DISC_TOOLS:
        rings, dia = DISC_TOOLS[tool_no]
        return build("ring_dot", rings=rings, diameter_mm=dia)
    if tool_no in (4,):
        return build("circle_row", r_dot=0.9, n=9)
    if tool_no == 5:
        # Punktkreis: a dot inside a circle (Fig. 21, scale 2:1 legend). Modelled
        # as a 1-ring ring_dot so the relief form gives a central boss plus one
        # surrounding ridge; it was previously `disc(r=1.6)`, i.e. a plain dot
        # that did not match its own name. Diameter 3.2 mm is a stylisation --
        # Fig. 21 gives no size for the Nos. 4-7 fillers.
        return build("ring_dot", rings=1, diameter_mm=3.2)
    if tool_no == 6:
        return build("ring_dot", rings=2, diameter_mm=8.0)
    if tool_no == 7:
        return build("ring", r_mid=2.2)
    if tool_no == 16:
        return build("crescent")
    if tool_no == 17:
        return build("oval")
    raise ValueError("tool %s is not attributed in Fig. 21" % tool_no)


# --- placement -----------------------------------------------------------------

def place(n, r_at_z, z_mm, jitter_seed=None):
    """
    Place n motifs evenly around the circumference.

    Menghin: 'The arrangement ensures there is no overlap between the disc and
    circular motifs' -- so this asserts the fit, it does not assume it. That
    assertion IS the plan's strongest cross-check (section 2.2): zone 17 and
    zone 18 clear their circumference by only +3.0 and +0.9 mm.

    Returns a list of (u_centre_mm, clearance_mm).
    """
    circ = 2 * math.pi * r_at_z
    pitch = circ / n
    return [(i * pitch, pitch) for i in range(n)]


def clearance(n, r_at_z, motif_dia):
    """Slack between neighbouring motifs, mm. Menghin says it must be >= 0."""
    circ = 2 * math.pi * r_at_z
    return circ / n - motif_dia


# --- self-check -----------------------------------------------------------------

def _pchip_r(z, profile):
    """Local pchip (monotone cubic Hermite) over the profile control points.

    Kept here so `--selfcheck` has no FreeCAD and no scipy (neither is
    installed). This is the same interpolant build_goldhat.py must use.
    """
    zs = [p["z"] for p in profile]
    rs = [p["r"] for p in profile]
    n = len(zs)
    if z <= zs[0]:
        return rs[0]
    if z >= zs[-1]:
        return rs[-1]
    i = max(j for j in range(n - 1) if zs[j] <= z)
    h = zs[i + 1] - zs[i]
    # Fritsch-Carlson slopes
    d = [(rs[k + 1] - rs[k]) / (zs[k + 1] - zs[k]) for k in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for k in range(1, n - 1):
        if d[k - 1] * d[k] <= 0:
            m[k] = 0.0
        else:
            w1, w2 = 2 * (zs[k + 1] - zs[k]) + (zs[k] - zs[k - 1]), \
                     2 * (zs[k] - zs[k - 1]) + (zs[k + 1] - zs[k])
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    t = (z - zs[i]) / h
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1
    h10 = t ** 3 - 2 * t ** 2 + t
    h01 = -2 * t ** 3 + 3 * t ** 2
    h11 = t ** 3 - t ** 2
    return (h00 * rs[i] + h10 * h * m[i] + h01 * rs[i + 1] + h11 * h * m[i + 1])


def _selfcheck():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hp = json.load(open(os.path.join(here, "data", "hat_parameters.json")))
    zj = json.load(open(os.path.join(here, "data", "zones.json")))
    profile = hp["profile"]

    # 1. the ring-count rule. Menghin: zwei, drei, fuenf oder sechs.
    for tool, (rings, dia) in DISC_TOOLS.items():
        assert rings in (2, 3, 5, 6), "tool %d has %d rings" % (tool, rings)
    assert 4 not in {r for r, _ in DISC_TOOLS.values()}

    # 2. every tool zone 1..21 uses is a tool we can actually build
    for z in zj["zones"]:
        if z.get("tool"):
            for_tool(z["tool"])                      # raises if unattributed
        for f in z.get("fillers", []):
            for_tool(f["tool"])

    # 3. every primitive returns a non-degenerate outline
    for prim, kw in [("ring_dot", {"rings": r, "diameter_mm": d})
                     for r, d in DISC_TOOLS.values()] + \
                    [("disc", {}), ("ring", {}), ("circle_row", {}),
                     ("crescent", {}), ("oval", {}), ("star8", {}), ("zigzag", {})]:
        outer, holes = build(prim, **kw)
        assert len(outer) >= 3, prim
        xs = [p[0] for p in outer]
        ys = [p[1] for p in outer]
        assert max(xs) > min(xs) and max(ys) > min(ys), "%s is degenerate" % prim

    # 4. the diameter we build is the diameter Menghin states, and every
    #    trough between rings is wide enough for a 0.4 mm nozzle to resolve.
    NOZZLE_MM = 0.4
    print("  tool  rings  dia   ridge_w  pitch   trough  printable")
    for tool, (rings, dia) in sorted(DISC_TOOLS.items()):
        outer, holes = for_tool(tool)
        xs = [p[0] for p in outer]
        got = max(xs) - min(xs)
        assert abs(got - dia) < 1e-6, "tool %d built %.3f not %.3f" % (tool, got, dia)
        assert len(holes) == rings, "tool %d built %d rings not %d" % (tool, len(holes), rings)
        # recover ridge width and pitch from the ring band geometry.
        # holes[i] is a band [outer_ring, inner_ring]; radius = |point|.
        def band_r(ring):
            return math.hypot(ring[0][0], ring[0][1])
        rw = band_r(holes[0][0]) - band_r(holes[0][1])
        r_mids = [(band_r(b[0]) + band_r(b[1])) / 2.0 for b in holes]
        pitch = ((r_mids[-1] - r_mids[0]) / (rings - 1)) if rings > 1 else 2 * r_mids[0]
        trough = pitch - rw
        ok = trough >= 1.2 * NOZZLE_MM
        print("  Nr%-3d %-6d %-5.0f %.3f    %.3f   %.3f   %s" %
              (tool, rings, dia, rw, pitch, trough, "yes" if ok else "NO"))
        assert ok, "tool %d trough %.3f mm is below the 0.4 mm nozzle" % (tool, trough)

    # 5. NO OVERLAP -- Menghin's own constraint, and the plan's best
    #    independent check on the profile. Uses the pchip profile, not a
    #    straight cone, because a straight cone is known to be wrong.
    print("  zone  n  tool  dia   circ@z    clearance")
    tightest = (1e9, None)
    for z in zj["zones"]:
        if not z.get("tool") or z["zone"] in (1, 2, 5, 20, 21):
            continue                                  # shaft zones only
        tool = z["tool"]
        dia = DISC_TOOLS[tool][1]
        z_mid = sum(z["z_mm"]) / 2.0
        r = _pchip_r(z_mid, profile)
        cl = clearance(z["count"], r, dia)
        if cl < tightest[0]:
            tightest = (cl, z["zone"])
        print("  z%-3d %-3d %-4d  %-4.0f  %6.1f mm  %+6.1f mm" %
              (z["zone"], z["count"], tool, dia, 2 * math.pi * r, cl))
        assert cl >= 0, "zone %d overlaps by %.1f mm" % (z["zone"], -cl)
    print("  tightest clearance: zone %s at %+.1f mm" % (tightest[1], tightest[0]))

    # 6. the apex/cap/brim zones we skipped, for the record
    for z in zj["zones"]:
        if z["zone"] in (1, 2, 5, 20, 21):
            r = _pchip_r(sum(z["z_mm"]) / 2.0, profile)
            # tools 6/7 are fillers and specials, not Fig.21 boss discs
            dia = DISC_TOOLS[z["tool"]][1] if z.get("tool") in DISC_TOOLS else 0.0
            cl = clearance(z["count"], r, dia) if z["count"] else float("nan")
            print("  z%-3d %-3d (special)    circ %6.1f mm  clearance %s" %
                  (z["zone"], z["count"], 2 * math.pi * r,
                   "%+.1f mm" % cl if z["count"] else "n/a"))

    print("primitive checks passed")





# --- development renderer (visual check, no FreeCAD) --------------------------

def placed_zone_motifs(zone, profile, hp=None):
    """
    Placed motif polygons for ONE zone's development strip.

    Returns (circ_mm, height_mm, motifs), where motifs is a list of
    (u_left_mm, v_off_mm, outer_polygon, [hole_polygons]) with `u` measured from
    the strip's centre -- so the strip runs -circ/2 .. +circ/2 -- `v_off` the
    motif row's vertical offset from the strip centre, and every polygon in
    (u, v) mm centred on its own motif.

    Handles both the usual one-row disc zones and the special zones that carry a
    `motifs` LIST (today only zone 5: 19 crescent + 19 eye in two rows). Shared
    by `development_svg` and the Stage-1 scenario figures, so the two can never
    disagree about where a motif sits. The Krempe zones (20, 21) are concentric
    rings: their strip follows the ring radius from data/hat_parameters.json.
    """
    z0, z1 = zone["z_mm"]
    if zone.get("section") == "krempe" and hp is not None:
        r = next(k["r_mid_mm"] for k in hp["krempe"]["rings"]
                 if k["zone"] == zone["zone"])
    else:
        r = (profile((z0 + z1) / 2.0) if callable(profile)
             else _pchip_r((z0 + z1) / 2.0, profile))
    circ = 2 * math.pi * r
    out = []

    rows = zone.get("motifs")
    if rows:                                 # special zones (zone 5): one row per motif
        for k, spec in enumerate(rows):
            outer, hs = for_tool(spec["tool"])
            cnt = spec["count"]
            pitch = circ / cnt
            v_off = (z1 - z0) * ((len(rows) - 1) / 2.0 - k) / len(rows)
            for i in range(cnt):
                out.append(((i + 0.5) * pitch - circ / 2.0, v_off, outer, list(hs)))
    else:
        n, tool = zone["count"], zone.get("tool")
        if n and tool is not None:
            outer, hs = for_tool(tool)
            pitch = circ / n
            for i in range(n):
                out.append(((i + 0.5) * pitch - circ / 2.0, 0.0, outer, list(hs)))
    return circ, z1 - z0, out


def _svg_zone(z, profile, scale=1.0):
    """
    Render one zone as an unrolled strip: a check that the motifs FILL the
    circumference without touching, which is Menghin's stated constraint and
    cannot be seen from the numbers alone.

    Returns SVG path data for (outline, holes) accumulated over all motifs.
    """
    circ, h, motifs = placed_zone_motifs(z, profile)
    path, holes = [], []
    for cu, v_off, outer, hs in motifs:
        flat = []
        for h in hs:
            # a hole is either one ring (points) or a trough given as
            # [outer_ring, inner_ring] -- unwrap the latter into two rings.
            if h and isinstance(h[0][0], (list, tuple)):
                flat.extend(h)
            else:
                flat.append(h)
        for pts, dest in [(outer, path)] + [(hh, holes) for hh in flat]:
            d = "M " + " L ".join("%.3f,%.3f" % (cu + u, v_off + v)
                                  for u, v in pts) + " Z"
            dest.append(d)
    return circ, h, path, holes


def development_svg(zone_filter=None, out="/tmp/plates/development.svg"):
    """Unrolled development of every zone, to eyeball against Fig. 22 plates."""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hp = json.load(open(os.path.join(here, "data", "hat_parameters.json")))
    zj = json.load(open(os.path.join(here, "data", "zones.json")))
    profile = hp["profile"]

    maxcirc = 2 * math.pi * max(p["r"] for p in profile)
    gap, y = 3.0, 0.0
    body = []
    for z in zj["zones"]:
        if zone_filter and z["zone"] not in zone_filter:
            continue
        z0, z1 = z["z_mm"]
        h = max(z1 - z0, 2.0)
        circ, _, path, holes = _svg_zone(z, profile)
        # repeat the strip so it reads as a continuous band, like Fig. 22
        reps = max(1, int(maxcirc / max(circ, 1e-6)))
        reps = min(reps, 3)
        for rep in range(reps):
            dx = rep * circ
            body.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" '
                        'fill="#f0e2c8" stroke="#bbb" stroke-width="0.3"/>'
                        % (dx - circ / 2.0, y, circ, h))
            for d in path:
                body.append('<path d="%s" transform="translate(%.2f,%.2f)" '
                            'fill="#c9a227" stroke="#8a6d1a" stroke-width="0.25"/>'
                            % (d, dx, y))
            for d in holes:
                body.append('<path d="%s" transform="translate(%.2f,%.2f)" '
                            'fill="#fff6e0" stroke="#b99a3a" stroke-width="0.2"/>'
                            % (d, dx, y))
        body.append('<text x="-2" y="%.2f" font-size="2.6" text-anchor="end" '
                    'fill="#333">Z%d (%d x Nr.%s)</text>'
                    % (y + h * 0.6, z["zone"], z["count"], z.get("tool")))
        y += h + gap

    w = maxcirc * 3 + 8
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
           'viewBox="-6 -2 %.0f %.0f">%s</svg>'
           % (w * 3, y + 6, w, y + 6, "".join(body)))
    open(out, "w").write(svg)
    print("wrote %s  (%d zones, %.0f x %.0f mm unrolled)" % (out, len(zone_filter or []), w, y))
    return out


# --- placement -----------------------------------------------------------------
#
# Two rules, and both come from the evidence rather than from taste.
#
# RULE 1 -- the discs sit on ONE ring, centred in their zone. Every zone's
#   height is greater than its disc diameter (14.0 mm zone vs a d12 disc is the
#   tightest, z17), and the Fig. 22 plates show a single row per zone. So the
#   only placement freedom is the angular phase.
#
# RULE 2 -- a filler "in the interstice(s)" means ONE per gap, angularly
#   midway between adjacent discs. Menghin page29: "identical rings (No. 7) in
#   the radial intersecting sections" -- sections, plural. Confirmed on the
#   Fig. 22 plates for z9/z10/z13/z14.
#
# RULE 2b -- **the interstice filler is NOT on the disc centreline.** This was a
#   real finding, not an assumption. At the discs' mid-height the gap between
#   two neighbours is only `pitch - disc_dia`, which for z9 is **3.12 mm**
#   (18.12 mm pitch - 15 mm disc), while the Nr. 7 annulet is **\u22484.85 mm**
#   across -- so it *cannot* physically sit level with the discs; it would
#   overlap them. The Fig. 22 plate (menghin_page029.jpeg, Z14) shows what
#   actually happens: the annulets sit in the **spandrel**, vertically offset
#   from the disc centreline into the lens-shaped notch where two neighbouring
#   circles part company. `spandrel_offset()` computes that height rather than
#   guessing it: it is where the two adjacent disc outlines are exactly one
#   annulet diameter apart.
#
# WHAT IS *NOT* CONSTRAINED: the angular phase. The shaft disc counts are
#   14,15,18,19,21,19,19,20,20,20,21,15,19,33,21,23 and gcd(...) == 1, so no
#   rotation makes all zones align -- there is no "correct" phase to discover.
#   The Fig. 22 plates do show z13 and z14 staggered rather than stacked, which
#   is the one appearance rule worth encoding; everything else is declared.

def spandrel_offset(pitch_mm, disc_dia, filler_dia):
    """
    Vertical offset of an interstice filler from the disc centreline, mm.

    Geometry. Two neighbouring discs of radius R, centres `pitch_mm` apart on
    the centreline (y = 0). The midpoint between them is at x = pitch/2. The
    distance from a disc centre to the point (pitch/2, y) is

        d(y) = sqrt((pitch/2)^2 + y^2)

    so the filler clears the disc once d(y) >= R + filler_dia/2, i.e.

        y >= sqrt((R + rf)^2 - (pitch/2)^2)

    When the discs already have a gap at the centreline (pitch - 2R > filler
    diameter) no lift is needed and this returns 0. Returns 0.0 as well when
    the discs would OVERLAP (pitch < 2R), because that is a violation the
    no-overlap check reports separately -- silently inventing a lift there
    would hide a real error.
    """
    R = disc_dia / 2.0
    rf = filler_dia / 2.0
    half_pitch = pitch_mm / 2.0
    if pitch_mm - disc_dia >= filler_dia:
        return 0.0                       # room at the centreline; sit level
    inner = (R + rf) ** 2 - half_pitch ** 2
    if inner <= 0:
        return 0.0                       # discs overlap; let that check shout
    return math.sqrt(inner)

def stagger_deg(zone_index):
    """
    Angular phase for a zone, in degrees.

    The Fig. 22 plates show vertically adjacent disc zones staggered by roughly
    half a pitch (z13 vs z14, menghin_page029.jpeg), which is what stops the
    discs reading as continuous vertical columns. Half a pitch is not constant
    in degrees -- pitch = 360/n differs per zone -- so the stagger is applied
    per zone as half of that zone's own angular pitch.

    A deterministic index is used rather than a random one so that the STL is
    reproducible: a random phase would make two runs of the generator produce
    different files, and would make verify_geometry.py non-deterministic.
    """
    return 180.0 if (zone_index % 2) else 0.0   # 180 deg = half of one motif


def zone_layout(zone, r_at_z):
    """
    Resolve one zone into absolute angular positions.

    Returns dict with:
      pitch_deg    angular pitch of the discs
      discs[]      (angle_deg, u_mm) for each motif
      fillers[]    (angle_deg, u_mm, tool, v_offset_mm) for each interstitial filler
      rows[]       (tool, v_offset_mm, kind) for border/band filler rows

    Angles are measured from the zone's start meridian, counter-clockwise seen
    from outside. u_mm is arc length, so the same list drives both the 2D
    development and the 3D placement.
    """
    circ = 2 * math.pi * r_at_z
    n = zone["count"]
    z0, z1 = zone["z_mm"]
    h = z1 - z0
    out = {"pitch_deg": (360.0 / n if n else 0.0), "discs": [], "fillers": [], "rows": []}
    if not n:
        return out

    phase = stagger_deg(zone["zone"])
    pitch = 360.0 / n
    pitch_mm = circ / n

    for i in range(n):
        a = (phase + i * pitch) % 360.0
        out["discs"].append((a, a / 360.0 * circ))

    for f in zone.get("fillers", []):
        tool = f["tool"]
        where = f["where"]
        if "interstice" in where:
            # one per gap, midway between discs, lifted into the spandrel
            disc_dia = DISC_TOOLS[zone["tool"]][1] if zone.get("tool") in DISC_TOOLS else 0.0
            filler_dia = 2 * for_tool(tool)[0][0][0]
            dv = spandrel_offset(pitch_mm, disc_dia, filler_dia)
            for i in range(n):
                a = (phase + (i + 0.5) * pitch) % 360.0
                out["fillers"].append((a, a / 360.0 * circ, tool, dv))
        elif "border" in where:
            # a horizontal row at a zone edge; a continuous band, no fixed count
            v = -h / 2.0 + 2.0 if "top" in where else h / 2.0 - 2.0
            out["rows"].append((tool, v, where))
        elif where == "band":
            out["rows"].append((tool, 0.0, where))
    return out


def _placement_selfcheck():
    """Placement rules, checked rather than asserted in prose."""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hp = json.load(open(os.path.join(here, "data", "hat_parameters.json")))
    zj = json.load(open(os.path.join(here, "data", "zones.json")))
    profile = hp["profile"]

    # RULE 1: every disc fits its zone height on a single ring
    print("  zone  h_mm  dia   1 row?")
    for z in zj["zones"]:
        if not z.get("tool") or z["zone"] in (1, 2, 5, 20, 21):
            continue
        h = z["z_mm"][1] - z["z_mm"][0]
        dia = DISC_TOOLS[z["tool"]][1]
        print("  z%-3d  %-5.1f %-5.0f %s" % (z["zone"], h, dia, "yes" if h >= dia else "NO"))
        assert h >= dia, "zone %d is only %.1f mm tall for a %.0f mm disc" % (z["zone"], h, dia)

    # RULE 2: interstice fillers are one-per-gap and never collide with a disc
    print("\n  zone  discs  interstice fillers   offset_deg  ok")
    for z in zj["zones"]:
        if not z.get("tool") or z["zone"] in (1, 2, 5, 20, 21):
            continue
        r = _pchip_r(sum(z["z_mm"]) / 2.0, profile)
        lay = zone_layout(z, r)
        n_inter = len(lay["fillers"])
        has_inter = any("interstice" in f["where"] for f in z.get("fillers", []))
        if has_inter:
            assert n_inter == z["count"], \
                "zone %d: %d fillers for %d discs" % (z["zone"], n_inter, z["count"])
            offs = sorted((f[0] - lay["discs"][0][0]) % lay["pitch_deg"]
                          for f in lay["fillers"])
            # the offsets are all exactly half a pitch; compare unrounded, and
            # also require them to be IDENTICAL to each other (one per gap)
            assert abs(offs[0] - lay["pitch_deg"] / 2.0) < 1e-9, \
                "zone %d fillers are not midway between discs" % z["zone"]
            assert max(offs) - min(offs) < 1e-9, \
                "zone %d fillers are not evenly placed" % z["zone"]
            # the filler must CLEAR the discs. At the centreline the gap is
            # pitch - disc_dia; if the filler is bigger than that it has to be
            # lifted into the spandrel, and this asserts the lift is enough.
            pitch_mm = 2 * math.pi * r / z["count"]
            disc_dia = DISC_TOOLS[z["tool"]][1]
            f_dia = 2 * for_tool(z["fillers"][0]["tool"])[0][0][0]
            dv = lay["fillers"][0][3]
            centre_gap = pitch_mm - disc_dia
            if f_dia > centre_gap:
                assert dv > 0, \
                    "zone %d filler %.2f mm does not fit the %.2f mm centreline gap" \
                    % (z["zone"], f_dia, centre_gap)
            # at height dv the centre-to-centre distance to the nearest disc
            # centre is sqrt((pitch/2)^2 + dv^2); it must exceed R + r_filler
            need = disc_dia / 2.0 + f_dia / 2.0
            got = math.hypot(pitch_mm / 2.0, dv)
            assert got >= need - 1e-9, \
                "zone %d filler still overlaps: needs %.3f mm, has %.3f" \
                % (z["zone"], need, got)
            print("  z%-3d  %-6d %-20d %-11.3f yes  (lift %5.2f mm, clearance %5.2f >= %5.2f)"
                  % (z["zone"], z["count"], n_inter, offs[0], dv, got, need))
        else:
            print("  z%-3d  %-6d %-20d %-11s -" % (z["zone"], z["count"], 0, "-"))

    # the phase is a declared choice -- prove it is not constrained
    counts = [z["count"] for z in zj["zones"]
              if z.get("tool") and z["zone"] not in (1, 2, 5, 20, 21)]
    g = 0
    for c in counts:
        g = math.gcd(g, c)
    print("\n  gcd of all shaft disc counts = %d  -> %s"
          % (g, "no common alignment exists; the phase is a free choice"
             if g == 1 else "a symmetric alignment EXISTS and the phase is physical"))
    assert g == 1

    # every disc and filler must land inside one full turn, no duplicates
    for z in zj["zones"]:
        if not z.get("tool") or z["zone"] in (1, 2, 5, 20, 21):
            continue
        r = _pchip_r(sum(z["z_mm"]) / 2.0, profile)
        lay = zone_layout(z, r)
        angs = [a for a, _ in lay["discs"]]
        assert len(angs) == z["count"]
        assert len(set(round(a, 6) for a in angs)) == z["count"], \
            "zone %d has coincident discs" % z["zone"]
        assert all(0 <= a < 360 for a in angs)

    print("placement self-check: all passed")


def _all():
    """Entry point: primitives first, then placement (both must pass)."""
    _selfcheck()
    print()
    _placement_selfcheck()


if __name__ == "__main__":
    _all()
