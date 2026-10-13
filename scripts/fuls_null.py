#!/usr/bin/env python3
"""fuls_null.py — reproduce Fuls (2008) combinatorial null, then run it as the
cross-hat test Menghin's hypothesis needs.

Source: A. Fuls, "Astronomisch-statistische Analyse von Kreissymbolen
bronzezeitlicher Goldhüte", in G. Wolfschmidt (ed.), *Prähistorische Astronomie
und Ethnoastronomie* (Nuncius Hamburgensis 8), Norderstedt 2008, pp. 113-129
(§8.4). Control: `research/controls/C4_fuls_null_result.md`, catalogue:
`research/catalogues/fuls.md`.

Input: the four per-zone ornament tables of Menghin 2000, transcribed in
`data/readings/menghin2000_zones.json` (control C6). Unit: Fuls/Menghin's
"counter" = concentric rings per punched disc x number of discs (`SK`). Zones
with a special symbol but no ring value (Berlin Z5, Ezelsdorf Z15/Z17) are
counted with K=1, i.e. their symbol count `A`; this is what makes the published
Berlin (1764) and Ezelsdorf (1761) circle totals come out right.

The four Fuls methods (§8.4) over N circle-bearing zones:
  A  arbitrary non-empty subsets                    G = 2**N - 1
  B  subsets of groups of zones sharing one stamp   G = 2**G_grp - 1
  C  contiguous blocks                              G = N(N+1)/2
  D  contiguous block minus any subset of the intercalary ("Schalt") zones
     inside it; the resulting *distinct* zone sets are counted, so that each
     sum is counted once  (this is what reproduces Fuls's G: Berlin 699,
     Schifferstadt 69, Avanton 111, Ezelsdorf 33573 with his 12 Schalt zones)

A "Schaltzone" is, per Fuls (§8.4.4, after Menghin 2003 p. 232), a zone whose
symbol type (stamp) occurs only once among the circle zones.

Hit test (§8.2, formula 8.1): a zone sum s is a hit for period p with tolerance
t_p iff there is an integer M >= 1 with |s - M*p| <= t_p. Reported as
  h = T/G * 100  (per cent of combinations that hit)
  w = 2*t_p/p * 100  (per cent expected under a random sum, formula 8.7)

Run:  python3 scripts/fuls_null.py            # report + cross-hat
      python3 scripts/fuls_null.py --check    # only compare with Fuls, exit 1 on unexpected diff
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "readings", "menghin2000_zones.json")

# Fuls 2008, Table 8.1: (name, period in days, tolerance in days)
PERIODS = [
    ("sidereal month", 27.32166, 1.0),
    ("synodic month", 29.530588, 1.0),
    ("solar month", 30.43685, 1.0),
    ("tropical year", 365.2422, 1.0),
    ("Mercury syn.", 115.88, 1.0),
    ("Venus syn.", 583.9229, 4.0),
    ("Mars syn.", 779.94, 20.0),
    ("Jupiter syn.", 398.88, 4.0),
    ("Saturn syn.", 378.09, 1.5),
]

# Fuls 2008 Tables 8.2-8.5, hit counts T, in PERIODS order.
FULS_PUBLISHED = {
    ("berlin", "A"): [76753, 70904, 68769, 5728, 18002, 13507, 65995, 20988, 8446],
    ("berlin", "B"): [87, 64, 64, 5, 16, 11, 43, 20, 5],
    ("berlin", "C"): [20, 12, 10, 0, 2, 4, 7, 2, 0],
    ("berlin", "D"): [58, 46, 34, 3, 13, 15, 27, 12, 1],
    ("schifferstadt", "A"): [71, 61, 81, 2, 27, 0, 0, 23, 5],
    ("schifferstadt", "B"): [2, 5, 2, 0, 0, 0, 0, 0, 0],
    ("schifferstadt", "C"): [3, 3, 6, 0, 1, 0, 0, 1, 0],
    ("schifferstadt", "D"): [3, 4, 7, 0, 1, 0, 0, 1, 1],
    ("avanton", "A"): [604, 553, 532, 31, 201, 1, 0, 124, 94],
    ("avanton", "B"): [3, 2, 0, 0, 0, 1, 0, 1, 0],
    ("avanton", "C"): [8, 6, 4, 0, 1, 1, 0, 3, 0],
    ("avanton", "D"): [8, 7, 6, 0, 2, 1, 0, 3, 0],
    ("ezelsdorf", "A"): [76823, 71007, 68889, 5751, 17940, 13504, 65582, 21065, 8321],
    ("ezelsdorf", "B"): [4808, 4459, 4347, 366, 1121, 869, 3404, 1298, 517],
    ("ezelsdorf", "C"): [20, 13, 10, 1, 3, 1, 7, 3, 1],
    # Ezelsdorf D depends on Fuls's Schaltzone set (12), which differs from ours
    # (the unique-stamp rule on Menghin 2000 gives 6), so G and T cannot be
    # compared.  Kept for reference only.
    ("ezelsdorf", "D"): [2462, 2286, 2222, 185, 553, 416, 1508, 629, 259],
}
# Fuls's published G (Tables 8.2-8.5)
FULS_G = {
    ("berlin", "A"): 1048575, ("berlin", "B"): 1023, ("berlin", "C"): 210, ("berlin", "D"): 699,
    ("schifferstadt", "A"): 1023, ("schifferstadt", "B"): 31, ("schifferstadt", "C"): 55, ("schifferstadt", "D"): 69,
    ("avanton", "A"): 8191, ("avanton", "B"): 31, ("avanton", "C"): 91, ("avanton", "D"): 111,
    ("ezelsdorf", "A"): 1048575, ("ezelsdorf", "B"): 65535, ("ezelsdorf", "C"): 210, ("ezelsdorf", "D"): 33573,
}

# Cells where a difference from Fuls's table is *explained* and expected.
KNOWN_DIFFS = {
    ("berlin", "A"): "Mars T is 65994 here vs 65995 in Fuls: the single zone-5 sum "
                       "(19 d) lies inside Mars's 20 d tolerance of *zero* periods. "
                       "Formula 8.1 requires M >= 1, so it is not a hit; Fuls's table "
                       "appears to have counted it (M = 0). The other 8 periods match.",
    ("berlin", "B"): "as method A: the zone-5 group value 19 counts against M = 0 in "
                       "Fuls's Mars cell (42 here vs 43 there).",
    ("ezelsdorf", "B"): "our transcription of Menghin 2000 Abb. 27 yields 12 stamp "
                          "groups; Fuls's figure has 16, so G (and T) differ. The "
                          "cross-hat result below uses our 12-group reading.",
    ("ezelsdorf", "D"): "our unique-stamp 'Schalt' set (6 zones) differs from Fuls's "
                          "(12), so G = 1237 here vs 33573 there. Cross-hat uses our rule.",
}


def load_hats(path=DATA):
    """Return {hat: [zone dicts in order]} for zones carrying a symbol count."""
    raw = json.load(open(path))
    hats = {}
    for key, hat in raw["hats"].items():
        zones = []
        for z in hat["zones"]:
            if not z.get("A"):
                continue  # star / undecorated apex: no counter
            sk = z.get("SK")
            if sk is None:  # special symbol: K = 1
                sk = z["A"]
            zones.append({
                "zone": z["zone"],
                "value": sk,
                "tool": z.get("tool_2000"),
                "special": z.get("special"),
                "reconstructed": z.get("reconstructed", False),
                "schalt": bool(z.get("schaltzone")),
            })
        hats[key] = zones
    return hats


def is_hit(s, p, t):
    if s <= 0:
        return False
    M = round(s / p)
    return M >= 1 and abs(s - M * p) <= t


def sums_with_counts(values):
    """{subset sum: number of subsets achieving it} including the empty set."""
    dp = Counter({0: 1})
    for v in values:
        nxt = Counter(dp)
        for s, c in dp.items():
            nxt[s + v] += c
        dp = nxt
    return dp


def hit_count(sums_counts, skip_empty=True):
    """T for each period, given {sum: count}."""
    out = []
    for _, p, t in PERIODS:
        T = 0
        for s, c in sums_counts.items():
            if skip_empty and s == 0:
                continue
            if is_hit(s, p, t):
                T += c
        out.append(T)
    return out


def schalt_positions(zones):
    """Fuls's rule: a zone whose stamp occurs only once is a Schaltzone."""
    freq = Counter(z["tool"] for z in zones)
    return {i for i, z in enumerate(zones) if freq[z["tool"]] == 1}


