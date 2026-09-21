# Screenshot Capture Details

## Environment

| Property | Value |
| --- | --- |
| Capture date | 5 September 2026 |
| Image size | 1920×1080 pixels, original PNG framebuffer captures |
| Desktop mode | Virtual-1, 1920×1080 at approximately 60 Hz, scale 1 (100%) |
| Hypervisor | QEMU/KVM, q35, UEFI/OVMF |
| Guest resources | 4 virtual CPUs, 6 GiB RAM, virtio disk/network, QXL display |
| Session | Aero7 Desktop on KWin Wayland |
| Capture method | QMP screendump of the actual guest framebuffer |
| Original-image policy | No cropping, resizing, painted corrections, generated replacements, or composites |

These are documentation captures, not installation screenshots from a newly
released ISO. The final online/offline Beta 2 images remain a separate release
gate. The currently public release was checked during this pass and remains
Beta 1.

## Installed versions queried from the guest

| Package | Captured version |
| --- | --- |
| aero7-desktop | 0.2.0-25 |
| aero7-file-explorer | 25.12.3-32 |
| linux-control-panel | 0.1.0-37 |
| aero7-gadgets | 3.0.0-1 |
| aero7-internet-explorer | 0.1.0-4 |
| aerothemeplasma-desktop-git | 6.7.0_742.r9c2d850-38 |
| plasma-workspace | 6.7.4-1 |
| kwin | 6.7.4-5 |
| qt6-base | 6.11.1-1 |

The Beta 2 source and recipes can be newer than these local test archives.
Package-version output identifies the installed package database; it is not
a clean-system integrity attestation for this previously modified test VM.

## How the views were prepared

- Booted a separate copy-on-write overlay of the existing desktop test disk;
  the saved base disk was not modified.
- Upgraded Explorer, Control Panel, Gadgets, browser compatibility, and the
  desktop theme using existing local test packages. Old unowned development
  files conflicted with package installation and were replaced by the scoped
  package payloads in the disposable overlay.
- Rebuilt the desktop-entry cache and restarted the guest after updating.
- Removed obsolete Plasma gadget instances from this test profile. Stopped
  the native host for the clean desktop view, then opened the native gallery.
- Retained the account's existing recent applications, Libraries, and feature
  states. Added an Aero7-Guides folder containing two documentation files to
  the guest Documents directory during the Library walkthrough.
- Arranged/maximized application windows through normal window controls.
- Selected the installed `sddm-theme-mod` theme and disabled automatic login
  in an overlay-only SDDM configuration to capture the real greeter and menu.

The gallery therefore documents an arranged, updated test session. It does
not claim that every screen is the untouched factory state.

## Observations that remain visible

The existing profile has duplicate Internet Explorer Start entries and a
QTerminal label. Control Panel has repeated generic icons. Computer's lower
hardware-summary text is partly clipped. The older gadget gallery has clipped
thumbnail text. Programs Center Beta is unavailable because this VM lacks its
verified optional-package cache, while other feature states reflect earlier
testing. SDDM shows a blank display-name area for the saved account.

The login and lock-screen logos are fully visible in these 1080p captures.
That single observation does not certify all display scales, themes, or GPUs.

## Verification and reuse

Every new image was opened for visual inspection and checked as 1920×1080 PNG.
The [SHA-256 manifest](images/beta2-1080p/SHA256SUMS.txt) identifies the original
bytes. The Desktop, Explorer, and Control Panel wikis use byte-identical copies
of their relevant images. Older 1024×768 captures remain historical and are
not represented as new 1080p material.

The screenshots verify the visible surfaces only. No claim is made here about
offline installation, rollback, file-operation failure recovery, all applet
backends, every keyboard layout, suspend/resume, or physical multi-monitor
acceptance. See [Testing and Release](Testing-and-Release) for that boundary.
