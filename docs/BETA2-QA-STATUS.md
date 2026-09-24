# Aero7 Beta 2 — QA status and evidence history

Updated 24 September 2026. This engineering record supports the
[approved website handoff](BETA2-WEBSITE-MAKER-HANDOFF.md). It preserves the distinction
between frozen-media tests and later component upgrades. The release owner's
publication approval is recorded in that handoff; this file remains technical
evidence rather than website copy.

### Current website rollout state

**Stale firmware clock candidate acceptance:** The
[24 September report](release-evidence/2026-09-24-stale-clock-bootstrap-acceptance.md)
records the repair for the physical-install failure where `aero7.db`, `core.db`
and `extra.db` were rejected because HTTPS certificates appeared not yet valid.
Both newly rebuilt candidates were booted with a deliberately stale
`2026-08-01` firmware clock and completed clean installation, OOBE, installed
repository synchronization and a second reboot. The embedded clock floor runs
before networking and package initialization, is retained in the installed
system and never moves a newer clock backwards. All 164 Python tests, all three
C++/Qt tests, static checks and both exact image verifiers pass. The pair is
unpublished and remains on the Friday release boundary.

**The 23 September local candidate pair has passed clean-install VM acceptance,
but remains unpublished until the planned Friday release decision.** Do not
enable either website download until the release owner gives the final go-ahead
and the uploaded bytes, final URL and checksum have been verified.

**Self-hosted repository candidate acceptance:** The
[23 September report](release-evidence/2026-09-23-self-hosted-repository-candidate-acceptance.md)
records the exact online and offline ISO hashes rebuilt from signed repository
build `20260923T180513Z-ce604b74debf`. Both exact images passed structural
verification, clean UEFI installation, OOBE, first desktop, reboot/password
login, File Explorer launch, diagnostic-manifest verification and powered-off
disk checks. The online system also opened the searchable Optional Features
manager and verified active firewalld. The offline cycle was repeated after a
QEMU launcher defect was found; the accepted rerun used explicit `-nic none`,
and its collected network inventory contains only loopback with no external
route. All 162 integration tests pass. These are VM results, not physical
GPU/hotplug or physical multi-monitor certification.

**Exact final-media acceptance:** The
[22 September final-media report](release-evidence/2026-09-22-final-online-offline-media-acceptance.md)
records the locally finalized offline and online images, exact byte sizes and
SHA-256 values. Each exact image completed a clean UEFI installation, OOBE,
first login, installed-system audit, optional Programs Center install/removal,
reboot and taskbar File Explorer launch at 1920x1080. The offline installation
ran with no network adapter; the online installation verified live networking
and synchronized time. Both systems had zero failed user/system units and no
collected coredumps. Both also proved that the rebuilt graphical-session
PolicyKit link starts `/usr/lib/uac-polkit-agent` before the first privileged
feature-manager request. The rebooted login branding was unclipped. These are
VM results, not physical GPU/hotplug or physical multi-monitor certification.

**Fresh rebuilt test-candidate acceptance:** both the online and offline
21 September images now pass structural verification, clean installation,
OOBE, reboot/login and exported-log validation. Each installed system reports
zero failed user or system units, no collected coredumps, active firewalld and
the selected Desktop 33 / Explorer 55 / Control Panel 55 / theme 65 stack. The
collector manifests verify 144 of 144 listed files. Login and lock branding,
the full SDDM Ease of Access dialog and session selector, File Explorer identity
and taskbar launch, the searchable Optional Features entry, Programs Center
install/removal, and the default-off vault were exercised. Meta+Shift+S also
passed rectangular selection, automatic PNG save, actual image-pixel clipboard
paste, notification display and notification-to-viewer launch. See the
[21 September acceptance report](release-evidence/2026-09-21-rebuilt-online-offline-acceptance.md).
These are accepted **test candidates**, not publication authorization or final
website artifacts. Physical GPU/hotplug and multi-monitor hardware remain
outside this VM pass.

**Refreshed selected-KWallet candidate acceptance:** The
[22 September candidate report](release-evidence/2026-09-22-selected-kwallet-candidate-acceptance.md)
records newly exported online and offline test images after the required
`kwallet 6.29.0-1.1` package was selected. Both images pass boot/source release
verification and fresh installation through OOBE to the installed desktop. The
installed audits confirm Desktop 33, Explorer 55, Control Panel 55, KWallet
`6.29.0-1.1`, Vault 7 absent by default, matching optional caches, enabled
firewalld and no coredumps. The offline helper then installs Vault 7 from its
verified local cache, and the native first-use/password UI is titled **Aero7
Credential Vault** with the existing bundled icon. The online graphical boot
has no error-priority journal entries or failed-unit result. Known image-mode
package-origin and Plymouth-hold warnings remain recorded. The offline replay
used embedded package paths but had a virtual NIC available, so it is not
misrepresented as a new no-NIC run. These are still internal test candidates,
not final/public artifacts.

**Vault presentation installed-VM checkpoint:** The
[scoped native-dialog patch](release-evidence/2026-09-13-vault-presentation-source.md)
builds the real KWallet service and passes 16 presentation results, five source
preparation tests and 16 upstream Secret Service results. The
[20 September native replay](release-evidence/2026-09-20-vault-presentation-native-vm.md)
then upgrades the test package normally, reboots and exits 0 after real Aero7
unlock/error/cancel/relock UI, two simultaneous clients and two decoded
synthetic read/lock cycles. Wallet filenames/non-ciphertext metadata, packages,
desktop services and final lock state are preserved with no failed units. The
accepted override is now selected in the source manifest. The refreshed
22 September candidates integrate that exact package and pass the native
first-use/password presentation replay described above. This closes the scoped
vault-presentation pre-build item. The rebuilt candidates also close the
separate login Ease of Access gate.

**Latest pre-build review:** The [requirement/website review](release-evidence/2026-09-13-prebuild-requirement-review.md)
reconciles later test evidence with historical pending statements. A fresh run
passes 160 integration tests, static checks, 19 online candidate-archive checks,
84 offline candidate/dependency-archive checks, 65 offline repository-entry
checks and the release-note version/optionality guard. [Reviewed storage cleanup](release-evidence/2026-09-13-build-space-plan.md)
leaves 38.9 GiB host capacity at its checkpoint. The review originally found two
unmet presentation requirements. The later installed-VM checkpoint above
resolves the scoped Aero7 vault prompt behavior, subject to release-package
selection. The rebuilt 21 September candidates subsequently close the full login
Ease of Access dialog and bottom session-tab requirement. Final-image build and
release gates remain unchanged.

**Latest native vault checkpoint:** [Two-window prompt replay and retention](release-evidence/2026-09-13-vault-native-prompts.md)
verifies shared cancellation, retry, closing one waiting client and successful
completion by the survivor. Two further native read/lock cycles confirm the
complete retained synthetic credential. The original encrypted-file hash check
exited 1 because lock/save re-encrypts with fresh random data; its failure remains
recorded, and the separate content/preservation follow-up exits 0. No production
package changed. Prompt-parenting limits remain explicit. The later review above
completes the documentation/storage actions and identifies presentation gaps.

**Latest diagnostic checkpoint:** [Startup resource and runtime triage](release-evidence/2026-09-13-startup-diagnostic-triage.md)
identifies all 13 SVG warnings in seven packaged/installed resources. All 80
selected theme resource hashes match the guest; the 200-resource installed scan
rejects none. Controlled Qt rendering comparisons pass on host and guest without
changing artwork. Software graphics and auxiliary portal/hardware limitations
remain documented. The full guest audit exits 1 because the scheduled update
check had already failed in the NIC-free VM; a separate classifier verifies
that exact failure without clearing it. Desktop PIDs, packages and configuration
remain unchanged with zero desktop-service restarts. This is diagnostic closure,
not warning-free logs or final-image acceptance. See the newer vault checkpoint
above for the subsequently completed native prompt replay.

