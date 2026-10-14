# Repo size — state and options for later cleanup

**Status:** first pass done (2026-10-13). `.git` **413 MB → 241 MB**. A second pass is
available and described below; it was deliberately not done because it costs image
quality on primary-source evidence.

This note exists so the work can be picked up later without re-deriving it. Nothing
here is urgent.

---

## 1. What was done (2026-10-13)

History rewritten with `git-filter-repo` and force-pushed. **All commit hashes changed.**

| Action | Reclaimed |
|---|---|
| `assets/menghin/2010/jpg/**` downscaled to 2000 px / q82 (raw-phone 4032 px photos) | 98 MB → 24 MB |
| `cad/**` removed from history — pre-reorg **duplicates**, dead in the working tree | ~102 MB |
| `reference/cad/{freecad_export,3mf,svg,freecad_import}/**` removed from history, now **gitignored but kept on disk** | ~83 MB |
| flat `assets/menghin/menghin_page*.jpeg` removed from history — a **second copy** of the Menghin originals at an old path | ~96 MB |

Result: `.git` 241 MB (pack 240.40 MiB), 82 commits.

**Not touched, on purpose:** `assets/menghin/2000/jpg` (93 MB) and
`assets/menghin/2010/jpg` (111 MB). They are already ~2000 px, so re-encoding them
is generation loss for ~18%, and they are the bulk of what remains. See §3.

---

## 2. Where the remaining 241 MB is

| Path | Tracked size | Files | Note |
|---|---|---|---|
| `assets/menghin/2010/jpg/**` | ~111 MB | 85 | the full 2010 book, ~2000 px |
| `assets/menghin/2000/jpg/**` | ~93 MB | 83 | ~2000 px |
| `reference/cad/*.FCStd`, `printed/` | ~10 MB | | CAD sources (kept in git on purpose) |
| everything else (plan, research, scripts, assets) | ~5 MB | | |

Also on disk but **not in git** (gitignored, ~300 MB): the scanned `assets/menghin/*/pdf/`
files. Those are fine — they never entered history.

> ℹ️ **2026-10-14 reorg:** the old phone-photo set (`2010/jpg`, 28 files, 24 MB,
> names like `page25`) and its `ocr/`/`text/` were **superseded and removed**; the
> full-scan files were moved out of `2010/full/` into `2010/` (names like `page025`).
> The duplicate/subset question in §4, option 0 is therefore moot — there is now a
> single 2010 tree.

---

## 3. The three ways to go smaller

### Option A — downscale the two remaining sets (simplest)
```bash
# 1600 px / q80: roughly halves them (~200 MB -> ~100 MB), best-case saving ~140 MB
for d in assets/menghin/2000/jpg assets/menghin/2010/jpg; do
  for f in "$d"/*.jp*; do sips -Z 1600 -s format jpeg -s formatOptions 80 "$f"; done
done
```
**Cost:** these are book pages used for OCR. 1600 px is readable by eye but weaker for
small footnotes. The plan's authoritative tier is the hand transcription in
`assets/menghin/**/text/`, so OCR should not need re-running — but confirm before doing it.
Then the files must be **re-added and the originals stripped from history** (see §5) or the
repo does not actually shrink.

### Option B — git-lfs (keeps full resolution, moves bytes off the pack)
```bash
git lfs install
git lfs track 'assets/menghin/**/jpg/*.jpeg'
git lfs migrate import --include='assets/menghin/**/jpg/*.jpeg' --everything
git push --force
```
**Cost:** LFS has a free storage/bandwidth quota on GitHub (1 GB storage / 1 GB-month
transfer on Free). This alone doesn't shrink the local clone much, and it rewrites history
again. Good if full-resolution scans must stay versioned.

### Option C — move the page photos out of git (smallest repo, least reversible in git)
Attach them to a **GitHub Release** (or any cloud bucket), keep a `SHA256SUMS` in the repo,
then `git-filter-repo` them out. The repo drops to a few MB. Cost: a clone no longer
contains the images; the plan's source paths point outside the repo.

**Recommendation:** option **0** (dedupe check) → then **A** at 1600 px if you accept the
OCR trade-off → else **B**. Do **C** only if the scans will live somewhere else anyway.

---

## 4. Before any of this — option 0: check the overlap

**Resolved 2026-10-14.** The overlap was the old phone-photo set, now removed by the
reorg (see the note in §2). No separate check is needed.

---

## 5. Recipe used (re-run if more history work is needed)

```bash
git filter-repo --force --path <path> --path <path> --invert-paths
git reflog expire --expire=now --all && git gc --prune=now
git remote add origin git@github.com:jsoeterbroek/duinroos_replica_goldhat.git
git push --force origin main
```
Notes learned the hard way:
- `git-filter-repo` **removes the working-tree files** at the stripped paths (its
  `reset --hard`). Back them up **before** running, and restore afterwards.
- It also **removes `origin`** and prunes commits that become empty (157 → 82 here).
- `--path-glob 'assets/menghin/menghin_page*.jpeg'` was needed for the second copy: the
  same files existed under two paths in history (a flat one and the `2010/jpg/` one).
  **Audit reachable blobs after every pass**, don't assume one strip is enough:
  ```bash
  git rev-list --objects --all \
    | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' \
    | awk '$1=="blob" && $2>1000000 {printf "%8.2f MB  %s\n",$2/1048576,$3}' | sort -rn
  ```
- After a force-push, **every other clone must re-clone** (or
  `git fetch && git reset --hard origin/main`).

---

## 6. Backups (delete once satisfied)

Kept at `~/Development/goldhat_precleanup_backup/` (~797 MB, **outside** the repo):

| Path | What |
|---|---|
| `repo.git/` | full pre-cleanup mirror — the rewrite is reversible from here |
| `menghin_fullres/2010_jpg/`, `2000_jpg/`, `2010_full_jpg/` | the **full-resolution** page photos |
| `reference_cad/` | the de-tracked exports (`freecad_export`, `3mf`, `svg`, `freecad_import`) |

Restore a single file: `cp <backup>/menghin_fullres/2010_jpg/<name> assets/menghin/2010/jpg/`.
Restore all history: `git clone <backup>/repo.git`.

---

## 7. Loose ends

- **Stale claim to fix in `IMPLEMENTATION_PLAN.md` (~line 1076):** it says the
  `assets/menghin/2010/jpg` images have "EXIF orientation 6 / rotated 90°", but `sips`
  reports **no orientation tag** on the originals and the compressed copies render upright.
  Verify against a full-res copy in the backup and correct the line.
- `assets/menghin/2010/` also carries its own `ocr/` and `text/` — cheap, no action.
- `stl/` is gitignored (regenerable), correct.
