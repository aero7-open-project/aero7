# Beta 2 corrected candidate acceptance

Status: **in progress; not approved for publication**.

This is a new test run, not a replacement for the failed-candidate record in
[the previous rebuild report](2026-09-05-rebuild-and-retest.md).

## Changes being verified

1. Control Panel `0.1.0-39` separates `pacman -Qp` metadata stdout from stderr
   warnings. Offline package identity validation still requires a successful
   query, the exact package name/version shape, and the pinned SHA-256.
2. The installer explicitly creates and assigns the user's `.config` parent
   before Fastfetch configuration and the pinned Shell's user setup commands.
   The separate pinned Shell source is unchanged.
3. Theme `6.7.0_742.r9c2d850-40` keeps lock-screen authentication failure text
   when the authenticator becomes idle and ignores empty informational messages.
   A new attempt or dismissing the failure resets feedback deliberately.

## Source/package checks

- Optional-feature helper: 14 Python tests passed, including stderr warnings,
  incorrect package identity and failed metadata queries.
- Control Panel package: 12/12 CTest executables passed.
- Installer disk/backend tests: 70 tests passed, including parent ownership order.
- Theme package: 13/13 CTest executables passed. These do not replace real
  lock-screen authentication checks.
- Offline profile preparation passed its complete source and payload checks.

Local package/build logs: `work/beta2-blocker-fixes.FXng3D/`.
Fresh guests: `/home/admin/VMs/aero7-beta2-fixed-mSLoUt/`.
Each guest has its own new 64 GiB virtual disk, UEFI, 4 vCPUs, 6 GiB RAM,
and a 1920×1080 virtio display. Offline uses `-nic none`; online uses NAT.
Only disposable virtual disks are installation targets.

## Acceptance results

Both initial corrected ISOs assembled and passed exact embedded verification.
Both completed fresh installation and OOBE on their own new disks. Initial
system/user failed-unit and coredump checks were clean, and OOBE logs had no
permission-denied or failed setup commands. Offline had no network device.

These are intermediate candidates, not final accepted release images:

| Variant | Bytes | SHA-256 |
| --- | ---: | --- |
| Offline | 3311304704 | `14b7f5057681761337146253d183b7ca3868e302e1c9e32afd9a3361d7861553` |
| Online | 1454567424 | `36d7b9e268958b15be04c727a2457bedd935039ae0292314f65e67efcbe34689` |

### Verified desktop behavior on the intermediate candidates

- Offline: Start search finds Turn Aero7 features on or off. Installing Programs
  Center Beta through that UI and the normal authentication prompt succeeds with
  no NIC; the completion dialog opens the application.
- Both: wrong-password lock feedback remains visible; valid-password unlock
  restores the desktop. The branding is fully visible at 1920×1080.
- Online: Meta+Shift+S, drag, release saves a 601×401 PNG without opening the
  Spectacle editor. Ctrl+V pastes actual image pixels into Paint. Clicking a
  second capture's notification opens that PNG in Gwenview. Escape cancels a
  subsequent selection without creating a third image. No Spectacle process,
  failed units or coredumps remained in the subsequent audit.
- Evidence: guest `offline/19*`, `offline/22*`, `offline/26*`,
  `online/10*` through `online/13*`, and
  `online/screenshot-workflow-audit.log`.

### Additional bugs found and local fixes

1. Programs Center's installed page incorrectly showed zero applications without
   repository databases. It now starts from the installed ALPM database, merges
   repository data without duplicate package rows, and resolves application
   metadata from package-owned desktop files. Missing repository data produces
   an explicit warning rather than an up-to-date claim. Four tests pass.
   Package `0.1.0.r12.g0405a2e-2` was manually upgraded in the offline guest:
   `offline/29-programs-local-inventory.png` shows 28 applications, and
   `offline/33-updates-status.png` shows the unavailable-information warning.
2. Many Control Panel applets used generic fallback icons despite appropriate
   assets existing in the pinned Windows 7 Aero icon pack. Original pack bytes
   are now bundled for all 45 entries, with semantic aliases where needed.
   The new regression verifies dedicated asset resolution and theme independence
   for every applet. All 12 CTest executables pass. Package `0.1.0-40` installs
   successfully in the offline guest; `offline/36-cp40-all-icons.png` verifies
   the corrected five-column icon grid.

Further intermediate-guest checks: cancelling removal at the authentication
prompt retained Programs Center and reported that no changes were made
(`offline/43-auth-cancel.png`, `auth-cancel-audit.log`). Retrying with valid
authorization removed the program and changed its status to Not installed
(`offline/46-remove-complete.png`, `removal-poweroff.log`). The online guest
completed a normal reboot, SDDM login and second desktop session
(`online/15-reboot-current.png`, `online/17-second-login-ready.png`), with no
failed system/user units or coredumps in `second-login-audit-confirmed.log`.

The Control Panel packaging log reaches successful completion and its archive
passes decompression and identity checks; the enclosing tool session reported
signal exit 143 after completion. The package was independently installed in
the guest rather than relying solely on that tool status.

The ISO payload manifest now selects these additional fixes. Refreshed ISO
assembly, exact verification, another fresh install, normal reboot and remaining
desktop regression checks are pending. Manually upgraded guests do not establish
success of the refreshed installation media.

## Refreshed image run

Fresh guest root: `/home/admin/VMs/aero7-beta2-final-CZc2ad/`.
Earlier guests were shut down cleanly and preserved, not reused as fresh disks.

- Offline refreshed ISO: 3,314,872,320 bytes;
  SHA-256 `3e5915706a0b20c8f9f81a64ffcb1db88c64b83e9389d1f09c5c6eccd74cf5df`.
  Exact embedded-source, variant and package-manifest verification passed in
  `verify-offline-r2.log`. A new no-NIC guest has been started for installation.
- Online refreshed ISO: 1,458,135,040 bytes;
  SHA-256 `2b658e7e29364a66f0a760bdae9b5fe150fff5eecd48d696e120b71a4a207f36`.
  Exact verification passed in `verify-online-r2.log`. A new NAT guest has
  started for installation. Both builder logs reached completed ISO assembly;
  tool sessions again reported signal exit 143 after the completed output.
  Independent image verification passed on the resulting bytes.

Checksum file: `out/beta2-refreshed-candidates-2026.09.05.sha256`.

No commits, pushes, repository promotion, ISO uploads, website edits or release
publication have been performed by this pass. Local QA packages are unsigned;
signed release packaging is a separate gate.

## Refreshed-image fresh installation and further regression checks

Both guests in `aero7-beta2-final-CZc2ad` completed installation and OOBE on new
64 GiB virtual disks. Offline has no network adapter; live and installed
`ip -br link` show only loopback. Initial installed audits confirm Desktop 27,
Explorer 34, Control Panel 40, Theme 40 and Gadgets 3, with Programs Center
absent by default. User configuration ownership, SDDM state permissions,
installer/OOBE completion, failed-unit checks and coredump checks passed.
These are fresh-image results, not manual package upgrades.

Offline additionally passed:

- Nested multi-monitor test: three outputs, disable to two, re-enable to three,
  125% scaling, and one correct Aero7 panel per output. This is simulated
  output coverage, not physical GPU hotplug acceptance (`multimonitor-result.log`).
- Forced shell termination and recovery to the Aero7 identity/layout, plus
  the supported restart command (`recovery-r2-complete.log`). The original
  test queried D-Bus before the restarted shell registered its interface.
  `tests/vm/test-recovery.sh` now waits a bounded time for readiness and still
  rejects a wrong identity. The initial test failure remains preserved.
