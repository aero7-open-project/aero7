# SDDM 46 correction and splash lifecycle investigation

Local work in progress. Theme 46 built and passed normal offline-VM upgrade,
reboot, targeted greeter and lock-screen checks. Broader greeter and final-image
acceptance are pending. No commit, signing, push or publication.

## Reproduced SDDM defects

Theme 45's installed post-reboot journal reports two Column/child-anchor
conflicts, a StackLayout/child-anchor conflict and an undefined keyboard layout
`shortName`. The login still renders, but these are real warnings, not clean
acceptance. The keyboard button also wrote its own bound index, which could
break tracking when the backend changes layouts.

The correction replaces the two anchor-managed Columns with Items, preserving
their centered origin and the existing avatar, label, password and Switch User
anchors. StackLayout owns the user-list page geometry. The keyboard button
reads its index from the backend, guards an absent current layout, and writes
the backend directly only when a layout exists. Invalid indices recover to the
first layout; an empty list is never used as a modulo divisor.

`tests/test_sddm_runtime.py` extracts the actual affected QML subtrees into
temporary fixtures with isolated models. It never starts SDDM, authenticates
or executes theme shell helpers. Qt 6 runtime warnings for anchor conflicts,
undefined properties and binding loops fail the tests. Geometry covers normal
and large avatars at 1920×1080 and 1366×768, plus normal at 800×600. Keyboard
coverage includes zero/one/two layouts, cycling, external index changes,
negative/out-of-range indices and clearing the model. Delegate geometry is
checked at both avatar sizes. These are component tests, not full greeter proof.

The final fixture gives the TestCase an explicitly visible parent; an earlier
fixture's hidden parent prevented a meaningful visibility assertion. The final
unchanged test reports 8 failed functional cases against theme 45 and all
10 cases passing against the correction (8 functional plus setup/cleanup).
The host's unqualified qmltestrunner is Qt 5; the test explicitly uses the Qt 6
runner. Platform/icon warnings outside the targeted component assertions remain
visible in the logs. Do not claim globally warning-free execution.

## Frozen package inputs

Recipe version: `6.7.0_742.r9c2d850-46`.
Build directory: `work/beta2-theme46.CmTCRV`.
Prepared visual fixture: `work/beta2-sddm46.LL8Rim/theme`.

- PKGBUILD SHA-256: `b7c9fb302c2b7729258b064336f0e74cb3741a88960d6e6f2a8320306f0c25f1`.
- SRCINFO SHA-256: `f16c2ec9555a2083c43e5c0c61713596d6a525fa024ab9ef8f644a66d50b19c1`.
- Layout patch SHA-256: `18ee0a2ba49b701d25a2a0ee749b2e9b753de1b0e46abba820dfcea7c61163b7`.
- Runtime test SHA-256: `bf7e44188d7a682d7aa0eddf865ced1569c0f518a8c04d47445d04e8571d0d9d`.

The package check runs both the existing CTest suite and the new runtime tests.
Python is declared as a check dependency. Existing logos, icon pack, backgrounds,
upstream pin and the immutable Shell checkout are unchanged. Source 45 and its
package remain preserved. The build completed at 01:32:23 CEST on 7 September:
all 15 CTest groups passed in 0.53 seconds, followed by 10 passing runtime cases
in 749 ms. The package is 5,139,743 bytes, SHA-256
`d46b5d1fa47e6aa884577ec0b8604cadf48343e3fcb032ad6a880f089b198a42`.
Its approved branding and repeat-setup archive checks passed; the next-ISO input
manifest now selects 46. Repository source/metadata validation passed. This is
still not a rebuilt ISO or full greeter acceptance.

## Installed upgrade and reboot evidence

The disconnected r9 guest upgraded normally from theme 45 to 46 using pacman,
with dependency checking enabled. Its before/after inventory changed only the
theme package. The VM then rebooted; the exported boot IDs differ. After login,
`pacman -Qkk` reported zero altered files for the theme (1,143 files), Explorer
(665 files) and Paint (709 files). The saved Paint configuration hash also
matched. The system failed-unit list was empty; this is not a claim that the
user session has no failed units or warnings.

The new boot journal contains none of the targeted `Main.qml` anchor/layout,
TypeError or ReferenceError warnings. Unrelated audio, virtual-GPU, portal and
late KSplash warnings remain in the complete warning log. Missing pacman sync
database warnings are retained in the disconnected guest's audit output.

Actual 1920×1080 screenshots are under
`/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`:

- `301-theme46-login.png`: complete approved logo and normal password screen.
- `303-theme46-user-select-settled.png`: Switch User opens the user list.
- `304-theme46-login-return.png`: selecting the user restores password entry.
- `305-theme46-ease-access.png`: the existing session/keyboard popup opens;
  the selected Aero7 Desktop session is preserved. This is not acceptance of
  a complete Windows-style accessibility dialog.
- `307-theme46-desktop-settled.png`: authenticated desktop and taskbar visible.
- `312-theme46-lockscreen-settled.png`: complete logo and white Switch User label.

Screenshots captured immediately after input sometimes show a transition;
settled captures above are the acceptance evidence. The current health snapshot
reports the AeroShell package, one Aero panel, one desktop, and valid appearance.
These checks used a normally upgraded guest, not newly rebuilt media. Multiple
greeter users/layouts, other resolutions and accessibility flows are not fully
certified by the isolated component tests.

Logs in `sddm-layout-logs/` include `theme46-upgrade.log`,
`theme46-reboot-audit.log`, the before/after boot IDs, failed-system-unit and boot
warning logs, and `session46-diagnostic.log`. The audit marker is
`THEME46_NEW_BOOT_AND_PACKAGE_INTEGRITY_VERIFIED_NOT_FULL_DESKTOP_ACCEPTANCE`.

## Splash evidence: not a failed initial splash

The actual `plasma-ksplash.service` started at 01:11:25 and finished successfully
at 01:11:30, consuming 4.637 seconds wall time. Its effective engine is
`KSplashQML` and theme `authui7`. A later D-Bus activation at 01:11:34 starts
`plasma_waitforname org.kde.KSplash`, which times out at 01:12:34 after the
original splash has already exited. The initial splash is not disabled or
failing to start. This is a late activation/lifecycle problem and needs its own
correction, not a disabled splash or a successful-exit stub to hide the warning.

Local Plasma 6.7.4 `shellcorona.cpp` sends a `desktop` progress message without
disabling D-Bus auto-start. That is a candidate late caller, not yet proven by a
message trace. The guest's shell journal confirms a restart at 01:11:33–34; the
Aero7 health log records a layout/output reconciliation at that point. Further
caller and installed-source provenance checks are needed
before choosing the correct package boundary. Theme 46 does not claim to fix it.

The theme 46 boot reproduced the sequence: successful initial splash, layout
reconciliation and shell restart, then the late KSplash wait failure at 01:40:33.
The installed shell service and setup helper belong to Desktop `0.2.0-27`; their
SHA-256 values match the current independent Desktop source exactly. The actual
`plasmashell` binary belongs to `plasma-workspace 6.7.4-3`, not the theme package.
The setup helper currently restarts the shell for every health reconciliation,
including layout-only repairs. Avoiding unnecessary restarts needs a separate
regression-tested change that preserves the dark/light appearance repair path;
it does not by itself establish a fix for all possible late splash callers.
