/* ABOUTME: Scenario management implementation
   ABOUTME: Implements a simple carousel of scenarios. */

#include "scenarios.h"
#include "M5Unified.h"
#include <Arduino.h>
#include <string>
#include <vector>

static uint32_t scenario_start_ms = 0;
static int current_scenario = 0;
static const uint32_t scenario_duration_ms = 8000; // show each scenario 8s

// internal registry entry
struct scenario_entry_t {
  const char *title;
  scenario_fn_t fn;
};

// simple static registry (order of registration follows static init order)
static std::vector<scenario_entry_t> &get_registry() {
  static std::vector<scenario_entry_t> registry;
  return registry;
}

int register_scenario(const char *title, scenario_fn_t fn) {
  auto &reg = get_registry();
  reg.push_back({title, fn});
  return (int)reg.size() - 1;
}

// layout helpers
void draw_header(const char *title, int index, int total) {
  display.startWrite();
  display.fillScreen(TFT_WHITE);
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  display.setTextColor(TFT_BLACK, TFT_WHITE);
  display.drawCentreString(title, display.width() / 2, 18, nullptr);
  // separator line
  int y = 40;
  display.drawFastHLine(4, y, display.width() - 8, TFT_BLACK);
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::top_left);
}

void draw_footer(int index, int total) {
  char buf[16];
  snprintf(buf, sizeof(buf), "%d/%d", index + 1, total);
  display.setTextDatum(textdatum_t::bottom_right);
  display.drawString(buf, display.width() - 6, display.height() - 6);
  display.endWrite();
}

void scenarios_init() {
  scenario_start_ms = millis();
  current_scenario = 0; // start with first registered scenario
  // Debug: print loaded scenarios to Serial
  auto &reg = get_registry();
  Serial.printf("scenarios: loaded %d scenarios\n", (int)reg.size());
  for (size_t i = 0; i < reg.size(); ++i) {
    Serial.printf("scenarios: [%zu] %s\n", i, reg[i].title);
  }
}

void scenarios_update() {
  uint32_t now = millis();
  auto &reg = get_registry();
  int total = (int)reg.size();
  if (total == 0)
    return; // nothing registered

  if (now - scenario_start_ms >= scenario_duration_ms) {
    // next scenario
    current_scenario = (current_scenario + 1) % total;
    scenario_start_ms = now;
  }

  // call the registered scenario function
  auto &entry = reg[current_scenario];
  if (entry.fn) {
    entry.fn();
  }
}

// scenario implementations are in separate files and should use
// STATIC_REGISTER_SCENARIO macro to register themselves at startup.
