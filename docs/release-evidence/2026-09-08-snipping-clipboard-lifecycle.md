# Screenshot clipboard lifetime — 8 September 2026

Status: source correction, controlled comparison, normal package 52 installation
and post-reboot capture/clipboard/cancellation checks verified. Final-media
acceptance remains pending.
The separate cold-login portal warning is not fixed by this change.

## Cause and compatibility

Plasma 6.7.4 defaults to ignoring ordinary image history. Its HistoryModel skips
image-only clipboard data unless it carries `x-kde-force-image-copy`.
[Spectacle 6.7.4](https://github.com/KDE/spectacle/blob/v6.7.4/src/ExportManager.cpp)
already supplies that marker for explicit screenshot copies. The Aero7 helper
supplied actual image/PNG data, but omitted this handoff. The image was therefore
available while the helper owned it and lost when that helper stopped.

The new `CaptureClipboardData.h` builds the same image and PNG payload with
Spectacle's explicit-copy marker. Invalid images/PNG encoding failure produce
no replacement payload. A focused test checks null input, required MIME formats,
absence of filename/text/URL substitutes, and exact RGBA image pixels.
All seven focused screenshot test groups pass. The first build command refreshed
CMake and built the helper, then failed to find the newly added test target in
the old Make invocation; a new invocation built the test and ran all seven.
Existing CMake configuration warnings remain recorded, not suppressed.

No global Klipper configuration is changed. This is not a claim that screenshots
are absent from history: copied screenshots can now be retained by the desktop
clipboard manager, including its configured persistent history. Clearing that
history does not delete the separately saved Screenshots PNG. There is no
additional Aero7 clipboard cache, last-file replay or startup image restoration.

## Controlled VM comparison

Guest: `aero7-r10-offline`, Wayland, 1920×1080, installed theme 51. The normal
helper and Spectacle binaries were preserved. A temporary user unit ran only
the candidate executable; normal service restoration was checked afterward.

- Installed helper SHA-256: `b8773ea8ae4a830ecd1703dd4d7a71b461bf182bdd660f7437ecdf147cc886bc`.
- Candidate helper SHA-256: `92638e602dee73beecd8a64a9cefd07dab74f42a403e661d246df0ef57466031`.
- Baseline replay: `snipping-clipboard-baseline.ZuEl3e`. A real region capture
  matched the clipboard pixel-for-pixel before stopping the normal helper.
  After stopping it, the probe reported `NO_IMAGE_ON_CLIPBOARD`, status 5.
  The fixture restored the normal service and exited 0.
- Candidate replay: `snipping-clipboard-candidate.efulLt`, invocation
  `6b3b0c3d11534bfc849f6cb0b341889f`. A real capture matched before producer exit,
  after exit and after starting the installed normal helper. All three image
  comparisons passed. The normal helper/binary hashes were restored unchanged.
- Both captures were 343×203, PNG SHA-256
  `1d3cf93bae5b3271daa880146fe0c6cfc64f8f6d74e45cd37577e31cb46c4d16`;
  canonical RGBA pixel SHA-256
  `aa28d2c6b2272c846c42a94c8747b4bdd86f7f7b5c44c25a3cf806c261857f35`.
  Baseline filename: `Screenshot 2026-09-08 19.26.42.980-4edf1d.png`.
  Candidate filename: `Screenshot 2026-09-08 19.28.03.590-e74727.png`.

### Preserved test-harness failures

After the candidate had exited and the normal installed helper was restored,
Paint opened with an empty 400×300 document. Actual Ctrl+V pasted the 343×203
captured region (frames 307–308). The scratch document was discarded at the
save prompt; the original captured PNG was retained. This is a real application
paste in addition to the independent clipboard pixel comparisons.

Initial baseline fixture `snipping-clipboard-baseline.WJVGTN` timed out after
printing a successful image comparison, before testing producer termination.
The diagnostic probe exited the event loop before KSystemClipboard's queued
read-lock release. Its teardown blocked. The probe now queues application exit
after returning to the event loop; the baseline replay above completed normally.
This is a corrected probe lifecycle error, not proof of an Aero7 helper hang.

The first candidate fixture's final cleanup tried to stop its already collected
temporary unit a second time and labelled restoration status 1. Actual normal
service restoration and the three image comparisons passed. Cleanup now checks
the unit's LoadState before stopping it; this first result is retained rather
than rewritten into an all-green fixture claim.

## Package 52 and installation

Build `work/beta2-theme52.2U8uTy` finished at 19:34:16 CEST after all 19 CTest
groups and ten isolated greeter tests passed. Prepared screenshot source exactly
matches the maintained tree. All 11 ELF direct-library requirement sets matched
51; non-ELF payload assets were unchanged. Branding/repeated-setup checks passed.
The inherited compiler/QML/build-directory warnings remain in the full log.

- Package: `aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-52-x86_64.pkg.tar.zst`.
- Bytes: `5151962`.
- Package SHA-256: `fee70b726e364f944ba41d6ab7f355697824a839fb9d883f5d2833917a6543bd`.
- Installed helper SHA-256: `533b1e4cfdf8b4210d64ee4f2fb89a47757c5ba3e9240f547ad29f8439235363`.
- Clipboard patch SHA-256: `74d04511619b5f05077bdb364f96c2d89d3c1624ae6d543cce6ecdc522f327e0`.

The normal offline upgrade changed only theme 51 to 52. All 1,147 installed
paths were present. Normal helper and desktop service checks passed before
reboot. The no-network update checker retained its expected failed state;
no blanket failure reset was used. The system failed-unit list was empty.

## Post-reboot verification and remaining boundaries

Post-reboot installed checks reached boot `7effdcc5-f4f4-44b7-958c-f5c10df546b1`
with the installed helper active, `NRestarts=0`, its normal recovery drop-in and
both system/user failed-unit lists empty. The duplicate portal-registration
warning remained visible in the helper journal; it is not suppressed or fixed.

Fixture `snipping-clipboard-installed52.YlWVGs` recorded a new 343×203 capture,
`Screenshot 2026-09-08 19.40.04.354-e93414.png`, with the PNG and canonical pixel
hashes listed above. The selector closed and the saved notification appeared
(frame 314); clicking its body opened that exact PNG in the default viewer
(frame 315). Exact clipboard pixels matched before stopping the installed
helper, after it stopped and after the normal service restarted. The fixture
restored normal operation and exited 0. No clipboard preferences were changed.

Cancellation fixture `theme52-cancel.T3fKgi` then tested Escape at 50, 300, 650
and 1,250 ms. Both selector-toolbar regions matched the verified idle frame
before each recovery key, with zero changed pixels. PNG inventories were equal,
the installed helper PID stayed unchanged, no backend child remained, and the
clipboard matched the same saved image exactly before and after all four attempts.

Finally, actual Ctrl+V pasted the same 343×203 region into a new empty Paint
document after the installed-helper restart and cancellation replay (frames
317–318). This confirms the normal application paste path as well as the probe.

The local repository recipe and `.SRCINFO` now match the tested package-52
inputs, including the clipboard patch hash. No commit, push, signed repository
promotion, frozen-ISO modification or publication was performed.

Final images still need the corrected packages and end-to-end tests.
Do not claim clipboard survival through arbitrary crashes
before Plasma has received the payload, logout, shutdown or cleared history.
