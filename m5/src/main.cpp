#include <Arduino.h>

#include "M5GFX.h"
#include "M5Unified.h"
#include "config.h"
#include "scenarios.h"

uint32_t updateTime = 0; // time for next update

#define INTERVAL_SETUP 40000
uint32_t _timeoutSETUP = millis();
#define INTERVAL_BTN 100 // 1/10 of a second
uint32_t _timeoutBTN = millis();
#define INTERVAL_MS 40000 // 40 seconds
uint32_t _timeoutMS = millis();

M5GFX display;

#ifndef APP_VERSION
#define APP_VERSION "0.0.unknown"
#endif

void setup() {
  M5.begin();
  Serial.begin(115200);
  display.begin();
  display.startWrite();
  display.fillScreen(TFT_WHITE);
  display.endWrite();

  // Simple splash screen: centered "Berlin Goldhat" with version
  display.startWrite();
  display.setTextSize(3); // large text
  display.setTextDatum(textdatum_t::middle_center);
  display.setTextColor(TFT_BLACK, TFT_WHITE);
  int cx = display.width() / 2;
  int cy = display.height() / 2;
  display.drawCentreString("Berlin Goldhat", cx, cy - 8, nullptr);
  // smaller version text under the title
  display.setTextSize(1);
  display.setTextDatum(textdatum_t::middle_center);
  display.drawCentreString("v" APP_VERSION, cx, cy + 18, nullptr);
  display.endWrite();

  delay(1500); // show splash for 1.5s

  updateTime = millis(); // Next update time
  scenarios_init();
}
void loop() {
  M5.update();
  if (millis() - _timeoutMS > INTERVAL_MS) {
    _timeoutMS = millis();
    scenarios_update();
  }

  delay(10);
}