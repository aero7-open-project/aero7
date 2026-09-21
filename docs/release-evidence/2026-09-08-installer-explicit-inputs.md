# Installer QML: explicit inputs and complete screen-loading regression

Local source/build/simulation evidence, 8 September 2026. This is not final
online/offline ISO acceptance or permission to publish.

## Failure and correction

The earlier full project check exited 1 with 150 `unqualified` QML warnings.
Most references were C++ context properties: controller, screenshot dimensions,
capture mode and documentation mode. Other references crossed delegate scopes
without explicit IDs. Qt documents why
[context properties are invisible to QML tooling](https://doc.qt.io/qt-6/qmllint-warnings-and-errors-context-properties.html)
and how [Loader initial properties](https://doc.qt.io/qt-6/qml-qtquick-loader.html#method-documentation)
can supply a component's inputs during construction.

The frontend now uses `setInitialProperties`. Main requires the real controller,
and every Loader replacement receives that controller and documentation mode.
The new `InstallerScreen` base declares this common input contract; SetupPage
inherits it. GlassWindow exposes a back-enabled property and a back-requested
signal instead of accessing a global controller. Both the Welcome window and
SetupPage explicitly connect the back action. Delegate IDs/scopes are qualified,
and unused imports are removed. No backend, partitioning, update preference,
firewall or layout policy was changed by this correction.

Standalone Qt 6 `qmllint` now exits 0 with no output. Warning levels and checker
failure handling are unchanged. The later ShellCheck stage exposed SC2043 in
the newly added one-item lsof policy loop. Its requirement is now part of the
existing multi-item system-backend loop. The policy test still executes the
actual verifier and rejects a base list missing lsof, firewalld or the update
dependencies, as well as fresh-install UFW.

## Validation

- Release build succeeds with the new QML resources embedded.
- Full `scripts/check.sh`: exit 0, `Static checks passed`; all 142 Python tests
  pass in 11.506 seconds. Package ownership/hashes, QML lint, approved branding,
  pinned Shell parity and ShellCheck all run through completion.
- All three CTest suites pass in 31.95 seconds: flowstate, installercontroller
  and installer-help. This includes existing guarded-backend/failure-path tests.
- UI suite: 19 passes including setup/cleanup, zero failures/skips (17 functional
  cases). Its eight loading configurations cover installer/OOBE, ordinary and
  documentation mode, and 1024×768/1920×1080. All 20 screens load forward and
  backward through the same engine (160 screen transitions in total), with
  correct source URLs, controller identity and documentation mode. Normal
  screen loading emits no QML-engine warnings.
- Missing controller is rejected for Main and all 20 screen resources. This
  deliberate negative test inspects component errors; its expected missing-input
  binding diagnostics are not mixed into the normal-loading warning check.
- Real simulated-controller Back/Next mouse actions pass for Welcome and
  Disk/Confirm. Existing mouse/keyboard help-dialog checks and time zone/region
  refresh checks also pass.
- The 1920×1080 Welcome capture before/after the change has absolute pixel
  difference 0 (`magick compare -metric AE`). It was also visually inspected.
- `git diff --check` passes.

Compiled local frontend SHA-256:
`afdbe32256ac849579796577f9824f8c259af680f16a0b68a13f891f155607e0`.

Logs and local offscreen captures are retained in
[installer-explicit-inputs-logs](installer-explicit-inputs-logs/). These captures
are engineering previews, not fresh-VM release screenshots.

## Still open

Follow-up: the [approved-icon correction](2026-09-08-installer-approved-icons.md)
resolves the two SVG warnings described below, with a stricter rendering test.
The following paragraph records the findings at this earlier checkpoint.

The screen sweep exposes Qt SVG parser warnings in the older original
`check-green.svg` and `recycle-bin.svg` filter markup. These are separate from
QML engine/lint warnings and remain recorded in the UI log. Follow-up must use
the project's approved icon pack, not invent replacement icons or hide parser
warnings. Other desktop/session warnings and the complete release checklist
remain open.

Neither final ISO has been rebuilt with this frontend and the selected
Explorer 50/Desktop 29/Plasma Workspace 3.2 stack. The previous offline VM PID
was no longer running when checked in this pass; no VM test or installation
is claimed here. Fresh online/offline install, OOBE, reboot and desktop checks
on the exact final artifacts are still required. No commits, pushes or public
downloads were made.
