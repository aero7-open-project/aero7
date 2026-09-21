# Explorer drive and breadcrumb consistency pass

Local work in progress. No publication or replacement of the immutable r9 ISOs.
Explorer 38 is selected locally and installed-package checks have passed in the
offline VM, subject to the limitations below. The immutable r9 images do not
contain this pass.

## Reproduced defects

- Computer's C: tile and the sidebar's C: action opened the home directory,
  while the common file dialog opened the actual filesystem root.
- Both Computer and the places model invented a CD drive. The old CD action
  could open the first mounted removable volume regardless of device type.
- Main-view drive labels could expose a raw mount path as the device name.
- The full accessibility test exposed hidden, zero-width breadcrumbs receiving
  focus and an asymmetric Tab/Shift+Tab chain. The focused-object trace identifies
  the hidden `/` button and the skipped destination button.

The two Computer regressions and two main-window regressions failed before
the fixes. Logs: `/tmp/aero7-drives-red-common.log` and
`/tmp/aero7-drives-red-main.log`. Later full-suite failures are retained rather
than replaced with standalone passing accessibility results.

## Implementation under test

- C: opens `/` from the tile, sidebar and common dialog. Its breadcrumb is
  labelled Local Disk (C:) rather than disappearing as a hidden Linux prefix.
- The synthetic CD bookmark is removed, but its old directory and any user
  files are left intact. Old CD shortcut activation goes to Computer, never an
  unrelated removable disk. Empty removable sections are not invented.
- A private shared storage policy filters ready mounted storage, suppresses
  internal mounts and other users' media, sorts roots consistently and uses
  filesystem labels rather than raw mount paths. Display letters start at D:;
  excess mounts are still listed without manufacturing letters after Z:.
- The sidebar uses native KIO device entries for mounted removable storage,
  preserving its native device actions. A three-second refresh re-evaluates
  device visibility and labels; unchanged labels do not emit repeated changes.
- Breadcrumb presentation uses actual layout order instead of QObject creation
  order. Hidden buttons lose keyboard focus eligibility, reused visible buttons
  regain their original policy, and stale queued hides re-check the button's
  current role before hiding it.
- Focus order/proxy are reconciled after the visual breadcrumb transformation
  and later KIO layout changes. The full accessibility test still requires
  matching forward/backward counts and now explicitly rejects hidden-path focus.
  It also waits for the current destination to become keyboard-reachable before
  auditing the static chain, rather than traversing a partially rebuilt bar.

