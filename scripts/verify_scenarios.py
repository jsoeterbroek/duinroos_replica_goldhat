#!/usr/bin/env python3
"""Check the Stage-2 lighting scenarios against the zone data and each other.

Run:  python3 scripts/verify_scenarios.py

Pure stdlib.  data/scenarios.json is a transcription of Menghin (2010)
pp. 60-63 (Figs 61.1-64.4): for each time block it says which zones light up
(red = solar, blue = lunar, green = intercalary) and what day value the block
carries.  This script checks the parts that are checkable:

  1. every zone referenced is one of 3..21;
  2. every green (excised) zone is one of the three single-use-stamp zones
     {7, 16, 17} -- the ones verify_calendar.py independently identifies;
  3. every stated solar/lunar identity really sums to its value on
     data/zones.json (this is Menghin's own arithmetic, re-run on our data);
  4. |solar - lunar| equals the stated delta;
  5. the sequence of time anchors is monotone (4..19 quarter-years, 12..59
     lunations) and the full-cycle state closes on 1739.

It deliberately does NOT invent arithmetic where the source has none
(61.2) or is self-inconsistent (64.4) -- those are reported, not asserted.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
load = lambda p: json.loads((ROOT / p).read_text())

zones = load("data/zones.json")["zones"]
day = {z["zone"]: z["day_value"] for z in zones}
scen = load("data/scenarios.json")
states = scen["states"]
INTERCALARY = set(scen["_intercalary_zones"])


def expand(ranges):
    for lo, hi in ranges:
        yield from range(lo, hi + 1)


def block_sum(spec):
    """sum(include) - sum(exclude) over zone day-values."""
    inc = sum(day[z] for z in expand(spec["include"]))
    exc = sum(day[z] for z in expand([(z, z) for z in spec["exclude"]]))
    return inc - exc


def check_structure():
    assert len(states) == 16, f"expected 16 states (Figs 61.1-64.4), got {len(states)}"
    seen = set()
    for s in states:
        assert s["id"] not in seen, f"duplicate state {s['id']}"
        seen.add(s["id"])
        assert 3 <= s["quarter_years"] <= 19, f"{s['id']}: bad quarter-years"
        # every referenced zone is real
        refs = list(expand(s["display"]["solar"])) + list(expand(s["display"]["lunar"]))
        refs += s["display"]["intercalary"]
        for spec in (s["solar"], s["lunar"]):
            if spec:
                refs += list(expand(spec["include"])) + spec["exclude"]
        bad = sorted({z for z in refs if z not in day})
        assert not bad, f"{s['id']}: zones outside 3..21: {bad}"
    print(f"  16 states, every referenced zone is 3..21  OK")


def check_intercalary_is_single_use_tools():
    """The green zones must be exactly the zones of the three once-only stamps."""
    for s in states:
        green = set(s["display"]["intercalary"])
        assert green <= INTERCALARY, \
            f"{s['id']}: green {sorted(green)} not within {sorted(INTERCALARY)}"
    # independently: zones whose DISC tool (Nr. 8-15) appears in exactly one zone.
    # Tools 16/17 are the once-only SPECIAL SIGNS of zone 5, not disc stamps --
    # that is why Menghin's running text (p47) can lump zone 5 in with the
    # intercalary zones while the Figs 61-64 colour only 7/16/17 green.
    single = set()
    for t in load("data/symbols.json")["tools"]:
        if t["no"] not in range(8, 16):
            continue
        zs = {z["zone"] for z in t["zones"]}
        if len(zs) == 1:
            single |= zs
    assert single == INTERCALARY, \
        f"single-use-disc zones {sorted(single)} != declared intercalary {sorted(INTERCALARY)}"
    print(f"  green zones are always within {{7,16,17}} = the three single-use disc stamps  OK")


def check_identities():
    """Re-run Menghin's stated zone arithmetic on our day-values."""
    n = 0
    for s in states:
        for side in ("solar", "lunar"):
            spec = s[side]
            if spec is None:
                continue
            got = block_sum(spec)
            assert got == spec["value"], \
                f"{s['id']} {side}: zones give {got}, source states {spec['value']}"
            n += 1
        if s["solar"] and s["lunar"]:
            diff = abs(s["solar"]["value"] - s["lunar"]["value"])
            assert diff == s["delta_days"], \
                f"{s['id']}: |solar-lunar| = {diff}, delta stated {s['delta_days']}"
    print(f"  {n} stated solar/lunar identities reproduce from data/zones.json  OK")


def check_monotone_and_total():
    qy = [s["quarter_years"] for s in states]
    lun = [s["lunations"] for s in states]
    assert qy == sorted(qy) == list(range(4, 20)), f"quarter-years not 4..19: {qy}"
    assert lun == sorted(lun), f"lunations not monotone: {lun}"
    assert sum(day[z] for z in range(3, 22)) == 1739, "zones 3..21 must sum to 1739"
    last = states[-1]
    assert last["id"] == "64.4" and last["solar"]["value"] == last["lunar"]["value"] == 1739
    print("  anchors monotone 4..19 QY / 12..59 L; full cycle closes on 1739  OK")


def report_open():
    """Surface (do not assert) the states the source leaves without a clean sum."""
    for s in states:
        if s["solar"] is None or s["lunar"] is None:
            print(f"  NOTE {s['id']}: no zone arithmetic in source ({s['note']})")
        else:
            green_in = set(s["display"]["intercalary"]) & set(expand(s["lunar"]["include"]))
            if green_in and not (green_in & set(s["lunar"]["exclude"])):
                extra = sorted(green_in)
                print(f"  NOTE {s['id']}: green {extra} lies inside the lunar block "
                      f"but is not subtracted ({s['note']})")


if __name__ == "__main__":
    print("verify_scenarios.py")
    for fn in (check_structure, check_intercalary_is_single_use_tools,
               check_identities, check_monotone_and_total):
        fn()
    print("structural + arithmetic checks passed; source caveats:")
    report_open()
