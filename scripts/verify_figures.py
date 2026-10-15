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
        p = os.path.join(outdir, "development_%s.png" % s["id"].replace(".", "_"))
        if not os.path.exists(p):
            missing.append(os.path.basename(p))
    for g in ("61", "62", "63", "64"):
        p = os.path.join(outdir, "sheet_%s.png" % g)
        if not os.path.exists(p):
            missing.append(os.path.basename(p))
    root = os.path.dirname(outdir)
    for rel in (os.path.join("compare", "hypotheses.png"),
                os.path.join("caution", "null_model.png")):
        if not os.path.exists(os.path.join(root, rel)):
            missing.append(rel)
    assert not missing, "figure set incomplete: %s" % ", ".join(missing)
    print("  figure set complete: %d panels + %d developments + 4 sheets + "
          "comparison + caution  OK" % (len(states), len(states)))


def check_hypotheses(zones):
    """The registry is well-formed and its derivable rules reproduce the sources."""
    hy = FG.load_hypotheses()
    hyps = hy["hypotheses"]
    ids = [h["id"] for h in hyps]
    assert len(ids) == len(set(ids)), "duplicate hypothesis id"
    assert "menghin_lunisolar" in ids, "Menghin must stay in the registry"
    by = {h["id"]: h for h in hyps}
    for h in hyps:
        for key in ("title", "source", "unit", "confidence", "caveat"):
            assert h.get(key), "hypothesis %s missing %s" % (h["id"], key)
        if h.get("zone_groups"):
            assert FG.zone_set(h["zone_groups"], zones), \
                "%s zone_groups resolves to nothing" % h["id"]
    lorenz = FG.zone_set(by["lorenz_metonic"]["zone_groups"], zones)
    assert len(lorenz) == 7, "Lorenz five-ring friezes should be 7"
    fuls = FG.zone_set(by["fuls_correction"]["zone_groups"], zones)
    assert fuls == {7, 16, 17}, "Fuls Schaltzonen should be {7,16,17}"
    print("  hypothesis registry valid: %d hypotheses, Lorenz 7, Fuls %s  OK"
          % (len(ids), sorted(fuls)))


def check_caution_data():
    """The caution panel's numbers are real and show only Schifferstadt selective."""
    p = os.path.join(HERE, "data", "readings", "fuls_null.json")
    d = json.load(open(p))
    assert d["chance_pct"] > 0
    sel = [h["hat"] for h in d["hats"] if h["selective"]]
    assert sel == ["Schifferstadt"], \
        "the null result says only Schifferstadt is selective, got %s" % sel
    print("  caution data: only %s above the %.2f %% chance line  OK"
          % (sel[0], d["chance_pct"]))


def check_development_bands():
    """Ring motifs must reach the renderer as BANDS, not flattened discs."""
    import motifs as M
    hp, zj = FG.load()
    z8 = next(z for z in zj["zones"] if z["zone"] == 8)   # tool 10, 5 rings
    circ, h, motifs = M.placed_zone_motifs(z8, hp["profile"], hp)
    assert motifs, "zone 8 placed no motifs"
    _, _, _, holes = motifs[0]
    assert holes, "zone 8 motif has no holes"
    assert all(isinstance(band[0][0], (list, tuple)) for band in holes), \
        "ring bands were flattened -- the renderer would fill them as solid discs"
    print("  ring bands preserved for the renderer (%d trough bands)  OK" % len(holes))


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
    check_development_bands()
    check_hypotheses(zones)
    check_caution_data()
    check_rendered(states)
    print("\nverify_figures: all checks passed")


if __name__ == "__main__":
    main()
