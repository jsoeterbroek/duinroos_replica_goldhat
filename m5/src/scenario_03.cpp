/* ABOUTME: Scenario 03 - Century lunar estimate
   ABOUTME: Computes and displays an approximate 100-year lunar months estimate.
 */

#include "scenarios.h"

static void scenario_3_century_lunar_estimate_impl() {
  const double synodic_days = 29.530588;
  const int years = 100;
  const double days_per_year = 365.2425; // average
  double total_days = years * days_per_year;
  double months = total_days / synodic_days;

  draw_header("Century estimate: 100y", 2, 3);

  display.setTextColor(TFT_BLACK, TFT_WHITE);
  int y = 44;
  int line_h = 20;
  char buf[64];
  snprintf(buf, sizeof(buf), "Years: %d", years);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "Total days: %.0f", total_days);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "Approx months: %.2f", months);
  display.drawString(buf, 8, y);

  draw_footer(2, 3);
}

extern "C" void scenario_3_century_lunar_estimate() {
  scenario_3_century_lunar_estimate_impl();
}
