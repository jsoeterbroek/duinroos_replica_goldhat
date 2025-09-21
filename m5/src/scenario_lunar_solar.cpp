/* ABOUTME: Lunar-Solar scenario
   ABOUTME: Demonstrates converting between lunar and solar calendar counts
   using the gold-hat layout. */

#include "M5Unified.h"
#include "led_mapper.h"
#include "scenarios.h"
#include "virtual_leds.h"
#include <Arduino.h>
#include <vector>

static void scenario_lunar_solar();
STATIC_REGISTER_SCENARIO("Lunar↔Solar: conversion", scenario_lunar_solar);

// canonical intercalary zones per gold_hat.md
static const std::vector<int> intercalary_zones = {5, 16, 17};

static void draw_calc_step(const char *line) {
  display.startWrite();
  display.setTextSize(1);
  display.setTextDatum(textdatum_t::top_left);
  display.drawString(line, 6, 48);
  display.endWrite();
}

static void highlight_ranges(const std::vector<std::pair<int, int>> &ranges,
                             uint32_t color) {
  // For now just log indices and print a placeholder rectangle per zone to
  // indicate activity
  for (auto &r : ranges) {
    Serial.printf("Highlight LEDs %d..%d color 0x%08x\n", r.first, r.second,
                  color);
    display.startWrite();
    // draw a thin bar per range (visualization only)
    int y = 60 + (r.first % 6) * 8;
    display.fillRect(6, y, display.width() - 12, 6, color);
    display.endWrite();
  }
}

void scenario_lunar_solar() {
  // Draw header
  draw_header("Lunar↔Solar conversion", 0, 1);

  // Ensure layout loaded
  static bool layout_loaded = false;
  if (!layout_loaded) {
    load_goldhat_layout("/goldhat_layout.json");
    layout_loaded = true;
  }

  // canonical example: zones 3..21
  int sum_all = sum_zone_range(3, 21);
  int sum_inter = sum_intercalaries(intercalary_zones);
  int result = sum_all - sum_inter;

  char buf[64];
  snprintf(buf, sizeof(buf), "Sum zones 3..21 = %d", sum_all);
  draw_calc_step(buf);
  snprintf(buf, sizeof(buf), "Intercalaries (5,16,17) = %d", sum_inter);
  draw_calc_step(buf);
  snprintf(buf, sizeof(buf), "Result = %d days -> 54 synodic months", result);
  draw_calc_step(buf);

  // Visualize included ranges (green) and intercalaries (red) via virtual LEDs
  auto ranges = map_zone_range_to_led_ranges(3, 21);
  auto inter_ranges = std::vector<std::pair<int, int>>();
  for (int z : intercalary_zones) {
    auto r = map_zone_range_to_led_ranges(z, z);
    for (auto &p : r)
      inter_ranges.push_back(p);
  }

  static bool vinit = false;
  if (!vinit) {
    vled_init(display.width(), display.height());
    vinit = true;
  }

  vled_clear();
  // pulse included ranges green
  vled_pulse_range(ranges, 0x00ff00, 1500);
  // overlay intercalaries in red (no pulse for simplicity)
  for (auto &rg : inter_ranges) {
    for (int i = rg.first; i <= rg.second; i++)
      vled_set(i, {255, 0, 0});
  }
  vled_render();

  draw_footer(0, 1);
}