- Stock-panel injection/reconciliation, invalid Control Panel deep-link and
  migration-path failure handling, and retired overlay absence
  (`failure-tests-result.log`).
- Programs Center Beta installation, removal and reinstallation through the
  real Features UI, including administrator authentication. The local cached
  version is `0.1.0.r12.g0405a2e-2`; all three transactions appear in
  `optional-cycle-audit.log`, with loopback-only network evidence. Installed
  Programs displays 28 applications and Updates explicitly reports missing
  repository information (`21-installed-programs.png`, `22-offline-updates.png`).
- Start search finds **Turn Aero7 features on or off**. Opening Programs Center
  from the reinstallation completion dialog works when Features is launched
  normally from Start (`23-start-features.png`, `27-start-launched-open.png`).
  The earlier QA launcher used a transient service with the default main-process
  lifetime, which killed detached descendants when Features closed; that
  harness-only launch was not counted as product failure or successful launch.

The online guest's taskbar Explorer shortcut opens the correctly named/iconed
application. Computer shows friendly C:/D: drives rather than internal mounts.
Lock-screen branding and persistent incorrect-password feedback are visible
in `08-current-state.png` and `09-lock-wrong-password.png`.

### Additional confirmed Explorer defect — candidate refresh required

`online/06-computer.png` exposes a clipped processor line in Computer's bottom
details strip. A one-line fixed label height was constraining two-line text.
The source now permits the label/host to grow to their content while preserving
the normal 54-pixel strip minimum. A regression test checks normal, large and
accessibility font sizes and verifies the label remains inside its parent.
All 18 Explorer CTest executables pass after the change; the targeted test
passes at 9, 12 and 18 points. Logs: `/tmp/aero7-explorer-footer-*.log`.

A local unsigned Explorer `25.12.3-35` package is being built from the exact
working-tree snapshot in `work/beta2-blocker-fixes.FXng3D/explorer-footer/`.
The refreshed r2 ISOs above still contain Explorer 34 and are **not final
accepted release artifacts**. They must be refreshed and checked again.

Normal reboot/second-login and the remaining final-image UI checks were still
pending at that checkpoint. Vendor QML/icon and deliberate recovery-test
shutdown warnings remain in logs; this report does not claim all logs are empty.

## Subsequent r2 checks and r3 refresh

Explorer 35 finished building successfully. Its archive SHA-256 is
`042f465d288f212ca76e3934c04c2127fae5e9b10e18e4d570f20f9ff217c303`.
The source snapshot SHA-256 is
`ac526a572eb88e3909a6ad494037390d76128d3e35260e7bb4d9bc854e57e6a7`.
The offline r2 guest was manually upgraded only for this Explorer check:
`28-explorer35-computer.png` confirms the full processor line is visible.
This manual check is not fresh Explorer 35 installation evidence.

Additional r2 offline results:

- All 45 Control Panel items displayed in five columns with bundled icons
  (`31-control-panel-45.png`).
- Screen Resolution changed the real output to 1600×1200, displayed the
  confirmation timer, and automatically restored 1920×1080 when not confirmed
  (`34-resolution-change.png`, `35-resolution-reverted.png`).
- The gadget gallery opened and a Clock was added. It persisted through normal
  reboot and a second SDDM login (`37-clock-desktop.png`, `41-reboot-desktop.png`).
- Post-reboot SDDM selected the Aero7 Wayland session. Configuration ownership,
  permissions, failed-unit checks and the corrected current-boot coredump query
  passed (`post-reboot-audit.log`, `post-reboot-display-audit.log`).

Additional r2 online results:

- Valid unlock succeeded after testing persistent wrong-password feedback
  (`15-unlocked.png`).
- Meta+Shift+S opened region selection; release saved a 601×401 PNG, closed the
  overlay, left no Spectacle editor process, and displayed the notification.
  Clicking opened Gwenview; Ctrl+V pasted actual pixels into KolourPaint
  (`16-region-selection.png` through `18-notification-viewer.png`,
  `21-pasted-into-paint.png`, `screenshot-after.log`). Escape cancellation
  created no additional PNG (`pre-reboot-audit.log`).
- Normal reboot, SDDM session menu and second login passed
  (`23-sddm-after-reboot.png` through `25-second-login.png`).
  `post-reboot-verified.log` confirms successful Aero7 Wayland authentication,
  no failed system units and no current-boot coredumps. Its extra queries used
  two wrong names (`/etc/sddm.conf` and `aero7-control-panel`); their errors are
  diagnostic-command errors, not evidence those components are missing.

QA limitations/errors are retained, not hidden: typing too soon after lock
feedback dismissal hit the theme's three-second input delay and the test
account's PAM limit; only the disposable QA account's failure counter was reset.
Typing after the delay unlocked successfully. An offline diagnostic launched
`kscreen-doctor` without the Wayland environment and caused a Qt abort; the
corrected user-manager invocation succeeded after reboot. `coredumpctl -b` is
unsupported here; current-boot journal queries replaced it. Neither error is
counted as successful product coverage.

The r3 offline ISO has rebuilt and passed embedded-payload/dependency-closure
verification (`verify-offline-r3.log`). The online r3 build and fresh r3 guests
are in progress. Their dedicated root is
`/home/admin/VMs/aero7-beta2-release-check-Mnoerz/`. Old guests and artifacts
remain preserved; no release, repository promotion or upload is authorized.

## r3 fresh installations and normal reboot — completed checks

Both r3 images finished building and passed their embedded-payload verifiers.
These are intermediate QA identities, **not approved download artifacts**:

| Variant | Filename | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Offline | `aero7-beta2-offline-2026.09.05-x86_64.iso` | 3314872320 | `2bee542fe18d6f315d50f7008d7bcfeed76bf025b6e49c85d58a477d2b07e75f` |
| Online | `aero7-beta2-online-2026.09.05-x86_64.iso` | 1458135040 | `e1af2fa2afef38a1cac8a5ad53ec2280693716a22b1c096c81b50e4d32f723aa` |

Evidence root: `/home/admin/VMs/aero7-beta2-release-check-Mnoerz/`.
Each guest has `iso.sha256`, `initial-installed-audit.log`,
`install-and-oobe-full.log` and `post-reboot-audit.log`.

- Fresh installation, account setup, first desktop, normal reboot, password
  authentication through SDDM and second Aero7 Wayland login passed in both.
  `42-current.png` and `43-reboot-login.png` record the latter two UI states.
- Offline has no network adapter and only loopback. Its frozen kernel is
  `7.2.2-arch1-1`; online installed `7.2.3-arch1-2` from the current repositories.
  This difference is expected for frozen offline versus online base packages.
- Both have Desktop 27, Explorer 35, Control Panel 40, Gadgets 3 and Theme 40.
  Computer's full processor line is visible in fresh Explorer 35:
  `offline/24-computer.png`, `online/15-computer.png`.
- Both post-reboot audits report no failed system/user units or current-boot
  coredumps, correct user configuration ownership, SDDM state permissions and
  restrictive ESP masks. Their SDDM journals confirm successful authentication
  into `/usr/share/wayland-sessions/aero7.desktop`.
- Programs Center was absent by default. On offline r3, Start found **Turn
  Aero7 features on or off**; install, real application launch, installed-app
  inventory, removal and reinstallation passed without adding networking.
  `optional-cycle-audit.log` records all three package transactions; screenshots
  `28-features-search.png` through `40-reinstall-auth.png` record the UI.
  The last filename is historical: it shows a completed reinstall, not an
  authentication error. Programs Center remained installed after reboot.
