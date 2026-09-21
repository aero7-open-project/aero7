# Pre-build requirement and website-claim review

13 September 2026. The review distinguishes functional bug fixes, historical
test results, incomplete presentation requirements and future final-image tests.
It does not turn documented limitations into fulfilled user requirements.

## Current selection and repeated checks

The manifest remains
`36d3c6a00f369ff6f86cfde5124e7b712fffebe8ad3b111ffb88dc862f543258`:
16 required packages and two optional packages. No runtime package changed in
this review. The [new integration run](prebuild-review-logs/integration.log)
passes all **153 tests**, package ownership/checksums, actual dialog-package
linkage, approved-icon checks, syntax, theme repeat-setup checks and ShellCheck.
The [online verifier](prebuild-review-logs/online.log) passes 18 archives; the
[offline verifier](prebuild-review-logs/offline.log) passes 53 archives and 35
repository-entry checks. Both verify release-note versions and optionality.
These are local tests, not published CI, signature verification or final media.

## Requirement-to-evidence map

| Requested area / website claim | Current evidence and exact boundary |
| --- | --- |
| Two ISOs; offline base installation without internet | [Frozen r10 installation report](2026-09-08-r10-current-stack-acceptance.md) records successful online and NIC-free offline install/OOBE paths. Those images predate the latest selection. Final images must repeat them. Offline is recommended because it avoids downloads, not because a fixed install duration was measured on every laptop. |
| Dedicated desktop, factory pins, production Recycle Bin-only desktop, explicit fallback | [Desktop source/profile checks](2026-09-13-desktop-source-cleanup.md), [current guest alignment](2026-09-13-selected-stack-alignment.md) and [live layout repair](2026-09-07-desktop-live-layout-repair.md). Diagnostic media intentionally adds the physical-install log folder. Do not present its screenshot as the production-only desktop. |
| Correct login/lock branding and no transient stock splash | [Theme branding ownership](2026-09-07-theme-branding-ownership.md), [SDDM lifecycle](2026-09-07-sddm-layout-lifecycle.md), [splash lifecycle](2026-09-07-plasma-splash-lifecycle.md) and current selected-package checks. This does not establish the full requested accessibility dialog; see the open finding below. |
| Explorer identity, Libraries/Computer, drive presentation and common dialogs | [Breadcrumbs](2026-09-08-common-dialog-breadcrumbs.md), [scaling/overflow](2026-09-08-dialog-overflow-scaling.md), [virtual USB recovery](2026-09-08-dialog-usb-recovery.md), [initial focus](2026-09-08-dialog-initial-focus.md), and [Explorer 54 concurrency](2026-09-13-dialog-concurrency.md). The latter passes 67 installed Wayland test results, including same/different caller IDs in one process; it is not two external processes or physical-device certification. Drive letters are presentation labels. |
| 45 applet names and five-column Control Panel | [Control Panel 55 native smoke/login](2026-09-13-control-panel-source-cleanup.md) observes the 45-entry view and optional-feature search policy. The catalog is entry-point parity, not 45 equivalent Windows services. |
| Working Linux-backed Screen Resolution and recovery | [Display correction](2026-09-13-display-rollback.md) covers drag/Apply, rollback result handling and native accepted/reverted scaling. Control Panel 55 retains the corrected runtime source. Physical GPUs and connector behavior remain untested. |
| Meta+Shift+S region → saved PNG → image clipboard → notification opens file, no editor | [Installed recovery](2026-09-08-snipping-installed-recovery.md), [early cancellation](2026-09-08-snipping-early-cancel.md), [clipboard lifetime](2026-09-08-snipping-clipboard-lifecycle.md), and [installed Qt/notification/Paint-paste replay](2026-09-08-portal-installed-validation.md). Clipboard pixels, file saving and notification activation are separate checks. Final images must contain and replay the fixes. |
| Gadgets, persistence, live providers and options | Later reports supersede earlier Gadgets 10/17 pending statements: [native media](2026-09-13-gadget-media-native.md), [settings preservation](2026-09-13-gadget-settings.md), [feed catalog recovery](2026-09-13-gadget-catalog-recovery.md), [slideshow options](2026-09-13-slideshow-options.md), plus current Gadgets 25 alignment. A working provider parser/cache is not perpetual availability of internet services. |
| Optional Programs Center, normal removal, retained configuration and offline retry | [Programs Center 3 / Paint 9](2026-09-08-programs-home-and-paint.md) and [later installed optional-feature failure/retry checks](2026-09-09-aligned-stack-offline-validation.md). The earlier frozen-image cycle used Programs Center 2 and is not relabeled. Additional software downloads still need connectivity. |
| Optional encrypted vault, off by default, enabled through Features | [Vault validation](2026-09-09-optional-vault-validation.md), [lock-state correction](2026-09-13-vault-lock-property.md), and [native overlap/content retention](2026-09-13-vault-native-prompts.md). It stores generic credentials, not whole-disk files; removal preserves the encrypted data. Native password-dialog appearance remains an ownership gap, not a cryptographic test failure. |
| Update checking toggle and approval before installation | [Preferences](2026-09-08-update-preferences.md) and [real online failure/recovery/approved full upgrade](2026-09-08-online-update-recovery.md). Turning checking off does not enable silent installation. Offline check failure reports unknown availability rather than claiming the system is up to date. |
| Fresh firewalld, existing UFW preserved, network-location behavior | [Approved defaults](2026-09-06-approved-defaults-and-cleanup.md), [r9 media/defaults evidence](2026-09-06-r9-time-final-media.md), the 22 firewall-default regressions included in the current checker, and current firewalld guest snapshots. The separate r4 UFW compatibility disk is protected, not deleted as redundant. No host firewall changed. |
| Date/time, selected region and time server | [Time synchronization](2026-09-06-time-synchronization.md), [r9 time/media evidence](2026-09-06-r9-time-final-media.md) and r10 online/offline time snapshots. Starting time synchronization is not evidence that an offline machine reached a server. |
| Session safety, unsaved work, multiple outputs and shell recovery | [Unsaved-work logout](2026-09-09-unsaved-work-logout.md), [selected KWin alignment](2026-09-13-selected-stack-alignment.md), [virtual outputs/recovery](2026-09-13-multi-output-recovery.md) and [automatic virtual-output repair](2026-09-13-automatic-output-repair.md). The old KWin integration-pending note is superseded; physical hotplug, suspend and every crash interleaving are not thereby tested. |
| Existing icon pack; no invented replacement artwork | [Owned-icon audit](../../../aero7-desktop/docs/AERO7-ICON-INDEPENDENCE-AUDIT.md), approved-asset checks in the current integration log and [retained source inputs](2026-09-13-retained-source-inputs.md). MIME/user-content/external-application artwork is distinguished from owned chrome. |
| Desktop logs and safe support guidance | Collector checks in the integration run and existing installation evidence. Logs can contain identifying information; the handoff requires review before sharing and forbids requesting passwords or publishing raw support archives. |
| Clean source distribution and preserved inputs | [Desktop 33](2026-09-13-desktop-source-cleanup.md), [Control Panel 55](2026-09-13-control-panel-source-cleanup.md), and all 95 declared [retained inputs](2026-09-13-retained-source-inputs.md). Reproducible source exports do not prove reproducible binaries or trusted signing. |

