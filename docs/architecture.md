# Architecture

```text
Archiso boot
  -> systemd on TTY1
  -> Cage kiosk compositor
  -> aero7-installer (Qt 6/QML)
       -> guarded live state machine (default)
       -> aero7-install-backend
            -> validate immutable disk fingerprint
            -> whole-disk GPT + ESP + ext4, or guarded advanced GPT target
            -> pacstrap complete Arch/Plasma dependency set
            -> signed Aero7 binary packages
            -> pinned PlymouthVista theme and initramfs
            -> systemd-boot

First installed boot
  -> aero7-oobe.service on TTY1
  -> Cage
  -> aero7-installer --oobe
       -> aero7-oobe-backend
            -> create user and password
            -> hostname/time/update preference
            -> guarded Aero7-shell image-mode stages
                 -> Plasma theme, layout, and wallpaper
                 -> SDDM and deferred first-login helper
                 -> Fastfetch, management commands, and validation
            -> configure one-time SDDM autologin and self-disabling cleanup timer
            -> disable OOBE, enable SDDM
       -> automatic Welcome and Preparing Desktop pages
       -> full-screen fade
       -> start SDDM without another reboot
       -> automatic first desktop login
```

In simulation mode only, the controller changes from the installer state
machine to the OOBE state machine after the restart countdown. Automatic
transition pages reproduce the applying-settings, video-check, Welcome, and
Preparing Desktop phases before a non-functional desktop preview. Live-install
mode performs one required reboot from the installation media into the newly
installed system. After personalization, it transitions directly from OOBE to
the real Plasma desktop without a second reboot or manual Continue button.

## Trust boundaries

QML never runs partitioning commands. The unprivileged UI sends a complete disk
and target fingerprint plus an exact confirmation path to one narrow backend.
Immediately before modifying anything, the backend repeats `lsblk`, mount,
live-media, VM, size, model, serial, read-only, removable, GPT, UUID, and sector
geometry checks. Advanced mode then saves a private restorable partition-table
dump. Unallocated, replace-one-partition, and NTFS-shrink plans are fixed in the
backend; arbitrary partitioning commands never cross the UI boundary.

The ISO service runs as root because Arch installation is privileged. This is
not carried into the installed desktop. OOBE also runs only for the first boot
and permanently disables itself after the Aero7-shell stages finish. Its SDDM
autologin drop-in is temporary: a 45-second one-shot timer removes it and
disables itself, returning later boots to password authentication. Image mode
requires root, an exact guard token, a ready provenance marker, and a validated
unprivileged target account. It creates no passwordless sudo policy.

## Source consumption

`scripts/build-iso.sh` reads `sources.lock`, verifies the source clone's origin,
HEAD, and porcelain-status digest, then copies a runtime-only subset plus the
public Aero7 repository key into the temporary Archiso profile. Git metadata,
tests, caches, and development output are excluded. The build does not execute
the source installer or write into the clone.

Before Archiso removes temporary build trees or begins image construction,
`scripts/check-build-space.py` performs a read-only capacity check. Its conservative
workspace floor is 16 GiB plus three times the prepared profile's apparent size,
covering live-root, SquashFS and staged-image coexistence. A separate output
filesystem also needs 4 GiB plus the profile size for the final copy. Root-reserved
blocks are excluded. Missing/unreadable paths fail closed; the check creates or
deletes nothing. This is a minimum staging safeguard, not a guarantee against
concurrent disk use or package growth. A shortage stops before cleanup so previous
images and diagnostics remain available for an explicitly reviewed cleanup or
relocation. It does not check or change the user's installation target disk.

Aero7-shell remains an independent repository with its own history, tests,
release decisions, and update path. The ISO repository owns only the installer,
OOBE, boot media, and the exact shell revision pin. Updating the desktop requires
a tested Aero7-shell commit first, followed by a deliberate `sources.lock`
change here; shell source is never vendored or maintained in the ISO tree.

## Display model

The QML root fills the output with original background artwork. Installer panels
are placed on a 1024×768 logical canvas and uniformly scaled, preserving spacing
and hierarchy at all required resolutions. Controls support mouse, keyboard
focus, Tab/Shift+Tab, Enter, Escape, and visible focus indicators.

The frontend passes the controller and capture/documentation settings using
`QQmlApplicationEngine::setInitialProperties`, not ambient context globals.
`Main.qml` requires a controller. Its Loader supplies the same controller and
documentation mode when constructing each screen. All screens inherit the
`InstallerScreen` input contract, directly or through `SetupPage`.
`GlassWindow` exposes `backEnabled` and `backRequested`; its presentation does
not reach into the installer controller itself. Root IDs and bound delegate
scopes make dependencies visible to standalone `qmllint`.

The installer-help CTest suite also checks the complete 20-screen resource set,
missing-controller rejection, forward/reverse loading in one engine, both
capture resolutions and documentation modes, navigation buttons, help dialogs
and live time-preview updates. These are simulation tests; real installation,
OOBE and session handoff still require fresh-VM acceptance on the final ISOs.

The completed-stage check mark and desktop-preview Recycle Bin are unchanged
PNG copies from the selected AeroThemePlasma icon package. Their provenance,
hashes, notices and QML resource references are tested. The UI test suite fails
on native rendering warnings as well as QML engine diagnostics; this prevents
an SVG parser warning from being mistaken for a clean rendering pass.
