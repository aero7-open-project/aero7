# Aero7 Beta 2 — website maker handoff and announcement drafts

**Working draft — DO NOT PUBLISH OR ENABLE DOWNLOADS YET.**

Updated 22 September 2026. Rebuilt online and offline test candidates have
completed clean-install acceptance, and the exact final local image pair has now
passed the same connected-online and disconnected-offline VM gate. The artifacts
are not public downloads: signing/upload decisions, hosted-file verification
and website publication approval remain open. This document supplies website
copy, implementation requirements and a release checklist. Draft announcement
wording is conditional on the remaining gates below. It is not approval to
publish, nor a claim that Beta 2 is already available.

Current QA status and package identities are recorded in the
[QA status and evidence history](BETA2-QA-STATUS.md). Its linked reports distinguish
fresh-image results from later upgrades to the test guests. Historical results
must not be presented as acceptance of the final package set or final ISOs.

## Current release status

The current candidate selects Desktop 33, Gadgets 25, Control Panel 55,
KWin 7.3 and optional Vault 7 alongside the other corrected packages. The
[release notes](BETA2-RELEASE-NOTES.md) match all 19 selected archive identities
and optional labels. The latest recorded integration run passes 160 tests,
19 online candidate-archive checks, 84 offline candidate/dependency-archive
checks and 65 offline repository-entry checks.

The [final-media acceptance report](release-evidence/2026-09-22-final-online-offline-media-acceptance.md)
records both locally finalized artifacts. Each exact ISO completed a clean
installation, OOBE, first-login audit, optional Programs Center install/removal,
reboot and pinned File Explorer launch at 1920x1080. The offline image ran with
no network adapter; the online image verified networking and synchronized time.
Both prove that the PolicyKit agent is active before the first privileged
feature request. Final URLs, signing state and upload-back verification remain
pending.

The [selected-stack alignment report](release-evidence/2026-09-13-selected-stack-alignment.md)
now verifies all 16 core versions after normal reboot/password login in both
existing test guests. The actual running Gadgets, Action Center and mapped KWin
library match their selected builds. Desktop services have zero restarts and
no failed units at those checkpoints. Both optional caches match the selection;
the disconnected guest's vault remains absent/disabled, while the online
guest's installed vault and encrypted wallet files are preserved.

The 21 September rebuilt online and offline candidates now add fresh installation,
OOBE and password-login evidence. Their exported collector manifests verify
144 of 144 listed files with zero failed units and no collected coredumps.
SDDM accessibility/session selection, login/lock branding, File Explorer,
Optional Features and Windows-style screenshot behavior passed on the installed
systems. Earlier component results and their exact version boundaries remain in the
[QA history](BETA2-QA-STATUS.md), including Explorer/common dialogs, Control
Panel, screenshots, updates, gadgets, vault lock-state handling and recovery.
All 18 retained build recipes match their archives' BUILDINFO hashes. The
[source-input follow-up](release-evidence/2026-09-13-retained-source-inputs.md)
also verifies the presence of all 95 declared inputs, the applicable file/Git
hashes, the Gadgets install hook and Qt's supplemental commit. Snapshot
comparisons classify later test-only and nested-companion changes. This is
local traceability, not a reproducible-build or trusted-signing claim.

