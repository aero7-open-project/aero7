# r9 corrected time/setup media — acceptance in progress

Not release approval. No commits, signing, promotion, uploads or publication.

Later modified-guest Paint r5/r6 testing is recorded separately in
[Paint startup and swatch regressions](2026-09-06-paint-startup-layout.md).
The local manifest selects r6; both immutable r9 images still contain r3.

## Inputs and required checks

This pass combines the installer disk-label and selected-timezone preview fixes,
fresh-install time-service startup, and Control Panel 0.1.0-49 Internet Time
validation/operation fixes. r8 proved earlier installation paths but did not
contain these corrections. Both r9 variants need exact-content verification,
fresh install with their intended network conditions, OOBE, reboot/login,
logs/package/firewall checks and the remaining application/failure matrix.

Prepared profiles and build logs will be under
`work/beta2-time-final.BzUOt4`. Exact artifacts are recorded below; full
acceptance remains pending. Never substitute modified-guest evidence.

## Completed artifacts and current fresh-VM evidence

Both builds/export operations finished successfully (`R9_BUILDER_EXIT=0`).
Both exact images passed `verify-release.sh` before later source edits.
Export directory: `work/beta2-profiles.UWsuLM/builder-output/r9-time-final/`.

| Variant | Filename | Bytes | SHA-256 |
|---|---|---:|---|
| Offline | `aero7-beta2-offline-2026.09.06-x86_64.iso` | 3318038528 | `164d812fff812ab680ec56575945d4d1c29e9b312c18eafec23ca1aec5451e30` |
| Online | `aero7-beta2-online-2026.09.06-x86_64.iso` | 1547726848 | `4600502f34605155f221a25059d6d60734f809d188b407d3871b0040cc0712c0` |

These are QA identities, not approved download hashes. Verification logs:
`work/beta2-time-final.BzUOt4/verify-offline-r9.log` and
`verify-online-r9.log`. The completed builder was shut down normally after the
build service became inactive, freeing memory for both installed guests.

Both fresh 1920×1080 guests completed GUI installation and first-run setup and
reached the desktop without package/service repairs. Fixtures and evidence:
`/home/admin/VMs/aero7-beta2-r9-xTfYQR/{offline,online}/`.
The offline guest has no network adapter; its choices were Dutch regional format,
US keyboard and automatic update checks off. The online guest uses NAT, US
regional format, automatic checks on and connected Home profile. Both selected
Amsterdam. Both target-disk screenshots show Disk 0 and `/dev/vda`, 64 GiB.

Offline initial and post-reboot package/system/firewall audits passed, including
real IPv4/IPv6 Public-zone packet filtering, no failed system units and no
current-boot coredump records. Time synchronization was enabled and active
without repair, correctly unsynchronized without a NIC. Its ordinary Start-menu
restart returned to SDDM and password login succeeded. The login logo was fully
visible. Logs: `offline/results/installed-audit.log`, `post-reboot-audit.log`,
`post-reboot-journal.log`, `previous-boot-journal.log`, `user-defaults.log`,
`oobe.log` and `installer-preserved.log`. The successful audit marker is
`R9_INSTALLED_STATE_AND_PUBLIC_PACKET_CHECKS_PASSED` in both audit logs.
Online first-boot audits also passed. The time service started during OOBE at
19:07:09 CEST and immediately synchronized with `0.arch.pool.ntp.org`, without
manual repair. Its active wired connection uses `aero7-home`, while the default
zone remains `aero7-public`. Evidence: `online/results/first-boot-time.log`
(`R9_FRESH_ONLINE_TIME_SYNCHRONIZED_WITHOUT_REPAIR`), `installed-audit.log`,
`first-boot-connections.log` and the preserved installer/OOBE journals.
The online VM then completed a Start-menu restart. One deliberately wrong
password produced the expected error and returned to usable login; the correct
password reached the desktop. Repeated package/system/Public packet checks
passed, Home persisted on the same wired connection, and automatic NTP
synchronized again without repair. Evidence: `online/results/post-reboot-*`,
`online/24-reboot-login.png` through `29-reboot-audits.png`. Boot IDs:
`79aadb4044384bafbcb845217554971d` before, and
`060f55d6bfe8486eb8d4e250bdf837f2` after restart.
The logged user audit also passed after reboot: automatic checking selected,
timer enabled/active and no failed user units (`online/results/user-defaults.log`,
`online/30-user-defaults.png`). The QA results share is root-only from the guest,
so the user audit was written to the test account's home and copied out with
administrator authorization. An earlier direct redirect failed; it was a test
log destination issue, not an update-checker failure. Application checks continue.

