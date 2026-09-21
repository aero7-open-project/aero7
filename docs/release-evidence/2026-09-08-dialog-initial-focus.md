# Explorer 53 — initial common-dialog keyboard focus

Status: source regression, full candidate package build, normal installed
upgrade and actual keyboard-only Save As/Open replay passed. This is not a
final ISO or repository promotion; no new reboot replay is claimed here.

Follow-up: [Explorer 54 and Theme 53](2026-09-08-panel-shadow-and-explorer-metadata.md)
subsequently correct the metadata warning and missing panel bindings. The
historical Explorer 53 results and limitations below are preserved as recorded.

## Reproduction and cause

On the disconnected 1920×1080 r10 Wayland guest, with Explorer 52 and Paint 9,
actual Ctrl+V successfully pasted a screenshot. Ctrl+S opened the Aero7 native
Save dialog, but typing did not enter a filename until the field was clicked.
After saving, a second Ctrl+Shift+S replay reproduced ignored initial typing;
that dialog was cancelled without writing another file.

The filename entry exists and works with mouse focus. The problem is the
initial keyboard target: the dialog constructor leaves Qt to choose the first
eligible widget, which is the breadcrumb QScrollArea. Five actual-widget
regressions reproduce this in Save (empty/suggested name), Open, multi-file
Open and folder selection. All five fail before the fix.

## Correction

At the end of construction, establish filename focus for file operations and
file-list focus for folder selection. Do not repeatedly refocus on directory
changes, search or mount refresh. Preserve the suggested-name selection so
typing immediately replaces it. No forced window activation, timeout loop,
new permission, branding change or external service is involved.

The regression sends text to the actual application focus widget without
clicking the filename field, verifies replacement of a suggested name, and
checks that a subsequent directory update does not steal search focus.
All five cases pass after the correction. The complete common-dialog test
binary reports 59 passed, zero failed, zero skipped. Expected offscreen
platform size-hint warnings are retained.

## Candidate provenance

- Candidate: `aero7-file-explorer` 25.12.3-53.
- Source archive: `aero7-file-explorer-25.12.3-r53.tar.gz`.
- Source SHA-256: `fc49b87b18871445ce8f821078bbaf4189087a5e1fed45060447aaef07230f15`.
- Only two extracted files differ from the Explorer 52 source archive:
  `src/aero7/aero7commondialog.cpp` and `src/tests/aero7commondialogtest.cpp`.
- Build runs from a fresh, checksum-verified extraction, with the existing
  package dependency declarations and normal CMake configuration preserved.
- As with the previous host build, makepkg's host dependency precheck is
  bypassed (`--nodeps`); no host dependencies are installed. The guarded VM
  installation must use normal dependency checking.

Baseline failures, fixed checks, full common-dialog results, recipe and guarded
installer: [dialog-focus-logs](dialog-focus-logs/).
The related [screenshot/notification evidence](2026-09-08-portal-installed-validation.md)
includes the GUI reproduction and pixel-exact Paint paste result.

## Completed package and installed result

The fresh build completed at 21:58:03 CEST with exit status 0. CTest reports
20/20 successful statuses, but the retained output shows that `appstreamtest`
returned early with “Not installed yet, skipping”. Count this as 19 executed
suites, not successful metadata validation. Direct `appstreamcli validate
--no-net` of the staged metadata reports a missing homepage URL warning and
content-rating/developer-info informational messages. The metadata is byte
identical to Explorer 52; this is a pre-existing, still-open packaging issue,
not a new focus regression. Do not hide it behind the CTest summary.

- Main package size: 8,290,085 bytes.
- Package SHA-256: `3b942d0e5253f430fc8eb2b800c59a013ca90ddb770bd9ad4ad601182ad5e0f6`.
- Installed common-dialog library SHA-256:
  `37c7e3b7b1940eaf03a19ac1e3f3e8dc31658de67da78aea4ca0a83ac496e6cc`.
- All seven shared libraries preserve the exact exported symbol inventories
  checked against Explorer 52 (names/versions/types/bindings/visibility/data
  sizes). This is not a complete C++ ABI proof.

Normal offline `pacman -U` at 22:00:11 installed the verified archive with
dependency checks enabled. All 665 package files are present and the installed
library hash matches. The first attempted terminal command instead reached an
idle-locked screen, producing an incorrect-password message; it did not run an
installation. The VM was unlocked normally with the test account password
before the command was issued to the visible terminal. No lock policy changed.

Paint was closed normally and reopened as PID 12093 at 22:01:08. Ctrl+Shift+S,
typing `explorer53-keyboard-save.png`, and Enter saved the file without a mouse
click inside the dialog. The output is byte-identical to `qt-paint-pasted.png`:
SHA-256 `e489d11c36c7b4a471f7f23ee993f249446a86370881b0378dfed8ae94d7b494`.
Ctrl+O then accepted an absolute file path through the initially focused field;
Enter opened that image. Screenshots 361–364 retain these actual GUI states.

The 22:04:20 audit `explorer53-focus.vXG99a` confirms installed versions,
non-deleted library mappings in the new Paint process, the library hash and
saved-file equality. Shell remains active. It also shows
`aero7-update-check.service` in failed state; the entire VM is therefore not
reported as free of failed units. The helper/portal/panel issues and final-media
gates remain open. The audit's earlier negative-grep guard was corrected to an
explicit failing condition and rerun; the retained result is from the corrected
script, which passes ShellCheck.

The retained update-check journal dates that failure to 21:46:23, before the
Explorer upgrade: the disconnected guest could not determine package
availability and exited 1. No update was installed and no failure state was
cleared. This needs separate offline-notification policy review, not attribution
to the common-dialog change.