**The rebuilt-candidate bug-test pass is complete.** The
[closure checklist](BETA2-PREBUILD-CHECKLIST.md) separates completed guest
alignment, source-input reconciliation, native vault prompt replay, startup
diagnostic triage, [requirement review](release-evidence/2026-09-13-prebuild-requirement-review.md)
and [build-space planning](release-evidence/2026-09-13-build-space-plan.md) from
two former presentation findings: the requested login Ease of Access dialog and
the stock KDE Wallet password dialog. The later
[installed-VM vault replay](release-evidence/2026-09-20-vault-presentation-native-vm.md)
passes the scoped Aero7 prompt, retry, cancel, overlap and retention behavior;
the selected source manifest now includes it. The rebuilt candidates include and
pass the SDDM Ease of Access dialog and desktop-session selector. These later
results close the SDDM gate without erasing the historical evidence. The
[vault presentation source patch](release-evidence/2026-09-13-vault-presentation-source.md)
builds and passes isolated tests using the existing pack icon. Its accepted
`kwallet 6.29.0-1.1` package now belongs to the required local transaction. The
[22 September refreshed-candidate acceptance](release-evidence/2026-09-22-selected-kwallet-candidate-acceptance.md)
verifies both new test images, exact installed selection, default-off Vault 7
state and the native Aero7-titled first-use/password presentation. This closes
the engineering gate, but do not describe it as shipped until the owner approves
and the exact final website-hosted images pass the release checks.
The [native vault follow-up](release-evidence/2026-09-13-vault-native-prompts.md)
verifies cancellation, retry, client closure and retained synthetic credentials
through two read/lock cycles. The original ciphertext-hash failure is preserved
and explained; no production package changed. Native prompt-parenting remains
limited. The [diagnostic follow-up](release-evidence/2026-09-13-startup-diagnostic-triage.md)
identifies the SVG resources and verifies their consumed elements without
changing the existing artwork. Logs still retain parser warnings, virtual
graphics/CPU diagnostics, unavailable optional backends and auxiliary portal
registration failures. The offline guest's later scheduled update check also
correctly reports unknown availability and remains a failed unit while offline;
the earlier clean reboot checkpoints do not mean permanent zero-error status.
Do not claim warning-free logs or verified physical-hardware compatibility.
No security checks were weakened or failed units cleared to suppress diagnostics.

The final local images contain the selected fixes and passed fresh exact-media
online/offline installation. Use sections 1–9 below as conditional website copy.
Keep downloads disabled and the current public release unchanged until the
remaining signing/upload, hosted-file verification and publication-approval
checks are complete.

## 1. What the website team should change

- Prepare the homepage Beta 2 announcement and a dedicated release-notes page.
- Prepare two download cards, with **Offline ISO — recommended** first.
- Host both ISO files and their checksum file on the Aero7 website/download
  infrastructure, **not GitHub Releases**. GitHub hosts source, issues and wikis.
- Update the Desktop, File Explorer, Control Panel, Gadgets and installation
  pages using the component descriptions below.
- Add an Optional Features section, with Programs Center Beta marked optional.
- Replace superseded promotional screenshots with verified 1920×1080 captures
  from the accepted images. Keep old screenshots only in a labeled archive.
- Add installation choices, update instructions, known limitations and safe
  diagnostic-log sharing guidance to the help pages.
- Keep the currently published release unchanged until explicit release approval.

Do not redesign application icons or generate new ones. Use the established
AeroThemePlasma icon pack and the project-owned Aero7 branding already in the
applications. Use genuine screenshots, not Windows reference images or mockups.

## 2. Homepage copy

### Headline

Aero7 Beta 2: a familiar desktop, with a Linux foundation

### Introductory text

Aero7 Beta 2 brings together the dedicated Aero7 desktop, a Dolphin-based File
Explorer, a Windows-inspired Control Panel and Desktop Gadgets. Choose the
recommended offline image for an installation that does not need internet,
or the smaller online image when you have a reliable connection.

### Calls to action

- Primary: **Download Offline ISO (recommended)**
- Secondary: **Download Online ISO**
- Supporting: **Read Beta 2 release notes** · **Installation guide** ·
  **Report a problem**

Show a visible beta notice next to the download choices: **Beta software:
back up important files and use a spare machine or virtual machine for testing.**
Aero7 is an independent Linux project, not Microsoft Windows. Familiar interface
names do not imply Windows drivers, services or universal application compatibility.

## 3. Downloads page

| Card | Offline ISO — recommended | Online ISO |
| --- | --- | --- |
| Short description | Includes the packages needed for the complete base installation. | Smaller installation image; downloads installation packages. |
| Internet during base installation | Not required. | Required throughout the package-download phase. |
| Main advantage | Avoids mirror and package-download delays during setup. | Smaller initial ISO download. |
| Trade-off | Larger download and more space needed on the USB drive. | Installation speed and reliability depend on the connection and mirrors. |
| After installation | Connect to the normal repositories for new updates. | Uses the same normal repository update path. |

Suggested recommendation copy:

> We recommend the Offline ISO, especially for slow laptops or unreliable
> connections. It avoids downloading the package set during installation and
> can therefore make setup much faster. USB, CPU and disk speed still matter;
> there is no guaranteed installation time.

