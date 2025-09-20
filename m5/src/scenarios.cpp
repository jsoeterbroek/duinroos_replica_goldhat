/* ABOUTME: Scenario management implementation
   ABOUTME: Implements a simple carousel of scenarios. */

#include "scenarios.h"
#include "M5Unified.h"
#include <Arduino.h>

static uint32_t scenario_start_ms = 0;
static int current_scenario = 0;
static const uint32_t scenario_duration_ms = 8000; // show each scenario 8s

// forward declarations for scenarios (implemented in separate files)
extern void scenario_1_lunar_54_months();
extern void scenario_2_metonic_19_years();
extern void scenario_3_century_lunar_estimate();

// layout helpers
void draw_header(const char *title, int index, int total) {
  display.startWrite();
  display.fillScreen(TFT_WHITE);
  display.setTextSize(3);
  display.setTextDatum(textdatum_t::middle_center);
  display.setTextColor(TFT_BLACK, TFT_WHITE);
  display.drawCentreString(title, display.width() / 2, 18, nullptr);
  // separator line
  int y = 36;
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
  current_scenario = 0; // start with scenario 1
}

void scenarios_update() {
  uint32_t now = millis();
  if (now - scenario_start_ms >= scenario_duration_ms) {
    // next scenario
    current_scenario =
        (current_scenario + 1) % 3; // rotate through three scenarios
    scenario_start_ms = now;
  }

  switch (current_scenario) {
  case 0:
    scenario_1_lunar_54_months();
    break;
  case 1:
    scenario_2_metonic_19_years();
    break;
  case 2:
    scenario_3_century_lunar_estimate();
    break;
  default:
    scenario_1_lunar_54_months();
    break;
  }
}

// scenario implementations moved to separate files: scenario_01.cpp,
// scenario_02.cpp, scenario_03.cpp
