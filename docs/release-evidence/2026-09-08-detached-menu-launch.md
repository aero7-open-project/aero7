# Theme 54 — detached menu application lifetime

Status: corrected source and full candidate package tested; normally upgraded
in the disconnected r10 Wayland guest, followed by normal reboot/password login.
This closes the reproduced menu-launch defect, not the complete Beta 2 release
gate. Nothing was committed, pushed, published or added to the frozen ISOs.

## Cause and correction

Taskbar Properties closed its context menu without leaving Control Panel open.
The same command launched directly with output redirected to a file worked.
A controlled QML probe using Plasma's executable engine reproduced that
difference. The detached application inherited output pipes whose reader
disappeared when the short-lived shell-action helper returned. A later write
could terminate the application. This establishes the pipe-lifetime defect;
the GUI failure was not separately traced to a specific delivered SIGPIPE.

The helper now gives detached applications independent journal streams for
stdout and stderr, with null standard input. Child redirection uses only
async-signal-safe descriptor operations. Parent descriptors are closed after
the launch attempt, and descriptors initially allocated as 0/1/2 are relocated
before redirection. If journald is unavailable, the helper explicitly reports
that condition and redirects the child to the null device so it can still run.
Failed executable launches continue to return failure with a diagnostic.

Program names, arguments, user identity, environment and privilege boundaries
are unchanged. No shell interpolation was introduced. Icons, taskbar defaults,
theme appearance and the locked Shell revision were not changed. The package
declares `systemd-libs` explicitly. Existing diagnostic collection already
includes these user/system journal records; no collector change was needed.

## Regression and package results

The regression fixture waits until the helper has exited and the caller has
closed its pipes, then writes both stdout and stderr before recording its
arguments. Four real helper actions are tested: taskbar properties, Start
properties, Explorer and Task Manager. All four fail against the old helper.
After the fix, both the normal-journal suite and a test-only forced-unavailable
journal variant pass: seven cases each including setup/cleanup and the missing
executable test. Normal-path delayed diagnostics are retained in the journal.

The full package build completed on 8 September at 22:55:03 CEST. Its 22
successful CTest statuses comprise 13 executed tests and nine ECM checks that
explicitly skip before installation. The separate ten SDDM runtime checks also
pass. Do not count the nine skipped checks as metadata validation. Existing
compiler/package advisory warnings are retained in the build log.

- Package: `aerothemeplasma-desktop-git` `6.7.0_742.r9c2d850-54`.
- Size: 5,157,232 bytes.
- Archive SHA-256: `bb560b76a36fe08979db2793c23ca97e300b32c20bddbf80f7bf09f3998f61f4`.
- Patch SHA-256: `a3b559b2c533e30599fd9b0e177de054b9a6ff63ccb09142bfa40d328b2e85c6`.
- Installed helper SHA-256: `bf378b131705f6c7f0d7db6b0ce67d23ab87c78e8ac9619ee945e63218818d1e`.
- Base source: `9c2d850f0907cd7d33c81e8a3fcc00abae3abb9b`, with retained patches.
- Shell pin remains `cf4d1d8969dfa5ae84308c937cc60146ea59f216`.

All five new/changed helper source files in the prepared package match the
maintained worktree. Archive identity, hash and path/VCS hygiene checks pass;
test fixtures and the forced-no-journal helper are not installed. The build
bypassed only the host makepkg dependency precheck. VM installation used normal
dependency-checked `pacman -U`, and all 1,147 package files were present.

## Actual installed desktop replay

The existing r10 offline VM retained no network adapter throughout. The
22:55–22:56 upgrade replaced Theme 53 with Theme 54 without a service repair.
Actual mouse actions then opened the correct windows:

| Action | Observed result | Screenshot |
| --- | --- | --- |
| Taskbar → Properties | Taskbar tab in Control Panel | [395](shell-launch54-logs/395-theme54-taskbar-properties.png) |
| Start → Properties | Start Menu tab in Control Panel | [397](shell-launch54-logs/397-theme54-start-properties.png) |
| Start → Open Windows Explorer | Branded File Explorer home | [398](shell-launch54-logs/398-theme54-start-explorer.png) |
| Taskbar → Start Task Manager | Tux Manager with live processes | [399](shell-launch54-logs/399-theme54-task-manager.png) |

The launched applications stayed open and were closed normally. No settings
were applied and no file operations were performed. Their later diagnostics
are now visible under the `aero7-shell-action` journal identifier.

A normal reboot and password login produced boot ID
`64792291-ea41-40e9-be0b-78240c2a6daf`, different from the preceding
`fda9a4d1-0e64-43bb-becf-39b2cb926567`. The SDDM logo remained fully visible.
The actual taskbar context menu then accepted End + Enter and opened Properties
([403](shell-launch54-logs/403-theme54-reboot-keyboard-properties.png)).
The 23:08 audit verified the exact helper hash, Theme 54, Explorer 54, Desktop
30, Control Panel 51, Spectacle 3 and Qt 6.11.2-3.1. Shell and snipping services
were active; the shell restart count was zero. Both failed-unit lists were empty
at that instant. The reproduced duplicate registration and missing panel-shadow
warnings were absent, but other startup warnings remain as listed below.

Meta+Shift+S entered the actual rectangular selector. After region release,
the overlay closed without a Spectacle editor, and the saved notification
appeared ([406](shell-launch54-logs/406-theme54-notification.png)). Clicking its
body opened the saved image in the default viewer
([408](shell-launch54-logs/408-theme54-viewer-loaded.png)). The PNG was retained
at `Pictures/Screenshots/Screenshot 2026-09-08 23.01.42.829-327bbf.png`:
451×401 pixels, SHA-256
`b8ca580caecbbfd402da182bb2c31c48bd876e67c10bd7acdbbf15fa1e24900e`.
The existing Qt clipboard probe verified every decoded image pixel against
that PNG; this is not merely a filename/URL clipboard check. Its pixel SHA-256
was `5226d493dac9710c42fe4bf45dfdcccf014ad1f7a910364d1f21a6d5c3e55b44`.
This run does not relabel the earlier actual Paint Ctrl+V replay as a new test.

An initial supplemental audit tried `wl-paste`, which is not installed in this
guest. That failed audit is retained as `theme54-capture.TKKN60`; no package was
installed to hide it. The corrected audit uses the existing read-only Qt probe
and passes in `theme54-capture.HcvuEG`. Probe binary SHA-256:
`c0cea1533909a8a07f42c57684c257d8aa2e5a43c3e5e36091d67b481e96a28b`.

## Retained evidence and remaining gates

[Evidence folder](shell-launch54-logs/) contains the before/after source tests,
package recipe/patch/build log, full CTest log, normal upgrade audit, both boot
audits, launch diagnostics, capture/probe results and 1920×1080 screenshots.
The failed audit is evidence of a missing QA utility, not a screenshot failure.

The disconnected update-check failure still requires successful online recovery
and a real approved update transaction. Empty failed-unit lists on this boot do
not prove that recovery. Missing helper portal identities, UAC process lookup,
disabled-KWallet portal policy, virtual graphics/power warnings and broader
keyboard, optional-feature, fallback and recovery workflows remain separate.
Neither this pass nor two fast observed reboots establish universal shutdown
reliability. The existing test desktop's diagnostic folder is intentional.

Candidate signing/recipe promotion, final online/offline image rebuilds and
full installation acceptance remain pending. The frozen r10 images still
contain their earlier component versions. Website copy stays a working draft
with no enabled downloads, final artifact table or publication approval.
