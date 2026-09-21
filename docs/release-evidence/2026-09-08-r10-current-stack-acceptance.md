# r10 current-stack media — acceptance in progress

This is a QA record, not publication approval. Both r10 ISOs completed fresh
installation, OOBE and first-reboot password login; full desktop acceptance
remains incomplete. Older r9 and modified-VM results are regression guidance,
not substitutes for testing these exact images. Later component upgrades are
identified separately below.

## Frozen candidate inputs

Prepared profiles: `work/beta2-r10.Sf7FVw/profile-{online,offline}`.
Both preparations completed with 144 passing Python tests, all three CTest
suites passing and the full source checker passing. The new strict UI suite
has 20 passes including setup/cleanup and emits no warnings.

| Input | Identity |
| --- | --- |
| Installer frontend | SHA-256 `52f467fdad31447f988daf4d7d54aa24c729b326b11d0bb37b75bce264df1d62` |
| Installer backend | SHA-256 `ec300f0f98c4dff28ac0962d72b68c8aca16687a020c06206523f49695905b77` |
| Local-package manifest | SHA-256 `2f612cf8d3a992a3c33e8d9fa4f90260f4590f1e75fb3f3fd6e01fea58466770` |
| File Explorer | `25.12.3-50` |
| Desktop | `0.2.0-29` |
| Plasma Workspace | `6.7.4-3.2` |
| Control Panel | `0.1.0-50` |
| Paint | `25.12.3-8` |
| Desktop theme | `6.7.0_742.r9c2d850-46` |
| Spectacle | `1:6.7.4-2` |
| Gadgets | `3.0.0-3` |

Both embedded frontends/backends and manifests match the selected inputs, and
all 14 embedded local-package hashes verify in both profiles. lsof is required
in the common base list and present in the offline bundle. The check mark and
Recycle Bin are unchanged copies of the selected approved icon pack; see the
[icon provenance and rendering report](2026-09-08-installer-approved-icons.md).

## Build and test isolation

The offline export completed and passes the full `verify-release.sh`, including
the additional byte-for-byte check of both retained installer icon notices.
The online export also completed and passes the same full verifier. Both export
markers, `R10_BOTH_BUILDS_EXPORTED` and `R10_BUILDER_EXIT=0` are recorded in
`r10-logs/both-builds-completed.log`. These are build results, not install results.

| Variant | QA artifact | Bytes | SHA-256 | Result |
| --- | --- | --- | --- | --- |
| Offline | `aero7-beta2-offline-2026.09.08-x86_64.iso` | 3,339,970,560 | `00cb8dc15162ed9698f5127ad1d7473675e8eabed079cf31ebdbfd71feeec1cf` | Content verification, fresh installation, OOBE and reboot/login passed; full acceptance incomplete |
| Online | `aero7-beta2-online-2026.09.08-x86_64.iso` | 1,562,912,768 | `f424e57f1d826db4946c378285a2a2c233b95fa174680543bad29e0df93caf0d` | Content verification, fresh installation, OOBE and reboot/login passed; full acceptance incomplete |

The notice-check addition changes only the verifier, not the frozen image
inputs. ShellCheck and all six candidate-package/policy tests pass afterwards.
Offline verification was rerun successfully with that stronger check.

The existing isolated builder is `/home/admin/VMs/aero7-beta2-builder.HD2BwR`.
Its `aero7-r10-builder.service` builds offline then online. Exports go to
`work/beta2-profiles.UWsuLM/builder-output/r10-current-stack/`. The final marker
`R10_BUILDER_EXIT=0`, successful export markers, checksum checks and exact ISO
verification are required before recording build success. An active service's
`Result=success` field alone is not a completion result.

Fresh QA root: `/home/admin/VMs/aero7-beta2-r10-oTmJ9G`. Its launcher verifies
the supplied SHA-256 before creating a guest, refuses an existing guest path,
and requires the builder to be stopped to limit memory pressure. Both guests
use fresh 64 GiB virtual disks, UEFI and 1920×1080. Offline has `-nic none`;
online has NAT. It does not install into or overwrite any older guest disk.
The old UFW compatibility guest, original desktop/wiki disks, Windows reference
and r9 baselines remain preserved.