def method_A(zones):
    values = [z["value"] for z in zones]
    sc = sums_with_counts(values)
    G = 2 ** len(values) - 1
    return hit_count(sc), G


def method_B(zones):
    groups = defaultdict(list)
    for z in zones:
        groups[z["tool"]].append(z["value"])
    values = [sum(v) for v in groups.values()]
    sc = sums_with_counts(values)
    G = 2 ** len(values) - 1
    return hit_count(sc), G


def method_C(zones):
    values = [z["value"] for z in zones]
    sums = [sum(values[i:j + 1]) for i in range(len(values)) for j in range(i, len(values))]
    T = [sum(1 for s in sums if is_hit(s, p, t)) for _, p, t in PERIODS]
    return T, len(sums)


def method_D(zones):
    values = [z["value"] for z in zones]
    schalt = schalt_positions(zones)
    seen = set()
    for i in range(len(values)):
        for j in range(i, len(values)):
            inside = [x for x in range(i + 1, j) if x in schalt]  # strictly between
            for r in range(len(inside) + 1):
                from itertools import combinations
                for sub in combinations(inside, r):
                    rem = set(sub)
                    fs = frozenset(x for x in range(i, j + 1) if x not in rem)
                    if fs:
                        seen.add(fs)
    sums = [sum(values[x] for x in fs) for fs in seen]
    T = [sum(1 for s in sums if is_hit(s, p, t)) for _, p, t in PERIODS]
    return T, len(seen)


