# Online and offline ISO acceptance — 5 September 2026

## Decision: FAIL — do not release these images

Both available 4 September images completed the clean-disk installer, first-run
setup, first desktop login, lock/unlock, and an installed-system reboot. This
is **not a full acceptance pass**: artifact freshness, screenshot capture,
Start-menu discovery, default session selection, and boot-file permissions fail.
The 5 September source fixes have not been packaged into these images.

No ISO was rebuilt, uploaded, published, committed, or pushed during this test.
The requested release announcement is deferred until corrected final images pass.
Website planning notes are in `../BETA2-WEBSITE-HANDOFF-PREPARATION.md` and are not
permission to announce availability.

## Exact artifacts

| Variant | Filename | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Offline | aero7-beta2-offline-2026.09.04-x86_64.iso | 3302631424 | `82beeb5160b7edfa90f0598256b4bfbed97fc9a3680071a769a57e4952bbea07` |
| Online | aero7-beta2-online-2026.09.04-x86_64.iso | 1445894144 | `883e62870fb53376f6863bda67f92efff0532e9943d71e80bc66240dabe44bdf` |

Both match `out/SHA256SUMS`. Both fail the current `scripts/verify-release.sh`
with exit 2: the embedded `usr/share/aero7/beta2-optional-package-names.txt`
does not exist. Verification stops there; later checks are not claimed as passed.

## Environment and procedure

- Two independent, newly created 64 GiB QCOW2 disks; no physical disk access.
- QEMU/KVM q35, UEFI OVMF, 4 vCPUs, 6 GiB RAM per guest, QXL/SPICE, 1024×768.
- Offline guest: `-nic none`, no virtual network adapter at any stage. Guest
  `ip -brief link` shows loopback only before and after installation/reboot.
- Online guest: QEMU user-mode NAT. Initial pacstrap downloaded 1649.99 MiB;
  another package phase reported 109.66 MiB. These are not the ISO file sizes.
- GUI workflow: English/US defaults, Install now, license, Custom, the only
  64 GiB disk, explicit `/dev/vda` confirmation, automatic installation/reboot,
  new account, password, recommended settings, Amsterdam time zone, Public network.
- OOBE configuration and all disk writes were performed by the installer UI.
  A temporary root serial console was started from the guest's console for
  diagnostics; it is test instrumentation, not an installer dependency.
- Existing user VMs and the legacy `aero_desktop` tree were not modified.

Evidence root on the test host:
`/home/admin/VMs/aero7-beta2-acceptance-7Shb97/`

Each `offline/` and `online/` subfolder contains the retained disposable disk,
screenshots, QEMU log, installed installer/OOBE logs, package inventory, and
first/second boot diagnostics. `qmp.py` and `serial.py` document the input and
log-collection instrumentation. The directory contains local Unix control
sockets: it is an internal QA workspace, not a public download artifact.

## Results

| Check | Offline | Online |
| --- | --- | --- |
| SHA-256 against existing manifest | Pass | Pass |
| Current release-artifact verifier | Fail: missing optional manifest | Same |
| UEFI graphical installer and clean-disk install | Pass | Pass |
| Installation without internet | Pass, no NIC | Not applicable |
| Account/password/time/network OOBE | Pass | Pass |
| Initial normal Aero7 Wayland desktop | Pass | Pass |
| Taskbar Terminal / Explorer / browser pins visible | Pass | Pass |
| Explorer taskbar launch, File Explorer name/icon | Pass | Pass |
| Explorer Computer page, friendly C:/CD labels | Pass | Pass |
| Control Panel, Programs and Features open | Pass | Pass |
| Optional-features window from Control Panel | Opens; features unavailable offline | Opens; package availability shown |
| Optional-features entry in Start search | Fail | Fail |
| Meta+Shift+S region capture | Fail: KWin authorization | Same |
| Lock; reject wrong password; accept correct password | Pass authentication; error text needs review | Same |
| Lock-screen Aero7 logo at 1024×768 | Visible, not clipped | Same |
| Normal reboot and password login; OOBE stays disabled | Pass | Pass |
| Normal session remains selected after reboot | Fail: Safe Mode selected | Same |
| System/user failed-unit snapshot after second login | None | None |
| Coredump inventory at inspection | No coredumps | No coredumps |
| Desktop diagnostic folder and retained installer logs | Present | Present |
| Collected diagnostic folder SHA-256 manifest | Pass, exit 0 | Pass, exit 0 |

`systemd-analyze` reported 11.434 seconds (offline) and 11.637 seconds (online)
for kernel + initrd + userspace startup. These numbers exclude firmware,
interactive login, OOBE, and installation, and are not physical-laptop benchmarks.

## Blocking findings and reproduction

