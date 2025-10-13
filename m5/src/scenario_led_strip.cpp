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
// #define NUM_LEDS 30
#define NUM_LEDS 25
#define DATA_PIN PORTA_PIN_1 // Port A, pin mapped in include/config.h (G2)
#define LED_TYPE SK6812
#define COLOR_ORDER GRB
#define BRIGHTNESS_LOW 64
#define BRIGHTNESS_HIGH 128
#define BRIGHTNESS_MAX 255

// Zone definitions: first 7 LEDs are zone 4, remaining 8 are zone 5
struct LedZone {
  const char *name;
  uint16_t start;  // inclusive start index
  uint16_t length; // number of LEDs in zone
};

static const LedZone zone4 = {"zone4", 0, 7};
// static const LedZone zone5 = {"zone5", 7, (uint16_t)(NUM_LEDS - 7)};
static const LedZone zone5 = {"zone5", 7, 15};
static const LedZone zone6 = {"zone6", 15, 25};

// Helper: set all LEDs in a zone to a color
static void setZoneColor(CRGB leds[], const LedZone &z, const CRGB &color) {
  for (uint16_t i = z.start; i < z.start + z.length && i < NUM_LEDS; ++i) {
    leds[i] = color;
  }
}

// Helper: clear a zone (set to black)
static void clearZone(CRGB leds[], const LedZone &z) {
  for (uint16_t i = z.start; i < z.start + z.length && i < NUM_LEDS; ++i) {
    leds[i] = CRGB::Black;
  }
}

// (No touch-to-exit) demo runs until scenario is interrupted by the app

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

  // Run continuously until user intervenes (touch)
  Serial.println(
      "scenario_led_strip: entering zone-based demo (parallel zones)");
  while (true) {
    // Define the sequence of colors and brightness levels to cycle per zone
    const CRGB colors[] = {CRGB::Red, CRGB::Blue, CRGB::Green};
    const uint8_t brightness_levels[] = {BRIGHTNESS_HIGH, BRIGHTNESS_MAX};
    const size_t n_colors = sizeof(colors) / sizeof(colors[0]);
    const size_t n_brights =
        sizeof(brightness_levels) / sizeof(brightness_levels[0]);

    // Cycle both zones in parallel. Start zone5 one step ahead so they differ.
    for (size_t b = 0; b < n_brights; ++b) {
      FastLED.setBrightness(brightness_levels[b]);
      size_t idx4 = 0;
      size_t idx5 = (n_colors > 1) ? 1 : 0; // offset so colors differ initially
      size_t idx6 = (n_colors > 1) ? 1 : 0; // offset so colors differ initially
      // Perform enough cycles to show each color in both zones
      for (size_t step = 0; step < n_colors; ++step) {
        setZoneColor(leds, zone4, colors[idx4]);
        setZoneColor(leds, zone5, colors[idx5]);
        setZoneColor(leds, zone6, colors[idx6]);
        FastLED.show();
        Serial.printf("scenario_led_strip: zone4 color=%d brightness=%d\n",
                      (int)idx4, (int)brightness_levels[b]);
        Serial.printf("scenario_led_strip: zone5 color=%d brightness=%d\n",
                      (int)idx5, (int)brightness_levels[b]);
        Serial.printf("scenario_led_strip: zone6 color=%d brightness=%d\n",
                      (int)idx6, (int)brightness_levels[b]);

        // show for 5s
        delay(5000);

        // advance indices
        idx4 = (idx4 + 1) % n_colors;
        idx5 = (idx5 + 1) % n_colors;
      }
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
