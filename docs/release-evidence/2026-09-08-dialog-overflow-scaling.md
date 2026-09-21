# Common-dialog overflow and scaling — 8 September 2026

Local candidate work after installed Explorer 51. Not packaged, shipped in an
ISO, committed or published. The earlier installed/reboot evidence remains in
[the breadcrumb report](2026-09-08-common-dialog-breadcrumbs.md).

## Reproduced defects and correction

The new regression created a narrow address bar with a 180-character final
folder name and tested 9-, 18- and 28-point fonts. Before the correction, all
three rows failed: the normal-font folder button exceeded the viewport width;
the two larger fonts exceeded its fixed 27-pixel height. Setup/cleanup passed.
The original test output was returned by the command session, not saved as a
raw test file; the original build log is retained. This is not a missing-log
claim that the old code passed.

The private breadcrumb bar now sizes its height from actual styled buttons,
elides overlong labels while preserving their full accessible names/tooltips
and real destinations, and exposes an ancestor menu when the hierarchy will
not fit. The first visual replay showed a small clipped fragment of the prior
button (166); the follow-up displays only a contiguous suffix of whole buttons.
The regression now checks every visible button's viewport containment.

The menu uses text and existing native controls, not new artwork. Ctrl+L still
edits the real address; Escape abandons editing without dismissing Open/Save.
No filesystem destination, save backend, public dialog class layout or global
shortcut was changed.

## Validation

- First correction: 5 passing focused rows including setup/cleanup, all 20
  CTest groups, then 54 Wayland rows and 6 focused rows each at 150% and 200%.
- Whole-button follow-up: all 20 CTest groups passed in 23.39 seconds.
- The final candidate passed 54 Wayland rows and the two scaled 6-row runs.
  Each scaled run covers normal/large/very-large fonts and Ctrl+L/Escape.
- Both VM passes used process-local `LD_LIBRARY_PATH`; the installed Explorer
  51 library hash was unchanged. No installed package or desktop scale changed.
- The native Save As preview navigated a real long temporary directory,
  exposed all ancestors through its menu, and navigated back to Projects while
  preserving `keep-this-name.png` without accepting the dialog (166–168).
- The isolated preview profile showed a dark palette, even with kdeglobals
  copied. A normal-profile replay displayed the expected light palette (169).
  This does not establish a production dark-mode regression; the incomplete
  QA profile must not be used as representative release imagery.
- The final candidate's normal-profile replay shows the long component and
  dropdown fully inside the bar with no preceding fragment (170), its complete
  ancestor menu (171), and successful Projects navigation (172). Cancel closed
  the dialog. The final audit found no remaining native-dialog process, no
  saved `keep-this-name.png`, 665 installed Explorer files with none missing,
  and the unchanged installed-library hash.

Final candidate library SHA-256:
`38281ed02c6ca759163e1139b3bd90e1e1eb4a10c85f3f1fdf86f0158038b799`.
Final test executable SHA-256:
`fba719e02594943cf264c685e71c4ea96ff01507bf63a76047da6afaae196736`.
Build/test logs and screenshots are retained in `dialog-overflow-logs/`.

## Removable-device replay and remaining gates

A separate sparse copy of the old 96 MiB FAT QA fixture was prepared at
`/home/admin/VMs/aero7-beta2-r10-oTmJ9G/usb-dialog-qa/removable.img`.
The old fixture was not modified. QEMU rejected hot-adding a USB controller
because this VM's root PCIe bus does not support hotplug. No USB device was
attached and no guest mount was performed. The unused block node was removed
successfully; the scratch image is retained for the next launch with a USB
controller configured. Do not count this as a live-removal acceptance pass.

Still required: actual mount/removal/recovery with this breadcrumb candidate,
package integration and installed/reboot regression, broader scaling and
multi-monitor checks, and both rebuilt final-media installation passes. The
early-Escape screenshot issue and the other release gates remain open.
