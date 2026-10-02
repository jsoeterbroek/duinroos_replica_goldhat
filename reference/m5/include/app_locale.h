/* ABOUTME: Application-level locale helpers
   ABOUTME: Minimal locale support for English and German UI texts. */
#pragma once

#include <stdint.h>

enum class AppLocale { EN, DE };

// Set the application locale
void app_locale_set(AppLocale loc);

// Get current locale
AppLocale app_locale_get();

// UI strings used by the app
const char *loc_choose_language();
const char *loc_option_english();
const char *loc_option_german();
const char *loc_touch_instructions();

// Scenario titles and labels
const char *loc_scn_title_1();
const char *loc_scn_months();
const char *loc_scn_years();
const char *loc_scn_total_days();
const char *loc_scn_years_and_daysrem();

const char *loc_scn_title_2();
const char *loc_scn_months_approx();

const char *loc_scn_title_3();
const char *loc_scn_approx_months();
