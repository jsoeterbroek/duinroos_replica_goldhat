/* ABOUTME: Virtual LED simulator implementation
   ABOUTME: Renders a simple circular layout of LEDs to the M5 display for
   demos. */

#include "virtual_leds.h"
#include "M5Unified.h"
#include "scenarios.h" // provides extern M5GFX display
#include <Arduino.h>
#include <cmath>

static int v_width = 0;
static int v_height = 0;
static std::vector<rgb_t> vbuf;
static int total_leds = 0;

void vled_init(int width, int height) {
  v_width = width;
  v_height = height;
  auto &zones = get_zones();
  total_leds = 0;
  for (auto &z : zones)
    total_leds += z.count;
  vbuf.assign(total_leds, {0, 0, 0});
}

void vled_set(int index, rgb_t c) {
  if (index < 0 || index >= (int)vbuf.size())
    return;
  vbuf[index] = c;
}

void vled_clear() {
  for (auto &p : vbuf)
    p = {0, 0, 0};
}

void vled_render() {
  display.startWrite();
  display.fillScreen(TFT_WHITE);
  int cx = v_width / 2;
  int cy = v_height / 2 + 20;
  int rings = 6;
  int idx = 0;
  for (int r = 0; r < rings; r++) {
    int n = (int)ceil((float)total_leds / rings);
    float radius = 20 + r * 12;
    for (int i = 0; i < n && idx < total_leds; i++, idx++) {
      float a = (float)i / (float)n * 2.0f * PI;
      int x = cx + (int)(cos(a) * radius);
      int y = cy + (int)(sin(a) * radius);
      auto &c = vbuf[idx];
      uint16_t color = display.color565(c.r, c.g, c.b);
      display.fillCircle(x, y, 4, color);
    }
  }
  display.endWrite();
}

bool vled_pulse_range(const std::vector<std::pair<int, int>> &ranges,
                      uint32_t color, uint32_t period_ms) {
  static uint32_t start = 0;
  if (start == 0)
    start = millis();
  uint32_t t = (millis() - start) % period_ms;
  float phase = (float)t / (float)period_ms;
  float brightness = 0.5f + 0.5f * sinf(phase * 2.0f * PI);
  uint8_t r = (color >> 16) & 0xff;
  uint8_t g = (color >> 8) & 0xff;
  uint8_t b = (color >> 0) & 0xff;
  for (auto &rg : ranges) {
    for (int i = rg.first; i <= rg.second; i++) {
      vled_set(i, {(uint8_t)(r * brightness), (uint8_t)(g * brightness),
                   (uint8_t)(b * brightness)});
    }
  }
  vled_render();
  return true; // always active
}