These successful checkpoints do not mean clean journals. First-boot journals
include a transient KWallet portal service exit and portal application-ID
registration warnings on both variants. The online log also includes a virtual
CPU clocksource watchdog warning. These need classification; do not hide them
behind the later empty `systemctl --failed` result. Neither reviewed restart
journal contained a Plasma stop timeout, but two successful restarts do not
close the previously intermittent shutdown issue.

Read-only portal inspection confirmed that both effective Wallet `Enabled` and
`First Use` are false. The pinned Shell and image setup explicitly configure
that behavior. KDE's packaged portal preferences still select `kwallet` for
the Secret interface, whose activation runs `ksecretd` and exits 255. Thus this
startup warning has a known configuration cause; it is not an installer crash.
It is also not proof that credential storage works. No wallet was enabled, no
secrets were read and no portal was disabled to silence it. Evidence:
`online/results/portals.log`; the pinned Shell remains unchanged. Credential
Manager currently routes to User Accounts, so full credential-manager parity
must not be advertised. Other application-ID registration warnings still need
functional portal checks/classification.

## Additional regional-preview regression (not in r9)

The Dutch regional choice still displayed an English 12-hour setup clock and
Sunday-first English calendar. This was reproduced on the fresh offline guest
and in a regression test. The source now follows the selected region for the
clock, month title, weekday labels and week start, while retaining the selected
timezone's actual instant and abbreviation. Dutch displays 24-hour time and a
Monday-first calendar; US displays 12-hour time and a Sunday-first calendar.

All three installer CTest groups passed after the correction and again after
adding render checks (24.76 seconds). The 1920×1080 Dutch simulation capture was
visually checked. Evidence under `work/beta2-time-final.BzUOt4/`:
`region-preview-before.log`, `region-preview-render-build.log`,
`region-preview-render-tests.log`, and `region-captures/`.
These are source/simulation checks, not proof that r9 contains the correction.
The frozen r9 frontend was not replaced. A later candidate is required.

## Internet Time saved-server regression (not in r9)

On the unchanged offline r49 package, saving `time.nist.gov` with authenticated
approval showed that server on reopening. Turning synchronization off, approving
the change and reopening instead displayed `time.cloudflare.com`. The dialog
used live service status to initialize a saved setting, which disappears when
the service stops. Screenshots: `offline/32-saved-server.png` and
`offline/34-reopen-disabled.png`. These are intentional settings tests after the
initial/reboot audits; they are not installer repairs.

Source now reads and validates the dialog's persisted single-server setting
first, with live status as fallback. It does not claim to parse all administrator
NTP overrides. Targeted persistence/validation and dialog-operation CTests pass
2/2 (`saved-time-server-tests.log`), and all 18 Control Panel CTest groups pass
(`saved-time-server-all-tests.log`, 9.14 seconds).

The rebuilt standalone binary was run from the read-only QA share in the same
offline VM, without replacing its installed r49 package. Reopening while NTP
was still off now showed `time.nist.gov`, with the checkbox off and server
controls disabled: `offline/37-saved-server-fixed.png`. Tested binary SHA-256:
`25d7a00d6ce7bdadb53471dde2788cc8cd2f3c8c3271dca163dfe5c111433a83`.
This is corrected-binary evidence, not fresh-media acceptance. Packaging and
new media remain pending; r9 still contains the reproduced defect.

Re-enabling synchronization through the corrected dialog requested administrator
approval, retained `time.nist.gov`, and reopened with the checkbox on and server
controls enabled (`offline/38-reenable-approval.png`,
`offline/39-reenabled-server.png`). The disconnected guest cannot prove a real
NTP exchange. Its installed package remains r49; only the separate QA binary was
used for this regression check.

## r50 local package and modified-offline-guest validation

The saved-server correction was packaged from the current Control Panel source
in `work/beta2-server-retention.xJ91qO`. `makepkg --nodeps --noconfirm` completed
successfully; the host dependency precheck was skipped, but compilation and all
18 CTest groups ran and passed. No host packages were installed.

