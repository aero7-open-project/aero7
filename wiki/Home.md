# Aero7 Wiki

<p align="center">
  <img src="https://raw.githubusercontent.com/aero7-open-project/aero7/beta/installer/assets/aero7-logo-circle.png" width="150" alt="Aero7 logo">
</p>

Welcome to the handbook for **Aero7**, an independent Arch Linux-based operating
system with a Windows-7-era-inspired installer and KDE Plasma 6 Wayland desktop.

Visit the [official Aero7 website](https://aero7.miku-dayo.com/) for project
news, downloads, screenshots, and an overview of the complete system.

[![Fresh Aero7 Beta 2 desktop at 1920×1080](images/beta2-1080p/desktop.png)](Screenshot-Gallery)

> **Beta 2 supports x86-64 UEFI PCs and virtual machines.** The guarded
> installer accepts non-removable SATA, NVMe, MMC, and VirtIO disks. Back up
> important data, disconnect unrelated disks, and verify the selected disk:
> Beta software and partition changes can still cause data loss.

> **Beta 2 is NOT publicly released.** Remaining bugs and stability checks
> are still being worked on. The September 22 source tag and local ISO
> checksums document previous engineering work, not a public launch.
> The official release date is to be announced.

## Start here

| I want to… | Read… |
| --- | --- |
| Read Beta 2 candidate installation guidance | [Installation](Installation.md) |
| Review draft Beta 2 release notes | [Beta 2 Release Notes](Beta-2-Release-Notes.md) |
| Learn the Beta 2 desktop and image choices | [Beta 2 Desktop Guide](Beta-2-Desktop-Guide) |
| Check whether my VM or test PC is supported | [System Requirements](System-Requirements.md) |
| Understand every setup page | [Installer Guide](Installer-Guide.md) |
| Learn what happens after restart | [First Boot and OOBE](First-Boot-and-OOBE.md) |
| See which programs are included | [Included Software](Included-Software.md) |
| Understand optional components | [Aero7 Optional Features](Optional-Features.md) |
| Browse the current interface | [Screenshot Gallery](Screenshot-Gallery.md) |
| Fix a failed or black-screen boot | [Troubleshooting](Troubleshooting.md) |
| Open the recovery console | [Recovery and Logs](Recovery-and-Logs.md) |
| Review Beta limitations | [Known Issues](Known-Issues.md) |

## Technical documentation

- [Architecture](Architecture.md)
- [Security and Disk Safety](Security-and-Disk-Safety.md)
- [Building the ISO](Building-the-ISO.md)
- [Testing and Release](Testing-and-Release.md)
- [Credits and Licensing](Credits-and-Licensing.md)
- [FAQ](FAQ.md)

## September Beta 2 test images — not publicly released

| | |
| --- | --- |
| Recommended offline file | `aero7-beta2-offline-2026.09.22-x86_64.iso` |
| Offline SHA-256 | `f44c52bf8171fd2842e2c6150909e9ca70a577f4e3ac9f6444baeea45f1676a5` |
| Smaller online file | `aero7-beta2-online-2026.09.22-x86_64.iso` |
| Online SHA-256 | `e1744b3be9692af6252bfdc42b83a1bc4c309f33f300771dd3b26cfeacafc936` |
| Firmware | x86-64 UEFI |
| Desktop | KDE Plasma 6 Wayland |
| Intended target | UEFI test PC or disposable QEMU/KVM VM |

These filenames and SHA-256 values identify **previously tested local images**.
They are not an announcement that Beta 2 downloads are available. The
[September GitHub source tag](https://github.com/aero7-open-project/aero7/releases/tag/v0.2.0-beta.2)
does not constitute the public Beta 2 release; watch the
[official website](https://aero7.miku-dayo.com/) for a later announcement.

## Project links

- [Official Aero7 website](https://aero7.miku-dayo.com/)
- [Aero7 repository](https://github.com/aero7-open-project/aero7)
- [Aero7-shell](https://github.com/memegeko/aero7-shell)
- [Signed Aero7 package repository](https://github.com/memegeko/aero7-repo)
- [Issue tracker](https://github.com/aero7-open-project/aero7/issues)

Aero7 is not affiliated with or endorsed by Microsoft Corporation. It does not
contain a licensed copy of Microsoft Windows.
