This repository includes an in-device verification scenario that checks canonical numeric examples from `gold_hat.md`.

How to run (on device):
1. Ensure `goldhat_layout.json` is present at SPIFFS root (use PlatformIO `data/` folder and `pio run --target uploadfs`).
2. Flash the firmware and open the device. Use the scenario carousel to select "Verify canonical sums".
3. The display will show VERFIED (green) if the canonical sums match the expected values (1739,142,1597) or a red failure screen with computed values.

Notes:
- The verification relies on the layout file counts. When you supply the primary Menghin sources we will use them to update the layout and tests to authoritative values.