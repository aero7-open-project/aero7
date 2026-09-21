# Aero7 Beta 2 release candidate

## Current status

Beta 2 source, package definitions, documentation, and wiki pages are ready for
review. Rebuilt online and offline test candidates passed fresh installation,
first-run setup, login, exported-log and graphical acceptance on 21 September.
The Beta 2 ISO files are not published yet: Beta 1 remains the current download
until the owner approves the final build and website publication.

## Choose the offline image when it is released

The offline ISO is the recommended Beta 2 installer. It contains the complete
base installation package set and works without internet during setup. Avoiding
package downloads can make installation much faster, especially on unreliable
connections; CPU, USB and disk speed still matter. The online ISO is smaller but needs a
stable connection for the complete package installation. Both use the normal
signed repositories for later updates.

## Highlights

- Aero7 Desktop Wayland session with AeroThemePlasma fallback
- Clean factory desktop and Windows 7-inspired taskbar layout
- Corrected SDDM and lock-screen branding with accessibility and session menus
- Windows-style rectangular screenshots on `Meta+Shift+S`
- Stable embedded Aero7 application icons across global icon-theme changes
- File Explorer identity, taskbar pinning, Recycle Bin settings, Libraries,
  Computer, common dialogs, and mount filtering improvements
- 45-item Control Panel and native Linux-backed settings pages
- Searchable **Turn Aero7 features on or off** manager
- Optional Programs Center Beta retained locally for offline enable/remove
- Renamed `aero7-device-manager` package with upgrade compatibility
- Persistent, privacy-scoped physical-install diagnostic folder on the desktop
- Separate online and complete offline installation paths

The full candidate package versions, technical changes, and release gate are in
the repository's
[Beta 2 release notes](https://github.com/aero7-open-project/aero7/blob/beta/docs/BETA2-RELEASE-NOTES.md).

## Still required before ISO publication

Rebuilt online and disconnected offline test candidates have completed
installation, first-run setup, reboot and password login with the selected
fixes. Their exported collector manifests verify 144 of 144 files with zero
failed user/system units and no collected coredumps. The notification-only
update scheduler and on/off setting pass policy/UI tests. Firewalld is active on
both fresh installs while existing UFW installations remain preserved during
upgrades. Dual-backend controls and per-connection Public/Home/Work choices are
implemented; physical-network packet validation remains a hardware limitation.
Home enables local mDNS discovery, not automatic file sharing or remote access.
Do not advertise unattended updates
or automatic trusted-network sharing as working features.

The latest local checks pass 124 installer/backend tests, three installer test
groups, 18 File Explorer test executables and five Desktop test groups. Paint's
rebuilt package passes its repeated-close regression and an offline-VM
save/reopen/Cancel/Discard/close check without new crash dumps. The theme package
also fixes splash/logout branding reverting during upgrades. These are local
QA results, not proof that the public repositories or final images contain them.

The screenshot follow-up passes all 15 theme tests and real offline-VM capture,
PNG saving, image paste, notification-open and Escape checks. Capture-process
crashes and nonzero exits now display an error instead of being treated as
cancellation. The local Spectacle `1:6.7.4-2` correction also makes internal
capture errors return failure and prevents background save errors from hanging.
Actual denied captures, successful PNG saves and unwritable-output checks passed;
Escape still exits successfully without saving. In the upgraded offline VM, a
failed-save notification offered Try Again, which reopened selection and led to
a successful capture and image-viewer launch. These tested error paths are fixed
locally; embedding the packages and final-image retesting remain open.
Normal Meta+Shift+S capture and Ctrl+V image paste into Paint also passed with
the exact corrected Spectacle package, not just the earlier backend.

Final-image desktop interactions, nondefault regional choices, recovery paths,
hardware coverage, package signing, embedded-content validation and exact image
checksums remain required. No Beta 2 ISO link or checksum is official until
the release gates and publication approval are complete.

After a theme/icon-package update, sign out and back in if an existing taskbar
icon appears blank. The upgrade test restored the icon after refreshing the
shell; seamless in-session icon refresh is not yet verified.
