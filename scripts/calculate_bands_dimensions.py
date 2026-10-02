import math

# --- objects ---
objects = [
    # LET OP: diam_mm x 2 + 2
    {"name": "z03", "height_mm": 14, "top_diam_mm": 64, "bottom_diam_mm": 60}, 
    {"name": "z04", "height_mm": 22, "top_diam_mm": 72, "bottom_diam_mm": 68}, 
    {"name": "z05", "height_mm": 24.5, "top_diam_mm": 80, "bottom_diam_mm": 76}, 
    {"name": "z06", "height_mm": 25, "top_diam_mm": 88, "bottom_diam_mm": 84}, 
    {"name": "z07", "height_mm": 29, "top_diam_mm": 96, "bottom_diam_mm": 92}, 
    {"name": "z08", "height_mm": 29, "top_diam_mm": 104, "bottom_diam_mm": 100},
    {"name": "z09", "height_mm": 34, "top_diam_mm": 112, "bottom_diam_mm": 108},
]

def frustum_strip(height_mm, top_diameter_mm, bottom_diameter_mm, thickness_mm=0.5):
    r_top = top_diameter_mm / 2.0
    r_bottom = bottom_diameter_mm / 2.0
    slant_height = math.sqrt(height_mm**2 + (r_top - r_bottom)**2)

    top_width = 2 * math.pi * r_top
    bottom_width = 2 * math.pi * r_bottom
    strip_length = (top_width + bottom_width) / 2.0
    area = 0.5 * (top_width + bottom_width) * slant_height

    if r_top != r_bottom:
        R_outer = (slant_height / (r_top - r_bottom)) * r_top
        R_inner = (slant_height / (r_top - r_bottom)) * r_bottom
        theta_rad = (2 * math.pi * (r_top - r_bottom)) / slant_height
        theta_deg = math.degrees(theta_rad)
    else:
        R_outer = R_inner = theta_rad = theta_deg = None

    return {
        "top_width_mm": top_width,
        "bottom_width_mm": bottom_width,
        "height_mm": slant_height,
        "strip_area_mm2": area,
        "strip_length_mm": strip_length,
        "thickness_mm": thickness_mm,
        "R_outer_mm": R_outer,
        "R_inner_mm": R_inner,
        "theta_rad": theta_rad,
        "theta_deg": theta_deg,
    }

def polar_to_cartesian(r, angle_rad):
    return r * math.cos(angle_rad), r * math.sin(angle_rad)


def make_svg(name, R_inner, R_outer, theta_rad, filename):
    """
    Generate an SVG path of an annular sector (curved band) in mm units.
    """
    # Points
    x1, y1 = polar_to_cartesian(R_outer, 0)
    x2, y2 = polar_to_cartesian(R_outer, theta_rad)
    x3, y3 = polar_to_cartesian(R_inner, theta_rad)
    x4, y4 = polar_to_cartesian(R_inner, 0)

    large_arc = 1 if theta_rad > math.pi else 0

    path = f"M {x1:.3f},{y1:.3f} " \
           f"A {R_outer:.3f},{R_outer:.3f} 0 {large_arc} 1 {x2:.3f},{y2:.3f} " \
           f"L {x3:.3f},{y3:.3f} " \
           f"A {R_inner:.3f},{R_inner:.3f} 0 {large_arc} 0 {x4:.3f},{y4:.3f} Z"

    # Add units in mm for proper scaling
    svg_content = f"""<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1"
     width="{2*R_outer:.3f}mm" height="{2*R_outer:.3f}mm"
     viewBox="{-R_outer-10:.3f} {-R_outer-10:.3f} {2*R_outer+20:.3f} {2*R_outer+20:.3f}">
  <title>{name} strip</title>
  <path d="{path}" fill="lightgray" stroke="black" stroke-width="0.2"/>
</svg>
"""
    with open(filename, "w") as f:
        f.write(svg_content)
    print(f"SVG saved to {filename}")


# --- Run calculations + SVG export ---
for obj in objects:
    res = frustum_strip(obj["height_mm"], obj["top_diam_mm"], obj["bottom_diam_mm"])
    print(f"\nObject {obj['name']}:")
    for k, v in res.items():
        if v is None:
            print(f"  {k}: N/A")
        else:
            print(f"  {k}: {v:.3f}")
    
    if res["R_inner_mm"] and res["R_outer_mm"]:
        make_svg(obj["name"], res["R_inner_mm"], res["R_outer_mm"],
                 res["theta_rad"], f"{obj['name']}_strip.svg")

