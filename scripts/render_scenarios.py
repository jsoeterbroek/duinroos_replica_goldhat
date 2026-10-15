#!/usr/bin/env python3
"""
Stage 1 renderer — scenario figures in the style of Menghin (2010) pp. 60-63.

Reads only `data/*.json` (via figure_geometry) and draws, per scenario state,
the hat silhouette with its 21 zones coloured red = solar / blue = lunar /
green = intercalary, plus the zone numbers, the intercalary (SZ) marks, a small
legend and the arithmetic caption. One figure per state; a state with a null
side (61.2) is drawn with the caption saying so rather than a guessed number.

    python3 scripts/render_scenarios.py --state 61.1
    python3 scripts/render_scenarios.py --all
    python3 scripts/render_scenarios.py --all --format png,svg,pdf

matplotlib (Agg) is the only dependency, and only here; the geometry kernel
and everything Stage 2 uses stay dependency-free.
"""

import argparse
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))

import matplotlib                                                   # noqa: E402
matplotlib.use("Agg")                                                # noqa: E402
import matplotlib.pyplot as plt                                      # noqa: E402
from matplotlib.patches import Polygon, Rectangle, Circle, Wedge     # noqa: E402

import band_geometry as G                                            # noqa: E402
import figure_geometry as FG                                         # noqa: E402

Z_TOP = 745.0


# --- scene -------------------------------------------------------------------

def _zone_polygons(zone, profile, hp):
    if zone.get("section") == "krempe":
        return FG.krempe_zone_polygons(zone, hp)
    return [FG.zone_band(zone, profile)]


def _draw_glyphs(ax, x_center=0.0, z=-16.0):
    """A sun and a crescent above the apex, as on the source plates."""
    ax.add_patch(Circle((x_center, z), 8.0, facecolor="#e0a800",
                        edgecolor="#8a6d1a", lw=0.6, zorder=5))
    for k in range(8):
        import math
        a = k * math.pi / 4.0
        ax.plot([x_center + 10 * math.cos(a), x_center + 14 * math.cos(a)],
                [z + 10 * math.sin(a), z + 14 * math.sin(a)],
                color="#8a6d1a", lw=0.9, zorder=5, solid_capstyle="round")
    # crescent: full disc in the outline colour, then a fill-coloured disc offset
    cx = x_center + 46.0
    ax.add_patch(Circle((cx, z), 9.0, facecolor="#3a3a6a",
                        edgecolor="#22224a", lw=0.6, zorder=5))
    ax.add_patch(Circle((cx - 4.0, z - 1.5), 8.0,
                        facecolor=FG.SILHOUETTE_FILL,
                        edgecolor="none", zorder=6))


def _draw_legend(ax, x=196.0, z=640.0, dy=30.0):
    ax.text(x, z - 24, "legend", fontsize=8.0, fontweight="bold", va="top")
    for i, cat in enumerate(FG.CATEGORY_ORDER):
        zz = z + i * dy
        ax.add_patch(Rectangle((x, zz - 10), 22, 20,
                               facecolor=FG.CATEGORY_COLOURS[cat],
                               edgecolor="#8a8a8a", lw=0.5, zorder=4))
        ax.text(x + 28, zz, FG.CATEGORY_LABELS[cat], fontsize=7.4, va="center")


