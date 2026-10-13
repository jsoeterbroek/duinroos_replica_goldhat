#!/usr/bin/env python3
"""
verify_geometry.py — the P4 acceptance harness.

Runnable, no frameworks, stdlib only, no FreeCAD:

    python3 scripts/verify_geometry.py                     # data checks + any stl/*.stl
    python3 scripts/verify_geometry.py --stl stl/z13.stl   # check specific files
    python3 scripts/verify_geometry.py --selftest          # exercise the STL maths

Two tiers, deliberately separate:

  DATA tier   — always runs.  Reads data/hat_parameters.json, data/zones.json
                and scripts/motifs.py, and asserts the things that can be
                checked before a single solid exists: the 745 mm budget, the
                per-zone pitch/ligature fit (motifs.place/clearance), and that
                every part, INCLUDING the three Krempe sectors, fits a
                256 mm bed.  This is the tier that must pass at P2/P3.

  STL tier    — runs when parts exist.  Parses each mesh, checks it is
                2-manifold and closed, has positive volume, and fits the bed.
                Written BEFORE the P4 parts, so the exit criterion ("all 22
                STLs watertight, verify_geometry passes") is a check, not a
                claim.  Point it at any STL with --stl.

The mesh maths is local on purpose: this script must run where FreeCAD is not
(the repo's other checkers are stdlib-only for the same reason).  It duplicates
nothing that matters -- `nonmanifold_edges` in build_goldhat is the build-time
guard, this is the artifact-time one.
"""

import argparse
import json
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import band_geometry as G                                     # noqa: E402
import motifs as M                                            # noqa: E402

BED_MM = 256.0                 # Bambu P1/X1 build volume
HEIGHT_TOTAL_MM = 745.0
HEIGHT_TOL_MM = 3.0
BUDGET = "769 - 40 (2 x tussenstuk) - 9 (tb19) + 18 (cuff) + 7 (Krempe rise)"
BUDGET_TERMS = [769.0, -40.0, -9.0, +18.0, +7.0]

# the Krempe is ONE flat plate of outer diameter 301 mm -- wider than the bed,
# so it is split radially into sectors (plan section 2.3). The sector count is
# a data value (krempe.sectors); this checks the claim rather than trusting it.
KREMPE_PART_NAMES = ("krempe_a", "krempe_b", "krempe_c")


# --- the STL tier -------------------------------------------------------------

def read_stl(path):
    """
    A binary or ASCII STL as a list of (a, b, c) vertex triples.

    Binary is detected by the file length matching `84 + 50*n` -- the same
    test most tools use, and the only reliable one, because the 80-byte
    header is free text (many exporters put a name there, sometimes starting
    with "solid", which is why "starts with solid" is NOT a valid ascii test).
    """
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(84)
    if len(head) == 84:
        n = struct.unpack("<I", head[80:84])[0]
        if size == 84 + 50 * n:
            tris = []
            with open(path, "rb") as f:
                f.seek(84)
                for _ in range(n):
                    v = struct.unpack("<12fH", f.read(50))
                    tris.append(((v[3], v[4], v[5]),
                                 (v[6], v[7], v[8]),
                                 (v[9], v[10], v[11])))
            return tris
    return _read_ascii_stl(path)


def _read_ascii_stl(path):
    tris, cur = [], []
    with open(path, "r", errors="replace") as f:
        for line in f:
            s = line.split()
            if s[:1] == ["vertex"] and len(s) >= 4:
                cur.append((float(s[1]), float(s[2]), float(s[3])))
                if len(cur) == 3:
                    tris.append(tuple(cur))
                    cur = []
    if not tris:
        raise ValueError("%s: no triangles found" % path)
    return tris


def _key(p, q=4):
    return (round(p[0], q), round(p[1], q), round(p[2], q))


