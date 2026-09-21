# Installer: approved icon artwork and strict rendering checks

Local source/build/simulation evidence, 8 September 2026. Not final ISO or
fresh-VM acceptance; no publication approval.

## Cause and correction

The [explicit-input sweep](2026-09-08-installer-explicit-inputs.md) exposed native
Qt SVG parser warnings in the original check mark and Recycle Bin artwork.
These diagnostics do not pass through the QML engine warning signal, so the
previous engine-only assertion did not fail on them.

The UI suite now uses
[QTest's warning-failure hook](https://doc.qt.io/qt-6/qtest.html#failOnWarning)
for every test case. Before replacing the assets, all eight screen-loading
configurations fail on the actual SVG diagnostics: eight failures, two passes
for setup/cleanup, 9501 ms. The log is retained as `red.log`.

The two original SVG files are replaced by unchanged PNGs extracted from the
already selected `aerothemeplasma-icons-git-11.r96950b8-3-any.pkg.tar.zst`.
The archive checksum is verified as
`54321ad3e691ea0c8185d86452b9a1f1530f7db34e7477d68146cdfda5314294`.
No icons were drawn, generated, recolored or modified.

| Bundled resource | Exact member under `usr/share/icons/Windows 7 Aero/` | SHA-256 |
| --- | --- | --- |
| `icons/check-green.png` | `emblems/32/emblem-default.png` | `a946a1ef3768da5c2d135eb8f415c3e8e2b2fc155cdee2733dad245039e58981` |
| `icons/recycle-bin.png` | `places/256/user-trash.png` | `6bbe8a9d5d1bf78114ba48949e38cf7da2fbf71e36bf69d3a9abf5001e3b7024` |

The package LICENSE and README are copied verbatim into `third_party`, installed
with the standalone frontend by CMake and identified in `THIRD_PARTY.md`.
Installed Aero7 desktops also retain the original icon package's notices.
The existing notice about upstream attribution and redistribution remains;
this pass does not claim new permissions from the artwork's rights holders.
The retired source SVGs remain recoverable from Git history.

## Tests and captures

- `config/installer-icons.sha256` pins both PNGs and both notices. The full
  project checker validates it before accepting visual assets.
- Two Python tests compare the actual files with members extracted from the
  selected checksum-verified package, check pinned hashes, resource use and
  retirement of the original SVGs. The Python suite now has 144 passing tests.
- Strict UI suite: 20 passes including setup/cleanup (18 functional), zero
  failures/skips, zero warnings, 22889 ms with screenshot capture enabled.
  This includes all 20 screens in both directions, two resolutions, both
  documentation modes, missing-controller rejection, navigation and help.
- A new visible-icon check starts real simulated installation progress, waits
  until the first stage completes, and verifies the displayed check-mark image
  is Ready and uses the approved PNG. It separately verifies the visible
  desktop-preview Recycle Bin. Both 1920×1080 captures were visually inspected.
- The first version of that visual probe searched QObject ownership and did
  not find a Repeater delegate. The probe now traverses the actual visual tree.
  Its initial failure log is retained; this was a test lookup issue, not a
  separate application defect or a waived assertion.
- `git diff --check` passes. No warning category was disabled in production.

Logs and engineering previews:
[installer-approved-icons-logs](installer-approved-icons-logs/).
Current compiled frontend SHA-256:
`52f467fdad31447f988daf4d7d54aa24c729b326b11d0bb37b75bce264df1d62`.

## Next candidate and remaining work

Separate r10 online/offline profiles are prepared under
`work/beta2-r10.Sf7FVw/`, incorporating this frontend plus Explorer 50,
Desktop 29, Plasma Workspace 3.2 and the lsof backend selected previously.
Both prepare operations completed successfully: each passed all 144 Python
tests, all three CTest suites (33.62 seconds each), and the full source checker.
The embedded frontend, backend, base and local-package manifests match the
current inputs byte-for-byte. All 14 embedded local-package hashes verify in
each profile, and both retained icon notices match their originals.

Input identities:

- Local-package manifest: `2f612cf8d3a992a3c33e8d9fa4f90260f4590f1e75fb3f3fd6e01fea58466770`.
- Installer backend: `ec300f0f98c4dff28ac0962d72b68c8aca16687a020c06206523f49695905b77`.
- Frontend: `52f467fdad31447f988daf4d7d54aa24c729b326b11d0bb37b75bce264df1d62`.

The existing isolated builder VM was confirmed stopped with its disk unused,
then started successfully for the next build pass. No host packages were
installed. Prepared profiles are not bootable ISO artifacts or fresh-install evidence.
Both exact resulting images still require build verification, full installation,
OOBE, reboot and desktop checks. Other release-wide issues and acceptance
requirements remain in the website handoff. Nothing was committed or pushed.

Build checkpoint, 12:07:55 CEST: the isolated VM's
`aero7-r10-builder.service` is active/running, MainPID 3182. The offline build
has entered package installation; the guarded script builds online afterwards.
It exports only into `builder-output/r10-current-stack`, preserving earlier
artifacts. Its final exit marker and artifact verification must be checked
before treating either build as successful. The observed `Result=success`
while the service is still running is not a completion result.