Both variants target the same Aero7 desktop, not different product editions.
Offline base installation does not mean every future app, update or optional
feature is available without internet. Programs Center Beta's installation
archive is included; its software catalog and new package downloads need a
connection. Other feature dependencies may require downloads.

### Artifact fields — fill only from the accepted build

| Field | Offline | Online |
| --- | --- | --- |
| Final filename | `aero7-beta2-offline-2026.09.22-x86_64.iso` | `aero7-beta2-online-2026.09.22-x86_64.iso` |
| Exact byte size | 3,407,151,104 bytes | 1,604,804,608 bytes |
| Display size | 3.17 GiB | 1.49 GiB |
| SHA-256 | `f44c52bf8171fd2842e2c6150909e9ca70a577f4e3ac9f6444baeea45f1676a5` | `e1744b3be9692af6252bfdc42b83a1bc4c309f33f300771dd3b26cfeacafc936` |
| Direct HTTPS download URL | Website owner to provide | Website owner to provide |
| Release date | Set when publication is approved | Same release date |

Do not reuse the hashes from the failed 4/5 September candidates. Rebuilt files
can have the same filename but different contents. After upload, verify the
actual downloaded bytes against the final checksum file before enabling buttons.
After the owner-approved pair is built, run
`scripts/finalize-release-artifacts.py` with both exact ISO paths and a clean
metadata directory. It runs the full release verifier on the recommended
offline image and then the online image, requires matching release dates, and
creates `SHA256SUMS` plus `BETA2-ARTIFACTS.md` only after both pass. These local
files do not sign, upload, publish or approve the release.

### Verification instructions for visitors

Download the ISO and the matching checksum file from the release page. On Linux,
run `sha256sum` followed by the downloaded ISO filename. On Windows PowerShell,
run `Get-FileHash` followed by the filename and `-Algorithm SHA256`. Compare the
entire result with the value displayed for that exact image. A checksum detects
corruption; it is not a substitute for a trusted download source or a signature.

## 4. Product-page updates

### Aero7 Desktop

Describe the dedicated Aero7 Wayland session, Start menu, glass-style taskbar,
window grouping/previews, desktop menus, tray and notifications. The factory
taskbar starts with Start, Command Prompt, File Explorer and the familiar
browser entry. Recycle Bin starts at the upper-left of the normal desktop.
Diagnostic test images additionally create **Aero7 Physical Install Logs**.

Explain that KDE/KWin and Linux remain the underlying technologies.
AeroThemePlasma/Plasma sessions remain explicit fallbacks; do not describe the
project as removing every KDE library. Desktop edit mode is not part of the
normal Aero7 shell interface. Safe Mode limits effects; it is not a separate OS.

### File Explorer

Present **Aero7 File Explorer** as the maintained Dolphin-based implementation,
not a brand-new file manager unrelated to Dolphin. Cover Libraries, Computer,
Network, Recycle Bin, properties, familiar navigation and common file dialogs.
Computer uses friendly drive presentation rather than exposing every internal
Linux mount. Preserve accurate upstream attribution and license information.

Explain that **Local Disk (C:) is Aero7's display label for the Linux system
filesystem**, not a Windows partition or a promise that applications accept
Windows-style paths. Drive letters shown for other mounted volumes are display
labels, not persistent Windows drive mappings. Do not depict a fabricated CD
drive simply to fill space in a promotional screenshot.

After final acceptance, include cancellable file-dialog search, file-type
filtering, library-folder scope and the supported Organize controls. Do not
describe the limited Organize menu as a complete Windows file-operation menu.
Include keyboard-friendly Open and Save As: the filename field is ready for
typing when the dialog opens. This correction has passed the component VM
replay, but must be present in the accepted final images before it is announced
as shipped; see the [Explorer 53 evidence](release-evidence/2026-09-08-dialog-initial-focus.md).

### Paint

Describe the ribbon Paint application, drawing tools, colour selection and
native Open/Save dialogs. Format-specific conversion, image-quality and preview
controls remain available. New profiles open another image in the current
document window, with Save/Discard/Cancel protection for unsaved work. An
existing preference for separate windows is preserved. Remote URL browsing
uses an explicit alternate file browser; do not advertise identical native
behavior for every protocol or file format.

