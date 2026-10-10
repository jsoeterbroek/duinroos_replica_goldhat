# duinroos_replica_goldhat
duinroos_replica_goldhat

## Note:
Developed with AI model Deepseek: "deepseek-v4.1-flash:cloud"

## Project Overview
This is a 3D printed replica of the Berlin Goldhat

## Project Goal
The goal of this project is to provide a 1-to-1 replica of the Berlin Goldhat:

- In the first stage, a model representation without LED lights
- In the second stage, I want to be able to demonstrate the calendar theory (theories) behind this object, using:
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
- gold_hat.md - explains the object Berlin Goldhat and theory behind it 
- sources.md - sources used (physical books)
- dimensions.txt - approximation of the dimensions (from Menghin, Wilfried); use as  an important source, but do check if correct (don't take these numbers blindly for granted)

## Commands
AI Model in PI <--->  MCP  <---> Freecad running MCP server

## Assets folder
The assets folder contains images of the real object in Berlin Museum. Use these a reference.

## Reference folder
An earlier attempt was made to create this, but was abandoned, see reference/ folder. Use for reference but do not recycle the files/code etc.

## Architecture
- LED lights
- M5 core S3 module for the demo code driving the LEDs (and display)

## Tech Stack
- pio for ESP32 code development
- Python for scripts to generate STL files
- C++ for ESP32 dev kit
- uv (uvx)
- FreeCAD with MCP Addon running MCP server
- M5 core S3 dev kit module
_ BambuLabs 3D printer

