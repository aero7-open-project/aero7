# Desktop Gadget Gallery — keyboard and palette defects

Local Beta 2 QA only. No commit, publication, package promotion or final ISO.
**Scoped pass:** installed gallery fixes and candidate 6 native single-monitor
drag/restart checks pass. Candidate 5 remains rejected. Broader gadget workflows,
account startup and next-build integration are still pending.

## Installed baseline

The disconnected `aero7-r10-offline` Wayland guest at 1920×1080 has
`aero7-gadgets 3.0.0-3`. Its installed `--self-test` succeeds and package-file
checks pass. A separate QA config/cache and private session bus were used under
`/mnt/a7-results/gadget-profile.zDkD5t`; the existing account's gadget layout was
not replaced. The QA profile starts with an empty `gadgets` array, as intended.
The companion README incorrectly claimed that clean profiles add Clock and
Weather; that documentation statement has been corrected locally.

Two real UI problems were observed:

1. With the QA profile's dark inherited palette, unselected gallery names are
   nearly invisible on the fixed light list background. The selected row is
   readable. [Baseline screenshot](gadget-gallery-logs/baseline-dark-labels.png).
   This is an isolated-profile palette check, not a claim that the account's
   existing Aero7 Light desktop changed theme.
2. Selecting Clock and pressing Return adds exactly one clock, but also opens
   the browser through the gallery's online button. The test profile's browser
   wrapper displayed its missing-backend message. The problem under test is
   the unintended website action, not that separate browser configuration.
   [Baseline screenshot](gadget-gallery-logs/baseline-enter-opens-browser.png)
   and [one-clock saved state](gadget-gallery-logs/baseline-after-enter-layout.json).

The existing gallery uses a fixed light list background without a corresponding
normal text color. Its Add context menu has the same incomplete color pairing,
and expanded details use a dark fixed foreground on an inherited background.
The online QPushButton also retains QDialog's automatic default-button behavior.
New tests exercise the actual gallery/manager with light and dark palettes,
context-menu contrast, and Return/keypad Enter without activating the website.
The website signal is disconnected before testing a broken baseline so the
automated regression cannot launch an external browser.

The controlled test build at `work/beta2-gadget-gallery.y2DAw2/baseline-build`
uses the preserved uncorrected gallery source. It waited for KWin compilation
to finish before using two jobs. The [baseline suite](gadget-gallery-logs/baseline-test.log)
reproduces four failures: dark list text, dark-palette context-menu text, Return
and keypad Enter activating the website. Its light-palette case passes.

The local correction pairs the fixed light list/menu surfaces with dark text,
uses inherited palette colors for details/link text, and removes default-button
behavior from the website action. No gadget artwork or icon resources change.
The [complete corrected build tests](gadget-gallery-logs/corrected-test.log)
pass all four CTest groups. The actual gallery suite passes seven Qt results,
including initialization/cleanup, in the
[detailed log](gadget-gallery-logs/corrected-gallery-details.log).
Normal package upgrade and corrected native replay remain pending; the selected
archive is still Gadgets 3 and does not contain these changes.

## Candidate package build

`work/beta2-gadgets4.ExdTih` builds `aero7-gadgets 3.0.0-4` from the canonical
Desktop companion, not the stale workcopy. The normal two-job `makepkg` build
completed at 23:49:31 CEST on 9 September with exit 0. All four CTest groups
pass inside the recipe's no-activation private bus; see the
[complete build log](gadget-gallery-logs/package4-build.log).

- Main archive: `aero7-gadgets-3.0.0-4-x86_64.pkg.tar.zst`, 349,540 bytes.
- Archive SHA-256: `f072ab2223767d0bfec506e5a785a2704a91cdc04be1467d326cf2475d741c16`.
- Installed host binary SHA-256 from archive: `0cf8eaf302d09c7f59e4dfd18b2db92c0af4f17171cd9d4e3a1f7c9ef3ab4948`.
- Source archive SHA-256: `67215c9dd48032d90ec6ee5b1f6fafc3f551c87e806ebee550a8d2d2364cef06`.
- Runtime dependencies remain unchanged. `dbus` is an explicit build/test
  dependency. The debug archive is not selected.

The log contains a `libfakeroot internal error: payload not recognized!`
diagnostic during tidying, despite successful completion. An archive comparison
therefore explicitly checks every member: both packages have the same 61 paths,
root ownership, and expected file modes; the host binary is 0755. The gallery
symlink's normal 0777 mode is not treated as a writable regular-file defect.
Only `.BUILDINFO`, `.MTREE`, `.PKGINFO` and the host binary differ in content.
All installed icons, gadget data, licenses, desktop entries, autostart and the
install hook remain byte-identical to release 3. This metadata check does not
replace a normal guest upgrade and runtime test, which remain pending.

