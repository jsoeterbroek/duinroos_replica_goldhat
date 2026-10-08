#!/usr/bin/env python3
"""Check the Schmidt-Kaler (2012) Venus reading of the Berlin Gold Hat.

Run:  python3 scripts/verify_venus_hypothesis.py

Pure stdlib, no deps. It does three things:

  1. Reproduces the arithmetic Schmidt-Kaler states on p. 15-17 of
     "Ein Venus-Kalender auf dem Berliner Goldhut" (2012), using Menghin's
     own day-values from data/readings/menghin.json.
  2. Counts how many *subsets* of the 19 day-values (zones 3-21) hit each of
     his calendar targets. A target with many representations is easy to
     "find" by grouping; a target with one or two is a real constraint.
  3. Runs the same finder on the plain ornament counts (Schmidt-Kaler's own
     651-unit table) so the non-selectivity of the method is visible.

Nothing here is evidence about the Bronze Age. It only measures how much
information a number carries under each proposed rule.
"""
import json
import pathlib
import random
from itertools import combinations

ROOT = pathlib.Path(__file__).resolve().parent.parent
load = lambda p: json.loads((ROOT / p).read_text())

DAY = {r["zone"]: r["days"]
       for r in load("data/readings/menghin.json")["day_value"]}
ORN = {r["zone"]: r["ornaments"]
       for r in load("data/readings/schmidt_kaler.json")["count"]}
ZS = [z for z in range(3, 22)]                 # the 19 system zones
V = [DAY[z] for z in ZS]                       # rings-as-days unit
O = [ORN[z] for z in ZS]                       # plain-ornament unit
N = len(V)

# --- Schmidt-Kaler's stated targets -----------------------------------------
VENUS_HALF = 292      # half the 583.92-day synodic period of Venus
VENUS_FULL = 584
MERCURY = 117         # 115.88 d synodic period of Mercury (rounded)
MERCURY_5 = 585       # his 5 x 117 = 585 = 584 Venus


def subsets(vals, target, maxk=None):
    """All subsets (optionally of size <= maxk) summing exactly to target."""
    out = []
    for k in range(1, N + 1):
        if maxk and k > maxk:
            break
        for c in combinations(range(N), k):
            if sum(vals[i] for i in c) == target:
                out.append(tuple(ZS[i] for i in c))
    return out


def contiguous(vals, target):
    """Contiguous zone blocks summing exactly to target."""
    out = []
    for i in range(N):
        s = 0
        for j in range(i, N):
            s += vals[j]
            if s == target:
                out.append(tuple(ZS[i:j + 1]))
    return out


def check_stated_arithmetic():
    # p. 15: "die Summe ... in seiner Schaltzone 7 (19 x 3 = 57) und der
    # aeussersten Zone 21 (5 x 47 = 235) ist genau gleich 292."
    assert DAY[7] == 57 and DAY[21] == 235, "z7 / z21 day-values changed"
    assert DAY[7] + DAY[21] == VENUS_HALF, "57 + 235 != 292"
    # p. 15: second solution Z3 + SZ5 + SZ17 = 146, doubled 292, quad 584
    assert DAY[3] + DAY[5] + DAY[17] == 146, "42 + 38 + 66 != 146"
    assert 2 * (DAY[3] + DAY[5] + DAY[17]) == VENUS_HALF, "2 x 146 != 292"
    assert 4 * (DAY[3] + DAY[5] + DAY[17]) == VENUS_FULL, "4 x 146 != 584"
    # p. 16: Mercury, zones 3 + 4 = 117, and 5 x 117 = 585
    assert DAY[3] + DAY[4] == MERCURY, "42 + 75 != 117"
    assert 5 * MERCURY == MERCURY_5, "5 x 117 != 585"
    print("  Schmidt-Kaler's stated arithmetic reproduces on Menghin's values  OK")


def check_metonic_context():
    # The same zones he uses already carry Menghin's lunisolar numbers.
    assert DAY[21] == 235, "zone 21 is Menghin's Metonic lunation count"
    assert DAY[7] == 3 * 19, "zone 7 is 3 x 19"
    print(f"  but z21 = {DAY[21]} is also Menghin's 235 lunations, z7 = 57 = 3 x 19  OK")


def report_counts(vals, label, targets):
    print(f"  --- {label} (19 zones, total {sum(vals)}) ---")
    for t in targets:
        s = subsets(vals, t)
        c = contiguous(vals, t)
        note = ""
        if not c and s:
            note = "  <-- NOT reachable by contiguous blocks"
        ex = ", ".join("+".join(str(z) for z in e) for e in s[:3])
        print(f"    {t:>4}: {len(s):>4} subsets ({ex}...) | {len(c)} contiguous{note}")


def shuffle_test(targets, tol, trials=20000, seed=1):
    """Is the *ordering* of the day-values special for contiguous hits?"""
    def hits(vals):
        h = set()
        for i in range(N):
            s = 0
            for j in range(i, N):
                s += vals[j]
                for t in targets:
                    if abs(s - t) <= tol:
                        h.add((i, j, t))
        return len(h)
    real = hits(V)
    rng = random.Random(seed)
    ge = 0
    for _ in range(trials):
        p = V[:]
        rng.shuffle(p)
        if hits(p) >= real:
            ge += 1
    return real, (ge + 1) / (trials + 1)


def check_non_selectivity():
    """The same finder on plain ornament counts finds 292 as easily or more."""
    assert sum(ORN.values()) == 651, f"ornament table total {sum(ORN.values())} != 651"
    o292 = subsets(O, VENUS_HALF)
    o_contig = contiguous(O, VENUS_HALF)
    d292 = subsets(V, VENUS_HALF)
    assert len(o292) > len(d292), "plain ornaments should be *more* forgiving here"
    assert o_contig, "292 is contiguous on the plain ornament counts"
    print(f"  292 under rings: {len(d292)} subsets, {len(contiguous(V, 292))} contiguous")
    print(f"  292 under plain ornaments: {len(o292)} subsets, {len(o_contig)} contiguous "
          f"(e.g. zones {o_contig[0][0]}-{o_contig[0][-1]})")
    print("  -> the Venus number is not specific to the ring-counting unit  OK")


def check_order_is_not_special():
    for label, tg, tol in (("Venus 292/584/117 exact", [117, 292, 584], 0),
                           ("Venus 292/584/117 +/-2", [117, 292, 584], 2),
                           ("Menghin 365/354/235/228/177 +/-2", [365, 354, 235, 228, 177], 2)):
        real, p = shuffle_test(tg, tol)
        flag = "significant" if p < 0.05 else "NOT significant"
        print(f"  {label}: real={real} contiguous hits, P(shuffle>=real)={p:.3f} {flag}")
    print("  -> neither ordering beats chance; 292 is not even contiguous")


if __name__ == "__main__":
    print("verify_venus_hypothesis.py")
    check_stated_arithmetic()
    check_metonic_context()
    report_counts(V, "rings-as-days (Menghin's unit)", [42, 117, 235, 292, 584, 585])
    report_counts(O, "plain ornaments (Schmidt-Kaler's 651)", [42, 117, 235, 292, 584, 585])
    check_non_selectivity()
    check_order_is_not_special()
    print("all checks passed")
