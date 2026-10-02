# analyze_cone.py
# Requires: pip install opencv-python numpy
import cv2
import numpy as np
import sys
import math

def find_largest_contour(gray):
    edges = cv2.Canny(gray, 50, 150)
    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None
    cnt = max(cnts, key=cv2.contourArea)
    return cnt

def fit_base_ellipse(cnt, img_h):
    # Attempt to get the lower-region contour points (base area)
    pts = cnt.reshape(-1,2)
    # Keep points below mid-height of contour bounding box (bottom half)
    _, ycoords = pts[:,0], pts[:,1]
    y_mid = (np.min(ycoords) + np.max(ycoords)) / 2.0
    lower_pts = pts[pts[:,1] >= y_mid]
    if len(lower_pts) < 5:
        # fallback to full contour
        lower_pts = pts
    try:
        ellipse = cv2.fitEllipse(lower_pts)
        # ellipse: ((cx,cy),(MA,ma),angle)
        return ellipse
    except Exception:
        return None

def main(img_path, real_height_mm):
    img = cv2.imread(img_path)
    if img is None:
        print("Failed to open image:", img_path); return 1
    h,w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    cnt = find_largest_contour(gray)
    overlay = img.copy()
    if cnt is None:
        print("No contour found automatically. Consider providing manual points.")
        cv2.imwrite("cone_debug.png", overlay)
        return 1

    # Find apex = topmost point of the contour
    top_idx = np.argmin(cnt[:,:,1])
    apex = tuple(cnt[top_idx][0])
    cv2.circle(overlay, apex, 6, (0,0,255), -1)

    # Fit ellipse for base
    ellipse = fit_base_ellipse(cnt, h)
    if ellipse is None:
        print("Ellipse fit failed.")
        cv2.imwrite("cone_debug.png", overlay)
        return 1

    (cx,cy),(MA,ma),angle = ellipse
    major = max(MA, ma)
    minor = min(MA, ma)
    cx_i, cy_i = int(round(cx)), int(round(cy))
    cv2.ellipse(overlay, ellipse, (0,255,0), 2)
    cv2.circle(overlay, (cx_i, cy_i), 4, (255,0,0), -1)

    # Pixel measurements
    pixel_height = math.hypot(cx - apex[0], cy - apex[1])  # apex -> ellipse center projection
    # Sometimes apex is slightly off-center; optionally use vertical distance apex.y -> cy
    pixel_height_vertical = abs(cy - apex[1])

    mm_per_pixel = real_height_mm / pixel_height if pixel_height>0 else None
    mm_per_pixel_vert = real_height_mm / pixel_height_vertical if pixel_height_vertical>0 else None

    diameter_mm_by_major = major * mm_per_pixel if mm_per_pixel else None
    diameter_mm_by_major_vert = major * mm_per_pixel_vert if mm_per_pixel_vert else None

    # If ellipse is clearly flattened (minor << major), estimate tilt angle and attempt correction:
    tilt_correction = None
    if minor > 0 and major > 0:
        ratio = minor / major
        tilt_angle_rad = math.acos(min(1.0, max(0.0, ratio)))  # cos(phi) = b/a
        tilt_deg = math.degrees(tilt_angle_rad)
        tilt_correction = (ratio, tilt_deg)
        # True diameter estimate from observed major axis: major_pixels is already projection of true diameter,
        # so diameter = major_pixels * mm_per_pixel (if mm_per_pixel measured along same image scaling).
        # This is approximate; if the apex-to-center distance is foreshortened, using vertical pixel height may help.
    else:
        tilt_deg = None

    # Print results
    print("Image:", img_path, "size:", w, "x", h)
    print("Apex (px):", apex)
    print("Ellipse center (px):", (cx, cy))
    print("Ellipse axes (px): major=%.1f minor=%.1f angle=%.1f" % (major, minor, angle))
    print("Pixel height (apex -> ellipse center): %.1f px" % (pixel_height))
    print("Pixel vertical height (apex.y -> center.y): %.1f px" % (pixel_height_vertical))
    print("Scale (from known height %.1f mm): mm_per_pixel = %.6f (using apex->center)" % (real_height_mm, mm_per_pixel))
    print("Diameter estimate (major axis * scale): %.1f mm" % (diameter_mm_by_major))
    print("Diameter estimate (using vertical scale): %.1f mm" % (diameter_mm_by_major_vert))
    if tilt_correction:
        print("Ellipse ratio minor/major = %.3f -> estimated tilt = %.1f deg (approx)" % (tilt_correction[0], tilt_correction[1]))
        print("If the tilt is large, expect higher uncertainty; consider taking a photo more frontal or include a ruler.")

    # Draw annotation text
    cv2.putText(overlay, "Apex", (apex[0]+6, apex[1]-6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.putText(overlay, "Center", (cx_i+6, cy_i-6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    cv2.putText(overlay, "Diam ~ %.1f mm" % (diameter_mm_by_major if diameter_mm_by_major else 0), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,128,255), 2)

    cv2.imwrite("cone_debug.png", overlay)
    print("Wrote annotated image cone_debug.png")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python analyze_cone.py image.jpg 745")
        sys.exit(1)
    img_path = sys.argv[1]
    real_height_mm = float(sys.argv[2])
    sys.exit(main(img_path, real_height_mm))