Older reports remain chronological evidence. In particular, their pending Qt,
Spectacle, Control Panel 51, Explorer 50, Gadgets 10/17, KWin integration and
vault-overlap statements must not be copied into current release status without
the later reports above. Conversely, newer upgraded-guest results must not be
written back as if they occurred on the old frozen ISO.

## Unfulfilled presentation requirements — not waived

The earlier Windows 7 request included a complete lower-left login Ease of
Access dialog with a desktop-environment tab at its bottom. The currently
selected SDDM implementation instead has a flat session-choice popup plus
On-Screen Keyboard. Inspection of
`aero7-desktop-workcopies/aerothemeplasma/plasma/sddm/sddm-theme-mod/Main.qml`
and the native SDDM screenshots confirms that distinction. The six requested
accessibility options and bottom tab are **not implemented by that popup**.
Branding and keyboard/layout tests do not close this requirement.

The earlier normal-session UI-ownership rule also rejects stock KDE-facing
dialogs. The real Vault 7 replay still displays **KDE Wallet Service** and
generic KDE request wording in its password prompt. That is direct visual
evidence against a blanket zero-visible-KDE claim. The vault's functional and
data-retention tests passed; they do not resolve this presentation gap.

These findings require implementation and native acceptance, or an **explicit
owner decision to defer them**. Merely mentioning them as limitations in the
website copy is not approval to omit requested work. Any correction must retain
working authentication, accessibility backends and wallet encryption rather than
introducing fake checkbox behavior or weakening security to alter appearance.
Other hardware/optional-service boundaries in the Control Panel parity guide
remain explicit; this review does not certify the entire historical Windows 7
parity specification.

## Website artifact and gate

The handoff has separate offline/online download cards, recommendation text,
component descriptions, all 15 feature-catalog entries, update/time/firewall
instructions, support privacy guidance, screenshot requirements, announcement
drafts and launch checks. Final filenames, sizes, hashes, URLs and 1920×1080
promotional assets remain pending. Local wiki edits are not assumed public.
The final local-link check resolves all 203 file targets across the seven edited
status/report documents, with no missing targets. It does not validate remote
URLs or rendered anchors. `git diff --check` and Bash syntax checks pass.

The evidence/claim review is complete **with the two open findings above**.
The safe [build-space plan](2026-09-13-build-space-plan.md) is separate. No final
build, commit, package promotion or publication is authorized by this review.
