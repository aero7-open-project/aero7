# r8 final-media acceptance — in progress

This is local QA evidence, not release approval. No final r8 installation has
passed yet. Do not publish these candidates or infer acceptance from prior VMs.

## Candidate and build

- Control Panel: `0.1.0-47`, including failed-check handling, active-update
  window/navigation protection and wrapped waiting guidance.
- Candidate manifest SHA-256:
  `ba0233b31855ec7056b3cd4133a3ab13fbc67bead5954649c8282fec57f014ce`.
- Prepared profiles: `work/beta2-updater-final.8Q4lde/profile-offline` and
  `profile-online`; preparation passed 130 backend tests and three installer
  CTest groups for each variant.
- Builder: existing isolated QEMU guest `aero7-beta2-builder.HD2BwR`, unit
  `aero7-r8-builder.service`. Output:
  `work/beta2-profiles.UWsuLM/builder-output/r8-updater/`.
- At 16:46 CEST, the unit was active, mksquashfs was using 176% CPU across two
  virtual CPUs, and the kernel had no matching OOM or I/O-error entries.
  `health-1646.txt` records this checkpoint. Compression subsequently advanced
  past 50%; the early unchanged progress display was not proof of a hang.
- Build completion and exact-ISO verification subsequently passed for both
  variants (hashes below). The external verifier compares the exact firewall module,
  installer backend, adapter and compiled frontend against candidate inputs.

## Fresh test preparation

New isolated test root: `/home/admin/VMs/aero7-beta2-r8-pWRIgW`.
Its launcher refuses an existing guest directory and creates a standalone
64 GiB virtual disk. Offline uses no NIC; online uses QEMU user networking.
Both use 1920×1080, 6 GiB RAM and two virtual CPUs. Read-only test inputs and
a separate writable results share do not expose host disks for installation.
The fresh offline guest was created and booted at 16:56 CEST. QMP confirmed
the exact new 64 GiB disk with only 200704 allocated bytes and no backing file;
its CD is the verified r8 offline image. No installation is complete yet.

### Offline export and exact-image verification

The builder emitted `R8_offline_BUILD_AND_EXPORT_PASSED`. The external
`scripts/verify-release.sh` returned zero and printed
`Aero7 Beta 2 offline image verification passed.` The log is
`work/beta2-updater-final.8Q4lde/verify-offline-r8.log`.

- File: `aero7-beta2-offline-2026.09.06-x86_64.iso`
- Bytes: `3318005760`
- SHA-256: `a04701a31aef268f7143b7afbe22c7046d067f9854f958d47996aa44bb0e73a7`
- Folder: `work/beta2-profiles.UWsuLM/builder-output/r8-updater/`

This validates the embedded inputs and archives, not fresh installation or
desktop behavior. The online builder continues; do not substitute its previous
output merely because an identically named file already exists inside the VM.

At 16:59:13, installation was approved for the new guest `/dev/vda` only.
The confirmation displayed 64.0 GiB and the exact guest path. QMP showed no
network interfaces. English interface, Dutch regional formatting and US keyboard
were selected. Installation is running; this is not yet an installed-system pass.

### Reproduced disk-label issue — open

The only eligible disk is labelled `Disk 3: Unknown disk`, also observed on r7.
Screenshots `07-disk.png` and `08-erase-confirm.png` reproduce this on r8.
`candidate_disks()` enumerates all lsblk top-level nodes before filtering loops
and other non-disks, so the visible disk index includes unrelated block devices.
The confirmation still identifies `/dev/vda`, and the QMP target is the intended
new empty disk. This display issue is not evidence of wrong-disk writes, but it
needs a regression test and corrected presentation. The unknown-model fallback
also provides little useful identification for virtual disks. Keep this issue
open; r8 is not a final release acceptance pass merely because it installs.

Source correction, after both r8 verifications completed: physical supported
disk paths are numbered before eligibility filtering, excluding loop/optical/
zram rows while preserving numbers when another real disk becomes mounted.
Missing/blank models now display the device path. Three new regression tests
reproduced the old failures, and all 133 backend tests passed after correction.
Evidence: `work/beta2-updater-final.8Q4lde/disk-label-before.log`,
`disk-label-after.log`, `backend-disk-label-tests.log`. The immutable r8 images
do not contain this correction; rebuilt-media verification remains required.

### Online build and verification

Both builder export markers and `R8_BUILDER_EXIT=0` are present. Online
`verify-release.sh` also returned zero before the subsequent source correction.
Log: `work/beta2-updater-final.8Q4lde/verify-online-r8.log`.

- File: `aero7-beta2-online-2026.09.06-x86_64.iso`
- Bytes: `1547694080`
- SHA-256: `014c8ac8ab0c3f2f516459878740d2da42f0f4a837cf3bc10a7fce8294b2db6e`
- Same r8 output folder as offline.

