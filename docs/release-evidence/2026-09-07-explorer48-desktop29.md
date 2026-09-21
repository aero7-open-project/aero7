# Explorer 48 breadcrumbs and Desktop 29 indexer identity

Local component and installed-VM evidence. Not final ISO acceptance or release
approval. Both packages remain local QA candidates, not published packages.

## Explorer 48

Candidate directory: `work/beta2-explorer48.dTOVsK/`.

- Package: `aero7-file-explorer-25.12.3-48-x86_64.pkg.tar.zst`.
- SHA-256: `60d5074d4dd262e37c8399c1f9037454c0c4f4e3f8de03730f8da60c3ef0933e`.
- All 20 source CTest suites passed in 26.16 seconds.
- All 14 packaged ELF direct-library requirements match Explorer 47.
- Normal upgrade from 47 in the disconnected, installed r9 offline VM passed.
- Installed common dialogs passed 49 cases including setup/cleanup (47
  functional), zero failures/skips, in 5125ms. The unchanged test executable
  resolves installed libraries, not a build-tree replacement.
- Paint 8 passed five isolated-profile workflows again; the actual user's
  preferences remained unchanged.

Main Explorer breadcrumbs now hide removable-drive mount-container ancestors
and show the drive label followed by relative folders. The helper picks the
longest permitted mount-root match with directory-boundary checks; it does not
match prefix siblings or invent persistent drive identities. Existing native
breadcrumb buttons retain their actual navigation targets. Live mount changes
refresh the presentation.

At 1920×1080, the actual virtual USB sequence verified:

1. The unmounted Computer tile opens the drive through native setup (`467`,
   `468`), with `AERO7_QA (D:)` as its root breadcrumb.
2. Opening nested folders shows `AERO7_QA (D:) > Photos > Trips` (`469`).
3. Clicking the root breadcrumb returns to the real USB files (`470`).
4. Local Disk (C:) still opens the system root with its normal label (`471`).
5. Back returns to the USB root with the correct label (`472`).

The fixture is a 96 MiB FAT virtual USB device, UUID `F921-93DA`. It was normally
unmounted after testing. The combined audit confirms no mounted fixture; QMP
device removal then completed before closing its block node. A subsequent host
FAT directory check found the original 314-byte README and the deliberately
added `Photos/Trips` test folders, with 100,442,112 bytes free. The image remains
available for future tests. No physical-drive claim follows from this fixture.

## Desktop 29: Baloo portal identity

Candidate directory: `work/beta2-desktop29.33Niy7/`.

- Package: `aero7-desktop-0.2.0-29-x86_64.pkg.tar.zst`.
- SHA-256: `56022d1d2689f02595ec8831847a340ef1ebf877c147a78245a54034ea58ad5d`.
- All seven source suites passed; all seven package-build suites passed again
  in 15.13 seconds.

The installed Baloo worker requested app ID `org.kde.baloo`, but the installed
Baloo package supplied no matching application desktop entry. The portal
reported `App info not found for 'org.kde.baloo'`. This was reproduced using
the real `/usr/lib/kf6/baloo_file_extractor`, not a mock Qt application.

An A–B–A test established the targeted cause: absent entry produced the warning;
a temporary hidden matching entry removed it; removing only that test entry
restored the warning. The temporary user-local entry was removed afterwards.
The worker received no document IDs. Its event loop ran for two seconds and
exited on input EOF; this checks registration, not document indexing. The
[upstream worker entry point](https://raw.githubusercontent.com/KDE/baloo/master/src/file/extractor/main.cpp)
and [input/batch implementation](https://raw.githubusercontent.com/KDE/baloo/master/src/file/extractor/app.cpp)
explain that probe boundary.

Desktop 29 installs a hidden `org.kde.baloo.desktop` compatibility identity in
`/usr/share/applications`, pointing to that existing worker. `NoDisplay=true`
keeps it out of Start. It adds no icon, autostart process, indexing policy or
warning-suppression environment setting.

Normal Desktop 28→29 upgrade preserved the shell PID and indexing preferences.
With the package-owned entry installed and no user-local override, three
consecutive launches of the actual worker passed registration without the
targeted portal warning. Desktop's 75 files, Explorer's 665, Paint's 709 and
Baloo's 758 all passed package checks with zero altered files. Zero failed
system units were reported. This does not establish a warning-free session.

## Retained evidence and remaining gates

Raw logs and selected screenshots are in [breadcrumb48-desktop29-logs](breadcrumb48-desktop29-logs/).
The final audit is `breadcrumb48-desktop29.YeYEFx/audit.log`, containing
`BREADCRUMB48_DESKTOP29_AUDIT_COMPLETE`. The A–B–A record is
`baloo-identity-probe.UGAWKs`; installed three-pass results are
`desktop29-baloo.zZq0LP`, both inside that audit directory.

No current ISO includes these candidates. Explorer 43 and Desktop 28 remain
the selected ISO inputs. Required work includes native setup cancellation and
denied/busy-device paths, multiple/physical/optical devices, common-dialog
address presentation, current-stack reboot, broader desktop recovery and both
fresh final-image installation matrices. No commit, push or publication.
