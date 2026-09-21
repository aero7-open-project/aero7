# Early screenshot cancellation — source candidate and VM replay

Date: 8 September 2026. Status: **releases 48 and 49 held: 49 passed ordinary
timing/reboot checks but failed forced-crash recovery. A startup cleanup and
automatic-restart candidate is under test**.

The original source-candidate results below remain valid for their recorded
runs, but do not establish reliable cancellation across the focus transition.
See the later package replay and correction at the end of this report.

## Original cause and focus-window correction (historical candidate)

Spectacle creates its region-selection window after the initial screen image
arrives. Escape pressed during that preparation interval previously reached
the application underneath instead of cancelling the pending capture.

The first AeroThemePlasma Snipping Tool candidate created a transparent,
temporary tool window while preparing capture. It handles Escape locally and
releases focus when Spectacle's real selector activates. It does not register
a global Escape shortcut, add artwork, or replace the screenshot backend.
The release-49 correction described below additionally uses a capture-only
global Escape binding; this original focus-only design was insufficient.

The preparation window has a ten-second deadline. Cancellation or timeout
requests termination of the owned backend process, escalating to kill after
500 ms if needed. A capture-generation check prevents that delayed kill from
affecting a subsequent capture. Cancelled attempts do not copy an image or
send a saved notification; any output created by that owned attempt is removed.
The real selection session is not subject to the preparation deadline once
focus has been handed over.

Changed source under `aerothemeplasma/helpers/snippingtool`:

- `PendingCaptureWindow.h`: temporary focus surface, Escape and deadline.
- `main.cpp`: process cancellation, bounded shutdown and guarded queue handling.
- `tests/PendingCaptureWindowTest.cpp`: pre-activation Escape, stale activation,
  unrelated input, focus handoff, timeout and disarm cases.
- `CMakeLists.txt`: register the new focused test.

## Exact candidate and test environment

Candidate executable SHA-256:
`a94c95038b9b6190653953a2dc089b991c822d0386a51253df48dc1ebb1d3db5`.

Built from the maintained helper source and temporarily run from the read-only
QA share in the disconnected r10 offline VM. The normal autostart helper was
stopped only for each bounded fixture, then restored. No installed executable
was replaced. Every fixture checked the installed Snipping Tool and Spectacle
hashes before/after and reported restoration status 0.

VM: 1920×1080, Wayland, 6 GiB RAM, two virtual CPUs, no network adapter;
installed Desktop 30, Explorer 52, Theme 47, Paint 9 and Programs Center 3.
These installed component versions are already newer than the frozen r10 ISOs.

## Verified results

| Check | Result and evidence |
| --- | --- |
| Focused source tests | All five Snipping Tool CTest groups passed; final replay took 0.73 seconds. This is not a full theme-package test run. |
| Early Escape | Key-only replay at 50, 300, 650 and 1,250 ms after Meta+Shift+S. All four captured screens show the desktop, not a lingering selector. The cancellation fixture's before/after PNG inventories and hashes match. |
| Normal selection | Real selector appeared. Dragging from (200,200) to (520,380) saved a 321×181 PNG on release and closed the overlay without opening the Spectacle editor. |
| Saved notification | Plasma displayed the saved notification. A prompt click in the repeat replay opened the corresponding timestamped PNG in the configured image viewer. The first click was too late after notification expiry; that attempt is retained, not counted as open success. |
| Real clipboard paste | Ctrl+V into a fresh Paint document pasted the 321×181 image while the candidate helper was active. A subsequent early cancellation left that image available for another Ctrl+V. Screenshots 228 and 229 record both. No clipboard byte/hash comparison is claimed for this replay. |
| Stalled backend | A scoped QA Python child ignored SIGTERM and never created a selector. The ten-second preparation timeout closed the input window, showed a failure/Try Again notification and killed the stuck child. The fixture found no remaining backend child and no new PNG. Two attempts logged the expected timeout reason. |
| Restoration | Normal helper active again; installed executable hashes unchanged. Temporary service invocation journals and every fixture's restoration status are retained. |