- Online r3 saved a real 601×401 PNG with region selection and a saved
  notification, without an editor process (`screenshot-audit.log`). Delayed
  notification clicks in `18-notification-viewer.png` and
  `48-notification-viewer.png` show only the desktop and are **not** counted as
  click-to-viewer passes. Earlier r2 viewer/paste coverage remains separate.
- Retesting with a prompt click on the notification image opened the saved
  601×401 PNG in the default viewer on r3 after reboot
  (`online/49-immediate-notification-click.png`). This confirms the earlier
  delayed clicks missed the notification; they were not a viewer failure.

### Newly confirmed blockers — do not announce an all-clear

1. Offline's full install log contains `vercmp: command not found` in the
   fontconfig install script. Pacman was scheduled after fontconfig by the
   alphabetical offline archive list. Installation completed and the font cache
   works, but the script skipped its initial configuration branch. The backend
   now schedules pacman first while preserving every archive and the relative
   order of the rest. All **71 installer tests pass**, including the new ordering
   regression. This source correction still requires a real transaction and
   rebuilt-image acceptance; it is **not embedded in r3**.
2. OOBE's update preference is written to `/etc/aero7/update-preference.conf`,
   but no consumer was found in the active installer/Desktop/Control Panel/
   Programs Center source. The screen promises automatic/security-only updates
   and has two help/privacy links without click handlers. Those promises are
   not validated behavior. An update-policy decision has been requested before
   implementing a new default; unattended upgrades are not being silently added.
3. OOBE accepts Home/Work/Public but finalization does not apply that choice.
   It enables the UFW systemd unit without activating the firewall rules.
   **Both r3 post-reboot audits report `Status: inactive`**, including after the
   Public network selection. This contradicts the setup description and needs
   correction and a real packet-policy test before a release claim.

The online full install log did not contain the offline fontconfig warning or
the searched configuration/command failure strings. Expected offline missing
repository database warnings and the expected online optional-package-absent
query are not installation failures. Neither fact cancels the blockers above.

No Git commits, pushes, signing, package promotion, ISO uploads or publication
were performed. All old QA disks, images and logs remain available.

## Firewall correction and real offline package-order verification

Follow-up source SHA-256 (`backend/aero7_install_backend.py`):
`381a29f1c0c375aacf3bf950574677234027161d3e16fbe7418efdfb1eb935f8`.
All **73 installer tests pass**, including activation ordering and propagation
of a failed UFW activation instead of allowing setup to continue silently.

### Firewall: source corrected, manual guest integration passed

OOBE now explicitly sets deny incoming, allow outgoing and deny routed policies,
activates UFW, and enables its boot unit after desktop setup. It does not reset
existing rules on a retry or automatically expose sharing services for Home.
This is the protective baseline, not a claim that Home/Work/Public profile
selection or automatic sharing configuration has been fully implemented.

The exact new helper was executed in the online r3 disposable guest, then
executed again and followed by a UFW service restart. Evidence:

- `online/firewall-preflight.log`: previously inactive firewall.
- `online/firewall-packets-before-retry.log`: IPv4 and IPv6 TCP connections
  accepted before activation, proving the local packet fixture works.
- `online/firewall-activation.log`: active UFW and persistent boot enablement.
- `online/firewall-packets-after.log`: fresh inbound TCP blocked for both address
  families; outbound connections and verified reply payloads succeeded. An
  external HTTPS request also returned HTTP 200.
- `online/firewall-retry-reload.log`: same packet results after applying the
  helper again and reloading the service.

`tests/firewall_packet_probe.py` creates a temporary namespace/veth pair only
inside a root-owned disposable QEMU guest and cleans up those fixtures. The
first attempted serial transport truncated the encoded probe; its base64 error
in `firewall-packets-before.log` is a QA transport failure, not a network result.
Chunked serial transfer fixed the transport before the successful baseline.
The source file later moved an import to module scope without changing behavior.

### Fontconfig: actual 739-archive offline transaction passed

The offline guest still had no NIC. Its ISO was mounted read-only; all **739**
base archives were independently checked against its SHA-256 manifest. The
current source's `pacstrap_arguments` function supplied the transaction order.
Pacstrap installed into a new, initially empty temporary root, not over the
installed desktop. `offline/font-order-full.log` records:

- pacman installed before fontconfig;
- `Creating fontconfig configuration...` ran successfully;
- no missing `vercmp` or arithmetic syntax error;
- `PACSTRAP_EXIT 0`, successful `vercmp`, and Noto Sans resolved by `fc-match`;
- the transient transaction unit completed with `Result=success` and exit 0.

Scope limits: this temporary root has no target partition/fstab or generated
locale. Its kernel hook consequently logged a root-filesystem detection error,
and Perl fell back to the C locale. These fixture diagnostics are preserved,
not represented as a clean bootable installation. This test proves the package
ordering/fontconfig correction, **not** a fresh final-ISO install or boot.
The previously recorded r3 full installation/reboot checks are separate.

Read-only media mounts were removed afterward; the temporary QA target and all
logs remain preserved under `/var/tmp/aero7-font-order-XpI42S` in the offline VM.

Neither source correction is embedded in the current r3 images. New builds and
fresh acceptance are still required. Update-policy selection remains awaiting
the release owner's choice; no unattended package upgrades were enabled. The
network-location selection and dead setup help/privacy links remain open work.

## Setup help links — source and rendered UI tests passed

The update-options help, setup privacy information and installation-type help
now open local modal dialogs. Their links support keyboard focus/Space; dialogs
close with Escape or the focused Close button, without advancing setup or
changing the chosen preference. The privacy copy describes the actual local
diagnostic collection and warns about identifiable data before sharing.
Update help explicitly reports the current missing automatic-update behavior;
it does not implement or select an unattended-update policy.

New `test-installer-help` exercises all three links at 1024×768 and 1920×1080.
All six data rows passed, plus init/cleanup (8 QtTest results). Rendered captures
under `/home/admin/VMs/aero7-beta2-release-check-Mnoerz/setup-help/` were inspected
for unclipped text. These are explicitly labeled host simulation captures,
**not VM/fresh-ISO acceptance screenshots**. An initial QML duplicate-font
assignment failure was corrected before the passing run; no broken help build
was deployed to a VM.

All three installer CTest groups pass (`flowstate`, `installercontroller`,
`installer-help`); all 73 Python backend tests pass; `git diff --check` is clean.
Built installer SHA-256:
`e2071df5a758b3052f7182cb2cba058c4a6cd5aea020ccea22ba424c50a49226`.
The r4 offline profile is now being prepared. Update-policy selection and the
unfinished network-location behavior remain open; publication remains on hold.

## r4 offline media built and verified — 6 September follow-up

The offline r4 build completed with exit 0. The same-named r3 image was retained
in `out/superseded-offline-6XDT1w/`; it was not destroyed. r4 identity:

- Filename: `aero7-beta2-offline-2026.09.05-x86_64.iso` (profile prepared 5 September).
- Exact size: **3314876416 bytes**.
- SHA-256: `e414e4d4e98c07763be7368283a77f0a11087858c48e5461954e798925cae507`.

The release verifier now compares the embedded installer frontend byte-for-byte
with the current compiled candidate, in addition to backend/adapter source and
package-manifest checks. Older marker strings alone cannot establish that a QML
fix was embedded. r4 passed this stronger check as well as offline archive hashes
and dependency closure (`verify-offline-r4-exact-frontend.log`).

