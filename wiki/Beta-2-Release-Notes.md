# Aero7 Beta 2

Released 22 September 2026. GitHub contains the tagged source and release notes
without ISO attachments. Official installation media and checksum information
are distributed through the [Aero7 website](https://aero7.miku-dayo.com/).

## Choose an image

The offline ISO is recommended. It contains the complete base installation
package set, works without internet during setup and avoids mirror/download
delays. The online ISO is a smaller initial download but requires a stable
connection throughout package installation. Both use the normal repositories
for later updates.

| Variant | Filename | Exact bytes | SHA-256 |
| --- | --- | ---: | --- |
| Offline — recommended | `aero7-beta2-offline-2026.09.22-x86_64.iso` | 3,407,151,104 | `f44c52bf8171fd2842e2c6150909e9ca70a577f4e3ac9f6444baeea45f1676a5` |
| Online | `aero7-beta2-online-2026.09.22-x86_64.iso` | 1,604,804,608 | `e1744b3be9692af6252bfdc42b83a1bc4c309f33f300771dd3b26cfeacafc936` |

Verify the complete checksum of the exact file you download. Do not use
unofficial mirrors. See [Installation](Installation.md) for USB, VM and safety
instructions.

## Highlights

- Aero7 Desktop Wayland session with AeroThemePlasma and Plasma fallbacks
- Windows-inspired factory desktop, taskbar, Start menu and window behavior
- Corrected login/lock branding, accessibility controls and session selection
- Windows-style `Meta+Shift+S` rectangle capture with automatic save,
  clipboard image data and an actionable notification
- Dolphin-based Aero7 File Explorer with Libraries, Computer, Recycle Bin,
  common dialogs and friendly storage presentation
- 45-item Control Panel and Linux-backed settings pages
- Searchable **Turn Aero7 features on or off** manager
- Optional Programs Center Beta and encrypted Credential Vault, both off by
  default
- Desktop Gadgets with improved layering, slideshow and feed behavior
- Firewalld defaults for fresh installations while existing UFW setups remain
  unchanged
- User approval before installing updates, with update checks configurable

## Validation record

Both exact images completed clean VM installation, OOBE, login, reboot and
desktop acceptance at 1920×1080. The offline image was installed with no
network adapter; the online image verified networking and synchronized time.
The checks included SDDM accessibility/session selection, File Explorer,
optional-feature install/removal, PolicyKit readiness and the complete
screenshot save/clipboard/notification path.

The detailed package versions, checks and scope are in the repository's
[full Beta 2 release notes](https://github.com/aero7-open-project/aero7/blob/beta/docs/BETA2-RELEASE-NOTES.md).

## Known boundaries

Aero7 remains beta software. Only x86-64 UEFI is supported. Secure Boot,
legacy BIOS, full-disk encryption and unrestricted manual partitioning are not
available. Physical GPU/hotplug and broad hardware compatibility are not
claimed from VM testing. Back up important files and disconnect unrelated
drives before installation.

After an upgrade that changes theme or icon packages, sign out and back in if
an existing taskbar icon remains stale.
