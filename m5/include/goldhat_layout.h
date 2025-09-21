/* ABOUTME: Embedded gold-hat layout JSON
   ABOUTME: Provides a compile-time JSON string used by the LED mapper when
   runtime filesystem access is not available. */
#pragma once

// Schema: each zone may include optional `multiplier` and optional
// `special_value` (for special symbols that carry a fixed numeric value).
// TODO: this is schmidt-kaler's berlin layout; replace with meghin's
static const char *berlin_goldhat_layout_json = R"json([
  {"zone":1,"count":17,"multiplier":1}, {"zone":2,"count":19,"multiplier":1}, {"zone":3,"count":29,"multiplier":1}, {"zone":4,"count":33,"multiplier":1},
  {"zone":5,"count":34,"multiplier":1,"special_value":38}, {"zone":6,"count":29,"multiplier":1}, {"zone":7,"count":33,"multiplier":1}, {"zone":8,"count":34,"multiplier":1},
  {"zone":9,"count":33,"multiplier":1}, {"zone":10,"count":34,"multiplier":1}, {"zone":11,"count":33,"multiplier":1}, {"zone":12,"count":34,"multiplier":5},
  {"zone":13,"count":33,"multiplier":1}, {"zone":14,"count":34,"multiplier":1}, {"zone":15,"count":33,"multiplier":1}, {"zone":16,"count":34,"multiplier":1},
  {"zone":17,"count":33,"multiplier":1}, {"zone":18,"count":34,"multiplier":1}, {"zone":19,"count":33,"multiplier":1}, {"zone":20,"count":34,"multiplier":1},
  {"zone":21,"count":21,"multiplier":1}
])json";
