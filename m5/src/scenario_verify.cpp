/* ABOUTME: Verification scenario
   ABOUTME: Runs canonical numeric checks (from gold_hat.md) and displays
   PASS/FAIL. */

#include "M5Unified.h"
#include "led_mapper.h"
#include "scenarios.h"
#include <Arduino.h>

static void scenario_verify();
STATIC_REGISTER_SCENARIO("Verify canonical sums", scenario_verify);

static void show_result(bool ok, const char *msg) {
  display.startWrite();
  display.fillScreen(ok ? TFT_GREEN : TFT_RED);
  display.setTextColor(TFT_BLACK, ok ? TFT_GREEN : TFT_RED);
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  display.drawCentreString(msg, display.width() / 2, display.height() / 2,
                           nullptr);
  display.endWrite();
}

void scenario_verify() {
  draw_header("Verify: canonical examples", 0, 1);
  static bool layout_loaded = false;
  if (!layout_loaded) {
    load_goldhat_layout("/berlin.json");
    layout_loaded = true;
  }

  int sum_3_21 = sum_zone_range(3, 21);
  int inter = sum_intercalaries(std::vector<int>({5, 16, 17}));
  int result = sum_3_21 - inter;

  bool pass = (sum_3_21 == 1739) && (inter == 142) && (result == 1597);
  Serial.printf("verify: sum=%d inter=%d result=%d pass=%d\n", sum_3_21, inter,
                result, pass);

  if (pass) {
    show_result(true, "VERIFIED");
  } else {
    char buf[64];
    snprintf(buf, sizeof(buf), "sum=%d inter=%d res=%d", sum_3_21, inter,
             result);
    show_result(false, buf);
  }

  draw_footer(0, 5);
}
