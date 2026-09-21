# Beta 2 pre-release audit — 2026-09-05

This is the original audit snapshot. The subsequently authorized
[fixes and cleanup pass](2026-09-05-beta2-fixes-and-cleanup.md) closes the local
Explorer test failures and records the focused cleanup. Final package/image
acceptance remains pending.

## Decision

**Not ready to close the Beta 2 release gate.** This was an audit, not a bug-fix,
cleanup, package-publication, or ISO-release pass. No project folders were
deleted, no runtime source was changed, and nothing was committed or pushed.
Existing documentation and screenshot changes were preserved.

The condition for cleanup (checks going smoothly) was not met. File Explorer
still has three failing CTest executables. Final package/image acceptance also
remains incomplete. Offscreen tests below are not graphical VM acceptance.

## Sources examined

Paths are relative to the shared scripts workspace, which is not itself a Git
repository. Repositories must be handled individually.

| Worktree | Branch / inspected HEAD | Role |
| --- | --- | --- |
| `aero7-physical-log-test-iso` | `beta`, `3d3ca2f` | Main Aero7 installer, media, documentation |
| `aero7-desktop` | `beta`, `a59648a` | Desktop session and bundled companion sources |
| `aero7-desktop-workcopies/aero7-file-explorer` | `beta`, `25517aaa5` | Maintained Dolphin fork |
| `aero7-desktop-workcopies/aero7-control-panel` | `feature/programs-center-integration`, `e3a1636` | Control Panel and optional features |
| `aero7-programs-center` | `main`, `0405a2e` | Optional Programs Center |
| `aero7-computer-management` | `main`, `6d7fe79` | Computer Management |
| `linux-devmgmt` | `main`, `6d080f8` | Source directory for renamed Device Manager |
| `aero7-desktop-workcopies/aero7-repo` | `beta`, `31dc904` | Candidate package recipes and source manifest |

The package workcopy fetches from the local sibling `aero7-repo` and has
`DISABLED_NO_PUBLISH` as its push destination. That guard must remain intact.
The sibling points to `memegeko/aero7-repo`, but is on an older
`replace-aero7-dolphin-with-file-explorer` branch at `ad52c09`. Do not mistake
either worktree for a disposable duplicate or publish without resolving the
intended source/destination and obtaining approval.

## Checks rerun

Existing builds were rebuilt before running their tests. Qt app tests used the
offscreen platform and an isolated session bus, with a 90-second per-test limit.

| Component / check | Result |
| --- | --- |
| Desktop `tests/run.sh` | Static checks and 4/4 CTest executables passed |
| Main ISO `scripts/check.sh` | 69 Python tests and source/package checks passed; QML warnings remain |
| Installer `build/installer` | 2/2 CTest executables passed |
| Control Panel `build-optional-features` | 12/12 passed |
| File Explorer `build-file-explorer-identity` | **13/16 passed; 3 failed** |
| Programs Center `build-icon-independence` | 3/3 passed |
| Computer Management `build-icon-independence` | 9/9 passed |
| Device Manager `build-icon-independence` | 4/4 passed |
| Desktop companion Gadgets `build-icon-independence` | 3/3 passed |
| Desktop companion Internet Explorer `build-icon-independence` | 4/4 passed |
| Package `tests/test-release-gates.py` | Passed |
| Package `tests/validate-repo.py` | Passed |
| Package `tests/test-prune-builder.sh` | Passed against its temporary fixtures |
| Whitespace checks, four pending documentation worktrees | Passed |
| Desktop clean build/install with `BUILD_TESTING=OFF` | Completed into a temporary staging directory; test payload still present |

CTest total: **54/57 executables passed**. This count is separate from the
69 Python installer tests and other static/recipe checks.

Local detailed CTest logs and the production staging tree are in
`/tmp/aero7-beta2-audit.70cfP7/`. These are temporary diagnostic artifacts, not
release artifacts, and may disappear on reboot.

## Findings requiring follow-up

### 1. File Explorer gate remains red — release blocker

Reproduced in this run using Qt 6.11.2:

- `dolphinsearchbartest`: popup lazy-loading assertions fail in
  `testPopupLazyLoading` and `testUrlChangeSignals`; CTest then reports a
  segmentation fault. The output reaches `cleanupTestCase` before termination.
- `viewpropertiestest`: `testExtendedAttributeFull` fails because the expected
  `.directory` fallback file does not exist after exhausting extended-attribute
  space (`src/tests/viewpropertiestest.cpp:329`).
- `dolphinmainwindowtest`: Places-panel focus transfer and accessibility-tree
  assertions fail. The latter identifies a QLineEdit without a distinguishing
  accessible name (`src/tests/dolphinmainwindowtest.cpp:1032`).

The test environment also reports offscreen-plugin limitations and a missing
`aero7-file-explorerui.rc` lookup. Do not classify every failure as a proven
interactive user bug, but do not dismiss them as harmless upstream failures
either. Reproduce in the correctly installed graphical environment, inspect
the search-test crash, and fix or explicitly justify the affected test contracts
before closing this gate. Do not simply disable the failing tests.

### 2. Local media packages are not the final candidate set — release blocker

