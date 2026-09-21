# Explorer 39 — Computer breadcrumb and sidebar

Local work only. The r39 source tests and package build pass. Explorer 39 is
selected locally and upgraded normally in the offline guest. The three visual
fixes and compatibility checks pass, but the longer navigation check exposed
a history defect described below. Neither immutable r9 image contains
these changes. No commit, publication, or signing was done.

## Defects and implementation

Explorer 38's installed VM displayed `aero7computer:` and logged unknown-protocol
warnings. Blocking navigator signals did not block its own KIO jobs. Computer
now uses the already existing local managed Computer place for the navigator,
while retaining the integrated Computer surface and original Dolphin folder
view behind it. Breadcrumb presentation reduces that exact location to
Computer; it does not relabel arbitrary folders called Computer.

The sidebar previously reserved a row for the literal name New Library even
when it did not exist. It now paints actual visible library model indices;
missing entries take no space. Drive rows also retain their model indices,
rather than looking them up again by potentially duplicated display names.

The default navigation pane now measures standard captions with the current
font plus icon/indent margins (minimum 160 pixels), instead of imposing 133
pixels. Longer nonstandard names are elided rather than cut mid-glyph. The
pane retains a resize range. This is not a claim of complete sidebar scrolling,
keyboard accessibility, runtime font-change, or device management acceptance.

## Regression evidence

Before implementation, new tests failed for Computer's unregistered URL and
the missing-library gap. After implementation all three targeted cases passed:
resolvable Computer breadcrumb/restoration, Pictures directly after Music, and
standard sidebar captions fitting the viewport. The default-label test also
passed under the smaller offscreen font before the change; the installed-VM
clipping finding remains the evidence for that visual issue.

The first full run correctly rejected the changed geometry because an older
chrome test required exactly 133 pixels. That assertion now requires the
font-aware default width; the independent text-fit assertion remains. All 19
CTest groups then passed in 18.76 seconds. The main-window group reports 41
passes. Existing offscreen plugin warnings and the unrelated filesystem-based
ViewProperties skip remain; neither is presented as full graphical acceptance.

Logs are retained under `computer-sidebar-logs/`, including both failing runs.

## Build identity and next gate

Source: `aero7-file-explorer-25.12.3-r39.tar.gz`.
SHA-256: `c5fbab6ff95c012dedad2bda6fd3da4c291ea826ac85055d6a6f91fda57fdecd`.
Its path inventory matches r38; existing icons are unchanged.
Canonical recipe and `.SRCINFO` are r39, with matching lock hashes.

The clean local package build completed at 23:30:25 CEST under
`work/beta2-explorer39.qW9GTB/`.
It uses `makepkg --nodeps` only for the host dependency-presence precheck,
with two compile jobs; it does not install host packages. Production packaging
disables test compilation, so the source test results above are separate.

Package: `aero7-file-explorer-25.12.3-39-x86_64.pkg.tar.zst`, 8,232,567 bytes.
SHA-256: `81bed01a1f925d0e4c42b7114a3488cd41f59ebeb511d54cc678549c159c4dd1`.
The local selection and VM input copies match. Repository source validation
passed; ISO static checks passed, including 133 backend cases and the actual
ELF shared-dialog dependency/SONAME guard. Existing QML warnings are retained.

The disconnected r9 guest upgraded from Explorer 38 to 39 through a normal
pacman transaction. The before/after package list differs only in Explorer;
Paint 8 stayed installed. Package checks found zero altered files across
Explorer's 665 and Paint's 709 files. This time a fresh pre-transaction Paint
settings checksum was taken and its post-transaction comparison passed.

## Installed graphical and compatibility results

The installed shared library passed 33 functional common-dialog checks plus
setup/cleanup on Wayland (35 passes, zero failures, 4,651 ms). Paint 8 passed
all five readiness-aware document workflows in the isolated profile
`paint8-readiness-workflow.kneeGg`. The final export/integrity/settings audit
passed; its marker certifies those checks, not all Explorer behavior.

Offline r9 screenshots 188–194 show the exact installed binary:

- Computer's breadcrumb says Computer, with no raw protocol.
- C: opens the real filesystem root; Recent Places and Local Disk (C:) fit.
- Pictures follows Music with no phantom New Library row and opens the actual
  Pictures library. Returning through the Computer sidebar entry works.
- The app closes normally, and its complete manual-run log has no KIO
  unknown-protocol warning (only the begin/end markers).

The longer sequence exposed a separate history defect: after C: → Pictures →
Computer, Back goes to C: instead of Pictures; Forward goes to Pictures and
cannot restore Computer. Computer had changed only the visible navigator,
not Dolphin's per-tab history. Initial Computer launch also retained a stale
sidebar selection, and history navigation left a partial selection highlight.
These are not accepted as working in Explorer 39. New failing source regressions
for Back/Forward and launch selection are in progress toward the next package;
the current r39 archive remains immutable.

Final rebuilt online/offline media and their complete installation matrix
remain separate release gates.
