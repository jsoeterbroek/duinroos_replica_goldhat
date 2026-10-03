#!/usr/bin/env python3
"""Measure the Berlin Gold Hat's silhouette from a photo, and forward-check r(z).

numpy + PIL only. No OpenCV, and none is needed.

    python3 scripts/measure_silhouette.py --list
    python3 scripts/measure_silhouette.py "assets/Cappello_....jpg" --dump
    python3 scripts/measure_silhouette.py "assets/Cappello_....jpg" --project

Segmentation: the background is *whatever the image border strip is* -- these
photos sit on a pure black surround -- so the foreground is any pixel far enough
from the border median. That is deliberately dumber than Otsu, which returns a
degenerate threshold when the border is one flat colour and then inverts.

`--dump` prints the mask as ASCII. That is how an agent whose model cannot
accept image content verifies that segmentation found the hat and not the
backdrop, a display stand, or a case reflection.

Why this is a *forward* check and not a measurement of r(z): the usable photo is
a tilted view (15 deg or so). A ring of radius r at height z projects to an
ellipse, not a point row, so the silhouette at a given row is

    max over z of  r(z) * sqrt(1 - ((v - z*cos t)/(r(z)*sin t))**2)

with v the image row in mm. Reading r(z) straight off the outline is therefore
wrong by up to r*sin(t) ~ 40 px of vertical smear. Instead the scale and tilt are
recovered from the brim, and the *planned* profile is projected and compared with
what the photo actually shows. See IMPLEMENTATION_PLAN.md section 12 (P1).
"""

import argparse
import glob
import json
import math
import os
import sys

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAT_HEIGHT_MM = 745.0
BRIM_DIA_MM = 301.0


