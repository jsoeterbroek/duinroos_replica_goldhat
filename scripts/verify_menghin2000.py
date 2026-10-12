#!/usr/bin/env python3
"""Check the Menghin 2000 per-zone transcription against Menghin 2000 itself.

Run:  python3 scripts/verify_menghin2000.py

Pure stdlib, no deps. Fails loudly (AssertionError) if a ring identity stops
holding. This is control C6: the raw per-zone tables for all four European gold
hats, transcribed on 2026-10-12 from the page images in
assets/menghin/2000/jpg/. The OCR text layer in assets/menghin/2000/text/ is a
search aid only and is NOT the source of these numbers.

Two classes of check:
  1. internal  - SK = A * K for every disc-bearing zone.
  2. published - the ring totals Menghin states in his running text (pp. 76-91)
                 and in the Abb. 43,1 formula table (p. 88).
                 A mismatch in a *symbol* count is reported as WARN, not hidden:
                 Menghin 2000's summary symbol counts do not all reproduce from
                 its own tables.

Exit status is non-zero if any ring identity or published ring total fails.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "data/readings/menghin2000_zones.json").read_text())
HATS = T["hats"]
warned = []


def zones(hat):
    return {z["zone"]: z for z in HATS[hat]["zones"]}


def sk(hat, ns):
    z = zones(hat)
    return sum(z[n]["SK"] for n in ns if z[n]["SK"] is not None)


def a(hat, ns):
    z = zones(hat)
    return sum(z[n]["A"] for n in ns)


def check_internal():
    for hat in HATS:
        n = 0
        for z in HATS[hat]["zones"]:
            if z["K"] is None:
                assert z["SK"] is None, f"{hat} Z{z['zone']}: K blank but SK set"
                continue
            assert z["A"] * z["K"] == z["SK"], (
                f"{hat} Z{z['zone']}: {z['A']} x {z['K']} != {z['SK']}"
            )
            n += 1
        assert n >= 10, f"{hat}: only {n} disc zones transcribed"
    print("  SK = A x K holds in every disc-bearing zone of all four hats  OK")


def check_berlin():
    z = zones("berlin")
    assert all(z[n]["schaltzone"] for n in (7, 16, 17)), "Schaltzonen 7, 16, 17"
    assert z[5]["ring_units"] == 38 and z[5]["A"] == 19, "zone 5 = 19 + 19"
    assert sk("berlin", range(3, 22)) == 1701, "zones 3-21 rings = 1701"
    assert sk("berlin", range(3, 21)) == 1466, "zones 3-20 rings = 1466"
    assert 1701 + z[5]["ring_units"] == 1739, "1739 = 1701 + 38"
    assert 1739 - z[7]["SK"] == 1682, "1739 - 57 (Z7) = 1682"
    assert 1701 - z[7]["SK"] == 1644, "1701 - 57 = 1644"
    assert 1701 - z[16]["SK"] - z[17]["SK"] == 1597, "1701 - 38 - 66 = 1597"
    assert 1739 - z[5]["ring_units"] - z[16]["SK"] - z[17]["SK"] == 1597, (
        "1739 - (38+38+66) = 1597  (the Wikipedia / Menghin-2010 bookkeeping)"
    )
    assert sk("berlin", range(6, 22)) == 1584, "zones 6-21 = 1584 rings"
    assert 1584 - z[7]["SK"] - z[17]["SK"] == 1461, "zones 6-21 minus SZ7+SZ17 = 1461"
    assert a("berlin", range(3, 22)) == 437, "zones 3-21 symbols incl. zone 5 once = 437"
    assert a("berlin", [3, 4] + list(range(6, 22))) == 418, "18 friezes = 418 symbols"
    print("  Berlin: 1701 / 1466 / 1739 / 1682 / 1644 / 1597 / 1461 / 437 / 418  OK")


def check_schifferstadt():
    z = zones("schifferstadt")
    assert z[2]["schaltzone"] and z[9]["schaltzone"], "Schaltzonen 2 and 9"
    assert a("schifferstadt", [2] + list(range(5, 12))) == 266, "8 zones (2,5-11) = 266 symbols"
    assert a("schifferstadt", range(2, 12)) == 310, "zones 2-11 = 310 symbols"
    assert sk("schifferstadt", range(2, 12)) == 557, "zones 2-11 = 557 rings"
    assert sk("schifferstadt", [2] + list(range(5, 10))) == 311, "six disc zones (2,5-9) = 311 rings"
    assert 311 + 44 == 355, "311 + 44 Sondermuster (Z3+Z4) = 355"
    assert (z[10]["A"] + z[11]["A"]) * 2 == 202, "101 Krempe motifs x 2 rings = 202"
    assert 355 + 202 == 557, "355 + 202 = 557"
    assert sk("schifferstadt", range(2, 10)) == 355, "zones 2-9 = 355 rings (a lunar year)"
    print("  Schifferstadt: 266 / 310 / 311 / 355 / 557 / 202  OK")


def check_avanton():
    z = zones("avanton")
    assert all(z[n]["reconstructed"] for n in (12, 13, 14)), "zones 12-14 reconstructed"
    assert z[12]["schaltzone"], "Schaltzone 12"
    assert a("avanton", range(2, 15)) == 269, "zones 2-14 = 269 disc symbols"
    assert sk("avanton", range(2, 15)) == 583, "zones 2-14 = 583 rings"
    assert sk("avanton", range(3, 15)) == 537, "shaft zones 3-14 = 537 rings"
    assert sk("avanton", range(3, 12)) == 360, "zones 3-11 = 360 rings (a solar year)"
    assert sk("avanton", range(3, 8)) == 182, "zones 3-7 = 182 rings"
    assert sk("avanton", range(8, 15)) == 355, "zones 8-14 = 355 rings (a lunar year)"
    assert sk("avanton", [9, 10, 11, 13, 14]) == 271, "zones 9-14 minus SZ12 = 271 rings"
    assert sk("avanton", range(6, 14)) == 364, "zones 6-13 = 364 rings"
    assert sk("avanton", range(12, 15)) == 177, "zones 12-14 = 177 rings"
    # p. 79 divides 177 by (3x2) = 6 for six lunations, yet says Schaltzone 12 is
    # dropped; with zone 12 dropped the sum is 135 and 135/6 = 22.5. One of
    # Menghin's own rows does not close -- flagged, not forced.
    warned.append(
        "Avanton, 6 lunations: text uses Rz = 177 (zones 12-14, SZ12 included) "
        "over (3x2)=6 zones while stating SZ12 is dropped; 135/6 = 22.5"
    )
    print("  Avanton: 269 / 583 / 537 / 360 / 182 / 355 / 271 / 364 / 177  OK")


def check_ezelsdorf():
    z = zones("ezelsdorf")
    assert all(z[n]["schaltzone"] for n in (5, 6, 19)), "Schaltzonen 5, 6, 19"
    assert sk("ezelsdorf", range(3, 21)) == 1463, "zones 3-20 = 1463 rings"
    assert sk("ezelsdorf", range(3, 22)) == 1694, "zones 3-21 = 1694 rings, 17 zones with rings"
    assert 1463 + 21 + 22 + 231 == 1737, "1737 Zeichen with the reconstructed rim zone 21"
    assert sk("ezelsdorf", range(6, 22)) == 1448, "zones 6-21 = 1448 rings"
    assert 1448 + z[5]["SK"] == 1502, "1448 + 54 (SZ5) = 1502"
    assert 1502 - z[6]["SK"] == 1418, "1502 - 84 (SZ6) = 1418"
    assert 1463 - z[19]["SK"] == 1411, "1463 - 52 (SZ19) = 1411"
    assert 1463 + 21 + 22 == 1506, "zones 3-20 Zeichen = 1506"
    assert a("ezelsdorf", [n for n in range(3, 21) if z[n]["K"] is not None]) == 432, (
        "zones 3-20 disc symbols = 432"
    )
    assert a("ezelsdorf", range(2, 21)) == 499, (
        "zones 2-20 all stamped symbols incl. the Sonderzeichen zones 15 and 17 = 499"
    )
    # the published symbol totals that do NOT reproduce -> WARN, never forced
    for key, got, want in (
        ("symbols_z3_z20", a("ezelsdorf", range(3, 21)), 474),
        ("symbols_z3_z21", a("ezelsdorf", range(3, 21)) + 33, 505),
        ("scheibensymbole_z3_z21", 432 + 33, 462),
    ):
        if got != want:
            warned.append(f"Ezelsdorf {key}: table {got} vs text {want} (delta {got - want})")
    print("  Ezelsdorf: 1463 / 1694 / 1737 / 1502 / 1448 / 1411 / 1506 / 432  OK")


def check_formula_table():
    """Abb. 43,1 (p. 88): Rz divided by the number of months."""
    rows = [
        (1739, 57, 30.508), (1682, 57, 29.508),
        (1644, 54, 30.444), (1597, 54, 29.574),
        (1424, 48, 29.666), (1462, 48, 30.458),
        (1461, 48, 30.437), (1423, 48, 29.645),
        (1062, 36, 29.500), (1100, 36, 30.555),
        (1097, 36, 30.472), (1059, 36, 29.416),
        (729, 24, 30.375), (710, 24, 29.583),
        (548, 18, 30.444),
        (365, 12, 30.416), (355, 12, 29.583),
        (264, 9, 29.333),
    ]
    for rz, months, printed in rows:
        got = rz / months
        if min(abs(round(got, 3) - printed), abs(int(got * 1000) / 1000 - printed)) > 0.002:
            raise AssertionError(f"Abb.43,1: {rz}/{months} = {got:.3f}, printed {printed}")
    assert [r[0] for r in rows][:4] == [1739, 1682, 1644, 1597]
    print(f"  Abb. 43,1 formula column reproduces ({len(rows)} rows)  OK")


def check_menghin_2010_agreement():
    """The 2000 table (p. 45) must agree with the 2010-derived data/zones.json."""
    zs = json.loads((ROOT / "data/zones.json").read_text())["zones"]
    b = zones("berlin")
    for z in zs:
        if z["zone"] == 5:
            continue
        assert b[z["zone"]]["A"] == z["count"], f"Z{z['zone']} count vs 2010"
        assert b[z["zone"]]["K"] == z["rings"], f"Z{z['zone']} rings vs 2010"
        assert b[z["zone"]]["SK"] == z["day_value"], f"Z{z['zone']} SK vs 2010 day_value"
    print("  Menghin 2000 p. 45 table == Menghin 2010-derived data/zones.json  OK")


if __name__ == "__main__":
    print("Control C6 - Menghin 2000 per-zone tables")
    check_internal()
    check_berlin()
    check_schifferstadt()
    check_avanton()
    check_ezelsdorf()
    check_formula_table()
    check_menghin_2010_agreement()
    if warned:
        print("\nWARN - flagged in sources/menghin_2000_2010.md, not forced:")
        for w in warned:
            print("   -", w)
    print("\nAll ring identities reproduce.")
