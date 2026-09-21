# Explorer storage refresh and small-volume capacity

Local QA follow-up, not final ISO acceptance. No release publication or package
selection change. The original reproduction used Explorer 43; Explorer 44 has
since upgraded normally in the disconnected r9 VM (see follow-up below).

## Real installed-application reproduction

The running 1920×1080 VM opened the normally installed File Explorer on Computer.
A guarded helper mounted an empty 16 MiB tmpfs at
`/run/media/aero7test/AERO7_STORAGE_QA`, then unmounted it and removed the empty
mount-point directory. No physical disk, user file or persistent mount setting
was changed. This is a mount-table transition test, **not** physical USB eject
or unplug acceptance.

- The manually refreshed Computer view displayed the mount as Removable Disk
  (D:), but its capacity was incorrectly shown as `0.0 GB free of 0.0 GB`.
- After successful unmount, the open Computer view retained the obsolete tile.
  Pressing its Refresh button removed that tile.
- The sidebar did not show the temporary mount when Computer showed it. This
  disagreement needs investigation along with the remaining refresh work.
- Source inspection confirms that Computer refresh is explicitly requested on
  entry and toolbar refresh. Common-dialog navigation is constructed once.
  These observations do not establish physical-device signal behavior.

Screenshots under `/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`:
`340-storage-computer-before.png`, `342-storage-mounted.png`,
`344-storage-after-refresh.png`, `345-storage-unmounted.png`,
`346-storage-stale-after-unmount.png`, `347-storage-clean-after-refresh.png`.
Screenshot 343 was captured before the window finished raising and is not used
as unobscured proof of the initial stale state. The stale tile is clearly
visible in 346, with successful cleanup recorded in 345 and 347.

## Capacity correction and regression

First moved the existing formatter unchanged into the private shared storage
header so the real production function could be tested. Ten data cases produced
eight failures, including the observed 16 MiB → `0.0 GB` defect; the two ordinary
GB cases passed. With initialization and cleanup the red total was 4 pass/8 fail.

The formatter now chooses bytes, KB, MB, GB, TB or PB using binary scaling and
the existing Windows-style labels. Negative/unavailable values no longer look
like a real zero-sized drive. Ordinary GB presentation is preserved.
The corrected test reports **12 pass, 0 fail** (10 data cases plus setup/cleanup).
The Computer tile calls this exact tested helper. No icon assets changed.

The new `aero7storagetest` is integrated into the normal source CTest list.
The shared library and common-dialog test executable rebuilt successfully;
the common-dialog and storage CTest groups both pass (3.85 seconds). Dynamic mount
refresh, sidebar consistency, actual device/eject behavior, complete source
suite, packaging and installed-VM verification of the correction remain open.

Working evidence: `work/beta2-storage-refresh.nsZcSb/`.

## Explorer 44 implementation and source checks

A private, parent-owned mount watcher compares `/proc/self/mountinfo` every
second. It refreshes on changes only and preserves its last good snapshot after
a read failure. It does not scan every filesystem's capacity on each timer tick.
Computer refresh retains scroll position and surviving drive focus. Common
dialogs update only Computer's drive children, preserving the folder, history,
filename, type filter, search model and selection. Native KIO device rows remain
native; synthetic persistent bookmarks are not introduced. A tmpfs transition
does not itself create a native Solid/KIO physical-device entry, so the earlier
sidebar observation must not be treated as physical USB acceptance.

Save and New Folder also check whether the original root/device still backs the
selected directory, including when an unmount leaves an ordinary directory in
place. The dialog rejects an unavailable destination instead of implicitly
writing into the filesystem underneath it. This is not a device-UUID guarantee.

Full source tests exposed a separate pre-first-folder clipboard crash. A
deterministic regression crashed the old main-window handler with SIGSEGV;
the corrected handler disables Paste until an active view exists. The regression
then passed. All **20 CTest groups passed**, followed by **three consecutive
passes of all 20 groups** (78.51 seconds). These are source checks, not final-media
or hardware acceptance.