The private QA host was stopped after its saved state was captured. The clock
disappeared and the original desktop session remained open. Further persistence,
removal, all-nine-gadget and network-provider checks are still required for
broader gadget claims.

## QA isolation follow-up

The original private bus used standard activation directories. Its log shows
extra desktop/document portal activation, and the full VM journal records the
existing document-portal unit exiting at the same time. Therefore the first
private-profile replay must not be described as having no session-service side
effects. The later normal reboot's audit is clean, but does not erase that
earlier finding.

The gallery regression and prepared guest launcher now use an explicit private
bus configuration without service directories or includes. A direct bus listing
shows only the daemon and the inspection client. Repeating the
[unmodified-source suite](gadget-gallery-logs/baseline-no-activation.log) still
reproduces the same four failures, and the
[corrected complete suite](gadget-gallery-logs/corrected-no-activation.log)
passes all four groups with activation disabled. No host compositor was started
by these checks. The revised guest launcher still needs its native replay with
the corrected packaged gallery.

## Installed release 4 replay, 10 September

The [normal offline upgrade](gadget-gallery-logs/package4-normal-upgrade.log)
completes with exit 0, all 57 installed paths present and the exact binary hash.
Only `aero7-gadgets 3.0.0-3 → 3.0.0-4` changes in the package list. QA profile
`gadget-profile.nOqsvc` uses the no-activation private bus and starts empty.
The original account's layout is not replaced.

- [Unselected names](gadget-gallery-logs/a7-gadgets4-gallery.png), the
  [Add menu](gadget-gallery-logs/a7-gadgets4-context.png) and
  [expanded details](gadget-gallery-logs/a7-gadgets4-details.png) are readable
  under the dark inherited QA palette.
- Return adds exactly one Clock; keypad Enter adds exactly one CPU Meter.
  No browser window or the former browser error appears. The retained
  [Return state](gadget-gallery-logs/package4-after-return.json) and
  [keypad state](gadget-gallery-logs/package4-after-keypad.json) confirm counts.
- Calendar is added once through its context menu. Stopping/restarting only
  the QA host restores the same three instance IDs, settings and positions;
  [restored desktop](gadget-gallery-logs/a7-gadgets4-restored.png).
- Close gadget removes only CPU Meter from the visible desktop and saved
  [layout](gadget-gallery-logs/package4-after-remove.json).

`kwin-actions-gallery4-stopped.EJTGtH` at 00:17:44 records the same boot/session
and active shell/KWin/Plasma units, no restarts and no failed units. The private
runtime logs only that no desktop portal is available on its deliberately
restricted bus; it does not activate a second portal. A later scheduled offline
update check appears as failed before shutdown; that is kept in the later
snapshot rather than presented as a clean update result.

## Further native drag defect and candidate 5

Layout restoration works, but pointer tracking does not. With the restored Clock
at `(1500,52)`, a native drag from `(1564,115)` to `(1300,115)` should preserve
the 64-pixel horizontal grab offset and end near `(1236,52)`. Instead it ends
at `(1408,52)`, visibly behind the pointer in the
[baseline capture](gadget-gallery-logs/a7-gadgets4-drag-baseline.png). No nearby
screen/gadget snapping target accounts for that difference.

The Wayland mouse handler adds each surface-local event coordinate to the
original press-time placement, even after moving the surface. It now uses the
current placement and removes the unused press-position member. X11/global
coordinate handling, snapping, artwork and data are unchanged.

A regression invokes the actual `GadgetWindow` mouse handlers with successive
surface-relative coordinates. A real LayerShellQt wrapper is attached to an
offscreen window via test friendship; this tests handler/state arithmetic, not
compositor acknowledgement timing. The
[baseline fails](gadget-gallery-logs/drag-baseline-test.log) on its second move
(`380,200` instead of `360,200`), while the
[corrected full gallery suite](gadget-gallery-logs/drag-corrected-test.log) passes
eight Qt results, including initialization/cleanup. Native revalidation remains
mandatory.

Candidate `aero7-gadgets 3.0.0-5` builds normally at 00:24:18 CEST, exit 0, with
all four CTest groups passing in the [build log](gadget-gallery-logs/package5-build.log).
The main archive is 349,283 bytes, SHA-256
`067edcb41c6c526dfb71ec65b37393e0a54a182db62499dad9b05e74d859576b`;
host binary SHA-256 `a95ccbbd6f6635e23ce3cbb6f15ea7dee35a305d662aa307aa79a002d3fd7d6f`.
Source archive SHA-256 `332eb05b7ba11f9615d7d92bd44d7449ef30d1d339732e204b8dfc3c609b89e3`.
All 61 archive paths, root ownership and file modes pass. Only package metadata
and the executable differ from release 4; installed icons/data/desktop files,
licenses and install hook are byte-identical. No final ISO or package promotion.

