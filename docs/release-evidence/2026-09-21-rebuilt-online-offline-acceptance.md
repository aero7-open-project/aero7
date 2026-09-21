# 21 September 2026 rebuilt online/offline acceptance

## Scope

This pass validates the rebuilt Beta 2 **test candidates**. It does not approve
publication, assign final public filenames or prove compatibility with every
physical graphics, storage, network or multi-monitor configuration.

## Exact test artifacts

| Variant | Internal test filename | Bytes | Display size | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Offline | `aero7-beta2-offline-2026.09.21-x86_64.iso` | 3,406,368,768 | 3.2 GiB | `068fe95698f86084e7f54d11dfc6dbe9031937e2085d81d58e76b6c7b2691589` |
| Online | `aero7-beta2-online-2026.09.21-x86_64.iso` | 1,604,009,984 | 1.5 GiB | `845c4c9dd4114ca8bfe7201aef7bc1e6ec74ca44cd12e4f5729dfca40bd6a38d` |

`scripts/verify-release.sh` passed against both exact files. These hashes are
engineering evidence only and must not be copied to a public download page as
final release hashes.

## Fresh installation and system checks

Both candidates were installed onto new virtual disks and completed setup,
OOBE, reboot and password login. The offline guest had no network dependency;
the online installer log records its package downloads. Both installed systems
reported:

- zero failed system units and zero failed user units;
- active firewalld;
- no collected coredumps;
- Desktop `0.2.0-33`, File Explorer `25.12.3-55`, Control Panel `0.1.0-55`
  and AeroThemePlasma Desktop `6.7.0_742.r9c2d850-65`;
- a collector manifest with 144 of 144 listed files verified (145 files total).

The retained journal warnings were reviewed. The remaining `xkbcomp` diagnostics
identify themselves as non-fatal. No Explorer D-Bus filename mismatch or old
implicit-handler QML warning reappeared.

## Graphical and workflow acceptance

- The SDDM and lock-screen Aero7 Professional brand remains fully visible.
- The lower-left SDDM Ease of Access dialog opens, and its desktop-session
  selector includes Aero7, AeroThemePlasma and Plasma choices.
- The factory taskbar File Explorer shortcut opens Aero7 File Explorer with the
  packaged icon and correct application name.
- Start search finds **Turn Aero7 features on or off**.
- Programs Center Beta is absent by default, installs after administrator
  approval, and removes again successfully. The encrypted vault is off by
  default, as documented.
- Meta+Shift+S opens rectangular selection without an editor window. Releasing
  the mouse saves a PNG under `Pictures/Screenshots`, copies actual image pixels
  to the clipboard and shows a saved notification. Clicking the notification
  opens Photo Viewer; Ctrl+V pastes the image into Paint.

## Remaining release boundary

The bug-test pass for these rebuilt candidates is complete. A final release
still requires owner approval, a final build from the approved commits,
exact-media checksum verification, website-hosted download verification and
explicit publication approval. Physical GPU/hotplug and physical multi-monitor
coverage remain limitations and must not be advertised as tested.
