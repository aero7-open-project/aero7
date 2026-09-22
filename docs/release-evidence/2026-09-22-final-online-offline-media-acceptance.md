# Beta 2 final online/offline media acceptance — 22 September 2026

This report records the local build identity and clean-install VM acceptance of
the exact Aero7 Beta 2 image pair below. It is evidence for a future release;
it is not signing, upload, repository promotion or publication approval.

## Exact artifacts

| Variant | Filename | Exact bytes | Display size | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Offline — recommended | `aero7-beta2-offline-2026.09.22-x86_64.iso` | 3,407,151,104 | 3.17 GiB | `f44c52bf8171fd2842e2c6150909e9ca70a577f4e3ac9f6444baeea45f1676a5` |
| Online | `aero7-beta2-online-2026.09.22-x86_64.iso` | 1,604,804,608 | 1.49 GiB | `e1744b3be9692af6252bfdc42b83a1bc4c309f33f300771dd3b26cfeacafc936` |

`scripts/finalize-release-artifacts.py` accepted both images and generated the
local `SHA256SUMS` and `BETA2-ARTIFACTS.md` records. A fresh hash verification
against that checksum file passed after both VM cycles were complete. The build
log contains `BETA2_FINAL3_20260922_OFFLINE_BUILD_AND_EXPORT_PASSED` and
`BETA2_FINAL3_20260922_ONLINE_BUILD_AND_EXPORT_PASSED`.

## Offline image acceptance

The exact offline image booted in a new UEFI/Q35 VM at 1920x1080 with no network
adapter. Installation and OOBE completed from the embedded package repository.
After the first password login:

- the installed audit ended with `FINAL_OFFLINE_INSTALLED_AUDIT_PASSED`;
- system and user failed-unit lists were empty and no current-boot coredumps
  were collected;
- firewalld was enabled and active;
- only loopback networking was present, and the expected disconnected clock
  state was retained rather than disguised as synchronized;
- Programs Center Beta installed from the verified bundled cache and removed
  again through **Turn Aero7 features on or off**;
- the first privileged feature action immediately displayed the Aero7 UAC
  authorization dialog;
- `plasma-polkit-agent.service` was active through the graphical-session target,
  resolved to `/usr/lib/systemd/user/plasma-polkit-agent.service`, and ran
  `/usr/lib/uac-polkit-agent`;
- reboot returned to the 1920x1080 Aero7 login screen, and the pinned taskbar
  shortcut opened File Explorer with the Aero7 name and icon.

The collector exported the installer, OOBE, journal, package and source-marker
evidence to the desktop log folder. Pacman database warnings in the disconnected
audit are expected because no repository databases were downloaded. The
`package ... was not found` lines verify that the two off-by-default optional
packages were absent after the removal check; they are not installer failures.

## Online image acceptance

The exact online image booted in a separate new UEFI/Q35 VM at 1920x1080 with a
working user-mode network adapter. Installation and OOBE completed through the
connected package path. After the first password login:

- the installed audit ended with `FINAL_ONLINE_INSTALLED_AUDIT_PASSED`;
- system and user failed-unit lists were empty and no current-boot coredumps
  were collected;
- `enp0s1` was up, the clock was synchronized and firewalld was enabled and
  active;
- Programs Center Beta installed and removed through **Turn Aero7 features on
  or off**;
- the first privileged feature action immediately displayed the Aero7 UAC
  authorization dialog;
- the graphical-session PolicyKit link, active unit and
  `/usr/lib/uac-polkit-agent` process were verified;
- reboot returned to the 1920x1080 Aero7 login screen with an unclipped
  **Aero7 Professional** mark;
- password login returned to the expected factory desktop, and the pinned
  taskbar shortcut opened the maintained File Explorer with its own name and
  icon;
- the powered-off disposable QCOW2 passed `qemu-img check` with no errors.

The `package ... was not found` audit lines again assert the final absent state
of optional packages after the install/remove test.

## Fix validated by this rebuild

The prior image could reach an administrator action before the graphical
PolicyKit agent was available. The rebuilt images install the graphical-session
wants link for `plasma-polkit-agent.service`. Both clean installations proved
that the agent is active at the first login and that the first feature-manager
elevation opens its authorization dialog without needing a logout, manual start
or second attempt.

## Preserved limits and remaining release work

- These are KVM/QEMU acceptance results, not physical GPU, USB, hotplug or
  physical multi-monitor certification.
- The tests do not claim warning-free logs, complete Windows compatibility or
  universal hardware support.
- The artifacts are not signed or uploaded. Final HTTPS URLs, download-back
  verification and explicit publication approval remain pending.
- The offline image remains the recommended download because its base install
  does not depend on network mirrors. Later updates, catalog downloads and some
  optional features can still require internet access.

The temporary installed-system disks were cleanly shut down, checked and
deleted after preserving screenshots and exported logs. The ISO files and
release metadata remain unchanged in the local output directory.
