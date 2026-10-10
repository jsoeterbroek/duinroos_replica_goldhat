# Control C4 — Fuls 2008's negative result must re-find

**What:** the published null result that the project's own scripts first found:
for the Berlin Gold Hat, the frequency of calendar "hits" is statistically
indistinguishable from chance; only Schifferstadt is selective. This is the
control for the *sceptical* claim — a pipeline that only ever finds positive
calendar readings is broken.

**Expected (Fuls 2008, §8.4.6–8.6):**
- Four combination methods with very different search spaces (Berlin: G = 210 to
  1 048 575).
- Chance baseline `w = 2·t_p/p`; hit rate `h = T/G`.
- Berlin `h ≈ w` for the synodic month and the tropical year under all methods
  (e.g. method D: synodic month 6.58 % vs 6.77 %; tropical year 0.43 % vs 0.55 %).
- **Only Schifferstadt** exceeds chance clearly: method B × synodic month
  16.13 % vs 6.77 %, factor ≈ 2.1, confirmed by its metrology.
- The author's own caveat that a true sparse encoding could be drowned by the
  large G — so the result is "not demonstrated", not "disproved".

**How to re-find:**
- Read on the page image:
  `evidence/2008_wurzburg_fuls_goldhats_stats_conclusions_fuls2008_p123_full.jpg`
  and `…_stats_tables_fuls2008_p121_full.jpg`.
- **Not yet scripted here.** A committed re-implementation of the combinatorial
  null is an open `todo/` item.

**If missed:** either the re-implementation is wrong or the corpus is wrong. The
point of the control is that a *negative* must be reachable; a pipeline that
cannot produce this negative cannot be trusted on a positive.