Fresh r4 QA root: `/home/admin/VMs/aero7-beta2-r4-Nlm227/`.
Its offline VM is starting with `-nic none`; fresh installation acceptance is
pending. The online r4 profile has passed preparation checks and its image build
is running (`prepare-online-r4.log`, `build-online-r4.log`). Original r3 guests
were shut down normally to free build memory; all their disks and logs remain.

The online r4 build and exact-frontend/backend/package verification also passed:

- Filename: `aero7-beta2-online-2026.09.06-x86_64.iso`.
- Exact size: **1458139136 bytes**.
- SHA-256: `81ceb52824608c76cdf5c02fd1915e6088ab5561aad20cbcc378f0c8c5c76a74`.

Both new VMs are under the r4 QA root above, each with a new 64 GiB virtual disk.
Offline has entered actual installation after its `/dev/vda` confirmation;
`offline/04-install-help.png` also proves the repaired help dialog works from
the real media. Online is booting. Full installed-system acceptance for both
r4 images remains pending; these identities are not approved release downloads.

## r4 fresh installation and first-login checks — 6 September

Both exact r4 images above completed installation to their new 64 GiB disks,
rebooted into OOBE, created the QA account and reached the Aero7 desktop. Offline
remained `-nic none`; its installed interface inventory contains only loopback.
No runtime source or package was patched into either installed r4 guest.

Evidence is under `/home/admin/VMs/aero7-beta2-r4-Nlm227/`, per variant:

- `installer-full.log` and `oobe-full.log`: complete serial-read log captures,
  each with the acceptance completion delimiter.
- Online `installed-audit.log`, offline `installed-audit-retry.log`: expected
  component versions, optional Programs Center absent, correct user config and
  SDDM state ownership, protected ESP mount, no failed system/user units and no
  current-boot coredumps.
- `firewall-packets.log`: fresh OOBE enabled UFW without manual activation.
  Isolated IPv4 and IPv6 probes both blocked unsolicited incoming TCP and
  allowed outgoing TCP with verified reply payload. Temporary namespace/veth
  fixtures were removed. Online also received HTTP 200 from the Arch mirror
  over HTTPS. The offline probe did not attach a network adapter or internet.
- Offline `installer-full.log`: pacman is installed before fontconfig, followed
  by `Creating fontconfig configuration...`; no missing-vercmp/arithmetic
  failure. `font-and-diagnostics.log` confirms working vercmp, Noto Sans font
  resolution, generated en_US locale and the desktop diagnostic folder.
- Offline `13-update-help.png`, `14-privacy.png`: real installed OOBE dialogs
  open with readable, unclipped content and close using Escape.
- Offline `23-explorer-pin.png`, `24-computer.png`: factory taskbar pin opens
  File Explorer; Computer has the full processor details line and filtered
  Local Disk/CD Drive presentation.
- Offline `25-screenshot-saved.png`, `26-screenshot-viewer.png`,
  `29-paste-pixels.png`: Meta+Shift+S saves a 601×401 PNG without the Spectacle
  editor; notification click opens it in Gwenview; Ctrl+V pastes the actual
  601×401 image into KolourPaint.

Warnings are retained, not characterized as a completely clean log: package
hooks temporarily use the default console and Perl C locale before installed
locale setup; the final locale is generated. Offline repository-database
warnings are expected without a sync; QA unsigned-package origin and the
pre-existing Plymouth hold warning remain recorded. KolourPaint's first launch
was delayed and emitted existing theme SVG-reference warnings; it ultimately
opened and accepted the image, with no coredump. This is not a startup-performance
pass. Earlier `27-image-pasted.png` captured Ctrl+V reaching Gwenview before
KolourPaint was ready, not a KolourPaint paste pass.

QA transport caveat: offline `installed-audit.log` is empty because first-login
autostart switched away from the TTY while the helper was being typed. The
partial command was cancelled, the console was explicitly verified in
`22-console-ready.png`, and `installed-audit-retry.log` is the valid result.
No product failure is inferred from that harness race.

Normal r4 reboots and second-login checks are now underway. Update-policy
selection still has no scheduler, and the promised network-location sharing
behavior remains unfinished. These images are still not release-approved.

### r4 normal reboot, password login and lock/unlock passed

Both VMs subsequently completed a normal `systemctl reboot`, showed SDDM and
accepted the QA password for the Aero7 Desktop session. Per-guest
`reboot-audit.log` confirms UFW remains active and boot-enabled, no failed
system/user units, no current-boot coredumps and preserved ownership/ESP
permissions. The offline guest still has only loopback. Packet tests above
were before reboot; post-reboot persistence was checked through UFW/service
state, not a second packet-probe run.

Both Meta+L lock screens displayed the complete Aero7 Professional branding
and accepted the password to return to the desktop. Screenshots:

- Offline: `30-reboot-login.png`, `35-lockscreen.png`, `36-unlocked.png`.
- Online: `24-reboot-login.png`, `25-second-desktop.png`, `28-lockscreen.png`,
  `29-unlocked.png`.

The early offline `31-second-desktop.png` and `32-reboot-tty.png` captured the
desktop during startup before icons finished appearing, not final presentation.
The later unlocked capture shows the expected Recycle Bin plus requested test
log folder. No arbitrary extra startup shortcuts were observed.

This clears the r4 install/OOBE/reboot/login/lock checks, not every release gate.
The previous r2/r3 broader component matrix is retained with its original
scope; it must not be relabeled a complete r4/final-release regression run.
No commit, push, package signing/promotion, ISO upload or announcement occurred.

## Post-r4 source correction: package-hook locale — 6 September

The r4 package-hook Perl warning was traced to inheriting `LANG=en_US.UTF-8`
before the target's locale generation. `CommandRunner` now supplies a private
child-process environment with `LANG=C.UTF-8`, `LC_ALL=C.UTF-8` and `LANGUAGE=C`.
It retains unrelated environment variables and does not mutate the installer
UI's environment or replace the installed user's locale. Both the blocking and
heartbeat subprocess paths use this environment, also stabilizing translated
command output used for progress parsing.

All **77 backend/adapter unittest tests pass**. New tests cover both execution
paths, inherited invalid locales, preservation of unrelated variables and the
parent environment, and a real Perl hook without locale warnings.

The exact revised `CommandRunner` class was additionally executed in memory in
the offline r4 VM. A direct Perl invocation with an ungenerated inherited locale
reproduced the warning; the revised runner suppressed its cause and completed
the same Perl command successfully in both modes. Evidence:
`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/locale-runner-source-probe.log`.
Temporary probe logs were confined to an automatically cleaned QA directory;
no installed backend, package, locale configuration or ISO was replaced.

Revised backend SHA-256:
`5a0fbc459448cb4da8e9d81af72472c8c2772b4f629d831ac343c40f99b827da`.
**This source fix is not embedded in r4.** The source-to-image verifier must
therefore reject r4 as matching the newest backend. A rebuilt final candidate
and fresh acceptance are still required after the remaining fixes are grouped.

### Additional setup preference audit — open bugs

The English/default-US tests do not establish nondefault preference support:

