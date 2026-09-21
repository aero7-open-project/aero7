# Explorer 50: preserve Aero7 breadcrumbs after Places refreshes

Local source/package/VM evidence. Not final ISO acceptance or publication approval.

## Cause and regression

The [Explorer 49 runtime pass](2026-09-08-explorer-storage-recovery.md) showed
the mounted drive's breadcrumb losing `(D:)` after a busy removal failed.
Its sidebar label stayed correct and retry/recovery worked.

The [upstream KUrlNavigator implementation](https://raw.githubusercontent.com/KDE/kio/master/src/filewidgets/kurlnavigator.cpp)
rebuilds its buttons on Places-model data and row changes, not just navigation.
Aero7 reapplied its presentation after URL and kernel mount-table changes,
but a failed unmount changes neither. The native model refresh could overwrite
the displayed label afterwards.

The new source regression opens the system root, waits for navigation-time
presentation to settle, then emits the real shared Places model's data-change
signal without changing the URL or mounting anything. Before the fix the
display became `/` instead of `Local Disk (C:)`: one functional failure, plus
passing setup/cleanup. This reproduces the missing event route without a
privileged host mount or a fabricated button label.

The correction follows model data/row/reset events and queues the existing
presentation routine after the native update. Native URLs, history and
breadcrumb button actions are retained. It does not introduce periodic
repainting, a new icon pack, force-unmounts or a new mount implementation.

## Source and package validation

- Regression now passes three successive model refreshes while preserving
  the same URL: three passes including setup/cleanup, zero failures, 984 ms.
- Full build and all 20 CTest suites pass; total time 12.70 seconds.
- `git diff --check` passes.
- Package build from freshly extracted, checksum-verified source succeeds.
  `--nodeps` skips the local host dependency precheck only; compiler/linker
  checks remain enabled and no host packages are installed.
- All 14 packaged ELF direct-library requirement lists match Explorer 49.

Candidate directory: `work/beta2-explorer50.BSWjxy/`.

| Artifact | SHA-256 |
| --- | --- |
| `aero7-file-explorer-25.12.3-r50.tar.gz` | `41c1d0a9ee6bb4b13af460cf1d16bdd54bc813c28b6e7f88602392f55c99c0c5` |
| `aero7-file-explorer-25.12.3-50-x86_64.pkg.tar.zst` (8,266,700 bytes) | `dfb3004c41f6a9145bd38cb39c8c16786cc95a9e53547ed56666e808f81920fe` |

Logs are in [breadcrumb50-logs](breadcrumb50-logs/). Offscreen warnings are
retained; passing tests are not a warning-free graphical-session claim.

## Missing busy-process diagnostic helper

The previous native busy error logged that `lsof` was missing. The cached Arch
package `lsof-4.99.7-1-x86_64.pkg.tar.zst` has SHA-256
`798590776e511d13ddde0763ed0b7e8cfc6e9a366be5bdc73e81e235dac857d0`.
Its detached signature verifies against the existing distro keyring, using
key `262A58EC6C51F7EA395B2E2DFDC3040B92ACA748`, Robin Candau.

The guarded disconnected-VM transaction verified the signature again and
installed only `lsof`; existing glibc/libtirpc satisfied its dependencies.
The before/after package inventory has no other change, and all 17 package
files are unaltered. The native Explorer replay then identified the actual
blocking process as `bash`, rather than the previous unnamed application.
No diagnostic observer or replacement Explorer binary was loaded.

`lsof` is now required by the shared fresh-install base package list. The
offline bundle contains the verified package and its checksum; its existing
glibc/libtirpc packages satisfy the dependencies. The release checker enforces
the helper's presence in the embedded base list, and its policy test rejects
a fixture missing `lsof`. It does not install anything on the build host.

## Installed VM replay

Normal Explorer 49→50 upgrade passed in the modified offline r9 VM, preserving
the other installed packages and Paint preferences. The installed common
dialogs passed 49 cases including setup/cleanup (47 functional), no failures
or skips, in 5033 ms. Paint 8 passed all five isolated Wayland workflows again.
Records: `explorer50-common-dialogs.pcpRkt/` and
`paint8-readiness-workflow.9xLNPr/` in the logs directory.

At 1920×1080, the ordinary Explorer process PID 48085 opened Computer and
mounted `AERO7_QA (D:)` (`523`, `524`). Leaving the terminal's working directory
on that fixture caused a genuine busy refusal. Both the sidebar and main
breadcrumb retained `(D:)`, and the banner named `bash` (`525`). After moving
the terminal Home, retrying from the same Explorer process succeeded and
returned the view Home without a stale banner (`526`). UDisks logged cache
synchronization, START STOP UNIT and successful power-off at 00:29:13.

The 00:30:07 restoration audit (`527`) confirms no mounted fixture, no temporary
polkit rule, no observer in Explorer's process maps, zero failed system units,
unchanged Paint preferences and clean package files: Explorer 665, Desktop 75,
Paint 709, lsof 17. The captured Explorer UI log is empty; this is scoped to
that process/replay, not a warning-free whole-session claim. Computer was
restored for inspection. QMP device deletion completed before the backing
node was closed. The retained 96 MiB FAT fixture still has its 314-byte README,
Photos folder and 100,442,112 bytes free. No physical disk was used.

## Next-image input selection

The selected local-package manifest now uses Explorer 50, Desktop 29 and the
previously tested Plasma Workspace `6.7.4-3.2` splash correction. Desktop 28
and Explorer 43 are no longer selected. Existing packages are retained in the
workspace; no historical evidence or VM disk was removed in this pass.

The selected archives pass hygiene/checksum validation for both variants:
14 online local packages, 49 offline local/custom archives, and all 35 offline
custom-repository entries match their manifest. The three selected dependency
closure tests pass in 11.701 seconds. All six candidate-policy/archive tests
also pass, including required `lsof` and excluded fresh-install UFW fixtures.
These checks do not build an ISO or prove installation of those selected bytes.
The complete Python installer/backend test run also passes all 142 tests in
12.133 seconds, with no skips reported.

### Broader project check: initial failure, resolved in follow-up

The failure below is retained as historical evidence. The later
[installer input-contract correction](2026-09-08-installer-explicit-inputs.md)
replaces implicit inputs and passes the full project checker. Final ISO
acceptance is still pending.

Running `scripts/check.sh` validates the selected package ownership, launcher
identity, approved icon hashes and shared-dialog linkage, and reruns all 142
Python tests successfully (12.101 seconds). It then exits 1 at the Qt 6 QML
lint stage with 150 `unqualified` warnings. The current installer exposes
`controller`, capture settings and documentation mode as C++ context properties;
the standalone linter cannot resolve those implicit references. The log is
`aero7-storage50-project-check.log`.

No installer QML or C++ binding code changed in this pass. This is an existing
static-binding/validation gap revealed by the broader check, not evidence that
the passing drive replay broke installation. It remains a failed project gate:
the full check must be repaired and rerun, not described as successful or
bypassed. Later checks after QML lint did not run in this invocation.

## Remaining acceptance

No final online/offline ISO includes this candidate yet. Multiple native
requests, physical/optical devices, current-stack restart/recovery and the
full final-image installation matrix remain required. No commit or push.
