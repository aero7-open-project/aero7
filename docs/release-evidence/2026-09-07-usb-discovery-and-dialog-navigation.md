# Removable-drive discovery and dialog navigation follow-up

Local pre-release QA. Initial findings below used Explorer 44. The additional
source corrections are now packaged and upgraded in the VM as Explorer 45;
their live behavior is under verification. Nothing here is published yet.
This report supplements, not replaces, the earlier static/mount-table checks.

## Test boundary and boot

The existing offline r9 VM shut down through Aero7's security-screen power
control. QTerminal required confirmation because it had launched a process;
after confirming, QEMU exited normally. No forced process termination or disk
reset was used. The same 64 GiB disk and existing UEFI variables then restarted
with a `qemu-xhci` controller. Network remains disconnected, display 1920×1080.

Current boot: `c0388ac1-1b28-4919-890f-1cd352dcda1e`. Evidence directory:
`storage44-boot.AikXjX`. Explorer 44, Paint 8, Desktop 28 and Plasma Workspace
6.7.4-3.2 were retained. Explorer and Paint file inventories were clean; Paint's
saved preferences were unchanged. No failed system units were listed. Other
logged warnings have not all been resolved, so this is not a warning-free claim.

A **new 96 MiB regular image file** was created with `mkfs.vfat -C` under
`/home/admin/VMs/aero7-beta2-r9-xTfYQR/usb-storage-qa.gr6LWi/`. No physical drive,
existing VM disk or user filesystem was formatted. FAT label `AERO7_QA`, UUID
`F921-93DA`, USB serial `AERO7QA96`; initial image SHA-256:
`4fd370070d50cb6c2415afb74acb141e902bfdd3645ba1d71fedd75651546c6d`.
The filesystem contained only the QA README. This exercises a virtual USB block
device through the guest's normal UDisks/Solid stack, not physical hardware.

## Actual installed-VM findings

1. **Unmounted discovery fails.** UDisks recognizes a non-ignored filesystem, but
   the attached, unmounted USB drive is absent from Computer and the sidebar.
   Screenshot `402-usb-attached-unmounted.png`; `storage44-usb.log` records the
   native device, empty mount list and successful inspection.
2. Normal non-root `udisksctl mount` succeeds. The existing Computer window and
   sidebar show the same `AERO7_QA (D:)` name, with **96 MB free of 96 MB** in
   Computer. Screenshot `406-usb-successfully-mounted.png`.
3. Save As can browse the actual mounted drive and see its README. After normal
   `udisksctl unmount`, the drive entry disappears and Save is disabled. The
   filename remains `usb-check.png`. New Folder warns that the location is no
   longer available. Screenshots `410`, `411` and `412` record these states.
4. **The file area retains a stale cached README after unmount.** Disabling Save
   protects the destination, but displaying that file as still available is a
   separate presentation defect.
5. **Single-click sidebar navigation does not navigate.** Double-click recovers
   to Documents and re-enables Save without changing the filename (`413`, `414`).
   Enter on the selected sidebar folder also invokes the dialog's default Save
   action. The standalone dialog printed a selected path; it does not write
   image data. Subsequent inspection confirmed no PNG or new folder was created.

One injected mount command lost its first character during window closure
(`ash` instead of `bash`) and never ran. It was corrected before the successful
mount. Screenshots `403`–`405` are not mounted-state acceptance evidence.

The test filesystem was normally unmounted, then the USB device and backing
node were detached through QMP. `info usb` returned no attached USB devices.
Host-side `mdir` afterwards still listed only the original README. The image is
retained for the next verification pass, not deleted.

## Source corrections in progress

- Native-device visibility now allows a real, non-ignored, unmounted removable
  filesystem while still hiding internal partitions, swap, ignored recovery
  volumes and devices mounted outside the user's permitted roots. It keeps
  native KIO rows rather than synthesizing bookmarks. Nine policy cases expose
  two failures under the former visibility rule and pass with the correction.
- Source inspection also found that the custom sidebar click and Open menu
  bypassed native setup. They now request KIO's asynchronous setup before
  navigating, using a lifetime-bound request, persistent model index, duplicate
  suppression and a bounded timeout. Navigating elsewhere cancels delayed
  navigation, not an already-started OS mount operation.
- Common dialogs replace inaccessible cached file rows with an unavailable
  location message, cancel the stale search, disable acceptance and retain the
  filename. Explicit valid navigation restores the file area. Private state
  uses QObject properties so the exported dialog class size is unchanged.
- Sidebar single-click and keyboard navigation are separated from Save/Open
  acceptance. Deterministic tests reproduced both the missing single-click
  navigation and unintended Enter acceptance before the correction.
- The custom sidebar now exposes native capability-aware unmount/safe-remove
  and optical-eject actions. Unmount retains Dolphin's terminal coordination;
  restricted teardown stays disabled. Menu ownership, persistent indices and
  trigger-time capability checks protect against device removal while open.
  Keyboard context menus target the selected row. No edit/hide/partition menu
  is added. Eject PNGs at 16/22/32/48 pixels are byte-identical copies from the
  already pinned icon-pack revision, not new artwork.