1. **Outdated artifacts.** Installed packages include Desktop `0.2.0-25`, File
   Explorer `25.12.3-32`, Control Panel `0.1.0-33`, and Gadgets `3.0.0-1`.
   These differ from the candidate versions in the release notes. Programs
   Center is already installed rather than optional/absent by default.
   Evidence: `installed-diagnostics.log`, `26-programs.png`, and root image
   verification logs. Build and verify updated signed packages before rebuilding.

2. **Screenshot shortcut does nothing useful.** Press Meta+Shift+S from the
   desktop. Spectacle starts, but no selection overlay appears. The journal says
   `KWin screenshot request failed: The process is not authorized to take a screenshot`.
   This reproduces on both initial normal Wayland sessions. PNG saving, image
   clipboard contents, notification, and notification-click opening cannot pass.
   Evidence: both `screenshot-shortcut.log` files. Do not bypass KWin permission
   checks to make a test appear green; correct application identity/authorization.

3. **Features hidden in Start.** Search `features`: no application result.
   `/usr/share/applications/aero7-optional-features.desktop` has
   `Name=Aero7 Optional Features` and `NoDisplay=true`. The Control Panel link
   works, but is not a substitute for the requested searchable entry.
   Evidence: `features-entry.log`, `24-feature-search.png`, `27-features.png`.
   Offline optional enable/remove/re-enable is not validated and is blocked by
   unavailable package metadata/candidate content.

4. **Default login switches to Safe Mode.** After the initial desktop, reboot
   normally and enter the password without touching the session selector.
   Both SDDM logs select `aero7-safe.desktop` and launch
   `/usr/bin/aero7-session --safe-mode`. Initial OOBE autologin used normal Aero7.
   Evidence: `second-boot-diagnostics.log`, `session-and-log-retention.log`.
   Successful second login therefore does not certify normal-session persistence.

5. **Boot random seed accessible to ordinary users.** `/boot` and
   `/boot/loader/random-seed` are mode 0755; `runuser -u aero7test -- test -r`
   succeeds. The persistent FAT mount uses `fmask=0022,dmask=0022`. Bootctl warns
   on the installed first and second boots. Fix restrictive ESP mount permissions
   and retest as an unprivileged user; this is not only a live-media warning.
   Evidence: `integration-checks.log`, both boot diagnostic logs.

## Additional issues / qualifications

- Offline OOBE logs `[FAIL] Unavailable pacman package(s) fastfetch` while later
  calling the result healthy. `/usr/bin/fastfetch` is actually present, so this
  points to offline availability/configuration handling, not a missing binary.
- Offline package queries warn that core/extra/aero7 sync databases are absent.
  `pacman -Dk` nevertheless reports no installed-database errors on both guests.
- Fresh Explorer creates `New Library`; source explicitly adds this because
  it appeared in a reference screenshot. `Projects` is also present. Review
  factory defaults rather than claiming these are leftover user files.
- The diagnostic folder sorts ahead of Recycle Bin. Clock and Weather gadgets
  also autostart. Document the test-image exception to the clean-desktop promise.
- Weather correctly reports unavailable offline, but also shows `0°`; online
  eventually shows a temperature. Offline error wording is clipped at this size.
- SDDM's user-name text is not visible in the captured login screen; the wrong
  password lock-screen state shows an OK button without explanatory text.
  Reproduce these visually before declaring login accessibility complete.
- QXL/SPICE captures sometimes show incomplete repaints. Switching virtual
  terminals can restore them. KWin output-configuration warnings occurred
  around VT changes; they must not be silently treated as full graphics approval.
- Other journal warnings include missing oxygen fallback icons, invalid SVG
  references, unavailable kameleon, portal app-identity failures, and optional
  hardware services. No-NIC weather, no battery/backlight/BlueZ, and unsupported
  virtual CPU facilities must be distinguished from actual application failures.

## Remaining acceptance work

After repairs, build new images and restart the clean-disk matrix using their
new hashes. Test normal session selection and a second normal-session login;
optional feature install/remove/repair/re-enable (including Programs Center
without internet); screenshot PNG/clipboard/notification/viewer end to end;
file create/copy/move/rename/trash/restore and search; theme changes; all Control
Panel backends; accessibility/session selection; display changes and multiple
monitors; sound/microphone; networking/Wi-Fi; suspend/resume; recovery; and
installer failure paths. These were **not completed** in this failed-candidate
pass. No physical-hardware or advanced partitioning acceptance is implied.

Retain the failing images and evidence for comparison. Do not publish the ISO,
an availability announcement, or final website screenshots until that gate passes.

At handoff both disposable VMs are left running at their desktops for inspection.
The temporary diagnostic root serial services were scheduled to stop; no such
service was enabled persistently. No application/package repairs were applied
to mask the failing-candidate results.
