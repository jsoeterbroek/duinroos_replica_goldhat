# FINDING_2026-10-13_menghin-2010-ingested

**Status:** verified (read on the page images; controls C6/C1 and the 2000↔2010
cross-check reproduce)
**Source:** W. Menghin, *Der Berliner Goldhut — Macht, Magie und Mathematik in der
Bronzezeit* (Die Sammlungen des Museums für Vor- und Frühgeschichte 2), Regensburg
2010. Whole book, pp. 1–88 + front matter, digitised by the project author.
Page images `assets/menghin/2010/jpg/`, text layer
`assets/menghin/2010/ocr/`, per-batch text `assets/menghin/2010/text/`.
**Subject:** the monograph itself — and what it says about the transfer of the
Berlin reading to the other three hats.

## What changed

Until today the case held Menghin 2010 only in part (pp. 20–31 and 47–63, the
Zahlensymbolik core). The **whole book** is now on disk and read. The decisive new
material is the chapter **"Der Vergleich" (pp. 64–72)**, where Menghin applies his
Berlin rule to Schifferstadt, Avanton and Ezelsdorf. It settles — from the author's
own pen — the question Peter-Röcher 2023 raised one sentence long: *does the rule
transfer?*

Nothing here changes the question or the hit definition in `CASE.md`. It changes
how much of the claim the primary author himself backs.

## Four results

### 1. Menghin himself calls the transfer only **partial**

p. 65, opening sentence of the comparison:

> „Die Interpretation des Zahlenwerks in der Ornamentik des Berliner Goldhutes
> hinsichtlich eines lunisolaren kalendarischen Konzeptes oder eines sogenannten
> ‚gebundenen Kalenders' **lässt sich partiell** auf seine drei Vergleichsstücke
> übertragen."

For Schifferstadt only "wenige kalendarisch annähernd verwertbare Zahlen wie 355,
266 und 272" are obtained; for Avanton likewise "nur wenige" (the 364 rings of Z6–13,
the 182 of Z3–7, the 355 of Z8–14, the 268 of Z3–9, the 177 of Z12–14). The
cross-hat test is, on the author's own account, a partial fit — not a clean second
confirmation.

### 2. For Ezelsdorf, the **stamp-identity rule yields no direct calendar values**

p. 68, on the second-most-complex hat:

> „Umso erstaunlicher ist es, dass sich etwa **aus der Addition identischer Stempel
> oder deren zonenweiser rhythmischer Abfolge**, wie im Fall des Berliner Beispiels,
> im Ornamentkanon des Goldkegels von Ezelsdorf-Buch **keine direkten kalendarische
> Werte ermitteln lassen** (Abb. 69)."

