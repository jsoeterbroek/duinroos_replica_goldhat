/* ABOUTME: LED mapper header
   ABOUTME: Maps logical gold-hat zones and symbols to LED indices. */
#pragma once

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
