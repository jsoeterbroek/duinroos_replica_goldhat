# Berlin Gold Hat — Demonstration Scenarios (Menghin 2000, 2010)

This document translates the descriptive material in `gold_hat.md` into actionable demonstration scenarios for a life-size Berlin Gold Hat replica with individually addressable LEDs for every symbol in all 21 zones. Each scenario ties directly to Wilfried Menghin's calendrical interpretation and shows how the hat could be used as a lunisolar counting device. The goal is to have the microcontroller application (the `m5` project) drive the LED array and display calculated results and explanation text on-screen at the same time.

Assumptions
- The replica has 21 horizontal bands (zones) that match the counts in `gold_hat.md`.
- Each symbol position on the hat is fitted with a uniquely addressable LED (e.g., WS2812 or SK6812 RGB LEDs).
- The controller has enough I/O / LED drivers to handle ~3400 LEDs (or the design will multiplex / segment them across multiple drivers or use LED controllers like WS2811/WS2812 daisy-chained via high-power driver chips and level-shifting).
- The app can simultaneously control the display (`M5GFX`) and LED drivers and can present text, calculations, and visual highlights mapping to LED patterns.

Structure of this document
- Demo goals
- Data model (how band and symbol counts map to software objects)
- Scenario list (detailed): inputs, LED patterns, on-screen visualization, step-by-step behaviour, learning objectives, and edge cases
- UI flow and controls
- Hardware/implementation notes and constraints
- Tests and verification
- Recommended next steps and extension ideas

Demo goals
- Make Menghin's argument tangible by lighting the exact symbols and zones that are summed/subtracted to produce calendar numbers (e.g., 54 synodic months, Metonic cycle groupings).
- Allow interactive exploration (select start zone, choose contiguous range, toggle inclusion of intercalary zones) with live LED feedback and calculation display.
- Provide pre-baked scenarios that demonstrate canonical calculations from Menghin's analysis (e.g., 54-month lunar period example) and broader educational scenarios (Venus cycle comparison, Metonic 19-year grouping).

Data model
- Zone: { id: 1..21, symbol_count: int, ring_multiplier: int? }
- Symbol: { global_index: 0..N-1, zone_id, local_index, led_index }
- Intercalary zones: zone ids [5, 7, 16, 17] (per `gold_hat.md`) and special symbol values (e.g., zone 5 special symbols = 38)
- Day-value of a zone-range: sum(symbol_count(zone_i) * ring_multiplier(zone_i)) - sum(intercalary_values_included)

Note: For simplicity, use the symbol counts table in `gold_hat.md` (zone → symbol_count). If ring multipliers are needed, expose them as per the recorded example (e.g., zone 12 uses symbols with 5 rings → value 20×5 = 100).

Scenarios (detailed)

1) 54-Month Lunar Example — Reproduce Menghin's worked example
- Purpose: Demonstrate the canonical example in `gold_hat.md`: zones 3 to 21 summed minus intercalary zones 5, 16, 17 → 1,739 − 142 = 1,597 days = 54 synodic months.
- UI Input: Pre-set scenario; user taps "Run".
- LED Pattern:
  - Light zones 3..21 in green, symbols in those zones pulse in a slow inward ripple (or simple steady glow) to indicate they are included in the sum.
  - Intercalary symbols in zones 5, 16, 17 flash red to indicate they will be subtracted.
  - After the initial highlight, animate a subtraction: intercalary LEDs dim to off while included zone LEDs remain at steady green.
- On-screen Display:
  - Show the sum steps: "Sum zones 3–21 = 1,739" then "Subtract zones 5,16,17 = 142" then "Result = 1,597 days → 54 synodic months (×29.5305)".
  - Show the calculation as it happens, with the numeric values updating in sync with LED animation.
- Learning Objective: Tangibly link symbol-count arithmetic to an exact lunar-month value.
- Edge Cases: Provide a toggle to highlight exactly which symbols in the intercalary zones are considered special (e.g., special symbol value 38) vs. regular symbols.