The upstream [KIO navigator implementation](https://github.com/KDE/kio/blob/master/src/filewidgets/kurlnavigator.cpp)
was inspected to check its breadcrumb reuse and focus-order/proxy behavior.
The Aero7 changes stay in the Explorer fork; no host KDE packages were changed.

## Source evidence and package preparation

All 19 Explorer CTest groups passed twice after the focus-order correction
(18.11 seconds and 18.61 seconds), with a complete all-target build between the
runs. The common-dialog suite reports 35 passes: 33 functional cases plus
setup/cleanup. The main-window suite reports 38 passes. One unrelated
ViewProperties test explicitly skips because this filesystem supports metadata
larger than a filesystem block; this is not reported as an exercised case.

New coverage includes mount-name privacy, user/path boundaries, C: navigation
and visible labeling, no fabricated devices, refresh without duplicate drive
tiles, and rejecting hidden breadcrumbs during the complete focus-chain audit.
The full final logs are `/tmp/aero7-drives-taborder-tests.log` and
`/tmp/aero7-drives-verified-tests.log`. Earlier failing logs are retained.

The source snapshot `aero7-file-explorer-25.12.3-r38.tar.gz` has SHA-256
`7d99d7941ba6c142f5278fe004cd74eae6e32d264561463dc64069fee6be9466`.
The exported common-dialog and Computer-view headers are byte-identical to r37.
Canonical package recipe, `.SRCINFO` and recipe hashes now describe r38;
repository validation passed. A fresh local package build completed at 22:58:44
CEST in `work/beta2-explorer38.cdozLK/`. It skipped only the host dependency-presence
precheck with `makepkg --nodeps`; no host packages are installed. Its recipe
disables test compilation, so the source CTest results above are separate from
the package build.

Selected package: `aero7-file-explorer-25.12.3-38-x86_64.pkg.tar.zst`,
8,232,995 bytes, SHA-256
`6d0e8857fd2a5c821f00ccfd79a5ea6c35f1190e4f53e04ce768f8814efe4989`.
The complete ISO static check passed with the selected package, including
133 backend tests and shared-dialog ELF/SONAME validation. Existing QML lint
warnings remain in `/tmp/aero7-explorer38-iso-static.log`.

The old installed r37 behavior was captured in offline r9 screenshots `153`
and `155`: the synthetic CD appears in both views, and clicking C: opens the
user's home directory. The old Computer breadcrumb also displays the raw
`aero7computer:` protocol and logs unknown-protocol warnings; this must be
rechecked separately, not assumed fixed by the storage changes.

## Acceptance still required

### Installed offline-VM evidence

The normal package transaction upgraded only Explorer 37 to 38 at 23:00:12
CEST; Paint 8 and Control Panel 50 stayed installed. No dependency bypass or
forced overwrite was used in the guest. The first upgrade helper stopped on
an obsolete Paint-settings checksum. The config modification time was
22:23:54, before this upgrade, following earlier manual Paint tests. A separate
audit records the transaction and package integrity; no legitimate settings
were restored over. This is not a before/after config-checksum proof for the
upgrade itself.

The installed shared library passed all 33 functional dialog cases plus
setup/cleanup on Wayland (35 passes, zero failures). The QA executable resolved
the guest's installed `/usr/lib/libaero7commondialogs.so.1`, not a build-tree
library. Screenshots 165–170 under the offline r9 evidence show:

- Computer no longer invents a CD tile or sidebar entry.
- Clicking the C: tile opens the real filesystem root, with a visible
  Local Disk (C:) breadcrumb.
- Documents navigation still works; clicking the sidebar C: returns to `/`.
- Explorer closes normally after these checks.

The initial Paint compatibility run failed before Open, reporting no initial
document window at the probe's fixed one-second check. Its original failed
logs remain in `paint8-wayland-workflow.9lmN4s`. A separate QA-only probe waits
for exactly one visible document window with the expected loaded filename,
bounded by ten seconds, instead of assuming readiness after one second. It
retains every workflow assertion and the overall timeout. With the unchanged
installed Paint 8 and Explorer 38 packages, all five scenarios passed:
same-window, explicitly separate-window, and unsaved Cancel/Discard/Save.
Readiness was observed after 105–229 ms in this run. This supports a probe
readiness problem; it does not establish the precise cause of the earlier
startup delay or certify all cold-start conditions.

The successful compatibility evidence is `paint8-readiness-workflow.ZcIFkZ`
and `explorer38-paint8-readiness-audit.log`. The QA-only probe binary hash is
`15aa9652d1afd1271b0e82d6fe5793add217caf4410a8305df161a552ef39608`.
It is not included in either production package. Final package integrity:
Explorer 665 files and Paint 709 files, zero altered files. The user's current
Paint settings checksum stayed unchanged during these isolated-profile checks.
The export helper now copies failure logs before asserting success, so failed
checks do not hide their own evidence.

The live VM also confirms two remaining defects: Computer still exposes
`aero7computer:` in the breadcrumb and logs unknown-protocol warnings; the
narrow sidebar clips captions and leaves a gap for an absent New Library.
These are not claimed fixed by Explorer 38. The original failed audit marker
has not been relabeled as passing; the separate readiness audit is the passing
compatibility result.

This remains a mounted-storage presentation pass, not complete Windows storage
management. Real USB insertion/removal, unmounted devices, empty optical drives,
mount/eject failure paths and stable persistent drive-letter assignment still
need implementation/acceptance review. No claim of complete hardware coverage
or fresh-final-ISO acceptance follows from the source tests.
