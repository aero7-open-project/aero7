# Aero7 Beta 2 — release notes draft

Updated 21 September 2026. **Not approved for publication or downloads.**
Rebuilt online and offline test candidates have passed fresh-install acceptance.
They remain internal candidates until the owner approves the final build and
website publication; their filenames and hashes are not public release
identifiers.

The [website maker handoff](BETA2-WEBSITE-MAKER-HANDOFF.md) supplies website copy,
download-card requirements, feature explanations and announcement drafts.
The [QA status record](BETA2-QA-STATUS.md) is the evidence index. Historical
candidate results must not be presented as tests of a later image.

## Planned installation images

- **Offline ISO — recommended.** Includes the installation package dependency
  closure and a checksum-pinned local repository. Installation works without
  internet and avoids mirror/download delays. Actual duration still depends on
  the computer and storage device.
- **Online ISO.** Smaller download; retrieves the distribution dependencies
  during installation and requires a stable connection. Corrected Aero7
  components remain pinned by the candidate manifest.

Both variants configure repositories for updates after installation. Final ISO
files and checksums will be hosted on the Aero7 website, **not GitHub Releases**.
Filenames, sizes, hashes and download URLs remain pending until build, acceptance
and publication approval.

## Desktop and application changes

- Dedicated Aero7 Desktop Wayland session, with AeroThemePlasma/Plasma fallback
  sessions retained.
- Factory taskbar layout and Recycle Bin-only production desktop. Diagnostic
  test images additionally create the requested physical-install log folder.
- Aero7 Professional login/lock-screen branding, session selection and supported
  login accessibility controls. This is not the complete Windows 7 pre-login
  accessibility dialog.
- Windows-style Meta+Shift+S rectangular capture: the overlay closes, a PNG is
  saved, image data is copied for paste, and the saved notification opens the
  image. The editor is not opened automatically.
- Desktop edit-mode suppression and Windows-inspired taskbar, Start, desktop
  menus, pinned application identity and window handling.
- Aero7 File Explorer based on the maintained Dolphin fork, with Libraries,
  Computer, Recycle Bin, breadcrumbs, storage handling and common dialogs.
  Raw Linux mounts are filtered where appropriate; this is not complete Windows
  storage-management compatibility.
- 45-app Control Panel layout, Windows-inspired Screen Resolution and Linux
  backends for supported settings. Unavailable features are identified honestly.
- Desktop Gadgets, including improved feed recovery, slideshow playback
  preservation, display scaling and desktop/window-layer behavior.
- Approved AeroThemePlasma icon-pack resources bundled with Aero7 applications.
  No replacement icon pack or newly drawn application icons was introduced.
- Device Manager naming uses `aero7-device-manager`, retaining
  `linux-devmgmt` compatibility for upgrades.

Recent candidate corrections include display Apply/rollback, automatic virtual
output-layout repair, screenshot cancellation/recovery, Explorer dialog request
isolation, delayed session shutdown handling, and generated-source cleanup.
See the linked QA reports for the exact package version and tested scope.

## Updates and firewall

Update checks and installation are separate. Users can turn update checking on
or off; installing updates requires approval. Unavailable repository information
must not be presented as proof that the system is up to date.

Fresh installations use firewalld. Existing UFW installations are preserved,
not silently migrated. Unassigned networks default to Public; selecting a
trusted network location does not itself create shares or enable remote login.
The website handoff documents the implemented Home/Work/Public behavior and
its testing boundaries.

## Optional features

Open **Start → Turn Aero7 features on or off**, or **Control Panel → Programs →
Programs and Features → Turn Aero7 features on or off**. Controls reflect
package/service state, require administrator authorization and explain retained
data and sign-out requirements.

- **Programs Center Beta** is optional and absent by default. Its bundled package
  supports offline enabling/removal/re-enabling; downloading additional software
  still requires the relevant repositories and connectivity.
- **Encrypted Credential Vault** is optional and off by default. It adds generic
  credential storage through KWallet, not custom cryptography. Enable the feature,
  sign out and back in, then open Credential Manager. Use a non-empty password.
  Removal retains encrypted wallet files; re-enabling requires the original
  password. Account-specific overrides are preserved. No password recovery,
  browser import, autofill, domain credentials or whole-disk encryption is
  provided.

