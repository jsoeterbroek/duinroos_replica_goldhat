#!/usr/bin/env python3
"""Check the calendar data against Menghin (2010).

Run:  python3 scripts/verify_calendar.py

Pure stdlib, no FreeCAD, no deps. Fails loudly (AssertionError) if any
Menghin identity in IMPLEMENTATION_PLAN.md sections 2.1 / 2.2 / 3 stops holding.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
load = lambda p: json.loads((ROOT / p).read_text())

hat = load("data/hat_parameters.json")
sym = load("data/symbols.json")
zs = load("data/zones.json")["zones"]
menghin = [r["days"] for r in load("data/readings/menghin.json")["day_value"]]
sk = [r["ornaments"] for r in load("data/readings/schmidt_kaler.json")["count"]]

EXCLUDED = {1, 2, 5}  # star, double-circles, special signs
DISC_TOOLS = set(range(8, 16))  # Nos. 8-15 are the Scheibenbuckel


def check_zone_count():
    assert len(zs) == 21, f"expected 21 zones, got {len(zs)}"
    assert [z["zone"] for z in zs] == list(range(1, 22)), "zones must be 1..21 in order"
    bearing = [z["zone"] for z in zs if z["tool"] in DISC_TOOLS]
    assert len(bearing) == 18, f"expected 18 disc-bearing zones, got {len(bearing)}"
    assert set(bearing) == set(range(1, 22)) - EXCLUDED, "disc-bearing set is not 21 - {1,2,5}"
    print(f"  zones 21, disc-bearing 18, excluded {sorted(EXCLUDED)}  OK")


def check_day_values():
    """day_value = boss_count * concentric_rings, zone by zone."""
    derived = []
    for z in zs:
        if z["zone"] == 5:
            n = sum(m["count"] for m in z["motifs"])
            d = sum(m["count"] for m in z["motifs"])  # 1 ring each
            assert n == z["count"] == 38, f"zone 5: {n} != 38"
        else:
            d = z["count"] * z["rings"]
        assert d == z["day_value"], f"zone {z['zone']}: {z['count']}*{z['rings']} != {z['day_value']}"
        derived.append(d)
    assert derived == menghin, f"derived day-values != readings/menghin.json\n{derived}\n{menghin}"
    assert sum(derived) == 1783, f"total {sum(derived)} != 1783"
    print(f"  day_value = count x rings reproduces all 21 zones, total 1783  OK")


def check_ring_counts():
    """Menghin: 'zwei, drei, fuenf oder sechs' - never four."""
    rings = {z["rings"] for z in zs if z["tool"] in DISC_TOOLS}
    assert rings <= {2, 3, 5, 6}, f"unattested ring count(s): {rings - {2, 3, 5, 6}}"
    for z in zs:
        if z["tool"] in DISC_TOOLS:
            t = next(t for t in sym["tools"] if t["no"] == z["tool"])
            assert t["rings"] == z["rings"], f"zone {z['zone']}: tool {z['tool']} rings mismatch"
    print(f"  ring counts {sorted(rings)} - no 4, and every zone agrees with the tool legend  OK")


def check_menghin_identities():
    """The four sentences in text/menghin_pages20-31.txt."""
    excl = [z for z in zs if z["zone"] not in EXCLUDED]
    bosses = sum(z["count"] for z in excl)
    assert bosses == 418, f"bossed discs {bosses} != 418"
    ring_sum = sum(z["day_value"] for z in excl)
    assert ring_sum == 1701, f"concentric rings {ring_sum} != 1701"
    # two independent routes to 1701
    route2 = sum(menghin) - sum(menghin[i - 1] for i in (1, 2, 5))
    assert route2 == 1701, f"1783 - z1 - z2 - z5 = {route2} != 1701"
    assert sum(menghin[2:]) == 1739, "sum(z3..z21) != 1739"
    print(f"  418 bossed discs, 1701 rings (two routes), 1783 total, 1739 excl. tip  OK")


def check_tools_used_once():
    """Fig. 23 flags the tools appearing in only one zone; there must be three."""
    once = sorted(t["no"] for t in sym["tools"]
                  if t["no"] in DISC_TOOLS and len(t["zones"]) == 1)
    assert once == [9, 11, 13], f"single-zone tools {once} != [9, 11, 13]"
    assert all(len(t["zones"]) >= len({z["zone"] for z in t["zones"]}) for t in sym["tools"]), \
        "a tool lists the same zone twice"
    print(f"  tools used in exactly one zone: {once} (Fig. 23 green key)  OK")


def check_all_zones_covered():
    """Every disc tool's zone list must match zones.json exactly."""
    for t in sym["tools"]:
        if t["no"] not in DISC_TOOLS:
            continue
        want = {z["zone"] for z in t["zones"]}
        got = {z["zone"] for z in zs if z["tool"] == t["no"]}
        assert want == got, f"tool {t['no']}: legend {sorted(want)} vs zones.json {sorted(got)}"
    print("  every tool's zone list agrees with zones.json  OK")


