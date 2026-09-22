# Screenshot Capture Details

## Environment

| Property | Value |
| --- | --- |
| Capture date | 22 September 2026 |
| Source image | `aero7-beta2-offline-2026.09.22-x86_64.iso` |
| Source SHA-256 | `f44c52bf8171fd2842e2c6150909e9ca70a577f4e3ac9f6444baeea45f1676a5` |
| Install state | Fresh whole-disk installation, completed OOBE, fresh account |
| Image size | 1920×1080 original PNG framebuffer captures |
| Desktop mode | Virtual-1, 1920×1080, scale 1 (100%) |
| Hypervisor | QEMU/KVM, q35, UEFI/OVMF |
| Guest resources | 4 virtual CPUs, 8 GiB RAM, VirtIO disk/network/display |
| Session | Aero7 Desktop on KWin Wayland |
| Capture method | QMP screendump of the actual guest framebuffer |
| Image policy | No cropping, resizing, painted corrections, generated replacements or composites |

The independent Online ISO clean-install test completed against the same final
desktop payload. Its SHA-256 is
`e1744b3be9692af6252bfdc42b83a1bc4c309f33f300771dd3b26cfeacafc936`.

## Installed versions

| Package | Captured version |
| --- | --- |
| aero7-desktop | 0.2.0-33 |
| aero7-file-explorer | 25.12.3-55 |
| linux-control-panel | 0.1.0-55 |
| aero7-gadgets | 3.0.0-25 |
| aero7-internet-explorer | 0.1.0-5 |
| aerothemeplasma-desktop-git | 6.7.0_742.r9c2d850-65 |
| plasma-workspace | 6.7.4-3.2 |
| kwin | 6.7.4-7.3 |
| qt6-base | 6.11.2-3.1 |

## Capture procedure

- Booted the exact final Offline ISO in a new 20 GiB copy-on-write disk.
- Completed the supported whole-disk installer path and every OOBE page.
- Created the disposable `beta2demo` documentation account.
- Allowed the first desktop to settle before capturing the factory layout.
- Opened shell surfaces and applications through their installed launch paths.
- Logged out to the installed SDDM theme for login, accessibility, session and
  on-screen-keyboard captures.
- Exercised `Meta+Shift+S` and captured the resulting saved notification.
- Checked every promoted PNG as exactly 1920×1080 and generated SHA-256
  manifests for the wiki and website handoff directories.

No password-entry frame, deliberate failure dialog or private log output is
included in the promoted gallery.

## Verification and reuse

The [SHA-256 manifest](images/beta2-1080p/SHA256SUMS.txt) identifies every
gallery PNG. Website-ready copies and their own manifest are stored under
`docs/website-assets/beta2-final-1080p/`.

Keep the original aspect ratio, use meaningful alt text and do not combine UI
from different captures. Optimized responsive copies are acceptable if the
original PNG remains available. The Offline ISO is recommended for release
documentation because it installs without package downloads; the Online ISO
remains a smaller network-dependent alternative.

The screenshots verify visible surfaces only. Hardware coverage, recovery,
rollback, suspend/resume, multi-monitor behavior and destructive disk paths
remain governed by the release QA evidence rather than this gallery.
