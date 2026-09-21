# Explorer 43 — preserve folder details across tab and split changes

Local source/package and upgraded-VM checks. Final fresh online/offline ISO
acceptance remains pending; this is not publication approval.

## Defect and correction

Explorer 42's installed VM lost the ordinary folder count after split collapse
and tab restoration. `DolphinStatusBar::setComputerMode(false)` cleared the
default and hover text even when it was already in ordinary-folder mode.
Explorer 43 returns early when the requested mode is unchanged. Actual mode
transitions retain their existing reset behavior.

Two red regressions reproduced empty text: one exercised repeated mode-setting,
the other switched active split panes. The green tests assert exact one-item
and two-item counts through new tabs, both focus directions, animated split
collapse, Computer tabs and restoration. A separate test checks hover text and
restoration of the normal count. These checks complement, not replace, real
Wayland interaction.

All 19 source CTest groups passed in 20.72 seconds; the main-window suite passed
49 cases in 10,319 ms. Frozen source and package identities:

- Source: `aero7-file-explorer-25.12.3-r43.tar.gz`
  SHA-256 `4dd434d828c5b61139b08fc39af8ca82010adb11b460448dc76df4d8e08ebf37`.
- PKGBUILD SHA-256 `9a12c30b2a379b1a3a7598745abc8dc8348ff254595092892e554501328be60a`.
- SRCINFO SHA-256 `8e245438b94a97fd82ee8f9ade0354839114e4fea7406a3c77e0d598329eaa27`.
- Package: `aero7-file-explorer-25.12.3-43-x86_64.pkg.tar.zst`, 8,231,597 bytes.
  SHA-256 `299e4aec98807fbe97c1d962b625230924367dca5a933b11cc753e4d97d38239`.

The normal two-job recipe finished on 7 September at 00:55:16 CEST, under
`work/beta2-explorer43.5nFR03`. The host-only dependency precheck skip did not
install host packages or bypass guest package dependency resolution. Previous
frozen source archives were preserved. Repository validation and ISO static
checks passed, including 135 backend tests and the theme-branding archive check.

## Installed VM gate

The disconnected r9 offline guest was normally upgraded from Explorer 42 to 43.
Only Explorer changed; Explorer and Paint reported zero altered files and Paint
preferences retained the original checksum. The initial sudo prompt timed out;
a later attempt stopped before creating its upgrade log. Retrying with the
normal input delay and shell tracing completed the guarded upgrade. No safety
guard or package dependency was removed to obtain success.

Installed common-dialog tests passed 35 cases (33 functional plus setup/cleanup),
zero failures/skips, in 3,857 ms. Paint passed all five isolated workflows with
profile `paint8-readiness-workflow.4mryap`. Evidence is under
`/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`;
the successful upgrade is recorded by screenshot 269 and the version-specific
upgrade log. These are upgraded-guest checks, not fresh final-media acceptance.

Actual 1920×1080 Wayland screenshots 272–284 verify:

- Pictures shows four items after splitting, focusing the other pane and
  collapsing the split (273–274).
- The four-item count survives a new Computer tab, mouse return to the split
  tab, opposite-pane focus and a second collapse (275–277).
- A selected image displays its details. A repeated selection/tab/deselection
  sequence restores the four-item count after settling (278–281). Screenshot
  279 was taken during the intermediate update and is not the settled result.
- Closing Pictures leaves Computer usable. Opening C:, Back to Computer and
  Forward to C: retain the correct view and readable drive name (282–284).
- Explorer closes normally. The exported audit confirms all test markers,
  no unknown Computer-protocol errors, zero altered Explorer/Paint files and
  unchanged Paint preferences.

This closes the reproduced missing-count regression. Mounted-device/unplug/eject
coverage, broader selection-state semantics and final fresh media remain separate
acceptance work. Source, package and VM logs are retained in `details-state-logs/`.