The [Optional Features guide](../wiki/Optional-Features.md) and
[website feature reference](BETA2-WEBSITE-MAKER-HANDOFF.md#5-optional-features-reference)
explain every catalog entry. The catalog has 15 entries: 13 searchable optional
features, one protected desktop core and one hidden discontinued CardSpace entry.
Not every optional backend is bundled for offline installation.

## Installer and diagnostics

The candidate validates package identities, dependency closure and local
checksums. Failures stop with a diagnostic instead of continuing through an
unverified transaction. Diagnostic test images collect installation, boot,
hardware, package, display-manager and session logs in **Aero7 Physical Install
Logs** on the desktop.

The collection avoids deliberate password, connection-profile, personal-file,
browser-data and full-memory-dump collection. Logs can still contain identifying
information such as device names, usernames and paths: review the privacy notice
and collected files before sharing them.

## Current local candidate packages

These are local QA selections, not a published repository availability claim.
Versions were read from all 19 package metadata records referenced by the
[local checksum manifest](../config/beta2-local-packages.sha256).

| Package | Selected version |
| --- | --- |
| `aero7-desktop` | `0.2.0-33` |
| `aero7-file-explorer` | `25.12.3-55` |
| `linux-control-panel` | `0.1.0-55` |
| `aero7-device-manager` | `2.2.1.r1.g6d080f8-1` |
| `aero7-computer-management-git` | `0.2.0.r20.g6d7fe79-2` |
| `aero7-gadgets` | `3.0.0-25` |
| `aero7-kolourpaint` | `25.12.3-9` |
| `aero7-internet-explorer` | `0.1.0-5` |
| `aerothemeplasma-desktop-git` | `6.7.0_742.r9c2d850-65` |
| `aerothemeplasma-icons-git` | `11.r96950b8-3` |
| `aerothemeplasma-sounds-git` | `4.r55d2f5f-3` |
| `spectacle` | `1:6.7.4-3` |
| `plasma-workspace` | `6.7.4-3.2` |
| `qt6-base` | `6.11.2-3.1` |
| `uac-polkit-agent-git` | `6.7.0_816.rd8c2262-2` |
| `kwin` | `6.7.4-7.3` |
| `aero7-programs-center-git` (optional) | `0.1.0.r12.g0405a2e-3` |
| `aero7-credential-vault` (optional) | `0.1.0-7` |
| `kwallet` | `6.29.0-1.1` |

## Acceptance and release gates

The latest selected manifest adds the accepted Aero7-scoped KWallet presentation
package to the required local transaction. The earlier 21 September rebuilt
candidates predate that selection, so their successful clean-install results
remain evidence for the rest of the stack but do not close the refreshed-image
vault gate. A new online/offline candidate cycle is required before final-build
approval.

The latest selected manifest passes 155 integration tests, static checks,
19 online candidate-archive checks, 84 offline candidate/dependency-archive
checks and 65 offline repository identity/checksum checks. These are local
results, not new GitHub CI results.

Fresh installations from both rebuilt 21 September test candidates verify the
selected stack after OOBE and password login. Both collector manifests verify
144 of 144 files with zero failed user/system units and no collected coredumps.
The detailed report also covers SDDM accessibility/session selection, lock/login
branding, Explorer identity, optional package install/removal and the complete
screenshot save/clipboard/notification path. Vault 7 retains its separate native
overlap, retained-content and isolated backend evidence.

The source and rebuilt-candidate bug-test pass is complete. Before final release:

1. Obtain approval for the final build, then build both variants from the
   approved sources/packages without bypassing dependency or signature checks.
2. Validate each exact image and repeat fresh online and disconnected offline
   installation checks against those final artifacts.
3. Repeat first-run setup, reboot/login/lock, optional features, taskbar/Start,
   Explorer, Control Panel, screenshot and gadget checks on that final media.
4. Record actual multi-monitor/recovery coverage, hardware limitations,
   signing/repository promotion, final 1920×1080 screenshots, sizes and hashes.
5. Obtain publication approval and verify the website-hosted files and links
   before enabling downloads or announcing availability.

Physical GPU/hotplug behavior, alternative vault configurations and other
unverified backends are not advertised as tested. Full Windows 7 parity and
universal bug-free operation are not claimed.

The [superseded notes](release-evidence/2026-09-13-superseded-release-notes.md)
preserve the older version table and historical blockers for reference only.
