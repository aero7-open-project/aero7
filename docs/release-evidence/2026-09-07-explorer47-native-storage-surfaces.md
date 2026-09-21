# Explorer 47: native drive access across Computer and common dialogs

Local pre-release evidence, not final-media acceptance or publication approval.

## Candidate and compatibility

- Candidate: `work/beta2-explorer47.j0El48/`.
- Package: `aero7-file-explorer-25.12.3-47-x86_64.pkg.tar.zst`, 8,262,098 bytes.
- Package SHA-256: `56d5d90331ec9600063cb013876267d2e01c46c2c81075b7a5c9e8445edf2eb7`.
- Frozen source SHA-256: `c3eb2e9556882a82e848786ec4fd7f06dd0c33a5dd07048a70c02736dd75f16c`.
- Fresh extraction/checksum passed. The reused incremental source tree matches
  that extraction recursively; `prepared-source-comparison.log` is empty.
- All **20 local CTest suites passed**, in 25.01 seconds. New missing-device
  mouse and Enter regressions ensure no navigation, acceptance or filename loss.
- Existing exported Aero7 shared-library symbols are unchanged. The only direct
  dependency differences across the 14 packaged ELF files are the shared dialog
  library's added `libKF6KIOFileWidgets.so.6` and `libKF6Solid.so.6` dependencies.
  The package already requires `kio` and `solid`; no public header dependency or
  exported dialog class-size change was introduced.

Explorer 47 was normally installed over 46 in the existing offline VM
`aero7-r9-offline`, with no network device, at 1920×1080. Only Explorer changed.
Explorer's 665 files and Paint 8's 709 files pass package checks; saved Paint
preferences are unchanged. This is not a clean install of new release media.
Explorer 43 remains the selected ISO input; 47 is not published or selected yet.

## Implementation

A private, owner-scoped native device broker shares KFilePlacesModel/Solid
discovery and setup between Computer and the common file dialogs. Unmounted
removable filesystems use native device identifiers, never placeholder folder
paths or fabricated capacity. Explicitly ignored volumes, unmounted internal
partitions and foreign-user/system mount paths remain excluded.

Opening requests normal native setup and accepts only an accessible, permitted
local mount. It retains authorization checks and reports removal, failure or
timeout. Closing/hiding the owning surface or navigating elsewhere cancels
delayed navigation, not the operating system's in-flight filesystem operation.
Model notifications are coalesced before UI refresh. Live cancellation and
authorization-failure acceptance remain separate unverified cases.

The main Explorer view also contains the earlier external-unmount correction:
it returns home if the surviving ancestor would expose the raw mount container.
Deleting an ordinary folder or a subfolder on a still-mounted drive retains
normal nearest-existing-parent recovery.

## Installed dialog and Paint regression tests

The standalone test executable resolves the installed
`/usr/lib/libaero7commondialogs.so.1`, without a build-tree RPATH/RUNPATH or
LD_LIBRARY_PATH/LD_PRELOAD override. Its SHA-256 is
`c892fd5a41c8ed4933b204bd835b524e4cb4fa4bc3967485e16f7f6373d422c4`.

`explorer47-common-dialogs.O825Qq` reports **49 passes, zero failures** including
setup/cleanup: 47 functional cases, 5119ms. The unchanged installed Paint 8
passes the same five instrumented Wayland workflows: same-window open,
separate-window open, unsaved cancel, discard and save. Its isolated profile
evidence is `paint8-readiness-workflow.CWbPGw`. The post-test audit confirms clean
package files, unchanged user preferences and no remaining Paint process.

## Actual virtual USB checks

The same 96 MiB FAT USB fixture was attached through QMP, without a terminal
mount before the Computer test. UUID `F921-93DA`, label `AERO7_QA`, serial
`AERO7QA96`; normal mounted location `/run/media/aero7test/AERO7_QA`.

1. **Computer discovery and setup:** unmounted AERO7_QA appears in the removable
   group with “Click to open” and no invented capacity (`447`). One click on its
   name performs setup and shows the actual README (`448`).
2. **External unmount recovery:** normal non-root UDisks unmount at 22:46:59
   returns the main Explorer view to the user's home with a warning (`450`),
   not the raw `/run/media/aero7test` directory seen in Explorer 46.
3. **Save As discovery and setup:** the unmounted drive appears under Computer
   (`451`). One click mounts it and shows README (`452`); `usb47-check.png`
   remains in the filename field, with the dialog still open and no save.
4. **Open-dialog unmount:** normal UDisks unmount at 22:48:47 hides cached files,
   disables Save/search and keeps the filename (`454`). The unmounted device
   remains available in the navigation tree.
5. **Keyboard recovery:** selecting that device with Down and pressing Enter
   remounts it, restores its README and enables Save (`455`, `456`), without
   accepting the dialog. Cancel subsequently closes the dialog.

The screenshot sequence is VM QA evidence, not approved promotional imagery.
An audit command was initially typed into Explorer's filter after a taskbar
click minimized the terminal. It did not execute there; terminal focus was
visually rechecked before retrying. Do not treat that input-driver error as an
installation or storage failure (`457`, `458`).

## Post-test audit and safe detach

`usb47-logs/storage47-audit.eNLNX3/` records the final normal unmount at
22:52:12, no mounted fixture filesystem, zero failed system units, clean
Explorer/Paint package checks and unchanged Paint preferences. The canceled
Save As result log is empty. QMP device removal completed before closing the
backing block node; a subsequent host FAT directory check finds only the
original 314-byte README, no PNG or new folder, with 100,446,208 bytes free.
The USB fixture image is retained for later tests.

The Explorer UI log is empty. The session journal still contains repeated
Baloo portal app-ID registration failures (`org.kde.baloo`); those messages
have not been resolved or accepted as harmless here. Do not call the entire
session log clean. Collected raw logs and selected screenshots are under
`usb47-logs/` beside this report.

## Still required

- Native mount cancellation, authorization denial, busy-device failure,
  physical hardware and optical-media testing.
- More than one removable drive, identity/selection continuity and mount-aware
  breadcrumbs. The current USB breadcrumb/address still exposes the Linux path.
- Broader recovery and desktop acceptance, both rebuilt final online/offline
  ISO installs, final logs and approved 1920×1080 promotional screenshots.
- Explicit approval before GitHub commits/pushes or release publication.

No claim is made that every Beta 2 bug is fixed. No commit, push, signing,
website publication or ISO upload occurred in this pass.
