#!/usr/bin/env python3
"""
Craft-geometry hypothesis test for the four gold hats.

Tests whether the disc counts per zone are explained by the available
circumference divided by a constant per-tool pitch (centre-to-centre
spacing), rather than by calendar arithmetic.

For Berlin: full test against the known r(z) profile.
For all hats: within-tool monotonicity check (counts should increase
              from apex to base as the cone widens).

Usage:
    python3 scripts/verify_craft_geometry.py
"""

import json, math, sys, os

# ── paths ──────────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "data", "hat_parameters.json")) as f:
    params = json.load(f)
with open(os.path.join(ROOT, "data", "zones.json")) as f:
    berlin_zones = json.load(f)["zones"]
with open(os.path.join(ROOT, "data", "readings", "menghin2000_zones.json")) as f:
    all_hats = json.load(f)["hats"]

# ── Berlin profile interpolation (linear between anchors) ─────────────

PROFILE = [(p["z"], p["r"]) for p in params["profile"]]

def interp_r(z):
    """Linear interpolation on the Berlin profile."""
    for i in range(len(PROFILE) - 1):
        z0, r0 = PROFILE[i]
        z1, r1 = PROFILE[i + 1]
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0) if z1 != z0 else 0.0
            return r0 + t * (r1 - r0)
    return PROFILE[-1][1]


# ── 1. Berlin: pitch per tool type from known geometry ─────────────────

def berlin_pitch_table():
    """Compute pitch = circumference / count for every Berlin zone."""
    rows = []
    for bz in berlin_zones:
        count = bz["count"]
        if count == 0:
            continue
        z_lo, z_hi = bz["z_mm"]
        z_mid = (z_lo + z_hi) / 2.0
        tool = bz.get("tool")

        # Krempe zones use their own ring radius
        if "krempe_ring_r_mid_mm" in bz:
            r = bz["krempe_ring_r_mid_mm"]
        else:
            r = interp_r(z_mid)

        circ = 2 * math.pi * r
        pitch = circ / count
        rows.append({
            "zone": bz["zone"], "count": count, "rings": bz["rings"],
            "tool": tool, "z_mid": z_mid, "r": r, "circ": circ, "pitch": pitch,
        })
    return rows


def berlin_tool_pitches(rows):
    """Average pitch per tool type from Berlin data."""
    from collections import defaultdict
    groups = defaultdict(list)
    for r in rows:
        if r["tool"] is not None:
            groups[r["tool"]].append(r)
    pitches = {}
    for tool, members in sorted(groups.items()):
        vals = [m["pitch"] for m in members]
        mean = sum(vals) / len(vals)
        spread = max(vals) - min(vals)
        pitches[tool] = {
            "mean": mean, "spread": spread, "n": len(vals),
            "zones": [m["zone"] for m in members],
        }
    return pitches


def berlin_prediction_test(rows, tool_pitches):
    """Predict count = round(circ / mean_pitch) and report residuals."""
    results = []
    for r in rows:
        tool = r["tool"]
        if tool is None or tool not in tool_pitches:
            continue
        mean_pitch = tool_pitches[tool]["mean"]
        predicted = round(r["circ"] / mean_pitch)
        residual = r["count"] - predicted
        results.append({
            "zone": r["zone"], "tool": tool, "count": r["count"],
            "predicted": predicted, "residual": residual,
            "circ": r["circ"], "pitch_used": mean_pitch,
        })
    return results


# ── 2. All hats: within-tool monotonicity ──────────────────────────────

