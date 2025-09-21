/* ABOUTME: Scenario 03 - Century lunar estimate
   ABOUTME: Computes and displays an approximate 100-year lunar months estimate.
 */

#include "app_locale.h"
#include "scenarios.h"

static void scenario_3_century_lunar_estimate_impl() {
  const double synodic_days = 29.530588;
  const int years = 100;
  const double days_per_year = 365.2425; // average
  double total_days = years * days_per_year;
  double months = total_days / synodic_days;

  draw_header(loc_scn_title_3());

  display.setTextColor(TFT_BLACK, TFT_WHITE);
  int y = 44;
  int line_h = 20;
  char buf[128];
  snprintf(buf, sizeof(buf), "Years: %d", years);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "Total days: %.0f", total_days);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), loc_scn_approx_months(), months);
  display.drawString(buf, 8, y);

  draw_footer();
}

static void scenario_3_century_lunar_estimate() {
  scenario_3_century_lunar_estimate_impl();
}
STATIC_REGISTER_SCENARIO("Century estimate: 100y",
                         scenario_3_century_lunar_estimate);
