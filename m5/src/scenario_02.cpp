/* ABOUTME: Scenario 02 - Metonic 19 years
   ABOUTME: Computes and displays Metonic 19-year cycle summary. */

#include "app_locale.h"
#include "scenarios.h"

static void scenario_2_metonic_19_years_impl() {
  const double synodic_days = 29.530588;
  const int years = 19;
  const int months = 235; // Metonic: 19 solar years ~= 235 synodic months
  double total_days = synodic_days * months;

  draw_header(loc_scn_title_2());

  display.setTextColor(TFT_BLACK, TFT_WHITE);
  int y = 44;
  int line_h = 20;
  char buf[128];
  snprintf(buf, sizeof(buf), loc_scn_years(), years);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), loc_scn_months_approx(), months);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), loc_scn_total_days(), total_days);
  display.drawString(buf, 8, y);

  draw_footer();
}

static void scenario_2_metonic_19_years() {
  scenario_2_metonic_19_years_impl();
}
// STATIC_REGISTER_SCENARIO("Metonic: 19 years", scenario_2_metonic_19_years);
