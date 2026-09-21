# Gadget menu checked-state indicators

## Native comparison

The Gadgets 15 Calendar menu changes Always on top correctly but does not show
its checked indicator with the normal theme. The preceding captured layout has
the boolean enabled and Calendar visibly stacks above applications; this is
not simply a failure to save the option.

The style audit `gadget-menu-style.0jDDVJ` confirms the VM has Kvantum 1.1.8,
the Windows7Aero chooser and Gadgets 15. A separate private host,
`gadgets15-desktop.jMEkm9`, uses `QT_STYLE_OVERRIDE=Fusion` for this diagnostic
only. The same native toggle/reopen sequence now shows a checkmark. Its saved
private layout has Always on top enabled. The private host was stopped; no
normal account style or gadget layout was changed.

Evidence is in [gadget-menu-indicator-logs](gadget-menu-indicator-logs/), with
the earlier missing-indicator capture in
[gadget-layer-update-logs](gadget-layer-update-logs/).

## Cause and source correction

The installed-version [Kvantum source](https://github.com/tsujan/Kvantum/blob/V1.1.8/Kvantum/style/Kvantum.cpp)
leaves `PE_IndicatorMenuCheckMark` empty; it draws checks within the complete
menu-item renderer instead. Qt's stylesheet renderer bypasses that complete
renderer when an item has custom padding/borders, and requests the empty
primitive directly. This explains the native themed/Fusion difference.

The Desktop companion now has a menu-local `QProxyStyle` that delegates just
that checkmark primitive to Qt's existing `QCommonStyle` implementation.
Other drawing and metrics remain delegated to the existing style. The same
owned style is assigned to Size and Opacity submenus. No replacement icon,
artwork, global style override or icon-pack change is introduced.

Three new tests inspect the real root/Size/Opacity menus, compare only the
indicator gutter in unchecked/checked/unchecked states, and include a timeout
guard around the popup event loop. A preserved pre-correction source snapshot
with these identical tests is in `work/gadgets16-indicators.mK9Qp7/baseline`.
The test runner requests Fusion, Windows and Kvantum and verifies each requested
style actually loaded.

## Verification gate

The native Fusion comparison establishes the diagnosis, not acceptance of the
new proxy implementation. The subsequent controlled matrix reproduces all three
indicator failures with Kvantum before correction (two setup/cleanup passes,
three failures), while Fusion and Windows controls pass. After correction,
all three styles pass all five results, with each requested style confirmed
loaded. The complete corrected Kvantum suite also passes all seven groups,
including 50 gallery and 74 provider results. Root menu and both submenu object
lifecycles complete normally in these tests.

The initial KWin 7.3 build was terminated with status 143 at 56%; its compiler
processes were confirmed absent and no compiler failure was recorded. These
small regression builds then ran sequentially. Gadgets 16 is now being packaged
in `work/beta2-gadgets16.BWprZ5`; the KWin build will resume from existing objects
afterward. Gadget source archive SHA-256:
`05ac79696ee224ad22523ec918e9fa754b2baf8e771368c1fc4252c50b7b66a6`.

Gadgets 16 completed at 14:38:54 CEST, with all seven package test groups
passing. Its archive SHA-256 is
`5bd3ae6855c91d6f64afe03011641039bfbbc2a71236ae683c7f21e085193ac9`;
the installed executable SHA-256 is
`27f3cdf3d61c1f97ca3cbce74d76050bd59182e62138467b23ecfe2690ecf8eb`.
The timestamp-normalized package manifest changes only the executable and
build/package metadata. Assets, launchers, hooks, modes and symlinks remain
unchanged.

Normal 15→16 upgrade passes in `gadgets16-upgrade.Tr7iAI`, verifying all
57 package files and the exact executable hash. Private native replay
`gadgets16-desktop.kTon4h` rejects a style override; plugin logging confirms
Kvantum loads. Always on top displays its check after enabling. Size displays
Small, then Large after selection; Calendar visibly resizes. Opacity displays
100%, then 60% after selection. Both submenus open and close normally. The
private layout is restored to small/100%/not-always-on-top before stopping the
host. Screenshots and the runtime trace are retained alongside the tests.

Normal logout/login audit `gadgets16-login.WGRe3t` also passes. Autostart owns
PID 18640 with the exact installed executable hash; the actual KWin child has
no permission-check bypass. Shell, compositor and Plasma services are active
with zero restarts; no failed user/system units are listed. The normal account
layout is byte-identical to its preceding Gadgets 15 snapshot. The VM runs
Gadgets 16 / KWin 7.2; KWin 7.3 has resumed incrementally in a separate build
log. No final media is selected or approved.

## Additional functional finding: opacity is not applied

The indicator replay establishes visible menu state, **not working opacity**.
Selecting 60% emits `This plugin does not support setting window opacity` in
the native Wayland log (line 4478 in the preserved run), and Calendar remains
opaque. The constructor and `setOpacityPercent()` currently use
`QWidget::setWindowOpacity`; the drag preview also copies that window property.
Actual translucency therefore remains a separate failed workflow. A correction
must preserve composed gadget/controls/transition alpha and the drag preview,
with before/after pixel and installed-VM evidence; changing only the checkbox
or saved percentage does not close this gate.

## Additional keyboard teardown crash

A subsequent private native run, `gadgets16-desktop.tA4UcC`, opens Size on
pointer motion without clicking. The first pointer entry alone did not select
the row; a second motion within it opened the submenu. Keyboard Down selects
Small, then Large, and Return saves the large size but crashes the gadget host.
The exit status is 139; the retained coredump identifies SIGSEGV in
`QWidget::clearFocus()` during child `QMenu` destruction at 15:09:23 CEST.
The normal gadget account/profile was not used for this replay.

The menu-local style was created as the root menu's first child, before the
submenus. Root teardown could therefore delete it before focused submenus
finished clearing focus. The candidate now declares the style before the root
as a scoped object so reverse stack destruction keeps it alive through every
submenu's teardown. Qt's [widget style API](https://doc.qt.io/qt-6/qwidget.html#setStyle)
does not transfer style ownership. New identical baseline/candidate tests
exercise focused Size and Opacity submenu selection with keyboard events and
include teardown in their scope. The offscreen matrix passes for both versions
under Fusion, Windows and Kvantum, so it does not reproduce the native crash
and cannot itself establish the fix.

A second native release-16 run on the updated KWin 7.3,
`kwin73-popup.Fyx876`, crashes at the same focused-submenu teardown (PID 2178,
15:27:32 CEST, exit 139). This separates the gadget lifetime defect from the
compositor popup correction. After the normal upgrade to Gadgets 17, native
`gadgets17-desktop.v4VoCm` passes the same Size → Large keyboard selection on
that compositor, then also passes Opacity → 60% keyboard selection. The host
remains running and the selected changes take effect. Its private restart and
normal logout/login binary/autostart audit also pass; see the
[package, native and persistence evidence](2026-09-13-gadget-opacity.md#package-and-installed-wayland-replay).
This closes the reproduced keyboard sequence, not every keyboard or gadget
workflow. The broader and final-media gates remain open.
