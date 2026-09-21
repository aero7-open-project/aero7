# Beta 2 blocker fixes — local development follow-up

## Status: partial; release remains blocked

This follows `2026-09-05-online-offline-iso-acceptance.md`. The two 4 September
ISOs remain unchanged and failed acceptance. No new ISO has been assembled,
and no commit, push, upload, or release publication was performed.

The existing **online disposable test VM** was modified to prove fixes. The
offline guest remains the original failed-candidate installation, with no NIC.
These development checks do not replace clean installation from rebuilt media.
The attempted QEMU snapshot was unsupported by the writable firmware device;
no snapshot is claimed. Original ISOs and pre-change logs were retained.

## Implemented and checked

| Change | Evidence / result |
| --- | --- |
| Screenshot authorization identity | New Desktop session helper restores installed Spectacle metadata and retargets the legacy Print launcher to Snipping Tool. No permission checks are disabled. |
| Meta+Shift+S workflow | Actual region selection, release-to-save PNG, closed overlay without Spectacle editor, notification, image pasted into KolourPaint, and notification opening the saved PNG in the default viewer all demonstrated in the VM. |
| Normal default login session | Installer seeds SDDM's persistent last-session state separately from temporary autologin. After reboot, SDDM logged selection of `aero7.desktop` and `/usr/bin/aero7-session`, not Safe Mode. |
| Boot-loader seed permissions | Installer mounts the EFI partition with `fmask=0077,dmask=0077`. VM reboot confirmed `/boot` and its seed at mode 0700; the ordinary user's read check exits 1. Remount alone did not update existing FAT inode permissions. |
| Start-menu Features entry | Rebuilt Control Panel 0.1.0-38 appears as **Turn Aero7 features on or off** in Start search and opens its feature window. Optional-feature installation/removal lifecycle is still pending. |
| Fastfetch offline setup | Image-mode skips the pinned Shell stage's unnecessary repository lookup. A configuration-only adapter checks the installed package with `pacman -Q`, copies the existing profile, and preserves custom default config. VM invocation and Fastfetch JSON output both succeeded. A fresh no-NIC OOBE rerun remains pending. |
| Explorer library defaults | Removed automatic creation of the screenshot user's example `New Library`. Separate fresh/existing-profile tests verify four standard libraries and preservation of user libraries. No existing user folder is deleted. |
| SDDM blank username | Theme source now falls back to the login name when the full-name field is empty. The two affected paths were patched in the VM and the username became visible after reboot. This theme fix is not yet packaged. |
| Wrong-password feedback | Rechecked after a settled login screen: the incorrect-password message is visible, and subsequent valid login succeeds. No additional error-label change was necessary. |
| ISO artifact retention | Builder now retains older dated images and archives a same-filename collision with its checksum instead of deleting every older image of that variant. Shell syntax/static checks pass; actual build-time retention still needs a rebuild test. |

KWin's executable-based service lookup explains why repairing only the main
Spectacle desktop entry was insufficient: the legacy Print launcher also
directly executed Spectacle without its authorization metadata. See the
[KWin 6.7 service lookup implementation](https://github.com/KDE/kwin/blob/Plasma/6.7/src/utils/serviceutils.h).

## Local packages

Built with `makepkg --nodeps` using the existing host toolchain, not a clean
release chroot. These are **unsigned local QA candidates**, not signed public
repository artifacts. They installed together in the disposable guest without
dependency overrides or file overwrites. The manually deployed screenshot
helper was first moved to a named temporary backup because it was unowned;
the installed helper is now owned by the Desktop package.

| Package | SHA-256 |
| --- | --- |
| `aero7-desktop-0.2.0-27-x86_64.pkg.tar.zst` | `ee3bc4bfc57ec7b32a00c1f78c5ba021941aea6d4dcf0c60659ad12bc1e232f4` |
| `aero7-file-explorer-25.12.3-34-x86_64.pkg.tar.zst` | `c320740251ef36e8e28ccc70a550dea6e9d5163f9a3e1a77c66c60bcbc548899` |
| `linux-control-panel-0.1.0-38-x86_64.pkg.tar.zst` | `b6fc25d3c849c62703820f2a081a8fecd55938d927eae4be6581f43937bdf1b6` |

Packages are retained in `local-packages/` and referenced by
`config/beta2-local-packages.sha256`. Source snapshots and exact local recipes
are retained under `work/beta2-candidates/2026-09-05/` (ignored build workspace).
The Desktop and Explorer snapshots include uncommitted working-tree fixes;
the canonical public recipe pins have **not** been promoted to these snapshots.

## Automated checks

- Desktop static checks and 6/6 CTest groups passed, including screenshot
  identity migration and three installation profiles.
- File Explorer rebuilt; 18/18 CTest executables passed, including both new
  library-profile cases (14.23 seconds).
- Control Panel package check: 12/12 CTest cases passed.
- Installer/media checks passed against the refreshed three-package manifest:
  72 Python tests, ownership/checksum checks, pinned artwork, Shell parity,
  Python syntax, QML analysis, and ShellCheck. QML advisory warnings remain.
- Package publication-gate test passed. The pinned Shell source stayed clean.
- Modified repositories passed `git diff --check`.

## Evidence location

`/home/admin/VMs/aero7-beta2-acceptance-7Shb97/`

Important files in `online/`:

- `fix-05-selection.png`, `fix-06-saved.png`, `fix-08-paste.png`,
  `fix-09-notification-viewer.png`: screenshot behavior proof.
- `fix-12-reboot-proof.log`: selected normal session and seed read denial.
- `fix-13-fastfetch.log`: configuration-only adapter and successful Fastfetch.
- `fix-15-features-search.png`, `fix-18-features-window.png`: searchable entry
  and real window, not only a desktop-file inspection.
- `fix-17-installed-candidates.log`: installed versions and helper ownership.
- `fix-20-sddm-username.png`, `fix-21-sddm-error.png`: settled login feedback.
- `fix-22-packaged-capture.png`: capture overlay after candidate upgrade/reboot.

Build/test logs are copied into the evidence root with
`aero7-beta2-*-package.log`, `aero7-beta2-explorer-tests.log`,
`aero7-beta2-blocker-desktop-tests.log`, and
`aero7-beta2-candidate-installer-checks.log` names.

## Remaining before the release draft

1. Refresh the remaining candidate payloads, especially the theme (including
   the username fix and prior icon work), Gadgets, browser, Device Manager,
   Computer Management, and optional Programs Center. Their existing ISO
   manifest entries still refer to older packages. Validate the complete
   dependency closure and the intended optional-feature cache/database.
2. Obtain administrator authorization for ISO assembly on the host:
   `sudo -n true` currently fails with “a password is required.” No guest
   password was assumed to be the host's password. Public signing/promotion
   is a separate pending gate, not permission granted by this fix request.
3. Prepare and rebuild both images, run artifact verification, and test both
   from fresh disks through OOBE, normal reboot, and desktop acceptance.
   Keep the offline guest disconnected throughout installation.
4. Test optional Programs Center install/remove/reinstall, screenshot cancel
   and repeated capture, recovery/failure paths, displays, and final
   1920×1080 screenshots. QXL repaint artifacts need separate graphics review.
5. Only after both final images pass, complete the release draft and website
   handoff. ISO download links belong on the website, not GitHub.
