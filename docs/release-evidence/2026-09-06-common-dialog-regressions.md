# Common item dialog correctness pass

6 September 2026. Source and preview-binary checks only; no new Explorer package
or ISO was produced in this pass. No commit or publication.

## Why this precedes Paint integration

Paint currently calls QFileDialog for opening and KFileCustomDialog for saving.
The latter embeds image depth, quality, conversion and preview controls. Replacing
it with a plain pathname subprocess would lose those controls, so that is not an
acceptable integration. Aero7's existing common dialog also had independent
correctness defects, addressed here before extending its integration interface.

## Fixed and tested

- Filename changes now update Save-button availability, including a suggested
  filename and clearing the field.
- Direct/keyboard acceptance rejects an empty filename instead of returning a
  hidden `.png` destination when a default suffix is configured.
- Saved file-type preference is applied after callers supply their filter list;
  an unavailable preference falls back to an offered filter. Repeated filter
  updates no longer add duplicate signal connections.
- Filter parsing uses the final parenthesized pattern group, allowing a
  description such as `Images (editable) (*.png *.jpg)`.
- Computer entries use the existing Explorer storage-visibility predicate and
  a Local Disk (C:) label, excluding internal mounts from the navigation pane.
  Actual paths remain usable; this is presentation, not an access-control rule.

Canonical source: `aero7-desktop-workcopies/aero7-file-explorer/src/aero7/`.
Tests: `src/tests/aero7commondialogtest.cpp`, linked to the real dialog library.
Seven cases cover the above, save-path selection without creating an image,
and preservation of an existing file when overwrite is declined. Each process
uses temporary XDG directories and a temporary library database; it does not
materialize host user directories. CTest has a 20-second timeout.

Evidence: `work/beta2-common-dialog.CQ9O2J/`.
`aero7-common-dialog-before.log` contains three reproduced failures before the
fixes. The first expanded suite passed six cases. The storage test then failed
before the drive fix; `aero7-common-dialog-storage-after.log` passes the final
suite in 0.06 seconds. An offscreen-platform size-hint warning remains visible
in the overwrite-dialog test. This is not full Explorer regression acceptance.

## VM preview evidence

The offline r9 guest runs the uninstalled binaries from its read-only QA share,
with normal user appearance and an isolated application preference ID.
No installed Explorer files were replaced.

- First preview SHA-256:
  `688ebbbda9854b57522dc681773e55491c5749eb3a145f3a67edf05e611a66af`.
  Screenshots `offline/73-common-dialog-save-empty.png` and
  `74-common-dialog-save-enabled.png` show Save changing from disabled to enabled
  after typing. `75-common-dialog-accepted.png` shows the accepted path under
  the real Documents save location, with `.png` appended, and normal exit.
- Storage-corrected preview SHA-256:
  `98d9d3f574d4083a8a076eba69c2488ac12521adf86a7e0f319baa0d65ecdd83`.
  `offline/76-common-dialog-filtered-storage.png` shows Local Disk (C:) without
  `/run`, `/tmp`, the EFI partition or QA shares. No physical removable device
  or remote network mount was tested here.
- Selecting JPEG, accepting an explicit `.jpg` filename and reopening restored
  JPEG even though PNG was the first supplied filter:
  `offline/77-common-dialog-filter-restored.png`. The reopened dialog was then
  cancelled; no image file is created by this path-selection service.

VM evidence root: `/home/admin/VMs/aero7-beta2-r9-xTfYQR/`.

## Still open

Packaging, final-media inclusion and full common-dialog acceptance remain open.
Paint needs an integration interface that preserves its format/quality options.
Further review is needed for responsive search/filter behavior, real Organize
actions, and Windows-style breadcrumb/layout parity. The path and folder fixes
below still need package and final-media acceptance.
Do not advertise system-wide interception of third-party toolkit dialogs or full
Windows common-dialog parity on the strength of these tests.

## Follow-up: extensions, typed paths and real library destinations

Four further defects were reproduced in `aero7-common-path-before.log`:
JPEG selection appended `.png`, a typed existing pathname did not enable Open,
New folder created a directory in the materialized library instead of the real
save location, and a save inside a library subfolder returned the library root.

Corrections now:

- Use the selected filter's first concrete extension for an extensionless name;
  generic wildcard filters retain the caller's default, and explicit extensions
  are not rewritten.