def stl_stats(tris):
    """
    A dict of the checks a slicer cares about: bbox, signed volume, edge-use
    histogram and the non-manifold edge list.
    """
    xs, ys, zs = [], [], []
    vol = 0.0
    edges = {}
    for a, b, c in tris:
        xs += [a[0], b[0], c[0]]
        ys += [a[1], b[1], c[1]]
        zs += [a[2], b[2], c[2]]
        # signed volume of the tetra (origin, a, b, c):  a . (b x c) / 6
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
        ka, kb, kc = _key(a), _key(b), _key(c)
        for p, q in ((ka, kb), (kb, kc), (kc, ka)):
            e = (p, q) if p <= q else (q, p)
            edges[e] = edges.get(e, 0) + 1
    bad = [e for e, n in edges.items() if n != 2]
    return {
        "bbox": (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)),
        "z": (min(zs), max(zs)),
        "max_r": max(math.hypot(a[0], a[1]) for a, _, _ in tris),
        "volume": abs(vol),
        "edges": len(edges),
        "nonmanifold": bad,
    }


def check_stl(path, name=None):
    name = name or os.path.basename(path)
    st = stl_stats(read_stl(path))
    dx, dy, dz = st["bbox"]
    assert dx <= BED_MM + 1e-6 and dy <= BED_MM + 1e-6 and dz <= BED_MM + 1e-6, \
        "%s: bbox %.1f x %.1f x %.1f exceeds the %.0f mm bed" % ((name, dx, dy, dz) + (BED_MM,))
    assert not st["nonmanifold"], \
        "%s: %d non-manifold edge(s); first %s" % (name, len(st["nonmanifold"]),
                                                   st["nonmanifold"][0])
    assert st["volume"] > 0.0, "%s: zero or negative volume -- not a closed solid" % name
    return st


# --- the DATA tier ------------------------------------------------------------

def sector_bbox(r_out, sectors, r_in=0.0):
    """
    The SMALLEST bounding box (width, height) of one radial sector of an
    annulus, over all rotations. A 120-degree sector of the 301 mm Krempe has
    a bounding box of 225.8 x 130.3 mm, not 150.5 x 260.7 -- orientation is
    the whole question, so this searches for the best one instead of assuming
    a symmetric layout (which would wrongly reject the 3-sector split).
    """
    alpha = 2 * math.pi / sectors
    pts = []
    for i in range(721):                         # the arc, half a degree apart
        t = alpha * i / 720.0
        pts.append((r_out * math.cos(t), r_out * math.sin(t)))
    if r_in > 0.0:
        for i in range(721):
            t = alpha * i / 720.0
            pts.append((r_in * math.cos(t), r_in * math.sin(t)))
    pts += [(r_out, 0.0), (r_in, 0.0)]
    best = None
    for deg in range(0, 90):
        p = math.radians(deg)
        c, s = math.cos(p), math.sin(p)
        xs = [x * c - y * s for x, y in pts]
        ys = [x * s + y * c for x, y in pts]
        wh = (max(xs) - min(xs), max(ys) - min(ys))
        if best is None or max(wh) < max(best):
            best = wh
    return best