- Source archive SHA-256:
  `dd89291c8c00e89b8727c45068fa2eb9c1381bfe8ccbc38ae2b6d6075c695914`.
- Package: `linux-control-panel-0.1.0-50-x86_64.pkg.tar.zst`, 9,333,656 bytes.
- Package SHA-256:
  `eea9f388da05067af57ece49b9271ff023d02992d50684c2a27d96a2da5e50f9`.
- Build/test evidence: `build-r50.log`; archive `.PKGINFO` confirms r50 and
  preserves the dual-backend optional firewall dependencies.

This is unsigned local packaging evidence, not a published package. After the
fresh-r9 checks, the offline guest was upgraded normally with `pacman -U` to
r50. No dependency bypass or forced overwrite was used. Full package integrity
reported 73 files and zero altered; the selected time-server configuration
retained its checksum. The before/after package lists differ only by Control
Panel r49 → r50. Firewalld and timesyncd remained active and no failed system
units were listed. `offline/results/cp50-install.log` ends with
`CP50_LOCAL_PACKAGE_INSTALL_PASSED_NOT_FRESH_R9`.

The installed `/usr/bin/control` then passed the saved-server regression:
`offline/46-cp50-server.png` displays the previously selected `time.nist.gov`;
turning synchronization off requested approval (`47-disable-auth.png`) and
reopening retained that server with disabled controls (`48-cp50-retained-off.png`).
Re-enabling also requested approval (`49-reenable-auth.png`) and reopened with
the same server and enabled controls (`50-cp50-retained-on.png`). This offline
guest cannot demonstrate an NTP exchange. Its earlier fresh-image evidence
remains r49; later results must be labeled as the r50-modified guest.

The local ISO package manifest now selects r50. `scripts/check.sh` completed
with `Static checks passed`; log:
`work/beta2-server-retention.xJ91qO/selected-r50-checks.log`. QML lint warnings
remain visible in that log. The online guest and both r9 artifacts still contain
r49. Later-image inclusion, online regression and full acceptance remain open.

The main installer executable was rebuilt after the regional clock/calendar fix,
not just its test targets. `build/installer/aero7-installer` SHA-256 is
`1956267143810a11c07b796a52a85471bd2706a4a319181e76444df3b7b46c07`.
All three installer CTest groups passed in 21.66 seconds. Logs are
`work/beta2-server-retention.xJ91qO/installer-regional-build.log` and
`installer-regional-tests.log`. The selected-r50 static check also ran all 133
backend tests successfully. This executable and package are future build inputs;
neither changes the frozen r9 profiles or existing ISO hashes. The pinned Shell
worktree remains clean at `cf4d1d8969dfa5ae84308c937cc60146ea59f216`.

## Online r9 screenshot happy path

Unchanged installed packages: Spectacle `1:6.7.4-2`, Desktop `0.2.0-27`,
Theme `6.7.0_742.r9c2d850-44`. Meta+Shift+S opened rectangular selection;
releasing the 601×401 selection closed the overlay without the Spectacle editor.
`online/results/r9-screenshot.log` records the saved PNG under the user's
XDG Pictures/Screenshots folder and no lingering Spectacle process.

`online/39-pasted-image.png` shows actual captured pixels pasted into Paint
with Ctrl+V, including both desktop icons, with 601×401 selection dimensions.
The initial CLI clipboard probe stopped because `wl-paste` is not installed;
this is a missing QA utility, not a clipboard failure. No package was added to
make the application-paste test pass. Paint subsequently displayed its normal
unsaved-document prompt; the disposable pasted copy was discarded, retaining
the original screenshot files.

A second capture produced the saved notification in
`online/40-prompt-toast.png`. Clicking its image opened
`Screenshot 2026-09-06 19.41.24.804-8fd59e.png` in the default viewer at
601×401 (`online/42-viewer-ready.png`), matching the saved-file log.
The earlier delayed captures missed the toast; the one-second post-click capture
was before the viewer became ready. Neither is counted as a failure or as
independent successful viewer evidence. Cancellation and failure-path checks
are recorded separately; offline/final-image coverage is still required.