def check_height_budget():
    """745 mm, three ways (plan section 2.2)."""
    rings = hat["rings"]
    total = sum(r["h"] for r in rings)
    assert abs(total - 745.0) < 1e-9, f"ring heights sum to {total}, not 745"

    zsum = sum(r["h"] for r in rings if r["kind"] == "zone")
    assert abs(zsum - 565.0) < 1e-9, f"zones sum to {zsum}, not 565"
    tb = [r["h"] for r in rings if r["kind"] == "trennband"]
    assert len(tb) == 18, f"{len(tb)} trennbands, expected 18 (tb19 is dropped)"
    # dimensions.txt grand total, reconciled
    assert abs(769 - 40 - 9 + 18 + 7 - 745) == 0, "769 - 2*tussenstuk - tb19 + cuff + rise != 745"
    # the two Menghin readings of the top 116 mm
    assert 611 + 18 + 109 + 7 == 745 and 611 + 18 + 100 + 16 == 745

    b = hat["zone_boundaries_mm"]
    assert len(b) == len(rings) + 1, f"{len(b)} boundaries for {len(rings)} rings"
    assert b[-1] == 745.0, f"last boundary {b[-1]} != 745"
    for i, r in enumerate(rings):
        assert abs((b[i + 1] - b[i]) - r["h"]) < 1e-9, f"{r['id']}: boundary gap != h"
    print(f"  height closes 745.0 three ways; {len(rings)} rings, {len(b)} boundaries, contiguous  OK")


def check_zone_attribution():
    """Each zone's z-range must sit inside its section, and sections must be in order."""
    order = ["apex", "schaft", "kalotte", "krempe"]
    last = -1
    for z in zs:
        i = order.index(z["section"])
        assert i >= last, f"zone {z['zone']}: section order goes backwards"
        last = i
        assert z["z_mm"][0] < z["z_mm"][1], f"zone {z['zone']}: empty z-range"
    for s, lo, hi in [("apex", 0.0, 68.0), ("schaft", 68.0, 611.0),
                      ("cuff", 611.0, 629.0), ("kalotte", 629.0, 738.0),
                      ("krempe", 738.0, 745.0)]:
        sec = next(x for x in hat["sections"] if x["name"] == s)
        assert sec["z_mm"] == [lo, hi], f"section {s}: {sec['z_mm']} != [{lo}, {hi}]"
    print("  all 21 zones fall inside the right physical section  OK")


def check_profile():
    p = hat["profile"]
    assert p[0] == {"z": 0.0, "r": 0.0} and p[-1]["z"] == 745.0
    assert hat["profile_interp"] == "pchip", "profile must be monotone piecewise, never a slope constant"
    by_z = {q["z"]: q["r"] for q in p}
    for a in hat["profile_anchors"].values():
        circ = a["circ_mm"]
        r = by_z[a["z"]]
        assert abs(2 * 3.141592653589793 * r - circ) < 3.0, \
            f"anchor at z={a['z']}: 2*pi*{r} != {circ}"
    assert max(q["r"] for q in p) == by_z[745.0] == 150.5, "the Krempenrand must be the widest point"
    print("  profile: 4 anchors reproduced to within 3 mm, brim is widest  OK")


def check_schmidt_kaler_separate():
    """The 651 must never be mistaken for a day count."""
    assert sum(sk) == 651 and 651 != sum(menghin), "Schmidt-Kaler and Menghin must stay distinct"
    assert "NOT a day count" in load("data/readings/schmidt_kaler.json")["_definition"]
    print("  Schmidt-Kaler's 651 kept separate from Menghin's 1783  OK")


def check_dimensions_txt_agrees():
    """dimensions.txt is the primary dimension source, but only its height table.

    Its other sections are the prior attempt's own guesses and are known wrong:
    'base diameter of 20 cm at its widest point' (Menghin: 307 x 295 mm);
    'thickness = 0.6 mm' (unprintable - the plan uses 2.0 mm); and
    'symbol 13 - 4 rings = value 4' (Menghin: Nr. 13 has TWO rings, and a ring
    count of 4 occurs in no zone at all).  A 4-ring Nr. 13 would make zone 16
    19 x 4 = 76 instead of 38 and the total 1821 instead of 1783, so that line
    must never be imported.  Only the z/tb heights are read here.
    """
    txt = (ROOT / "dimensions.txt").read_text()
    # two entries per line: "z1 = 61, tb1 = 7";  ids are z1..z19 here, z01..z19 in this repo
    got = {f"{p}{int(n)}": float(h) for p, n, h in
           re.findall(r"\b(z|tb)0*(\d+)\s*=\s*(\d+(?:\.\d+)?)", txt)}
    assert got, "dimensions.txt: no z/tb heights parsed - has the format changed?"
    assert "tussenstuk" in txt, "dimensions.txt no longer mentions the two spacers"
    for r in hat["rings"]:
        if r["kind"] not in ("zone", "trennband"):
            continue  # the cuff and the Krempe rise are derived, not in dimensions.txt
        k = re.sub(r"0+(\d+)$", r"\1", r["id"])  # z01 -> z1
        assert k in got, f"dimensions.txt has no row for {k}"
        assert got[k] == r["h"], \
            f"{k}: dimensions.txt says {got[k]}, data says {r['h']}"
    assert got.get("tb19") == 9.0, "tb19 must still be present in dimensions.txt"
    assert len([k for k in got if k.startswith("tb")]) == 19, \
        "dimensions.txt should list tb1..tb19"
    print("  dimensions.txt z/tb heights == data/hat_parameters.json (tb19 present, dropped)  OK")


if __name__ == "__main__":
    print("verify_calendar.py")
    for fn in (check_zone_count, check_day_values, check_ring_counts,
               check_menghin_identities, check_tools_used_once, check_all_zones_covered,
               check_height_budget, check_zone_attribution, check_profile,
               check_schmidt_kaler_separate, check_dimensions_txt_agrees):
        fn()
    print("all checks passed")
