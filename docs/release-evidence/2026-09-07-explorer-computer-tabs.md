# Explorer 41 — keep Computer below the real tab bar

Local source, packaging and upgraded-VM work, not final release acceptance.
Explorer 41 was installed in the offline VM and selected for the next ISO during
this check. Explorer 42 subsequently superseded it; see the split-layout report.
No commits, signing, promotion, upload or publication occurred.

## Reproduced defect and correction

The installed Explorer 40 VM screenshots 211–214 show that activating Computer
hides the tab strip. Keyboard switching works, but another tab cannot be clicked.
The window-wide alternate-content stack contains the entire DolphinTabWidget,
so selecting Computer also hides the widget that owns the tab bar.

Explorer 41 keeps the actual DolphinTabWidget as the central widget. Each
DolphinViewContainer owns its own folder/Computer stack below that tab bar.
The main window follows the active container's content without replacing the
tabs, sibling split pane or per-tab navigation history. Opening a drive first
activates its owning container, then navigates through that container's real
URL/history backend. Icons and exported common-dialog API are unchanged.

## Regression evidence

- A new mouse-click test failed on the old implementation because the tab bar
  was not visible after selecting Computer.
- After the correction, it clicks Computer, clicks back to the folder tab,
  returns to Computer and closes that tab. Visibility, mouse-accessible region,
  selected tab, surface and surviving folder URL are asserted.
- A split-pane regression checks that Computer and the neighboring home pane
  remain visible, and navigating Computer to root preserves the other pane.
- The existing launch selection, Back/Forward and keyboard tab restoration
  checks remain in the suite.

An initial full run reported 45 main-window passes and one failure in the
fresh-library sidebar test: Qt's shared `.qttest` profile contained a preexisting
New Library entry. The failure log is retained. No old profile data was deleted
and the expected Pictures row was not changed. The main-window test now creates
a process-local temporary XDG profile with four explicitly isolated library
folders before QApplication startup. It no longer shares `.qttest` libraries.

The subsequent all-target build and all 19 CTest groups passed in 19.59 seconds.
The main-window group reports 46 passes; its new mouse and split-pane assertions
passed. ViewProperties reports 12 passes and no skips in this run, including
the extended-attribute-full path; earlier runs' capability skips are not carried
forward as the result of this run.
This is source/offscreen evidence, not installed Wayland graphical acceptance.

## Packaging identity and remaining checks

Source: `aero7-file-explorer-25.12.3-r41.tar.gz`.
SHA-256: `c8e42a6f716f1b4eee876a65b38d022e6a9f4b509c74abd7737d1982eb34bd3d`.
PKGBUILD SHA-256: `2aaa9921d513769e2f1a4343b74996f6649e3447195d2ba2c7068e74962f183c`.
SRCINFO SHA-256: `ce8f66d6a2648a34ba942e007724e46541b68e732f156a005c1c298d9faf81da`.

Build directory: `work/beta2-explorer41.dGgJgn`; log: `explorer41-package.log`.
The normal local recipe builds with two jobs. `makepkg --nodeps` skips the host
dependency presence precheck only; it does not install host packages or force
package dependencies in the VM. The frozen r40 archive is preserved.

The build finished successfully on 7 September at 00:13:41 CEST.
Package: `aero7-file-explorer-25.12.3-41-x86_64.pkg.tar.zst`, 8,232,258 bytes.
SHA-256: `76c7fb88da148eb982ee891811c43936c899ac8a096571645b22e71f4b14c3c9`.
Shared-dialog linkage, repository source verification and ISO static checks
passed. The latter includes all 134 backend tests after the repeat-branding fix.

Prepared VM helpers are in `/home/admin/VMs/aero7-beta2-r9-xTfYQR/inputs/` with
`explorer41` names. They have run. The shared-dialog test binary is an
exact copy of the previously used ABI-compatible QA executable, not a different
product library; it resolves the actual installed library with no override.

## Installed Wayland VM results

The existing disconnected r9 guest upgraded normally from Explorer 40 to 41.
Only Explorer changed; Paint 8 settings matched their pre-upgrade checksum.
Package integrity reported 665 Explorer files and 709 Paint files, zero altered.
Installed shared-dialog checks passed 35 cases (33 functional plus setup and
cleanup), with no skips, in 3,886 ms. Paint's five isolated workflows passed:
same window, separate window and unsaved Cancel, Discard and Save. Exported
audit logs contain the success markers; the manual Explorer process closed
normally and had no unknown Computer-protocol warning.

Actual 1920 x 1080 screenshots 221–236 in the r9 offline VM evidence directory
confirm Computer/C:/Pictures navigation, Back/Forward, visible mouse tab
switching, Computer-tab closure and preservation of the other split pane.
The drive click in the left Computer pane activates and navigates that pane
without replacing the right Pictures folder.

The deeper split-view sequence exposed **two remaining layout defects**:
an inactive pane retains an extra details row (232–234), and closing split view
leaves the secondary breadcrumb visible (235). These are not excused by the
passing dialog/process audit. Explorer 42 source regression work follows;
Explorer 41 is not complete graphical or final-image acceptance.

Logs are in `computer-tabs-logs/`. Final new online/offline ISO builds and full
installation acceptance remain separate and pending. Credential Manager/Wallet,
portal failures, branding package ownership and the intermittent Plasma shutdown
timeout remain on the wider release checklist.