**Latest source-input checkpoint:** [Retained source inputs](release-evidence/2026-09-13-retained-source-inputs.md)
verifies all 95 declared inputs of the 18 selected recipes, plus the Gadgets
install hook and Qt's supplemental commit. No missing inputs were found. Five
complete source-snapshot comparisons classify the later Explorer/Vault tests
and Desktop's older nested vault source without hiding those differences.
Six auditor tests pass. No source fetch, runtime package change, signature
reverification or final image build occurred. Source-input traceability is now
closed for this selection; the other pre-build checklist items remain open.

**Latest combined-guest checkpoint:** [Selected-stack alignment and recipe audit](release-evidence/2026-09-13-selected-stack-alignment.md)
passes normal reboot/password login and all 16 selected core versions in both
existing test guests. Both optional caches match the selected archives; the
offline vault stays absent/disabled, while the online vault and encrypted files
are preserved. Running Gadgets, Action Center and the actual mapped KWin library
match their builds, with zero desktop-service restarts and no failed units at
both checkpoints. All 18 retained recipe hashes match BUILDINFO. This is not
fresh-media acceptance, a warning-free log claim or complete source attestation.
Follow the [pre-build closure checklist](BETA2-PREBUILD-CHECKLIST.md) for the
specific remaining actions, separately from later final-image/publication gates.

**Latest tests and documentation:** [Vault overlap and documentation consistency](release-evidence/2026-09-13-vault-overlap-and-docs.md)
adds five backend cases for reversed/dropped-client unlock replies, duplicate
requests, late completion after deletion and explicit account disable. All 31
host results and 22 private-bus Wayland backend results pass; real wallet state
and desktop services are unchanged. No production package changed. Release
notes now match all 18 archive identities and optional labels; a new verifier
guard prevents stale version tables. The Optional Features guide now includes
the vault. All 153 integration tests and both archive-variant checks pass.
Broader pre-build review and final-media acceptance remain open.

**Current optional-package correction:** [Vault lock-state type verification](release-evidence/2026-09-13-vault-lock-property.md)
reproduces three paths that accepted malformed non-boolean lock state. The source
fix passes 26 host test results, 17 private-bus Wayland backend results and both
local release-7 package test groups. Native upgrade preserves the encrypted
wallet files; two installed application processes unlock and lock together,
including dismissing the other window's revealed editor. The final collection
lock and exact optional cache are verified. The manifest now selects Vault 7;
all 149 integration tests and online/offline archive checks pass again.
The native script's final zero-failed-units assertion found an earlier QA mount
command launched without Terminal; the retained diagnostics establish that
setup failure separately. It is not presented as a fully green native script.
The earlier offline selected-stack audit below still used a cached Vault 6.
Broader pre-build/failure-path review and final media remain pending.

**Current selection and login:** [Control Panel 55 source cleanup and login](release-evidence/2026-09-13-control-panel-source-cleanup.md)
closes the generated Python-cache source-bundle item. All 21 package test groups,
normal upgrade, the visible 45-applet/five-column view and Optional Features
open/close checks pass. The catalog has 15 entries and exposes 13 searchable
optional features, excluding the protected core and hidden discontinued entry.
A normal logout/login verifies all 16 core versions, including Desktop 33 /
Control Panel 55 / Gadgets 25 / KWin 7.3, the newly autostarted Action Center,
unchanged gadget layout and active desktop services with zero restarts.
All 149 integration tests, 18 online / 53 offline archive checks and 35 offline
repository-entry checks pass. Final-media and broader failure-path review remain
open; this is an upgraded-VM login, not a new fresh-install claim.

**Previous source-package correction:** [Desktop 33 source cleanup](release-evidence/2026-09-13-desktop-source-cleanup.md)
removes generated build trees/nested archives from the source snapshot without
deleting old artifacts. Seven new exporter tests and all 10 package test groups
pass; the normal VM upgrade and rebuilt Recovery-window open/close check pass
without desktop-service restarts. Desktop 33 is selected with Gadgets 25 /
Control Panel 54 / KWin 7.3. The 149 integration tests and 18 online / 53 offline
archive / 35 repository-entry checks pass again. The earlier combined reboot
below used Desktop 32. Control Panel source-cache cleanup was subsequently closed
by release 55 above; final media remain pending. These source checks do not
authorize publication.

**Overlapping dialog coverage:** [Eight new concurrency cases](release-evidence/2026-09-13-dialog-concurrency.md)
pass against the existing Explorer 54 library. They cover same/different app
state IDs, pending-search cancellation/destruction/reopening and independent
Save As results in either completion order. The full suite passes 67 results
offscreen and against the installed Wayland library, with no desktop-service
PID/restart changes. This is library-dialog coverage, not independent external
process or physical-device coverage. No production package changed.

**Combined selected-stack reboot:** The [13 September normal-reboot audit](release-evidence/2026-09-13-combined-stack-reboot.md)
passes all 16 selected core versions, installed-file presence, the actual running
KWin library and Gadgets 25 executable, disabled-vault policy, active firewalld
and unchanged gadget layout. Desktop units have zero restarts and no failed
user/system units at the checkpoint. The VM restarted through Start and password
login; this is not a powered-off cold start or a fresh-image install. Full logs
retain virtual graphics/CPU, optional-hardware and auxiliary portal-registration
warnings. Final media and broader pre-build acceptance remain open.

**Current selected correction:** [Slideshow Options](release-evidence/2026-09-13-slideshow-options.md)
reproduces unchanged OK resetting the picture and resuming a paused slideshow.
Gadgets 25 passes all eight source/package test groups, normal upgrade and the
native unchanged-OK, paused-delay-change and explicit-resume replay. The current
picture and pause state are preserved; the new interval takes effect on Play.
Normal logout/login verifies the autostarted release-25 executable, unchanged
account layout and active desktop services with zero restarts/no failed units
at that checkpoint. Gadgets 25 / Control Panel 54 / KWin 7.3 are now selected;
all 149 integration tests, 18 online / 53 offline archive checks and 35 offline
repository-entry checks pass. Neither frozen ISO has changed. Final-media and
broader acceptance remain open; previous selections below are historical.

**Previous selected correction:** [Damaged feed-list recovery](release-evidence/2026-09-13-gadget-catalog-recovery.md)
fixes a path that could overwrite an invalid saved catalog with defaults or a
partial list. Gadgets 24 preserves the original, disables editing, displays a
readable explanation and reloads a repaired file through Try Again. All eight
source/package test groups pass, including seven new damaged/unreadable-file
cases. Normal VM upgrade, native preservation/retry/reopen and normal-login
autostart checks pass; the ordinary account layout is unchanged.
The manifest now selects Gadgets 24 / Control Panel 54 / KWin 7.3. All 149
integration tests, 18 online / 53 offline archive checks and 35 offline
repository-entry checks pass. Older selection statements below are historical.
Neither frozen ISO includes these newer fixes; final-media acceptance is open.