def data_checks(hp, zj, verbose=True):
    profile = G.Profile(hp["profile"])
    print("== data tier ==")

    # 1. the height budget, twice: ring table and the one-line closure
    total = sum(r["h"] for r in hp["rings"])
    print("  ring table sum            %.1f mm   (expect %.1f)" % (total, HEIGHT_TOTAL_MM))
    assert abs(total - HEIGHT_TOTAL_MM) < 1e-6, "ring table does not sum to 745"
    budget = sum(BUDGET_TERMS)
    print("  budget closure            %.1f mm   (%s)" % (budget, BUDGET))
    assert abs(budget - HEIGHT_TOTAL_MM) < 1e-6, "the 769 mm budget does not close to 745"

    # 2. contiguous boundaries
    zb = hp["zone_boundaries_mm"]
    for i in range(len(zb) - 1):
        assert zb[i] < zb[i + 1], "zone boundaries not increasing at %d" % i

    # 3. per-zone pitch vs circumference -- Menghin's no-overlap constraint,
    #    and, for the window forms, the 3 mm ligature. The narrowest edge of
    #    the band is the binding circumference, not the middle.
    lig = hp["window_ligature_min_mm"]
    form = hp.get("motif_form", "TBD")
    # All discs in a zone sit on ONE row, so their widest circle is at that
    # row's height -- there the neighbours are nearest. That circumference is
    # the binding one; the zone's narrowest EDGE is not (a disc is a point at
    # its top and bottom). The plan's phrase "min circumference in zone" is the
    # stricter, edge reading. Both are printed; the assertion is on the row.
    print("\n  zone  n   tool dia   r_row    slack_row  edge_total  window_max(3mm)")
    worst_slack = (1e9, None)
    worst_win = (1e9, None)
    tight = []
    for z in zj["zones"]:
        n = z["count"]
        if not n or z.get("tool") not in M.DISC_TOOLS:
            continue
        dia = M.DISC_TOOLS[z["tool"]][1]
        if z["section"] == "krempe":
            r_row = next(k["r_mid_mm"] for k in hp["krempe"]["rings"]
                         if k["zone"] == z["zone"])
            edge_total = None
        else:
            z0, z1 = z["z_mm"]
            r_row = profile(0.5 * (z0 + z1))       # motifs.py places at mid-zone
            edge_total = 2 * math.pi * min(profile(z0), profile(z1)) - n * dia
        slack = M.clearance(n, r_row, dia)
        win_max = dia + slack - lig
        print("  z%-3d  %-3d %-4d %-5.1f %-8.2f %+-9.2f %-11s %.1f"
              % (z["zone"], n, z["tool"], dia, r_row, slack,
                 "-" if edge_total is None else "%+.2f" % edge_total, win_max))
        assert slack >= 0.0, "zone %d: motifs overlap by %.2f mm" % (z["zone"], -slack)
        if edge_total is not None and edge_total < 0.2:
            tight.append((z["zone"], edge_total))
        if slack < worst_slack[0]:
            worst_slack = (slack, z["zone"])
        if win_max < worst_win[0]:
            worst_win = (win_max, z["zone"])
    print("  tightest row slack         %+.2f mm at z%d" % worst_slack)
    print("  tightest window @3 mm lig  %.1f mm at z%d" % worst_win)
    for zone, et in tight:
        print("  WARNING z%d: only %+.2f mm total slack at the zone's narrowest edge;"
              " relief is fine (discs are centred) but a full-height window is not"
              % (zone, et))
    if form in ("window", "relief_window"):
        assert worst_win[0] > 0.0, \
            "z%d: no 3 mm-ligature window fits under its boss (max %.1f mm)" \
            % worst_win
    else:
        # 'TBD'/'relief': the ligature applies to windows only, so record it
        print("  motif_form=%r: the 3 mm ligature is a window constraint only" % form)

    # 4. printability -- every stacked part, and the Krempe sectors, on the bed.
    print("\n  part            max_dia  fits %.0f mm" % BED_MM)
    worst = 0.0
    for r in hp["rings"]:
        if r["kind"] in ("trennband", "krempe"):
            continue
        _, ring, z0, z1 = G.band_ring(hp["rings"], r["id"])
        n = 40
        d = 2 * max(profile(z0 + (z1 - z0) * i / n) for i in range(n + 1))
        worst = max(worst, d)
        print("  %-14s %6.1f   %s" % (r["id"], d, "yes" if d <= BED_MM else "NO"))
        assert d <= BED_MM, "%s is %.1f mm wide" % (r["id"], d)
    k = hp["krempe"]
    bw, bh = sector_bbox(k["r_outer_mm"], k["sectors"], k["r_inner_mm"])
    print("  krempe (%d sectors) %6.1f x %.1f   %s   (full disc %.1f mm would NOT fit)"
          % (k["sectors"], bw, bh, "yes" if max(bw, bh) <= BED_MM else "NO",
             2 * k["r_outer_mm"]))
    assert max(bw, bh) <= BED_MM, \
        "%d Krempe sectors still do not fit the bed" % k["sectors"]
    for s in range(2, k["sectors"]):
        bw2, bh2 = sector_bbox(k["r_outer_mm"], s, k["r_inner_mm"])
        if max(bw2, bh2) <= BED_MM:
            print("  NOTE: %d sectors would also fit (%.1f x %.1f); the data says %d"
                  % (s, bw2, bh2, k["sectors"]))
    print("  worst stacked-part diameter %.1f mm" % worst)


# --- STL discovery + stack ----------------------------------------------------