### Control Panel

Explain the 45 familiar applet entry points, five-column All Control Panel Items
view, search and Linux-backed settings. Highlight Screen Resolution, network,
sound, power, accounts, programs, updates and administrative tools. **45 entry
points does not mean 45 fully equivalent Windows services.** Hardware-dependent,
optional and unavailable features must explain their state rather than look like
working features when they are not.

### Desktop Gadgets

List Calendar, Clock, CPU Meter, Currency, Feed Headlines, Picture Puzzle,
Slide Show, Weather and Media Center. Explain the gallery, adding/removing
gadgets and their individual settings. Weather, feeds and currency data depend
on network services and their availability; do not promise perpetual live data
or offline weather. Use actual project captures and existing gadget artwork.

### Screenshots

Once the final-image check passes, use this visitor-facing instruction:

> Press **Meta+Shift+S**, drag a rectangle and release. The selector closes
> without opening the editor. Aero7 saves a PNG in the Screenshots folder below
> your configured Pictures directory, copies the image to the clipboard and
> shows a saved notification. Click the notification to open the image, or use
> **Ctrl+V** in an application that accepts pasted images. **Esc** cancels.

Do not call a copied filename equivalent to copied image pixels.

Privacy note for the released handoff correction: explicitly copied screenshots
can appear in the desktop clipboard history and follow its retention settings.
Clearing clipboard history does not delete the PNG in Pictures/Screenshots.
The correction does not turn on history for other image copies globally.

### Login and lock screen

Mention the corrected Aero7 Professional branding, lower-left login menu,
available session choices and on-screen keyboard. Distinguish logging into a
different desktop from unlocking the existing session. Do not claim the full
Windows 7 pre-login accessibility checkbox dialog has been implemented; use
the precise supported controls shown in the tested build.

## 5. Optional Features reference

Location: **Start → Turn Aero7 features on or off**, or **Control Panel →
Programs → Programs and Features → Turn Aero7 features on or off**.

| Feature | Explain to visitors |
| --- | --- |
| Aero7 Desktop Core | Required desktop, shell, Control Panel and File Explorer; cannot be removed through this dialog. |
| Programs Center Beta | Optional graphical software manager, absent by default. Its bundled installer allows offline enabling/removal/re-enabling once verified. Managing new downloadable software still needs network access. |
| Encrypted Credential Vault | Optional and off by default. Adds Credential Manager for generic usernames and passwords using KWallet encryption and password prompts. Enable through this dialog, sign out and back in, then open Credential Manager. Choose a non-empty vault password. Add, edit, remove and lock controls are available; passwords are masked until explicitly revealed. Removal retains encrypted vault files and account settings, and re-enabling uses the original vault password. Sign out after disabling. No password recovery, browser import, autofill, Windows domain integration or whole-disk encryption is provided. |
| Parental Controls | Uses malcontent for managed-account application restrictions; sign out after enabling. |
| Backup and Restore | Déjà Dup for personal-file backups and restores. Removing the feature retains archives and settings. |
| System Recovery | Snapper and Btrfs Assistant for snapshots on Btrfs roots only; existing snapshots are retained. This is not a promise that every installation uses Btrfs. |
| Advanced Accessibility Services | Orca, Speech Dispatcher and eSpeak NG for screen reading and speech output; sign out after enabling. |
| Speech Recognition | Not available: there is no supported dictation/voice-control backend yet. Screen reading is not speech recognition. |
| Sync Center | Syncthing and its per-account system service for trusted folder synchronization; removal retains files and configuration. |
| Aero7 Defender | ClamAV with its signature-update service for on-demand scanning. Updated signatures need internet. Do not promise Windows Defender or complete malware protection. |
| Windows CardSpace | Hidden/unavailable: no safe supported equivalent for the discontinued technology. |
| Remote Desktop Connections | FreeRDP client for connecting to another machine; does not enable inbound remote login. |
| File and Printer Sharing | Samba and SMB services. No shares are created automatically; existing configuration is retained. |
| Mobile Broadband and Modem Support | ModemManager service and compatible modem support; the UI reports when hardware is absent. |
| Color Management | colord and ICC profile workflows; sign out after enabling. Profiles remain after removal. |