The local package hashes/closure pass their checks, but the inspected media tree
still contains Desktop `0.2.0-25`, File Explorer `25.12.3-32`, Control Panel
`0.1.0-37`, Gadgets `3.0.0-1`, and Internet Explorer `0.1.0-4` as its current
test versions. The planned candidates are respectively `-26`, `-33`, `-38`,
`-3`, and `-5`. Device Manager, Computer Management, and Programs Center also
have newer candidate identities in the release notes.

The Desktop recipe's pinned commit differs from HEAD only in the CI workflow;
that difference is not evidence of missing runtime code. Nevertheless, older
embedded binary packages cannot certify the new recipe versions. Produce and
validate the exact signed candidates before refreshing both media manifests.
Do not delete the working offline closure while replacements are unverified.

### 3. Production desktop includes test-only tools — packaging cleanup

`aero7-desktop/CMakeLists.txt:40` onwards unconditionally builds/installs
`aero7-test-status-notifier`, `aero7-screenshot-test`, the visual-test desktop
identity, VM scripts, and the ydotool device-classification rule. A new
`BUILD_TESTING=OFF` build and staged installation confirmed this behavior.

Consider an explicit test-tools option or separate test package/media payload.
Keep recovery and user-facing diagnostics available. Update the live-session
test expectations at the same time: they currently require these helper files.
The ydotool rule classifies a virtual input device; this audit does not identify
it as a permissions bypass or security vulnerability.

### 4. Obsolete native-shell prototypes remain tracked — coordinated cleanup

Thirty source files under Desktop `shell/start`, `shell/taskbar`, `shell/tray`,
`shell/notifications`, `shell/desktop`, and `shell/controlpanel` are not part of
the active CMake build. Their old desktop entries/systemd units and per-surface
VM tests remain in the tree. For example, `tests/vm/test-taskbar.sh` expects
`aero7-taskbar.service`, while the active `test-session.sh` explicitly checks
that this obsolete service is absent. `tests/taskbar/test_pins_store.cpp` is
also outside the current CTest suite.

These are candidates for coordinated removal or archival after a full reference
check, not evidence that two taskbars are currently installed. Keep the active
`shell/recovery`, `shell/session`, shell integration, migration, and current
surface tests. Passing static lint on an old file does not make it active code.

### 5. Embedded desktop recipe differs from candidate recipe — maintenance

Desktop `packaging/arch/PKGBUILD` is still release 25 with `linux-devmgmt` and
an `aero7-programs-center` optional dependency. The candidate package recipe is
release 26 with `aero7-device-manager`; the canonical Programs Center package
is `aero7-programs-center-git`. Align or explicitly retire the embedded recipe
so future maintainers do not build a different dependency set by accident.
Preserve Programs Center's optional status.

## Folder and artifact cleanup plan

No folder deletion was performed. Do not run blanket `git clean`, recursive
workspace deletion, or remove everything named `build`.

| Area | Proposed treatment |
| --- | --- |
| Older Control Panel `build-*` directories | Review generated-only contents, then remove exact obsolete build paths; retain the active optional-feature build until follow-up is complete |
| File Explorer's other build trees | Keep the identity test build and its failure evidence; review older reproducible builds separately |
| Package workcopy `retired-packages` (about 623 MiB) | Untracked; inventory and recoverably archive before any deletion |
| Tracked old File Explorer `r30` and Control Panel `r24`/`r33` source tarballs | Current recipes use Explorer `r33` and Control Panel `r38`; check historical/release references before a focused cleanup commit |
| Package source tarballs used by current recipes | Keep; compressed files are not automatically junk |
| `offline-packages` (about 1.8 GiB), ISO `work`/`out` | Keep current offline closure and test media; review mount state and replacements before build cleanup |
| `aero7-beta2-test-inputs` | Keep; contains the pinned source required by the main validation gate |
| Branding backups, VM images, pending wiki screenshots | Keep; useful rollback/evidence, not proven obsolete |
| Legacy `aero_desktop` and other independent project copies | Outside this cleanup scope; do not execute, merge into the new desktop, or delete |

For future structure, keep each Git repository as its own source root, put new
generated builds outside source roots, and separate test evidence from release
artifacts. Do not move the current trees casually: existing build caches,
source locks, local remotes, and scripts refer to their paths. Correct those
references and rebuild when a deliberate relocation is approved.

## Remaining release acceptance

This pass did not boot a VM, install onto a physical disk, test internet-free
installation, or inspect newly built ISO artifacts. Prior 1920×1080 screenshots
are useful appearance evidence, but use older test packages and are not final
candidate acceptance. Their documented visual limitations also remain open.

Before Beta 2 ISO publication:

1. Resolve or formally disposition all three Explorer test failures.
2. Complete the focused source/package cleanup and rerun the same checks.
3. Build and verify the exact signed candidate package set and both images.
4. Test a fresh online install and a fresh offline install with networking
   unavailable; retain the physical-install logs.
5. Verify reboot, OOBE, SDDM/lock-screen branding, second login, defaults,
   taskbar pins, Start, Explorer, Control Panel, screenshot clipboard/save,
   optional-feature install/remove/reinstall, multi-monitor, and recovery.
6. Record final image checksums and sizes. Ask for explicit publication approval
   before committing/pushing or uploading release artifacts.
