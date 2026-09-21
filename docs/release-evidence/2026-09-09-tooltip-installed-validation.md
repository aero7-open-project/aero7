# Theme 55 — installed tooltip validation

Status: package build, normal upgrade, reboot, installed-file regressions and
bounded graphical replay passed. A separate grouped-preview geometry binding
loop was exposed by the replay and **remains open**. No final ISO, repository
publication or commit was made.

This continues the [startup and source regression report](2026-09-08-startup-and-tooltip.md).
The source fix clears missing task-model roles instead of leaving stale typed
tooltip values. It does not redesign the existing grouped-preview geometry.

## Package provenance and build

The fresh two-job build started 8 September at 23:55:06 CEST and finished
9 September at 00:00:28. It used the retained Theme 54 recipe/patch sequence,
adding only the tooltip patch and release increment. The three prepared source
files match the maintained worktree. Shell action source is unchanged.

| Item | Verified value |
| --- | --- |
| Package | `aerothemeplasma-desktop-git 6.7.0_742.r9c2d850-55` |
| Archive size | 5,158,541 bytes |
| Archive SHA-256 | `dd4bc31e4e25f4bc1770317fb75a0b601e42e01fe066574195273f0259821245` |
| Tooltip patch SHA-256 | `32ae458475b1d1fc84f669860ae1cde4b0a0efc78113ee130401540b9d6a6dfe` |
| Installed Task.qml SHA-256 | `4f3fad0ddb016d209aa157630cde29c1b92a2ae2a2f23f5ca7630571f7978754` |
| Base source commit | `9c2d850f0907cd7d33c81e8a3fcc00abae3abb9b` |
| Unchanged Shell pin | `cf4d1d8969dfa5ae84308c937cc60146ea59f216` |

All 23 CTest statuses succeeded: 14 executed tests and nine ECM metadata checks
that explicitly skipped before installation. The separate ten SDDM runtime
checks also passed. The complete build includes the three test executables
missing from the earlier incremental run. Archive identity/hash and forbidden
path/VCS checks passed. Compiler advisories and embedded build-path warnings
are retained in the [full package log](tooltip55-logs/theme55-package.log).
Only the host makepkg dependency precheck was bypassed; no host packages were
installed. The VM used normal dependency-checked `pacman -U`.

## Normal upgrade and reboot

[Upgrade evidence](tooltip55-logs/theme55-upgrade.u9otEP/upgrade.log) records
only Theme 54 → 55 changing in the installed package list, all post-transaction
hooks completing, 1,147 package files present and exit zero. The rebuilt
`aero7-shell-action` binary hash is
`e6a6de8fd67185971f6242b20848754ae8cfc89df8e063d953c4cf7a65896c18`;
its source matches Theme 54, but the rebuilt binary hash is not identical.

A normal reboot and password login produced new boot
`91b6f0dd-822a-48dd-8ace-5361dd82e5c3`. The installed stack also retains Desktop
30, Explorer 54, Control Panel 52, Qt 6.11.2-3.1 and Spectacle 3.
The [login screen](tooltip55-logs/236-theme55-login.png) shows the unclipped
branding; [the desktop](tooltip55-logs/237-theme55-desktop.png) loaded normally.

The test fixture was compiled from the package's exact test source, changing
only its compile-time input path to the actual installed `Task.qml`. Its SHA-256
is `a4a1a710579d61fad145f3a217965d5882286df58f691e4ead8796d81b693825`.
On the same VM's Theme 54 file, all four regression cases failed as expected
([baseline](tooltip55-logs/tooltip-baseline.YXHDdS/qt-test.log)). On Theme 55,
all four pass under Wayland, with six total QtTest results including setup and
cleanup, no failures/skips and unchanged installed package state
([candidate](tooltip55-logs/tooltip-candidate.KGnhEh/qt-test.log)). This fixture
executes isolated production bindings, not the whole Plasma delegate.

## Actual taskbar replay

| Action | Observed result |
| --- | --- |
| Launch Explorer from its pin, then hover | Correct [single preview](tooltip55-logs/239-theme55-running-preview.png) |
| Click the preview close button | [Window closes](tooltip55-logs/240-theme55-preview-close-result.png) |
| Relaunch, then Ctrl+N | Two windows in one [grouped preview](tooltip55-logs/241-theme55-grouped-preview.png) |
| Click the first preview | The corresponding previously rear window [comes forward](tooltip55-logs/242-theme55-preview-activation.png) |
| Close one grouped preview | That window closes and the group [reduces to one preview](tooltip55-logs/244-theme55-group-to-single.png) |
| Close the remaining preview, hover its pin | No stale window preview; [pinned label returns](tooltip55-logs/245-theme55-back-to-pin.png) |

No files were created, modified or deleted in these Explorer actions.
The final [audit](tooltip55-logs/theme55-replay.m0ntxd/audit.log) confirms the
shell and actual authentication service active with zero restarts. Failed-unit
lists were empty at that snapshot; transient earlier KWallet failures remain
visible in the full journal. The previous boot's Plasma shutdown completed
between 00:02:38 and 00:02:39, without a timeout in that user journal.

## New finding and remaining gates

The [complete replay journal](tooltip55-logs/theme55-replay.m0ntxd/user-journal.txt)
contains no reproduced typed-role assignment warnings from `Task.qml`. However,
at 00:08:47 it records binding loops in `GroupThumbnails.qml`'s
`maxThumbnailHeight` and `WindowThumbnail.qml`'s `height`. The group selects a
maximum-size delegate while delegate geometry reads the group's maximum, and
updates can run during implicit-height evaluation. This geometry path needs a
separate regression/fix and another installed replay. Visual success alone is
not sufficient to close that finding.

The [UAC ownership audit](tooltip55-logs/uac-unit-ownership.0x0GwX/audit.log)
confirms the duplicate standalone unit and the active Plasma-unit override both
come from `uac-polkit-agent-git` release 1. The active agent remains correctly
under `plasma-polkit-agent.service`; no authentication settings were changed.
Review that package's duplicate unit declaration separately from the protected
`/proc` portal warning. Existing KWallet policy remains unchanged.

No new fixes were promoted into the frozen online/offline ISOs. Broader workflow
checks, package promotion/signing, final-image testing and publication approval
remain separate gates. Do not describe this pass as “all bugs fixed”.
