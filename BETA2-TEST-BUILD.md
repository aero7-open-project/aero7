# Aero7 Beta 2 Online and Offline Test ISOs

This local, unpublished test release produces two installation images from the
same guarded Aero7 Beta 2 source and pinned package set:

> **Recommended:** use the offline ISO for normal installations. It contains
> the complete package set, avoids mirror and download delays during setup,
> and is substantially faster and more reliable on slower laptops. Use the
> online ISO only when its smaller download size matters and a stable Internet
> connection is available throughout installation.

- `aero7-beta2-online-*.iso` is the smaller normal installer. It retrieves the
  current Arch Linux and Aero7 repository packages during installation.
- `aero7-beta2-offline-*.iso` embeds the complete dependency closure used by
  the installer plus a checksum-pinned local pacman repository database. It
  installs the base system and Aero7 desktop without an Internet connection,
  while retaining the configured public repositories for normal updates after
  installation.

Both images use the guarded Aero7 installer and the current Beta 2 desktop and
package manifests. The build deliberately uses a separate, pinned shell input clone
and does not read from the legacy local `aero_desktop` working tree.

The current candidate embeds the selected packages from signed Aero7 repository
build `20260923T180513Z-ce604b74debf` at `https://aero7.org/repo/$arch`.
The complete 23-package repository database, its detached signature and every
selected package signature were verified against fingerprint
`72C79ABBBBE96446DD3324042694BFE1090F4FD6` before candidate assembly. The
supplemental Plasma, Qt, KWin, Spectacle, KWallet and optional encrypted-vault
packages remain checksum-pinned local Beta 2 inputs because they are not part
of that repository release.

The pre-update package transaction explicitly installs `cups` and
`baloo-widgets`, which are required by the embedded Control Panel and File
Explorer builds. A dependency-closure test reads the real package metadata and
fails the build if another embedded package dependency would be missing from
the installed target.

Control Panel r56 makes **Turn Aero7 features on or off** visible immediately
in the Programs and Features sidebar, fixes the Programs-category task so it
opens the Optional Features manager instead of silently doing nothing, publishes
the same searchable entry in the Start menu, verifies the retained offline
package before every transaction, and limits authorization to the signed-in
local administrator.

AeroTheme `6.7.0_752.r8c7d820-3` carries the corrected, unclipped Aero7
Professional branding for both SDDM and the Plasma lock screen. Aero7 Desktop
0.2.0-36 pins File Explorer with
the case-correct `org.aero7.FileExplorer.desktop` identity and migrates the
broken lowercase factory pin written by earlier test images.

File Explorer 25.12.3-56 gives both the launcher and the running window the stable
`File Explorer` name and uses the project-pinned `system-file-manager` artwork
from AeroThemePlasma Icons for its application icon. No host icon-theme lookup
or newly drawn replacement icon is used. Its startup class matches the Wayland
application ID so the running window groups into the pinned taskbar shortcut.

The Internet Explorer compatibility launcher is built from the current Aero7
Desktop companion source. Its namespaced application and action icons are the
approved files from the pinned AeroThemePlasma icon pack, including the
pack-provided `internet-web-browser` application artwork.

Computer Management deliberately does not ship the standalone Device Manager
launcher. This gives `/usr/share/applications/aero7-device-manager.desktop` one
package owner and allows the complete Beta 2 package set to install in a single
transaction.

This is test media, not a release. Do not publish it until installation,
hardware, multi-monitor, remote-filesystem, screenshot, and failure-path testing
has passed.

This physical-install diagnostic build also enables persistent journald storage
and installs an automatic collector. After OOBE, the selected user's desktop
contains `Aero7 Physical Install Logs`. System data is refreshed every ten
minutes and desktop-session data every five minutes. The folder contains a
plain-language privacy notice, a manual refresh launcher, per-boot sections,
and a SHA-256 manifest so the complete folder can be returned after testing.

The collector includes installer and partition-action output, the complete
live-media installation journal, the current and previous installed-system
boot journals, warnings, kernel messages, failed services, Aero7 and
display-manager journals, hardware and firmware inventory, disk health,
network state, installed-package and integrity reports, user-session state,
small application log files, and crash summaries. It excludes passwords,
NetworkManager connection profiles, browser data, user documents, and full
core-memory images.

The exact 23 September candidate pair and its clean-install results are recorded
in the [self-hosted repository acceptance report](docs/release-evidence/2026-09-23-self-hosted-repository-candidate-acceptance.md).
Both candidates remain unpublished pending the Friday release decision.
