/* ABOUTME: Scenario - Venus day in cycle
   ABOUTME: Computes Venus day in cycle for 2025-05-22 and displays result.
 */

#include "M5Unified.h"
#include "cal_gregorian.h"
#include "scenarios.h"
#include "venus.h"
#include <Arduino.h>

static void scenario_venus_impl() {
  double jd = gregorian_to_jd(2025, 5, 22);
  int vd = venus::day_in_cycle(jd);
  display.startWrite();
  draw_header("Venus day");
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  char buf[64];
  snprintf(buf, sizeof(buf), "venus_day = %d", vd);
  display.drawCentreString(buf, display.width() / 2, display.height() / 2,
                           nullptr);
  draw_footer();
  display.endWrite();
  Serial.printf("scenario_venus: venus_day=%d\n", vd);
  delay(500);
}

static void scenario_venus() { scenario_venus_impl(); }
STATIC_REGISTER_SCENARIO("Venus day (2025-05-22)", scenario_venus);