**Previous display pass:** [Display scaling and rollback](release-evidence/2026-09-13-display-rollback.md)
confirms that the installed Control Panel 53 returns a single virtual output
from 125% to 100% after its confirmation timeout, with the original Aero panel
and unchanged desktop-service processes. A separate native check reproduces
Apply staying disabled after dragging the selected monitor. Five source
regressions expose that defect, rollback using the draft position, and hidden
keep/restore/failure messages. The correction passes all 21 Control Panel test
groups. Release 54 also passes all package-check groups, normal VM upgrade,
enabled-Apply replay, the 125% timeout rollback, accepted 125% and accepted
return to 100%. Result messages remain visible. The final backend/panel audit
confirms the original output state and unchanged desktop-service processes.
The separate notification-only update check has failed in the NIC-less VM;
this is recorded, not hidden as a completely clean failed-unit list.
Control Panel 54 is selected with Gadgets 23 / KWin 7.3; all 149 integration
tests, 18 online / 53 offline archive checks and 35 offline repository-entry
checks pass.

**Multi-output/recovery follow-up:** [Installed virtual-display and recovery evidence](release-evidence/2026-09-13-multi-output-recovery.md)
now covers three virtual outputs at actual 100%/125%/150% scales, output
disable/re-enable with explicit layout reconciliation, and a private Plasma
restart. The normal VM also passes one injected shell crash, an explicit
recovery-command restart and 60 seconds of stable layout/service checks.
The [automatic repair follow-up](release-evidence/2026-09-13-automatic-output-repair.md)
also passes the installed supervisor/helper path after output disable/re-enable,
with no manual repair after initial setup. Runtime/service-manager isolation
was checked before starting it; the normal session stays unchanged. Physical
hotplug/graphics drivers, normal service-manager interaction during output
changes, broader failure paths and final media remain open. The windowed
backend's ignored scaling and initial harness failure are preserved in the
evidence; they are not reported as successful mixed-DPI tests.

**Previous installed correction:** [Feed address validation](release-evidence/2026-09-13-gadget-feed-addresses.md)
rejects malformed/empty/non-HTTP addresses with visible feedback and no catalog
write. Five dialog failures were reproduced before correction; all eight source
and package groups now pass (135 gallery, 74 provider, 11 media Qt results).
Release 23 passes normal upgrade, native invalid-address/valid-retry/cancel/
reopen checks and normal logout/login with the correct autostarted binary.
Ordinary account layout is unchanged. Gadgets 23 is selected with KWin 7.3;
all 149 integration tests pass, along with hygiene checks for 18 online and
53 offline archives and identity/checksum checks for 35 offline repository
entries. Earlier release-22 selection below is historical. Final media and
broader acceptance remain pending.

**Previous native finding:** [Weather Find and feed management](release-evidence/2026-09-13-gadget-find-feeds.md)
release 21 upgrades normally and passes the native feed-save failure/retry,
empty-list and typed-URL checks. Weather preserves settings after an offline
failure, but its new error message is clipped. Three font-size regressions
reproduce this; release 22 passes all eight source/package groups (123 gallery,
74 provider, 11 media results), normal upgrade, the native unclipped-message
replay and normal logout/login with the correct autostarted binary. The account
layout is unchanged and desktop services have zero restarts/no failed units.
Gadgets 22 is selected with KWin 7.3; all 149 integration tests pass, as do
archive hygiene checks for 18 online and 53 offline archives and identity/checksum
checks for 35 offline repository entries.
Earlier release-20/21 notes below are historical. No final ISO has been built.

**Installed settings correction (release 20):** [Gadget Options](release-evidence/2026-09-13-gadget-settings.md)
now applies accepted Weather/Feeds refresh intervals immediately and preserves
the current puzzle on unchanged OK. All eight source/package groups pass (99
gallery, 74 provider, 11 media results). Release 20 upgrades normally; the native
replay verifies unchanged puzzle pixels, explicit New puzzle, saved/reopened
intervals and cancellation. Normal logout/login verifies the autostarted binary,
unchanged account layout and healthy desktop services. Gadgets 20 is selected
with KWin 7.3; all 149 integration tests and online/offline archive hygiene pass.
Earlier release-19 results below are history,
not the current package selection. The frozen ISOs remain unchanged.

**Earlier native media result (release 19):** [the installed comparison](release-evidence/2026-09-13-gadget-media-native.md)
reproduces stale covers, missing initial artwork, dim track text and skip arrows
sending PlayPause. Release 19 passes all eight source/package groups (71 gallery,
74 provider and 11 media results), the installed artwork/readability/button
replay, actual VLC pause/resume/next/previous behavior and normal-login binary/
autostart verification. The ordinary layout is unchanged and desktop services
have zero restarts/no failed units. Gadgets 19 is installed and selected with
KWin 7.3 after the full 149-test integration and online/offline package hygiene
checks pass. Broader tests remain open.

**Earlier artwork checkpoint:** [Media Center artwork tests](release-evidence/2026-09-13-gadget-media-artwork.md)
reproduce seven stale/invalid-cover failures while metadata and player commands
pass. The source correction passes all ten media results and all eight gadget
groups. Gadgets 18 builds and passes all eight package-check groups; its
installed stale-cover check subsequently passes as recorded above. Selected
Gadgets 17 does not contain that correction.

**Earlier package checkpoint (superseded by release 19 above):** the [13 September alignment](release-evidence/2026-09-13-gadget-compositor-package-alignment.md)
selects the normally built and VM-tested Gadgets 17 / KWin 7.3 archives. All
149 project tests, selected-package checks and online/offline archive hygiene
pass. Counts remain 18 archives / 16 required / 2 optional, with the Shell pin
unchanged. Earlier selection and pending-build statements below are historical
checkpoints, not the current package list. No final ISO has been built.

**13 September Show Desktop result:** KWin 7.2 builds, upgrades and passes the
corrected cold-boot running-process/library audit. The unit MainPID is its
launcher, so the strengthened audit verifies both launcher and actual compositor
child. The installed visibility replay now keeps gadgets visible, but a timed
capture catches Calendar staying above restored applications until its next
refresh. Four isolated layer-update regressions fail before the gadget-side
correction; all 47 gallery results pass afterward. Gadgets 15 builds, upgrades,
passes the installed timed replay and normal-login autostart/binary audit with
the account layout unchanged. A new popup check still restores hidden apps when
right-clicking Calendar during Show Desktop. The
[popup correction](release-evidence/2026-09-13-gadget-popup-membership.md)
reproduces two failures before the change and passes all 76 layer-shell results
afterward. KWin 7.3 now builds, upgrades and passes the normal reboot
running-library audit. Its installed root/submenu/dismissal replay retains
Show Desktop until the user explicitly restores applications. The checked
menu indicator [correction](release-evidence/2026-09-13-gadget-menu-indicators.md)
now passes the before/after three-style matrix, all seven gadget groups, normal
Gadgets 16 upgrade and native root/Size/Opacity checkmark replay under Kvantum.
Normal-login autostart and running-binary checks pass with the account layout
unchanged. Selecting opacity exposes a separate failure: Wayland rejects the
window-opacity request and the gadget remains opaque. This is subsequently
corrected in Gadgets 17 as recorded below. Next-build package selection is
completed by the alignment above. See the
[Gadgets 15 results and remaining menu findings](release-evidence/2026-09-13-gadget-layer-update.md) and
[evidence and preserved harness failure](release-evidence/2026-09-12-gadget-show-desktop.md).

The KWin package resume failed at linking after an earlier interruption left
two zero-byte object files. Those exact generated files are preserved, and an
incremental recovery recompiles them with unchanged recipe/hardening. Recovery
completes successfully; the package audit preserves all 2,256 paths and checks
63 ELF files. The [opacity correction](release-evidence/2026-09-13-gadget-opacity.md)
reproduces nine baseline failures at each of 100%, 150% and 200% device-pixel
ratios, then passes all eleven results at each scale. All seven gadget test
groups pass, including 61 gallery and 74 provider results. Gadgets 17 builds,
upgrades normally and passes native transparency, drag-preview and restart
pixel checks on KWin 7.3. Normal logout/login verifies the exact autostart
binary, unchanged account layout, zero desktop-service restarts and no failed
units. Neither new package is in the frozen ISOs.

