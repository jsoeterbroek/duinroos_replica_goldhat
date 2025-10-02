/* ABOUTME: Scenario - Hardware LED strip test
   ABOUTME: Drives an SK6812 strip (30 LEDs) connected to Port A data pin (G2).
   ABOUTME: Cycles all LEDs red for 5s, then blue for 5s, green for 5s,
   repeating a few times at different brightness levels.
 */

#include "M5Unified.h"
#include "config.h"
#include "scenarios.h"
#include <FastLED.h>

// Adjust these if your strip differs
#define NUM_LEDS 30
#define DATA_PIN PORTA_PIN_1 // Port A, pin mapped in include/config.h (G2)
#define LED_TYPE SK6812
#define COLOR_ORDER GRB
#define BRIGHTNESS_LOW 64
#define BRIGHTNESS_HIGH 128
#define BRIGHTNESS_MAX 255

static void scenario_led_strip_impl() {
  static bool initialized = false;
  static CRGB leds[NUM_LEDS];

  if (!initialized) {
    FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS)
        .setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(BRIGHTNESS_LOW);
    initialized = true;
    Serial.printf("scenario_led_strip: initialized data_pin=%d num=%d\n",
                  DATA_PIN, NUM_LEDS);
  }

  // Run continuously until user intervenes (touch or button A)
  Serial.println("scenario_led_strip: entering continuous demo");
  while (true) {

    // // All red low brightness
    // fill_solid(leds, NUM_LEDS, CRGB::Red);
    // FastLED.setBrightness(BRIGHTNESS_LOW);
    // FastLED.show();
    // Serial.println("scenario_led_strip: color=RED, brightness=LOW");
    // for (int ms = 0; ms < 5000; ms += 200) {
    //   delay(200);
    // }
    // // All blue low brightness
    // fill_solid(leds, NUM_LEDS, CRGB::Blue);
    // FastLED.setBrightness(BRIGHTNESS_LOW);
    // FastLED.show();
    // Serial.println("scenario_led_strip: color=BLUE, brightness=LOW");
    // for (int ms = 0; ms < 5000; ms += 200) {
    //   delay(200);
    // }
    // // All green low brightness
    // fill_solid(leds, NUM_LEDS, CRGB::Green);
    // FastLED.setBrightness(BRIGHTNESS_LOW);
    // FastLED.show();
    // Serial.println("scenario_led_strip: color=GREEN, brightness=LOW");
    // for (int ms = 0; ms < 5000; ms += 200) {
    //   delay(200);
    // }

    // All red HIGH brightness
    fill_solid(leds, NUM_LEDS, CRGB::Red);
    FastLED.setBrightness(BRIGHTNESS_HIGH);
    FastLED.show();
    Serial.println("scenario_led_strip: color=RED, brightness=HIGH");
    for (int ms = 0; ms < 5000; ms += 200) {
      delay(200);
    }
    // All blue HIGH brightness
    fill_solid(leds, NUM_LEDS, CRGB::Blue);
    FastLED.setBrightness(BRIGHTNESS_HIGH);
    FastLED.show();
    Serial.println("scenario_led_strip: color=BLUE, brightness=HIGH");
    for (int ms = 0; ms < 5000; ms += 200) {
      delay(200);
    }
    // All green HIGH brightness
    fill_solid(leds, NUM_LEDS, CRGB::Green);
    FastLED.setBrightness(BRIGHTNESS_HIGH);
    FastLED.show();
    Serial.println("scenario_led_strip: color=GREEN, brightness=HIGH");
    for (int ms = 0; ms < 5000; ms += 200) {
      delay(200);
    }
    // All red MAX brightness
    fill_solid(leds, NUM_LEDS, CRGB::Red);
    FastLED.setBrightness(BRIGHTNESS_MAX);
    FastLED.show();
    Serial.println("scenario_led_strip: color=RED, brightness=MAX");
    for (int ms = 0; ms < 5000; ms += 200) {
      delay(200);
    }
    // All blue MAX brightness
    fill_solid(leds, NUM_LEDS, CRGB::Blue);
    FastLED.setBrightness(BRIGHTNESS_MAX);
    FastLED.show();
    Serial.println("scenario_led_strip: color=BLUE, brightness=MAX");
    for (int ms = 0; ms < 5000; ms += 200) {
      delay(200);
    }
    // All green MAX brightness
    fill_solid(leds, NUM_LEDS, CRGB::Green);
    FastLED.setBrightness(BRIGHTNESS_MAX);
    FastLED.show();
    Serial.println("scenario_led_strip: color=GREEN, brightness=MAX");
    for (int ms = 0; ms < 5000; ms += 200) {
      delay(200);
    }
  }

LED_STRIP_EXIT:

  // Turn off
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();

  // Draw a simple confirmation on the display
  display.startWrite();
  draw_header("LED strip test");
  display.setTextSize(2);
  display.setTextDatum(textdatum_t::middle_center);
  display.drawCentreString("Done", display.width() / 2, display.height() / 2,
                           nullptr);
  draw_footer();
  display.endWrite();

  Serial.println("scenario_led_strip: completed");
  delay(500);
}

static void scenario_led_strip() { scenario_led_strip_impl(); }
STATIC_REGISTER_SCENARIO("HW: LED strip test", scenario_led_strip);