The new online guest was launched at 17:09 CEST; installation began at 17:12:11
on its newly created `/dev/vda` only. It reached account setup without manual
repair. No earlier candidate or existing guest disk was reused. OOBE selected
automatic checks on and Home on the connected virtual NIC; finalization and
installed-state verification remain pending at this checkpoint.

### r8 offline first-login audit

The offline image completed installation and OOBE without manual repair and
reached the desktop. Automatic update checks were explicitly set off. Home was
selected while no NIC existed; setup visibly reported retaining Public defaults.
At 17:08:49 the installed audit printed
`R8_INSTALLED_STATE_AND_PUBLIC_PACKET_CHECKS_PASSED`: exact versions of all 12
required local candidate packages, zero missing package files, firewalld
active/enabled, no UFW, Programs Center absent by default, Public IPv4/IPv6
inbound blocking and outbound replies passed. There were no failed system
services or current-boot coredumps in that checkpoint. Timezone was correctly
Europe/Amsterdam. No NTP synchronization is expected without a NIC.
Evidence: `/home/admin/VMs/aero7-beta2-r8-pWRIgW/offline/results/installed-audit.log`.
This does not yet prove reboot, the complete application matrix or final media
containing the new disk-label correction.

### Offline reboot and account checks

The normal Start-menu restart at 17:13:00 completed: the old boot ended at
17:13:01 and the new kernel boot started at 17:13:07. Boot IDs changed from
`ebe74dc4113b40608ff4a4010e44835c` to `f5651dad3d4248b6aae2a2f6615a66f2`.
Password login succeeded, the 1920×1080 Aero7 branding was fully visible, and
the installed/package/firewall packet audit passed again at 17:20:05 without
repair. Evidence: offline `results/boot-history-1719.log`,
`session-audit-1719.log`, `session-journal-1719.log`, screenshots 24–26.

Before reboot, normal-user checks also verified that the actual update helper
exits with “Automatic update checks are off”, while manual configuration remains
available. Firewall information queries were allowed without authorization;
mutation actions still required authorization. Evidence: `a7-user-defaults.log`
and `a7-user-policy.log`. These are specific checks, not full desktop acceptance.

### Online first-login audit

The online guest completed installation and OOBE and reached its desktop with
no manual repair. At 17:24:06 the installed audit passed the same required
package, missing-file, service and Public-zone packet checks as offline.
The actual connected `enp0s1` interface belongs to `aero7-home` in permanent and
runtime state; the fallback default remains `aero7-public`. Automatic checks
are recommended/on. Normal-user defaults and information-policy checks passed;
information queries took about 0.34 seconds and mutations still require auth.
Logs are under the online guest's `results/` directory. Online NTP is inactive
at this checkpoint, despite connectivity; investigate before advertising
automatic clock synchronization. Application checks remain pending.

Start-menu Restart was selected at 17:28:26. The old boot ended at 17:28:29,
and the new kernel started at 17:28:36, with boot ID changing from
`d9fb8f28c9f4452d91af4422b3bb00e8` to `dadcdc085471435f96144e1a2f5bc1cd`.
Password login succeeded and the full installed audit passed after reboot.
Home remained assigned to `enp0s1`, with Public still the default fallback.
Evidence: online `results/post-reboot-audit.log`, `post-reboot-boot-history.log`,
`post-reboot-connections.log`, both boot journals and screenshots 17–22.

### Optional Programs Center, fresh disconnected guest

On r8 offline, Programs and Features exposes “Turn Aero7 features on or off”.
Programs Center Beta was absent initially. Selecting its checkbox showed the
explicit package-change confirmation and then required administrator approval.
Installation completed without a NIC, and the Open button launched Programs
Center. It correctly warns that repository information is unavailable and
retains installed-program browsing. Screenshots 30–34 record this flow.
Removal also completed after explicit confirmation and administrator password
approval. The pacman log confirms installation at 17:24:15 and removal at
17:29:49 of `aero7-programs-center-git 0.1.0.r12.g0405a2e-2`; no other packages
were removed. Evidence: screenshots 35–39 and
`results/pacman-after-feature-removal.log`. Re-enable still needs a separate test.
During later log collection, an expired sudo authorization made two queued
diagnostic commands land in the password prompt. The actual QA password then
succeeded without changing PAM or credentials. Those two log-collection
authentication failures were test-input errors, not failed GUI feature actions.

### Setup clock preview correction in source — not in r8

Online screenshot `09-time.png` shows Europe/Amsterdam selected but 15:19:52,
two hours behind the actual 17:19:52 CEST. `TimeScreen.qml` used process-local
JavaScript dates while timezone application happens later. Installed timezone
is correct. A display-only controller conversion now supplies selected-zone
calendar and clock fields using Qt's timezone database; the analog and digital
clocks share those fields. The decorative DST checkbox is now read-only with
an explanation that the selected zone supplies DST rules, rather than accepting
a change that is never applied. Source build and all three installer CTest
groups passed (23.72 seconds), including selected-zone QML binding, summer/
winter offsets, DST boundary, invalid zone and year/day rollover. The 1920×1080
Tokyo preview was rendered and inspected: calendar day and both clocks agree.
Evidence: `work/beta2-updater-final.8Q4lde/time-preview-tests.log` and
`time-preview-screens/time-preview-tokyo-1920.png`. This is a source simulation;
the correction still requires rebuilt-media acceptance.