| Setup choice | Source evidence | Current result |
| --- | --- | --- |
| Dutch installation language | `LanguageScreen.qml` offers Nederlands; `writeInstallPlan()` writes `language`; backend always generates/writes en_US.UTF-8 and never consumes that field | Not applied; no claim of Dutch setup support |
| Dutch keyboard | `writeInstallPlan()` writes `keyboard`; backend does not consume it or configure KEYMAP/LayoutList | Not applied; requires console, greeter and session validation |
| Regional time/currency format | `m_timeFormat` is exposed to the UI but absent from `writeInstallPlan()` | Lost before the backend; not applied |
| Home/Work/Public | OOBE validates the value but never applies it; Control Panel explicitly reports one global UFW rule set | Baseline protection works, location-dependent sharing does not |
| Update selection | Written to `/etc/aero7/update-preference.conf`, no scheduler consumer | Awaiting owner policy choice; no unattended upgrades enabled |

These are implementation gaps, not a proposal to remove the choices or replace
them with unsupported marketing promises. Nonfatal default-console warnings and
theme SVG-reference/startup-performance investigation also remain recorded.

## Post-r4 source correction: independent regional preferences — 6 September

The frontend now serializes `language`, `time_format` and `keyboard` separately.
The backend validates the offered values before disk discovery or destructive
work. Missing values in older plans retain English/US defaults; invalid explicit
values fail closed rather than entering system configuration.

Before package installation and initramfs hooks, setup now seeds:

- `/etc/locale.conf` with independent language and regional-format categories;
- `/etc/vconsole.conf` with the selected console keymap;
- `/etc/xdg/plasma-localerc` and `/etc/xdg/kxkbrc` with KDE defaults;
- `/etc/X11/xorg.conf.d/00-keyboard.conf` with the selected XKB layout;
- an OOBE service drop-in using the locale file and selected Cage keyboard layout.

Locale generation enables both selected locales as needed, preserving other
enabled entries and comments without duplicating entries on retries. The r4
guest's actual SDDM configuration uses `kwin_wayland --locale1`; the system
keyboard configuration is intended for that path too, but a fresh nondefault
SDDM login has not yet been tested.

Validation:

- **84 backend/adapter tests pass**, including all eight independent preference
  combinations, invalid-value rejection before disk/network work, idempotence,
  locale preservation and mocked online/offline install ordering before pacstrap.
- Installer rebuild succeeded; **all three CTest groups pass**, including the
  controller regression for preserving independent setup preferences.
- The exact candidate helper functions were extracted and executed in memory
  in the offline r4 guest with a temporary target, not installed over its backend.
  `kreadconfig6` read the selected Dutch defaults through isolated XDG config
  directories; both US and Dutch XKB maps compiled and console maps were present.
  `localedef` generated Dutch locale data in the temporary directory; `locale`
  reported comma decimal formatting and `date` reported `maandag` for Monday.
  The temporary target was removed automatically. Installed preferences and
  package/service configuration were unchanged.

Probe source: `tests/regional_preferences_probe.py`. Host evidence:
`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/regional-source-probe.log`.

Candidate backend SHA-256:
`26004b7823c65968937a4cda8b0e9f51b38a6dec068ad144d3d17d8273d74e57`.
Rebuilt frontend SHA-256:
`cda9a78579157728a5aa059b5f99f81d04c64c9a1221f4bfc9ac3e287f830787`.

**Not in the r4 media.** Fresh nondefault installation, first-run keyboard entry,
reboot/login and session persistence remain pending. Custom Aero7 UI translation
and live-installer keyboard switching are not established by locale support.
The update scheduler and network-location behavior remain separate open issues.
No commit, push, signing, promotion, upload or publication was performed.

## Post-r4 theme/package cleanup and Paint close failure — 6 September

The existing Windows7Aero Kvantum SVG contained exactly two unresolved local
references: the lower slider corners referred to removed top-corner IDs. The
references now target the existing top-corner artwork. A Qt SVG regression checks
all local references and renders both lower corners; it rejects the original
file and passes the corrected one. All **14 theme CTest tests pass**.

Local unsigned candidate changes:

| Package | Candidate version | SHA-256 |
| --- | --- | --- |
| aerothemeplasma-desktop-git | 6.7.0_742.r9c2d850-41 | `03c264c9305ba76a092e21c94928e6336c521819014cc92b2d238bff9449a576` |
| aerothemeplasma-icons-git | 11.r96950b8-3 | `54321ad3e691ea0c8185d86452b9a1f1530f7db34e7477d68146cdfda5314294` |
| aerothemeplasma-sounds-git | 4.r55d2f5f-3 | `4daa78d8ae8f903a1f6419971245174e8aa96d5f5882d4ce49f68da97592d8bc` |

The icon metadata correction already existed in the package recipe but was not
selected by the ISO. The refreshed recipe also excludes the source `.git`
directory. The same packaging defect was found and fixed in the sound recipe.
Archive comparison confirms the same 8,159 non-Git icon file/link paths, with
only `Windows 7 Aero/index.theme` changed; every icon image remains identical.
All 887 non-Git sound file/link entries are identical. Each old package contained
44 Git metadata entries; neither refreshed package contains any.

The local package set now selects these versions for both variants. The offline
custom repository and manifest also replace the old icon/sound versions; old
archives remain in the developer cache, outside the selected image manifest.
The original repository database was preserved under
`work/beta2-icons-refresh.tuy1hM/repository-before/` before replacement.
New offline repository SHA-256:
`56d363ae3ff482e1e2a3947a33e73fe5ba89e26b57c716896fe4b396368a8c04`.

`scripts/verify-candidate-packages.py` is now called by ISO preparation and release
verification. It streams selected archives without extracting them, rejects VCS
metadata and unsafe member names, checks package hashes/identities, and verifies
the offline repository against its package manifest. It passes for the 11 local
online candidates and all 46 local/offline custom dependency archive paths;
all 35 offline repository entries agree. Five new regressions bring the complete
backend/adapter/artifact unittest suite to **89 passing tests**.

Offline VM runtime probe: `tests/paint_theme_runtime_probe.py` uses temporary XDG
directories and the exact original/corrected SVG hashes. It does not overwrite
installed packages or settings. Successful evidence:
`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/paint-theme-runtime-probe-journal.log`.
Baseline: 65 targeted warnings, first toplevel configure at 4.357 seconds.
Corrected: zero targeted warnings, first configure at 4.391 seconds. These are
single instrumented warm starts, not a performance improvement or first-paint
benchmark. The earlier two probe attempts only captured stderr and therefore
missed KDE's direct journald warnings; they are not accepted comparison results.

### Newly confirmed blocker: Paint crashes on normal close

Clicking Close on the unchanged blank Paint window in r4 produced SIGSEGV in
`QWidgetPrivate::inheritStyle`, through `QWidgetAction::releaseWidget`,
`SAColorMenu` and `SARibbonColorToolButton` destruction. This was the installed
original theme/package, not a patched candidate. Core evidence is retained:
`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/paint-close-coredump.log`, PID 8024,
6 September 00:53:47 CEST. The earlier r4 clean-core audits remain historical;
the VM now has this confirmed application core. No failed system/user units
remain after collected QA services exit, but that does not cancel the crash.

Investigation is checking ribbon-owned style lifetime during child-menu cleanup.
The SIGTERM-ended temporary theme probes do not test normal close and must not
be used to clear this blocker. Normal close, save/discard and repeat-launch
acceptance are required after a reproduced source fix. No new ISO, package
promotion, signing, commit, push, upload or publication has occurred.

### Paint style-lifetime fix: reproduced and VM-probed, packaging pending

The pinned SARibbon commit `540624e98a53cff47fc1b0531d9129ae3a7fe6b2` owns each
button's proxy style through `d_ptr`. The empty button destructor lets that style
die before QWidget deletes child menus. A menu's QWidgetAction can reparent its
default widget while being destroyed and consult the now-invalid style.

