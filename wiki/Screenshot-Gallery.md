# Aero7 Beta 2 Screenshot Gallery — 1920×1080

These are unedited QEMU/KVM framebuffer captures from a **fresh installation
of the final Aero7 Beta 2 Offline ISO on 22 September 2026**. Every image is an
original 1920×1080 PNG captured at 100% scale. The Online ISO uses the same
desktop packages; its separate clean-install acceptance is recorded in the
Beta 2 QA evidence.

See [Capture Details](Screenshot-Capture-Details) for the exact ISO checksum,
package versions, VM profile and reuse rules. Click any image for the original
PNG.

## Desktop and Start

[![Fresh Aero7 Beta 2 desktop](images/beta2-1080p/desktop.png)](images/beta2-1080p/desktop.png)

The fresh account starts with the factory taskbar order and only the Recycle
Bin plus the physical-install diagnostic folder on the desktop.

[![Aero7 Start menu](images/beta2-1080p/start-menu.png)](images/beta2-1080p/start-menu.png)

The Start menu exposes search, Libraries, Computer, Control Panel and the
installed application list without desktop edit mode.

## Control Panel and features

[![Control Panel category view](images/beta2-1080p/control-panel-home.png)](images/beta2-1080p/control-panel-home.png)

[![All Control Panel Items in five columns](images/beta2-1080p/control-panel-all-items.png)](images/beta2-1080p/control-panel-all-items.png)

The full 45-item Windows-style applet layout is shown using the packaged Aero7
icons and routes to Linux-backed settings.

[![Screen Resolution at 1920×1080](images/beta2-1080p/screen-resolution.png)](images/beta2-1080p/screen-resolution.png)

The displayed mode is the guest's actual KScreen mode, not a resized image.

[![Turn Aero7 features on or off](images/beta2-1080p/optional-features.png)](images/beta2-1080p/optional-features.png)

Programs Center Beta and Encrypted Credential Vault are optional and off by
default. Installed, unavailable and hardware-dependent states are reported by
the real feature backend.

## File Explorer

[![Computer integrated into File Explorer](images/beta2-1080p/explorer-computer.png)](images/beta2-1080p/explorer-computer.png)

[![Aero7 Libraries](images/beta2-1080p/explorer-libraries.png)](images/beta2-1080p/explorer-libraries.png)

[![Documents Library Properties](images/beta2-1080p/library-properties.png)](images/beta2-1080p/library-properties.png)

Explorer uses the Aero7 name and icon, provides Windows-style Libraries and
Computer views, shows friendly drive labels, and filters implementation-only
mounts. Library Properties identifies the real Linux folder that backs the
Library; it does not pretend the filesystem is NTFS.

## Desktop Gadgets

[![Aero7 Desktop Gadget Gallery](images/beta2-1080p/gadget-gallery.png)](images/beta2-1080p/gadget-gallery.png)

The first gallery page contains Calendar, Clock, CPU Meter, Currency, Feed
Headlines, Picture Puzzle, Slide Show and Weather. The gallery uses packaged
assets and does not depend on a host icon theme.

## Lock, login and accessibility

[![Aero7 lock screen](images/beta2-1080p/lock-screen.png)](images/beta2-1080p/lock-screen.png)

[![Aero7 SDDM login screen](images/beta2-1080p/login-screen.png)](images/beta2-1080p/login-screen.png)

Both views show the complete Aero7 Professional branding at 1920×1080.

[![Ease of Access at login](images/beta2-1080p/login-ease-of-access.png)](images/beta2-1080p/login-ease-of-access.png)

[![Desktop-environment selector](images/beta2-1080p/login-session-menu.png)](images/beta2-1080p/login-session-menu.png)

[![On-screen keyboard](images/beta2-1080p/login-keyboard.png)](images/beta2-1080p/login-keyboard.png)

The lower-left Ease of Access control provides Narrator, Magnifier, High
Contrast, On-Screen Keyboard, Sticky Keys and Filter Keys toggles. Its desktop
selector includes Aero7 Desktop, Safe Mode and the Plasma fallback sessions.

## Screenshot workflow

[![Screenshot saved notification](images/beta2-1080p/screenshot-saved.png)](images/beta2-1080p/screenshot-saved.png)

`Meta+Shift+S` starts rectangular selection. Releasing the pointer closes the
overlay, saves a PNG under `Pictures/Screenshots`, copies the image to the
clipboard and shows the clickable saved notification without opening the
Spectacle editor window.

## Scope

These images verify the visible final-ISO surfaces in this VM. They do not
claim pixel-perfect Windows identity, physical GPU compatibility, every scale
factor, multi-monitor hardware acceptance or universal Windows application
compatibility. Read [Testing and Release](Testing-and-Release) and
[Known Issues](Known-Issues) before publishing release claims.