2) Interactive Range Explorer — Pick start zone and count contiguous symbols
- Purpose: Let users explore how different contiguous ranges translate to day totals; shows how the hat could be used as a counting device.
- UI Input: Touch-select a start zone (tap a zone on the hat or the on-screen band map). Then drag or tap an end zone.
- LED Pattern:
  - Light the selected contiguous zones in cyan; as the user expands the range, newly included zones gently fade in.
  - If an intercalary zone is included, those symbols light in orange and a small hazard icon appears on-screen explaining subtraction rules.
  - Optionally show an animated pointer that steps through each symbol to emulate counting day-by-day (fast-forwardable).
- On-screen Display:
  - Live numeric sum; breakdown by zone; show whether intercalaries are included and how they affect the total.
  - A "Play" button to animate advancing one symbol per tick with LED stepping, illustrating the daily counting concept.
- Learning Objective: Demonstrate the fundamental operation of the device — contiguous counting and selective subtraction for intercalaries.
- Edge Cases: Very large ranges — provide a time-compression slider for day-by-day animation to finish within a reasonable demo time.

3) Metonic 19-Year Cycle Demo
- Purpose: Show how the hat encodes longer cycles (e.g., Metonic 19-year cycle or other derived long-period counts) by combining zone multiplications.
- UI Input: Pre-set scenario or "Show Metonic" button.
- LED Pattern:
  - Highlight the band groupings that Menghin or other scholars map to the Metonic grouping (e.g., show bands multiplied or repeated) in purple.
  - Animate a 19-year progression: for each fictional year, advance a marker that moves across the hat; after 19 cycles, show the cumulative day total.
- On-screen Display:
  - Show the Metonic calculation steps: e.g., "19×(some monthly grouping) = X days; compare against 19 solar years = Y days; difference = Z".
  - Optionally show error accumulation per year to explain why these cycles are approximations.
- Learning Objective: Show how multiplication of shorter counts yields long cycles and demonstrate the historical significance of Metonic approximations.
- Edge Cases: Clarify rounding and observational error; allow switching to historical day-length constants (e.g., 365.2425 vs. 365.25) to show sensitivity.

4) Symbol-Level Explanation — Why some symbols count differently
- Purpose: Visually explain ring-multipliers and special symbols (example: zone 12's symbol ×5 rings → 100).
- UI Input: Tap a single zone to zoom into symbol shapes and their ring counts.
- LED Pattern:
  - Light a single symbol slowly and display its ring multiplier as brighter concentric rings (if the LED array supports per-ring control); otherwise, use color/brightness to encode multiplier.
  - For symbols that are ornaments (not counted), light them at low brightness and display "not counted".
- On-screen Display:
  - Show the arithmetic: "20×5 = 100" with the 20 symbols numbered and the multiplier highlighted.
- Learning Objective: Clarify how individual symbols contribute to zone totals.
- Edge Cases: If the replica can't show per-ring differences, use color-coded small LEDs or per-symbol labels on-screen.

5) Venus Cycle Comparison (Schmidt-Kaler tie-in)
- Purpose: Compare Menghin's lunisolar reading with Schmidt-Kaler's Venus-cycle interpretation by lighting groupings that match Venus counts (292, 584, 2,920).
- UI Input: Toggle between "Lunar" and "Venus" interpretive overlays.
- LED Pattern:
  - For Venus overlay: highlight the bands whose sums equal 292 or 584 in gold/yellow; animate a 584-day sweep with a two-phase indicator (morning/evening).
  - For Lunar overlay: show Menghin zones and their sums.
- On-screen Display:
  - Side-by-side numeric comparison: "Grouping A = 584 days vs. Grouping B = 592 days; difference = 8 days" and explanatory text about observational/interpretive variance.
- Learning Objective: Demonstrate competing readings of the same artifact and how band groupings produce similar yet not identical astronomical cycles.

6) Educational Guided Tour
- Purpose: A guided script that walks the audience through the hat band-by-band, explains meaning, shows how to compute a lunar month, and demonstrates a full 54-month calculation with LEDs and text narration.
- UI Input: "Start tour"; optional step-forward/back controls for the presenter.
- LED Pattern:
  - For each tour step, light the current zone(s) in a unique color and pulse them while dimming previous zones.
  - Use soft transitions and a narrator voice (if speakers attached) or prerecorded audio clips.
- On-screen Display:
  - Show slide-like text with bullet points, numbers, and diagrams. Include "Why subtraction applies here" notes for intercalary zones.