Checked, unchecked, partially installed and unavailable states are meaningful.
Changes require administrator authorization. Explain retained user data and
any sign-out/restart requirement. Never tell visitors to bypass dependency,
signature or checksum validation to make a failing transaction continue.

Vault-specific guidance: existing account wallet/portal overrides are preserved.
The selected candidate does not yet include the scoped Aero7 password-dialog
override, and unrelated KWallet/GPG surfaces retain upstream branding. If locking
cannot be verified, sign out before leaving the computer; a cleared list alone
is not proof that the backend locked. Never ask users to share vault passwords
or decrypted entries in bug reports. The vault protects its saved collection,
not every file on the computer. It is a local candidate until included in the
accepted release images; see the [native lock and two-client evidence](release-evidence/2026-09-09-vault-lock-verification.md).

## 6. Installation, updates and support pages

Keep disk-erasure warnings prominent. The images are x86-64 UEFI media; do not
advertise legacy BIOS, Secure Boot, dual-boot partition resizing or particular
physical hardware as tested without matching evidence. Backups are essential.
Installer failures should be reported with the actual error and logs, not worked
around by repeatedly wiping a real disk.

Installed systems retain the Arch/Aero7 repository configuration. For connected
systems, document the normal full-system update (`sudo pacman -Syu`) and the
graphical update route where supported. Do not recommend partial upgrades or
`pacman -Sy` alone. Changes only present in local QA packages are not already
available to users through the public package repository.

### Update preferences — visitor-facing copy after acceptance

Maintainer evidence: [r10 update preferences and approval checks](release-evidence/2026-09-08-update-preferences.md)
and [actual online recovery and approved full upgrade](release-evidence/2026-09-08-online-update-recovery.md).
This is bounded verification, not permission to publish the whole release.

Open the Control Panel update page and choose **Change settings**. Turn
**Check for updates automatically and notify me** on or off, then choose
**Save**. This preference applies to your account. Turning automatic checks
off leaves **Check for updates** available for manual use.

Automatic checks notify you; they do not install packages. You must approve
installation, and system changes require administrator authorization. Keep the
computer powered on while updates run. Aero7 prevents ordinary page navigation
or window closing from interrupting an active graphical update, but this cannot
protect against power loss, forced process termination or ending the session.
An unsuccessful check is not evidence that the computer is up to date.
Successful installation confirms the selected transaction; check again for
newly available updates. If AUR checking is unavailable, the status says so.
Update history does not assume every package absent from the repository
catalog came from the AUR; unknown sources are labeled explicitly.

### Clock and Internet Time — visitor-facing copy after acceptance

First-run setup previews the date and clock in the time zone you select, using
your selected regional clock format and calendar week start.
Daylight saving follows that zone's rules. Fresh systems start automatic time
synchronization without waiting for an internet connection; an offline computer
cannot synchronize until it can reach a time server.

In **Control Panel → Date and Time → Internet Time → Change settings**, turn
synchronization on/off or select a time-server hostname or IP address. Changes
require administrator approval. **Update now** applies the selected server and
asks the time service to synchronize. Cancelling approval does not apply the
change. Your chosen server stays selected when synchronization is turned off
and back on. Starting the service is not proof that a server has been reached.

### Firewall and network locations — visitor-facing copy after acceptance

Fresh installations use **firewalld**. Existing installations configured with
**UFW** keep their existing backend and rules; this release does not silently
migrate them. Firewall information can be viewed without granting permission
to change the configuration. Changes still require administrator approval.

On fresh firewalld installations, **Change network location…** in the Firewall
page lets you select an active wired or wireless connection and choose Public,
Home or Work. **Public** is the default and blocks unsolicited incoming traffic.
**Home** additionally permits local mDNS discovery; it does not automatically
enable file sharing or remote login. **Work** also starts with unsolicited
incoming traffic blocked; add only services approved for that network.
Choosing a trusted profile for one connection does not make every later network
trusted. With no active wired/wireless connection, connect first before changing
its location. Existing UFW systems do not gain these firewalld-only controls.

