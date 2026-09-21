# Overlapping common dialogs — 13 September 2026

Local test-coverage addition only. Production code, selected package archives,
source pins and frozen ISOs are unchanged. Nothing committed or published.

## Added coverage

Eight data-driven cases were added to the maintained Explorer source's
`src/tests/aero7commondialogtest.cpp`:

- Two searches submitted together with either identical or different application
  state IDs. Rejecting or destroying the first dialog while its request is
  pending must not cancel the second request or mix their result models.
- Each search uses a separate temporary directory containing 512 files. The
  survivor must return only its own paths. Reopening the first caller must
  produce its own results without altering the survivor; accepting the survivor
  returns exactly the selected path.
- Two simultaneous Save As dialogs, with identical or different application
  state IDs, completed in either order. Each retains its own directory, typed
  name and file-type filter. Accepting one leaves the other visible and
  unaccepted; final results have their respective PNG/Text suffixes. Acceptance
  does not create either file.

These tests use temporary configuration/data/cache profiles and temporary
fixtures, not the user's real documents or saved dialog preferences.

## Results

The [targeted offscreen run](dialog-concurrency54-logs/targeted.log) passes
10 Qt results (eight rows plus setup/cleanup). The
[full offscreen suite](dialog-concurrency54-logs/full.log) passes 67 results,
zero failures/skips, in 7.493 seconds, linked to the existing packaged library.
No failing production behavior was reproduced in these new cases.

The [installed Wayland audit](dialog-concurrency54-logs/installed/audit.log)
also passes all 67 results with zero failures/skips, in 11.435 seconds.
It runs on the normal post-reboot offline VM, boot
`b4d20d4c-2122-454c-b361-fb67d20c63de`, without a library-path or style override.
The separate test executable has no build-directory RPATH/RUNPATH and resolves
`libaero7commondialogs.so.1` from `/usr/lib`.

- Installed Explorer: `25.12.3-54`.
- Installed dialog-library SHA-256:
  `17457ea55f0716537bde7c2652d88e26241c85e67a179848e2068d78a6de620a`.
- VM test-executable SHA-256:
  `d003cf9be28e738158f44d72a92ba52df51adf52a8f62d1578a5a8a9f0dbee71`.
- Shell, Plasma and KWin stay active with byte-identical before/after PID and
  restart-count records; no desktop restart was used to recover the tests.

The [guarded VM script](dialog-concurrency54-logs/test-dialog-concurrency54-installed.sh)
checks guest identity, no-network state, installed package version, test/library
hashes and live linkage before running the suite. The
[small build harness](dialog-concurrency54-logs/CMakeLists.txt) builds only the
test executable against the existing candidate library, with two build jobs.
The original package build and its earlier suite are not rewritten or relabeled.

## Scope limits

This proves overlapping library dialogs in one application process, including
same/different state IDs and pending-search cancellation/destruction. It is not
two independent external CLI callers, process-death recovery, cancellation
during a device authorization prompt, or a physical-device reconnection test.
The existing active-search teardown tests also pass in the full suite, but are
not a claim of every interleaving. Final-image acceptance remains separate.
