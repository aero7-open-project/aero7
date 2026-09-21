# Explorer 40 — Computer in normal navigation history

Local source and packaging work. Explorer 40 is built, selected for the next
ISO build and normally upgraded in the offline VM. The targeted installed
history and compatibility checks passed, with a separate tab-strip visibility
defect recorded below; final ISO acceptance is not claimed. Nothing was committed,
signed, pushed or published.

## Reproduced failure

The installed Explorer 39 sequence C: → Pictures → Computer → Back goes to C:
instead of Pictures. Forward then goes to Pictures, not Computer. Screenshots
191–193 in the offline r9 VM evidence demonstrate this. A direct Computer launch
also leaves the old C: sidebar selection (188). Native history navigation can
leave a partial selection highlight because the custom sidebar uses different
row geometry from KFilePlacesView.

New source regressions for Computer Back/Forward history and initial sidebar
selection both failed before the change. Those logs are retained, not replaced
by the subsequent green runs.

## Source correction

- Computer now adopts the existing local managed Computer location in Dolphin's
  real per-tab navigator, instead of changing only the visible address bar.
- The normal URL signal selects the integrated Computer surface for that exact
  location. No unregistered KIO protocol is used internally.
- Hiding the Computer surface changes presentation only; it no longer reloads
  or rewrites navigation state behind a history operation.
- Direct Computer launches start with that managed location, and switching
  tabs restores the correct Computer/folder surface and sidebar selection.
- Programmatic sidebar URL changes request a complete viewport repaint because
  native row invalidation rectangles do not match the custom grouped layout.
  The installed sequence below confirms intact selection highlights.

## Tests and immutable source

The targeted history, launch, breadcrumb and Computer-details checks passed.
A full all-target build followed by all 19 CTest groups passed in 18.88 seconds.
The main-window group reports 44 passes, including a new Computer/home tab-switch
test. Back/Forward coverage checks multiple traversals between root, Pictures
and Computer; this does not certify every history-menu, multi-window or session
restore path. The unrelated ViewProperties filesystem-capability skip remains.

Source: `aero7-file-explorer-25.12.3-r40.tar.gz`.
SHA-256: `fff1c24db8a2251eeed27d8201680702ec1a8d63dba07a49c9ce192227f4ef61`.
Canonical recipe and `.SRCINFO` now describe r40, with updated lock hashes.
Build: `work/beta2-explorer40.xNxPjx/explorer40-package.log`, two compile jobs.
As with the earlier local builds, `makepkg --nodeps` skips the host dependency
presence precheck only; no host packages are installed. The production recipe
does not build tests, so source-test results are a separate evidence set.

Package: `aero7-file-explorer-25.12.3-40-x86_64.pkg.tar.zst`, 8,232,844 bytes.
SHA-256: `01f857ace0d429ad1843f39be459172ed284c0acc0a6d1de5cb46eef69c5d738`.
The build completed at 23:50:24 CEST on September 6. Native shared-dialog ELF
linkage verification and the ISO static checks passed. The existing QML lint
warnings remain; passing static checks do not demonstrate graphical acceptance.

Normal offline-VM upgrade changed only Explorer 39 to 40. Paint 8 remained
installed with its configuration checksum unchanged. Package integrity checks
reported 665 Explorer files and 709 Paint files with none altered. Missing sync
database warnings in this disconnected test guest were retained in the log.

## Installed Wayland checks at 1920 x 1080

Screenshots are retained under `/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`.
This guest was originally installed from r9 and then normally upgraded; it is
not a fresh install of new final media.

- 201: direct Computer launch selects Computer, with a readable address label.
- 202–204: the real C: tile opens root; Pictures opens the four existing PNG
  fixtures; the Computer sidebar entry returns to the integrated drive view.
- 205–210: Back reaches Pictures; Forward reaches Computer. Repeated Back
  reaches Pictures and then C:, followed by Forward to Pictures and Computer.
  Sidebar selection remains intact in every captured state.
- 211–214: Ctrl+T creates a second tab, which is navigated to Pictures.
  Ctrl+Tab restores the original Computer surface and another Ctrl+Tab restores
  Pictures. The address, command bar, status area and sidebar match each tab.
- 215: closing the second tab and then the window exits normally. Its exported
  log contains no unknown-protocol warnings.

**Remaining defect:** the tab strip disappears while Computer is active
(211 and 213), because Computer replaces the container that owns the tab bar.
Keyboard tab switching works, but mouse access to the other tab is hidden.
Do not describe tab UI acceptance as complete. This requires a subsequent
source/package correction; do not modify the already hashed r40 archive.

The actual installed shared-dialog library passed 33 functional cases plus
setup/cleanup (35 passes, zero failures, 4,566 ms). Installed Paint 8 passed
same-window, separate-window, unsaved Cancel, Discard and Save workflows using
the QA-only readiness probe and isolated `paint8-readiness-workflow.bTAamv`
profiles. The unchanged user Paint configuration checksum passed again.
The export audit marker `EXPLORER40_DIALOGS_PAINT8_AND_COMPUTER_LOGS_VERIFIED_NOT_FRESH_ISO`
does not assert visual correctness; the tab-strip finding remains separate.

Logs and isolated Paint workflow evidence are retained in
`computer-history-logs/`. Final rebuilt online/offline media retain their own
complete acceptance gate. Full removable-device, history-menu, multi-window
and session-restore coverage is still pending.
