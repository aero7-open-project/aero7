# Gadget opacity on Wayland

## Installed failure

The normal Gadgets 16 / KWin 7.2 replay records a 60% menu selection and saved
percentage, but Calendar remains opaque. The preserved native log emits
`This plugin does not support setting window opacity`. The checked indicator
fix is independently verified; it does not establish functional transparency.
See the [native indicator evidence](2026-09-13-gadget-menu-indicators.md).

## Candidate source change

The constructor retains a clamped 20–100 percentage without asking the platform
to change window opacity. For values below 100, painting composes the complete
body, text, hover controls and slideshow transition into a transparent image at
the widget's device-pixel ratio, then applies the chosen opacity once to that
finished image. At 100%, painting retains the direct path. The widget clears
old alpha before painting; changing the setting schedules an immediate update.
The drag preview uses the already-composed pixels without another window-opacity
multiplier. No artwork, icon-pack, global style or compositor setting changes.

## Verification plan and current boundary

`work/gadgets17-opacity.a9zvNu/baseline` preserves the preceding runtime with
the same new tests as the candidate. Seven data rows cover Calendar percentages,
restored settings and a partially completed slideshow fade with hover controls.
They compare every premultiplied color/alpha channel with a single composition
of the opaque reference, and require returning to 100% to restore those pixels.
Separate checks cover immediate repaint and drag-preview alpha without a second
multiplier. The private test runner requests and verifies 100%, 150% and 200%
device-pixel ratios in isolated sessions.

The first regression build caught a test-only type error: the preview is stored
as QWidget, so inspecting its pixmap requires a checked QLabel cast. That same
correction was applied to both baseline and candidate tests; the failed build
log is retained. No runtime behavior changed for this harness correction.

The baseline `baseline-opacity.zm9SLY` reproduces all nine opacity failures at
each requested scale (two setup/cleanup passes and nine failures per run).
Candidate `corrected-opacity.TRqbmb` passes all eleven results at each scale,
with actual device-pixel ratios verified from the test output. Every composed
pixel differs from its expected reference by at most two channel levels; the
test includes restored settings, complete controls/crossfade composition,
immediate repaint, preview alpha and return-to-100% identity.

The complete corrected Kvantum suite passes all seven groups, including
61 gallery and 74 provider results. The candidate also includes the separately
documented [keyboard style-lifetime correction](2026-09-13-gadget-menu-indicators.md#additional-keyboard-teardown-crash).
The offscreen keyboard matrix passes before and after the correction, so it
does **not** reproduce or close the native keyboard crash.

## Package and installed Wayland replay

Gadgets 17 completes its normal build and all seven package test groups in
`work/beta2-gadgets17.NZZMLA`, from source archive SHA-256
`84c50d32e4cc57d822f90645b415d4159f7d8b01f61637f9901825104b27553d`.
The archive `aero7-gadgets-3.0.0-17-x86_64.pkg.tar.zst` has SHA-256
`906a802bc78979ad046ab96cce7d472f57ad96229e1bc04eb8aaa6d24e6c443b`;
its executable has SHA-256
`4a8c673e8e22cdde5c6d56574af0059fd28f892b7f939e04f642c33f972748b6`.
The 57-file package preserves dependencies, artwork, launchers, hooks and modes;
only the executable and package build metadata change from release 16.
Normal offline upgrade `gadgets17-upgrade.VzMD35` passes on KWin 7.3.

Native private-profile replay `gadgets17-desktop.v4VoCm` uses the installed
binary and normal Kvantum style, without a style override. Keyboard selection
of Size → Large and Opacity → 60% closes the menus without the release-16 crash.
Calendar visibly becomes translucent, and its runtime no longer reports an
unsupported window-opacity request. Dragging the large calendar from (850,450)
to (950,530) preserves 60% opacity. The held-preview and released-calendar
screen crops at (950,530)-(1202,750) are pixel-identical.

Stopping and resuming that private host restores large/60% at (950,530).
The restored calendar crop is pixel-identical to the released-drag crop, and
the private layout JSON is unchanged across the restart. Both private runs
were stopped; this does not claim complete puzzle-game persistence or full
gadget acceptance.

Normal Start-menu logout and password login also pass in
`gadgets17-login.g1lVml`, session 5, boot
`fde6a493-c3b9-459c-a5c9-47f8afe5cb9c`. Autostart owns PID 6529 with the exact
release-17 executable hash. The audit verifies the actual KWin child (6225),
no permission-check bypass, active shell/compositor/Plasma services with zero
restarts, and no failed system or user units. The normal account layout is
byte-identical to `gadgets16-login.WGRe3t`; private QA gadgets were not added
to it. Package-query warnings about absent repository sync databases are
retained; the disconnected guest uses local packages, not a network refresh.

These are scoped upgraded-VM passes. Subsequent
[package alignment](2026-09-13-gadget-compositor-package-alignment.md) selects
Gadgets 17 / KWin 7.3 and passes the complete project checker. Broader
gadget/scaling/recovery coverage and final online/offline media remain open.
Logs and screenshots are in [gadget-opacity-logs](gadget-opacity-logs/).
