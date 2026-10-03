#!/usr/bin/env python3
"""
build_coupons.py — build the P3.5 motif-form coupons, HEADLESS.

Run it with freecadcmd, not through the MCP GUI bridge:

    freecadcmd scripts/build_coupons.py

Why headless: the MCP bridge enforces a ~90 s transport limit, and a real
boolean job on a band with 45 motifs takes longer than that. Exceeding it
wedges the bridge's GUI thread (the server then reports state `stuck`) and
needs a FreeCAD restart. `freecadcmd` has no GUI thread and no such limit, so
it is the correct place for any OCCT work that is not interactive.

Emits the three coupons for z15 into stl/test/, plus a fit-test trio, and
writes a report the plan can cite.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import band_geometry as G            # noqa: E402
import motif_features as F           # noqa: E402
import build_goldhat as B            # noqa: E402

OUT = os.path.join(HERE, "stl", "test")


def main():
    hp, zj = G.load()
    os.makedirs(OUT, exist_ok=True)
    results = []

    print("=== P3.5 coupons — zone 15, tool Nr.15 (d21 / 6 rings) ===")
    print("bare shell first, then one coupon per motif form\n")

    for form in F.FORMS:
        t = time.time()
        try:
            solid, info = F.build_coupon(hp, zj, form, zone_no=15,
                                         verbose=False)
            dt = time.time() - t
            path = os.path.join(OUT, "z15_%s.stl" % form)
            facets = B.export_stl(solid, path)
            size = os.path.getsize(path) / 1e6
            print("  z15_%-14s %8.1f mm3  (%+7.1f vs bare)  solids=%d valid=%s"
                  "  %d facets  %.1f MB  %.1fs"
                  % (form, solid.Volume, solid.Volume - info["bare_volume"],
                     len(solid.Solids), solid.isValid(), facets, size, dt))
            results.append(dict(info, facets=facets, mb=size, seconds=dt,
                                stl=os.path.basename(path)))
        except Exception as e:
            print("  z15_%-14s FAILED: %s" % (form, e))
            raise

    # --- the fit-test trio: z13 + z14 + z15 plain, to check the lap joint
    print("\n=== fit-test trio (plain bands, no motifs) ===")
    for bid in ("z13", "z14", "z15"):
        t = time.time()
        band = B.build(bid, out_dir=None, verbose=False)
        path = os.path.join(OUT, "%s_fit.stl" % bid)
        facets = B.export_stl(band, path)
        print("  %-4s %8.1f mm3  solids=%d valid=%s  %d facets  %.1fs"
              % (bid, band.Volume, len(band.Solids), band.isValid(),
                 facets, time.time() - t))

    # --- report
    rep = os.path.join(OUT, "coupon_report.txt")
    with open(rep, "w") as f:
        f.write("P3.5 motif-form coupons, zone 15 (15 x tool Nr.15, d21/6 rings)\n")
        f.write("built %s\n\n" % time.strftime("%Y-%m-%d %H:%M"))
        f.write("%-16s %10s %10s %8s %8s %8s\n"
                % ("form", "volume", "vs bare", "solids", "facets", "MB"))
        bare = results[0]["bare_volume"]
        for r in results:
            f.write("%-16s %10.1f %+10.1f %8d %8d %8.1f\n"
                    % (r["form"], r["volume"], r["volume"] - bare,
                       r["solids"], r["facets"], r["mb"]))
        f.write("\nbare shell: %.1f mm3\n" % bare)
        f.write("wall %.1f mm, relief %.1f mm\n"
                % (results[0]["wall_mm"], results[0]["relief_mm"]))
        f.write("\nJudgements 1-5 are in IMPLEMENTATION_PLAN.md 6.3.\n"
                "Print all three in matte PLA, in one job, and keep the silk out.\n")
    print("\nwrote %s" % rep)


if __name__ == "__main__" or __name__ == os.path.splitext(os.path.basename(__file__))[0]:
    # ⚠️ freecadcmd runs a script passed as a FILE ARGUMENT with __name__ set
    # to the script's basename ('build_coupons'), NOT '__main__'. A plain
    # `if __name__ == "__main__"` guard therefore silently does nothing and
    # freecadcmd still exits 0 -- a failure that looks like success. Accept
    # both forms.
    main()