Two repeated wallpaper captures from the first positive fixture have identical
PNG file SHA-256 `1ec4149d4b5abcdbea400be182966dbbb78be076d8aae75fae9423ac270cdfce`.
This establishes repeatability of those saved files, not a clipboard comparison.

The VM does not have `wl-paste`. The optional clipboard-hash branch in the
fixture was therefore skipped. Stopping the temporary helper also releases its
clipboard ownership, so the valid paste replay was performed with the helper
still active. Do not report the earlier post-restoration blank Paint window as
a successful paste, or claim clipboard persistence across helper replacement.

## Evidence locations

Preserved alongside this report in `snipping-early-cancel-logs/`:

- `focus-final-escape-inputs.jsonl` and four timing screenshots.
- `snipping-focus.UHzvhS`: early cancellation inventory and journal.
- `snipping-focus.5CKdWO`: save/open replay inventory and journal.
- `snipping-focus.n7my0s`: Paint paste and subsequent cancellation replay.
- `snipping-focus-timeout.eXNbVF`: timeout reason, no-child check and restoration.
- Screenshots 222–232, the screenshot audit, build/test logs and QA fixture sources.

Original QA workspace: `/home/admin/VMs/aero7-beta2-r10-oTmJ9G`.
The test scripts are fixtures, not software installed into the product.

## Remaining gates

Build the promoted theme package from the exact reviewed source, run its full
suite, verify normal upgrade/reboot, and replay on both final ISO variants.
Stress rapid repeat/cancel/queue races, failed backend startup, focus switching,
slow hardware and multiple monitors. The 50 ms QMP replay does not prove every
possible input timing on every machine. Existing Spectacle QML warnings remain
in the journal; no clean-journal or whole-desktop acceptance claim is made.

The frozen r10 ISOs and their manifests/hashes are unchanged. No commit, push,
wiki update, release publication or download enablement was performed.

## Later package replay: release 48 is NOT accepted

A clean build from the pinned source plus a focused early-cancel patch passed
all 17 registered CTest cases and all ten greeter-layout cases. Prepared helper
source matched the previously tested candidate exactly. Package assets, file
inventory, declared dependencies and all eleven ELF direct-dependency lists
matched release 47. Rebuilt ELF bytes and package metadata differ as expected.
The branding/repeat-setup verifier passed. Existing upstream compiler warnings
and embedded build-directory references remain in the log.

- Package: `aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-48-x86_64.pkg.tar.zst`
- Size: 5,152,402 bytes.
- SHA-256: `fe569524b66ac1a678fb1ec9ee1f2df24120885058df6a0ad9dbea314f6067bd`.
- Installed helper: `579349ab5e6aadf02b3b0d5246b2f07e4c223eef053e4405f82b5fd458ee55a3`.
- Build workspace: `work/beta2-theme48.aGi4pd`.

Normal offline `pacman -U` changed only theme 47 to 48; the package file check
reported 1,143 files and zero missing. No installed-file overrides were used.
However, the installed keyboard replay **failed at 1,250 ms**: the screenshot
`theme48-escape-1250ms.png` shows a remaining selector. The 50/300/650 ms frames
show cancellation. The replay script subsequently sends a recovery Escape;
therefore its no-new-file/no-child checks alone do not prove timely cancellation.
Its old `THEME48_INSTALLED_CANCELLATION_PASSED` marker is misleading and must
not be treated as acceptance. The fixture's future marker has been narrowed
to the properties it actually checks. Original logs are preserved.

Release 48 remains installed only in this test VM for diagnosis. It has not
been promoted to repository recipes, release manifests or ISO images. Reboot
acceptance was not attempted after the failure. The offline update-check
service failure and the autostart-unit reload warning are retained, not hidden.

## Revised source: capture-only Escape binding