- Learning Objective: Present a polished museum-grade explanation.
- Edge Cases: Add a "skip animation" toggle for faster demo pacing.

UI flow and controls
- Main menu (on-screen):
  - Scenarios: [54-month demo], [Interactive Range], [Metonic 19y], [Symbol Detail], [Venus comparison], [Guided Tour]
  - Controls: LED brightness, animation speed, day-per-tick speed, color palettes, language selection (EN/DE per your project)
  - Mapping: Tapping a zone on-screen selects that zone; hardware touch on the hat may map to nearest zone if sensors are available.

Hardware / Implementation notes
- LED driver choices:
  - For many LEDs (~3,400): prefer segmented LED strings with local level shifting and high-current power injection points. Consider multiple parallel data lines (several WS2812 chains) or use a dedicated LED driver IC per segment (e.g., TLC5940, LED matrix drivers, or smart LED drivers with chaining).
  - Ensure the microcontroller and wiring can supply the peak current; WS2812 at full white can draw ~60 mA per LED — plan for worst-case current and implement brightness limiting and per-zone power gating.
- Power budgeting:
  - For demo mode, limit brightness to safe levels (10–30%). At 3,400 LEDs and 30% brightness white worst-case approximation: 3400×60mA×0.3 ≈ 61 A (peak) — use dedicated power supplies and current-limiting.
- Physical segmentation:
  - Divide the hat into 21 addressable ring segments (one per zone) with accessible connectors.
  - For each zone, predefine `start_led_index` and `end_led_index` in the software table.
- Performance:
  - Update LED buffer in RAM; ensure the microcontroller (ESP32) has enough RAM — consider using multiple SPI-based LED drivers or small MCU front-ends per zone.
- Safety:
  - Include a watchdog and overheating/current-monitoring to prevent damage.

Tests and verification
- Unit test (software): Validate the `zone` → `symbol_count` table and arithmetic for representative ranges (e.g., 3..21 minus 5,16,17 should equal 1,597 days).
- Hardware smoke test: Light one LED in each zone sequentially and log the expected vs. actual LED indices.
- Integration demo test: Run the 54-month scenario and measure elapsed animation time vs. expected timeline.

Recommended next steps
1. Map the exact LED counts and ring multipliers into a JSON table the app reads at startup (example `goldhat_layout.json`).
2. Create a "Zone Map" debug UI that overlays LED indexes on the on-screen hat image for commissioning.
3. Implement the `Interactive Range Explorer` first — it's the core tool for demonstrating the counting behavior and will help calibrate the physical wiring and timings.
4. Add a "safe brightness" default and a hardware kill-switch for installers.
5. If desired, add audio narration and translate text to German (you already have EN/DE in the project).

Appendix A — Example `zone` table (from `gold_hat.md` counts)
```json
[
  {"zone":1,"count":17}, {"zone":2,"count":19}, {"zone":3,"count":29}, {"zone":4,"count":33},
  {"zone":5,"count":34}, {"zone":6,"count":29}, {"zone":7,"count":33}, {"zone":8,"count":34},
  {"zone":9,"count":33}, {"zone":10,"count":34}, {"zone":11,"count":33}, {"zone":12,"count":34},
  {"zone":13,"count":33}, {"zone":14,"count":34}, {"zone":15,"count":33}, {"zone":16,"count":34},
  {"zone":17,"count":33}, {"zone":18,"count":34}, {"zone":19,"count":33}, {"zone":20,"count":34},
  {"zone":21,"count":21}
]
```

Appendix B — Quick numeric checks (implement as unit tests)
- Sum zones 3..21 = 1,739
- Sum intercalaries 5+16+17 = 142
- 1,739 − 142 = 1,597 (54 × 29.5305 ≈ 1,593.64 — historical rounding; Menghin counts 1,597)

Appendix C — Glossary & references
- "Intercalary zone": a band whose symbols must be added/subtracted depending on the counted range.
- Menghin (2000, 2010): Berlin Gold Hat lunisolar calendar theory; see `gold_hat.md` for full references.

---

File generated by the assistant to propose demonstration scenarios. Adjust LED specifics and hardware choices to match your actual replica wiring and power constraints.
