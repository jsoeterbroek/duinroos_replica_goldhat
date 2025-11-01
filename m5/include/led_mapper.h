/* ABOUTME: LED mapper header
   ABOUTME: Maps logical gold-hat zones and symbols to LED indices. */
#pragma once

#include <FastLED.h>
#include <stdint.h>
#include <vector>

struct zone_t {
  int zone;          // 1..21
  int count;         // number of symbols
  int start_index;   // first LED index in global LED array (inclusive)
  int end_index;     // last LED index (inclusive)
  int multiplier;    // rings multiplier (default 1)
  int special_value; // optional fixed value for special symbols (0=none)
};

// Load layout from JSON file on disk; returns false on failure
// If `path` is null, loader will use embedded layout JSON. Returns false on
// failure.
bool load_goldhat_layout(const char *path);

// Compute numeric day-value for a zone (count * multiplier) + special_value
int zone_value(const zone_t &z);

// Query functions
const std::vector<zone_t> &get_zones();
int sum_zone_range(int start_zone, int end_zone);
int sum_intercalaries(const std::vector<int> &zones);

// Map a zone range to LED index ranges (pairs of start,end) for animation
std::vector<std::pair<int, int>> map_zone_range_to_led_ranges(int start_zone,
                                                              int end_zone);

#define DATA_PIN PORTA_PIN_1 // Port A, pin mapped in include/config.h (G2)
#define LED_TYPE SK6812
#define COLOR_ORDER GRB
#define BRIGHTNESS_LOW 64
#define BRIGHTNESS_HIGH 128
#define BRIGHTNESS_MAX 255

struct LedZone {
  const char *name;
  uint16_t start;  // inclusive start index
  uint16_t length; // number of LEDs in zone
};

// Adjust these if your strip differs
#define NUM_LEDS 32
static const LedZone zone3 = {"zone3", 0, 7};   // 7 LEDs
static const LedZone zone4 = {"zone4", 7, 14};  // 7 LEDs
static const LedZone zone5 = {"zone5", 14, 22}; // 8 LEDs
static const LedZone zone6 = {"zone6", 22, 32}; // 10 LEDs
// static const LedZone zone7 = {"zone7", 25, 37}; // 12
// static const LedZone zone8 = {"zone8", 37, 50}; // 13
// static const LedZone zone9 = {"zone9", 50, 64}; // 14

void setZoneColor(CRGB leds[], const LedZone &z, const CRGB &color);
void clearZone(CRGB leds[], const LedZone &z);

// Convenience API: set/clear by numeric zone id (zone numbers as in layout)
// Returns true if the zone id was found and the operation applied.
bool setZoneColorById(int zoneId, CRGB leds[], const CRGB &color);
bool clearZoneById(int zoneId, CRGB leds[]);