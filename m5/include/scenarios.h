/* ABOUTME: Scenario management header
   ABOUTME: Declares carousel scenario API for runtime selection */
#pragma once

#include "M5GFX.h"

extern M5GFX display;

// Initialize scenarios and start the carousel
void scenarios_init();

// Call regularly from main loop to update current scenario and handle switching
void scenarios_update();

// Layout helpers used by scenario implementations
void draw_header(const char *title, int index, int total);
void draw_footer(int index, int total);