## Retained intermediate evidence

The r4 online guest was manually upgraded to Control Panel r47. Its final mock
updater log and fixture markers were collected into
`/home/admin/VMs/aero7-beta2-r4-Nlm227/online/r44-results/r47/`.
The copied pacman log's last transaction was the explicit r46-to-r47 upgrade;
the simulated updater did not execute a real package transaction. UFW remained
active and enabled. This is not full-system-upgrade acceptance.

That guest shut down through Start at 16:44:56; its QEMU process was gone at
the next check, less than 30 seconds later. No forced power-off was used. Its
disk and logs remain. This successful shutdown does not by itself clear the
older intermittent shutdown timeout.

The fresh r7 offline guest (older CP r44 image) showed the expected incorrect
password message during lock-screen testing. One automated retry also failed;
the next retry, after waiting for the form and explicitly clearing/retyping,
successfully unlocked without resetting credentials or altering PAM. Input
timing is a possible explanation, not a confirmed diagnosis. Repeat this on r8.
Screenshots `34-wrong-password.png`, `36-retry-form.png`, and
`38-unlock-result.png`, plus `results/after-lock-test.log`, are retained under
`/home/admin/VMs/aero7-beta2-r7-xGDR49/offline/`. The Aero7 branding is fully
visible in these 1920×1080 lock-screen captures.

The r7 guest subsequently shut down through Start at 16:50:01; its QEMU process
was absent at the next check. Its disk and results are preserved. Only the
builder remains running from these three test guests.

## Remaining acceptance gates

### Build-drive cleanup during r8 export

The owner-approved obsolete-artifact cleanup removed only
`/home/admin/VMs/aero7-beta2-r5-oz8Pm4/offline/disk.qcow2` (about 6.4 GiB).
Immediately before deletion it was a regular, non-symlink file, had no fuser
holder and no live guest QMP socket. All eight then-present VM qcow2 backing
chains were inspected; no other disk depended on it. This was the old manually
repaired r5 guest, not a fresh acceptance candidate. Its results, screenshots,
inputs and scripts remain. Replaying that guest now requires reinstallation;
the disk was permanently deleted, not put in Trash. Host free space rose from
about 13 to 19 GiB. Current r7, both r4, builder and reference disks remain.

At the later low-space checkpoint (3.4 GiB free), the obsolete stopped r7
`/home/admin/VMs/aero7-beta2-r7-xGDR49/offline/disk.qcow2` was also permanently
deleted, freeing about 6.4 GiB. Regular-file/non-symlink, no-holder and absent
QMP-socket checks passed; all nine then-present qcow2 backing chains were
inspected, with no disk depending on r7. Its logs/screenshots/scripts remain;
recreating that guest requires reinstalling. Both r4 disks, current r8 disks,
builder and Windows/desktop/wiki reference disks were preserved. The completed
builder shut down normally through `systemctl poweroff`; its PID exited.

### Tests still required

- Rebuild images with the later disk-label, timezone-preview, time-service
  startup and Control Panel r49 Internet Time corrections;
  checksum/verify their exact embedded inputs, then repeat fresh installation.
- r8 no-network offline installation, OOBE, reboot/login and audits have passed;
  this is intermediate evidence, not acceptance of subsequently corrected media.
- r8 online installation, OOBE, reboot/login and audits have also passed;
  finish the app matrix and repeat it on the later corrected media.
- Repeat update preferences, firewall policy, optional Programs Center lifecycle,
  desktop/application checks, lock failure/recovery and repeated session exit.
- Record untested hardware, multi-monitor and recovery paths explicitly.
- Populate final website artifact/screenshot inventory only from accepted bytes.
- Obtain separate approval for commits, signing, promotion and publication.

### Later time-service and r49 package checks

The missing NTP startup action was corrected in the installer source. Manually
applying that action synchronized the online guest and started safely with no
NIC in the offline guest. Both remained enabled/active after another normal
reboot/login; the online guest synchronized again with its selected server.
These are explicitly modified r8 guests, not fresh corrected media.

Control Panel r48 GUI checks covered invalid server input, cancelled approval,
selected-server Update now, and offline off/on. A later malformed IPv6 scope
regression superseded r48 with r49. All 18 source/package groups and the full
ISO static checks passed; both guests installed r49 with zero altered package
files. No replacement ISO has been built yet. The original r8 hashes above
still describe unchanged older media and must not be promoted.

The offline lock screen rejected a wrong password and then accepted the correct
password; one failure/recovery sequence is recorded, not every lock scenario.
See [time synchronization evidence](2026-09-06-time-synchronization.md) for logs,
package hashes, screenshots, remaining warning qualifications and boot IDs.
