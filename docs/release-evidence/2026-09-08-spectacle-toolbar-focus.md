# Spectacle toolbar focus correction — 8 September 2026

Status: source, QML-component, package and bounded offscreen-startup checks
complete. The [installed follow-up](2026-09-08-portal-installed-validation.md)
now verifies normal upgrade/reboot and actual region/clipboard-lifetime replay.
Keyboard, notification/viewer and broader workflow checks remain pending. No final media,
signed package repository, commit or publication was changed.

## Reproduced cause and fix

The installed r10 journal `snipping-recovery-packaged.log` repeatedly records
focusPolicy override warnings from ButtonGrid, UndoRedoGroup and
AnnotationOptionsToolBarContents. These containers declared their own integer
focusPolicy even though [Qt Quick Item already provides that property](https://doc.qt.io/qt-6/qml-qtquick-item.html#focusPolicy-prop).

The patch renames the custom setting to `buttonFocusPolicy` and updates the
child bindings and two explicit capture-overlay overrides. It does not assign
StrongFocus to the containers themselves: their native Item focus policy stays
NoFocus, avoiding an unintended extra keyboard-focus stop. Normal toolbar
buttons retain StrongFocus, and capture-overlay annotation buttons retain their
NoFocus setting. Icons, geometry, artwork and capture/save behavior were not
changed. The existing background-error exit-status patch is retained.

Patch: `../../patches/aero7-toolbar-button-focus.patch`

SHA-256: `d3c3d90bb3a2f8888fe30d29fff7867376a040ed8fdc30b9d50407b661d145ef`.

## Actual-component checks

The fixture loads the real QML component files with real KDE controls and the
real KQuickImageEditor annotation document. Only the SpectacleCore application
singleton and window context are substituted. It checks native container focus,
StrongFocus defaults and NoFocus/StrongFocus propagation to actual tool buttons.
It also rejects the original focus warnings and QML errors.

- ButtonGrid: passed, no tool buttons in this base container.
- UndoRedoGroup: passed, 2 tool buttons.
- AnnotationsToolBarContents: passed, 14 tool buttons.
- AnnotationOptionsToolBarContents: passed, 2 tool buttons with rectangle options.

All four pass under `org.kde.desktop`; the unmodified source fails all four and
emits the original override warnings. This checks component properties and
bindings, not real keyboard-event routing through the fullscreen capture window.

An initial fixture explicitly using Qt's Basic control style passed three cases
but exposed an annotation-options height binding loop and a text-context-menu
signal mismatch. That result is retained, not counted as a pass or suppressed.
The KDE-desktop-style run has neither QML error. Basic-style compatibility is
not established by this pass. A missing Breeze icon-theme warning in the isolated
host fixture is also retained; no icon assets were invented or replaced.

## Full application and package

`spectacle-1:6.7.4-3-x86_64.pkg.tar.zst`

- Finished: 20:40:05 CEST.
- Size: 2,477,980 bytes.
- Package SHA-256:
  `d918e0041351a7c1b9643e15e8eee7e05547e6062b80b4bfd95cc29fb206797b`.
- Packaged executable SHA-256:
  `69a1d278003966fc79cc8aa5177ecaf8fc804583469ccb5d1dd97d45379bcc19`.

The signed KDE 6.7.4 source archive passed SHA-256 and GPG verification. Host
runtime/build dependency checks passed without installing packages. Fresh
package compilation and all four component tests passed; the upstream filename
suite passed. The other upstream CTest entry, appstreamtest, reports success
while skipping before installation. It is not counted as metadata validation:
`appstreamcli validate --no-net` was run directly on the exact source metadata
and passed. All six ELF direct-library requirement sets match package 2. Every
non-ELF payload file is unchanged; only package metadata and the main executable
differ. This does not establish runtime dependency closure on the guest.

The bounded full-application probe opens KDE's bundled logo image through
`--new-instance --edit-existing` in an offscreen session. The original binary
logs ButtonGrid and UndoRedoGroup focus overrides; the exact packaged candidate
does not. The independent annotation-options component test covers the third
warning, which this particular full-application startup did not reproduce.
Each application was deliberately terminated after eight seconds; status 124 is
the fixture's timeout, not proof of a normal application exit or a startup hang.
No screenshot was taken and no modified image was saved.

The first offscreen probe isolated the application's XDG directories but set the
environment after starting the private bus. The corrected probe applies that
environment before dbus-run-session, including to its activated services.
Earlier logs are retained; their bus and portal processes exited, and no fixture
FUSE mount remained. Both corrected attempts use fresh configuration/cache/data
and runtime directories. Limited offscreen/backend/icon warnings remain recorded
and are not represented as a warning-free real desktop.

Evidence: [spectacle-focus-logs](spectacle-focus-logs/).
Work directory: `work/beta2-spectacle-focus.m9778x/`.
Corrected full-application probes: baseline `viewer-startup.nD6t19`, packaged
candidate `viewer-startup.G7V5N6`.

The package is staged in the r10 QA inputs share but not installed. Next gates:
normal installation, real region selection and Escape, toolbar keyboard behavior,
PNG saving, image paste, notifications, error/retry and post-reboot checks.
Package-repository selection remains at Spectacle 2 until those checks. Frozen
r10 ISOs are unchanged.

The guarded `install-cp51-spectacle3.sh` and post-reboot
`audit-cp51-spectacle3.sh` are staged alongside those exact archives. ShellCheck
passes; both scripts reject the host with status 2 before changing anything.
The archive verifier confirms both package identities/checksums and finds no
unsafe member paths or VCS metadata. Its six regression tests also pass.
These are preparation checks, not guest installation results. The reboot audit
discovers Action Center's actual service from its running executable instead
of assuming a generated unit name, and retains full logs for review.

## Qt build still separate and active

At 20:40:19 CEST the existing `aero7-qt-portal-resume.service` remained
active/running with MainPID 9713. Its original failed preparation unit remains
failed as historical evidence; do not confuse that with the resumed compilation.
The full Qt build subsequently passed step 1,095 of 2,178. A fresh 20:53:29 CEST
snapshot (`qt-portal-status.bBI6xG`) confirms the same resume unit, MainPID 9713,
makepkg 10023 and Ninja 15575 remain active; compilation subsequently passed
step 1,512 of 2,178. Package completion and installed-library/VM checks remain
pending. The QA guest remains powered off while this build runs.
