/* ABOUTME: Scenario - Goldhat zone formatting
   ABOUTME: Formats the Goldhat zone for 2025-05-22 and shows it on-screen and
   Serial. */

#include "M5Unified.h"
#include "cal_goldhat.h"
#include "cal_gregorian.h"
#include "scenarios.h"
#include <Arduino.h>
#include <string>

static void scenario_zone_impl() {
  double jd = gregorian_to_jd(2025, 9, 21);
  std::string zone = format_goldhat_zone(jd, GoldHats::Berlin);
  display.startWrite();
  draw_header("Goldhat zone (2025-09-21)");
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  display.drawCentreString(zone.c_str(), display.width() / 2,
                           display.height() / 2, nullptr);
  draw_footer();
  display.endWrite();
  Serial.printf("scenario_zone: zone=%s\n", zone.c_str());
  delay(500);
}

static void scenario_zone() { scenario_zone_impl(); }
STATIC_REGISTER_SCENARIO("Goldhat zone (2025-05-22)", scenario_zone);
