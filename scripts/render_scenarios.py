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
import motifs as M                                                   # noqa: E402

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


def draw_scenario(ax, state, profile, zones, hp, day_value, legend=True):
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
    if legend:
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


def render_sheet(states, profile, zones, hp, day_value, out_dir, fmt,
                 group_id, verbose=True):
    """
    One 4-up contact sheet in the source's page layout (2 x 2), like Menghin's
    pp. 60-63. Four states, a shared legend, a page title, and each panel keeps
    its own numbers, SZ marks, glyphs and arithmetic caption.
    """
    fig = plt.figure(figsize=(12.4, 15.4), dpi=130)
    grid = fig.add_gridspec(2, 2, left=0.03, right=0.97, top=0.905, bottom=0.035,
                            wspace=0.04, hspace=0.10)
    for i, st in enumerate(states[:4]):
        ax = fig.add_subplot(grid[i // 2, i % 2])
        ax.set_aspect("equal")
        ax.set_xlim(-238, 178)
        ax.set_ylim(848, -46)                # inverted: apex (z=0) at the top
        ax.axis("off")
        draw_scenario(ax, st, profile, zones, hp, day_value, legend=False)
        ax.set_title(FG.state_title(st), fontsize=9.4, fontweight="bold", pad=4)
        cap = FG.caption(st, day_value)
        ax.text(0, 812, "\n".join(textwrap.wrap(cap, 52)), fontsize=7.0,
                ha="center", va="top")

    handles = [Rectangle((0, 0), 1, 1, facecolor=FG.CATEGORY_COLOURS[c],
                          edgecolor="#8a8a8a", lw=0.5,
                          label=FG.CATEGORY_LABELS[c]) for c in FG.CATEGORY_ORDER]
    fig.legend(handles=handles, loc="upper center", ncol=4, frameon=False,
               fontsize=8.4, bbox_to_anchor=(0.5, 0.972), columnspacing=2.4)
    fig.suptitle("Menghin (2010) — solar / lunar / intercalary blocks, "
                 "Abb. %s.x  (%s)" % (group_id,
                                      ", ".join(s["id"] for s in states[:4])),
                 fontsize=13.5, fontweight="bold", y=0.988)
    fig.text(0.5, 0.008,
             "data/scenarios.json + data/zones.json + data/hat_parameters.json"
             "  ·  scripts/render_scenarios.py",
             ha="center", va="bottom", fontsize=6.2, color="#777777")

    written = []
    if fmt:
        os.makedirs(out_dir, exist_ok=True)
        for f in fmt:
            path = os.path.join(out_dir, "sheet_%s.%s" % (group_id, f))
            fig.savefig(path, format=f, facecolor="white",
                        metadata={"Software": None} if f != "pdf" else None)
            written.append(path)
    plt.close(fig)
    if verbose:
        print("  sheet_%-4s %s -> %s" % (group_id,
                                         ", ".join(s["id"] for s in states[:4]),
                                         ", ".join(os.path.basename(p) for p in written)))
    return written


def draw_development(ax, state, zones, hp, profile, day_value, maxcirc):
    """
    Unrolled ornament (Abrollung), coloured by the scenario.

    Unlike the F1 silhouette, each zone is drawn at its OWN circumference, so
    the strips form the unrolled trapezoid and every motif appears exactly once
    -- the number attached to a zone becomes visible AS the ornaments it counts.
    Motifs come from motifs.placed_zone_motifs(), the same placement the SVG
    development and (in placement terms) the 3D build use. The two Krempe zones
    are concentric rings on a flat plate, so they are drawn as their real RADIAL
    widths (25 mm and 31 mm), not as the 7 mm stack height.
    """
    krempe_ids = [k["zone"] for k in hp["krempe"]["rings"]]
    split = FG.krempe_split_radius(hp)
    k0 = hp["krempe"]
    krempe_y = min(z["z_mm"][0] for z in zones if z.get("section") == "krempe")
    for zone in zones:
        cat = FG.classify(state["display"], zone["zone"])
        circ, h, motifs = M.placed_zone_motifs(zone, profile, hp)
        if zone.get("section") == "krempe":
            idx = krempe_ids.index(zone["zone"])
            width = (split - k0["r_inner_mm"]) if idx == 0 else (k0["r_outer_mm"] - split)
            y0, y1 = krempe_y, krempe_y + width
            krempe_y = y1
        else:
            y0, y1 = zone["z_mm"]
        zc = 0.5 * (y0 + y1)

        ax.add_patch(Rectangle((-circ / 2.0, y0), circ, y1 - y0,
                               facecolor=FG.CATEGORY_COLOURS[cat],
                               edgecolor="#b8b8b8", lw=0.3, zorder=1))
        for cu, v_off, outer, holes in motifs:
            ax.add_patch(Polygon([(cu + u, zc + v_off + v) for (u, v) in outer],
                                 closed=True, facecolor="#c9a227",
                                 edgecolor="#8a6d1a", lw=0.12, zorder=2))
            for hh in holes:
                if hh and isinstance(hh[0][0], (list, tuple)):
                    # a ring band (trough): outline its two circles so the
                    # concentric rings read, instead of filling a solid disc
                    for ring in hh:
                        ax.add_patch(Polygon(
                            [(cu + u, zc + v_off + v) for (u, v) in ring],
                            closed=True, facecolor="none",
                            edgecolor="#8a6d1a", lw=0.22, zorder=3))
                else:
                    ax.add_patch(Polygon(
                        [(cu + u, zc + v_off + v) for (u, v) in hh],
                        closed=True, facecolor="#fff6e0",
                        edgecolor="#b99a3a", lw=0.1, zorder=3))
        ax.text(-maxcirc / 2.0 - 6.0, zc, "Z%d" % zone["zone"],
                fontsize=5.6, ha="right", va="center")


def render_development(state, profile, zones, hp, day_value, out_dir, fmt,
                        maxcirc, verbose=True):
    fig = plt.figure(figsize=(11.6, 10.8), dpi=140)
    ax = fig.add_axes([0.055, 0.115, 0.92, 0.82])
    ax.set_aspect("equal")
    ax.set_xlim(-maxcirc / 2.0 - 52, maxcirc / 2.0 + 10)
    dev_bottom = hp["krempe"]["z_inner_mm"] + \
        (hp["krempe"]["r_outer_mm"] - hp["krempe"]["r_inner_mm"])
    ax.set_ylim(dev_bottom + 36, -46)
    ax.axis("off")
    draw_development(ax, state, zones, hp, profile, day_value, maxcirc)

    fig.suptitle("Unrolled ornament (Abrollung) — %s" % FG.state_title(state),
                 fontsize=12.0, fontweight="bold", y=0.972)
    fig.text(0.5, 0.062, "\n".join(textwrap.wrap(FG.caption(state, day_value), 104)),
             ha="center", va="bottom", fontsize=8.2)
    handles = [Rectangle((0, 0), 1, 1, facecolor=FG.CATEGORY_COLOURS[c],
                          edgecolor="#8a8a8a", lw=0.5,
                          label=FG.CATEGORY_LABELS[c]) for c in FG.CATEGORY_ORDER]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
               fontsize=8.0, bbox_to_anchor=(0.5, 0.022), columnspacing=2.4)
    fig.text(0.5, 0.006, "data/*.json  ·  scripts/render_scenarios.py  ·  "
             "motifs by data/symbols.json", ha="center", va="bottom",
             fontsize=6.0, color="#777777")

    written = []
    if fmt:
        os.makedirs(out_dir, exist_ok=True)
        for f in fmt:
            path = os.path.join(out_dir,
                                "development_%s.%s" % (state["id"].replace(".", "_"), f))
            fig.savefig(path, format=f, facecolor="white",
                        metadata={"Software": None} if f != "pdf" else None)
            written.append(path)
    plt.close(fig)
    if verbose:
        print("  dev %-6s -> %s" % (state["id"],
                                    ", ".join(os.path.basename(p) for p in written)))
    return written


def render_all(out_dir, fmt, only=None, sheets=True, developments=True, verbose=True):
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
    if developments:
        maxcirc = max(M.placed_zone_motifs(z, profile, hp)[0] for z in zones)
        for st in states:
            written += render_development(st, profile, zones, hp, day, out_dir,
                                          fmt, maxcirc, verbose)
    if sheets and not only:
        # group by the leading figure number: 61.x, 62.x, 63.x, 64.x = 4 sheets
        groups = {}
        for st in states:
            groups.setdefault(st["id"].split(".")[0], []).append(st)
        for gid in sorted(groups):
            written += render_sheet(groups[gid], profile, zones, hp, day,
                                    out_dir, fmt, gid, verbose)
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", action="append", default=None,
                    help="scenario id(s), e.g. --state 61.1 (repeatable)")
    ap.add_argument("--all", action="store_true",
                    help="every state in scenarios.json, plus the 4-up sheets")
    ap.add_argument("--no-sheets", action="store_true",
                    help="with --all, skip the 4-up contact sheets")
    ap.add_argument("--no-developments", action="store_true",
                    help="with --all, skip the scenario-coloured developments (F2)")
    ap.add_argument("--out", default=os.path.join(HERE, "figures", "menghin"))
    ap.add_argument("--format", default="png", help="comma list: png,svg,pdf")
    args = ap.parse_args()
    fmts = [f.strip() for f in args.format.split(",") if f.strip()]
    if not args.all and not args.state:
        ap.error("pass --all or at least one --state")
    written = render_all(args.out, fmts, only=set(args.state or []),
                         sheets=not args.no_sheets,
                         developments=not args.no_developments)
    print("\n%d file(s) written to %s" % (len(written), args.out))