## Candidate 5 native drag rejection, 10 September

The [normal release 5 upgrade](gadget-gallery-logs/package5-normal-upgrade.log)
passes; only Gadgets 4 → 5 changes. New isolated profile `gadget-profile.8hifUb`
starts empty and Return adds exactly one Clock with no browser window.
However, dragging from `(1818,75)` to `(1500,115)` moves that Clock from
`(1754,22)` to **`(198,218)`**, rather than the expected `(1436,62)`.
The [native screenshot](gadget-gallery-logs/package5-drag-failed.png) and
[saved layout](gadget-gallery-logs/package5-drag-failed.json) preserve this failure.
**Candidate 5 is rejected for next-build selection.** The controlled arithmetic
test did not model asynchronous surface movement and was insufficient.

A further local revision keeps the input surface stationary during its pointer
grab and moves an input-transparent preview, committing the real gadget position
on release. This avoids interpreting queued surface-local events as evidence
that the compositor has applied the latest requested margins. The revised
regression checks a fixed input surface, moving preview and final release-only
coordinate. This revision still requires a build and installed native replay;
do not describe gadget dragging as fixed yet. No icons or artwork were changed.

## Candidate 6 installed drag and persistence replay

The stationary-input revision builds as `aero7-gadgets 3.0.0-6` at 00:41:36 CEST,
exit 0, with [all four CTest groups passing](gadget-gallery-logs/package6-build.log).
The archive is 351,429 bytes, SHA-256
`06af9972be7255b7150180a2e7547229a809c5376ed9a39b4c2990f4b8d00e89`;
binary SHA-256 `d1b1859c441d19e2a7c05730a70a48222c1c25ce8efc8e261d4e68c14a819e7b`.
Source archive SHA-256 `f989b67c9d25b6bc5ddbbb2bf49b45b05c2b010d6acb6b648557585b928e5811`.
Archive comparison verifies the same 61 paths, root ownership and modes; only
metadata and the executable differ from release 5. Icons/data/hooks are unchanged.

[Normal offline upgrade](gadget-gallery-logs/package6-normal-upgrade.log) exits 0,
verifying all 57 installed paths and the exact binary. Isolated native profile
`gadget-profile.cFLasV` starts empty. Return adds one Clock, keypad Enter later
adds one CPU Meter, with no browser window or error.

| Native gesture | Expected final position | Observed |
| --- | --- | --- |
| Clock `(1818,75)` → `(1500,115)` | `(1436,62)` | Exact match |
| Held Clock `(1500,115)` → `(1300,115)` | `(1236,62)` | Exact match on release |
| Reverse diagonal `(1300,115)` → `(1650,255)` | `(1586,202)` | Exact match |
| Clock drag handle `(1731,292)` → `(1531,432)` | `(1386,342)` | Exact match |
| CPU body `(1818,60)` → `(1720,450)` | `(1656,412)` | Exact match |

The [first drag](gadget-gallery-logs/a7-gadgets6-drag1.png) and
[reverse drag](gadget-gallery-logs/a7-gadgets6-drag3.png) preserve the grab offset.
While the mouse button is held, the [preview](gadget-gallery-logs/a7-gadgets6-held.png)
moves and the original is transparent; saved layout stays at `(1436,62)` until
release. The release writes `(1236,62)`. No second visible gadget remains.

Stopping and restarting only the private QA host restores both gadgets with the
same IDs, settings and exact positions. The saved JSON is byte-identical before
and after restart: [retained layout](gadget-gallery-logs/package6-before-restart.json),
[native restored desktop](gadget-gallery-logs/a7-gadgets6-restored.png).
Clicking CPU Meter's Close control afterwards removes only that gadget;
the [remaining layout](gadget-gallery-logs/package6-after-remove.json) retains
Clock's instance and position.
The [session audit](gadget-gallery-logs/package6-session-audit.log) retains the
same boot/session, active shell/KWin/Plasma units and zero restarts. Its sole
failed user unit is the disconnected update checker; system failures are zero.
The private runtime logs only the expected unavailable-portal message on its
no-activation bus. No host compositor or package was changed.

This closes the reproduced single-monitor pointer-tracking failure for release 6,
not all gadget acceptance. Cross-monitor/scaled dragging, the normal account's
next-login startup, all nine gadget workflows and package integration remain
separate checks. No final ISO, commit, push or publication.
