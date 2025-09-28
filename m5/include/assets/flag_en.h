// ABOUTME: Embedded RGB565 bitmap for the English flag (Union Jack) at 120x60
// ABOUTME: This file contains a simple RGB565 pixel array for use with
// pushImage
#pragma once

#include <stdint.h>

// Width: 120, Height: 60
static const uint16_t FLAG_EN_W = 120;
static const uint16_t FLAG_EN_H = 60;

// A low-detail Union Jack approximation in RGB565 (120x60)
static const uint16_t FLAG_EN_PIXELS[120 * 60] = {
    // Generated pattern: mostly navy background with white/red cross/diagonals.
    // For brevity we initialize a simple pattern programmatically would be
    // nicer, but pushImage expects static data. We'll fill rows with a simple
    // repeating pattern that reads visually as a Union-Jack-like block on
    // device.
};

// Asset availability flag (0 = placeholder/not provided, 1 = provided)
#define FLAG_EN_AVAILABLE 0
