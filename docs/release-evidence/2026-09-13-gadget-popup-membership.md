# Gadget menus must preserve Show Desktop

## Reproduction and scope

The installed Gadgets 15 / KWin 7.2 replay `gadgets15-desktop.z2TABM`
shows the Calendar context menu restoring hidden applications. The saved
Wayland trace maps an `xdg_popup`, associates it with Calendar using the layer
surface's `get_popup`, then reports Show Desktop switching off. This remains
after the separately verified immediate-layer-commit correction.

KWin's `Workspace::breaksShowingDesktop()` exempts windows belonging to the
desktop. The existing Aero7 layer-shell fix marks the gadget and drag-preview
surfaces accordingly, but `XdgPopupWindow` inherited the base implementation
returning false. Its parent is already resolved during popup initialization,
before mapping. Mapping the menu therefore broke Show Desktop.

## Correction and controlled regression

`kwin-desktop-popup-membership.patch` overrides membership only for XDG popups,
inheriting it from their transient parent. This also covers nested submenus.
It does not classify ordinary toplevel windows by application identity, turn
gadgets into wallpaper/docks, or exempt all layer-shell menus.

Four new layer-shell rows exercise a gadget menu, preview menu, ordinary
layer-shell menu and similar-name non-exempt menu. An ordinary application is
present so the tests check both the global mode and whether that application
remains hidden. Each passing row also maps/closes a nested submenu and checks
parent links, desktop membership and closing-menu behavior.

Against KWin 7.2, the targeted run has **four passes and two failures**: both
desktop-component menu rows incorrectly exit Show Desktop; both unrelated
controls pass. With the correction, the complete layer-shell suite has
**76 passes and zero failures**. Logs are retained in
[gadget-popup-logs](gadget-popup-logs/). Setup/cleanup count toward Qt totals.
The protocol-error output in the final test is its deliberate invalid-buffer
case, which passes; it is not a spontaneous compositor failure.

- Patch SHA-256: `db680d1b7bc030f4767bab0e79eaaa6209450950eed8de94c0251aab3ecc6d94`.
- Test executable SHA-256: `1432324cfad6202881a3d6e2a88e204f8f621c9470d079bc6c1eeafeb94f1608`.
- Test library SHA-256: `77cb0541d00219797e71f1503ac33e25a37ebfc76c42051ba9e60ba082b53873`.

## Package and release gate

A normal KWin `6.7.4-7.3` package build is started in
`work/beta2-kwin73.N1i470`, using the preceding recipe plus this patch and a
release-number increment. Source checksum and upstream signature verification
pass. A recursive comparison confirms the prepared package source is identical
to the source that passed the 76-result suite (`tested-source-comparison.log`
is empty, comparison exit 0). Builds remain limited to two jobs. The test-build library is not installed
or substituted into a distribution package.

Package completion, identity/hardening comparison, normal VM upgrade and native
menu/submenu replay remain pending. The VM still runs KWin 7.2. The build
manifest remains KWin 7.1 / Gadgets 10. The
[checked-menu indicator follow-up](2026-09-13-gadget-menu-indicators.md) and
broader gadget/release gates remain open. No final ISO or publication is approved.

The initial build was unexpectedly terminated (exec exit 143) at 56%, with no
compiler error reported. Read-only process checks confirmed makepkg and its
compiler children had stopped; the source comparison remains identical. The
object files and original build log are retained for an incremental resume,
after the small gadget-indicator regression/package pass. This is not a
successful package build or a failure of the controlled compositor tests.

The first incremental resume reached linking but failed with unresolved
`GLVertexBuffer` and `IccShader` methods (exit 4). Inspection confirmed that
`glvertexbuffer.cpp.o` and `icc_shader.cpp.o` were both zero bytes; these were
the two compilation units active at the interruption. A scan of all generated
object files found no other zero-byte objects. The two empty files were moved
recoverably to `interrupted-objects.5ltp8F` inside the package work directory.
The original and failed-resume logs are retained. A second incremental build
in `build-recovered-objects.log` recompiles precisely these two missing objects
and retries linking, with two jobs and the normal recipe/hardening unchanged.
Completion and installed verification are still pending.

The recovered normal build completed successfully at 15:14:27 CEST. No generated
object files remain zero bytes. Archive SHA-256:
`32fdebc384498639412bbfd10822c47ae7139c4c041de4e8a93ba58dcd35ca75`.
The package comparison `work/kwin73-package-audit.4ef5Gf` preserves all 2,256
paths/modes/symlinks and direct dependencies, stack permissions and RELRO status
for all 63 ELF files. Package metadata is unchanged apart from expected version,
timestamp and size. The normal hardening/link flags remain in the build cache.

Executable SHA-256:
`dbc604c4a6cbe57ae7c049a897aa88da5adbb375d79a3b48dd1f194d90f3c20b`.
Library SHA-256:
`eb45e25fa8e76366b35ebc15fedbbfd52129f180a50a7a00193bb3306651497e`.
Wrapper SHA-256 (unchanged):
`a6b23e6a6ad26fe4a421a20b8b2d7eefe6be61dc38d49d4b9d60706045b53887`.

Normal offline 7.2→7.3 upgrade passes in `kwin73-upgrade.r5KuHg`, with all
package files, executable/library identities and `cap_sys_nice=ep` verified.
A normal Start-menu restart is requested. Post-reboot running-library audit
and native popup/submenu replay remain required; a package install alone does
not prove the old mapped compositor library was replaced.

Post-reboot audit `kwin73-boot.D6zmy2` passes in normal session 2, boot
`fde6a493-c3b9-459c-a5c9-47f8afe5cb9c`. It verifies wrapper PID 760, compositor
child 767 and the mapped library inode/hash, with no permission-check bypass.
Shell/compositor/Plasma services have zero restarts; no failed units are listed.

Native replay `kwin73-popup.Fyx876`, still using Gadgets 16, passes the scoped
popup workflow: Meta+D hides Paint/Terminal while gadgets remain; right-clicking
Calendar opens its root menu without restoring the applications; pointer motion
opens the Size submenu without restoring them; dismissing both menus retains
Show Desktop. The trace has `show_desktop_changed(1)` before both popup mappings,
and no reset when either maps or closes. Explicit Meta+D then reports state 0
and restores the applications, with Calendar promptly behind them. Screenshots
and the native trace are retained in `gadget-popup-logs`.

A subsequent, separate keyboard Size→Large→Return probe in the same compositor
again crashes Gadgets 16. This confirms the native menu-style teardown finding
is not fixed by changing KWin and remains a separate gadget gate. It does not
invalidate the preceding successful pointer popup/Show Desktop sequence.
The subsequent Gadgets 17 upgrade passes that same keyboard replay on KWin 7.3,
and its transparency, drag/restart persistence and normal-login audit also pass;
see the [release-17 evidence](2026-09-13-gadget-opacity.md#package-and-installed-wayland-replay).
Broader compositor/gadget and final-media acceptance remain open.
