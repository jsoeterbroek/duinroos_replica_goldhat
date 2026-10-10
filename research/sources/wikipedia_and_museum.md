# Source: Wikipedia + the Neues Museum text — the public synthesis

**What it is:** the public-facing synthesis of the calendar theory, useful for
tracking what the *museum* says (as opposed to what scholars publish).
- Wikipedia, *Berlin Gold Hat* and *Gold hat* (en), *Berliner Goldhut* and *Goldhut*
  (de), and *Golden Hat of Schifferstadt*.
- The Neues Museum / Museum für Vor- und Frühgeschichte display text, quoted on
  Google Arts & Culture: "a complex counting system is encoded, enabling calendar
  calculations, especially the 19-year cycle of the sun and the moon…".
- Wikimedia Commons, *Berlin Gold hat calendar.jpg* (the source of the calendar
  diagram the earlier digest links to).

**Licence:** CC BY-SA (Wikipedia); museum text © the museum.

**Already on this machine?** Partly — `assets/Berlin_Gold_hat_calendar.jpg`,
`assets/berliner_goldhut_abrollung.jpg` and the other object photos.

## Getting it

```sh
for p in Berlin_Gold_Hat Gold_hat; do
  curl -s "https://en.wikipedia.org/w/index.php?title=$p&action=raw"
done
curl -s "https://de.wikipedia.org/w/index.php?title=Berliner_Goldhut&action=raw"
curl -s "https://de.wikipedia.org/w/index.php?title=Goldhut&action=raw"
```

## Page images

The object photographs are in `assets/` (Museum photos, CC/own work mixes — check
each file's licence before reuse). The calendar diagram is on Commons.

## Citation format

Wikipedia, *Berlin Gold Hat*, accessed 2026-10-10; Neues Museum, display text
(quoted via Google Arts & Culture).

## Key content (verified)

- The museum text asserts a **19-year sun–moon cycle**, **354** lunar days and
  **365** solar days, **7 intercalary months in 19 years**, and even lunar-eclipse
  prediction. It is the strongest public claim and is a secondary synthesis of
  Menghin.
- Wikipedia's calendar section reproduces Menghin 2000 (the 54-month example,
  intercalary zones {5,7,16,17}). It is a **transcript**, not a new measurement.

## Known traps in this source

- The Wikipedia text is where the earlier digest's errors entered the repo:
  the `{5,7,16,17}` set (superseded by Menghin 2010's `{7,16,17}`), the "~3,393
  symbols" figure (garbled), and the Ezelsdorf 1739 (copied from Berlin).
- Museum text is **not** peer review. Quote it as "the museum's reading", never as
  a result.