Focus-only handling has a transition interval between the temporary surface
and Spectacle's selector. The revised helper requests an Escape binding only
while its owned capture is running. It unregisters that action on cancellation,
normal finish or startup failure, using the existing KGlobalAccel dependency.
The preparation window/deadline and bounded child shutdown remain in place.
The API's registered-key query and shortcut removal are documented in
[KDE's KGlobalAccel reference](https://api.kde.org/kglobalaccel.html).

The first revised candidate (`5cd381e9f0233a75af6d76adf73f3b014ae19d9c0652684ea4a4e35e0ba814fc`)
passed the four timing replays. An independent observer recorded Escape as
FREE, then owned by `cancelActiveCapture`, then FREE after cancellation; the
same ownership/release sequence occurred for a real saved selection. The saved
notification appeared without an editor. These are runtime observations, not
an assumption based solely on calling the removal API.

An occupied-key fixture showed that merely avoiding `stealShortcutSystemwide`
was insufficient to avoid an additional registration: both owners were listed,
although the existing fixture action continued receiving Escape. The source now
checks for an existing registration first and skips its capture binding when
occupied. The explicit collision replay for the resulting candidate
`8a9329d502a7e9a7b34e016feba9a5e4584e2ef96e0bd4ed51fb2e3cb75ae374`
listed only the existing QA owner, delivered Escape to that owner, and retained
the selector's mouse Cancel action. That fixture restored the normal helper.
An existing user-defined global Escape action takes precedence; this collision
case is not claimed to provide keyboard cancellation through the new binding.

At this stage the revised source was not packaged. Complete its repeated timing, lifecycle,
startup-failure and rapid-queue checks, then rebuild and repeat installed and
reboot tests. Neither a passing source run nor the rejected release-48 package
is a substitute for that gate.

The final collision-aware candidate subsequently passed another four timing
frames at 50/300/650/1,250 ms (`focus-scoped-v2-escape-*`), with matching before/
after PNG inventories and normal-helper restoration. A missing-backend fixture
displayed the failure/Try Again notification and left Escape unreserved after
startup failure (`238-scoped-start-failure.png`). All five focused source CTest
cases still pass; their scope is unchanged and does not itself test KGlobalAccel
ownership. Ownership evidence comes from the separate live VM observer.

Current copied artifacts include `theme48-replay/` with the rejected package
build/review/upgrade logs, the original timing failure, and unchanged-file
checks. The `scoped-binding-*` logs and revised fixture sources retain the
later ownership/conflict/failure tests. Every intermediate result remains
distinguishable from the final candidate by its recorded executable hash.

## Release 49 — installed follow-up

The clean package build finished at 18:00:17 CEST on 8 September. All 17 CTest
groups and ten isolated greeter cases passed. The branding/repeated-setup
verifier passed. All eleven ELF files retained their direct library requirements
relative to release 47; the non-ELF assets and installed path inventory are
unchanged. Build metadata and rebuilt ELF bytes differ. Existing upstream build
warnings and package build-directory-reference warnings are retained in the log.

- Package: `aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-49-x86_64.pkg.tar.zst`
- Bytes: `5153433`
- Package SHA-256: `27ae116ab30f62629dd45ee6aab25616de3cf86a49e5effefe12191fe3281133`
- Installed helper SHA-256: `2dc8dbb5de09483fa3157764f9669c15cf8ee8b1cfc1b8fdde5c7fe3e5c1f481`
- Consolidated patch SHA-256: `293a8443651364428ad5f57542543d13cd878f2baec4c4c15f1b43c09126c911`

Normal offline-guest upgrade changed only theme 48 to 49, with all 1,143 package
files present and the installed helper running from `/usr/bin`. User service
definitions were reloaded before restarting the normal helper. No candidate
binary or backend override was used for this replay.

The four initial installed timings (50, 300, 650 and 1,250 ms) passed. A further
ten attempts repeated 50/300/650/1,250/1,800 ms twice. Before/after PNG inventories
matched, the helper PID stayed unchanged, and no backend child remained. The
frames recorded **before** recovery Escape show no selector toolbar. The new
image checker compares both toolbar areas with the verified idle frame; all
fourteen frames had zero changed pixels in those regions. Its negative control
correctly rejected the known theme-48 1,250 ms failure. This detects visible
selector residue, not invisible focus ownership or clipboard preservation.

Real installed capture saved PNGs without opening an editor. An initial
notification click arrived after the notification faded and did not open a
viewer; it is not counted as a successful click. A fresh capture followed by a
timely notification click opened `Screenshot 2026-09-08 18.07.02.181-3556ed.png`
in the default viewer at 322 by 182 pixels. Starting Paint with no file argument
and pressing Ctrl+V pasted that actual image as a 322 by 182 selection. This
replay is visual image-paste evidence, not a newly measured pixel-identity test.
The scratch Paint document was discarded; the original screenshot remains.

The normal reboot reached the full-logo greeter and password login. The new
boot ID is `334c39a0-b460-4eb3-a5ab-1bb0fa318a0f`; the installed audit passed with
the normal helper and shell active, no QA backend override and no temporary
candidate service. Further cancellation and crash-lifecycle checks follow.
The frozen r10 images and their release manifests are still unchanged.

### Forced-crash regression — release 49 held

Four additional post-reboot timings passed with unchanged PNG inventories.
However, deliberately sending SIGKILL to the guest's exact normal screenshot
unit at 18:12:50 exposed a separate lifecycle failure. KGlobalAccel retained
`aero7-snipping-tool/cancelActiveCapture` after the helper died and after it was
manually started again. A new screenshot at 18:13:27 logged that capture Escape
was unavailable; the post-Escape frame still showed the selector. Recovery
input eventually closed it. The fixture's PNG lists matched at 18:13:55, but
the later restored-state audit contains `Screenshot 2026-09-08 18.13.27.898-d00ffe.png`.
Thus that bounded snapshot did not establish that recovery left no late output;
the recovery mouse/Enter sequence must not be described as a clean cancellation.
The new fixture also checks that no backend child remains before completing.
The normal helper was restored, but this is a failed ownership/recovery replay.

Release 49 must not be selected for final media. The revised source now
registers **only its own internal cancellation action** with an empty shortcut
at startup, then unregisters it. It does not purge the whole component or change
another application's bindings. A narrowly scoped user-service drop-in sets
`Restart=on-failure` and `RestartSec=1s` for the desktop's generated screenshot
autostart unit. Explicit stop/logout is not intended to trigger a restart;
normal service start-rate limits remain in force.

The first rebuilt recovery candidate has SHA-256
`79195d43d4764ce2078ab61b152e926ed8fdd2d4341f0527c1d09b3f99be9635`.
Its five existing source tests pass; those tests do not verify global shortcut
ownership or systemd restart behavior. The separate live fixture records these
properties using the real candidate and an independent key-registration probe.

Fixture `snipping-restart.m6iD2D` observed the stale release-49 registration being
removed on candidate startup at 18:15:54.244. After SIGKILL at 18:15:58, systemd
automatically restarted the candidate once (`NRestarts=1`), and Escape became
FREE again at 18:15:59.656. Four post-restart cancellation frames at
50/300/650/1,250 ms all passed the toolbar check while the candidate remained
active. The registration observer's 45-second window ended before these four
later attempts, so it proves crash/startup cleanup, not each later key release.
No PNG was added, the replacement helper PID remained stable through the
replay, explicit fixture stop succeeded, and the normal installed helper was
restored with unchanged helper/backend hashes. The source candidate and its
transient restart policy are not yet an installed package/drop-in acceptance.

The recovery candidate's occupied-key replay (`scoped-binding-occupy.nniD6g.log`,
`snipping-focus.ZyyDyR`) registered only the pre-existing QA Escape action,
delivered Escape to that action and did not add a competing capture binding.
Mouse Cancel remained usable; after a separate Enter the normal helper was
restored with status 0. The initial attempt to start this fixture had malformed
terminal input and never launched; frame 257 records that harness error and is
not counted as an application test. Frames 258/259 and the successful fixture
logs distinguish the actual replay. The fixture's legacy `QA completion:
timeout` text also appears on blank Enter, so it is not itself proof of timeout.

Next gate: package the startup cleanup and service drop-in together, verify
the actual installed restart policy, repeat forced-crash recovery and collision
handling, exercise queued requests and save/retry paths, then rerun the normal
reboot and final-media workflows. Releases 48/49 and frozen r10 media are not
promoted by these source-candidate results.
