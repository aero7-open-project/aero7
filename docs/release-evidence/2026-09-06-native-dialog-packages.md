# Native dialog packages and installed-VM acceptance

Local QA only. Nothing committed, signed, promoted or published. Both immutable
r9 ISOs still contain Explorer 35 and Paint 3; the tests below do not certify a
fresh installation of the new packages.

## Explorer 36 and Paint 7

Explorer was built from a fresh prepared canonical source archive. Paint reused
its prepared source/build tree. Both builds skipped only the host dependency
precheck (`makepkg --nodeps`); compilation and package `check()` ran. No host
packages were installed. Paint used the staged common-dialog SDK at
`work/beta2-common-dialog.CQ9O2J/sdk`, not a host system installation.

| Package | Bytes | SHA-256 |
| --- | ---: | --- |
| `aero7-file-explorer-25.12.3-36-x86_64.pkg.tar.zst` | 8132026 | `73cef1c4d757d55cb8ecf31007a9a78d11dbf4cd05e661f2c7cea5a093dda10a` |
| `aero7-kolourpaint-25.12.3-7-x86_64.pkg.tar.zst` | 6619805 | `7abc9675ba7ed9d2c85442aa719e58418ffada3b480dddd15499d0b2126f6c49` |

Explorer's canonical source archive is `aero7-file-explorer-25.12.3-r36.tar.gz`,
SHA-256 `b9d4893dbc39aeee929a8cfadbbb1e35a996fe60924868e0b9ab2599c4459534`.
It supplies the Qt-only `libaero7commondialogs.so.1`, public header and CMake SDK.
Paint declares `aero7-file-explorer>=25.12.3-36`. Both Paint and the standalone
file-dialog executable link the shared library without temporary build RPATHs.
The repository build order now places Explorer before Paint.

The ISO preflight validates actual package metadata, runtime library/SDK entries,
ELF dependencies, SONAME and forbidden build paths. The Explorer 35/Paint 6 pair
and the mixed Explorer 35/Paint 7 pair were both rejected. The valid 36/7 pair
passed. Canonical `.SRCINFO`, source verification and repository validation also
passed. Canonical Control Panel metadata was synchronized to the already selected
r50 source archive; this did not create a new Control Panel binary.

Logs remain in `work/beta2-explorer36.10ku0O/explorer36-package.log`,
`work/beta2-paint-package.jlCu8M/paint7-package.log`, and the copied validation
logs beside this report under `native-dialog-package-logs/`.

## Real installed offline guest

The existing r9 offline VM upgraded Explorer 35 → 36 and Paint 6 → 7 through
normal `pacman -U`, with no dependency bypass or forced overwrites. The package
list comparison found no other version changes. `pacman -Qkk` reported Explorer
665 files and Paint 709 files, both with zero altered files. Actual installed
executables resolved `/usr/lib/libaero7commondialogs.so.1` normally.

Paint ran with `LD_LIBRARY_PATH` and `LD_PRELOAD` unset. Its native Save As saved
the existing red/green drawing to `Pictures/paint7-native.png`; native Open
reopened it. Exported PNG SHA-256:
`af3fde99964de8d1389f0632fb2c80cf8a77baab3b103bfd1cfbf1b2c6b19dc0`.
ImageMagick decoded-pixel comparison against `paint6-lines.png` returned
`0 (0)` absolute-error pixels. This demonstrates no pixel changes in this PNG
round trip, not arbitrary-format equivalence.

Explorer launched from the actual taskbar shortcut, opened Computer and its
Libraries root, and closed. Screenshots 114–120 and 129–131 are in
`/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`. Computer's CPU footer and drive
rows rendered; this is not complete library-layout or hardware-mount acceptance.

### Apparent Paint shutdown hang resolved

After one window was closed, Paint's process remained. Investigation found a
second real document window: the inherited default opened a non-empty image in
a new window. Closing the remaining window normally terminated the process.
No kill or debugger-forced exit was used. The guest log contains
`INSTALLED_PAINT7_CLOSED_NORMALLY`; the exported audit contains
`INSTALLED_PAINT7_SAVE_REOPEN_ALL_WINDOWS_CLOSED_VERIFIED_NOT_FRESH_ISO`.
The audit repeats package integrity checks after closure. Missing repository
database warnings remain in this disconnected guest's log; do not omit them
when assessing offline package operations.

Guest results, including the output image, logs and package-list comparison,
are retained under `/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/results/`.

## Document workflow correction: Paint 8

The new five-scenario test reproduced `Open unexpectedly created a second
window` against Paint 7 using non-empty fixture images. A focused source patch
makes fresh profiles reuse the document window while retaining explicit
separate-window preferences. Existing save/discard/cancel protection is used.

All five scenarios pass after the patch: same-window Open, retained separate
windows, cancel with unsaved changes, discard, and save before replacement. The
tests use real Paint actions, verify the adopted document path, on-disk image
changes, modified state and normal closure. Earlier native-dialog tests used a
blank document and therefore did not cover this non-empty-document default.

Red/green evidence: `aero7-document-workflow.H4KMv1` and
`aero7-document-workflow.ZZqZZi` under the host's Codex temporary directory.
Paint 8 subsequently built successfully, including all five workflow cases,
four native-dialog scenarios, four layout scenarios and ribbon lifetime/colour
cache checks. The prepared build tree was reused; the same host dependency
precheck exception applies. Package `aero7-kolourpaint-25.12.3-8-x86_64.pkg.tar.zst`
is 6,620,038 bytes, SHA-256
`db5ea8637cca914c650d65c4aa6387462e60045f92dd1c2ff0d12d554a40b5a5`.
It replaces r7 only in the local selected-package manifest; old packages remain.
Build log: `work/beta2-paint-package.jlCu8M/paint8-package.log`.

The offline guest upgraded normally from r7 to r8. No other package version
changed, the existing `kolourpaintrc` checksum was unchanged, and package
integrity checks still reported zero altered files. The installed application
then passed all five workflow scenarios using Wayland, isolated QA profiles
and a host-built test-only action probe. Runtime libraries came from `/usr/lib`,
not the staging SDK. The probe is never installed in the package. Each scenario
closed normally and no Paint process remained. Screenshot 133 records
`INSTALLED_PAINT8_WAYLAND_FIVE_WORKFLOWS_PASSED_ISOLATED_PROFILES_NOT_FRESH_ISO`.
This proves these workflows on the upgraded guest, not a fresh ISO installation
or a manual visual review of every dialog. Repository source/metadata validation
and the selected-package ISO static check also passed; their complete logs are
copied under `native-dialog-package-logs/`. QML and missing repository database
warnings remain visible in the relevant logs.

## Still required

Finish remaining common-dialog behavior/layout issues, rebuild both ISO variants and
repeat exact-media installation/application/failure-path acceptance. Remote KIO
remains an explicit fallback; no full Windows parity or zero-bug claim is made.
