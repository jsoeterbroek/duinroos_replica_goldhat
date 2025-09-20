/* ABOUTME: Scenario 01 - Lunar 54 months
   ABOUTME: Computes and displays a 54-month lunar cycle summary. */

#include "scenarios.h"

static void scenario_1_lunar_54_months_impl() {
  const double synodic_days = 29.530588; // days per lunar month
  const int months = 54;
  double total_days = synodic_days * months;
  int years = (int)(total_days / 365.25);
  int days_rem = (int)round(total_days - years * 365.25);

  draw_header("Lunar: 54 months", 0, 3);

  display.setTextColor(TFT_BLACK, TFT_WHITE);
  int y = 44; // start below separator
  int line_h = 20;
  char buf[64];
  snprintf(buf, sizeof(buf), "Months: %d", months);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "Total days: %.2f", total_days);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "~Years: %d, ~Days rem: %d", years, days_rem);
  display.drawString(buf, 8, y);

  draw_footer(0, 3);
}

// register scenario automatically
static void scenario_1_lunar_54_months() { scenario_1_lunar_54_months_impl(); }
STATIC_REGISTER_SCENARIO("Lunar: 54 months", scenario_1_lunar_54_months);
