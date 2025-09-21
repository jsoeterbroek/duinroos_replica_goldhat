/* ABOUTME: Scenario - Wikipedia 54 lunar months verification
   ABOUTME: Computes canonical 54-month days using goldhat helper and shows
   result on-screen and Serial. */

#include "M5Unified.h"
#include "cal_goldhat.h"
#include "led_mapper.h"
#include "scenarios.h"
#include <Arduino.h>

static void scenario_54_lunar_impl() {
  int days = goldhat_days_54_lunar_months();
  display.startWrite();
  draw_header("54 lunar months");
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  char buf[64];
  snprintf(buf, sizeof(buf), "days = %d", days);
  display.drawCentreString(buf, display.width() / 2, display.height() / 2,
                           nullptr);
  draw_footer();
  display.endWrite();
  Serial.printf("scenario_54_lunar: days=%d\n", days);
  delay(500); // keep the screen stable for a short time
}

static void scenario_54_lunar() { scenario_54_lunar_impl(); }
STATIC_REGISTER_SCENARIO("54 lunar months", scenario_54_lunar);