def draw_scenario(ax, state, profile, zones, hp, day_value):
    """Draw one state's hat onto `ax` (data coords: x = radius mm, y = z mm)."""
    # silhouette
    sil = FG.silhouette(profile)
    ax.add_patch(Polygon(sil, closed=True, facecolor=FG.SILHOUETTE_FILL,
                         edgecolor="none", zorder=1))
    # coloured zone bands
    zmap = {z["zone"]: z for z in zones}
    for zone in zones:
        cat = FG.classify(state["display"], zone["zone"])
        col = FG.CATEGORY_COLOURS[cat]
        for poly in _zone_polygons(zone, profile, hp):
            ax.add_patch(Polygon(poly, closed=True, facecolor=col,
                                 edgecolor="none", zorder=2))
    # outline last so it stays crisp over the bands
    ax.add_patch(Polygon(sil, closed=True, facecolor="none",
                         edgecolor=FG.OUTLINE_COLOUR, lw=0.8, zorder=3))

    # zone numbers, ticks and SZ marks on the left
    x_num, x_tick, x_sz = -168.0, -150.0, -205.0
    krempe_ids = [k["zone"] for k in hp["krempe"]["rings"]]
    for zone in zones:
        z0, z1 = zone["z_mm"]
        if zone["zone"] in krempe_ids:
            # both Krempe rings live at the same z: stagger their labels and
            # point each tick at its own ring radius
            idx = krempe_ids.index(zone["zone"])
            zc = 742.0 + idx * 13.0
            r_edge = hp["krempe"]["rings"][idx]["r_mid_mm"]
        else:
            zc = FG.zone_center_z(zone)
            r_edge = profile(0.5 * (z0 + z1))
        ax.plot([x_tick, -r_edge - 2.0], [zc, zc],
                color="#9a9a9a", lw=0.5, zorder=3)
        ax.text(x_num, zc, str(zone["zone"]), fontsize=7.6, ha="right",
                va="center", zorder=4)
        if FG.classify(state["display"], zone["zone"]) == "intercalary":
            ax.text(x_sz, zc, "SZ", fontsize=6.6, ha="right", va="center",
                    color="#2e6b3f", fontweight="bold", zorder=4)

    _draw_glyphs(ax)
    _draw_legend(ax)


def render_state(state, profile, zones, hp, day_value, out_dir, fmt, verbose=True):
    title = FG.state_title(state)
    cap = FG.caption(state, day_value)

    fig = plt.figure(figsize=(6.6, 9.4), dpi=150)
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.95])
    ax.set_aspect("equal")
    ax.set_xlim(-340, 340)
    ax.set_ylim(786, -30)                    # inverted: apex (z=0) at the top
    ax.axis("off")

    draw_scenario(ax, state, profile, zones, hp, day_value)

    fig.text(0.5, 0.965, title, ha="center", va="top",
             fontsize=11.5, fontweight="bold")
    fig.text(0.5, 0.035, "\n".join(textwrap.wrap(cap, 74)), ha="center",
             va="bottom", fontsize=8.6)
    fig.text(0.5, 0.006,
             "source: data/scenarios.json + data/zones.json + data/hat_parameters.json"
             "  ·  generated by scripts/render_scenarios.py",
             ha="center", va="bottom", fontsize=6.2, color="#777777")

    written = []
    if fmt:
        os.makedirs(out_dir, exist_ok=True)
        for f in fmt:
            path = os.path.join(out_dir, state["id"].replace(".", "_") + "." + f)
            fig.savefig(path, format=f, facecolor="white",
                        metadata={"Software": None} if f != "pdf" else None)
            written.append(path)
    plt.close(fig)
    if verbose:
        print("  %-6s %-30s -> %s" % (state["id"], title,
                                      ", ".join(os.path.basename(p) for p in written)
                                      or "(no file)"))
    return written


def render_all(out_dir, fmt, only=None, verbose=True):
    hp, zj = G.load()
    profile = G.Profile(hp["profile"])
    zones = zj["zones"]
    day = {z["zone"]: z["day_value"] for z in zones}
    sc = __import__("json").load(open(os.path.join(HERE, "data", "scenarios.json")))
    states = sc["states"]
    if only:
        states = [s for s in states if s["id"] in only]
    written = []
    for st in states:
        written += render_state(st, profile, zones, hp, day, out_dir, fmt, verbose)
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", action="append", default=None,
                    help="scenario id(s), e.g. --state 61.1 (repeatable)")
    ap.add_argument("--all", action="store_true", help="every state in scenarios.json")
    ap.add_argument("--out", default=os.path.join(HERE, "figures", "menghin"))
    ap.add_argument("--format", default="png", help="comma list: png,svg,pdf")
    args = ap.parse_args()
    fmts = [f.strip() for f in args.format.split(",") if f.strip()]
    if not args.all and not args.state:
        ap.error("pass --all or at least one --state")
    written = render_all(args.out, fmts, only=set(args.state or []))
    print("\n%d file(s) written to %s" % (len(written), args.out))
