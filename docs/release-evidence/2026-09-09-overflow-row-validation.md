# Theme 57 — overflow-row lifecycle follow-up

Status: full package build, normal upgrade/reboot, installed-code tests and
bounded graphical overflow replay passed. This closes the reproduced overflow
row reference error, not the entire release bug pass. No publication, commit,
repository promotion or final ISO rebuild was made.

This follows [Theme 56's grouped-preview validation](2026-09-09-group-preview-validation.md).
The group-only list delegate incorrectly retained a single-window close branch
and single-window hover branch. Both referenced an undeclared `isGroupDelegate`.
The fix removes those inapplicable branches: closing requests only the selected
window's close, and row highlighting follows the row/close-button hover state.

## Regressions and package

Two isolated tests execute the actual production close function and hover
binding. Both fail before the fix, with the same reference error observed in
the VM. The close test also verifies the requested model index and that the
surviving group's popup is not hidden. The hover test covers enter, close-button
hover and leave with non-icons-only taskbar settings in its fixture.

The [installed Theme 56 baseline](overflow57-logs/overflow-baseline.VwPpJT/qt-test.log)
has nine passing results and the two expected failures, under Wayland, using
actual installed QML. The extended fixture's SHA-256 is
`ded641080650e04e2ee4d9ee1afac36a38a7a9edc9510aa02600c160c4069114`.
The corrected source passes [all 11 results](overflow57-logs/aero7-overflow-fixed.log).
These isolated tests supplement rather than replace actual Plasma interaction.

The fresh two-job build ran 9 September 2026, 00:47:00–00:52:33 CEST.
All 24 CTest statuses succeeded: 15 executed tests and nine ECM metadata checks
that explicitly skipped before installation. Ten separate SDDM runtime results
passed. The [complete build log](overflow57-logs/theme57-package.log) and
[CTest detail](overflow57-logs/package-LastTest.log) preserve advisories too.
Host dependency prechecking was bypassed without installing host packages;
the VM used normal dependency-checked package installation.

| Item | Verified value |
| --- | --- |
| Package | `aerothemeplasma-desktop-git 6.7.0_742.r9c2d850-57` |
| Archive size | 5,158,299 bytes |
| Archive SHA-256 | `7c6d37e69418c3a9e406a5deffedbc5e6d11b4e8a37637e721c6d23abb1e2f0a` |
| Overflow patch SHA-256 | `9d757bb53c455caa923e79fa36dc3b826d0bb7787da7876f616f97437ab89c3d` |
| Installed WindowListDelegate.qml SHA-256 | `73d71795c608a0e167c99a1f1b8518d61d5281c57605eb374acba3242673d59d` |
| Base source commit | `9c2d850f0907cd7d33c81e8a3fcc00abae3abb9b` |
| Unchanged Shell pin | `cf4d1d8969dfa5ae84308c937cc60146ea59f216` |

Archive identity/hash and unsafe-path/VCS checks passed. Both prepared changed
files match the maintained worktree. The retained Theme 56 recipe/patch sequence
is unchanged apart from the added overflow patch and release increment.
The [normal upgrade](overflow57-logs/theme57-upgrade.666gJZ/upgrade.log) changed
only Theme 56 → 57, completed all hooks, found 1,147 files with none missing and
exited zero. GroupThumbnails.qml, WindowThumbnail.qml and the Shell pin remain
unchanged from Theme 56. This package is not in the frozen online/offline ISOs.

## Reboot and actual overflow replay

Normal reboot/password login produced boot
`e003564f-55bc-4e5e-96bc-38c6d3dab830`. The
[login branding](overflow57-logs/280-theme57-greeter.png) is fully visible and the
[desktop](overflow57-logs/281-theme57-desktop.png) loaded normally. The
[installed candidate fixture](overflow57-logs/overflow-candidate.aFmTk9/qt-test.log)
passes all 11 results on Wayland with no failures/skips. Package lists before
and after the fixture are identical. The earlier upgrade command hit an idle
lock-screen race and was rejected as a password; it did not execute there.
After a successful unlock it was rerun in the verified terminal and completed.

Ten temporary Explorer windows were launched through the application's normal
`--new-window` entry point, browsing only the test user's home directory. The
[launcher records](overflow57-logs/overflow-windows.Rye5P6/launched-pids.txt)
and real screenshot confirm ten windows; no user files were changed.

| Action | Observed result |
| --- | --- |
| Hover the Explorer taskbar group | [Ten distinct overflow rows](overflow57-logs/285-theme57-ten-window-list.png) |
| Click the first row | Its previously rear window [becomes active](overflow57-logs/286-theme57-list-activation.png) |
| Hover that row's close control | [Close control appears](overflow57-logs/287-theme57-list-close-ready.png) |
| Click close | Only that window closes; ten-row list becomes [nine live thumbnails](overflow57-logs/288-theme57-list-to-thumbnails.png) |
| Use the taskbar's Close all windows action | All remaining temporary windows close and the [pin label returns](overflow57-logs/290-theme57-back-to-pin.png) |

The [complete post-replay journal](overflow57-logs/theme57-replay.MJz7YD/user-journal.txt)
has no `ReferenceError`, `TypeError`, binding loop or typed assignment warning
from these taskbar components. In particular, the Theme 56 close-row error and
Theme 55 sizing loop do not recur. The [audit](overflow57-logs/theme57-replay.MJz7YD/audit.log)
confirms the shell and actual authentication service active, zero restarts and
empty failed-unit lists at that snapshot. The previous boot's Plasma shutdown
started and completed during 00:55:50, with no observed timeout in its journal.

Known VM graphics/hardware diagnostics, upstream helper metadata warnings,
the protected UAC `/proc` portal warning and disabled-KWallet Secret backend
failure remain visible. They were not suppressed or reclassified as fixed.
Duplicate authentication-unit packaging, KWallet policy, broader workflow
checks, package promotion/signing and final-media acceptance remain separate
gates. Non-icons-only hover is covered by the isolated regression, not a claim
that every real taskbar configuration has been exercised.