Working source/test evidence: `work/beta2-usb-discovery.v2ZvSz/` and the current
Explorer worktree. The pre-address-bar follow-up passes all 20 source CTest
groups (23.59s). The address-bar Enter test subsequently reproduced the same
unintended acceptance (2 setup/cleanup passes, 1 functional failure). A private
navigation-only line edit now consumes Enter after requesting folder navigation.
The final complete CTest rerun passes **all 20 groups (24.13s)**. The targeted
navigation and unavailable-location cases also pass. These changes leave the
ordinary filename field's event handling untouched. Source results are not
installed-package acceptance.

The storage-menu follow-up passes all 20 CTest groups (22.18s). Three new
main-window tests cover invalid/foreign model indices, capability-matched menu
contents/ownership, and ordinary bookmark activation without teardown. They
never execute storage actions against host devices. These checks are not a
substitute for actual USB/optical operations in the VM. The eject-icon fixture
first failed because the resource was missing; after adding the assets its
pixel comparison required normalization to the same premultiplied QImage
format. The corrected comparison and theme-independence checks pass.

Local package candidate: `work/beta2-explorer45.xwDCrt/`, Explorer 45,
8,249,643 bytes, SHA-256
`35c18226cc5cae9dc6d2d5283e0b9927d7f4857983816786e8fbb56920f96464`.
Source archive SHA-256
`a7b9856d9e60ff08858b2fe5e4508dd27ace1c99a7d5ec2f3b0c4b53a6f63dfd`.
All 14 packaged ELF files retain the same direct library requirements as 44.
The initial incremental-build attempt used stale source because `rsync` was
unavailable. Its package/logs were quarantined under `rejected-stale-source`,
never installed. The corrected build used a normal directory copy, an empty
recursive source comparison, and a fresh package build; only that hash above
is eligible for VM QA. This package is not in release media or published.

The offline VM completed a normal pacman upgrade from 44 to 45. Its recorded
package inventory changed only Explorer. Explorer (665 files) and unchanged
Paint 8 (709 files) both pass `pacman -Qkk`, and the saved Paint preferences
hash is unchanged. Local pacman reports missing sync databases on this
network-disconnected QA guest; the local-file upgrade completed successfully.
Evidence: `explorer45-upgrade.log`, before/after package lists and preference
hash file. This verifies package installation, not the remaining workflows.

## Explorer 45 live follow-up

The unmounted fixture is still missing in 45 (`420`). A native Solid/KIO
diagnostic identifies the actual input: the USB volume is a non-ignored FAT
filesystem on a removable/hotpluggable USB drive, but its StorageAccess object
reports `ignored=true` while its mount path is empty. This is confirmed in
`storage45-native-v4.log`. Early headless diagnostic attempts exited before
their timer when a KIO event-loop lock finished; the final probe disables
automatic quit-on-last-window/quit-lock termination and records 21 places and
52 Solid devices. Earlier empty probe logs are not evidence of missing devices.

The [upstream StorageAccess implementation](https://raw.githubusercontent.com/KDE/solid/master/src/solid/devices/backends/udisks2/udisksstorageaccess.cpp)
treats a path outside user mount locations, including an empty path, as ignored.
The [StorageVolume policy](https://raw.githubusercontent.com/KDE/solid/master/src/solid/devices/backends/udisks2/udisksstoragevolume.cpp)
separately preserves explicit ignore/hide options, swap and backing-file rules.
Working source now applies Access's path-based ignore only when accessible,
while retaining Volume's exclusions. Six additional input-policy tests and the
complete 20-group suite pass (21.40s). **This later correction is not in the
frozen Explorer 45 package; it needs the next package/VM verification.**

Mounted-device sidebar operation does pass in installed 45:

- Normal user `udisksctl mount` reveals `AERO7_QA (D:)` (`424`).
- Clicking it opens the real USB README. A right-click exposes Open, Open in
  new window and Safely Remove, with the bundled pack eject icon (`426`).
- Clicking Safely Remove returns the open USB view to the user's home (`427`).
- `storage45-audit.rFhu3k` verifies no mount of the fixture UUID, no failed
  system units, unchanged package files and unchanged Paint preferences.
  UDisks at 22:12:10 records mount cleanup, SYNCHRONIZE CACHE, START STOP UNIT
  and successful power-off through sysfs. No forced unmount was used.
- Shift+F10 immediately after navigating focused the file area, and therefore
  opened its folder menu (`425`); that screenshot is not sidebar-menu evidence.

The powered-off virtual USB device remains a QEMU controller object until the
QA harness detaches it. This success verifies this virtual USB safe-removal
path, not optical eject, busy-device failure, physical hardware or all storage
surfaces.

After the audit, QMP device removal completed (`info usb` empty) and the
backing node was closed. Host `mdir` still lists only the original 314-byte
README, with 100,446,208 bytes free. The fixture image is retained.

## Still required

- Installed Paint workflows and updated common-dialog regression fixtures;
  the rebuilt package and normal upgrade are done, with Paint unchanged.
- Native unmounted-drive click/setup, cancellation, device disappearance during
  setup, reconnect, busy-device failure and optical eject. The installed sidebar
  safe-removal path passed for the mounted virtual USB fixture only.
- Computer and common-dialog discovery/opening of unmounted removable drives,
  not just the sidebar; connected-but-unmounted drive presentation remains open.
- Installed verification of the unavailable-location message and navigation
  corrections, including restoration after reconnect.
- Physical hardware, final online/offline media rebuilds and end-to-end installs,
  plus the existing release-wide checks and publication approval.

Do not announce complete USB support or final Beta 2 acceptance from this pass.