The next shortcut invocation was cancelled with Escape. The subsequent file
inventory still contains only the two deliberately captured region PNGs and no
lingering Spectacle process. The normal Paint discard path returned to the
terminal; this is not a full draw/save/reopen test.

`online/results/r9-spectacle-probe.json` records four passing checks against the
installed `/usr/bin/spectacle`: new-instance and unique-instance background
captures each saved valid 1920×1080 PNGs, and each corresponding forced save to
a unique nonexistent `/proc` path returned exit 1 without hanging or creating
a file. Successful captures returned exit 0. All completed in under one second.
The probe was run as the normal Wayland user; it changed no packages, services
or directory permissions. Its private temporary evidence directory is retained.
This checks backend error reporting, not the Snipping Tool error-toast/retry UI.

### Controlled failure and graphical retry

A VM-only transient service ran the installed Snipping Tool with the opt-in
fail-once fixture, redirecting only its first Spectacle output to an unwritable
`/proc` path. No installed binary was replaced. The failure notification
displayed **Try Again** (`online/50-forced-save-error.png`). The first click
missed the timeout and is not a successful retry. Repeating with a prompt click
produced `52-error-before-click.png`, reopened selection
(`53-ready-after-retry.png`) and saved a 401×301 PNG. Its notification opened
`Screenshot 2026-09-06 19.50.44.632-de9281.png` in the viewer
(`55-retry-viewer.png`).

The QA shell was edited while waiting for completion, which caused a trailing
shell parse error after the graphical test. Its EXIT cleanup still stopped the
temporary service and restarted the normal service; the log retains exit 2
instead of being relabeled a clean harness pass. This is a test-runner error,
not a Snipping Tool error. The current script passes bash syntax and ShellCheck;
do not edit an active QA script. The separate read-only restoration audit proves
the normal service is active, its executable matches the packaged SHA-256,
the fixture is inactive and no test backend overrides remain. Evidence:
`online/results/r9-snipping-retry.log`, `r9-snipping-restored.log`, with marker
`R9_NORMAL_SNIPPING_SERVICE_RESTORED_WITHOUT_QA_OVERRIDES`.

That audit also reports five altered theme files. Setup's branding functions
rewrite GenericButton.qml and SDDM backgrounds/preview and copy the lock logo;
these differences must not be hidden by a claim of whole-theme integrity.
Spectacle has zero altered files and the Snipping Tool binary itself matches
the package. Installer branding/update ownership remains a separate concern.

## Approved build-drive cleanup

Only the superseded r7 exported offline and online ISO files were permanently
deleted from `work/beta2-profiles.UWsuLM/builder-output/r7-firewall-status/`.
They were regular non-symlink files with no open fuser holders. The running r8
VMs use the separate r8 exports, confirmed from their actual QEMU arguments.
The two deleted images total 4,865,712,128 bytes. Their checksums/build log remain;
recovery requires rebuilding. Current r8 and reference VM disks were untouched.
Host free space rose from approximately 8.9 to 14 GiB.

The isolated builder was confirmed stopped before starting. Its launcher now
uses `discard=unmap` for that builder's qcow2 disk only, so a guest filesystem
trim can reclaim already-unused virtual blocks. No host filesystem trim or
physical disk wipe is authorized by this change.

Guest inspection showed ext4 on `/dev/vda2`, 27 GiB available, and six superseded
ISO copies consuming about 13.6 GiB. The exact six paths are recorded in
`work/beta2-time-final.BzUOt4/cleanup-builder-isos.sh`. All were checked for
regular-file/non-symlink identity, retained checksums, absent loop associations
and absent fuser holders before any deletion. Only those six ISO files were
permanently removed; their directories/checksums and the current r8 outputs
remain. Recovery requires rebuilding, not Trash restoration.

After guest `fstrim /`, the guest reported 41 GiB available and the host about
48 GiB available. The trimmed byte count includes already-free blocks; it is
not a claim that the deleted images alone freed all of that space. Evidence:
`work/beta2-profiles.UWsuLM/builder-output/r9-builder-inspect.log` and
`r9-builder-cleanup.log`.

## Prepared r9 profiles

Both preparations passed their static/backend/installer tests. Prepared inputs:

- Installer binary SHA-256:
  `66d1bf65732ad8e935243c0c905ad98dfb1fa7835bd244ad8a434fc8ca315848`.
