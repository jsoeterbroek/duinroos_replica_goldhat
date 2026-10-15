# duinroos_replica_goldhat
duinroos_replica_goldhat

## Note:
Developed with AI model Deepseek: "deepseek-v4.1-flash:cloud"

## Project Overview
This is a 3D printed replica of the Berlin Goldhat

## Project Goal
The goal of this project is to provide a 1-to-1 replica of the Berlin Goldhat, in three stages that all read the same `data/*.json` as the single source of truth:

- **Stage 1 — visual scenario figures (active):** script-generated, stylised images (PNG/JPG/SVG) of the object, per calendar scenario/hypothesis, in the style of Menghin (2010) Figs 61.1–64.4 (coloured zone bands, legend, the arithmetic, the caveat). For articles, documentation, the demo, and a later video. No FreeCAD, no printer.
- **Stage 2 — 3D-printable replica:** separate STL files for 3D printing, one per band, stacking into the full 745 mm model.
- **Stage 3 — LED demonstration:** the calendar theory (theories) behind the object, using:
  -  LED lights behind the outer surfaces behind the symbols to light any one band showing the corresponding symbols with different colors
  - A esp32 dev kit to drive the scenarios lighting up different sections
  - A screen to display information and calculation of the scenario 
- separate STL files for 3D printing
- The real live object consists of muliple 'bands' or 'slices' (see dimensions.txt).
- Each band should be a separate 3D-printable STL file with the object to stack each on top of the other to create the complete model
- Each band should show the correct symbols and decorations as the real object (but without the real dents and bruises), the model should be a stylised model of the real object, not a copy of the actual surface irregularities
- An earlier attempt was made to create this, but was abandoned, see folder reference/

## Background
Important files on the background of the object:
- research/CASE.md - the research question, scoped, with the sources, controls and plan (entry point)
- research/theories/ - the competing calendar readings (Menghin lunisolar, Schmidt-Kaler Venus, Fuls, Lorenz, ...)
- research/sources/ - one recipe per primary source
- sources.md - sources used (physical books)
- dimensions.txt - approximation of the dimensions (from Menghin, Wilfried); use as  an important source, but do check if correct (don't take these numbers blindly for granted)

## Commands
AI Model in PI <--->  MCP  <---> Freecad running MCP server

## Research folder
The research folder contains AI-assisted research (using https://github.com/jessewaites/antiquity). Use these a reference.

## Assets folder
The assets folder contains images of the real object in Berlin Museum. Use these a reference.

## Reference folder
An earlier attempt was made to create this, but was abandoned, see reference/ folder. Use for reference but do not recycle the files/code etc.

## Repo size
What is tracked, why, and the options for shrinking the repo further: `repo_size_cleanup.md`.

## Architecture
- LED lights
- M5 core S3 module for the demo code driving the LEDs (and display)

## Tech Stack
- pio for ESP32 code development
- Python for scripts to generate STL files
- matplotlib for the Stage-1 scenario figures (PNG/SVG/PDF)
- C++ for ESP32 dev kit
- uv (uvx)
- FreeCAD with MCP Addon running MCP server
- M5 core S3 dev kit module
_ BambuLabs 3D printer

