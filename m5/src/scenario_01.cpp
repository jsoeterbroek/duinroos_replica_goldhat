/* ABOUTME: Scenario 01 - Lunar 54 months
   ABOUTME: Computes and displays a 54-month lunar cycle summary. */

#include "app_locale.h"
#include "scenarios.h"

static void scenario_1_lunar_54_months_impl() {
  const double synodic_days = 29.530588; // days per lunar month
  const int months = 54;
  double total_days = synodic_days * months;
  int years = (int)(total_days / 365.25);
  int days_rem = (int)round(total_days - years * 365.25);

  draw_header(loc_scn_title_1());

  display.setTextColor(TFT_BLACK, TFT_WHITE);
  int y = 44; // start below separator
  int line_h = 20;
  char buf[128];
  snprintf(buf, sizeof(buf), "%s %d", loc_scn_months(), months);
  display.drawString(buf, 8, y);
  y += line_h;

  snprintf(buf, sizeof(buf), "%s %.2f", loc_scn_total_days(), total_days);
  display.drawString(buf, 8, y);
  y += line_h;
  snprintf(buf, sizeof(buf), loc_scn_years_and_daysrem(), years, days_rem);
  display.drawString(buf, 8, y);

  draw_footer();
}

// register scenario automatically
static void scenario_1_lunar_54_months() { scenario_1_lunar_54_months_impl(); }
// STATIC_REGISTER_SCENARIO("Lunar: 54 months", scenario_1_lunar_54_months);