The diagnostic desktop folder contains installer, boot, hardware, package,
service and session evidence plus a checksum manifest and privacy notice.
Ask users to review it before sharing: logs can contain usernames, hostnames,
hardware identifiers, device paths and network information. Do not request
passwords or publish raw archives as website downloads. Screenshots should
also be checked for personal information.

### FAQ copy

**Which ISO should I use?** The Offline ISO is recommended. Choose Online if
the smaller download matters more and you have reliable internet during setup.

**Does Offline mean I never need internet?** No. It covers the base installation.
New updates, additional software and live-data gadgets can need internet.

**Is Programs Center required?** No. It is optional and can be enabled through
Turn Aero7 features on or off. Removing it does not remove the desktop.

**Is the encrypted vault enabled automatically?** No. Enable Encrypted Credential
Vault in Turn Aero7 features on or off and sign out and back in. It stores generic
credentials, not all your personal files. Keep its password safe: there is no
password-recovery feature. Removing the optional feature does not erase the vault.

**Is this Windows 7?** No. Aero7 is Linux with a familiar Windows-inspired UI.
Windows programs and drivers are not universally compatible.

**Will my laptop install as quickly as the VM?** Not necessarily. Disk, USB,
CPU and network performance differ. We do not promise a fixed installation time.

## 7. Screenshot handoff

Final asset directory and capture evidence: **PENDING new-image acceptance**.
Use 1920×1080 at 100% scale, PNG, without stretching or compositing UI states.
Do not use private QA logs, deliberate failure screens or password-entry shots
as promotional assets. Where the diagnostic folder is visible, label the image
as diagnostic test media; do not silently erase it and imply a different build.

| Suggested filename | Caption / alt text |
| --- | --- |
| beta2-desktop.png | Aero7 desktop with its factory taskbar and Recycle Bin. |
| beta2-start.png | Aero7 Start menu and searchable applications. |
| beta2-computer.png | File Explorer Computer view with friendly drive information. |
| beta2-libraries.png | File Explorer showing Documents, Music, Pictures and Videos libraries. |
| beta2-control-panel.png | All Control Panel Items in the five-column Aero7 layout. |
| beta2-screen-resolution.png | Aero7 Screen Resolution settings on the test display. |
| beta2-features.png | Turn Aero7 features on or off, including optional Programs Center Beta. |
| beta2-gadgets.png | Aero7 Desktop Gadgets gallery. |
| beta2-login-menu.png | Aero7 login screen with available session and accessibility controls. |
| beta2-lock-screen.png | Aero7 lock screen with fully visible Professional branding. |
| beta2-screenshot-saved.png | Screenshot saved notification after a rectangular capture. |

Retain original PNG downloads; responsive web copies may be optimized without
changing the depicted UI. Add real alt text and do not put essential instructions
only inside screenshots. Do not publish a missing asset link as if it exists.

**Local handoff integrity check, 22 September:** all 148 relative links across
this handoff, the release notes, pre-build checklist and QA status resolve. The
nine intermediate preview PNGs and four fresh-r3 preview PNGs match their
retained SHA-256 inventories and are all exactly 1920×1080. They remain labeled
QA/layout previews and do not fill the pending final-image asset directory.

## 8. Announcement draft — use only after approval

### Long announcement

**Aero7 Beta 2 is ready for testing**

Aero7 Beta 2 brings our dedicated desktop, Dolphin-based File Explorer,
Windows-inspired Control Panel and Desktop Gadgets together in a new test
release. The familiar taskbar, Start menu, login branding and screenshot
workflow are joined by clearer optional-feature controls.

There are two installation images. **We recommend the Offline ISO**: it carries
the base installation package set, works without internet during setup and
avoids package-download delays. The smaller Online ISO remains available for
people with a reliable connection. Both use the normal repositories for later
updates.

Programs Center Beta is optional rather than part of every fresh installation.
Find it through **Turn Aero7 features on or off** in Start or Control Panel.
The release also includes diagnostic collection to help us investigate install
and desktop problems; review logs for personal information before sharing.

This is beta software. Back up your files, read the known limitations and test
on a spare machine or VM. Aero7 is an independent Linux project, not Microsoft
Windows. Thank you to everyone testing and reporting reproducible problems.

**Downloads:** [INSERT WEBSITE RELEASE URL]
**Release notes and known limitations:** [INSERT WEBSITE NOTES URL]
**Installation/help:** [INSERT VERIFIED GUIDE URL]

