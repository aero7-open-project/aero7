# Historical release notes — superseded on 13 September 2026

This snapshot preserves the previous release-notes content, including its old
package versions and then-current blockers. It is not current release guidance.
Use [the maintained release notes](../BETA2-RELEASE-NOTES.md) instead.

---

# Aero7 Beta 2 release candidate notes

## Publication status

The Beta 2 source, package definitions, documentation, and wiki content are
prepared for public review. The online and offline ISO files are deliberately
not part of this source publication. Beta 1 remains the current downloadable
release until both Beta 2 images complete the remaining installation and
graphical acceptance gates.

## Planned media

Beta 2 is prepared as two installation images built from the same guarded
installer and pinned package set:

- **Offline ISO — recommended.** Embeds the complete package dependency closure
  and a checksum-pinned local pacman repository. It installs without internet
  and avoids mirror/download delays on slower hardware.
- **Online ISO.** Smaller download that retrieves the current Arch and Aero7
  packages during installation. It requires a stable internet connection for
  the complete package phase.

Both variants retain the normal signed repositories for updates after setup.

## Desktop and application changes

- Ships the dedicated Aero7 Desktop Wayland session, with AeroThemePlasma
  available as a fallback session.
- Applies the factory taskbar layout and a clean production desktop containing
  only the Recycle Bin. These diagnostic test images additionally create the
  requested `Aero7 Physical Install Logs` folder.
- Keeps the corrected Aero7 Professional branding on SDDM and the Plasma lock
  screen, including session selection and login accessibility controls.
- Uses Windows-style `Meta+Shift+S` rectangular screenshots: selection closes,
  the PNG is saved, image data is copied to the clipboard, and the notification
  opens the saved file.
- Removes user-facing desktop edit mode and aligns taskbar, Start, desktop, and
  context-menu behavior with the Aero7 shell contract.
- Embeds approved AeroThemePlasma icon-pack resources in Aero7 applications so
  their identity does not change with the global icon theme.
- Updates File Explorer naming, icon, Wayland identity, taskbar pinning, Recycle
  Bin settings, Libraries, Computer, common dialogs, and Linux-mount filtering.
- Includes the 45-item Control Panel layout and Linux-backed Screen Resolution,
  networking, power, sound, users, updates, programs, and administration pages.
- Renames the maintained device application and package to
  `aero7-device-manager`, while preserving `linux-devmgmt` compatibility for
  upgrades.

## Optional features

**Turn Aero7 features on or off** is searchable from Start and available from
Control Panel's Programs category and Programs and Features page. It reports
real package/service state and supports install, remove, repair, verification,
retained-data explanations, and audited Polkit authorization.

Programs Center Beta is optional and absent on a fresh installation. Both media
variants retain its checksum-verified package locally, allowing it to be
enabled, removed, and enabled again without internet. Other optional features
and their backends are documented in the
[Optional Features guide](../../wiki/Optional-Features.md).

## Installer and diagnostic changes

- Adds strict local-package manifests and dependency-closure validation.
- Adds a complete offline package repository preparation path.
- Improves online package failure reporting and safely stops without leaving a
  partially configured target.
- Creates `Aero7 Physical Install Logs` on the installed user's desktop with
  installer, boot, hardware, package, service, display-manager, and session
  diagnostics plus a SHA-256 manifest and privacy notice.
- Keeps passwords, network connection profiles, personal documents, browser
  data, and full core-memory images out of the collected folder.

## Candidate component versions

| Component | Candidate package |
| --- | --- |
| Aero7 Desktop | `0.2.0-27` |
| Aero7 File Explorer | `25.12.3-35` |
| Aero7 Control Panel | `0.1.0-43` (local build; final VM acceptance pending) |
| Aero7 Device Manager | `2.2.1.r1.g6d080f8-1` |
| Aero7 Computer Management | `0.2.0.r20.g6d7fe79-2` |
| Aero7 Gadgets | `3.0.0-3` |
| Aero7 Paint | `25.12.3-3` |
| Aero7 Internet Explorer compatibility | `0.1.0-5` |
| AeroThemePlasma Desktop | `6.7.0_742.r9c2d850-44` |
| AeroThemePlasma icon pack | `11.r96950b8-3` |
| AeroThemePlasma sound pack | `4.r55d2f5f-3` |
| Spectacle screenshot backend | `1:6.7.4-2`, local downstream correction |
| Programs Center Beta | `0.1.0.r12.g0405a2e-2`, optional |

## Release gates

Source checks, package-manifest checks, optional-feature helper tests, and
installer unit tests are required before the source push. The main Aero7 source
gate, Aero7 Desktop CI, and the 23-package recipe-manifest validation were green
at the earlier source-publication checkpoint. The current local manifest has
24 recipes, including the Spectacle correction, and passes repository validation.
That local result is not a new CI run or publication of the candidate packages.

