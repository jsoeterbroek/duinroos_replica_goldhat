# Catalogue: Menghin's numbers (how they were checked)

**What it is:** the reference set of Menghin's own counts, so that any "new"
number can be checked against it before being called a find.

**How checked:** **full read** of `assets/menghin/2010/text/menghin_pages47-63.txt`
and the derived `data/zones.json` / `data/readings/menghin.json`, re-verified by
`scripts/verify_calendar.py` and `scripts/verify_scenarios.py`.

## The catalogue

| Quantity | Value | Note |
|---|---|---|
| ring-units, zones 3–21 | 1739 | = 1701 + 38 |
| ring-units, zones 2–21 | 1783 | |
| concentric rings on the 418 discs | 1701 | |
| special signs, zone 5 | 38 | 19 crescent+dot + 19 eye |
| zone day-values | 42,75,38,90,57,105,57,95,60,100,60,105,90,38,66,126,138,162,235 | zones 3–21 |
| intercalary set (2010 figs) | {7,16,17} | 2000 text: {5,7,16,17} |
| height total | 745.0 mm | |

## What is *not* in it

- `~3,393` "symbols" (garbled; no zone table sums to it).
- `1739` as an Ezelsdorf symbol count (that is Berlin's ring total).
- any plain-ornament count (`651` etc.) — that is Schmidt-Kaler's unit.

## Use

Before writing a new finding: does the number already appear here? If yes, the
finding is a *re-finding* (still useful as a control) and not novel.