Launcher negative checks passed: a wrong checksum is rejected before any guest
directory is created, and a correctly identified older fixture is rejected
while the builder disk is in use. These are harness safety tests, not r10
boot/install results. At 12:29:45 CEST the online compressor PID 36970 remained
active under build-service MainPID 3182, using both assigned cores.

The installed-state helper checks the current pinned package versions, absent
fresh-install UFW, absent optional Programs Center, active Firewalld/public
policy, update/time-service defaults, NIC isolation, failed units, crash records
and package-file integrity. Its isolated IPv4/IPv6 packet fixture also checks
blocked unsolicited inbound traffic and working outbound replies. These checks
are prepared, not yet passed on r10.

## Exact-media acceptance matrix

The builder was normally powered off after export/verification. The checksum-
guarded fresh offline VM was then created and booted with no network adapter.
GUI installation targeted only its new 64 GiB `/dev/vda`; setup restarted into
OOBE and reached the desktop without package or configuration repairs. OOBE
selected `aero7test`, hostname `aero7-r10-offline`, English/US, Amsterdam,
automatic update checks and Public network. First-session arrival alone is not
full acceptance; subsequent results are recorded below.

The first-session installed audit subsequently passed: all selected versions,
package file presence, no system-level failed units or crash dumps, active
Firewalld/Public with UFW absent, Programs Center absent, update timer enabled,
Amsterdam/NTP enabled but unsynchronized offline, and only loopback networking.
The isolated IPv4 and IPv6 packet tests both blocked unsolicited inbound traffic
while allowing outbound traffic and verified replies. Evidence:
`r10-logs/offline-first-session-audit.log` and `r10-logs/offline-installer.log`.
The system was then normally rebooted to SDDM, with an unclipped logo; an
incorrect password was rejected with the expected recovery dialog. Dismissing
that dialog and entering the correct password returned to the normal desktop;
the 1920×1080 capture `offline/results/23-password-login-desktop.png` records
that result. The offline guest was subsequently shut down normally and is
preserved. No host packages/firewall settings changed.

This audit does not mean every journal message is resolved. First-session logs
still contain the known disabled-wallet Secret-portal failure, application-ID
registration warnings, a missing kameleon object and a variable-width terminal
font warning. User-service and graphical follow-ups remain required. Missing
repository database warnings during disconnected package queries are retained
in the logs; package versions/integrity checks nevertheless passed.

The QA-only live log collector initially stopped because `hostname` is absent
from the minimal live environment. Its guard now reads the same kernel value
from `/proc/sys/kernel/hostname`; ShellCheck passes. The installer restarted
before a live export was captured. The normal installer's preserved target
logs are being collected instead. No ISO/package repair was made for this
QA-helper issue.

### Fresh online installation and first reboot

The checksum-guarded online guest was created separately at the same QA root,
with a new 64 GiB virtual disk and NAT networking. GUI installation and OOBE
completed without repair. Its account is `aero7test`, hostname
`aero7-r10-online`, English/US, Amsterdam, automatic checks enabled and Public
network. The live collector now works and recorded the active installer and
network interface while packages were installing. Final installer logs were
also preserved automatically in the target and exported.

The installed-state audit passed all selected package versions/file-presence
checks, Firewalld/Public policy, absent UFW and optional Programs Center,
enabled update timer, no system-level failed units or crash dumps, and the
IPv4/IPv6 inbound-blocked/outbound-and-reply packet fixtures. Unlike offline,
the online clock synchronized automatically. Evidence is in
`r10-logs/online-first-session-audit.log` and `r10-logs/online-installer.log`.
Normal reboot reached the intact SDDM login screen and correct-password login
returned to the desktop, captured in `online/results/17-password-login.png`.
The online VM remains running at that desktop; the offline VM is stopped.

The read-only user-session diagnostics reported zero currently failed user
units and an enabled, waiting update-check timer. Its journal nevertheless
retains the disabled-wallet portal activation failure and terminal font
warnings. A cleared/transient unit list does not establish absence of those
errors. `online/results/session-diagnostics.log` retains the full evidence.

