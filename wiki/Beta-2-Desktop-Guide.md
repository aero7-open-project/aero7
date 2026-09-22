# Beta 2 Desktop Guide

This guide describes the released Beta 2 desktop. Read
[Beta 2 Release Notes](Beta-2-Release-Notes) and download official installation
media only through the [Aero7 website](https://aero7.miku-dayo.com/).

## Choose an installation image

| Image | Best use | Internet during installation | Later updates |
| --- | --- | --- | --- |
| Offline Beta 2 | Recommended, particularly for slow laptops and unreliable connections | Complete base install package set is carried on the image | Uses the normal repositories and needs internet for new updates |
| Online Beta 2 | When a smaller ISO download is more important | Required throughout package download/install | Same normal repository update path |

Offline installation is normally faster because it avoids downloading the
installation package set from mirrors. It cannot make a slow USB drive, CPU,
or disk fast, and there is no fixed installation-time promise. The two images
are intended to install the same Aero7 desktop, not different editions.
Optional features added later may still need downloads.

## First login

The default is **Aero7 Desktop**, a dedicated session using KWin/Wayland and
KDE infrastructure. The taskbar starts with Start, Command Prompt, File
Explorer, and the Internet Explorer-compatible browser entry. The normal
clean desktop has Recycle Bin at the upper-left. Diagnostic test media also
provides **Aero7 Physical Install Logs**.

The SDDM lower-left menu offers installed session choices and an on-screen
keyboard. Aero7 Safe Mode is the same shell with a restricted effects policy.
AeroThemePlasma and Plasma can remain explicit fallback sessions; they are not
silently substituted by normal shell recovery. The lock screen unlocks the
current session, rather than choosing a different desktop.

The SDDM menu is not yet the complete Windows 7 pre-login accessibility
checkbox dialog. See the
[login/defaults guide](https://github.com/aero7-open-project/aero7-desktop/wiki/First-Login-and-Defaults)
for the precise boundary.

## Everyday applications

| Component | What to use it for | Detailed documentation |
| --- | --- | --- |
| Aero7 Desktop | Start, taskbar, window grouping/previews, desktop menus, tray, notifications, and recovery | [Desktop handbook](https://github.com/aero7-open-project/aero7-desktop/wiki) |
| File Explorer | Files, Libraries, Computer, Network, Recycle Bin, properties, and file operations | [Explorer handbook](https://github.com/aero7-open-project/aero7-file-explorer/wiki) |
| Control Panel | The 45 familiar applet entry points and 71 searchable desktop settings | [Control Panel handbook](https://github.com/aero7-open-project/aero7-control-panel-/wiki) |
| Desktop Gadgets | Calendar, Clock, CPU Meter, Currency, Feed Headlines, Picture Puzzle, Slide Show, Weather, and Media Center | [Gadget guide](https://github.com/aero7-open-project/aero7-desktop/wiki/Desktop-Gadgets) |
| Internet Explorer compatibility | Familiar browser launcher and taskbar grouping backed by a maintained browser | [Included components](https://github.com/aero7-open-project/aero7-desktop/wiki/Included-Components) |
| Computer Management | Administration routes for devices, services, logs, users/groups, tasks, shares, and storage | [Project](https://github.com/aero7-open-project/aero7-computer-management) |
| Device Manager | Real Linux hardware/device information and supported administration | [Project](https://github.com/aero7-open-project/aero7-device-manager) |
| Programs Center Beta | Optional graphical software installation/removal/update frontend | [Optional Features](Optional-Features) |

Familiar Windows names do not install Windows services or drivers. HomeGroup
means the supported Samba/SMB sharing route, Defender uses ClamAV, updates use
pacman, and Remote Desktop is a client feature, not a remote-login server.

## Capture and share a screenshot

Press **Meta+Shift+S**, drag a rectangle, and release. The selector closes
without opening the Spectacle editor. Aero7 saves a PNG below your configured
Pictures directory in **Screenshots**, copies image data to the clipboard,
and sends a **Screenshot saved** notification. Click it to open the file, or
paste into an image-capable application with **Ctrl+V**. Esc cancels.

See [Screenshots and Clipboard](https://github.com/aero7-open-project/aero7-desktop/wiki/Screenshots-and-Clipboard)
for folder behavior and troubleshooting. The wiki's full-screen gallery is
captured directly from a VM framebuffer; it is not a set of region-capture
test results.

## Optional software and services

Search Start for **Turn Aero7 features on or off**, or open it through
Programs and Features. Desktop Core is required. Programs Center Beta is
optional and the Beta 2 installer retains its checksum-verified package for
offline re-enabling. The [feature reference](Optional-Features) explains every
toggle, dependencies, authentication, hardware requirements, and retained data.

Speech Recognition is not offered as a working feature; speech synthesis and
screen reading are different capabilities. CardSpace is not installable.

## Test and report honestly

The [screenshot gallery](Screenshot-Gallery) records a fresh installation of
the final offline ISO at 1920×1080/100% scale. It is not physical GPU
certification or a claim that every optional backend works on all hardware.

After a physical-install issue, use **Collect Aero7 Logs Now** when available,
review the resulting diagnostic folder for private information, and provide
it with exact steps and the failure time. Read [Recovery and Logs](Recovery-and-Logs)
before modifying the failed installation.
