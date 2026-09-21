# Beta 2 refreshed-image rebuild and retest

Status: **release gate failed; fresh installation and reboot checks completed**.

Administrator authentication on the host succeeded through the local polkit
prompt. No host password was copied into commands. No commit, push, signing,
upload, or publication is authorized or performed by this test pass.

## Candidate refresh

The manifest now includes the previously tested Desktop 0.2.0-27, Explorer
25.12.3-34, and Control Panel 0.1.0-38, plus newly built:

- Gadgets 3.0.0-3: 3/3 package tests.
- Internet Explorer 0.1.0-5: 4/4 package tests.
- Device Manager 2.2.1.r1.g6d080f8-1: package compiled successfully.
- Computer Management 0.2.0.r20.g6d7fe79-2: 9/9 tests.
- Optional Programs Center 0.1.0.r12.g0405a2e-1: 3/3 tests.
- AeroThemePlasma Desktop 6.7.0_742.r9c2d850-39: 13/13 tests.

The theme preserves the packaged login/accessibility overlay and adds the
tested username fallback plus Snipping Tool resources from the existing icon
pack. Replacing the whole overlay with an older workcopy was deliberately
avoided because that would lose newer login behavior.

The first assembly check detected conflicting ownership of
`usr/share/applications/aero7-device-manager.desktop` between Computer
Management and Device Manager. Computer Management release 2 no longer
installs that compatibility launcher; Device Manager remains its sole owner.
This collision is fixed by package ownership, not by an overwrite exemption.
The existing installer still uses its separately scoped
`--overwrite usr/bin/aero7-file-explorer` compatibility flag; it does not use
a dependency-bypass flag. The earlier version of this report incorrectly said
there was no overwrite flag at all.

These are unsigned local QA packages built using the host toolchain, not
clean-chroot signed repository releases. Exact archives are checksum-pinned
in `config/beta2-local-packages.sha256`. Public recipe/source promotion remains
a separate approval and verification step.

## Build and test evidence

- Build recipes, source clones, package checks and assembly logs:
  `work/beta2-package-refresh.TT06FA/`.
- Prior failed images and disks remain preserved; both older QA guests were
  shut down through guest power controls, not by killing QEMU.
- Fresh QA workspace: `/home/admin/VMs/aero7-beta2-retest-zQPhkv/`.
- New guests: independent 64 GiB QCOW2 disks, UEFI OVMF, KVM/q35, 4 vCPUs,
  6 GiB RAM, virtio graphics at screenshot-verified 1920×1080. This changes the graphics device from
  the older QXL tests and is not proof that QXL repaint problems are fixed.
- Offline guest launcher specifies `-nic none`; online uses user-mode NAT.

## Refreshed ISO artifacts

Online ISO assembly completed and `scripts/verify-release.sh` passed, including
exact backend/source comparison and every embedded package checksum:
`aero7-beta2-online-2026.09.05-x86_64.iso`, SHA-256
`88bbffb4b021205a17a8115d24d35a72a6bca6149cdb9c17fbb6919c3caca5c8`.
Size: 1,454,522,368 bytes.

Offline assembly and the same embedded-artifact verification also passed:
`aero7-beta2-offline-2026.09.05-x86_64.iso`, SHA-256
`ec05d716462f996a673b66062aeabfe9cc8b3512554b3cc03482d7fcd0ec88d0`.
Size: 3,311,259,648 bytes. The candidate checksum file is
`out/beta2-candidates-2026.09.05.sha256`; older images/manifests are preserved.

## Fresh installed-system observations

Both guests completed disk installation, rebooted into account setup, and
reached the Aero7 desktop with disposable user `aero7test`. The offline VM had
no virtual NIC throughout; live and installed `ip -brief address` show only
loopback. No manual package or configuration repair was applied to either
guest to obtain these results. Transient root serial consoles were started
inside the disposable guests for diagnostics.

- Expected Desktop 27, Explorer 34, Control Panel 38, Gadgets 3 and Theme 39
  were installed. Programs Center was absent by default.
- Both EFI mounts use `fmask=0077,dmask=0077`; reading the boot random seed as
  the ordinary test user fails. SDDM state is mode 0600, owned by sddm, and
  selects `/usr/share/wayland-sessions/aero7.desktop`.
- At initial desktop audit, neither system nor user service managers reported
  failed units; no coredumps were present. This is not a clean OOBE-log pass.
