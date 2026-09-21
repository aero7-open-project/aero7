# Beta 2 fixes and focused cleanup — 2026-09-05

## Status

Authorized local follow-up to the pre-release audit. All 16 File Explorer test
groups and all five Desktop test groups pass. No commit, push, signed package,
ISO build, VM deployment, or release upload was performed. Earlier wiki and
screenshot work was preserved.

## File Explorer fixes

- Search scope controls move into the popup only on its first real opening.
  The popup remains lazy and subsequent openings reuse the controls.
- The Places-model singleton releases its KIO jobs during Qt application
  cleanup. GDB previously traced the exit crash to a KJob event-loop lock being
  released after QCoreApplication had already been destroyed. The fix uses
  [Qt's documented cleanup routine](https://doc.qt.io/qt-6/qcoreapplication.html#qAddPostRoutine).
- Folder settings now reach a real `.directory` fallback if extended attributes
  cannot be written. Repeated saves serialize fresh state rather than an empty
  buffer, preserve unrelated folder metadata, and can migrate back to extended
  attributes after space becomes available.
- Ordinary local folders retain a visible Computer disk entry in Places, and
  activating it returns keyboard focus to the file view.
- Search, navigation, view, preview, and help controls have accessible names.
- The renamed application's action layout is loaded from the actual embedded
  Dolphin resource rather than an inferred, nonexistent Aero7 filename.

Regression coverage includes popup reopening and scope selection, fallback
reload/update/migration while preserving a Desktop Entry comment, the embedded
action layout, and the existing full focus/accessibility checks. No tests were
disabled or changed to accept the former failures.

## Desktop cleanup

Removed 47 tracked files: 30 unused native shell source files, six obsolete
desktop entries, five obsolete systemd units, five obsolete per-surface VM
scripts, and the unbuilt PinsStore test. These were the retired duplicate
taskbar, Start, desktop, tray, notifications, and Control Panel prototypes.
They remain recoverable from the repository's existing HEAD/history.

Recovery/session source, current AeroShell integration, migration, defaults,
approved icon assets, and active acceptance scripts remain. Historical audit
documentation now explicitly labels the removed implementations as historical.

`AERO7_INSTALL_TEST_TOOLS` defaults to OFF. Normal packages no longer install
synthetic tray/screenshot helpers, VM scripts, the visual-test identity, or the
ydotool rule. Test images opt in explicitly; the VM package installer does so.
`BUILD_TESTING=ON` alone does not install these helpers. The new install-profile
test builds/stages production, test-image, and developer configurations and
checks both helper exclusion and preservation of recovery/session files.

The embedded Arch recipe now uses the current Device Manager name and the
correct optional Programs Center Beta package name. It is aligned to the
existing candidate release number 26; no binary package was published.

## Validation performed after changes

- File Explorer rebuilt: 16/16 CTest executables passed, 14.19 seconds in the
  final run; Qt 6.11.2, offscreen platform, isolated session bus.
- The three previously failing executables each passed three consecutive runs
  (`ctest --repeat until-fail:3`), without excluding their regression cases.
- Desktop `tests/run.sh`: static validation and 5/5 CTest groups passed,
  including the new three-profile staged-install test.
- Main installer/media `scripts/check.sh`: 69 Python tests, source safety,
  current local package hashes/closure, ShellCheck, and asset checks passed.
  Existing installer QML unqualified-access warnings remain.
- Package workcopy `tests/test-release-gates.py` passed. Recipe source archives,
  candidate pins, signatures, and embedded media packages were not regenerated.

Explorer's final CTest log is `/tmp/aero7-explorer-beta2-fixes-ctest.log`;
Desktop's detailed log is `aero7-desktop/build/Testing/Temporary/LastTest.log`.
Temporary logs are diagnostic evidence, not release artifacts. These automated
results do not constitute a new graphical VM or physical-install pass.

## Deliberately retained / next gate

Untracked retired-package folders, older build copies, package source archives,
offline dependencies, ISO outputs, VM disks, branding backups, and unrelated
legacy trees were not deleted or moved. Their rollback/reference value has
not been ruled out. No active source root was relocated, avoiding breakage of
existing build caches, local Git remotes, and pinned-source paths.

After review and explicit publication approval, the approved source commits
must be used to refresh package pins/source archives, build signed candidates,
and validate the exact online/offline image contents. Do not assume the current
candidate pins or older embedded packages include this uncommitted work.
Fresh installs, offline-without-network installation, reboot/login/lock-screen,
taskbar, search/clipboard, optional features, multi-monitor, and recovery still
need final-candidate graphical/physical acceptance before ISO publication.
