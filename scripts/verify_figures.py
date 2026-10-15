#!/usr/bin/env python3
"""
Verify the Stage 1 figure set: every colour and every caption number in the
figures is re-derived from `data/*.json`, and — when the figures have been
rendered — the set is complete (16 panels + 4 contact sheets).

Pure stdlib, no matplotlib, no FreeCAD. Run:  python3 scripts/verify_figures.py

This is the checks-and-balances partner of scripts/render_scenarios.py: the
renderer is allowed to draw, but it is not allowed to know a number that the
data does not contain. The verifier re-runs the same derivations the kernel
exposes and fails if the two disagree.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import figure_geometry as FG                                          # noqa: E402


def check_states(hp, zones, sc):
    """Every state colours real zones, and every stated day value re-derives."""
    day = {z["zone"]: z["day_value"] for z in zones}
    states = sc["states"]
    assert len(states) == 16, "expected 16 states, got %d" % len(states)

    valid = {z["zone"] for z in zones}
    n_colour = n_value = 0
    for s in states:
        cats = {z["zone"]: FG.classify(s["display"], z["zone"]) for z in zones}
        assert set(cats.values()) <= set(FG.CATEGORY_ORDER), \
            "state %s: unknown colour category" % s["id"]
        assert any(v != "off" for v in cats.values()), \
            "state %s colours no zone" % s["id"]
        assert any(v == "off" for v in cats.values()) or len(cats) == 0, \
            "state %s colours every zone (the source never does)" % s["id"]
        n_colour += 1

        for side in ("solar", "lunar"):
            spec = s.get(side)
            if not spec:
                continue
            got = FG.rederive(s, side, day)
            assert got == spec["value"], \
                "state %s %s: re-derived %s != recorded %s" \
                % (s["id"], side, got, spec["value"])
            assert str(got) in FG.caption(s, day), \
                "state %s %s: caption does not carry the re-derived value" \
                % (s["id"], side)
            n_value += 1
        # every display zone is a real zone
        for cat, ranges in s["display"].items():
            for r in ranges:
                a, b = (r, r) if isinstance(r, int) else (r[0], r[1])
                assert {int(a), int(b)} <= valid, \
                    "state %s: %s references a zone outside 1..21" % (s["id"], cat)
    print("  %d states colour only real zones; %d stated day values re-derived  OK"
          % (n_colour, n_value))
    return states


def check_rendered(states):
    """If figures/ has been generated, the set must be complete."""
    outdir = os.path.join(HERE, "figures", "menghin")
    if not os.path.isdir(outdir):
        print("  figures/ not rendered yet "
              "(run: python3 scripts/render_scenarios.py --all)")
        return
    missing = []
    for s in states:
        p = os.path.join(outdir, s["id"].replace(".", "_") + ".png")
        if not os.path.exists(p):
            missing.append(os.path.basename(p))
    for g in ("61", "62", "63", "64"):
        p = os.path.join(outdir, "sheet_%s.png" % g)
        if not os.path.exists(p):
            missing.append(os.path.basename(p))
    assert not missing, "figure set incomplete: %s" % ", ".join(missing)
    print("  figure set complete: %d panels + 4 contact sheets  OK" % len(states))


def check_kernel_matches_renderer():
    """
    The renderer lives in render_scenarios.py and must import the kernel, not
    re-implement it. A cheap guard: the day values must come from the kernel,
    so the renderer source may not contain a hard-coded day-value table.
    """
    src = open(os.path.join(HERE, "scripts", "render_scenarios.py")).read()
    for needle in ("1783", "1739", "1701", "418", "365", "354"):
        assert needle not in src, \
            "render_scenarios.py hard-codes %r -- values must come from data" % needle
    assert "figure_geometry" in src and "FG.caption" in src, \
        "render_scenarios.py does not use the figure kernel for captions"
    print("  renderer contains no hard-coded day values  OK")


def main():
    hp, zj = FG.load()
    zones = zj["zones"]
    sc = json.load(open(os.path.join(HERE, "data", "scenarios.json")))
    states = check_states(hp, zones, sc)
    check_kernel_matches_renderer()
    check_rendered(states)
    print("\nverify_figures: all checks passed")


if __name__ == "__main__":
    main()
