// ABOUTME: Embedded RGB565 bitmap for the German flag at 120x60
// ABOUTME: This file contains a simple RGB565 pixel array for use with
// pushImage
#pragma once

#include <stdint.h>

// Width: 120, Height: 60
static const uint16_t FLAG_DE_W = 120;
static const uint16_t FLAG_DE_H = 60;

// Simple German tricolor: black, red, yellow horizontal bands
static const uint16_t FLAG_DE_PIXELS[120 * 60] = {
    // We'll leave the array empty here as a placeholder; main.cpp will fall
    // back to vector drawing if the array is empty. This keeps the change
    // low-risk.
};

// Asset availability flag (0 = placeholder/not provided, 1 = provided)
#define FLAG_DE_AVAILABLE 0
