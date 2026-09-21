# Snipping Tool notification handoff — 8 September 2026

## Reproduced failure

On the disconnected r10 offline VM (Desktop 29, theme 46, Spectacle
`1:6.7.4-2`), a real selected-region save deliberately directed to an
unwritable `/proc` path failed as expected. However, the expected Snipping Tool
error popup was replaced by a Notification Manager summary saying one
notification arrived while Do Not Disturb was active. Screenshot 107 records
the failure; it is not counted as a successful Try Again test.

The fullscreen selector can exit before Plasma clears its notification
inhibition. The Snipping Tool immediately sent its failure notification from
the process-finished callback. This is consistent with the observed race;
the baseline did not include a timestamped D-Bus inhibition trace.

Before fault injection, the actual installed Spectacle passed both independent
instance and normal instance tests: each saved a 1920×1080 PNG, then returned
exit 1 for an unwritable output, without timeout. Results are retained in
`r10-snipping-handoff-logs/offline-spectacle-probe.json`. No existing file or
directory permission was changed to induce failure.

## Change

The helper now checks Plasma's exported `Inhibited` notification property
asynchronously before sending either a saved or failed notification. If
inhibited, it retries at 50 ms intervals, with a one-second overall deadline.
It does not alter Do Not Disturb, clear another application's inhibition, or
elevate screenshot notifications to critical urgency. Persistent suppression
still receives normal notification/history delivery at the deadline. Missing
properties, unavailable servers and delayed replies cannot retain notifications
indefinitely.

Clipboard copying still occurs immediately after successful image decoding;
only notification delivery waits. Each notification keeps its original image
path and action. Owner destruction cancels pending delivery, and late callbacks
cannot send a notification twice.

Source tests cover immediate delivery, transient inhibition, persistent
inhibition, absent and late replies, and destruction while pending. All four
Snipping Tool CTest groups passed (notification gate, capture status, approved
icon independence and icon policy). No icons were created or replaced.

## Candidate binary VM replay

The source-built candidate ran in a temporary user service, not over the
installed binary. The QA-only fail-once fixture changed only the first output
path, then executed the installed Spectacle unchanged for retry.

- Screenshots 109 and 111 show the actual **Snipping Tool** error and **Try
  Again** action, rather than the inhibited-notification summary.
- The first manual click occurred after the transient popup expired; screenshot
  110 is not a passing retry. A second controlled run captured the error and
  clicked its action immediately in the same input sequence.
- Screenshot 112 shows that **Try Again** reopened selection. Releasing the
  rectangular selection closed the overlay and displayed **Screenshot saved**
  (113), without the Spectacle editor opening.
- Clicking that notification opened the same saved image in the default viewer
  (114): `Screenshot 2026-09-08 15.02.59.341-340101.png`, 321×231 pixels,
  SHA-256 `5c30e636309d5e66f40c0bffbdc0b39452154128d86d98da6684cc3a728aed5b`.
- Real Ctrl+V pasted the image into Paint (116). For pixel verification only,
  Paint's Ctrl+T cropped its initially larger canvas to the pasted selection;
  Ctrl+S saved `gated-retry-pasted.png`. ImageMagick comparison reported **zero
  differing pixels** against the screenshot. Screenshot 118 records the save.

The VM had no network adapter throughout. The test fixture restores the normal
autostart service and verifies that neither QA override remains in its process
environment. Installed binaries are hashed before and after the fixture.

## Packaging and release boundary

The theme recipe has a focused notification-handoff patch and release 47
metadata. The first build workspace inadvertently included old prepared source;
prepare correctly stopped on existing patched files. A second, empty workspace
uses only recipe files and the cached pinned Git source. The prepared helper
source matches the tested source exactly.

The clean package build completed successfully: 16/16 CTest groups and 10/10
greeter-layout cases passed. Existing upstream build/QML warnings remain in the
log; this is not a warning-free build claim. Comparing release 46 and 47 found
11 ELF files in each and no changed direct library dependencies.

- Package: `aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-47-x86_64.pkg.tar.zst`
- Size: 5,145,186 bytes.
- SHA-256: `efe1f9d9163d82b48bc85408dd5ab3001cf9a300b973aec706481ebefadbb2ab`.
- Installed helper SHA-256:
  `28611e394962468b43c6b48b967c44516a038c968fb28d67ec87133a68d2668e`.

Normal `pacman -U` installation in the disconnected offline VM changed only
theme 46 to 47. Its file check reported 1,143 files, zero missing. The installed
package then passed the fail-once workflow: visible error (121), Try Again
selector (122), saved notification (123), and correct default viewer (124).
Actual Ctrl+V into Paint (127) and saving the cropped pasted selection (129)
again produced zero differing pixels against the saved 341×261 screenshot,
`Screenshot 2026-09-08 15.15.52.873-da5024.png`, SHA-256
`31eb439ac5ceac3e8be16c866388efcf8040f4267a9e5b3a065f1585c4b38623`.

Escape after visually confirmed selector readiness (130) closed the overlay
(131). Before/after audits contain exactly the same four screenshot paths and
hashes, with no additional PNG. All four installed Spectacle background probes
also passed. These are installed-package checks, not only source tests.

The packaged fixture exited successfully and restored the normal installed
helper without either QA environment override. A subsequent user-manager
daemon reload and normal service restart passed. The final audit retains zero
failed system units and one failed user unit: `aero7-update-check.service`,
whose journal reports unknown package availability in the no-network guest.
That failure was not cleared or represented as a successful update check.
The normal helper hash and all 1,143 package files were verified again.

The repository's checked recipe registry now matches the tested theme-47,
Paint-9 and Programs-Center-3 recipes. Source pins remain unchanged, and
`tests/validate-repo.py` passes. These recipe hashes are separate from the
frozen ISO manifests.

Frozen r10 ISO manifests and images have not been promoted or rebuilt. No
commit, push or publication was made. Final-media acceptance remains pending.

This change does not fix Escape pressed before the selector obtains keyboard
focus. Spectacle creates capture windows after the initial screen image is
available; the earlier controlled early-input failure remains open. It also
does not certify full desktop, screenshot multi-monitor, accessibility or
release acceptance.
