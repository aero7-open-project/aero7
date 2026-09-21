# Startup classification and task tooltip lifecycle — 8 September 2026

Status at this source checkpoint: read-only installed startup audit complete;
tooltip source regression fixed. See the later [Theme 55 installed validation](2026-09-09-tooltip-installed-validation.md)
for its completed package/replay and the new grouped-preview sizing finding. No commit,
publication, final ISO, authentication policy or extra application identities
were changed in this pass.

## Installed startup audit

The existing online r10 guest remains on boot
`d6401675-6853-46a9-bdc5-6c15a0047a97`, with Desktop 30, Control Panel 52,
Qt 6.11.2-3.1 and the previously installed Theme 54. Password unlock passed.
The full user journal and service snapshots are retained under
[startup-tooltip-logs](startup-tooltip-logs/).

At 23:47 the shell, ksmserver, global-menu proxy, XEmbed proxy, activity manager,
PowerDevil and desktop portal were active/running with zero service restarts.
There were no loaded failed system/user units at that snapshot. This does not
mean there were no earlier failures: the full journal includes a transient
KWallet portal exit 255 and the protected-process registration warning.

Five helpers lack matching application desktop entries. The exact errors match
[KDE bug 516858](https://bugs.kde.org/show_bug.cgi?id=516858), where the July 9
maintainer comment classifies the warning as harmless. This is a documented
upstream diagnostic, not proof that these services failed. No additional
launcher metadata or registration suppression was added just to remove it.

The first audit queried the unused `uac-polkit-agent.service` by name. Loading
that definition emitted a duplicate bus-name diagnostic; its inactive state
does **not** describe the running authentication agent. PID-based inspection
identified the actual `plasma-polkit-agent.service`, active since 23:28:52 with
UAC child PID 907. The corrected audit queries that actual unit. Both audits
and [PID-based evidence](startup-tooltip-logs/uac-running-unit.txt) are retained.
This duplicate installed definition still merits packaging review. Nothing was
enabled, disabled or restarted by the audit.

The separate `/proc/907/root` registration warning is not fixed by adding an
application entry (the matching entry already exists). Authentication
protections and the existing disabled-KWallet policy remain unchanged. Real
administrator approval already passed in the
[online update replay](2026-09-08-online-update-recovery.md).

## Tooltip regression and source correction

The prior offline Theme 54 journal records eight typed-property assignment
warnings from SevenTasks `Task.qml:62–73` at 22:25:58. The shared tooltip's
bindings could receive missing model roles during task transitions. Rejected
assignments also leave previous typed values in place, rather than clearing
the old task's state.

The new `aero7-task-tooltip-lifecycle` Qt test executes the actual production
`updateToolTipBindings()` function with an isolated typed tooltip. Four cases
cover removed roles, a null model, an undefined model and a partial launcher.
All four fail against the old function, reproducing the assignment warnings.

The correction uses null-safe role reads with typed empty defaults. It clears
old title, icon, PID, launcher URL, window IDs, grouping and attention/activity
state while keeping bindings reactive. The partial launcher's valid index zero
is preserved. Re-populating the model restores the real values without calling
the binding function again.

All four cases now pass, with six QtTest results including setup/cleanup and no
skips. The source `Task.qml` SHA-256 is
`4f3fad0ddb016d209aa157630cde29c1b92a2ae2a2f23f5ca7630571f7978754`.
See [before](startup-tooltip-logs/aero7-tooltip-baseline.log),
[after](startup-tooltip-logs/tooltip-LastTest.log) and
[full local CTest attempt](startup-tooltip-logs/aero7-tooltip-all-tests.log).

The full local CTest attempt is **not a complete suite pass**: three unrelated
test executables were not built in this incremental build directory
(`systemtraymodeltest`, `aero7tasksmodeltest`, `aero7-kvantum-svg-test`). The
focused test was explicitly rebuilt and rerun successfully afterwards.

## Remaining acceptance

- Carry the tooltip correction and its test into the next Theme package, run
  its complete package build/tests, then upgrade normally in the VM.
- Replay actual pinned/running/grouped task tooltips across launch, close,
  hover and restart; retain full journals. The isolated test does not reproduce
  the entire Plasma model or establish visual acceptance.
- Review duplicate UAC unit packaging without weakening authentication.
- Keep KWallet policy, remaining workflow tests and final-image rebuild/testing
  gates explicit. The existing frozen ISOs do not contain this source change.
