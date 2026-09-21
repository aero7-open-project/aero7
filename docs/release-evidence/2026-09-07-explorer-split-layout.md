# Explorer 42 — split-view details and breadcrumb ownership

Local source and packaging work. Final online/offline ISO acceptance is pending;
no commit, signing, promotion, upload or publication is authorized by this report.

## Reproduced defects

Installed Explorer 41 screenshots 232–234 show an extra details/status row inside
the inactive split pane, in addition to the active full-window row. Screenshot
235 shows that closing split view leaves a second breadcrumb behind.

Both were reproduced in source tests before correction. The inactive-status
assertion failed; a separate test failed when the secondary breadcrumb remained
visible after collapsing split view. Both failure logs are retained.

## Corrections

- Tab containers opt into window-managed details bars at creation, including
  inactive containers that have not yet received focus. Returning a bar to its
  container returns ownership without adding a visible row to that pane.
- Status-mode refreshes keep inactive details hidden. Per-pane compact-bar
  geometry cannot overwrite the window-managed bar's layout.
- Secondary breadcrumb visibility now follows the explicit split-view state,
  including active-tab changes. It no longer depends on Show/Hide events from
  a dummy widget inside Aero7's hidden upstream toolbar.
- The whole secondary breadcrumb frame and its separator hide together.

Tests exercise both focus directions, status-mode refresh, Computer-to-C:
navigation beside another folder, closing/reopening split view, switching to
a single-pane tab, returning to the split tab and closing it. Existing mouse
Computer-tab navigation remains covered.

All 19 CTest groups passed in 20.00 seconds. The main-window suite reports
47 passes, zero failures and zero skips. Targeted tests report five passes
(three functional plus setup/cleanup). These are source/offscreen results,
not a substitute for actual installed Wayland interaction.

## Frozen source and package gate

Source: `aero7-file-explorer-25.12.3-r42.tar.gz`.
SHA-256: `9b447c2ff7dd96df3251ccb6924f87ff3146460d051d66671b0d7f91b21d2f30`.
PKGBUILD SHA-256: `9284414eb0142b628ff30c6003a6cff2f7953380459e7e1f99d3a6121f0b3445`.
SRCINFO SHA-256: `cc3d4ef681560ee0a8be1844ac3d57a6588853fecc0c0aaf720a4ade6a61bf8c`.

Build directory: `work/beta2-explorer42.kZzu6J`.
The normal local recipe built with two jobs. The host-only `--nodeps`
precheck skip does not install host packages or bypass VM package dependencies.
Frozen r41 source/package evidence is preserved. Repository source validation
passes; its prune tests remove only their own temporary fixtures.

The package build finished on 7 September at 00:37:02 CEST.
Package: `aero7-file-explorer-25.12.3-42-x86_64.pkg.tar.zst`, 8,231,257 bytes.
SHA-256: `c04921d6d86fe33d53b254f9adbe87992089fb643745fa41512d5325452acb22`.
Shared-dialog linkage and ISO static checks passed, including 134 backend tests.
Explorer 42 is now selected for the next ISO and normally upgraded in the offline
VM. Only Explorer changed, Paint 8 settings were preserved, and both packages
reported zero altered files. Version-guarded VM helpers use separate r42 logs.
## Installed Wayland results and remaining status-text defect

Installed dialog checks passed all 35 cases (33 functional plus setup/cleanup),
zero failures/skips, in 3,899 ms. Paint 8 passed all five isolated workflows;
the exported profile is `paint8-readiness-workflow.YUZ27V`. The first attempt
to start Paint checks failed before launching the helper because the QMP text
driver did not type `~` in a log path. Retrying with the full user-home path
ran the checks successfully. This input-driver error is not a Paint failure.

Screenshots 245–261 under `/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`
confirm on the actual installed binary:

- Computer and Pictures remain visible in separate panes, with one window-wide
  details row, not a second row in the inactive pane.
- Clicking the left Computer drive activates/navigates only that pane.
- Closing split view hides the complete second breadcrumb; reopening restores it.
- Mouse switching between a split tab and a single Computer tab shows the right
  breadcrumb count and preserves both views. Closing the split tab leaves the
  Computer tab usable. Computer/C: Back and Forward still work.
- Explorer closes normally; exported logs show no unknown Computer protocol
  warning. Post-test integrity reports zero altered Explorer/Paint files and
  unchanged user Paint settings.

**Not complete graphical acceptance:** the remaining row loses its ordinary
folder item count after collapsing split view or returning to the split tab
(249–251 and 255). Waiting and moving the pointer away did not restore it;
reopening a view did. Source inspection identifies that
`DolphinStatusBar::setComputerMode(false)` unconditionally clears `m_defaultText`,
even when already in ordinary-folder mode. Active-view restoration now calls
that mode reset. This needs an idempotent mode transition and regression checks
that assert the text, not merely the bar's visibility. Do not change the frozen
r42 archive; any source correction must be packaged as a later revision.

Evidence logs are in `split-layout-logs/`. The immutable r9 images contain older
packages; even an upgraded guest passing these checks is not final-image proof.