Terminal-font triage: the fresh QTerminal settings contain no explicit font
family. Fontconfig resolves the generic monospace family to Noto Sans Mono;
DejaVu Sans Mono and Liberation Mono are also installed. QTerminal 2.4.0 uses
the generic `Monospace` default and reads `fontFamily`/`fontSize`, with a legacy
`font` override ([upstream configuration](https://github.com/lxqt/qterminal/blob/2.4.0/src/config.h),
[settings implementation](https://github.com/lxqt/qterminal/blob/2.4.0/src/properties.cpp)).
The isolated Qt probe measured equal ASCII widths for the default Noto Sans
Mono and both explicit mono families. Qt nevertheless reports `fixedPitch=0`
for Noto Sans Mono and `fixedPitch=1` for DejaVu/Liberation Mono.
[QTermWidget's warning](https://github.com/lxqt/qtermwidget/blob/2.4.0/lib/TerminalDisplay.cpp)
checks that flag; the measurements do not demonstrate ASCII alignment damage.
An explicit DejaVu profile reduced warnings from three to one, but did not
eliminate the startup warning. The first comparison's apparent PASS was
invalid: a standalone negated grep did not trigger Bash errexit. The corrected
test explicitly exits on the remaining warning and fails, recorded in
`online/results/font-comparison-corrected.log`. The stronger system-default
test also failed before reaching custom/legacy preference checks. Its trace
is `online/results/system-font-trace.log`; metrics are in
`online/results/font-metrics.log`. The ineffective proposed packaged default
was withdrawn completely; Desktop remains package release 29. No installed
terminal preferences were overwritten, and this issue remains unresolved.

| Area | r10 evidence required | Current result |
| --- | --- | --- |
| Both ISO artifacts | Export completion, byte sizes/hashes and both `verify-release.sh` runs | Both passed; fresh-install results are recorded separately below |
| Fresh installation | GUI install, OOBE and password login without repairs for both variants | Both passed this path and first-session package/system audits; broader acceptance below remains pending |
| Offline guarantee | No NIC throughout install and optional-feature operations | Install/OOBE plus Programs Center install/open/remove/reinstall passed with no NIC; other optional features are not claimed offline-capable |
| Defaults | Expected pins, Recycle Bin and diagnostics folder; Firewalld; update checks toggleable with approval before installing | Offline appearance observed; Public/firewalld audited. Subsequent offline update-settings pass verified OFF/Cancel/relaunch, manual offline failure, ON/reboot persistence and approval-decline test replay; successful online transactions remain pending |
| Existing systems | Preserved UFW behavior on the compatibility guest | Earlier evidence only; regression remains |
| Time setup | Correct selected zone/preview, persisted server and online/offline synchronization behavior | Both used Amsterdam; online synchronized and offline remained unsynchronized; additional server-edit workflow pending |
| Session/branding | Unclipped login/lock logos, wrong-password recovery, reboot, logout/shutdown, theme reload and no late splash | Pending |
| Explorer/dialogs | Correct identity/pins, Libraries/Computer, file operations, dialogs, drive labels and removal/failure recovery | Pending |
| Screenshots | Region shortcut/release, PNG saved, pixels pasted, notification opens same file; cancellation/error recovery | Online and offline success, confirmed-overlay Escape cancellation and backend save/error probes passed. Later theme-47 installed package passed failed-save/Try Again/save/open/pixel-paste and ready-Escape replay; final-media acceptance and rapid-start timing remain |
| Applications | Paint save/reopen/close, Control Panel routes, management apps, gadgets persistence | Pending |
| Optional features | Programs Center install/open/remove/reinstall offline and approval/failure handling | Programs Center cycle and pre-transaction confirmation cancellation passed; broader error/authentication-cancellation paths remain |
| Broader coverage | Multi-monitor, service recovery, unavailable-device paths; explicitly separate untested physical hardware | Pending |
| Handoff | Verified screenshots, artifact table, detailed website/announcement Markdown and owner review | Draft maintained; not publishable |

Credential Manager policy remains an owner decision: the current candidates
keep the existing disabled password-wallet default. A question has been sent
about retaining that default versus enabling encrypted password storage. No
password-storage policy has been changed by this build/test pass.

## Fresh online screenshot workflow, 8 September

Tested in the unmodified installed r10 online Wayland session at 1920×1080,
with Spectacle `1:6.7.4-2`, Desktop `0.2.0-29` and Paint `25.12.3-8`.
No clipboard utility or replacement package was installed for this test.

- Actual Meta+Shift+S opened the rectangular selector. A mouse drag/release
  closed the overlay and produced the Plasma “Screenshot saved” notification,
  with no editor/main window. Evidence: `online/results/21-region-overlay.png`
  and `22-region-released.png` under the r10 QA directory.
- The saved PNGs are in `/home/aero7test/Pictures/Screenshots`, matching the
  XDG Pictures directory plus Screenshots. Repeated 401×301 captures had
  distinct filenames. Both had SHA-256
  `045c013bb5e0c3ab41590bcfbba00006e2496998bc4b9919ad9da9f73ce5e758`.
- Clicking the notification preview opened the matching named PNG in the
  default viewer (`org.kde.gwenview.desktop`). A later capture also opened
  through a click on the notification text body. Screenshots:
  `24-notification-viewer.png` and `31-notification-body-open.png`.
- Actual Ctrl+V into fresh Paint pasted the image, not a path. Saving through
  its native Save Image As dialog produced `paint-pasted.png`, 401×301.
  ImageMagick `compare -metric AE` against the original screenshot returned
  `0 (0)` with exit 0: zero differing pixels. Screenshots 25–27 retain the
  paste, save dialog and saved document. Paint then closed normally.
- The first rapid cancellation sequence was **not a valid cancellation
  pass**: its audit command was not received by the terminal, and an extra
  fullscreen image appeared. Inputs had continued without first confirming
  overlay readiness/closure. This startup-timing anomaly needs a controlled
  rapid-Escape replay; it is not silently counted as success or attributed
  definitively to the product.
- The controlled repeat captured the visible overlay in
  `30-cancel-overlay.png`, sent Escape, then refocused the terminal. The
  before/after audits (`screenshot-retry.log`,
  `screenshot-cancel-verified.log`) retained the same four filenames and
  hashes, with no remaining Spectacle process. The Snipping Tool daemon
  correctly remained running. A later region capture succeeded.
- The installed background probe passed all four cases: new-instance and
  unique-instance saves produced 1920×1080 PNGs and exit 0; their deliberately
  impossible `/proc` save destinations returned exit 1, without a timeout.
  Runtime was 0.543–0.770 seconds per case. Evidence:
  `r10-logs/online-spectacle-probe.json`. Subsequent shortcut capture and
  notification opening still worked (`31-notification-body-open.png`).

This establishes the listed online paths, not the full screenshot matrix.
Offline replay, early-input timing, failure notification/Try Again behavior
and broader application/dialog coverage remain open. The Save Image As
dialog visibly exposes the raw library location in its address field; visual
parity of that dialog is not certified by the successful PNG save.

### Controlled early-Escape replay

A separate QMP replay sent only Meta+Shift+S and Escape, without Enter, text,
mouse selection or clipboard changes. Escape at approximately 50, 300 and
650 ms after the shortcut was missed: the selector was still visible 1.5
seconds later. Escape at approximately 1,250 ms closed it. Each case also
sent a late Escape to leave the selector closed before the next test.
A guest-side observer recorded the same five pre-existing screenshot names
throughout its completed 90-second observation; no new PNG was produced.
Evidence in the r10 online results directory:
`early-escape-inputs.jsonl`, `early-escape-files.jsonl` and the four
`early-escape-*.png` captures. Early cancellation therefore remains a genuine
input-timing limitation, but Escape alone did not cause the extra fullscreen
capture. No speculative startup/input patch was installed or packaged.

## Fresh offline Programs Center optional-feature cycle

The online VM shut down normally before the installed offline VM resumed.
The offline ISO checksum was reverified and the existing disk/UEFI state was
preserved. No new install, package repair or network adapter was introduced.
The offline guest again reached SDDM and password login at 1920×1080.

Programs Center was absent in the baseline package audit. The actual
“Turn Aero7 features on or off” window showed Programs Center Beta as optional
and not installed, while Desktop Core was installed and non-removable.
Cancelling the install confirmation left the complete package list byte-for-byte
unchanged. A subsequent confirmed request prompted for the administrator
password and installed the bundled package successfully.

The feature window's Open button launched Programs Center. Its Installed
Programs page remained usable without repository databases; the Home page
truthfully warned that repository information was missing and required an
internet refresh. No repository refresh was attempted. The app closed normally.

Unchecking Programs Center and confirming removal required authentication
again and completed successfully. The UI returned to “Not installed.” A
second install from the bundled cache also authenticated and completed, and
the Open button launched the app again. Transaction evidence records:

| Operation | Guest local time | Result |
| --- | --- | --- |
| Install | 13:45:54–55 | Installed `aero7-programs-center-git 0.1.0.r12.g0405a2e-2` |
| Remove | 13:48:56–57 | Removed that package; helper verified removal |
| Reinstall | 13:50:01 | Installed the same bundled package again |

Both installed/reinstalled audits passed `pacman -Qk` and found no failed
system units. Each stage recorded only loopback networking. The installed
and reinstalled complete package lists match; compared with baseline, their
only addition is Programs Center. The intermediate post-removal audit did
not run because early typed input lost its `bash` prefix during window
closure (captured in `47-terminal-postcycle.png`); removal is instead proven
by the UI, helper transaction and completed pacman removal transaction. No
post-removal package-list comparison is claimed.

Evidence is under the r10 QA `offline/results` directory, screenshots 33–48,
`optional-{baseline,cancelled,installed,reinstalled}.log`, package lists and
`optional-reinstalled-transactions.jsonl`. Copies of the final audit and
transaction log are retained in `r10-logs/offline-optional-reinstalled.log`
and `r10-logs/offline-optional-transactions.jsonl`.

Programs Center was left installed on this **test VM only**, for further
checks; the frozen ISO default still leaves it optional and absent. At this
stage its Home page overflowed horizontally and its metadata labelled Paint
as “KolourPaint.” The subsequent [layout and Paint identity component pass](2026-09-08-programs-home-and-paint.md)
corrects both in normally upgraded packages, with source tests and installed
Wayland evidence. The frozen r10 images have not gained those fixes.
This cycle does not certify the whole Programs Center, all optional
features, authentication cancellation, corrupt-bundle recovery or preserved
user-data behavior.

## Subsequent offline recovery and screenshot checks

Subsequent [offline recovery and screenshot testing](2026-09-08-offline-recovery-and-screenshots.md)
verified administrator-approval cancellation, release-3 removal with existing
settings retained, damaged-bundle rejection and same-window Try Again recovery.
The original bundle was restored after testing. It also verified offline PNG
capture, pixel-preserving paste into Paint, notification opening and Escape
cancellation after selector readiness. These component-upgraded guest results
do not update the frozen ISO contents or certify the entire release matrix.

The subsequent [update-settings pass](2026-09-08-update-preferences.md) adds
installed UI persistence/error checks and 20 passing Qt test rows in the
offline guest's Wayland session. No packages changed during that pass.

The [Snipping Tool notification handoff pass](2026-09-08-snipping-notification-handoff.md)
subsequently reproduced an error-notification suppression race and tested a
source-built and installed theme-47 correction with actual Try Again recovery,
pixel-identical clipboard paste and ready-Escape cancellation. It is not a change to
the frozen r10 images, and it leaves early Escape timing unresolved.

## Read-only project-link check

GitHub API metadata was checked on 8 September. All six handoff repositories
resolve and are unarchived. Current default branches are `beta` for Aero7,
Desktop, File Explorer and the package repository; Control Panel and Programs
Center use `main`. No branch was renamed. File Explorer's GitHub parent and
source are both `KDE/dolphin`, confirming the registered fork relationship.

The three linked wiki Git repositories also resolve:

| Wiki | Observed HEAD |
| --- | --- |
| Desktop | `fce0dafde10d0eede1a1b75ca9d739c0977d0b26` |
| File Explorer | `9a05f125d43e1e392ea9d36eeeb0bda7ed9476f3` |
| Control Panel | `8ea59cc66b2fe77be45cfb4c928e4762cc826d09` |

These checks establish destination availability, not that unpublished local
documentation or final screenshots are already present there. No GitHub writes
were performed.