A separate installed Gadgets 16 keyboard check opens Size by pointer motion,
then selects Large with Down/Return. The selection saves, but menu teardown
crashes the private host (SIGSEGV, exit 139). The retained stack and candidate
style-lifetime correction are in the
[menu evidence](release-evidence/2026-09-13-gadget-menu-indicators.md#additional-keyboard-teardown-crash).
The failure reproduces again on KWin 7.3 before the gadget upgrade, then the
same Size keyboard sequence and a second Opacity keyboard sequence pass with
Gadgets 17. The offscreen keyboard matrix passes before and after, so it does
not reproduce the native crash; the installed comparison supplies that evidence.
Broader gadget, scaling/multi-monitor, recovery and final-media checks remain
open. The build manifest now selects Gadgets 17 and KWin 7.3 after the complete
project checker passes; frozen images still contain their older packages.

**Installed Gadgets 14 desktop replay:** the
[paired desktop/puzzle check](release-evidence/2026-09-12-gadget-desktop14-replay.md)
reproduces the Show Desktop failure on the old compositor and verifies native
3×3 puzzle valid/invalid moves and small/large resize retention. Reversing the
move and resizing back restores the original board pixels. This does not cover
complete-game behavior or all difficulties. The normal KWin 7.2 package build
was still running at that checkpoint; its prepared source tree exactly matches the tree that passed
the 72-result controlled compositor suite.

**Slideshow playback finding:** a
[native damaged-file replay](release-evidence/2026-09-12-gadget-slideshow.md)
confirms that one invalid picture can freeze playback while an otherwise
identical control keeps advancing. The before-fix gallery run reproduces six
failures; the bounded image-skip/transition/delay correction passes the complete
43-result gallery run. Gadgets 14 builds, upgrades normally and passes the same
installed damaged-file replay plus native pause/previous/next/resume checks.
Its normal-login running-binary/autostart audit passes, with the account layout
unchanged. Broader gadget and compositor gates stay open.

**Earlier 12 September Show Desktop checkpoint (superseded above):** the
[12 September compositor follow-up](release-evidence/2026-09-12-gadget-show-desktop.md)
finds two distinct causes. Gadgets 13 fixes malformed Wayland permission values,
passes seven component groups and normal upgrade/login checks, but still fails
native visibility. The corrected trace proves that Show Desktop events and
layer commits work; KWin still hides the custom gadget surfaces as ordinary
windows. A scoped desktop-membership patch fixes the two failing native
compositor regressions; its full layer-shell suite passes 72 results. The normal
compositor package build and installed-VM validation remain pending, and
Gadgets 10 remains selected for media.

**Current gadget request/feed source pass:** the
[12 September regression record](release-evidence/2026-09-12-gadget-query-feed-validation.md)
reproduces and fixes mixed weather replies, superseded requests overwriting
newer data, old values surviving query changes, feed parsing/cache failures and
incorrect feed click targets. All 74 provider and 34 gallery Qt results and
five CTest groups pass. Gadgets 11 builds and upgrades normally, passes native
cached/empty/error-feed and weather-instance checks, and passes normal-login
running-binary/autostart verification. A subsequent normal-session test
reproduces gadgets disappearing during Show Desktop; that follow-up remains
open. The manifest still selects Gadgets 10. No final ISO or publication is
approved.

**Previously installed gadget provider/puzzle pass:** the
[10 September validation record](release-evidence/2026-09-10-gadget-provider-validation.md)
adds strict response/cache validation, preserves genuine zero readings, omits
invalid forecasts, reports failed refreshes with valid cached readings retained,
and fixes Picture Puzzle difficulty resetting. Installed Gadgets 10 also shows
readable cached-data labels in both sizes. All five component test groups
(52 provider and 23 gallery Qt results), normal upgrades, a normal-login running
binary/autostart audit and the full 149-test
integration checker pass. The local manifest now selects Gadgets 10; the
18/16/2 archive/required/optional counts and Shell pin are unchanged. Live
provider success, request-identity races and remaining desktop gates stay open.

**Gadget Gallery follow-up:** an [installed isolated-profile replay](release-evidence/2026-09-09-gadget-gallery.md)
reproduced unreadable unselected labels with a dark palette and an unintended
website action when Return adds a gadget. Installed Gadgets 4 passes native
readability, Return/keypad Enter, add/remove and layout restoration checks.
That replay exposed faulty Wayland dragging. Candidate 5 passes its build but
fails native pointer tracking and is rejected for next-build selection. The
stationary-input/transparent-preview revision builds as Gadgets 6, upgrades
normally and passes five native body/handle drag gestures with exact final
coordinates, a held-button preview check and restart persistence. The
[10 September runtime follow-up](release-evidence/2026-09-10-gadget-runtime-followup.md)
verifies release 6/8 normal-account autostart and all-nine-gadget add/render
checks. Release 8 additionally passes installed preview scaling/alignment,
honest unavailable-weather display and Calendar week-start persistence. It is
selected with KWin 7.1 in the next-build manifest: 18 archives, 16 required,
two optional, with the complete 149-test checker passing. Broader gadget
provider/settings and scaled/multi-monitor workflows remain open.
Clean profiles stay empty; no icon or artwork changes were made.

**Current unsaved-work hold:** [Paint Cancel leaves a forced-logout countdown](release-evidence/2026-09-09-unsaved-work-logout.md).
The separate Cancel Logout action preserved the test drawing. A KWin candidate
removes the unconditional timer and passes its structural source guard and full
package build; all 63 ELF paths retain their direct library requirements. Normal
offline upgrade passes with all package files and the original capability
present. Normal reboot/password login and the running compositor hash also
pass, with zero failed units at that snapshot. The same session/compositor/Paint
survived 219.24 seconds beyond the document-cancel marker, and the saved PNG
matches all 120,000 original pixels. Cancel Logout, notification dismissal and
repeated requests pass. Saving/closing the last pending app returned to SDDM;
the next login has a new session and no failed units. Explicit Log Out Anyway
also returns to SDDM; its disposable unsaved Paint exits during compositor
shutdown, as recorded rather than treated as a clean app close. New-session
checks pass. Normal Start-menu power-off, confirmed QEMU exit, cold start and
password login also pass with the exact running candidate binary; the retained
shutdown journal has no stop timeout in that sequence. KWin 7.1 is now in the
local next-build selection, as recorded in the runtime follow-up above. The
ordinary lifecycle results below do not cover this failure path.
The follow-up controlled-flow suites pass 11 enabled and six no-notification
Qt results after also fixing reentrant notification cleanup. These supplement,
not replace, the native evidence and remaining installed-package checks.

Earlier integration baseline: [next-build package alignment](release-evidence/2026-09-09-next-build-package-alignment.md)
selects Desktop 32, Explorer 54, Control Panel 53, Theme 57, Paint 9, optional
Programs Center 3, Spectacle 3, Qt Base 6.11.2-3.1, UAC 2 and optional Vault 6.
All 17 archive integrity/ownership checks and the full 149-test project checker
pass, including versioned dependency and optional-feature isolation checks.
This supersedes older next-build selection statements below, not their historical
VM evidence. The subsequent [combined offline transaction and reboot](release-evidence/2026-09-09-aligned-stack-offline-validation.md)
passes all 15 required packages together without dependency/conflict overrides,
post-reboot package/service checks and all 59 installed Explorer dialog results.
The vault stays absent and disabled; the native optional-features list reflects
that state. This is an upgraded guest, not a new ISO or fresh installer replay.

Latest [installed Qt, Action Center and Spectacle checks](release-evidence/2026-09-08-portal-installed-validation.md)
pass normal offline upgrades/reboots, eliminate the reproduced duplicate portal
registrations in the observed cold login/restart, and verify actual region saving
plus pixel-exact clipboard retention across helper exit/restart. Notification
body/thumbnail clicks opened the actual saved images in the default viewer,
and real Ctrl+V into Paint preserved all screenshot pixels through a native
Save dialog. That replay exposed an initial filename-focus defect: five new
cases fail before its source fix and pass after, with all 59 common-dialog
checks passing. [Explorer 53](release-evidence/2026-09-08-dialog-initial-focus.md)
then built, upgraded normally and passed actual keyboard-only Save As/Open.
The later [Theme 53 and Explorer 54 pass](release-evidence/2026-09-08-panel-shadow-and-explorer-metadata.md)
fixes the missing panel shadow properties and Explorer homepage metadata.
Both packages built and upgraded normally. A cold-login audit no longer finds
the four panel warnings; all 59 installed Explorer dialog cases pass on Wayland.
The direct metadata validator now runs rather than relying on ECM's skipped
check. The subsequent [Theme 54 menu-launch correction](release-evidence/2026-09-08-detached-menu-launch.md)
fixes the detached application's inherited output-pipe lifetime. Four launch
regressions fail before the change and pass afterwards, including a separate
no-journal fallback suite. The complete package built and upgraded normally;
actual Taskbar Properties, Start Menu Properties, Explorer and Task Manager
menu actions passed. A normal reboot/password login and keyboard-only taskbar
Properties selection also passed. Region saving, notification opening and
pixel-exact image clipboard content passed again in that boot.
The following [online update pass](release-evidence/2026-09-08-online-update-recovery.md)
verifies real disconnected failure and same-window recovery, unchanged package
state after declining installation, administrator-approved full `pacman -Syu`,
successful post-transaction hooks, a no-repository-updates recheck and normal
reboot/password login. Control Panel 52 fixes two presentation defects found
during that replay: overbroad successful-install status and false AUR origin
labels for local packages. Its full build passes all 20 CTest suites, normal
upgrade passes, and actual installed update history shows the corrected labels.
This does not establish AUR installation acceptance or final-image readiness.
The [startup classification and tooltip follow-up](release-evidence/2026-09-08-startup-and-tooltip.md)
confirms the five metadata-warning helpers are running and distinguishes their
upstream harmless diagnostics from authentication and KWallet concerns. Four
tooltip lifecycle regressions fail before a typed-default correction and pass
afterwards. The subsequent [Theme 55 installed validation](release-evidence/2026-09-09-tooltip-installed-validation.md)
completes its full package build, normal upgrade, reboot and Wayland regression
replay. Real single/grouped previews, activation, closing and return to the pin
work. Its complete journal exposes a separate grouped-preview height binding
loop. The [Theme 56 sizing pass](release-evidence/2026-09-09-group-preview-validation.md)
then passes its complete build, normal upgrade, reboot, nine installed QtTest
results and real grouped-preview actions without reproducing that loop. The
16-window overflow replay exposes a separate undefined-variable error when
closing a row. The [Theme 57 follow-up](release-evidence/2026-09-09-overflow-row-validation.md)
then passes its full build, normal upgrade/reboot and all 11 installed QtTest
results. A real ten-window list activates and closes the selected window,
returns to nine live thumbnails and closes all remaining windows without the
reference error or sizing loop recurring. This closes those reproduced taskbar
findings. The subsequent [authentication service pass](release-evidence/2026-09-09-uac-service-validation.md)
fixes the duplicate UAC unit and broken disabled-selector fallback. Its normal
package upgrade, two cold-boot audits and real password-approval/cancellation
dialogs with both Aero and Plasma agents pass. Both unit names address one
active D-Bus-ready process; security policy and anti-debugging protection remain
unchanged. The candidate is not yet in the frozen images. Other keyboard
workflows and final-image gates remain open. The user has now approved an
optional encrypted Credential Manager, off by default and enabled through
Turn Aero7 features on or off. Its local implementation and package candidates
are being tested; this policy decision is resolved, not a completed acceptance gate.
Earlier progress observations below are historical, not the current test result.

The [Programs Center layout and Paint identity follow-up](release-evidence/2026-09-08-programs-home-and-paint.md)
records the latest normally installed component fixes, exact package hashes,
Wayland regression results and 1920×1080 screenshots. These packages have not
yet been promoted into the frozen images; do not advertise them as shipped.

The [offline recovery and screenshot follow-up](release-evidence/2026-09-08-offline-recovery-and-screenshots.md)
adds actual administrator-approval cancellation, removal with existing settings
retained, damaged-bundle rejection and same-window Try Again recovery. Offline
region capture, pixel-preserving clipboard paste, notification opening and
confirmed-overlay cancellation also passed. These are bounded acceptance
results, not permission to remove the release hold.

Latest component follow-up: the
[Explorer 49 storage-recovery correction](release-evidence/2026-09-08-explorer-storage-recovery.md)
reproduced two callback failures and passes all 20 source test suites after
the fix. Its normal package upgrade, installed dialog/Paint checks and a real
busy-drive failure followed by recovery in the same Explorer process also
passed in the modified offline VM. That replay exposed a drive-label
inconsistency after failure, subsequently corrected in Explorer 50 below. Do not describe this as
included in the final ISOs or as complete USB-device acceptance.

The [Explorer 50 breadcrumb follow-up](release-evidence/2026-09-08-breadcrumb-refresh.md)
reproduces and corrects the model-refresh cause of that label inconsistency.
All 20 source test suites, the package build, normal upgrade, installed
dialog/Paint checks and the actual busy/retry replay pass. The drive label
survives the failure, and the added `lsof` helper names the blocking process.
The next-image manifests now select Explorer 50, Desktop 29 and Plasma
Workspace 6.7.4-3.2; `lsof` is in both installation variants' base package
list and the offline bundle. Input validation passes. Both r10 candidates
have now been built and verified with this selection.
Both completed fresh installation, OOBE and first-reboot password login.
The broader desktop, recovery and compatibility acceptance gates remain open.
The [installer input-contract follow-up](release-evidence/2026-09-08-installer-explicit-inputs.md)
resolves the 150 unqualified QML warnings without weakening lint. The full
project checker now passes, including all 142 Python tests and ShellCheck.
All three CTest suites pass; the UI tests exercise all 20 screens in both
directions at 1024×768 and 1920×1080, plus navigation and help dialogs.
The Welcome capture is pixel-identical to the earlier local build. These are
local build/simulation results, not new ISO installation acceptance.
The [approved-icon follow-up](release-evidence/2026-09-08-installer-approved-icons.md)
replaces the two warning-producing SVGs with unchanged check-mark and Recycle
Bin artwork from the selected AeroThemePlasma pack. The stricter UI suite now
passes all 20 cases with no warnings, and the Python suite has 144 passing
tests including icon provenance/resource checks. Updated online/offline r10
profiles are prepared and their embedded frontend, manifests, package hashes
and notices verified; profile preparation is not ISO acceptance.
Both r10 exports passed their checksums and full embedded-content checks,
including both retained icon notices. The build job completed successfully.
Neither image is accepted for download until fresh installation testing
finishes successfully.
Both fresh r10 VMs have now completed GUI installation, first-run setup,
normal reboot and password login without repair. The offline VM had no network
adapter throughout. Both first-session package/system audits and IPv4/IPv6
Public firewall packet tests passed. The online clock synchronized automatically;
the disconnected offline clock correctly remained unsynchronized. Application
workflows, user-service warnings and optional-feature cycles still need broader
coverage; this is not release approval. The fresh online screenshot pass now
confirms region-release saving, notification opening, actual Ctrl+V into Paint
with zero pixel differences after saving, confirmed-overlay cancellation and
four backend save/error cases. Offline replay, rapid-input timing and full
failure/Try Again UI remain open. The original explicit-terminal-font proposal
was withdrawn because it left a startup warning. The later Desktop 30
[generic monospace correction](release-evidence/2026-09-08-terminal-font-default.md)
passes all eight source/package test suites and four installed Wayland terminal
profiles without that warning, preserving explicit user font choices. Normal
taskbar launch, reboot/password login and the post-reboot terminal check also
passed. This package is not yet in the frozen ISOs; final-media checks remain.
The fresh disconnected r10 VM also passed Programs Center's optional
install/open/remove/reinstall cycle, with administrator authentication and
the bundled package only. Cancelling the initial confirmation changed no
packages. Programs Center presentation issues and broader failure paths
remain open; its optional status in the ISO has not changed.

The following area summary is historical. Its package versions and pending
statements describe earlier checkpoints; newer reports above and the pre-build
checklist identify what has since been tested and what is still open.

| Area | Verified evidence | Still required before release claims |
| --- | --- | --- |
| Online and offline installation | Both r10 images passed embedded-content checks, fresh installation, first-run setup, normal restart/password login and package/system/firewall audits. The offline guest had no network adapter. | Complete the remaining application, optional-feature, recovery and compatibility checks on these exact candidates. |
| Updates and firewall | Update checks can be disabled/enabled; installs require approval. The r10 offline VM passed OFF/Cancel/relaunch, manual disconnected error reporting, ON and reboot persistence. Approval-decline regression tests passed for repository/AUR updates in its Wayland session. Fresh installs use firewalld; earlier existing-UFW upgrade checks preserved 20 checked files and active/enabled state. Real IPv4/IPv6 Public-profile filtering passed. | Complete online transactions and final-image compatibility/failure/shutdown coverage. Do not claim automatic sharing or security-only upgrades. |
| Clock and setup | r9 online synchronized automatically; disconnected offline correctly stayed unsynchronized. Home profile, update preference and time service survived restart. Control Panel 50 passed 18 test groups and installed offline-VM server-retention checks. Installer regional-preview corrections passed 3 test groups; backend suite now passes 135 tests, including repeat-run and precisely prebranded lock-screen handling. | Control Panel 50 and the later installer fixes are not on the immutable r9 images. |
| Paint and shared dialogs | Explorer 36/Paint 7 upgraded normally; installed native PNG Save/Open preserved every pixel and closed normally. Paint 8 retains explicit preferences and defaults fresh profiles to one document window. Five installed Wayland workflow tests passed, including unsaved save/discard/cancel. | Tests used an upgraded VM and isolated profiles, not fresh corrected media. Remote browsing retains a KIO fallback. |
| Search and Organize | Explorer 37 built and upgraded normally. All 19 source test groups passed; all 29 functional dialog cases passed on the installed Wayland VM. Paint 8's five compatibility workflows passed again. Manual Open-dialog checks confirmed search, filtering, Organize, List layout, clearing and normal closure. | Final media; remaining common-dialog layout and file-operation parity. Search and ordinary folder views still use different image icons from the same approved pack. |
| Drive and breadcrumb consistency | Explorer 50 is built, selected and normally installed in the modified offline VM. All 20 source groups passed; installed dialogs passed 47 functional cases and Paint 8 passed five workflows with unchanged preferences. The actual 1920×1080 busy-drive replay preserves the breadcrumb label, names the blocker and recovers Home after successful retry in the same process. Earlier component reports retain the split/tab/history checks. | Multiple simultaneous native requests, external-request reconnection, physical/optical devices, broader selection-state behavior and final media remain pending. Do not advertise persistent Windows drive-letter assignment, complete storage management or complete graphical acceptance. |
| Login and lock-screen branding | Theme 46 retains the approved Welcome artwork and white lock-button label, and fixes the targeted SDDM anchor/layout and missing keyboard-layout warnings. All 15 package test groups, 10 isolated Qt 6 runtime cases and the branding archive checks passed. Normal offline-VM upgrade and reboot passed; the real user-list/password flow and complete login/lock-screen logo were checked at 1920×1080. All 1,143 theme files matched the package. | Full-Shell reapplication, broader greeter/accessibility/multi-layout testing and fresh final-media checks. Other startup warnings remain. No new artwork or icon pack was introduced. |
| Desktop startup and appearance recovery | Desktop 28 separates live layout repair from appearance reloads. Its seven source/package test groups, normal upgrade, three repairs without a shell restart and reboot checks passed. Local Plasma Workspace 3.2 now also passes the isolated splash regression, normal offline-VM upgrade, cold login and dark/light reloads observed for 80 seconds each without late splash activation. The taskbar, Explorer shortcut and a visible notification were checked afterwards; Aero7Light is restored. | These are modified-VM results, not final ISO acceptance. Other startup/QML warnings, multi-monitor/recovery stress tests and both final images remain pending. Do not claim the entire desktop is bug-free. |
| Screenshots | Online and offline region capture saved PNGs without opening the editor; notification clicks opened the saved image; actual Ctrl+V into Paint preserved every pixel. Confirmed-overlay Escape cancellation passed on both. Both guests passed background save/error probes. Later installed packages fixed the reproduced notification, early-cancellation, recovery and clipboard-lifetime defects; bounded evidence follows below. | Complete final-media acceptance and remaining multi-monitor/concurrent-input cases. Do not describe the frozen r10 images as containing the later fixes. |
| Optional Programs Center Beta | Fresh r10 offline install/open/remove/reinstall passed with no NIC. Later Programs Center 3/Paint 9 fixes passed five build suites and three Wayland layout replays. Actual approval cancellation changed no packages/settings; release-3 removal preserved the existing configuration; a damaged bundle was rejected without package changes; the same dialog's Try Again installed the verified release-3 package and restored the exact baseline package list. | Keep it optional. These newer packages are not yet in the frozen ISOs. Test broader application/transaction behavior and final media; the configuration-retention check is not proof about every possible user's data. |

**Known limitations and wording restrictions**

The [early screenshot cancellation follow-up](release-evidence/2026-09-08-snipping-early-cancel.md)
records both initial passing source runs and a later failure: the normally
installed theme-48 package missed Escape at 1,250 ms during focus handoff.
Release 48 is held and is not selected in the release manifests. Release 49
subsequently passed eighteen installed timing attempts across a normal reboot,
PNG saving, notification-click opening and real image paste into Paint. However,
a forced-crash test showed that its Escape registration survives the crash and
breaks cancellation after restart, so release 49 is also held.
The [installed release-50 correction](release-evidence/2026-09-08-snipping-installed-recovery.md)
clears only its own stale registration and installs automatic crash recovery.
The normal package passed forced crash/automatic restart, four post-crash
timings, queued-request cancellation, ten repeated timings, PNG saving,
notification opening, real image paste after cancellation, a normal reboot,
four post-reboot timings and an existing-Escape collision test. This closes
those reproduced recovery defects, not every possible timing or monitor case.
A separate [empty app-ID portal correction](release-evidence/2026-09-08-snipping-portal-identity.md)
passed positive registration in the source-candidate VM test. Its full release-51
package built with 18 passing test groups and ten greeter cases, then passed
normal installation, forced-crash recovery, four post-crash timings, normal
reboot, four post-reboot timings, saved notification, viewer opening and real
image paste. Cold login still logs a distinct duplicate-registration warning;
that lifecycle issue remains under investigation. Both final images still
need the corrected packages and end-to-end verification. Do not claim
that the frozen r10 images contain these fixes or that all cancellation races
are resolved.

The [clipboard-lifetime follow-up](release-evidence/2026-09-08-snipping-clipboard-lifecycle.md)
reproduces image loss after stopping the installed helper. The corrected source
uses Spectacle's explicit-image handoff and passes exact pixel comparisons
before producer exit, after exit and after normal-service restoration. Package
52 passed its full build, normal installation and reboot, then repeated those
pixel comparisons, saved-notification/viewer opening and four Escape timings
without losing the clipboard image. Final-media checks remain pending. The
separate portal warning is now traced to duplicate registrations from one client
during portal activation. A [Qt registration candidate](release-evidence/2026-09-08-qt-portal-registration.md)
passes eight isolated D-Bus regression scenarios, each repeated five times;
unmodified Qt fails seven of those scenarios. Full-library packaging is now
complete; installed-VM checks are still pending. A separate Action Center identity and hidden desktop
entry correction is packaged in Control Panel 51 with all 19 test groups passing;
VM verification remains pending. Neither correction is in the frozen ISOs.
Do not extend these bounded comparisons into a promise about every crash or logout.

Full Qt packaging has now [completed in the isolated builder](release-evidence/2026-09-08-portal-package-builds.md).
All eight package regression scenarios passed. The candidate preserves all 67
shared libraries' exported symbol records, all 88 ELF direct-library requirements
and the complete header/shared-asset trees. The builder shut down normally and
the existing offline QA guest resumed for installed testing. This is not full
C++ ABI or installed-desktop acceptance.
Control Panel package 51 completed with all 19 package test groups passing and
unchanged direct library requirements; its Action Center correction still needs
normal installation and VM checks. These package-build results are not final-media
acceptance and must not be advertised as available in the frozen r10 downloads.

A separate [Spectacle toolbar-focus correction](release-evidence/2026-09-08-spectacle-toolbar-focus.md)
is packaged as Spectacle 3. Four real QML-component tests pass, and a bounded
offscreen application-startup comparison reproduces the original focus-property
warnings only in the baseline. Normal toolbar buttons retain their focus policy
without adding a focus stop to their containers. Installed-VM capture, keyboard
and reboot checks remain pending; this package is not in the frozen r10 images.

The later [native-dialog breadcrumb candidate](release-evidence/2026-09-08-common-dialog-breadcrumbs.md)
replaces the normal internal library path with clickable library/folder
breadcrumbs and subfolder menus. Explorer 51 passed all 20 package test groups,
a normal offline upgrade, 51 installed Wayland dialog checks and five Paint
document workflows. Real Paint navigation and Ctrl+L/Escape were also checked
at 1920×1080 using the source candidate. Normal reboot/password login, package
file checks and the taskbar Explorer launch passed afterwards. Final-media
acceptance remains pending; this package is not in the frozen r10 images. Do not announce it as
already shipped.

A subsequent [long-path and scaling correction](release-evidence/2026-09-08-dialog-overflow-scaling.md)
keeps complete breadcrumb buttons visible, provides a parent-folder overflow
menu, and accommodates larger fonts. It passed 20 local test groups, 54
Wayland dialog checks, and focused 150%/200% scaling checks. A normal-profile
1920×1080 replay confirms the long-label layout. This correction is now packaged
as Explorer 52: all 20 package test groups, a normal offline upgrade, 54 installed
Wayland dialog checks and five Paint workflows passed. Normal reboot/password
login, the installed library hash, package-file checks and the taskbar Explorer
shortcut also passed. Final-ISO acceptance remains required: Explorer 52 is not
in the frozen r10 images. Keep it in preparation notes, not shipped claims.

The [subsequent virtual-USB replay](release-evidence/2026-09-08-dialog-usb-recovery.md)
passed native discovery/mounting, mounted-drive breadcrumbs, unavailable-save
and New Folder protection, disconnect/reconnect discovery and keyboard remount.
The filename was preserved throughout; cancellation and safe detach left the
entire test image byte-for-byte unchanged. This narrows the removable-device
gap for the candidate, not physical-device or final-media acceptance.

- The frozen media route Credential Manager to User Accounts. New Control Panel
  53 and Desktop 32 candidates add an optional, off-by-default encrypted vault
  and disabled-wallet portal policy. The [vault validation record](release-evidence/2026-09-09-optional-vault-validation.md)
  records native setup cancellation fixes, password-protected storage, editing,
  actual lock/wrong-password/reopen checks, and removal with byte-identical
  retained data. Desktop 32 additionally fixes the runtime portal policy's KDE
  identity after a disabled boot exposed the mismatch. Candidate builds and
  normal upgrades pass. The [Vault 5 failure-path follow-up](release-evidence/2026-09-09-vault-lock-recovery.md)
  fixes missed external-lock signals and unavailable backend reactivation.
  New isolated D-Bus tests and native VM replays verify editor dismissal and
  last-saved-value recovery without restarting the desktop. The subsequent
  [Vault 6 verification pass](release-evidence/2026-09-09-vault-lock-verification.md)
  fixes the uncertain-lock state transition and passes its full package build,
  normal upgrade, and a native two-window lock/editor-dismissal replay.
  Remaining broader
  lifecycle/release gates are listed in those records. These packages are not
  in the frozen images.
- The [combined-stack lifecycle replay](release-evidence/2026-09-09-session-lifecycle-validation.md)
  passes wrong-password lock-screen feedback and valid retry, native logout/login,
  native power-off and a new power-on/password login. No Plasma stop timeout
  recurred, with zero failed units and zero shell/agent restarts at the recorded
  snapshots. The older intermittent timeout remains unproven fixed; unsaved-work
  inhibitors, suspend and broader lifecycle conditions are not covered by this pass.
- Setup still records package-origin/Plymouth warnings. Theme 46's targeted
  SDDM layout/keyboard warning fixes passed the reboot check, but full Shell
  reapplication and other UI issues need review. Desktop 28 removes the
  unnecessary login-time shell restart; its normal-boot timeout check passed.
  The separate late KSplash activation has a tested local correction in Plasma
  Workspace 6.7.4-3.2; final-image confirmation remains required. Do not advertise the system as bug-free,
  warning-free or perfectly identical to Windows.
- Do not promise unattended installation, a fully translated Dutch interface,
  telemetry, or seamless live icon/theme upgrades. Advise signing out and back
  in after icon/theme updates.
- Final 1920×1080 screenshots, package signing/promotion where required, owner
  approval and website hosting are still release gates. Nothing is published.

### Technical evidence history

The entries below describe earlier checks and discoveries. Use the current
selection and status above for website claims; older candidates are not the
downloadable release.

The [native-dialog package/VM report](release-evidence/2026-09-06-native-dialog-packages.md)
and [search regression report](release-evidence/2026-09-06-common-dialog-search.md)
contain the detailed current component evidence. Older iteration histories
remain in the reports below, not in visitor-facing release copy.
The [drive consistency report](release-evidence/2026-09-06-explorer-drive-consistency.md)
tracks the later source changes and their separate packaging/VM gate.
The [Computer/sidebar follow-up](release-evidence/2026-09-06-explorer-computer-sidebar.md)
records Explorer 39 source and installed-package checks, including the history
failure discovered during the longer VM sequence.
The [Computer history correction](release-evidence/2026-09-06-explorer-computer-history.md)
records r40 source and installed-VM results, including the remaining tab-strip
visibility defect. The [Computer tab correction](release-evidence/2026-09-07-explorer-computer-tabs.md)
records r41 source tests, isolated test-profile repair, installed package/VM checks
and the two remaining split-view layout defects.
The [split-view correction](release-evidence/2026-09-07-explorer-split-layout.md)
records r42's red/green regression evidence and all 19 passing source test groups;
its package and targeted installed-VM checks passed, while the deeper sequence
exposed the separate missing item-count defect recorded there.
The [details-state correction](release-evidence/2026-09-07-explorer-details-state.md)
records r43's two red regressions, all 19 passing source groups, normal upgrade,
installed dialog/Paint checks and the actual VM sequence that closes that defect.
The [repeat-branding correction](release-evidence/2026-09-07-branding-repeat-setup.md)
records the installer repeat-run failure and its passing regression. The
[theme ownership follow-up](release-evidence/2026-09-07-theme-branding-ownership.md)
records theme 45, the expanded 135-test backend suite, archive validation and
successful normal upgrade/reboot branding checks. Final media remains pending.
The [SDDM layout and splash lifecycle follow-up](release-evidence/2026-09-07-sddm-layout-lifecycle.md)
records theme 46's runtime regressions, normal upgrade, actual greeter/lock-screen
checks and clean targeted-warning reboot audit. It also distinguishes the
successful initial splash from the separate late activation timeout.
The [live layout repair report](release-evidence/2026-09-07-desktop-live-layout-repair.md)
records Desktop 28, the scoped trace identifying Plasma as the late caller,
normal upgrade/reboot results, dark/light recovery and the remaining caller fix.
The [Plasma caller correction](release-evidence/2026-09-07-plasma-splash-lifecycle.md)
records the verified upstream source and matching Arch recipe, the isolated
D-Bus regression tests (including ten consecutive passing runs), and the clean
installed-VM baseline. The first full package built and upgraded normally, but
failed graphical acceptance: an undeclared Flatpak library dependency prevented
the taskbar and notification applets from loading. The VM was rolled back and
the taskbar returned after reboot. Corrected package 3.2 has built and upgraded
normally; all 152 binaries match the original direct library requirements and
the guest's affected applet plugins resolve their runtime libraries. Cold login
and both dark/light reload observations now pass beyond 80 seconds, with no late
splash activation. File Explorer launches from its taskbar pin and a notification
renders after restoring light mode. Keep release-wide claims on hold; neither
final ISO contains this fix and other warnings still require triage.
The [live mount refresh investigation](release-evidence/2026-09-07-storage-live-refresh.md)
records two later Explorer 43 findings: a stale Computer tile after unmount and
a 16 MiB filesystem incorrectly displayed as zero GB. Explorer 44 now packages
capacity formatting, live mount-table refresh and unavailable Save/New Folder
destination protection. It also fixes a clipboard event arriving before the
first folder opens. All 20 source groups pass, including a three-repeat run;
the normally upgraded offline VM passes all 39 functional shared-dialog cases
and Paint 8's five workflows. Two QA-harness issues were diagnosed and corrected
(duplicate native message-box counting and a fixed-delay confirmation check);
the original failures remain recorded. The ordinary installed Computer window
also passed a live temporary-volume cycle: it added the drive automatically,
displayed 16 MB correctly and removed the tile after unmount without Refresh.
Physical USB/eject, open-dialog unmount testing and fresh final media remain
open at that stage. Package 44 was a local QA candidate, now superseded by 50;
do not claim complete storage or final-media acceptance.

The later [USB and dialog-navigation follow-up](release-evidence/2026-09-07-usb-discovery-and-dialog-navigation.md)
uses a newly created virtual USB filesystem through UDisks/Solid. Mounted naming
and capacity agree between Computer and the sidebar; an actual unmount disables
Save and blocks New Folder while retaining the filename. It also found remaining
defects: unmounted drives are hidden, cached file rows survive unmount, and dialog
navigation can require double-click or accidentally trigger Save with Enter.
These corrections and native sidebar storage actions are now built into the
local Explorer 45 candidate, with all 20 source test groups passing. A normal
offline VM upgrade passed with Paint and its preferences unchanged. The first
45 check still found the unmounted USB device missing from the sidebar. Its
backend-policy correction is now installed as Explorer 46: the unmounted drive
appears, and a single sidebar click mounts it and opens its files. In 45, right-click
Safely Remove does work on the mounted virtual USB fixture: Explorer returns
home and UDisks confirms unmount, cache synchronization and power-off.
The [Explorer 46 installed validation](release-evidence/2026-09-07-explorer46-installed-storage.md)
also passes 45 functional shared-dialog cases and all five unchanged Paint 8
workflows. A real USB unmount while Save As is open hides stale files, disables
Save, blocks New Folder and preserves the filename; one click on Documents
restores the dialog. Explorer 47 now closes the next two gaps in the existing
offline VM: unmounted drives appear and open through native setup in Computer
and Save As, and external unmount returns the main Explorer view home. Keyboard
Enter also remounts the drive from Save As without accidentally saving. Its
20 local suites, 47 installed functional dialog cases and five unchanged Paint
workflows pass. See the [Explorer 47 storage-surface report](release-evidence/2026-09-07-explorer47-native-storage-surfaces.md).
These are modified-VM checks, not final-media acceptance. Native cancellation,
denied/busy-device failure, physical/optical media, multiple-drive behavior and
common-dialog address presentation still need checking or work. Nothing here is published;
keep complete USB support and release-wide claims on hold.

The [Explorer 48 and Desktop 29 follow-up](release-evidence/2026-09-07-explorer48-desktop29.md)
now verifies removable-drive breadcrumbs in the main Explorer window, including
nested folders, clicking the drive root, switching to C: and returning with Back.
All 20 Explorer source suites, 47 installed functional dialog cases and five
Paint workflows pass. Desktop 29 also supplies the missing hidden identity for
the existing Baloo indexer: an actual-worker A–B–A test identified the portal
registration cause, and three installed-package launches now pass without that
specific warning. The upgrade preserved the shell process and indexing settings;
all seven Desktop package suites passed. This does not certify document indexing
or a warning-free desktop. Desktop 29 is now selected with Explorer 50 for
the next builds; both final-media test matrices remain required.

The [installed authorization and busy-drive checks](release-evidence/2026-09-07-storage48-authorization.md)
now cover cancelling real drive authorization, retrying successfully, keeping
Documents selected when a delayed mount completes, retaining a Save As filename
after cancellation and closing Save As during a pending mount without returning
a file. Busy-drive refusal displays an explanation in repeated checks, including
the normal uninstrumented app; removal succeeds after the blocking directory
references are released. The first silent attempt remains inconclusive, and
the then-missing `lsof` prevented the fallback warning from identifying the
blocking app. The Explorer 50 replay above verifies that capability after
installing the helper.
Temporary QA authorization policy and observer were removed; the final audit
confirmed clean packages, unchanged preferences and safe drive removal. Keep
the broader storage and final-media gates open.

Evidence and provenance:
[r9 corrected-media acceptance in progress](release-evidence/2026-09-06-r9-time-final-media.md),
[final r8 media checks in progress](release-evidence/2026-09-06-r8-final-media-acceptance.md),
[time synchronization checks](release-evidence/2026-09-06-time-synchronization.md),
[updater and UFW checks](release-evidence/2026-09-06-updater-error-paths.md),
[fresh-image firewall/OOBE history](release-evidence/2026-09-06-r5-fresh-image-acceptance.md),
[broader corrected-candidate report](release-evidence/2026-09-05-fixed-candidate-acceptance.md).
Existing [component previews](website-assets/beta2-qa-preview/README.md) and
[fresh r3 previews](website-assets/beta2-r3-qa-preview/README.md) are QA assets,
not approved final-image promotional screenshots. No release was published.
