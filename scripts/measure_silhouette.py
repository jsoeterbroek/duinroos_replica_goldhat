#!/usr/bin/env python3
"""Measure the Berlin Gold Hat's silhouette from a photo, to derive the r(z) profile.

No OpenCV needed: numpy + PIL only.

    python3 scripts/measure_silhouette.py assets/Cappello_....jpg
    python3 scripts/measure_silhouette.py --list

Segmentation: the hat is assumed to be the foreground. For photos on a plain
(dark or light) background, Otsu's threshold on the border strip separates them.
The row-wise left/right extent of the foreground gives the silhouette width
profile, which is what Q5 (straight cone vs. Kalotte+Krempe) turns on.

Output is in *pixels* and in mm, the latter scaled so the object bounding-box
height equals --height (default 745 mm, the Menghin total).
"""

import argparse
import glob
import os
import sys

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def otsu(values):
    hist, edges = np.histogram(values, bins=256)
    centers = (edges[:-1] + edges[1:]) / 2
    w = hist.astype(float)
    if w.sum() == 0:
        return 128.0
    w /= w.sum()
    omega = np.cumsum(w)
    mu = np.cumsum(w * centers)
    mu_t = mu[-1]
    denom = omega * (1 - omega)
    denom[denom == 0] = 1e-12
    sigma_b = (mu_t * omega - mu) ** 2 / denom
    return float(centers[int(np.argmax(sigma_b))])


def silhouette(path):
    gray = np.asarray(Image.open(path).convert("L"), float)
    h, w = gray.shape
    pad = max(2, min(h, w) // 100)
    border = np.concatenate(
        [
            gray[:pad].ravel(),
            gray[-pad:].ravel(),
            gray[:, :pad].ravel(),
            gray[:, -pad:].ravel(),
        ]
    )
    thr = otsu(border)
    bg_is_dark = border.mean() < thr
    mask = gray > thr if bg_is_dark else gray < thr
    return mask, thr, bg_is_dark


def profile(mask, min_run=3):
    """Per-row first/last foreground column; drops rows with a shorter run (noise)."""
    rows = []
    for y in range(mask.shape[0]):
        idx = np.flatnonzero(mask[y])
        if idx.size >= min_run and idx[-1] - idx[0] >= min_run:
            rows.append((y, int(idx[0]), int(idx[-1])))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="*")
    ap.add_argument("--height", type=float, default=745.0, help="true object height in mm")
    ap.add_argument("--samples", type=int, default=12)
    ap.add_argument("--list", action="store_true")
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
            mask, thr, dark = silhouette(p)
            rows = profile(mask)
        except Exception as exc:  # pragma: no cover - diagnostic path
            print(f"{name}: FAILED ({exc})")
            continue
        if len(rows) < 20:
            print(f"{name}: no usable silhouette (thr={thr:.0f}, foreground rows={len(rows)})")
            continue

        y0, y1 = rows[0][0], rows[-1][0]
        x0 = min(r[1] for r in rows)
        x1 = max(r[2] for r in rows)
        obj_h, obj_w = y1 - y0 + 1, x1 - x0 + 1
        mmpp = a.height / obj_h

        print(f"\n=== {name}")
        print(f"    canvas {mask.shape[1]}x{mask.shape[0]}  thr={thr:.0f} "
              f"({'light hat on dark bg' if dark else 'dark hat on light bg'})")
        print(f"    object bbox {obj_w}x{obj_h} px   aspect h/w = {obj_h / obj_w:.2f}")
        print(f"    scale        {mmpp:.3f} mm/px   =>  widest point = {obj_w * mmpp:.0f} mm diameter")
        print(f"    {'z mm':>7} {'width mm':>9} {'dia mm':>8}  {'d/dx':>6}")
        prev = None
        for i in range(a.samples):
            y = int(round(y0 + i * (obj_h - 1) / (a.samples - 1)))
            near = min(rows, key=lambda r: abs(r[0] - y))
            wid = (near[2] - near[1] + 1) * mmpp
            z = (near[0] - y0) * mmpp
            slope = "" if prev is None else f"{(wid - prev) / (wid / 2):.4f}"
            print(f"    {z:7.1f} {wid:9.1f} {wid:8.1f}  {slope:>6}")
            prev = wid
        print("    ('d/dx' is the local diameter growth per mm of height; constant => straight cone)")


if __name__ == "__main__":
    sys.exit(main())
