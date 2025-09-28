#include <Arduino.h>

#include "M5GFX.h"
#include "M5Unified.h"
#include "app_locale.h"
#include "assets/flag_de.h"
#include "assets/flag_en.h"
#include "config.h"
#include "leds.h"
#include "scenarios.h"
#include <SPIFFS.h>

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
  // Try to mount SPIFFS so we can load image assets placed in data/
  bool spiffs_ready = false;
  if (SPIFFS.begin(true)) {
    spiffs_ready = true;
    Serial.println("SPIFFS mounted");
  } else {
    Serial.println("SPIFFS mount failed or not available");
  }
  // Draw two selectable flag buttons (English and German)
  display.startWrite();
  int w = display.width();
  int h = display.height();
  int pad = 12;
  int box_w = (w - 3 * pad) / 2;
  int box_h = 60;
  int x1 = pad;
  int y1 = h / 2 + 30;
  int x2 = pad * 2 + box_w;
  // English flag: prefer embedded bitmap when available and matches box size
  display.drawRect(x1, y1, box_w, box_h, TFT_BLACK);
  // Try loading PNG from SPIFFS first if available
  bool drew_en = false;
  if (spiffs_ready && SPIFFS.exists("/flag_uk.png")) {
    // drawPngFile will scale to maxWidth/maxHeight if provided
    drew_en = display.drawPngFile("/flag_uk.png", x1 + 1, y1 + 1, box_w - 2,
                                  box_h - 2);
    if (!drew_en) {
      Serial.println("drawPngFile for /flag_uk.png failed; falling back");
    }
  }
  if (!drew_en) {
    // fallback to embedded asset or vector drawing
#if defined(FLAG_EN_AVAILABLE) && FLAG_EN_AVAILABLE == 1
    if (box_w == FLAG_EN_W && box_h == FLAG_EN_H) {
      display.pushImage(x1 + 1, y1 + 1, box_w - 2, box_h - 2, FLAG_EN_PIXELS);
    } else
#endif
    {
      display.fillRect(x1 + 1, y1 + 1, box_w - 2, box_h - 2, TFT_NAVY);
      int cross_w = box_h / 5;
      display.fillRect(x1 + box_w / 2 - cross_w / 2, y1 + 4, cross_w, box_h - 8,
                       TFT_WHITE);
      display.fillRect(x1 + 4, y1 + box_h / 2 - cross_w / 2, box_w - 8, cross_w,
                       TFT_WHITE);
      int thin = max(1, cross_w / 3);
      display.fillRect(x1 + box_w / 2 - thin / 2, y1 + 4, thin, box_h - 8,
                       TFT_RED);
      display.fillRect(x1 + 4, y1 + box_h / 2 - thin / 2, box_w - 8, thin,
                       TFT_RED);
      int diag_thick = max(1, cross_w / 4);
      for (int t = -diag_thick; t <= diag_thick; ++t) {
        display.drawLine(x1 + 2 + t, y1 + 2, x1 + box_w - 3 + t, y1 + box_h - 3,
                         TFT_WHITE);
        display.drawLine(x1 + 2 + t, y1 + box_h - 3, x1 + box_w - 3 + t, y1 + 2,
                         TFT_WHITE);
      }
      int diag_thin = max(1, diag_thick / 3);
      for (int t = -diag_thin; t <= diag_thin; ++t) {
        display.drawLine(x1 + 2 + t, y1 + 2 + 1, x1 + box_w - 3 + t,
                         y1 + box_h - 3 - 1, TFT_RED);
        display.drawLine(x1 + 2 + t, y1 + box_h - 3 - 1, x1 + box_w - 3 + t,
                         y1 + 2 + 1, TFT_RED);
      }
      display.setTextSize(1);
      display.setTextDatum(textdatum_t::middle_center);
      display.setTextColor(TFT_WHITE, TFT_NAVY);
      display.drawCentreString("EN", x1 + box_w / 2, y1 + box_h - 12, nullptr);
    }
  }

  // German flag box (three horizontal bands). Prefer embedded bitmap when
  // available
  display.drawRect(x2, y1, box_w, box_h, TFT_BLACK);
  // Try loading PNG from SPIFFS first if available
  bool drew_de = false;
  if (spiffs_ready && SPIFFS.exists("/flag_de.png")) {
    drew_de = display.drawPngFile("/flag_de.png", x2 + 1, y1 + 1, box_w - 2,
                                  box_h - 2);
    if (!drew_de) {
      Serial.println("drawPngFile for /flag_de.png failed; falling back");
    }
  }
  if (!drew_de) {
#if defined(FLAG_DE_AVAILABLE) && FLAG_DE_AVAILABLE == 1
    if (box_w == FLAG_DE_W && box_h == FLAG_DE_H) {
      display.pushImage(x2 + 1, y1 + 1, box_w - 2, box_h - 2, FLAG_DE_PIXELS);
    } else
#endif
    {
      int band_h = (box_h - 2) / 3;
      display.fillRect(x2 + 1, y1 + 1, box_w - 2, band_h, TFT_BLACK);
      display.fillRect(x2 + 1, y1 + 1 + band_h, box_w - 2, band_h, TFT_RED);
      display.fillRect(x2 + 1, y1 + 1 + 2 * band_h, box_w - 2,
                       box_h - 2 - 2 * band_h, TFT_YELLOW);
      display.setTextSize(1);
      display.setTextDatum(textdatum_t::middle_center);
      display.setTextColor(TFT_BLACK, TFT_YELLOW);
      display.drawCentreString("DE", x2 + box_w / 2, y1 + box_h - 12, nullptr);
    }
  }

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
        // pressed-state: briefly invert colors of the left flag area
        display.startWrite();
        // draw inverted Union-jack-like pressed-state: white bg, blue bands,
        // red accents
        display.fillRect(x1 + 1, y1 + 1, box_w - 2, box_h - 2, TFT_WHITE);
        int inv_cross_w = box_h / 5;
        display.fillRect(x1 + box_w / 2 - inv_cross_w / 2, y1 + 4, inv_cross_w,
                         box_h - 8, TFT_NAVY);
        display.fillRect(x1 + 4, y1 + box_h / 2 - inv_cross_w / 2, box_w - 8,
                         inv_cross_w, TFT_NAVY);
        int inv_thin = max(1, inv_cross_w / 3);
        display.fillRect(x1 + box_w / 2 - inv_thin / 2, y1 + 4, inv_thin,
                         box_h - 8, TFT_RED);
        display.fillRect(x1 + 4, y1 + box_h / 2 - inv_thin / 2, box_w - 8,
                         inv_thin, TFT_RED);
        int inv_diag_thick = max(1, inv_cross_w / 4);
        for (int t = -inv_diag_thick; t <= inv_diag_thick; ++t) {
          display.drawLine(x1 + 2 + t, y1 + 2, x1 + box_w - 3 + t,
                           y1 + box_h - 3, TFT_NAVY);
          display.drawLine(x1 + 2 + t, y1 + box_h - 3, x1 + box_w - 3 + t,
                           y1 + 2, TFT_NAVY);
        }
        int inv_diag_thin = max(1, inv_diag_thick / 3);
        for (int t = -inv_diag_thin; t <= inv_diag_thin; ++t) {
          display.drawLine(x1 + 2 + t, y1 + 2 + 1, x1 + box_w - 3 + t,
                           y1 + box_h - 3 - 1, TFT_RED);
          display.drawLine(x1 + 2 + t, y1 + box_h - 3 - 1, x1 + box_w - 3 + t,
                           y1 + 2 + 1, TFT_RED);
        }
        display.setTextColor(TFT_BLACK, TFT_WHITE);
        display.drawCentreString(loc_option_english(), x1 + box_w / 2,
                                 y1 + box_h / 2 - 6, nullptr);
        display.endWrite();
        delay(120); // brief pressed-state
        app_locale_set(AppLocale::EN);
        Serial.println("English selected");
        chosen = true;
        break;
      }
      if (tx >= x2 && tx <= x2 + box_w && ty >= y1 && ty <= y1 + box_h) {
        // pressed-state: briefly invert colors of the right flag area
        display.startWrite();
        // invert German flag: white background with inverted bands
        display.fillRect(x2 + 1, y1 + 1, box_w - 2, box_h - 2, TFT_WHITE);
        int inv_band_h = (box_h - 2) / 3;
        display.fillRect(x2 + 1, y1 + 1, box_w - 2, inv_band_h, TFT_YELLOW);
        display.fillRect(x2 + 1, y1 + 1 + inv_band_h, box_w - 2, inv_band_h,
                         TFT_RED);
        display.fillRect(x2 + 1, y1 + 1 + 2 * inv_band_h, box_w - 2,
                         box_h - 2 - 2 * inv_band_h, TFT_BLACK);
        display.setTextColor(TFT_WHITE, TFT_BLACK);
        display.drawCentreString(loc_option_german(), x2 + box_w / 2,
                                 y1 + box_h / 2 - 6, nullptr);
        display.endWrite();
        delay(120); // brief pressed-state
        app_locale_set(AppLocale::DE);
        Serial.println("German selected");
        chosen = true;
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