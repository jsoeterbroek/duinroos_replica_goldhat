/* ABOUTME: Application-level locale implementation
   ABOUTME: Provides simple in-memory string selection for EN/DE. */

#include "app_locale.h"

static AppLocale current = AppLocale::EN;

void app_locale_set(AppLocale loc) { current = loc; }

AppLocale app_locale_get() { return current; }

// UI strings
const char *loc_choose_language() {
  return (current == AppLocale::DE) ? "Sprache wählen" : "Choose language";
}

const char *loc_option_english() {
  return (current == AppLocale::DE) ? "Englisch" : "English";
}
const char *loc_option_german() {
  return (current == AppLocale::DE) ? "Deutsch" : "German";
}
const char *loc_touch_instructions() {
  return (current == AppLocale::DE) ? "Berühre links/rechts"
                                    : "Touch left/right";
}

// Scenario 1
const char *loc_scn_title_1() {
  return (current == AppLocale::DE) ? "Lunar: 54 Monate" : "Lunar: 54 months";
}
const char *loc_scn_months() {
  return (current == AppLocale::DE) ? "Monate:" : "Months:";
}
const char *loc_scn_total_days() {
  return (current == AppLocale::DE) ? "Gesamttage:" : "Total days:";
}
const char *loc_scn_years_and_daysrem() {
  return (current == AppLocale::DE) ? "~Jahre: %d, ~Resttage: %d"
                                    : "~Years: %d, ~Days rem: %d";
}

// Scenario 2
const char *loc_scn_title_2() {
  return (current == AppLocale::DE) ? "Metonisch: 19 Jahre"
                                    : "Metonic: 19 years";
}
const char *loc_scn_months_approx() {
  return (current == AppLocale::DE) ? "Monate (approx): %d"
                                    : "Months (approx): %d";
}

// Scenario 3
const char *loc_scn_title_3() {
  return (current == AppLocale::DE) ? "Jahrhundert-Schätzung: 100y"
                                    : "Century estimate: 100y";
}
const char *loc_scn_approx_months() {
  return (current == AppLocale::DE) ? "Ungefähr Monate: %.2f"
                                    : "Approx months: %.2f";
}
