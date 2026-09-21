# Theme 56 — grouped-preview sizing validation

Status: the reproduced geometry defect passes source and installed-code tests,
normal package upgrade, reboot and bounded graphical replay. The many-window
replay exposed a separate overflow-row reference error. That follow-up has a
source correction and passing regressions. Its subsequent package/VM acceptance
is recorded in the [Theme 57 follow-up](2026-09-09-overflow-row-validation.md).
No commit, publication, repository promotion or final ISO rebuild was performed.

This follows [Theme 55's installed tooltip pass](2026-09-09-tooltip-installed-validation.md).

## Geometry correction and provenance

The group now stores numeric maximum natural dimensions instead of binding to a
delegate whose assigned size depends on that same group. Measurements consider
all live delegates, including shrinking/removing the previous maximum. Child
caption/media sizing uses implicit dimensions; delegate-triggered measurements
are deferred until layout evaluation finishes. Count/model changes schedule a
measurement, including transitions to an empty model.

The fresh two-job build ran 9 September 2026, 00:24:31–00:30:08 CEST.
All 24 CTest statuses succeeded: 15 executed tests and nine ECM checks that
explicitly skipped before installation. Ten separate SDDM runtime checks passed.
See the [full build log](group-preview56-logs/theme56-package.log) and
[CTest detail](group-preview56-logs/package-LastTest.log), including retained
compiler/build-path advisories. Only the host dependency precheck was bypassed;
no host packages were installed. VM installation checked dependencies normally.

| Item | Verified value |
| --- | --- |
| Package | `aerothemeplasma-desktop-git 6.7.0_742.r9c2d850-56` |
| Archive size | 5,157,132 bytes |
| Archive SHA-256 | `0194af5ebef1fa277e15ba14315c5135f9fb77fee747d351930031d9190a5ef4` |
| Sizing patch SHA-256 | `c6c3b5649cbe7247630da21cd5dbc298eacc0aeb87940a239986dc168a0474be` |
| Base source commit | `9c2d850f0907cd7d33c81e8a3fcc00abae3abb9b` |
| Unchanged Shell pin | `cf4d1d8969dfa5ae84308c937cc60146ea59f216` |

Archive identity/hash and unsafe-path/VCS checks passed. All five prepared
changed files matched the maintained worktree before the later overflow edit.
The [normal upgrade](group-preview56-logs/theme56-upgrade.pAwj4s/upgrade.log)
changed only Theme 55 → 56, completed its hooks, found all 1,147 files present
and exited zero. The three installed sizing files match the source hashes.

## Installed tests and graphical replay

The same test-only fixture runs isolated production geometry against the actual
installed QML files. Its SHA-256 is
`cd7d14fe8efeff61ef6860800f99e3efd4f98f6cf2c7b7e57e022d505c4b2f10`.
Theme 55 produced [six expected failures](group-preview56-logs/group-size-baseline.jqvGhx/qt-test.log).
After normal reboot/password login, boot
`ea3d1c63-41fc-4a75-a35c-a4d85b21b7ae` passed all
[nine QtTest results](group-preview56-logs/group-size-candidate.FogFyo/qt-test.log)
under Wayland, with no failures/skips and no package changes during the fixture.
These are seven cases plus setup/cleanup, not nine full desktop workflows.

The real 1920×1080 replay verifies:

- Unclipped [login branding](group-preview56-logs/252-theme56-greeter.png).
- Two Explorer windows grouped; [live images and close controls appear](group-preview56-logs/257-theme56-close-ready.png).
- Clicking a preview [activates its window](group-preview56-logs/256-theme56-activation.png).
- Closing one leaves a [single preview](group-preview56-logs/258-theme56-group-to-single.png); closing the last restores the [pin label](group-preview56-logs/259-theme56-back-to-pin.png).
- A [16-row overflow list](group-preview56-logs/264-theme56-overflow-rehover.png) displays and [activates the selected window](group-preview56-logs/265-theme56-list-activation.png).
- The taskbar's Close all windows action [closes the temporary Explorer windows](group-preview56-logs/273-theme56-close-all.png).

Initial images can appear after the preview container; the retained captures
distinguish early empty containers from subsequently populated live images.
No test files were created/deleted through Explorer. An audit command was
accidentally typed into an Explorer filter after focus changed; it did not run
there. The terminal audit was subsequently run with focus verified.

The [post-overflow journal](group-preview56-logs/theme56-replay.37DfpO/user-journal.txt)
has no reproduced GroupThumbnails/WindowThumbnail sizing loop or Task.qml typed
role warning. The shell and actual authentication service remain active with
zero restarts. Previous-boot Plasma shutdown completed within 00:34:54, without
an observed timeout in that user journal.

## Separate overflow finding — source checkpoint

At 00:42:26, clicking the overflow close control closes the window but logs
`WindowListDelegate.qml:45: ReferenceError: isGroupDelegate is not defined`.
This group-only component retained single-window branches from another delegate.
The same missing variable also affects its non-icons-only hover expression.

Two new [source regressions fail before correction](group-preview56-logs/aero7-overflow-baseline.log).
Removing those inapplicable branches makes the complete
[11-result suite pass](group-preview56-logs/aero7-overflow-fixed.log).
The same extended fixture also reproduces both failures against the actual
[installed Theme 56 file](group-preview56-logs/overflow-baseline.VwPpJT/qt-test.log),
with nine other results passing and unchanged package state.
At this source checkpoint, Theme 57 still required package/reboot/live overflow
replay. The subsequent [installed Theme 57 report](2026-09-09-overflow-row-validation.md)
records those completed checks and closes the reproduced row reference error.
Do not treat this earlier source-only checkpoint as that acceptance evidence.

Duplicate UAC unit packaging, disabled-KWallet policy, broader workflows,
package promotion/signing and final media remain separate gates. The frozen
online/offline images have not changed. Do not claim all bugs are fixed.
