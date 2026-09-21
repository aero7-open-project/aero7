# Gadgets 14: installed desktop and puzzle replay

12 September 2026, approximately 19:53–19:56 CEST. This is a scoped installed
interaction check, not release acceptance. No final ISO, commit or publication.

## Environment and isolation

The running offline VM is `aero7-r10-offline`, Wayland at 1920×1080, with no NIC.
Gadgets is `3.0.0-14`; the compositor is still `kwin 6.7.4-7.1`.
The launch helper checks the installed gadget executable SHA-256 against
`ad042dd2e5815b627cd10403b5f99e131accd182746c7b6a06d6d82b11dd480a`.
Clock, Calendar and Picture Puzzle run on a private D-Bus with separate
configuration/cache; the normal account layout is not edited. The private host
is stopped with Ctrl+C after this sequence.

The fixture image is an existing QA screenshot, not new product artwork. The
initial layout/helper remain in the VM input share as
`gadgets14-desktop-layout.json` and `gadgets14-desktop-qa.sh`. Runtime evidence
comes from `gadgets14-desktop.dHhsFO` in the results share; copies and screenshots
are retained in [gadget-desktop14-logs](gadget-desktop14-logs/).

## Show Desktop baseline

Clock and Puzzle are visible outside the ordinary application windows; Calendar
starts behind the overlapping terminal/Paint windows. Meta+D hides the visible
gadgets along with applications. Toggling it off restores them. The native trace
contains `show_desktop_changed(1)` and all three Top-layer requests, followed by
`show_desktop_changed(0)` and all three Bottom-layer requests. This confirms that
Gadgets 14 still needs the separate compositor correction. The KWin 7.2 package
is building; this replay does not claim it is installed or passes.

## Puzzle interaction

The 3×3 large puzzle begins with its blank at bottom left.

1. Clicking the non-adjacent top-right tile leaves the arrangement unchanged
   visually. The screenshot cursor is over that tile, so whole-board pixel
   equality is not claimed for this frame.
2. Clicking bottom-middle moves exactly that adjacent picture tile into the
   blank, leaving the blank at bottom-middle.
3. The size control reduces the puzzle to small; the arrangement is retained.
4. Clicking bottom-left in the small board moves the same tile back.
5. Returning to large reproduces the original board exactly: the RGB region
   `(53,353)` to exclusive `(297,597)` has SHA-256
   `b73a5d899263d05cc075ff847fa2f001dfe4dbb87471107ca88b92c8c2df1568`
   in both initial and round-trip screenshots. The intermediate moved board is
   `dedc412e441a6036e7153a34c812d45d7a55ddbd472e352ab07512e3275b30b2`.

This proves these native move/invalid-move/resize interactions only. Other
difficulties, complete-game behavior, restart persistence and the rest of the
gadget acceptance matrix are not covered by this small replay.
