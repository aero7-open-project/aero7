# Desktop source-package hygiene — 13 September 2026

Local source/recipe correction and candidate validation. No commit, push,
publication, final ISO build or deletion of old artifacts.

## Finding and correction

Desktop 32's source snapshot recursively included old build trees, compiled
helpers and nested archives under `packaging/arch/src`. Those files were not
installed into the desktop package, but the source archive was 182,444,198 bytes.

The maintained Desktop tree now has `packaging/create-source-snapshot.py`.
It selects tracked and non-ignored new source files, includes working-tree edits,
honors deletions and excludes ignored output through Git's file inventory.
Unexpected tracked generated files cause a visible failure, not silent removal.
It refuses an output inside the source tree, overwriting an existing archive,
escaping symlinks, unsupported entries and unsafe archive prefixes.
It does not commit, clean or otherwise mutate the source working tree.

The clean source archive has 273 files and is 18,330,473 bytes. Two independent
exports of the same working tree produce byte-identical archives. Seven new
tests cover edited/new/deleted sources and executable modes, ignored output,
repeatability, tracked build output, symlinks, overwrite protection, repository
root validation and safe prefixes. They run through the normal CTest setup.

The embedded Arch recipe is aligned to release 33, includes Git for the snapshot
tests, and retains both Programs Center and Credential Vault as optional
dependencies. Its `SKIP` source checksum remains explicitly a working-tree
template; the [actual candidate recipe](desktop33-source-logs/PKGBUILD) pins the
exact archive digest. That template is not a signed release recipe.

## Evidence and scope of comparisons

All 31 regular files in the Desktop runtime directories `shell`, `services`,
`migrations`, `defaults`, `compatibility`, `plasma`, `kwin`, `assets` and
`integration` match the Desktop 32 source snapshot byte-for-byte.
The installed payload has the same 37 non-directory entries; 36 match in type,
mode and content/link target. Only the rebuilt `aero7-recovery-ui` binary differs.
This comparison does not claim compiler-output reproducibility.

Separate current-source comparisons find no content mismatch in Gadgets 25's
41 audited runtime/build-input files or Explorer 54's 654 files (excluding
`src/tests`). Control Panel 54 has 537 matching files and three extra Python
cache files in its source archive. Cleaning that source bundle was pending at
this checkpoint and is now covered by the [Control Panel 55 follow-up](2026-09-13-control-panel-source-cleanup.md);
these are not three missing application source files.

## Desktop 33 validation

- Source SHA-256:
  `ebaaadcd10cbbb6d4993c9ee7f668f487404b1d410a8995496f2156bad9088cd`.
- Package SHA-256:
  `eda2eeb5c9d255fa500dc179e804f6b67590bebfbeb1a1eb3b22c4c92bb1280d`.
- Recovery executable SHA-256:
  `8200ea7ba2f069e4680fb955e5e93d49116d6f50a0c3f4767a60739d67214c02`.

The [package build](desktop33-source-logs/package-build.log) uses two jobs and
passes all 10 CTest groups in 16.81 seconds, including clean production/test/
developer install-profile checks. Host-only dependency checking was bypassed
for this local build, not package tests or the guest installation transaction.

The [normal offline-VM upgrade](desktop33-source-logs/upgrade/audit.log) passes
dependency checks, all 79 installed-file presence checks and the recovery binary
hash. Shell, Plasma and KWin PIDs/restart counts are unchanged. The expected
missing repository-sync-database warnings remain in this disconnected VM.
The first typed invocation lost its `bash` prefix during unlock and received
permission denied; no package operation occurred until the corrected invocation.

The [Recovery window smoke test](desktop33-source-logs/recovery/audit.log)
opens and closes normally with exit zero and unchanged desktop services.
The [screenshot](desktop33-source-logs/a7-desktop33-recovery.png) is a deliberate
manual invocation for QA: its failure text is not evidence that the shell
actually failed. No restart/reset/sign-out action was clicked. Software EGL
fallback warnings are retained. Earlier recovery-action tests remain separate.

Desktop 33 is selected for the next builds. The manifest SHA-256 is now
`54b4a88ac2ddd21507851e5a687c831c09fd48a9aa9d6676ed0308e825fed9b9`.
All 149 integration tests, 18 online / 53 offline archive checks and 35 offline
repository-entry checks pass again. The earlier combined reboot used Desktop
32; this report adds a normal upgrade and rebuilt-UI check, not a Desktop 33
reboot or a fresh final-image installation. Frozen ISOs are unchanged.