### Short announcement

Aero7 Beta 2 is ready for testing: dedicated Aero7 Desktop, Dolphin-based File
Explorer, Control Panel, Gadgets and optional Programs Center Beta. Two ISOs are
available; Offline is recommended and installs the base system without internet.
Back up first—this is beta software. Downloads and notes: [WEBSITE URL]

### Pre-release alternative, if the gate is still incomplete

The rebuilt Aero7 Beta 2 online and offline test candidates have passed fresh
installation and desktop acceptance. The Offline ISO remains the recommended
option. Downloads will be announced only after the owner approves the final
build and the website-hosted files are verified; Beta 2 is not available yet.

## 9. Release gate and website launch checklist

### Source and documentation destinations

These destinations follow the configured project repositories. Check that each
published wiki page exists and contains the approved revision before launch;
local documentation edits are not automatically public.

Read-only checks on 8 September confirmed all six repository destinations below
and the three wiki Git repositories exist. File Explorer is registered on GitHub
as a fork of `KDE/dolphin`. This verifies the links and relationship only; final
published wiki revisions and screenshots still need review after approval.

- [Aero7 source and issues](https://github.com/aero7-open-project/aero7)
- [Desktop wiki](https://github.com/aero7-open-project/aero7-desktop/wiki)
- [File Explorer wiki](https://github.com/aero7-open-project/aero7-file-explorer/wiki)
- [Control Panel wiki](https://github.com/aero7-open-project/aero7-control-panel-/wiki)
- [Programs Center source](https://github.com/aero7-open-project/aero7-programs-center)
- [Package repository](https://github.com/memegeko/aero7-repo)

Use project website download URLs for ISO buttons, not repository archive links.

### Launch checks

- [x] Both exact final local images pass embedded-package/checksum verification.
- [x] The exact final online image passes fresh installation, OOBE and normal
  reboot/login.
- [x] The exact final offline image passes fresh installation with no network
  adapter attached.
- [x] First-login collector manifests pass with zero failed units/coredumps.
- [x] Optional Programs Center installs and removes through the feature manager.
- [x] Login/lock branding, SDDM accessibility and session selection pass.
- [x] Shutdown and logout complete without the delayed Plasma-close warning.
  Native KWin evidence covers normal completion, cancellation, explicit
  override, power-off and cold start; the selected 7.3 source also passes the
  11-result notification and six-result no-notification control-flow suites.
- [x] Taskbar, Start, Explorer, Control Panel and screenshot checks pass.
- [x] Multi-output and recovery/failure-path coverage is recorded accurately.
  Three virtual outputs, output disable/re-enable, automatic layout repair,
  shell crash recovery and disconnected transaction recovery are documented;
  physical multi-monitor hardware is explicitly outside the VM claim.
- [x] Physical-hardware limitations and untested backends are explicitly listed.
  The release copy excludes legacy BIOS, Secure Boot, physical GPU/hotplug,
  physical multi-monitor, unsupported voice control and unavailable optional
  backends from the tested claim.
- [ ] Release package provenance/signing and repository promotion are verified.
- [x] Final artifact table and local checksum file are complete. Exact local
  bytes and hashes are recorded in the final-media acceptance report; hosted
  URLs and download-back verification remain separate checks.
- [ ] Website owner provides the final URLs and explicit publication approval.
- [ ] Uploaded ISO downloads match the published byte sizes and SHA-256 values.
- [ ] Download cards, checksum links, mobile layout and help links are tested.
- [ ] Announcement placeholders are replaced and claims match the evidence.

For the current run see
[r10 current-stack acceptance](release-evidence/2026-09-08-r10-current-stack-acceptance.md).
Earlier baselines are recorded in
[r9 exact-media acceptance and checklist](release-evidence/2026-09-06-r9-time-final-media.md),
[earlier r8 media acceptance](release-evidence/2026-09-06-r8-final-media-acceptance.md)
and the [earlier corrected-candidate evidence](release-evidence/2026-09-05-fixed-candidate-acceptance.md).
Do not describe unit tests, screenshots or older-image success as proof of a
complete final-image acceptance pass. Never claim every possible bug is fixed.