That is the method the Berlin reading actually rests on (Menghin's 2000 rhythmic
zone blocks / identical stamps, and Fuls's *method B*), and Menghin states it fails
on Ezelsdorf. He then falls back to **contiguous zone-block sums** ("Dennoch können
… analog zum Berliner Goldhut aufeinanderfolgende Zeitabschnitte … errechnet
werden"), i.e. exactly the post-hoc block selection `CASE.md` excludes as a hit.
Menghin's own solar/lunar targets for Ezelsdorf (Abb. 70/71) reconcile to
Quersumme +1 (solar) and −4 (lunar) only through those chosen blocks.

### 3. The Ezelsdorf **intercalary set moves between his own publications**

- **Menghin 2000** (Abb. 27): Schaltzonen `{5, 6, 19}`; Z15 and Z17 are *Sonderzonen*
  ("Augenmotiv", "Räder").
- **Menghin 2010, table Abb. 69, p. 68:** green Schaltzone rows are
  `{5, 6, 15, 16, 17, 19}` (six).
- **Menghin 2010, text p. 68:** „die Zonen 5, 6 und 19 sowie die Zonen 15 und 17"
  (five — Z16 omitted).
- **Fuls 2008** (his „Symboltyp tritt nur einmal auf" rule): **12** Schaltzonen.

The Berlin set `{7,16,17}` + Sonderzone 5 is stable across his publications. The
**Ezelsdorf** set is not, and the 2010 book is not even self-consistent between its
own table and text. This is the "free parameter that moves between publications"
`CASE.md` names as disqualifying, now documented on the primary pages. It is the
concrete form of Peter-Röcher's and Schlosser's critique.

### 4. The Ezelsdorf 2010 zone table **reproduces the 2000 table**, and the Z8 slip is in the typescript

Abb. 69 (p. 68) read against `data/readings/menghin2000_zones.json`: every
disc-bearing zone agrees ring for ring (Z5 54, Z6 84, Z7 66, Z9 150, Z10 96, Z11 95,
Z12 140, Z13 45, Z14 102, Z16 57, Z18 98, Z19 52, Z20 154). The 2010 table prints
**Zone 8 A = 40 with SK = 78** — the same `A`-column vs `A×K` slip flagged in the
2000 finding (left column 40, right column/text 39; 39 × 2 = 78). Because it recurs in
a second publication, it is a slip in Menghin's typescript, not a scanning artefact.
The 1506 (zones 3–20) and 1737 (with the reconstructed rim) totals reproduce. The
text's **"433 Buckelscheiben"** for the 1463-ring set (zones 3–14, 16, 18–20) also
follows from the table — *because* Z8 is read as 40. Read with Z8 = 39 (the 2000
value) the same set is **432**. So the one-digit slip changes the **disc total
between the editions** (2000: 432, 2010: 433) while leaving the ring sums identical
— a clean demonstration that the symbol totals, not the rings, are the fragile
layer.

## Control that passed

**Berlin 2010 Abb. 23 (p. 30) == Berlin 2000 Abb. 14 (p. 45)**, zone by zone and
ring by ring (Z3 3/14, Z4 5/15, Z5 19/19, Z6 5/18, Z7 3/19, Z8 5/21, Z9 3/19,
Z10 5/19, Z11 3/20, Z12 5/20, Z13 3/20, Z14 5/21, Z15 6/15, Z16 2/19, Z17 2/33,
Z18 6/21, Z19 6/23, Z20 3/54, Z21 5/47). The two publications measure the same
object the same way; only the *comparison to the other hats* is new.

## Checks

- [x] Read on the page image (p. 65, p. 68 enlarged from the native 1661×2100 scan)
- [x] 2000↔2010 cross-check: Berlin Abb. 23 == Abb. 14; Ezelsdorf Abb. 69 == Abb. 27
- [x] Intercalary set counted from the green row highlights, not from the caption text
      (the text and the table disagree; both states reported)
- [x] Units kept as Menghin's ring-counter, separate from Fuls/Schmidt-Kaler counts
- [x] Negative/flagged states reported, not forced (partial transfer; moving set;
      Z8 slip; and its knock-on to the 432/433 disc totals)
- [x] Novelty: the book in full was not in the repo before 2026-10-13; the
      comparison chapter and the 2010 intercalary marks are new to the case

## Evidence

- Pages: `assets/menghin/2010/jpg/menghin_page065.jpeg` (p. 65, transfer),
  `…page068.jpeg` (p. 68, Ezelsdorf table Abb. 69 + the quote),
  `…page030.jpeg` (p. 30, Berlin Abb. 23, the control),
  `…page064.jpeg` (p. 64, the four hats),
  `…page069.jpeg`–`…page071.jpeg` (Abb. 70–72, Ezelsdorf solar/lunar summary).
- Whole-book text: `assets/menghin/2010/text/`.
- Controls: C6 (`verify_menghin2000.py`), C1.

## Open questions

- Is the 2010 Ezelsdorf intercalary set six (table) or five (text)? The green rows on
  p. 68 are unambiguously six; the sentence omits Z16. A 300–400 dpi re-scan of p. 68
  would let the colour blocks be checked against the caption once more.
- Which is the intended Ezelsdorf Z8 count, 39 or 40? Both editions print the *other*
  number in the graphic's left-hand `A` column, and the published disc totals follow
  whichever is used (432 vs 433) while the ring sum stays 78. Unresolved in both
  publications.
- pp. 73–88 (Die goldenen Kalenderhüte, Der Kult, Literatur) are now in hand but only
  skimmed; the cult/context chapter may carry the find-context arguments (`todo`).