- Accept typed existing files, navigate typed directories and clear stale
  selection when the user edits the filename.
- Create library folders in the real save location, refresh the merged view,
  and avoid implicitly recreating a missing library mount's parent directories.
- Resolve entered library subfolders to their real canonical folder rather
  than flattening saves to the library root.

The VM then exposed another independent bug: file-type filters hid directories.
`aero7-common-folder-filter-before.log` reproduces the invisible-directory result.
The model now retains all directories while filtering files. The final test
group has 15 cases and passes in 0.14 seconds. Five related CTest groups also
pass, including fresh/existing library profiles, icon independence and icon
policy (`aero7-common-related-tests.log`, 0.30 seconds). These are focused checks,
not the full Dolphin/application matrix. Logs are in the same evidence directory.

Additional uninstalled offline-VM previews:

- Path-fix binary SHA-256:
  `efa4c96ca709c0b1121f118c93302b16f5b3fbd6a3a4f5286aab5df529191f35`.
  `offline/86-common-path-nested.png` shows navigation into the newly created
  real Documents/New folder. `87-common-path-selected.png` confirms the returned
  destination ends in `Documents/New folder/dialog-path-qa.jpg`, although the
  caller's fallback extension was PNG. The service selected a path; it did not
  encode or write an image. The empty QA folder remains in the test account.
- Final folder-filter binary SHA-256:
  `03cef72c358bf13f30bd660be9630178938336d02d0c26610e2cbacbf6eb71e0`.
  `offline/88-common-visible-folder.png` shows the folder with the PNG filter
  active; `89-common-typed-open.png` shows an existing absolute PNG path enabling
  Open. All preview binaries are retained separately; none replaced the
  installed Explorer package.

`offline/90-common-typed-selected.png` confirms that Open returned the typed
existing PNG path and exited normally. The guarded filesystem audit verified
that New folder exists in the real Documents directory, its library entry is a
symlink to that directory, and the path-selection service did not create the
proposed JPEG. Exported logs are under `offline/results/`; the audit ends with
`COMMON_DIALOG_REAL_FOLDER_AND_PATH_RESULTS_VERIFIED_NOT_INSTALLED`.

One launch attempt reached the auto-lock password prompt rather than the
terminal; it is not application failure evidence (`80`–`82` captures). The
guest was unlocked normally before repeating the actual preview checks.

## Native Paint integration and dialog width — 6 September, evening

Status: **source and uninstalled VM previews tested; packaging pending**.

Explorer now builds `libaero7commondialogs.so.1`, with embedded existing icon-pack
resources and one shared library-state implementation. Its installed CMake SDK
exports `Aero7::CommonDialogs`. File-operation/property UI remains internal.
The common-dialog public API exposes selected-filter changes and an owned custom
widget area so callers retain their actual save-options and preview controls.

Paint's prepared source uses this API for local Open/Save As. It preserves the
existing save-options widget, conversion/quality settings, preview, selected
format, saved option defaults, lossiness checks and local-only restriction.
An explicit Network location button preserves the existing remote-protocol KIO
browser; a remote initial URL takes that existing route. This is intentionally
not a claim that remote UI is Aero7-native or that remote transfers were tested.
The native path remains local/mounted-network browsing.

Canonical integration artifacts are under
`aero7-desktop-workcopies/aero7-repo/packages/aero7-kolourpaint/`:

- `aero7-common-dialog.patch`:
  `03ede31258d775eb31a7cc4e5bf9610c892091ed894977d06477a168276cc0e8`.
- `aero7-common-dialog-probe.cpp`:
  `51bac7246e0c8a0ec4b7ad2b261832bdb4ce733ba1666bcc180d72bfd355e4af`.
- `aero7-common-dialog-test.sh`:
  `eba4bc7cb9eae4e5ac2abb1656bfca83ffd5bf3452e0794518da893af0f7a371`.

The patch dry-runs cleanly against the pinned Paint source with the existing r6
patches applied. It is **not yet wired into PKGBUILD/.SRCINFO**: Explorer must
first provide the shared library in a new package, then Paint must declare that
runtime dependency and include the patch/tests. Selected local packages remain
Explorer 35 and Paint 6; neither has this shared-library integration.

### Regression results

