# Common-dialog search and Organize regression pass

Local development/QA only. No commit, publication or replacement of immutable
r9 media. This follows the Explorer 36 / Paint 8 package work.

## Reproduced defects

The previous common dialog enumerated all directories synchronously in its GUI
thread. It ignored the selected file-type filter during search, displayed files
in Choose Folder search, silently truncated results at 1,000 matches, and
searched every included library location even from a selected subfolder.
Switching repeatedly between search and directory models also retained obsolete
selection models. Organize was an unconnected button.

Three initial regression cases failed against the earlier implementation:
image filtering returned 3 rows instead of 2; dispatch already contained 1,000
results instead of returning before traversal; Choose Folder returned a file
as well as its matching directory. The full red log is retained under
`common-search-logs/aero7-search-before.log`.

## Corrections

- Debounced, off-thread directory enumeration. Only one worker is active per
  dialog; query/filter/navigation changes interrupt its work. Generation checks
  discard stale results. Closing or destroying a dialog requests interruption
  without waiting for filesystem I/O on the GUI thread.
- Results arrive in batches of at most 64. Acknowledgement bounds the queued
  work to one batch, so fast storage cannot flood the GUI event queue. There is
  no silent 1,000-result limit. The command bar reports progress and final count.
- File-type filters apply to files, while directories stay visible. Choose
  Folder searches show directories only. Hidden-file preference applies to
  both the directory view and recursive search.
- A library-root search covers its included locations; a search inside a
  materialized subfolder stays in that real subfolder. Canonical, overlapping
  roots are deduplicated. Directory symlinks are shown but not recursively
  followed. Missing/unreadable folders are counted in the status message.
- Old private selection models are deleted when swapping view models. Search
  result items are explicitly non-editable; no fake rename is exposed.
- Organize offers working New folder, Select all (multi-file mode only),
  Large icons/List layout and Show hidden files controls. This is not yet a
  complete Windows Organize menu with clipboard/trash/properties operations.
- Search result image/audio/video/document icons come from eight unchanged
  files in the existing Windows 7 Aero icon pack. Each was byte-compared against
  the selected `aerothemeplasma-icons-git-11.r96950b8-3` archive before copying.
  No new artwork or image conversion was used. Filename-extension MIME lookup
  avoids restatting result files from the GUI thread.

The exported `aero7commondialog.h` is byte-identical to the Explorer 36 source
archive. Search implementation state lives in a private child object, retaining
the dialog's public object layout and existing shared-library SONAME for Paint.

Thread lifetime/cancellation uses the documented Qt
[QThread interruption and finished/deletion mechanisms](https://doc.qt.io/qt-6/qthread.html).
Directory-link traversal follows the documented
[QDirIterator flags](https://doc.qt.io/qt-6/qdiriterator.html).

## Evidence so far

- All 19 Explorer CTest groups passed after the implementation, in 18 seconds.
- After the final singular/plural status-label correction, the common-dialog
  suite passed 29 functional cases plus setup/cleanup (31 reported passes).
- Ten new cases cover filter changes, >1,000 matches/non-blocking dispatch,
  folder-only selection, query/navigation cancellation, active-search closure,
  symlink loops, nested library scope, overlapping/unavailable roots, Organize
  actions and selection-model lifetime.
- Logs are copied into `common-search-logs/` beside this report.
- Canonical source `aero7-file-explorer-25.12.3-r37.tar.gz` SHA-256:
  `fcc0c15043f5b07af9aacd19dfb679052782012287e8572fb3828e35313b332e`.
- A fresh package build completed in `work/beta2-explorer37.NUkh2g/` using
  `makepkg --nodeps` only to skip the host package-presence precheck. No host
  packages were installed. The build recipe disables its upstream test build;
  the separate full source test results above are not package `check()` results.
- Package `aero7-file-explorer-25.12.3-37-x86_64.pkg.tar.zst` is 8,210,542 bytes,
  SHA-256 `8a0ad97ebce41509b18f1c73f866be6951c09ff6496121ecd51e553ff8b72a9c`.
  It is selected in the local manifest alongside unchanged Paint 8. Repository
  source/metadata validation and the ISO static check passed, including actual
  ELF/SONAME linkage verification. The immutable r9 ISOs were not modified.
- Normal `pacman -U` in the offline r9 guest upgraded Explorer 36 → 37. Only
  Explorer's package version changed. Explorer's 665 files and Paint's 709 files
  both passed integrity checks with zero altered files; the user's Paint
  configuration checksum remained unchanged.

## Installed Wayland checks

The upgraded offline r9 guest ran all 29 functional dialog cases plus
setup/cleanup: 31 passes, zero failures, in 3,877 ms. The QA executable resolved
the installed `/usr/lib/libaero7commondialogs.so.1`, without library-path or
preload overrides. Its test profile was isolated from the normal user's files.

Paint 8 compatibility was repeated against installed Explorer 37. All five
document workflows passed: same window, separate window, unsaved Cancel,
unsaved Discard and unsaved Save. Evidence is in the new isolated profile
`paint8-wayland-workflow.R4XEGX`, not the earlier Explorer 36 test profile.

Manual checks used Paint's real Open dialog: searching Pictures returned four
matching PNGs; Organize opened; Layout switched the results to List; selecting
JPEG-2000 filtered out those PNGs; clearing search returned the ordinary folder
view. Cancel preserved the original drawing, and Paint then closed normally.
This was not a manual round trip through every format or menu action.

Evidence root: `/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`.
Screenshots `141` through `148` record the manual interaction. Exported logs in
`results/` are `explorer37-common-dialogs.log`, `explorer37-paint8-compat.log`,
`explorer37-paint-open.log` and `explorer37-dialogs-audit.log`. The audit verified
all success markers, exported the profile and repeated package integrity checks:
Explorer 665 files and Paint 709 files, zero altered files. Missing repository
database warnings in this disconnected guest remain in the logs.

Search currently uses the pack's generic image icon, while the ordinary folder
view uses its specific PNG icon. Both are unchanged pack artwork, but that visual
difference remains. These are upgraded-guest results, not fresh final media.

## Remaining acceptance boundaries

Worker interruption is cooperative: a single kernel/filesystem call on a hung
network mount cannot be forcibly interrupted by Qt. The GUI does not wait on
it, but a replacement query waits for that worker to return. Missing/readability
checks cannot diagnose every low-level directory enumeration I/O error. Real
remote-mount failure tests and very large storage performance remain pending.
No whole-desktop or fresh-final-ISO acceptance follows from these source tests.
