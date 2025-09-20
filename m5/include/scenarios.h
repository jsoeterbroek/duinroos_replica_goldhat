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

// Automatic registration API
// A scenario is a void function with no args that draws its view.
using scenario_fn_t = void (*)();

// Register a scenario. Typically called from a translation-unit static
// initializer in each scenario file. Returns the index assigned (0-based).
int register_scenario(const char *title, scenario_fn_t fn);

// Helper macro for static registration in scenario files. Usage:
// STATIC_REGISTER_SCENARIO("Title", function_name);
#define STATIC_REGISTER_SCENARIO(_title, _fn)                                  \
  namespace {                                                                  \
  struct _StaticScenarioRegister {                                             \
    _StaticScenarioRegister() { register_scenario((_title), (_fn)); }          \
  } _static_scenario_register_instance;                                        \
  }
