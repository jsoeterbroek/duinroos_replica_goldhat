/* ABOUTME: Scenario - Hardware LED strip test
   ABOUTME: Drives an SK6812 strip connected to Port A data pin (G2).
   ABOUTME: Cycles all LEDs red for 5s, then blue for 5s, green for 5s.
 */

#include "M5Unified.h"
#include "config.h"
#include "led_mapper.h"
#include "scenarios.h"
#include <FastLED.h>

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

  // Run continuously
  Serial.println(
      "scenario_led_strip: entering zone-based demo (parallel zones)");
  while (true) {
    // Define the sequence of colors and brightness levels to cycle per zone
    const CRGB colors[] = {CRGB::Red, CRGB::Blue, CRGB::Green};
    // const uint8_t brightness_levels[] = {BRIGHTNESS_HIGH, BRIGHTNESS_MAX};
    const uint8_t brightness_levels[] = {BRIGHTNESS_MAX};
    const size_t n_colors = sizeof(colors) / sizeof(colors[0]);
    const size_t n_brights =
        sizeof(brightness_levels) / sizeof(brightness_levels[0]);

    // Cycle all zones in parallel.
    for (size_t b = 0; b < n_brights; ++b) {
      FastLED.setBrightness(brightness_levels[b]);
      size_t idx3 = 0;
      size_t idx4 = 1;
      size_t idx5 = 2;
      size_t idx6 = 0;
      size_t idx7 = 1;
      size_t idx8 = 2;
      size_t idx9 = 0;
      // Perform enough cycles to show each color in all zones
      for (size_t step = 0; step < n_colors; ++step) {
        setZoneColor(leds, zone3, colors[idx3]);
        setZoneColor(leds, zone4, colors[idx4]);
        setZoneColor(leds, zone5, colors[idx5]);
        setZoneColor(leds, zone6, colors[idx6]);
        // setZoneColor(leds, zone7, colors[idx7]);
        // setZoneColor(leds, zone8, colors[idx8]);
        // setZoneColor(leds, zone9, colors[idx9]);
        FastLED.show();
        Serial.printf("scenario_led_strip: zone3 color=%d brightness=%d\n",
                      (int)idx3, (int)brightness_levels[b]);
        Serial.printf("scenario_led_strip: zone4 color=%d brightness=%d\n",
                      (int)idx4, (int)brightness_levels[b]);
        Serial.printf("scenario_led_strip: zone5 color=%d brightness=%d\n",
                      (int)idx5, (int)brightness_levels[b]);
        Serial.printf("scenario_led_strip: zone6 color=%d brightness=%d\n",
                      (int)idx6, (int)brightness_levels[b]);
        // Serial.printf("scenario_led_strip: zone7 color=%d brightness=%d\n",
        //               (int)idx7, (int)brightness_levels[b]);
        // Serial.printf("scenario_led_strip: zone8 color=%d brightness=%d\n",
        //               (int)idx8, (int)brightness_levels[b]);
        // Serial.printf("scenario_led_strip: zone9 color=%d brightness=%d\n",
        //               (int)idx9, (int)brightness_levels[b]);

        // Also draw the zone status to the display: label + small colored
        // circle
        display.startWrite();
        draw_header("LED strip test");
        // Clear a small rectangle in the top-left where we draw the status
        const int ox = 6;
        const int oy = 46;
        const int status_w = 120;
        const int status_h = 114;
        // display.fillRect(ox - 2, oy - 2, status_w, status_h, TFT_WHITE);
        display.setTextSize(1);
        // text color black on white background
        display.setTextColor(TFT_BLACK, TFT_WHITE);
        int y = oy;
        const int lineh = 14;

        // zone3
        uint16_t col3 =
            display.color565(colors[idx3].r, colors[idx3].g, colors[idx3].b);
        display.fillCircle(ox + 6, y + 6, 5, col3);
        display.drawString("zone 3", ox + 16, y);
        y += lineh;

        // zone4
        uint16_t col4 =
            display.color565(colors[idx4].r, colors[idx4].g, colors[idx4].b);
        display.fillCircle(ox + 6, y + 6, 5, col4);
        display.drawString("zone 4", ox + 16, y);
        y += lineh;

        // zone5
        uint16_t col5 =
            display.color565(colors[idx5].r, colors[idx5].g, colors[idx5].b);
        display.fillCircle(ox + 6, y + 6, 5, col5);
        display.drawString("zone 5", ox + 16, y);
        y += lineh;

        // zone6
        uint16_t col6 =
            display.color565(colors[idx6].r, colors[idx6].g, colors[idx6].b);
        display.fillCircle(ox + 6, y + 6, 5, col6);
        display.drawString("zone 6", ox + 16, y);
        y += lineh;

        // // zone7
        // uint16_t col7 =
        //     display.color565(colors[idx7].r, colors[idx7].g, colors[idx7].b);
        // display.fillCircle(ox + 6, y + 6, 5, col7);
        // display.drawString("zone 7", ox + 16, y);
        // y += lineh;

        // // zone8
        // uint16_t col8 =
        //     display.color565(colors[idx8].r, colors[idx8].g, colors[idx8].b);
        // display.fillCircle(ox + 6, y + 6, 5, col8);
        // display.drawString("zone 8", ox + 16, y);
        // y += lineh;

        // // zone9
        // uint16_t col9 =
        //     display.color565(colors[idx9].r, colors[idx9].g, colors[idx9].b);
        // display.fillCircle(ox + 6, y + 6, 5, col9);
        // display.drawString("zone 9", ox + 16, y);

        draw_footer();
        display.endWrite();

        // show for 5s
        delay(5000);

        // advance indices
        idx3 = (idx3 + 1) % n_colors;
        idx4 = (idx4 + 1) % n_colors;
        idx5 = (idx5 + 1) % n_colors;
        idx6 = (idx6 + 1) % n_colors;
        // idx7 = (idx7 + 1) % n_colors;
        // idx8 = (idx8 + 1) % n_colors;
        // idx9 = (idx9 + 1) % n_colors;
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