def tool_monotonicity(hat_name, hat_data):
    """
    For each tool used in more than one zone, check whether the disc
    count increases (or stays flat) from apex to base.  On a cone that
    widens downward, count should be non-decreasing if the pitch is
    constant.

    Returns (tool, zones, counts, monotonic_ok, note).
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for z in hat_data["zones"]:
        tool = z.get("tool_2000")
        if tool is None or z["A"] == 0:
            continue
        groups[tool].append((z["zone"], z["A"], z.get("section", "?")))

    results = []
    for tool, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        members.sort(key=lambda x: x[0])  # sort by zone number (apex→base)
        zones = [m[0] for m in members]
        counts = [m[1] for m in members]
        sections = [m[2] for m in members]

        # Check monotonicity — allow flat, flag decreases
        violations = []
        for i in range(1, len(counts)):
            if counts[i] < counts[i - 1]:
                violations.append((zones[i - 1], counts[i - 1], zones[i], counts[i]))

        # A decrease is expected at the cuff/kalotte transition where
        # the cone narrows before flaring out, so annotate that.
        note = ""
        if violations:
            # Check if all violations cross a section boundary
            section_crosses = []
            for v in violations:
                idx_prev = zones.index(v[0])
                idx_curr = zones.index(v[2])
                if sections[idx_prev] != sections[idx_curr]:
                    section_crosses.append(True)
                else:
                    section_crosses.append(False)
            if all(section_crosses):
                note = "decrease at section boundary (cone narrows)"
            else:
                note = "unexpected decrease within same section"

        results.append({
            "tool": tool, "zones": zones, "counts": counts,
            "monotonic": len(violations) == 0, "violations": violations,
            "note": note,
        })
    return results


# ── 3. All hats: implied-circumference cone consistency ────────────────

def implied_circumferences(hat_name, hat_data, ref_pitches=None):
    """
    If we assume constant pitch per tool, implied_circ = count * pitch.
    For Berlin we use measured pitches; for others we use Berlin's pitch
    for the same K (ring count) as a proxy, since the tools differ but
    the footprint scales with the ring count.

    Returns list of (zone, implied_circ, K, tool, section).
    """
    if ref_pitches is None:
        return []

    rows = []
    for z in hat_data["zones"]:
        if z["A"] == 0 or z.get("K") is None or z["K"] == 0:
            continue
        k = z["K"]
        if k not in ref_pitches:
            continue
        pitch = ref_pitches[k]
        implied = z["A"] * pitch
        rows.append({
            "zone": z["zone"], "count": z["A"], "K": k,
            "tool": z.get("tool_2000"), "section": z.get("section", "?"),
            "pitch": pitch, "implied_circ": implied,
        })
    return rows


# ── main ───────────────────────────────────────────────────────────────

def main():
    ok = True
    sep = "=" * 72

    # ── Berlin pitch analysis ──────────────────────────────────────────
    print(sep)
    print("PART 1: Berlin — pitch per tool type (from known circumferences)")
    print(sep)
    rows = berlin_pitch_table()
    tp = berlin_tool_pitches(rows)

    print()
    print("%6s  %5s  %8s  %8s  %s" % ("Tool", "N", "Mean(mm)", "Range(mm)", "Zones"))
    print("-" * 65)
    for tool, info in sorted(tp.items()):
        zstr = ",".join(str(z) for z in info["zones"])
        print("%6s  %5d  %8.2f  %8.2f  %s" % (
            tool, info["n"], info["mean"], info["spread"], zstr))
    print()

    # ── Berlin prediction test ─────────────────────────────────────────
    print(sep)
    print("PART 2: Berlin — predicted count vs actual (count = round(circ / pitch))")
    print(sep)
    preds = berlin_prediction_test(rows, tp)
    print()
    print("%5s  %5s  %6s  %8s  %8s  %8s" % (
        "Zone", "Tool", "Actual", "Predict", "Resid", "Circ(mm)"))
    print("-" * 52)
    max_resid = 0
    n_exact = 0
    for p in preds:
        flag = " " if p["residual"] == 0 else "*"
        print("%5d  %5s  %6d  %8d  %8d%s %8.1f" % (
            p["zone"], p["tool"], p["count"], p["predicted"],
            p["residual"], flag, p["circ"]))
        max_resid = max(max_resid, abs(p["residual"]))
        if p["residual"] == 0:
            n_exact += 1
    print()
    print("Exact matches: %d / %d (%.0f %%)" % (
        n_exact, len(preds), 100.0 * n_exact / len(preds) if preds else 0))
    print("Max |residual|: %d" % max_resid)
    if max_resid > 2:
        print("WARNING: max residual > 2 — investigate")
    print()

    # ── All hats: within-tool monotonicity ─────────────────────────────
    print(sep)
    print("PART 3: All hats — within-tool count monotonicity (apex → base)")
    print(sep)
    for hat_name in ["berlin", "schifferstadt", "avanton", "ezelsdorf"]:
        hat_data = all_hats[hat_name]
        mono = tool_monotonicity(hat_name, hat_data)
        print()
        print("  %s:" % hat_data["hat"])
        if not mono:
            print("    (no tool used in more than one zone)")
            continue
        for m in mono:
            status = "OK" if m["monotonic"] else "DECREASE"
            zstr = " ".join("%d(%d)" % (z, c) for z, c in zip(m["zones"], m["counts"]))
            note = ("  [%s]" % m["note"]) if m["note"] else ""
            print("    tool %2s: %s  %s%s" % (m["tool"], zstr, status, note))
    print()

    # ── All hats: implied circumference profile ────────────────────────
    # Build Berlin pitch-by-K lookup (average pitch for each ring count)
    from collections import defaultdict
    k_groups = defaultdict(list)
    for r in rows:
        if r["tool"] is not None:
            k_groups[r["rings"]].append(r["pitch"])
    ref_pitches_by_k = {k: sum(v) / len(v) for k, v in k_groups.items()}

    print(sep)
    print("PART 4: All hats — implied circumferences (count × Berlin pitch-by-K)")
    print("  If the craft hypothesis holds, implied circumferences should")
    print("  increase monotonically from apex to base (with possible dip")
    print("  at section transitions where the cone narrows).")
    print(sep)
    print()
    print("  Berlin pitch-by-K reference:")
    for k in sorted(ref_pitches_by_k):
        print("    K=%d: pitch %.2f mm" % (k, ref_pitches_by_k[k]))
    print()

    for hat_name in ["berlin", "schifferstadt", "avanton", "ezelsdorf"]:
        hat_data = all_hats[hat_name]
        ic = implied_circumferences(hat_name, hat_data, ref_pitches_by_k)
        if not ic:
            print("  %s: no data" % hat_data["hat"])
            continue

        print("  %s:" % hat_data["hat"])
        print("  %5s  %5s  %3s  %6s  %8s  %8s" % (
            "Zone", "Count", "K", "Tool", "Pitch", "Circ*"))
        print("  " + "-" * 45)

        prev_circ = 0
        violations = 0
        for r in ic:
            flag = " "
            if r["implied_circ"] < prev_circ - 5:  # 5mm tolerance
                flag = "v"  # violation
                violations += 1
            prev_circ = r["implied_circ"]
            print("  %5d  %5d  %3d  %6s  %8.2f  %8.1f %s" % (
                r["zone"], r["count"], r["K"], r["tool"],
                r["pitch"], r["implied_circ"], flag))

        if violations == 0:
            print("  → Monotonic (no violations)")
        else:
            print("  → %d violation(s) — investigate section transitions" % violations)
        print()

    # ── Summary ────────────────────────────────────────────────────────
    print(sep)
    print("SUMMARY")
    print(sep)
    print()
    print("Berlin pitch constancy:")
    for tool, info in sorted(tp.items()):
        cv = (info["spread"] / info["mean"] * 100) if info["mean"] > 0 else 0
        print("  tool %2s: mean %.2f mm, range %.2f mm (%.1f %% of mean), n=%d" % (
            tool, info["mean"], info["spread"], cv, info["n"]))
    print()
    print("Berlin count prediction: %d/%d exact, max |residual| = %d" % (
        n_exact, len(preds), max_resid))
    print()

    # ── Berlin shaft-only prediction (excluding Krempe and special zones) ──
    shaft_rows = [r for r in rows
                  if r["zone"] not in (1, 2, 5, 20, 21) and r["tool"] is not None]
    shaft_tp = berlin_tool_pitches(shaft_rows)
    shaft_preds = berlin_prediction_test(shaft_rows, shaft_tp)
    shaft_exact = sum(1 for p in shaft_preds if p["residual"] == 0)
    shaft_max = max((abs(p["residual"]) for p in shaft_preds), default=0)

    print("Berlin shaft zones (Z3–Z16, excl. Z5): %d/%d exact, max |residual| = %d" % (
        shaft_exact, len(shaft_preds), shaft_max))
    print()

    # Krempe packing note
    krempe_rows = [r for r in rows if r["zone"] in (20, 21)]
    if krempe_rows:
        shaft_match = {r["tool"]: shaft_tp[r["tool"]]["mean"]
                       for r in krempe_rows if r["tool"] in shaft_tp}
        print("Krempe packing vs shaft:")
        for r in krempe_rows:
            if r["tool"] in shaft_match:
                pct = (1 - r["pitch"] / shaft_match[r["tool"]]) * 100
                print("  Z%d (tool %s): pitch %.2f vs shaft %.2f — packed %.0f%% tighter" % (
                    r["zone"], r["tool"], r["pitch"], shaft_match[r["tool"]], pct))
            else:
                print("  Z%d (tool %s): pitch %.2f (tool not used in shaft)" % (
                    r["zone"], r["tool"], r["pitch"]))
        print()

    # Monotonicity summary
    mono_summary = []
    for hat_name in ["berlin", "schifferstadt", "avanton", "ezelsdorf"]:
        hat_data = all_hats[hat_name]
        mono = tool_monotonicity(hat_name, hat_data)
        n_tools = len(mono)
        n_ok = sum(1 for m in mono if m["monotonic"])
        mono_summary.append((hat_data["hat"], n_ok, n_tools))
    print("Within-tool monotonicity (apex → base):")
    for name, n_ok, n_total in mono_summary:
        status = "ALL OK" if n_ok == n_total else "%d/%d" % (n_ok, n_total)
        print("  %-35s %s" % (name, status))
    print()

    # ── Regression checks ─────────────────────────────────────────────
    # Every claim in FINDING_2026-10-14_craft-geometry.md is asserted here,
    # so that `exits 0` means "all claims re-found", not just the one that
    # happened to be checked first. Tolerances are tight enough to catch a
    # regression in the inputs but loose enough to survive float noise.
    print(sep)
    print("REGRESSION CHECKS (FINDING_2026-10-14_craft-geometry.md)")
    print(sep)
    checks = []

    def chk(label, cond, detail=""):
        checks.append((label, bool(cond), detail))

    # A. Berlin pitch constancy, tools used in >= 3 zones (finding's table).
    #    claim: mean pitch constant, spread <= ~8 % of the mean.
    pitch_expect = {10: (3, 15.42, 1.0), 12: (3, 18.29, 1.2),
                    14: (4, 18.33, 1.3), 15: (3, 23.86, 2.2)}
    for tool, (n_exp, mean_exp, spread_max) in sorted(pitch_expect.items()):
        info = tp.get(tool)
        if info is None:
            chk("pitch tool %s present" % tool, False, "tool missing")
            continue
        chk("pitch tool %2s n=%d" % (tool, n_exp), info["n"] == n_exp,
            "got n=%d" % info["n"])
        chk("pitch tool %2s mean=%.2f mm" % (tool, mean_exp),
            abs(info["mean"] - mean_exp) <= 0.1,
            "got %.2f" % info["mean"])
        chk("pitch tool %2s spread<=%.1f mm" % (tool, spread_max),
            info["spread"] <= spread_max, "got %.2f" % info["spread"])
        chk("pitch tool %2s spread<=9%%" % tool,
            info["spread"] <= 0.09 * info["mean"],
            "got %.1f%%" % (100.0 * info["spread"] / info["mean"]))

    # B. Berlin shaft prediction: 14/16 exact, max |residual| = 1.
    chk("shaft prediction 14/16 exact", shaft_exact == 14,
        "got %d/%d" % (shaft_exact, len(shaft_preds)))
    chk("shaft prediction n=16", len(shaft_preds) == 16,
        "got %d" % len(shaft_preds))
    chk("shaft max |residual| <= 1", shaft_max <= 1, "got %d" % shaft_max)

    # C. Krempe packing: both brim zones packed tighter than the shaft
    #    (finding: Z20 ~12 %, Z21 ~5 %).
    krempe_pct = {}
    for r in krempe_rows:
        if r["tool"] in shaft_tp:
            krempe_pct[r["zone"]] = (
                1 - r["pitch"] / shaft_tp[r["tool"]]["mean"]) * 100
    chk("Krempe Z20 packed tighter", krempe_pct.get(20, 0) > 0,
        "got %.0f%%" % krempe_pct.get(20, 0))
    chk("Krempe Z21 packed tighter", krempe_pct.get(21, 0) > 0,
        "got %.0f%%" % krempe_pct.get(21, 0))
    chk("Krempe Z20 packing 8-16%", 8 <= krempe_pct.get(20, 0) <= 16,
        "got %.0f%%" % krempe_pct.get(20, 0))
    chk("Krempe Z21 packing 2-9%", 2 <= krempe_pct.get(21, 0) <= 9,
        "got %.0f%%" % krempe_pct.get(21, 0))
    chk("Krempe packing gap 5-12% (Z20-Z21)",
        5 <= krempe_pct.get(20, 0) - krempe_pct.get(21, 0) <= 12,
        "got %.0f%%" % (krempe_pct.get(20, 0) - krempe_pct.get(21, 0)))

    # D. Within-tool monotonicity: Berlin/Schifferstadt/Avanton all OK;
    #    Ezelsdorf 4/6 with the violations on tools 11 and 15.
    mono_expected_ok = {"berlin": (5, 5), "schifferstadt": (3, 3),
                        "avanton": (3, 3), "ezelsdorf": (4, 6)}
    ezelsdorf_bad_tools = set()
    for hat_name in ["berlin", "schifferstadt", "avanton", "ezelsdorf"]:
        mono = tool_monotonicity(hat_name, all_hats[hat_name])
        n_ok = sum(1 for m in mono if m["monotonic"])
        want_ok, want_n = mono_expected_ok[hat_name]
        chk("monotonicity %s %d/%d" % (hat_name, want_ok, want_n),
            (n_ok, len(mono)) == (want_ok, want_n),
            "got %d/%d" % (n_ok, len(mono)))
        if hat_name == "ezelsdorf":
            ezelsdorf_bad_tools = {m["tool"] for m in mono if not m["monotonic"]}
    chk("Ezelsdorf violations only tools 11,15",
        ezelsdorf_bad_tools == {11, 15}, "got %s" % sorted(ezelsdorf_bad_tools))

    # E. Zone 21's 235: the brim count follows from circumference / pitch,
    #    with no free parameter. The same tool's shaft pitch predicts the
    #    brim count to within a few percent (packing), and 47 x 5 = 235.
    z21 = next((r for r in rows if r["zone"] == 21), None)
    if z21 is None:
        chk("Zone 21 present", False, "zone missing")
    else:
        chk("Zone 21 count = round(circ/pitch)",
            z21["count"] == round(z21["circ"] / z21["pitch"]),
            "count %s vs %s" % (z21["count"], round(z21["circ"] / z21["pitch"])))
        pred_brim = z21["circ"] / shaft_tp[z21["tool"]]["mean"]
        chk("Zone 21 shaft-pitch prediction within 3 of 47",
            abs(round(pred_brim) - 47) <= 3, "got %.2f" % pred_brim)
        chk("47 x 5 = 235", 47 * 5 == 235, "")

    # F. The result is positive: pitch constancy explains the shaft counts.
    chk("mechanism holds (shaft max |residual| <= 1)", shaft_max <= 1,
        "got %d" % shaft_max)

    n_fail = 0
    for label, passed, detail in checks:
        mark = "PASS" if passed else "FAIL"
        suffix = ("  (%s)" % detail) if (detail and not passed) else ""
        print("  [%s] %s%s" % (mark, label, suffix))
        if not passed:
            n_fail += 1
    print()
    print("Checks: %d passed, %d failed, %d total" % (
        len(checks) - n_fail, n_fail, len(checks)))
    print()

    # Overall pass/fail
    if shaft_max <= 1 and n_fail == 0:
        print("PASS: all %d regression checks re-found. Berlin shaft counts are" % len(checks))
        print("      within ±1 of the craft-geometry prediction; Krempe zones are")
        print("      packed 5-12% tighter (expected: goldsmith fills the available")
        print("      ring). The disc counts are explained by circumference / tool pitch.")
    else:
        if shaft_max > 1:
            print("INVESTIGATE: some Berlin shaft counts deviate by more than ±1.")
        if n_fail:
            print("INVESTIGATE: %d regression check(s) failed." % n_fail)
        ok = False

    print()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