A focused QApplication/ribbon-color-button test with an application stylesheet
reproduced SIGSEGV through `QWidgetPrivate::inheritStyle` and
`QWidgetAction::releaseWidget` using the unmodified library. Detaching the private
style with `setStyle(nullptr)` while it is still alive removes the dangling
reference. The same test then completes **20 create/delete cycles**, including
under GDB, with a normal process exit. Evidence is in:
`work/beta2-paint-close.echG0Z/baseline-close-gdb.log` and
`work/beta2-paint-close.echG0Z/fixed-close-gdb.log`.

The package recipe under `aero7-desktop-workcopies/aero7-repo/packages/aero7-kolourpaint`
now has a proposed release 3, a checksum-pinned lifetime patch, and this regression
in `check()`. The pinned upstream file uses CRLF, so prepare normalizes that one
translation unit before applying the patch. Reverse dry-run application passed.
The complete Paint package has **not yet been rebuilt or selected in the ISO
manifest**; the current installed and selected application remains release 2.

For an offline VM check, the rebuilt library and test binary were delivered on
a temporary read-only QA CD, without adding a network adapter. The regression
returned 0 inside the VM. `/proc/<pid>/maps` confirmed actual Paint loaded the
candidate library from `/run/aero7-paint-qa`, SHA-256
`d72e0739b1e7ae71deaa0b7098a866054c19b2e3d6dd833e140b7f38abfd2834`.

Three actual launches were exercised with that library:

- unchanged blank window closed normally;
- drawing a line showed the modified-document prompt; Cancel kept it open,
  then Discard closed it without another core;
- a further blank-window close was observed through a waiting user service,
  which reported **exit status 0/SUCCESS**.

VM evidence: `paint-close-fixed-launch.log`, `paint-close-fixed-first-result.log`,
`paint-close-fixed-discard-and-third.log` and `paint-close-fixed-cleanup.log` in
`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/`. Screenshots 42 and 47 show the
actual application; 45 shows the modified-document prompt. Earlier immediate
captures 44/46 may include transition frames and are not standalone proof of
dialog completion.

The QA mount was unmounted and removed after all probe applications exited,
and QMP restored the original r4 offline ISO to the CD drive. The installed
library and theme hashes remain unchanged; networking still consists only of
loopback. No new core appeared during the corrected-library checks; the earlier
PID 8024 core is retained. The old theme warnings remain in these runs because
only the ribbon library was substituted here, not the separately tested theme.

Remaining: build/check the full Paint package, update both candidate dependency
sets and offline metadata, test save/reopen and menu interactions, then validate
the packaged fix on the rebuilt images. This clears the reproduced lifetime
cause in source and a manual VM probe, **not** the final Paint/ISO release gate.

## Full Paint package and upgrade-safe branding — 6 September follow-up

The host administrator approved installation of the declared handbook build
dependency (`kdoctools 6.29.0-1`, with DocBook dependencies). The existing prepared
Paint build resumed with `--noextract`; no documentation option was disabled.
`BUILD_DOC=ON`, the full build, recipe `check()` and package creation succeeded.
All declared build/runtime dependencies were present according to `pacman -T`.
The focused recipe check runs 20 stylesheet/color-menu destruction cycles.
Optional KSane scanner integration was not built; no hardware scanning claim is
made. Nonfatal upstream compiler/translated-handbook warnings remain in the log.

Build evidence: `work/beta2-paint-package.jlCu8M/resumed-build.log`.
Package `aero7-kolourpaint-25.12.3-3-x86_64.pkg.tar.zst` is 6,614,791 bytes,
SHA-256 `288add74a5b58b7cce36933e936159f294fcc1f23aae85a14b5efaa115aa21b5`.
The English handbook source and compiled cache are present in the archive and
installed guest. The installed ribbon library has SHA-256
`2735b83d30ed241a3efbd685bf1ea41295d529df6e197522c5d70e1f07b7adae`.

Both online/local and offline dependency selections now select Paint `-3`.
The offline database was updated through a staged `repo-add`, with the previous
database/files preserved under `work/beta2-paint-full-qa.ylYOPA/repository-before`.
Its new SHA-256 is
`8f216ce7297e0c76ef445c09a7fd306eb674f2598a79ef847869713914719531`.
The selected set contains 12 online/local archives, 47 offline/local/custom
archive paths and 35 offline repository entries. Package hygiene and repository
identity/checksum checks pass; the complete Python suite still passes 89 tests.

### Installed-package Paint tests

This is the existing r4 offline guest, **manually upgraded**, not a new install.
Packages were transferred on a read-only QA CD while the VM retained only its
loopback interface. The first CD mount raced media detection and failed without
installing anything; an explicit ISO9660 mount after settling succeeded. The
package transaction returned 0, with no dependency bypass or forced overwrite.
It installed Paint `-3`, theme `-41`, icons `-3` and sounds `-3`.

The real Paint UI passed:

- Draw a line and save through the PNG file dialog.
- Close the saved document and reopen it in a new Paint process; the line is
  visibly retained, with a clean, unmodified title.
- Draw a second line, close, then Cancel: the application and edit remain open.
- Close again and Discard: the application exits and the saved PNG is unchanged.
- Launch a third blank window and close normally: `0/SUCCESS`, with explicit
  `FINAL_PAINT_EXIT=0` in the complete serial transcript.

The fixture `/home/aero7test/Pictures/beta2-paint-package-qa.png` is an actual
400×300 PNG with two colors, SHA-256
`62dbf87efd2d2b32c1eba01b07ce28c85c9a0b633aa42fa6cde3d286407ea397`.
That hash is unchanged after Cancel and Discard. No coredumps were recorded
since 01:38 CEST; the earlier 00:53 PID 8024 core is deliberately preserved.

Guest evidence is under `/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/`:
`paint-full-package-install-retry.log`, `paint-full-package-launch.log`,
`paint-full-package-save-result.log`, `paint-full-package-reopen.log`,
`paint-full-package-cancel-result.log`, `paint-full-package-discard-result.log`,
`paint-full-package-final-close.log` and `paint-full-package-cleanup.log`.
Screenshots `50-paint-full-package.png` through `56-paint-final-blank.png`
record the tested GUI states at 1920×1080.

### Branding regression discovered during the upgrade

Theme `-41` restored the upstream authui7 splash/logout bitmap and QML references
that the installer had rewritten. This reintroduced clipped Aero7 lettering in
the logout UI (`58-theme41-logout.png`). The correction must be package-owned,
not merely an installer-time mutation.

The first attempted correction, local theme `-42`, failed safely with a file
conflict against the older installer's unowned `aero7-watermark.png`. It is not
selected in the candidate manifests. Theme `-43` instead owns the distinct
`aero7-package-branding.png`, updates both QML references and metadata, and omits
the unused upstream bitmap/previews from the generated package. The established
branding bitmap is copied unchanged; no new artwork was created. The older
installer-generated file is left untouched.

Theme `aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-43-x86_64.pkg.tar.zst`
has SHA-256 `9995cc3fdfcc6ec1f2ef4e88f896658f220366a54fe3bbba966547c8c001de4b`.
It is selected for both candidate variants. This local package was repackaged
from the existing prepared build; all 14 theme CTests pass. Package-time checks
verify the branding image bytes and both QML references. A clean signed builder
remains a separate requirement.

