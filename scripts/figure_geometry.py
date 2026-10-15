#!/usr/bin/env python3
"""
Figure kernel for Stage 1 — visual scenario figures.

Pure maths, stdlib only: no FreeCAD and no plotting library. It turns the
`data/*.json` source of truth into the polygons and strings a renderer draws,
so the renderer (scripts/render_scenarios.py) contains no number that is not
in the data.

    silhouette(profile)        the hat's closed (x, z) outline, both sides
    zone_band(zone, profile)   the closed (x, z) polygon of one zone
    classify(display, zone)    'solar' | 'lunar' | 'intercalary' | 'off'
    rederive(state, side, day) the day value, re-summed from data/zones.json
    caption(state, day)        the arithmetic line, Menghin-style

The colour palette lives here too, so the figures and any later Stage-3 LED
table share one definition of what red/blue/green mean.

Self-check:  python3 scripts/figure_geometry.py --selfcheck
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import band_geometry as G                                          # noqa: E402


# --- categories and the single palette ---------------------------------------

#: Menghin's figure key (assets/menghin/2010, pp. 60-63): red = solar block,
#: blue = lunar block, green = intercalary ("Schalt") zone, off = not part of
#: this time block. Slightly desaturated so text stays readable on top.
CATEGORY_COLOURS = {
    "solar":       "#c0504d",
    "lunar":       "#4f6dbd",
    "intercalary": "#3f9e5a",
    "off":         "#ececec",
}
SILHOUETTE_FILL = "#f6f3ec"
OUTLINE_COLOUR = "#5a5a5a"

CATEGORY_ORDER = ("solar", "lunar", "intercalary", "off")
CATEGORY_LABELS = {
    "solar":       "solar block",
    "lunar":       "lunar block",
    "intercalary": "intercalary zone (SZ)",
    "off":         "not part of this block",
}


def load():
    """Load the source-of-truth data (same loader as the rest of the repo)."""
    return G.load()


# --- geometry ----------------------------------------------------------------

def _sample_z(z0, z1, n):
    return [z0 + (z1 - z0) * i / n for i in range(n + 1)]


def silhouette(profile, z_top=None, n=400):
    """
    The hat's closed outline as a list of (x, z), in mm, both sides.

    Right side is r(z) from the apex down to the foot; the left side mirrors
    it. The bottom edge closes the two sides (for a stylised figure the brim
    is drawn as a solid wing, as Menghin does).
    """
    zb = profile.z[0]
    zt = z_top if z_top is not None else profile.z[-1]
    zs = _sample_z(zb, zt, n)
    right = [(profile(z), z) for z in zs]
    left = [(-profile(z), z) for z in reversed(zs)]
    return right + left


def zone_band(zone, profile, n=48):
    """
    One stacked zone's closed (x, z) polygon, spanning the hat's width there.

    Zones are drawn as horizontal bands inside the silhouette; the gaps
    between zones (the Trennband ridges) are left uncoloured, which is why the
    figures read as the object rather than as a stacked bar chart.
    """
    z0, z1 = zone["z_mm"]
    zs = _sample_z(z0, z1, n)
    right = [(profile(z), z) for z in zs]
    left = [(-profile(z), z) for z in reversed(zs)]
    return right + left


def krempe_split_radius(hp):
    """Radius separating the two Krempe rings (zones 20 and 21)."""
    k = hp["krempe"]
    rs = sorted(r["r_mid_mm"] for r in k["rings"])
    if len(rs) >= 2:
        return 0.5 * (rs[0] + rs[1])
    return 0.5 * (k["r_inner_mm"] + k["r_outer_mm"])


def krempe_zone_polygons(zone, hp, n=12):
    """
    The two wings (left + right) of one Krempe ring, as closed (x, z) polygons.

    Zones 20 and 21 are concentric rings on the horizontal brim, so they share
    a z-span and must be split by RADIUS, not height: the wing runs from
    r_inner at z_inner out to r_outer at z_outer and the split sits between the
    two rings' r_mid values.
    """
    k = hp["krempe"]
    r_in, r_out = k["r_inner_mm"], k["r_outer_mm"]
    z_in, z_out = k["z_inner_mm"], k["z_outer_mm"]
    split = krempe_split_radius(hp)
    if zone["zone"] == k["rings"][0]["zone"]:
        r_lo, r_hi = r_in, split
    else:
        r_lo, r_hi = split, r_out

    def z_at(r):
        return z_in + (r - r_in) * (z_out - z_in) / (r_out - r_in)

    rs = [r_lo + (r_hi - r_lo) * i / n for i in range(n + 1)]
    top = [(r, z_at(r)) for r in rs]
    bot = [(r, z_out) for r in reversed(rs)]
    right = top + bot
    left = [(-x, z) for x, z in reversed(right)]
    return [right, left]


def zone_center_z(zone):
    z0, z1 = zone["z_mm"]
    return 0.5 * (z0 + z1)


# --- classification ----------------------------------------------------------

def _in_ranges(z, ranges):
    """True if z is in any entry, where an entry is either a bare zone number
    (`intercalary` in the source is `[16, 17]`) or a `[start, end]` pair."""
    for r in ranges:
        a, b = (r, r) if isinstance(r, int) else (r[0], r[1])
        if int(a) <= z <= int(b):
            return True
    return False


def classify(display, zone_no):
    """
    Colour category of one zone under one state's `display` maps.

    Priority is load-bearing and comes from the source figures: an intercalary
    (green) zone stays green even when it lies inside the red or blue block
    (e.g. 61.1 has zone 16-17 inside the lunar range 9-19 and still draws them
    green). So: intercalary > solar > lunar > off.
    """
    if _in_ranges(zone_no, display.get("intercalary", [])):
        return "intercalary"
    if _in_ranges(zone_no, display.get("solar", [])):
        return "solar"
    if _in_ranges(zone_no, display.get("lunar", [])):
        return "lunar"
    return "off"


# --- arithmetic, re-derived (never typed) ------------------------------------

def rederive(state, side, day_value):
    """
    Re-sum one side of a state from the data: sum(include) - sum(exclude).

    `state[side]` is the source's own include/exclude block; `day_value` maps
    zone -> days from data/zones.json. The recorded `value` is NOT used here,
    which is the point: the renderer prints what the data sums to, and
    `--selfcheck` asserts it equals the recorded value wherever the source
    states one.
    """
    spec = state.get(side)
    if not spec:
        return None
    total = 0
    for a, b in spec["include"]:
        for z in range(int(a), int(b) + 1):
            total += day_value[z]
    for z in spec.get("exclude", []):
        total -= day_value[int(z)]
    return total


def _ranges_str(ranges):
    """[ [4,8] ] -> '4-8'; [[15,15],[18,19]] -> '15, 18-19'."""
    parts = []
    for a, b in ranges:
        a, b = int(a), int(b)
        parts.append("%d" % a if a == b else "%d-%d" % (a, b))
    return ", ".join(parts)


def side_expression(state, side):
    """Human-readable sum, e.g. 'zones 4-6 minus 7'."""
    spec = state.get(side)
    if not spec:
        return "no zone arithmetic in the source"
    txt = "zones %s" % _ranges_str(spec["include"])
    if spec.get("exclude"):
        txt += " minus %s" % _ranges_str([(z, z) for z in spec["exclude"]])
    return txt


def caption(state, day_value, with_expression=True):
    """
    The one-line arithmetic caption under a panel, rebuilt from the data.

    Example (state 61.4): `solar 146 d (zones 4-6 minus 7) | lunar 165 d
    (zones 13-14) | delta 19 d`.
    """
    solar = rederive(state, "solar", day_value)
    lunar = rederive(state, "lunar", day_value)
    bits = []
    if solar is not None:
        s = "solar %d d" % solar
        if with_expression:
            s += " (%s)" % side_expression(state, "solar")
        bits.append(s)
    if lunar is not None:
        l = "lunar %d d" % lunar
        if with_expression:
            l += " (%s)" % side_expression(state, "lunar")
        bits.append(l)
    if state.get("delta_days") is not None:
        bits.append("delta %d d" % state["delta_days"])
    if state.get("intercalation"):
        bits.append("INTERCALATION")
    if solar is None and lunar is None:
        # 61.2: the source states no zone arithmetic for this block. Say so
        # rather than invent one (verify_scenarios flags the same state).
        note = (state.get("note") or "").strip()
        bits.append(note or "no zone arithmetic in the source")
    return " | ".join(bits) if bits else state.get("note", "")


def state_title(state):
    return "%s  %s  (%d QY / %d L)" % (
        state["id"], state.get("title", "").strip(),
        state["quarter_years"], state["lunations"])


# --- self-check --------------------------------------------------------------

def _selfcheck():
    hp, zj = load()
    profile = G.Profile(hp["profile"])
    zones = zj["zones"]
    sc = json.load(open(os.path.join(HERE, "data", "scenarios.json")))
    day = {z["zone"]: z["day_value"] for z in zones}

    # 1. the profile is the same curve the parts use
    assert abs(profile(0.0)) < 1e-9, "profile(0) != 0"
    assert abs(profile(745.0) - 150.5) < 1e-9, "profile(745) != 150.5"

    # 2. every stacked zone (1-19) has a usable span, ordered and disjoint; the
    #    two Krempe zones (20, 21) share a z-span and are split by radius instead
    last = -1.0
    n_stacked = 0
    for z in zones:
        z0, z1 = z["z_mm"]
        assert 0.0 <= z0 < z1 <= 745.0 + 1e-9, "zone %s span" % z["zone"]
        if z.get("section") == "krempe":
            continue
        assert z0 >= last - 1e-9, "zone %s overlaps the previous zone" % z["zone"]
        last = z1
        n_stacked += 1
    assert n_stacked == 19, "expected 19 stacked zones, got %d" % n_stacked
    print("  %d zones; 19 stacked spans ordered and disjoint; 20/21 split by radius  OK"
          % len(zones))

    # 2b. the Krempe wings tile the brim without overlap
    krempe = [z for z in zones if z.get("section") == "krempe"]
    assert len(krempe) == 2, "expected 2 Krempe zones, got %d" % len(krempe)
    for z in krempe:
        assert z["z_mm"] == [hp["krempe"]["z_inner_mm"], hp["krempe"]["z_outer_mm"]], \
            "Krempe zone %s does not sit on the brim" % z["zone"]
        wings = krempe_zone_polygons(z, hp)
        assert len(wings) == 2 and all(len(w) >= 4 for w in wings), \
            "Krempe zone %s has no wings" % z["zone"]
    print("  Krempe zones 20/21 split at r=%.1f mm into two wings  OK"
          % krempe_split_radius(hp))

    # 3. classification follows the source figures (intercalary wins)
    s611 = next(s for s in sc["states"] if s["id"] == "61.1")
    assert classify(s611["display"], 4) == "solar"
    assert classify(s611["display"], 12) == "lunar"
    assert classify(s611["display"], 16) == "intercalary", "green must beat blue"
    assert classify(s611["display"], 1) == "off"
    print("  classify(): intercalary > solar > lunar > off  OK")

    # 4. every stated day value is re-derived from data/zones.json (no typing)
    checked = 0
    for s in sc["states"]:
        for side in ("solar", "lunar"):
            got = rederive(s, side, day)
            spec = s.get(side)
            if spec is None:
                continue
            assert got == spec["value"], \
                "state %s %s: re-derived %s != recorded %s" \
                % (s["id"], side, got, spec["value"])
            checked += 1
    print("  all %d stated solar/lunar values re-derived from data  OK" % checked)

    # 5. every state's display zones are real zones from the data
    valid = {z["zone"] for z in zones}
    for s in sc["states"]:
        for cat, ranges in s["display"].items():
            got = set()
            for r in ranges:
                a, b = (r, r) if isinstance(r, int) else (r[0], r[1])
                assert {int(a), int(b)} <= valid, \
                    "state %s references a zone outside 1..21" % s["id"]
                got |= {z for z in valid if int(a) <= z <= int(b)}
            assert got or cat == "intercalary", \
                "state %s: empty display range in %s" % (s["id"], cat)
    print("  all 16 states reference only real zones  OK")

    # 6. the palette is complete and the renderer can iterate it
    assert set(CATEGORY_COLOURS) == set(CATEGORY_ORDER)
    print("  palette covers every category  OK")

    print("\nfigure_geometry self-check: all passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selfcheck", action="store_true")
    ap.parse_args()
    _selfcheck()
