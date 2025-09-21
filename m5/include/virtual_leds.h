/* ABOUTME: Virtual LED simulator header
   ABOUTME: Provides a simple on-screen LED renderer for testing/visualization. */
#pragma once

#include <stdint.h>
#include <vector>
#include "led_mapper.h"

struct rgb_t { uint8_t r,g,b; };

// Initialize virtual LED system (needs display to be available)
void vled_init(int width, int height);

// Set LED color by global LED index
void vled_set(int index, rgb_t c);

// Render current buffer to display
void vled_render();

// Helper: draw pulse animation for a range of LED indices; returns true while active
bool vled_pulse_range(const std::vector<std::pair<int,int>> &ranges, uint32_t color, uint32_t period_ms);

// Clear all virtual LEDs
void vled_clear();