The local 5 September follow-up fixes pass all 16 File Explorer CTest
executables, including search-popup lifecycle, extended-attribute fallback,
keyboard focus, accessibility, and Aero7 identity/icon checks. Regression tests
also cover repeated popup opening, fallback persistence and migration, and the
renamed application's action-layout resource. Desktop passes all five test
groups, including production/test-image installation separation. These are
local, uncommitted source results. Local QA packages and intermediate test images
have since been rebuilt; signed release packages and final-image acceptance
remain separate gates. See the
[follow-up evidence](2026-09-05-beta2-fixes-and-cleanup.md) and
[current corrected-candidate report](2026-09-05-fixed-candidate-acceptance.md).

The latest local payload additionally fixes offline optional-package metadata
parsing, first-login configuration ownership, persistent wrong-password lock
feedback, missing dedicated Control Panel icons, and Programs Center's installed
inventory when repository databases are unavailable. Programs Center no longer
claims the system is up to date when it cannot read repository information.
Explorer 35 also fixes the clipped processor line in Computer's details strip.
All 18 Explorer CTest executables pass, including the footer regression at
9, 12 and 18 point fonts. This package is a local unsigned QA candidate;
repository promotion and final-image acceptance remain separate gates.

The following remain release blockers for the ISO files:

- embed Spectacle `1:6.7.4-2` and theme `-44`, then repeat screenshot tests on
  final media. The backend now distinguishes actual capture denial from Escape
  and terminates failed background saves instead of hanging. Both background
  entry points passed PNG save/error tests; the upgraded offline VM also passed
  failed-save notification, Try Again, subsequent capture and notification-open.
  Theme `-44` separately passed image paste and all 15 theme CTests;
- embed the rebuilt Paint package and repeat fresh-image regressions; the
  complete package passes its 20-cycle close test and an offline-VM install,
  PNG save/reopen, Cancel/Discard and normal-close checks with no new coredumps;
- verify positive update notifications and approval-before-installation on
  final media. The upgraded r4 offline guest saves on/off preferences, runs the
  checker without installation, and reports an unavailable repository honestly;
  r43 additionally corrects the misleading grey settings link;
- VM-test connection-specific Home/Work/Public selection. The implementation
  keeps unassigned networks Public, permits mDNS discovery on Home only, and
  never starts file sharing or remote access automatically;
- embed and freshly verify the regional-preference correction with nondefault
  language, keyboard and regional-format choices through first-run setup,
  SDDM and the installed session; isolated VM checks do not replace this;
- embed and freshly verify the post-r4 command-locale correction (89 passing
  backend/adapter tests and real VM probes are source-level evidence);
- embed the tested theme-slider, upgrade-safe splash/logout branding and
  icon/sound packaging corrections, then repeat the relevant graphical checks
  on the new images; a running-session taskbar icon needed a shell refresh
  after the icon-pack upgrade, so seamless live icon refresh is not established;
- fresh installation from the final online image;
- fresh installation from the final offline image with networking unavailable;
- reboot, OOBE, SDDM, lock-screen, and second-login verification;
- taskbar, Start, File Explorer, Control Panel, screenshot, optional-feature,
  multi-monitor, and recovery-path acceptance;
- final image verification, sizes, SHA-256 checksums, and release-page upload.

No Beta 2 ISO should be announced as available until these checks are recorded.

The r4 local images now embed the fontconfig ordering, firewall activation and
working help/privacy dialogs. Both completed fresh installation and first-run
setup; the offline VM has no network adapter. Both fresh installed firewalls
passed IPv4/IPv6 incoming-block/outgoing-reply packet tests, and the offline
fontconfig initialization completed correctly. Both then passed normal reboot,
SDDM password login and lock/unlock, with active firewalls and no failed services
or current-boot coredumps at those checkpoints. Subsequent application testing
found the Paint close crash listed above; its retained core means the earlier
checkpoint must not be read as a current clean-coredump claim.
Broader final-release acceptance remains incomplete.
This does not resolve the update/network-location
blockers or approve the unsigned QA packages for release.

Intermediate r3 online and offline fresh installations, OOBE, normal reboot and
second SDDM login have passed. Fresh Explorer 35 and the offline Programs Center
install/remove/reinstall cycle also passed. These results do not clear the newly
confirmed setup blockers or establish acceptance for subsequently rebuilt media.

The signed package builder must produce and validate these exact recipe versions
before the final online and offline ISO manifests are refreshed. Older packages
in a developer's local test cache are not release artifacts.