The real offline upgrade from `-41` to `-43` returned 0 without forced overwrites.
`pacman -Qo` confirmed ownership of the new file and `pacman -Qk` reported
1,143 files, zero missing. Both installed QML references and image SHA-256
`d45164d6d67f2d8ccae63c4fd83bd0dd73e05808f3c8cd739c4850b5680d4982` match.
`59-theme43-logout.png` and `60-theme43-lock.png` show complete, unclipped
branding. See `theme42-package-install.log` for the negative migration test
and `theme43-package-install.log` for the successful package transaction.

One existing Command Prompt pin displayed a blank icon after the in-session
icon-pack replacement, despite valid unchanged `bash.png` artwork and launcher
configuration. Restarting the test guest's Plasma shell restored it, verified
in `57-after-icon-refresh.png`. Automatic live icon refresh is **not** established;
the package-update guidance recommends signing out and back in. No forced shell
restart was added to package hooks.

All QA CD mounts were removed and the original r4 offline boot ISO restored,
with its exact path verified through QMP. Installed QA packages remain in this
guest. Final fresh-image install/reboot/application tests, broader menu actions,
scanner/hardware behavior, update/network-location implementation and release
signing/promotion remain pending. Nothing in this follow-up was published.

## Screenshot workflow and capture-process failure follow-up — 6 September

This pass used the existing disconnected r4 offline guest at 1920×1080, first
with theme `-43`, then manually upgraded to `-44`. It is not fresh-image
acceptance. Paint was the complete `25.12.3-3` package; Spectacle was
`1:6.7.4-1`. The VM retained only its loopback interface.

### Defect and correction

The Snipping Tool previously classified missing or empty output as cancellation
before examining the capture process status. A failing `/bin/false` test backend
therefore produced no failure notification. `CaptureResult.h` now checks crash
and nonzero status first; empty output is also a failure, and only a clean exit
with no output is classified as cancellation. The existing PNG decoder still
checks nonempty output before copying it to the clipboard.

The regression executable covers eight outcome combinations plus a real
`/bin/false` process. All 15 theme CTests pass. An initial build invocation
regenerated its Makefile but did not see the newly added test target; rebuilding
that target and rerunning CTest succeeded. The earlier Not Run is not a passing
test result. Logs are in `work/beta2-package-refresh.TT06FA/theme/`:
`snipping-result-build.log`, `snipping-result-test-build.log`,
`snipping-result-tests.log` and `snipping44-package-build.log`.

The canonical theme recipe selects `aero7-snipping-capture-result.patch`, SHA-256
`cb8668171f61fd6cf7a00089ee6a2c6289250b8ea18024eff46bafcd8936dfe4`.
Local package
`aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-44-x86_64.pkg.tar.zst`
has SHA-256
`ca48cc2041e4ef8b087ab15c1cddfdedaba54888ebfea2620ccce8be032ed295`.
It retains the package-owned branding correction from `-43` and is selected by
the shared local manifest. The guest transaction returned `THEME44_INSTALL_EXIT=0`.
This was repackaged from the prepared compiled tree, not a clean signed release
build. No package was promoted or published.

### Real desktop results

Evidence is under `/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/`:

- `72-snipping-failure-before-unlocked.png`: controlled failure before the fix,
  with no error notification. The earlier image 71 was locked and is not valid
  unlocked notification evidence.
- `73-snipping-failure-after.png`: the same failing backend after the upgrade
  displays the Snipping Tool error and Try Again action.
  `snipping-failure-after-result.log` records the corresponding diagnostic.
- `74-snipping44-before-cancel.png` and `75-snipping44-cancel.png`: Escape closes
  the ready selector with no error and no new PNG. The following process/file
  audit found only the normal Snipping daemon and the four pre-existing PNGs.
- `78-snipping44-selector-unlocked.png`: Meta+Shift+S enters rectangular
  selection. Attempt 77 occurred after idle locking and is not selector evidence.
- `79-snipping44-saved.png`: releasing a 401×301 selection closes the overlay,
  saves the PNG and displays the saved notification, with no Spectacle editor.
- `80-snipping44-viewer.png`: clicking that notification opens the exact newly
  saved file in Gwenview. `snipping44-normal-result.log` confirms its process
  argument is `Screenshot 2026-09-06 02.15.37.557-f12c01.png`, not the older image.
- `81-snipping44-pasted.png`: Ctrl+V inserts actual 401×301 image data into Paint.
  The unsaved QA paste was subsequently discarded through the normal close
  prompt (image 82); source screenshot PNGs were preserved.

Earlier `-43` images 64 and 70 independently show actual Paint image paste and
notification-open behavior. Early Escape attempt 65 preceded a ready selector;
the delayed notification click in image 68 missed its expiry. Neither is counted
as a pass; their correctly synchronized repeats are recorded separately.

`snipping44-normal-result.log` and `snipping44-cleanup.log` have complete serial
completion markers. No new coredumps occurred since 01:56 CEST, including the
normal Paint close after the paste test. The historical Paint core remains.
No failed system/user services remained. The temporary failing-backend services
were stopped; no matching QA units remained. Normal Snipping autostart was
restored, the user manager reloaded, and its process had no test-backend override.
The QA mount was unmounted and removed. The original r4 offline ISO was restored
and its exact path confirmed through QMP `query-block`. An initial media-change
call used `id` instead of `device` and failed without changing media; the corrected
call succeeded. Both VMs and all QA files remain available.

### Remaining backend limitation and release boundary