METHODS = {"A": method_A, "B": method_B, "C": method_C, "D": method_D}


def compute(hats):
    results = {}
    for hat, zones in hats.items():
        for name, fn in METHODS.items():
            results[(hat, name)] = (fn(zones), zones)
    return results


def check(results):
    """Compare our T/G with Fuls's published values.  Return the number of
    *unexplained* differences (0 = the control reproduces); KNOWN_DIFFS are
    reported with their explanation and do not count."""
    bad = 0
    print("Comparison with Fuls 2008 (Tables 8.2-8.5)")
    print("  [ok]      T and G both reproduce;  [edge]  a documented, explained difference\n")
    for (hat, m) in sorted(FULS_PUBLISHED):
        (T, G), _ = results[(hat, m)]
        pubT = FULS_PUBLISHED[(hat, m)]
        pubG = FULS_G[(hat, m)]
        tdiff = sum(1 for a, b in zip(T, pubT) if a != b)
        gok = "G=" + str(G) + ("==" if G == pubG else "!=") + str(pubG)
        if tdiff == 0 and G == pubG:
            tag = "ok"
        elif (hat, m) in KNOWN_DIFFS:
            tag = "edge"
        else:
            tag = "DIFF"
            bad += 1
        print(f"  [{tag:4s}] {hat:14s} method {m}: {gok:18s} T-diffs={tdiff}")
        if tag == "edge":
            print(f"           -> {KNOWN_DIFFS[(hat, m)]}")
    return bad


def report_crosshat(results, hats):
    print("\nCross-hat: does the Berlin reading transfer?  h vs w (chance)\n")
    print(f"  {'hat':14s} {'m':1s} {'G':>8s} " + " ".join(f"{p.split()[0][:5]:>7s}" for p, _, _ in PERIODS))
    print(f"  {'':14s} {'':1s} {'':>8s} " + " ".join(f"{'w':>7s}" for _ in PERIODS))
    for hat in ["berlin", "schifferstadt", "avanton", "ezelsdorf"]:
        zones = hats[hat]
        recon = sorted(z["zone"] for z in zones if z["reconstructed"])
        for m in "ABCD":
            (T, G), _ = results[(hat, m)]
            cells = " ".join(f"{t/G*100:6.2f}%" if t else "   -   " for t in T)
            print(f"  {hat:14s} {m} {G:8d} {cells}")
        if recon:
            print(f"  {'':14s}   (reconstructed zones held in the data: {recon})")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="compare with Fuls and exit 1 on unexpected diff")
    args = ap.parse_args()

    hats = load_hats()
    results = compute(hats)
    bad = check(results)
    if args.check:
        return 1 if bad else 0
    report_crosshat(results, hats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
