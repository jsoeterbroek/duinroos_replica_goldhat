Project: duinroos_replica_goldhat (M5)

Quick RTC sync notes

This project should keep the on-board RTC in sync so scenarios that use
calendar calculations show correct dates and times.

Planned behaviors (tracked in TODO):
- On boot, attempt to set RTC from NTP when Wi‑Fi is available.
- Provide a touchscreen UI to set date/time manually when Wi‑Fi is unavailable.
- Persist RTC settings so time survives reboots (battery-backed RTC or saved
  to non-volatile storage and reapplied at startup).
- Show an on-screen indicator showing whether time was obtained from NTP or
  set manually. Serial logs should also report the source and any failures.

How to set the RTC manually (quick tip for developers):
- Use the device's RTC API (e.g. `rtc.adjust(DateTime(year, month, day, hour, minute, second))`)
  from a small helper function or from the REPL/serial console after building a
  small firmware helper. Make sure to store timezone info separately if required.

Next steps for implementers:
1. Add an NTP client on startup and call `rtc.adjust(...)` with the retrieved time.
2. Add a small Settings screen with touch controls and numeric steppers to set
   date/time (accept and cancel actions). When confirmed, call `rtc.adjust()`
   and persist a flag that indicates manual override.
3. Add an on-screen icon or small text line in the footer showing the time source.

If you want I can implement the NTP + touchscreen flow; tell me whether to
prioritize NTP-first behavior or manual-first UI for offline commissioning.