def silhouette(path, tol=None):
    """Foreground = far from the border median. Returns (mask, bg, tol)."""
    gray = np.asarray(Image.open(path).convert("L"), float)
    h, w = gray.shape
    pad = max(2, min(h, w) // 50)
    border = np.concatenate(
        [gray[:pad].ravel(), gray[-pad:].ravel(),
         gray[:, :pad].ravel(), gray[:, -pad:].ravel()]
    )
    bg = float(np.median(border))
    mad = float(np.median(np.abs(border - bg)))
    if tol is None:
        # 6*MAD tolerates a noisy background. The floor is 4, not 12: on the
        # museum photo the hat's own shadowed gold is barely brighter than the
        # black surround, and a floor of 12 carves holes out of the lower shaft
        # (48 collapsed rows at 12, 1 at 4). A floor of ~4 is just above this
        # scan's JPEG noise. Override with --tol.
        tol = max(4.0, 6.0 * mad)
    return np.abs(gray - bg) > tol, bg, tol


def runs(row):
    """Contiguous foreground spans in one row, as [(x_start, x_end)] inclusive."""
    idx = np.flatnonzero(row)
    if idx.size == 0:
        return []
    brk = np.flatnonzero(np.diff(idx) > 1)
    starts = np.concatenate(([0], brk + 1))
    ends = np.concatenate((brk, [idx.size - 1]))
    return [(int(idx[s]), int(idx[e])) for s, e in zip(starts, ends)]


def envelope(mask, gap_tol=25, min_run=3):
    """Per-row outer extent of the object, as [(y, x0, x1)].

    The gold surface fragments into many runs per row -- the dark seams between
    bosses fall below tolerance -- so a row's extent is the *envelope* of its
    runs, not its longest run. Runs lying further than `gap_tol` px from the
    widest run are case reflections and are dropped. That is a row-wise stand-in
    for connected-component labelling, which numpy alone cannot do here.
    """
    out = []
    for y in range(mask.shape[0]):
        spans = runs(mask[y])
        if not spans:
            continue
        k = max(range(len(spans)), key=lambda i: spans[i][1] - spans[i][0])
        lo = hi = k
        while lo > 0 and spans[lo][0] - spans[lo - 1][1] - 1 <= gap_tol:
            lo -= 1
        while hi < len(spans) - 1 and spans[hi + 1][0] - spans[hi][1] - 1 <= gap_tol:
            hi += 1
        x0, x1 = spans[lo][0], spans[hi][1]
        if x1 - x0 + 1 >= min_run:
            out.append((y, x0, x1))
    return despike(out)


def despike(env, half=10, frac=0.6):
    """Drop single-row envelope dropouts.

    Where a whole flank of the object falls into shadow, one row's envelope can
    collapse to a fraction of its neighbours'. Interpolating those from the
    surrounding rows is what any hand measurement would do; left in, a single
    such row moves a control-point reading by tens of mm.
    """
    if len(env) < 2 * half + 1:
        return env
    ys = np.array([r[0] for r in env], float)
    w = np.array([r[2] - r[1] + 1 for r in env], float)
    cx = np.array([(r[1] + r[2]) / 2.0 for r in env])
    good = np.ones(len(env), bool)
    for i in range(half, len(env) - half):
        window = np.median(w[i - half:i + half + 1])
        if w[i] < frac * window:
            good[i] = False
    if good.all():
        return env
    w_fix = np.interp(ys, ys[good], w[good])
    cx_fix = np.interp(ys, ys[good], cx[good])
    out = []
    for i, (y, x0, x1) in enumerate(env):
        if good[i]:
            out.append((y, x0, x1))
        else:
            a = int(round(cx_fix[i] - w_fix[i] / 2.0))
            out.append((y, a, a + int(round(w_fix[i])) - 1))
    return out


def ascii_dump(mask, cols=72, rows=30):
    h, w = mask.shape
    return [
        "".join(
            "#" if mask[r * h // rows:max(r * h // rows + 1, (r + 1) * h // rows),
                         c * w // cols:max(c * w // cols + 1, (c + 1) * w // cols)].any()
            else "."
            for c in range(cols)
        )
        for r in range(rows)
    ]


def planned_profile():
    """Control points from data/hat_parameters.json, as (z, r) in mm."""
    with open(os.path.join(REPO, "data", "hat_parameters.json")) as fh:
        d = json.load(fh)
    return [(p["z"], p["r"]) for p in d["profile"]]


def sampled(ctrl, step=0.5):
    """The planned profile on a fine z grid (linear between control points)."""
    zs = np.array([z for z, _ in ctrl], float)
    rs = np.array([r for _, r in ctrl], float)
    z = np.arange(zs[0], zs[-1] + step, step)
    return z, np.interp(z, zs, rs)


def projected_halfwidth(ctrl, s, theta, y0, rows, zcap=None):
    """Half-width in mm that a tilted projection of r(z) shows at each image row.

    Each ring at height z and radius r projects to an ellipse of horizontal
    semi-axis r and vertical semi-axis r*sin(theta); the silhouette is the
    upper envelope over all rings.
    """
    z, r = sampled(ctrl)
    if zcap is not None:
        keep = z <= zcap
        z, r = z[keep], r[keep]
    ring_v = z * math.cos(theta)          # ring centre, in mm down the image
    semi = np.maximum(r * math.sin(theta), 1e-6)
    v = (np.asarray(rows, float) - y0) * s
    t = (v[:, None] - ring_v[None, :]) / semi[None, :]
    inside = np.abs(t) <= 1.0
    hw = np.where(inside, r[None, :] * np.sqrt(np.maximum(0.0, 1.0 - t * t)), -1.0)
    return hw.max(axis=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dump", action="store_true", help="print the mask as ASCII")
    ap.add_argument("--project", action="store_true",
                    help="recover scale+tilt from the brim and forward-check r(z)")
    ap.add_argument("--samples", type=int, default=12)
    ap.add_argument("--tol", type=float, default=None)
    a = ap.parse_args()

    paths = a.images
    if a.list or not paths:
        paths = sorted(
            p for p in glob.glob(os.path.join(REPO, "assets", "*"))
            if p.lower().endswith((".jpg", ".jpeg", ".png"))
        )

    for p in paths:
        name = os.path.relpath(p, REPO)
        try:
            mask, bg, tol = silhouette(p, a.tol)
        except Exception as exc:
            print(f"{name}: FAILED to open ({exc})")
            continue
        env = envelope(mask)
        print(f"\n=== {name}")
        print(f"    canvas {mask.shape[1]}x{mask.shape[0]}  bg={bg:.0f} tol={tol:.0f} "
              f"foreground={100.0 * mask.mean():.1f}% of pixels")
        if len(env) < 20:
            print("    no usable silhouette -- is the object actually in this image?")
            continue

        if a.dump:
            print("    mask ('#' = foreground):")
            for line in ascii_dump(mask):
                print("      " + line)

        y0 = env[0][0]
        widest = max(env, key=lambda r: r[2] - r[1])
        brim_px = widest[2] - widest[1] + 1
        # Horizontal scale is exact: the brim's half-width IS the Krempenrand radius.
        s = (BRIM_DIA_MM / 2.0) / (brim_px / 2.0)
        cx = (widest[1] + widest[2]) / 2.0

        print(f"    rows {y0}..{env[-1][0]}   widest row {widest[0]} = {brim_px} px"
              f"  =>  scale {s:.4f} mm/px")
        print(f"    naive aspect h/w = {(env[-1][0] - y0 + 1) / brim_px:.3f}"
              f"   (745/301 = {HAT_HEIGHT_MM / BRIM_DIA_MM:.3f})")

        # Symmetry about the brim axis: a body of revolution seen front-on is
        # symmetric. A drift means the view is off-axis, so the outline is not
        # to be trusted whatever else agrees.
        # Rows below the brim's own silhouette edge are specks, not the hat.
        brim_bottom_guess = widest[0] + (BRIM_DIA_MM / 2.0) * math.sin(math.pi / 9) / s
        asym = [abs((cx - r[1]) - (r[2] - cx)) * s
                for r in env if y0 + 30 < r[0] < brim_bottom_guess]
        print(f"    worst L-R asymmetry about the brim axis: {max(asym):.1f} mm"
              f"{'   <-- off-axis view' if max(asym) > 6.0 else ''}")
        print(f"    {'z mm':>7} {'dia mm':>8} {'L mm':>7} {'R mm':>7}")
        obj_h = env[-1][0] - y0 + 1
        for i in range(a.samples):
            y = int(round(y0 + i * (obj_h - 1) / (a.samples - 1)))
            near = min(env, key=lambda r: abs(r[0] - y))
            print(f"    {(near[0] - y0) * s:7.1f} {(near[2] - near[1] + 1) * s:8.1f}"
                  f" {(cx - near[1]) * s:7.1f} {(near[2] - cx) * s:7.1f}")

        if not a.project:
            continue

        # Recover the tilt from the brim: its centre row is the widest row, and
        # the axis point at z=0 sits on the apex row, so cos(t) follows from the
        # projected axis length. Then refine against the whole outline.
        ctrl = planned_profile()
        cos_t0 = (widest[0] - y0) * s / HAT_HEIGHT_MM
        t0 = math.acos(min(1.0, cos_t0))
        rows = np.array([r[0] for r in env], float)
        meas = np.array([(r[2] - r[1] + 1) / 2.0 * s for r in env])

        def rms(theta, lo, hi):
            m = (rows >= lo) & (rows <= hi)
            pred = projected_halfwidth(ctrl, s, theta, y0, rows[m])
            return float(np.sqrt(np.mean((pred - meas[m]) ** 2)))

        grid = np.radians(np.arange(max(0.0, math.degrees(t0) - 8.0),
                                    math.degrees(t0) + 8.0, 0.1))
        best = min(grid, key=lambda t: rms(t, y0, rows[-1]))
        for span in (0.05, 0.01):
            grid = np.arange(best - span, best + span, span / 10.0)
            best = min(grid, key=lambda t: rms(t, y0, rows[-1]))

        th = math.degrees(best)
        print(f"\n    --- tilt recovered from the brim: {math.degrees(t0):.1f} deg,"
              f" refined to {th:.2f} deg")
        brim_bottom = widest[0] + (BRIM_DIA_MM / 2.0) * math.sin(best) / s
        print(f"    brim lower silhouette edge predicted at row {brim_bottom:.0f}"
              f" (foreground ends {env[-1][0]})")
        print(f"    {'z mm':>7} {'row':>6} {'planned r':>10} {'photo r':>8}"
              f" {'delta':>7}   section")
        secs = [(0, 68, 'apex z1'), (68, 160, 'shaft z2-5'), (160, 312, 'shaft z6-9'),
                (312, 445, 'shaft z10-12'), (445, 611, 'shaft z13-16'),
                (611, 629, 'cuff/Kalotte base'), (629, 738, 'Kalotte z17-19'),
                (738, HAT_HEIGHT_MM, 'Krempe')]
        for z, r in ctrl:
            if z <= 0:
                continue
            y = y0 + z * math.cos(best) / s
            near = min(env, key=lambda rr: abs(rr[0] - y))
            got = (near[2] - near[1] + 1) / 2.0 * s
            pred = float(projected_halfwidth(ctrl, s, best, y0, [y])[0])
            name = next((n for a, b, n in secs if a <= z < b), '')
            print(f"    {z:7.1f} {y:6.0f} {pred:10.1f} {got:8.1f} {got - pred:+7.1f}"
                  f"   {name}")
        print("\n    RMS of (photo - projected profile), in radius:")
        for a, b, n in secs:
            lo, hi = y0 + a * math.cos(best) / s, y0 + b * math.cos(best) / s
            if n == 'Krempe':
                continue
            print(f"      {n:<14} (rows {lo:4.0f}-{hi:4.0f}): {rms(best, lo, hi):5.2f} mm")
        print("\n    P1 criterion (plan section 12): <= 2 mm radius at the Krempenrand,")
        print("    the Kalottenfuss and the mid-shaft z=312; <= 5 mm elsewhere except")
        print("    the stepped cuff. Every larger residual must be attributed.")


if __name__ == "__main__":
    sys.exit(main())