- Full Explorer build succeeds after the library split, including the real
  application and all test targets. All 19 CTest groups pass in an isolated
  configuration/offscreen session: final run 14.46 seconds. The common-dialog
  group now contains 19 functional cases (21 with init/cleanup).
- API tests cover effective filter notifications, custom-widget ownership,
  replacement, acceptance/cancellation lifetime and long-filter sizing.
- Real Paint action probe fails against packaged r6, as expected (old dialog).
  The integrated build passes PNG save, PNG open, cancellation, and explicit
  KIO-route cancellation with the original options widget still alive.
  The Save scenarios exercise PNG/JPEG switching, quality retention and the real
  image preview. These are not arbitrary-format encode/remote-transfer tests.
- The first remote-route test looked for a literal button prefix and missed
  KDE's inserted accelerator marker; the probe now ignores `&` in button labels.
  The initial failed run is retained, not hidden.
- VM screenshot 100 exposed an Open dialog stretched to the screen by the
  aggregate image filter. A new test reproduced a 3142-pixel minimum width.
  `AdjustToMinimumContentsLengthWithIcon` bounds that control's size hint. The
  new regression and all related suites pass after this correction.

Build/test/install logs are retained in `work/beta2-common-dialog.CQ9O2J/` with
the `aero7-native-` prefix. Real Paint per-scenario logs remain in
`/home/admin/.local/state/codex-desktop/tmp/aero7-native-paint.CEVZcu/` (final),
`JotDY4` (first passing integration), `2mYAGO` (accelerator-probe failure), and
`O9xlfv` (expected r6 failure). These are isolated QA profiles, not host defaults.

### VM acceptance evidence and limits

The offline r9 guest used its normal Wayland desktop configuration, without
installing the preview executable or replacing system libraries. Its package
versions remain those recorded in the prior manual-upgrade evidence.

- Paint executable SHA-256:
  `e2a32ae4c2aba883073f90b9db424a652f8b58ee1fa81284fdf0d26352ce7d3e`.
- Initial shared library SHA-256:
  `d081f109a2562035afe1233f5ca7dfb8779244039c3a9fea63a2ac71c56ed497`.
- Width-corrected library SHA-256:
  `9b43fd0cc125495da8d39be88b29e523b021e745fc98a82307b78bda77ccf9b3`.
- Both sets are retained separately in the VM's read-only input share.
- `offline/94-native-paint-save.png`: native PNG conversion controls and
  cleaned Computer list. `98-native-paint-quality-preview.png`: JPEG quality
  plus the actual preview. `99`/`101`: PNG destination and reopened document.
- `100`: confirmed over-wide Open dialog before correction. `103` still
  restores the previously saved oversized geometry; it is not a fixed-width
  screenshot. Manual resize in `104`–`106` demonstrates the corrected dialog
  can shrink below 900 pixels; the test independently verifies a fresh dialog.
  `107` confirms the same saved image reopens through the corrected dialog.
- Output `Pictures/native-dialog-paint.png` is a real 400×300 RGBA PNG:
  `261a70c5e3350a281ce0467ca4c4ffc5c44885515407876afbfade5eaa2a033b`.
  It is a blank QA image, not a new drawing-stroke validation.
- Both preview runs closed normally. Exported image/logs and
  `paint-common-dialog-audit.log` are under `offline/results/`, with marker
  `PAINT_NATIVE_DIALOG_VM_SAVE_REOPEN_AND_NORMAL_CLOSE_VERIFIED_NOT_INSTALLED`.
  The audit's initial negated `pgrep` guard was corrected after its run ended;
  the guarded audit was rerun. It does not change system packages.

Remaining work includes shared-library packaging/dependency closure, final ISO
rebuilds and fresh installation tests; responsive search; functional Organize
actions; breadcrumb/display-name and layout polish; oversized saved-geometry
handling; and genuine remote/file-format acceptance. The small inherited preview
window also elides its title. Do not claim full Windows parity or zero bugs.

### Follow-up: package and installed-guest checks

The subsequent [native-dialog package report](2026-09-06-native-dialog-packages.md)
records Explorer 36 and Paint 7/8 builds, ordinary offline-guest upgrades,
installed PNG save/reopen with zero decoded-pixel differences, normal closure,
and the new single-document default with five passing installed Wayland workflow
tests. These supersede the packaging-pending status above, but do not supersede
the outstanding common-dialog or final-media acceptance gates.