- Both screenshot workflows produced a rectangular PNG on mouse release,
  closed the overlay without an editor, and pasted actual pixels into Paint
  with Ctrl+V. Clicking a fresh notification launched Gwenview with the saved
  PNG path. Online repeat capture and Escape cancellation also worked; the
  canceled attempt added no file.
- The online taskbar File Explorer launcher opened the branded application.
  Its saved library catalog contains exactly Documents, Music, Pictures and
  Videos, with no auto-created New Library. A separate Projects home folder
  still exists; this is not a claim of exact Windows visual parity.
- Start search on the offline desktop finds and opens the exact
  `Turn Aero7 features on or off` entry.
- Online Programs Center installation and removal through the feature UI and
  polkit succeeded, with matching package-query results and JSONL records.
  Full application launch and reinstall acceptance remain pending.
- The offline lock-screen branding is fully visible at 1920×1080 and a valid
  password unlocks it. Wrong-password rejection has a visual defect below.
- Both guests subsequently rebooted through normal SDDM login to Aero7 Desktop,
  without repeating OOBE. `reboot-audit.log` confirms OOBE disabled, SDDM active,
  `/usr/bin/aero7-session` selected, no failed system/user units and no cores.
  Each Desktop log folder now contains separate directories for both boots.
  Both login logos are fully visible; the online SDDM wrong-password message
  is visible and the following valid login succeeds. This distinguishes the
  locker feedback defect from the working SDDM error page.
- Journals are not completely empty of error-level messages: virtual-machine
  TDX capability and PowerDevil diagnostics are present, and switching to the
  diagnostic text console produces a KWin output-configuration message. The
  desktop returns after switching back; graphics-device coverage is limited
  to this virtio configuration.

Local evidence is under each variant directory in
`/home/admin/VMs/aero7-beta2-retest-zQPhkv/`. The `guest-logs.tar.gz` archives
contain the installer/OOBE/Shell/package logs and passed `gzip -t`; they are
private local QA artifacts, not website assets. Individual screenshots and
audit logs identify each check.

## Release-blocking findings

### 1. Offline Programs Center package identity check

The optional archive exists and SHA-256 equals
`1cc7c27bf85336f7caeef6549b74e3171b6f5cf8e5cda3c1e49d0d72909603b6`.
Nevertheless the normal feature UI fails with "invalid package identity".
`helpers/aero7-feature-helper` captures `pacman -Qp` with stderr merged into
stdout, then treats the first whitespace-separated token as the package name.
On the genuinely offline installation, missing sync-database warnings precede
the valid identity. Evidence: `offline/feature-failure-audit.log`,
`offline/13-feature-result.png` and the guest optional-features JSONL.
Separate metadata stdout from diagnostics; do not disable integrity checks or
populate repository databases over the network to hide this failure.

### 2. First-run configuration ownership in both variants

Both OOBE logs contain eight failed user commands, including `kwriteconfig6`
and creating `~/.config/aero7-shell`. The newly added configuration-only
Fastfetch adapter creates `~/.config/fastfetch` with `install -d -o USER`, but
does not explicitly create/own the intermediate `~/.config` first. A disposable
reproduction confirms that the intermediate directory becomes root-owned
0755 and is not writable by the user. Later light-default setup corrects its
ownership, explaining why the desktop starts despite earlier errors.

Evidence: both `oobe-warning-details.log`, offline `oobe-ownership.log` and
`ownership-reproduction.log`. Fix ownership before invoking the pinned Shell;
do not modify the separate pinned Shell tree. A subsequent clean-install run
must show those failed commands are gone, not merely a working final desktop.

### 3. Lock-screen wrong-password message is invisible

The offline locker rejects the deliberately incorrect password, but its
failure page shows only an OK button and no explanatory text, including after
settling. Pressing OK restores the prompt and the valid password unlocks.
Evidence: `offline/18-wrong-password.png`,
`offline/19-wrong-password-settled.png` and `offline/lock-auth-audit.log`.
This is a missing feedback message, not an authentication bypass.

## Remaining release gates

Normal post-OOBE reboot/login checks passed. Both-image full acceptance
is withheld because of the findings above. Feature reinstall, every Control
Panel applet/backend, multi-monitor, recovery/failure paths and physical
hardware coverage must not be represented as passed by these observations.

No successful-release announcement or publishable screenshot handoff is
produced from these failed candidates. Website download hosting and the
offline-ISO recommendation remain the intended release plan, contingent on
the corrected images passing fresh tests.