## Package and normal VM upgrade

Working directory: `work/beta2-explorer44.Tr5F4W/`.

- Frozen source SHA-256:
  `c595d3403b7d13eb773d99dad1aea9b422250db04e28776b126bf5a3878dd3cb`.
- Package: `aero7-file-explorer-25.12.3-44-x86_64.pkg.tar.zst`, 8,244,816 bytes.
- Package SHA-256:
  `e078ac4b574c940499910b1e3fe573320fd84c446454af8415a962c97cd38c48`.
- Standard makepkg completed successfully. All 14 ELF files have the same direct
  library requirements as package 43. This check alone does not prove ABI safety.
- Normal `pacman -U` upgrade in `aero7-r9-offline` passed: only Explorer changed;
  Paint 8 and its saved preferences were unchanged. Package verification reports
  Explorer 665 files and Paint 709 files, with zero altered files in either.
- Screenshot: `389-explorer44-upgrade.png`; guest results:
  `explorer44-upgrade.log`, package before/after inventories and preference hash.

Initial installed Wayland dialog run: **39 pass, 2 fail**, counting setup and
cleanup. Diagnostic logging showed that the platform theme exposes both a native
message box and its Qt wrapper. Enumerating all top-level widgets counted one
warning twice. The fixture now dismisses only the active modal warning, as a user
would. The installed-library rerun passes **41/41 including setup/cleanup** (39
functional cases). The complete source suite passes again (20 groups, 23.62s).
The frozen package source is unchanged; the test-only correction is preserved
separately in `common-test/current-fixture.patch` and the current worktree.

Paint's initial probe passed same-window, separate-window and unsaved-cancel but
its 250ms confirmation check ran before the unsaved-discard modal was ready.
The QA-only probe now waits for that modal for up to five seconds. The new
five-workflow run passes, including unsaved-discard and unsaved-save. Paint 8's
binary was not rebuilt or modified. The probe is test instrumentation, not an
ordinary uninstrumented manual acceptance result.

Evidence copied from the VM:
`explorer44-common-dialogs.G648pE` (initial failure),
`explorer44-dialog-diagnostic.log`, `explorer44-common-dialogs.3qJhKL` (pass),
`paint8-readiness-workflow.YCtsPp` (initial timing failure),
`paint8-readiness-workflow.CqV0NM` (five passes),
`explorer44-tests-audit.log` (pass, both package inventories clean and Paint
preferences unchanged). Corrected test binary SHA-256:
`4dbc4925e938ad13842a202ed35858b7bac473113f0b78d50b4a35619c74f9bb`.
Corrected QA probe SHA-256:
`c5d9fd21744008df2813190f71bc6233739fa19c2701286a1dbb4c87e225eba8`.

Physical-device hotplug/eject, actual live mounted-volume dialog checks and fresh
final media remain open. Neither final ISO contains Explorer 44 yet; no GitHub
or package-repository publication occurred.

## Installed Computer live mount/unmount check

The ordinary installed Explorer 44 opened `aero7computer:/` in the active Wayland
session at 1920×1080. A separately timed, guarded root helper mounted the empty
16 MiB test tmpfs at 21:21:23 CEST and unmounted it at 21:21:53. No refresh button,
folder navigation, application restart or test-library injection was used.

- `394-storage44-before-mount.png`: one local disk; no removable-volume tile.
- `395-storage44-auto-mounted.png`: the same window automatically adds Removable
  Disk (D:) and correctly shows **16 MB free of 16 MB**.
- `396-storage44-auto-unmounted.png`: the same window automatically removes the
  obsolete removable-volume tile.
- `explorer44-mount-cycle.log`: both guarded operations completed, and the empty
  temporary mount point was removed. No physical disk or persistent mount
  configuration was changed.

This closes the reproduced stale-Computer-tile and tiny-capacity defects for this
normally upgraded VM. It does not establish physical USB detection, native KIO
sidebar eject, an open Save dialog surviving actual unmount, or final ISO parity.