- Installer backend SHA-256:
  `a32147b013dcbf2bc7c70b20ce77bbae70b74b74eeab0580f2709edbdc4dc305`.
- Local package manifest SHA-256:
  `19567d953dcb55c9101b0c482e3636bd18381ec0c1034079c238360976ce444c`.
- Control Panel r49 package SHA-256:
  `45ea2224eff8db789a98eac17e408d45fc329c63fe0246544d9430b05331ad88`.

The guarded build script verifies these values before staging, requires at least
18 GiB free on the backing/export filesystem, runs the existing guest capacity
check, and exports to a new `builder-output/r9-time-final/` directory. The build
started under `aero7-r9-builder.service` in the isolated builder. At 18:32 CEST
the service was active/running and the offline SquashFS compressor was active.
No finished-image acceptance is implied.

The older r8 QA guests were unlocked and shut down with `systemctl poweroff`;
both QEMU processes exited normally. Their disks and results remain available.
This freed memory for r9 tests without killing guests or deleting their disks.
The new fixtures live at `/home/admin/VMs/aero7-beta2-r9-xTfYQR`. They require
Control Panel r49 and enabled/active time synchronization after fresh setup.
The disconnected test permits an unsynchronized clock; the connected test has
a separate read-only check requiring actual synchronization without repair.

## Exact-media acceptance checklist

The table is the required matrix, not a claim that every row is either complete
or untouched. Completed r9 checks are recorded above; remaining checks stay open.
Earlier results are regression guidance, not substitutes for the exact installed
package set. Retain the screenshot, log,
boot identity and package identity for each completed runtime check.

| Area | Required evidence |
|---|---|
| Artifact identity | Both `verify-release.sh` runs pass; exact byte sizes and SHA-256 recorded. |
| Installation | Offline QEMU has no NIC; online has NAT. Both complete GUI installation, OOBE, reboot and password login without repairs. |
| Setup corrections | Single target is Disk 0 with its real/fallback model; selected Amsterdam timezone previews the correct time; installed timezone matches. |
| Fresh defaults | Firewalld active with Public default; selected connected Home profile persists; disconnected selection falls back safely; UFW absent only on these fresh systems. |
| Updates | Off/on preference persists, real notification works, install requires approval, cancellation performs no transaction, failed check/install cannot report success. |
| Clock | Service enabled/active on both; actual synchronization online, no-network behavior offline; selected server, invalid input, cancelled approval and off/on/reopen behavior. |
| Desktop | Expected pins, Recycle Bin plus the requested diagnostics folder, no edit mode or brightness tray icon; Start/Explorer route and identity correct. |
| Branding/session | Login and lock logos unclipped; wrong-password recovery; repeated normal logout/shutdown and reboot with logs. |
| Explorer | Libraries/Computer, properties, copy/move conflicts, trash/restore and confirmed permanent deletion on disposable files; full processor line and no raw system mounts. |
| Screenshots | Meta+Shift+S region/release saves PNG, closes selector without editor, copies real pixels for Ctrl+V, shows toast opening that same file; Escape, save failure and retry. |
| Applications | Paint draw/save/reopen/normal close without crash; Control Panel routes; Device/Computer Management; gadgets add/persist/remove. |
| Optional features | Programs Center install/open/remove/re-enable on disconnected media; dependency and approval failure behavior; retained user data. |
| Icons/themes | Existing pack only; owned chrome remains stable across installed themes; capture actual dialogs, menus and notification identity. |
| Failure/device coverage | Record service-unavailable, removable-media, display and recovery tests separately; no physical Bluetooth/printer/audio claims from a VM without the corresponding device. |
| Release handoff | Complete website Markdown, announcement drafts, exact 1920×1080 screenshot inventory and unresolved limitations; no upload/promotion without fresh approval. |

Historical scope references re-read during this pass include the user's
remaining-parity and icon-independence prompts, the repository's
`docs/WINDOWS7-SYSTEM-PARITY.md` and `docs/VISIBLE-KDE-AUDIT.md`, and Desktop's
`docs/AERO7-ICON-INDEPENDENCE-AUDIT.md`. The first two matrices are dated
23 August, and the icon audit 3 September. Their Partial/Missing/Pending items
are not cleared by this build or by newer source tests alone. Reconcile each
with current runtime evidence before claiming full parity or zero visible KDE.