The zero-exit/no-file case is not unambiguous. In pinned Spectacle 6.7.4,
background screenshot failures can emit `allDone`, while cancellation also emits
`allDone`; the new-instance entry point connects it to normal application quit.
The background error path logs a warning rather than opening its error dialog.
Thus some internal errors can still be mistaken for cancellation by the wrapper.
This is a source-derived limitation, not a newly reproduced compositor failure.
See upstream [SpectacleCore.cpp](https://raw.githubusercontent.com/KDE/spectacle/v6.7.4/src/SpectacleCore.cpp)
and [Main.cpp](https://raw.githubusercontent.com/KDE/spectacle/v6.7.4/src/Main.cpp).
Do not claim comprehensive error handling from the nonzero-exit fault injection.
Matching arbitrary stderr is not used: normal capture/cancellation also produced
nonfatal Qt focusPolicy warnings in the guest journal.

Final reruns passed 89 Python tests, 15 theme CTests, 12 online candidate archive
checks, 47 offline candidate/custom archive checks and all 35 offline repository
identity/checksum checks. The website-maker handoff, local release notes and local
wiki draft now describe theme `-44`, the verified workflow and this open limitation.
They have not been pushed. Neither r4 ISO embeds this package; final rebuilt
online/offline install-to-desktop acceptance remains required.

Update-scheduler behavior and connection-specific Home/Work/Public firewall
behavior remain unresolved. No unattended updates were enabled and no firewall
backend or existing UFW rules were migrated in this pass. Owner policy confirmation,
implementation, final-media regression, signing and publication are still pending.

## Spectacle capture status and failed-save recovery — 6 September

This checkpoint supersedes the backend limitation immediately above for the
tested error paths. It does not supersede the final-media release gate.

### Reproduction and correction

The signed KDE Spectacle 6.7.4 release archive was verified using an isolated
keyring and pinned primary fingerprint
`0AAC775BB6437A8D9AF7A3ACFE0784117FBCE11D`. Its SHA-256 is
`5c61ffd9b37ca6384b754d44a051c8f979ab77984f92e7ddf3a1c15156d65665`.
The actual release tarball, not the previously inspected cached GitHub source,
was used for the build. Existing KDE artwork, desktop identity, translations,
handbook and capture authorization are retained.

Two distinct failures were reproduced in the disconnected r4 test VM:

- Copies of the original and patched executable run from untrusted QA paths
  received the same real KWin capture-authorization denial. The original exited
  **0**, the patched executable **1**; neither created an image. KWin permissions
  were not weakened. See `spectacle-authorization-comparison.log`.
- Original installed Spectacle could not write a background screenshot to an
  unwritable `/proc` path and remained running until the 10-second test deadline
  terminated it. The failure status of that test service was a timeout, **not**
  a nonzero exit from Spectacle itself. See `spectacle-save-error-before.log`.

The downstream patch records a sticky failure status, ends failed background
exports, and returns that status through queued completion in both normal and
`--new-instance` paths. Escape retains success/no-file semantics; GUI and D-Bus
error dialogs are unchanged. No localized warning-string matching is used.

The complete package `spectacle-1:6.7.4-2-x86_64.pkg.tar.zst` is 2,477,322 bytes,
SHA-256 `d452b15edf563b55eed1bc4d9975a448ce09577797fe3e2a7719a1f49c859cb4`.
Both upstream CTests passed during its clean package build. It installed using
normal `pacman -U`, without dependency bypass or forced overwrite. Package
verification reported 308 files and zero missing. This is a local unsigned QA
package and an unpublished packaging patch, not a newly published GitHub fork.

### Real installed-package checks

Evidence is retained under `/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/`:

| Check | Observed result | Evidence |
| --- | --- | --- |
| New-instance PNG save | 1920×1080 image, exit 0, 0.976 seconds | `spectacle-installed-probe-ready.log` |
| New-instance failed save | Exit 1, 0.533 seconds, no timeout | Same log |
| Unique-instance PNG save | 1920×1080 image, exit 0, 0.637 seconds | Same log |
| Unique-instance failed save | Exit 1, 0.515 seconds, no timeout | Same log |
| Actual failed-save notification | Visible failure with Try Again | `96-save-failed-before-atomic-click.png` and retry log |
| Retry and next capture | Selection reopens, PNG saves, notification opens that file in Gwenview | Images 97–99 and `spectacle-retry-verified.log` |
| Escape from ready region selector | Process exits 0, no PNG, no timeout | Images 100–101 and `spectacle-cancel-exit-status.log` |

The saved retry image is `Screenshot 2026-09-06 12.18.53.244-e58b85.png`,
401×301 pixels, 115,459 bytes. Its exact path appears in Gwenview's arguments.
The opt-in `tests/spectacle_fail_once.py` fixture redirected only the first
capture to an unwritable output, then delegated unchanged to installed Spectacle.
It is QA-only and is not included in the desktop payload. The background probe
requires a preceding successful capture before counting each failed-save test,
so authorization failure cannot masquerade as an unwritable-output pass.

Early CD filename/mount timing errors, serial-console login harness errors,
untrusted-path capture attempts and the expired first retry click are preserved
in the logs but are not counted as passing product tests. The successful installed
probe, retry and cancellation logs include complete serial completion markers.
Upstream Qt/Mesa warnings remain; these results are not warning-free acceptance.
Image paste was demonstrated with theme `-44` before this backend upgrade and
is not represented as a new clipboard regression pass for this exact package.

### Candidate integration and boundary

The required local-package manifest now selects the patched Spectacle for both
ISO variants. The installer installs it in the required local transaction after
base packages; it does not rely on the older Spectacle in the offline base cache.
The recipe registry now contains 24 recipes, including source URL, archive digest
and signing-fingerprint validation. Seven signed-archive regression checks and
the publication-gate check pass. These checks validate metadata, not a package's
release signature. All 89 installer/backend tests and the ISO static gate pass;
the static gate still reports existing QML warnings. Archive checks pass for 13
online and 48 offline candidate/custom archives, and all 35 offline repository
entries match identities/checksums.

Normal Snipping autostart was restored with no test-backend override. No failed
system or user units remained; the only recorded core was the historical Paint
crash, not a new crash in these tests. Permanent serial getty remained disabled
and inactive. The QA CD mount was unmounted and its empty mountpoint removed.
The original r4 offline ISO was restored and its exact path verified through
QMP. The first change was rejected because the unmounted optical drive remained
locked; forced media replacement then succeeded without touching the VM disk.
The temporary interactive root console ignored the initial termination signal
and was killed at its service stop deadline. Only this QA unit's failed state was
reset; its journal is preserved. Image `107-console-final-state.png` shows
`ActiveState=inactive`, `SubState=dead`, `MainPID=0`; the permanent serial getty
remains disabled. No root console is being left active. After the host restart
only the offline VM was restarted;
the online VM is not being reported as running.

The website-maker handoff, release notes and local wiki draft now describe this
correction. No commits, pushes, signatures, promotion or uploads were performed.
Neither existing r4 ISO embeds these latest packages. Updated setup policies,
final rebuilt online/offline fresh installs, reboot/login, regional and recovery
checks, signing and explicit publication approval remain outstanding.

The final repository source verification also passed: all 24 `.SRCINFO` files
match their recipes, ShellCheck and the isolated temporary-directory pruning
test pass, and publication gates remain intact. The build filesystem has about
14 GiB free at this checkpoint; capacity must be checked before staging two new
images and fresh-install disks. Existing images, VM disks and evidence were
preserved rather than deleted to make room.

## Exact-package clipboard regression and build-capacity guard — 6 September

The normal Snipping autostart, without a QA backend override, was exercised again
on the disconnected r4 VM with installed Spectacle `1:6.7.4-2` and theme `-44`.
Image 111 shows the ready rectangular selector after Meta+Shift+S. The selected
top-left desktop region saved as
`Pictures/Screenshots/Screenshot 2026-09-06 12.39.47.348-0d7d72.png`.
Image `112-patched-clipboard-saved.png` shows the closed selector and saved
notification; `113-patched-clipboard-pasted.png` shows actual desktop image pixels
and the 301×251 selection dimensions in Paint immediately after Ctrl+V. No file
was opened manually in Paint. This closes the earlier exact-package clipboard
coverage gap, but remains an upgraded-VM result rather than final-media acceptance.

The unsaved QA paste was discarded through Paint's normal prompt (image 115).
`116-patched-clipboard-verified.png` confirms the installed Spectacle version,
the saved filename, no remaining Spectacle process and no coredumps since 12:39.
The original saved PNG was preserved. No root console was restarted for this
test; inspection used the ordinary graphical user's terminal.

The image builder had no disk-capacity preflight before removing temporary
staging and running Archiso. A new read-only helper now checks unprivileged
available space before the first build-tree removal. It accounts separately for
work/output filesystems and fails closed on unreadable paths. Twelve tests cover
capacity boundaries, same/different filesystems, reserved blocks, symlinks,
missing paths and guard ordering. The complete ISO static gate and all **101**
Python tests pass; existing QML warnings are not hidden.

The real helper returned failure with 13.3 GiB available against a conservative
16.1 GiB floor for the currently prepared small profile. It made no filesystem
changes. The full offline selected archives total 1,992,663,270 bytes (1.86 GiB),
so the larger offline profile requires a higher floor; the 16.1 GiB figure must
not be used as its capacity claim. See `docs/architecture.md` for the estimate,
and `work/beta2-spectacle-status.5SyqaU/build-space-preflight.log` for the refusal.
These are build-host requirements, not end-user installation disk requirements.

The updated handoff and local wiki draft include this clipboard result. Final
image builds remain pending capacity and the requested update/firewall policy
decisions; nothing has been committed, pushed, signed or published.
