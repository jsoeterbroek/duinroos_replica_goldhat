# Source: Schmidt-Kaler 2012 — the Venus reading

**What it is:** T. Schmidt-Kaler, *Ein Venus-Kalender auf dem Berliner Goldhut —
Zur Entstehung und Entwicklung der Goldhüte als Kalender-Gerät* (2012). A
minority essay arguing the ornament encodes a Venus (and Mercury) calendar. The
PDF also binds a second, separate article on the Schifferstadt hat; only the Venus
paper is relevant.

**Licence:** in copyright (author posted it openly).

**Already on this machine?** Yes. `research/data/sources/schmidt_kaler_2012.pdf`
(gitignored). The repo's earlier copy came from the URL below.

## Getting it

```sh
curl -L -o schmidt_kaler_2012.pdf \
  "https://www.quantenbit.physik.uni-mainz.de/files/2020/03/Goldhut-TSchmidtKaler-2012.pdf"
```

**Trap:** the PDF is a **scan with no text layer**. Use OCR (`tesseract -l deu`) and
check digits against the scan. A machine OCR of the relevant pages already exists
in the earlier assessment's provenance.

## Page images

Render with PyMuPDF:

```python
import fitz
d = fitz.open("schmidt_kaler_2012.pdf")
d[PAGE-1].get_pixmap(matrix=fitz.Matrix(2,2)).save("evidence/..._full.jpg")
```

## Citation format

Schmidt-Kaler 2012, p. N.

## Known traps in this source

- He **adopts Menghin's day-values explicitly** ("gemäß Menghin"); the paper adds
  an interpretation, not a measurement. Its Venus half-cycle is built from
  Menghin's 235 + 57 = 292.
- He offers **two mutually exclusive Venus solutions** and asks in the paper which
  is better — a fitted, not a read, result.
- He also extracts a **Mercury** calendar from the same zones.
- The OCR can corrupt the German digits; verify on the scan.
