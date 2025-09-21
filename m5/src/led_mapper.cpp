/* ABOUTME: LED mapper implementation
   ABOUTME: Minimal loader and mapper for the gold-hat layout; parses a very
   small JSON layout file included in the project. */

#include "led_mapper.h"
#include "M5Unified.h"
#include "goldhat_layout.h"
#include <Arduino.h>
#include <ArduinoJson.h>
#include <FS.h>
#include <SPIFFS.h>

static std::vector<zone_t> zones;

// Very small JSON-ish parser for the known layout file format (array of
// {"zone":n,"count":m})
bool load_goldhat_layout(const char *path) {
  zones.clear();
  // If a path is provided, attempt to read the layout from SPIFFS first.
  String jsonBuf;
  bool usedEmbedded = false;
  if (path != nullptr) {
    if (!SPIFFS.begin(true)) {
      Serial.println("led_mapper: SPIFFS.begin failed, using embedded layout");
      usedEmbedded = true;
    } else {
      if (SPIFFS.exists(path)) {
        File f = SPIFFS.open(path, "r");
        if (f) {
          size_t sz = f.size();
          jsonBuf.reserve(sz + 1);
          while (f.available())
            jsonBuf += (char)f.read();
          f.close();
        } else {
          Serial.printf("led_mapper: failed to open %s, using embedded\n",
                        path);
          usedEmbedded = true;
        }
      } else {
        Serial.printf("led_mapper: %s not found on SPIFFS, using embedded\n",
                      path);
        usedEmbedded = true;
      }
    }
  } else {
    // No path given => try the default file on SPIFFS; if missing, use embedded
    if (SPIFFS.begin(true) && SPIFFS.exists("/goldhat_layout.json")) {
      File f = SPIFFS.open("/goldhat_layout.json", "r");
      if (f) {
        size_t sz = f.size();
        jsonBuf.reserve(sz + 1);
        while (f.available())
          jsonBuf += (char)f.read();
        f.close();
      } else {
        Serial.println(
            "led_mapper: failed to open /goldhat_layout.json, using embedded");
        usedEmbedded = true;
      }
    } else {
      usedEmbedded = true;
    }
  }

  // Parse JSON using ArduinoJson; prefer SPIFFS content if available
  DynamicJsonDocument doc(4096);
  DeserializationError err;
  if (usedEmbedded) {
    err = deserializeJson(doc, goldhat_layout_json);
  } else {
    err = deserializeJson(doc, jsonBuf);
  }
  if (err) {
    Serial.printf("led_mapper: JSON parse error: %s\n", err.c_str());
    return false;
  }
  JsonArray arr = doc.as<JsonArray>();
  for (JsonObject obj : arr) {
    zone_t zt;
    zt.zone = obj["zone"] | 0;
    zt.count = obj["count"] | 0;
    zt.multiplier = obj["multiplier"] | 1;
    zt.special_value = obj["special_value"] | 0;
    zt.start_index = -1;
    zt.end_index = -1;
    zones.push_back(zt);
  }

  // assign start/end indices sequentially
  int cur = 0;
  for (auto &z : zones) {
    z.start_index = cur;
    z.end_index = cur + z.count - 1;
    cur += z.count;
  }
  Serial.printf("led_mapper: loaded %d zones total_leds=%d\n",
                (int)zones.size(), cur);
  return true;
}

int zone_value(const zone_t &z) {
  int base = z.count * (z.multiplier > 0 ? z.multiplier : 1);
  if (z.special_value != 0)
    base += z.special_value;
  return base;
}

const std::vector<zone_t> &get_zones() { return zones; }

int sum_zone_range(int start_zone, int end_zone) {
  int sum = 0;
  for (auto &z : zones) {
    if (z.zone >= start_zone && z.zone <= end_zone)
      sum += z.count;
  }
  return sum;
}

int sum_intercalaries(const std::vector<int> &zlist) {
  int sum = 0;
  for (int znum : zlist) {
    for (auto &z : zones) {
      if (z.zone == znum)
        sum += z.count;
    }
  }
  return sum;
}

std::vector<std::pair<int, int>> map_zone_range_to_led_ranges(int start_zone,
                                                              int end_zone) {
  std::vector<std::pair<int, int>> ranges;
  for (auto &z : zones) {
    if (z.zone >= start_zone && z.zone <= end_zone) {
      ranges.push_back({z.start_index, z.end_index});
    }
  }
  return ranges;
}
