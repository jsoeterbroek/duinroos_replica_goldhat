/* ABOUTME: Scenario 02 - Metonic 19 years
   ABOUTME: Computes and displays Metonic 19-year cycle summary. */

#include "scenarios.h"

static void scenario_2_metonic_19_years_impl() {
  const double synodic_days = 29.530588;
  const int years = 19;
  const int months = 235; // Metonic: 19 solar years ~= 235 synodic months
  double total_days = synodic_days * months;

  draw_header("Metonic: 19 years", 1, 3);

  display.setTextColor(TFT_BLACK, TFT_WHITE);
  int y = 44;
  int line_h = 20;
  char buf[64];
  snprintf(buf, sizeof(buf), "Years: %d", years);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "Months (approx): %d", months);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "Total days: %.2f", total_days);
  display.drawString(buf, 8, y);

  draw_footer(1, 3);
}

extern "C" void scenario_2_metonic_19_years() {
  scenario_2_metonic_19_years_impl();
}