def expected_parts(hp):
    names = ["z%02d" % i for i in range(1, 20)]
    if hp["krempe"]["sectors"] == 3:
        names += list(KREMPE_PART_NAMES)
    else:
        names += ["krempe_%d" % (i + 1) for i in range(hp["krempe"]["sectors"])]
    return names


def discover_stls():
    d = os.path.join(HERE, "stl")
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, f) for f in os.listdir(d)
                  if f.lower().endswith(".stl"))


# --- self-test ----------------------------------------------------------------

def selftest():
    """A closed tetrahedron and an open square: the maths must tell them apart."""
    a, b, c = (0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (0.0, 10.0, 0.0)
    d = (0.0, 0.0, 10.0)
    tet = [(a, c, b), (a, b, d), (b, c, d), (c, a, d)]      # outward
    st = stl_stats(tet)
    assert not st["nonmanifold"], "the tetra should be manifold"
    assert abs(st["volume"] - 1000.0 / 6.0) < 1e-9, "tetra volume %.4f" % st["volume"]
    open_sq = [(a, b, c), (a, c, d)]
    st2 = stl_stats(open_sq)
    assert st2["nonmanifold"], "an open square must be reported as non-manifold"
    bw, bh = sector_bbox(150.5, 3, 94.5)
    assert max(bw, bh) <= BED_MM, "3 Krempe sectors should fit, got %.1f x %.1f" % (bw, bh)
    bw2, bh2 = sector_bbox(150.5, 2, 94.5)
    print("  self-test: tetra volume %.1f, open square flagged, "
          "3-sector bbox %.1f x %.1f, 2-sector %.1f x %.1f"
          % (st["volume"], bw, bh, bw2, bh2))
    print("verify_geometry self-test: all passed")


# --- main ---------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stl", nargs="*", default=None,
                    help="STL files or dirs to check (default: stl/*.stl)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        selftest()
        return 0

    hp, zj = G.load()
    data_checks(hp, zj)

    print("\n== STL tier ==")
    if a.stl is None:
        paths = discover_stls()
    else:
        paths = []
        for p in a.stl:
            if os.path.isdir(p):
                paths += [os.path.join(p, f) for f in sorted(os.listdir(p))
                          if f.lower().endswith(".stl")]
            else:
                paths.append(p)
    if not paths:
        print("  no STL files found -- P4 parts not built yet.")
        print("  expected once built: %s" % ", ".join(expected_parts(hp)))
        print("\nverify_geometry: data checks passed (STL tier not run)")
        return 0

    zmin, zmax = 1e9, -1e9
    names = []
    for p in paths:
        name = os.path.basename(p)
        names.append(name.split(".")[0].replace("_stacked", ""))
        st = check_stl(p, name)
        dx, dy, dz = st["bbox"]
        z0, z1 = st["z"]
        zmin, zmax = min(zmin, z0), max(zmax, z1)
        print("  %-22s vol %9.1f mm3  bbox %.1f x %.1f x %.1f  z %.1f..%.1f  "
              "maxR %.1f  2-manifold"
              % (name, st["volume"], dx, dy, dz, z0, z1, st["max_r"]))
    # The stack height is the UNION of the parts' z-ranges, not a sum: three
    # Krempe sectors each 7 mm tall sum to 21, but together they are one 7 mm
    # plate. Only assert it when all 22 parts are present.
    expected = set(expected_parts(hp))
    if expected <= set(names):
        ext = zmax - zmin
        print("  stack z extent           %.1f .. %.1f = %.1f mm (expect %.1f +- %.1f)"
              % (zmin, zmax, ext, HEIGHT_TOTAL_MM, HEIGHT_TOL_MM))
        assert abs(ext - HEIGHT_TOTAL_MM) <= HEIGHT_TOL_MM, \
            "stack is %.1f mm, not %.1f +- %.1f" % (ext, HEIGHT_TOTAL_MM, HEIGHT_TOL_MM)
    else:
        print("  (%d of %d expected parts present -- stack-height check skipped)"
              % (len(expected & set(names)), len(expected)))

    print("\nverify_geometry: all passed")
    return 0


if __name__ == "__main__" or __name__ == os.path.splitext(
        os.path.basename(__file__))[0]:
    sys.exit(main())
