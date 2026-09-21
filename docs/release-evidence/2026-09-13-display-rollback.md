# Display scaling and rollback — 13 September 2026

Local QA only. No commit, push, final ISO build or publication is authorized.

## Installed baseline

The offline VM has Desktop 32, Control Panel 53, Gadgets 23 and KWin 7.3,
running Wayland with one Virtual-1 output at 1920×1080, 75 Hz, scale 1. Its one
40-logical-pixel Aero taskbar and one desktop match the output count. Shell,
KWin and Plasma are active with zero restarts and no failed user units.

Using the real Control Panel **Screen Resolution → Advanced settings** page,
125% scaling applies and displays the 15-second confirmation. Leaving it
unanswered returns to scale 1 automatically. The native output snapshot after
rollback again reports mode 1, 1920×1080, scale 1 and position (0,0). The panel
snapshot is byte-identical to baseline and the same desktop-service processes
remain active with zero restarts. This proves the single-output scaling timeout
path on this virtual GPU, not multi-monitor or physical-driver acceptance.

Evidence: [baseline audit](display-rollback-logs/native53-baseline.log),
[baseline outputs](display-rollback-logs/native53-baseline-outputs.json),
[pending confirmation](display-rollback-logs/a7-display-scale-pending.png),
[restored UI](display-rollback-logs/a7-display-scale-reverted.png),
[post-timeout audit](display-rollback-logs/native53-timeout.log) and
[post-timeout outputs](display-rollback-logs/native53-timeout-outputs.json).

## Reproduced defects

Five real-page regressions fail before correction:

- Dragging the already-selected monitor leaves Apply disabled. Selecting a
  different monitor can incidentally enable it, masking this defect. Native
  Control Panel 53 also reproduces the disabled button while its status says
  to select Apply; [screenshot](display-rollback-logs/a7-display53-drag-disabled.png).
  The native draft was cancelled without applying it.
- Declining a two-output arrangement sends the edited monitor position as the
  rollback position, rather than the original backend position. Dragging had
  already modified the only stored output vector.
- Successful rollback, failed rollback and accepted changes all lose their
  result message when the generic output-detection label replaces it. The
  rollback subprocess failure itself was also ignored.

The baseline Qt result is two passing setup/cleanup results and five failures:
[baseline regression log](display-rollback-logs/baseline53.log). These tests use
the real diagram mouse events, OK/apply path and confirmation dialog, with a
controlled child-process display backend. They do not change host displays.

## Correction and current verification

The page keeps a separate snapshot of the last backend configuration for
rollback, enables Apply when dragging a monitor, checks the rollback result,
and displays the transaction result after refreshing output controls. A refresh
failure is also reported instead of hiding the transaction result.

All 21 Control Panel CTest groups pass after correction, including all five new
display regressions; [corrected suite](display-rollback-logs/corrected54.log).
Only DisplayPage.cpp/.h differ from the release-53 runtime
source; the other additions are the regression test and its build registration.

Candidate 54 packaging completed under `work/beta2-control54.S0WZbU`, from
source SHA-256 `2665e0c48c5ce1047c3f005fdf8c558f3dde76813772cafa0a11e5b47170255d`.
The established host-only `makepkg --nodeps` workflow avoids installing guest
runtime dependencies on the host; all 21 package-check groups passed. Normal
`pacman -U` installation in the VM enforced dependencies and succeeded, with
74 package files and zero missing files. Evidence:
[package build](display-rollback-logs/package54-build.log) and
[normal upgrade](display-rollback-logs/upgrade54.log).

Archive SHA-256:
`6b75e85c83120b38931ca3dcf30e47925f895483a538ee40fbe371a860959e23`.
Installed `/usr/bin/control` SHA-256:
`1ab88b79e2a2eb14c2b1900766253242c069e1964fde262c565d838ba2dd2b09`.

## Installed corrected replay

The native release-54 page now enables Apply after dragging the selected
monitor. That draft was cancelled. Applying 125% scaling and letting the
confirmation expire restores 100% with the complete restored-settings message.
Applying 125% again and accepting retains that scale with the kept-settings
message. Finally, selecting and accepting 100% returns the VM to its baseline.

- [Dragging enables Apply](display-rollback-logs/a7-display54-drag-enabled.png).
- [125% confirmation](display-rollback-logs/a7-display54-timeout-pending.png).
- [Timeout restores 100%](display-rollback-logs/a7-display54-timeout-restored.png).
- [Accepted 125%](display-rollback-logs/a7-display54-kept125.png).
- [Accepted return to 100%](display-rollback-logs/a7-display54-kept100.png).

The bounded read-only observer records scale 1 at sample 0, 1.25 at sample 8,
1 at sample 22 and 1.25 at sample 65. It completed after 90 samples, before
the final return to 100%; that last state is independently established by the
18:11 [backend audit](display-rollback-logs/native54-final.log) and
[output JSON](display-rollback-logs/native54-final-outputs.json). Mode 1 and
position (0,0) are restored. The [panel JSON](display-rollback-logs/native54-final-panels.json)
is byte-identical to the release-53 baseline. Shell, KWin and Plasma retain
the same running PIDs and zero restarts. This is not a release-54 reboot test.

The post-test failed-unit list contains `aero7-update-check.service`:
the [journal](display-rollback-logs/update-check54.log) records an unavailable
update check at 18:00:23 in this deliberately NIC-less guest. Earlier boots
show the same behavior. Do not describe the final snapshot as having no failed
user units or infer that offline update availability was verified.

## Next-build selection

Control Panel 54 is now selected with Gadgets 23 and KWin 7.3. Manifest SHA-256:
`407b48d4d4d4bc996a9ee5da909a97f78885cee82db26c705ea03bb2195602f1`.
All [149 integration tests](display-rollback-logs/integration54.log) pass.
Archive checks pass for [18 online archives](display-rollback-logs/online54.log)
and [53 offline archives / 35 offline repository entries](display-rollback-logs/offline54.log).
These validate selected inputs, not a newly built ISO. The Shell source pin is
unchanged, and no final media, commit, push or publication was produced.

Live multi-output/mixed-DPI, connector hotplug, broader recovery and exact final
online/offline media checks remain separate acceptance gates. Neither frozen
ISO includes this correction.
