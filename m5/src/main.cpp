#include <Arduino.h>

#include "M5GFX.h"
#include "M5Unified.h"
#include "app_locale.h"
#include "config.h"
#include "leds.h"
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

  // After splash: ask user for language selection (A = English, B = German)
  display.startWrite();
  display.fillScreen(TFT_WHITE);
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  display.setTextColor(TFT_BLACK, TFT_WHITE);
  display.drawCentreString(loc_choose_language(), display.width() / 2,
                           display.height() / 2 - 12, nullptr);
  // display.setTextSize(1);
  // display.drawCentreString(loc_option_english(), display.width() / 2,
  //                          display.height() / 2 + 4, nullptr);
  // display.drawCentreString(loc_option_german(), display.width() / 2,
  //                          display.height() / 2 + 22, nullptr);
  display.endWrite();

  // wait for touch selection: left = English, right = German
  uint32_t choice_start = millis();
  bool chosen = false;
  // debug: report whether touch interface is available
  if (!display.touch()) {
    Serial.println("Touch interface not available (display.touch() == false)");
  } else {
    Serial.println("Touch interface available");
  }
  // Draw two selectable panels
  display.startWrite();
  int w = display.width();
  int h = display.height();
  int pad = 12;
  int box_w = (w - 3 * pad) / 2;
  int box_h = 60;
  int x1 = pad;
  int y1 = h / 2 + 30;
  int x2 = pad * 2 + box_w;
  display.drawRect(x1, y1, box_w, box_h, TFT_BLACK);
  display.drawRect(x2, y1, box_w, box_h, TFT_BLACK);
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  display.drawCentreString(loc_option_english(), x1 + box_w / 2,
                           y1 + box_h / 2 - 6, nullptr);
  display.drawCentreString(loc_option_german(), x2 + box_w / 2,
                           y1 + box_h / 2 - 6, nullptr);
  display.endWrite();

  while (!chosen && (millis() - choice_start) < 10000) {
    M5.update();
    // check touch
    int tcount = M5.Touch.getCount();
    if (tcount > 0) {
      auto d = M5.Touch.getDetail(0);
      int tx = d.x;
      int ty = d.y;
      Serial.print("Touch count: ");
      Serial.print(tcount);
      Serial.print(" id:");
      Serial.print(d.id);
      Serial.print(" x:");
      Serial.print(tx);
      Serial.print(" y:");
      Serial.println(ty);
      if (tx >= x1 && tx <= x1 + box_w && ty >= y1 && ty <= y1 + box_h) {
        // visual feedback: fill left box and invert text
        display.startWrite();
        display.fillRect(x1 + 1, y1 + 1, box_w - 2, box_h - 2, TFT_BLACK);
        display.setTextColor(TFT_WHITE, TFT_BLACK);
        display.drawCentreString(loc_option_english(), x1 + box_w / 2,
                                 y1 + box_h / 2 - 6, nullptr);
        display.endWrite();
        app_locale_set(AppLocale::EN);
        Serial.println("English selected");
        chosen = true;
        delay(200); // allow user to see feedback
        break;
      }
      if (tx >= x2 && tx <= x2 + box_w && ty >= y1 && ty <= y1 + box_h) {
        // visual feedback: fill right box and invert text
        display.startWrite();
        display.fillRect(x2 + 1, y1 + 1, box_w - 2, box_h - 2, TFT_BLACK);
        display.setTextColor(TFT_WHITE, TFT_BLACK);
        display.drawCentreString(loc_option_german(), x2 + box_w / 2,
                                 y1 + box_h / 2 - 6, nullptr);
        display.endWrite();
        app_locale_set(AppLocale::DE);
        Serial.println("German selected");
        chosen = true;
        delay(200); // allow user to see feedback
        break;
      }
    }
    delay(20);
  }

  // default to English if nothing chosen
  if (!chosen) {
    app_locale_set(AppLocale::EN);
    Serial.println("No selection: defaulting to English");
  }

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