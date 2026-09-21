# Offline optional-feature recovery and screenshot acceptance

8 September 2026. **QA evidence, not publication approval.**

The existing r10 offline guest remained at 1920×1080, on Wayland, with no
network adapter. It had already been normally upgraded to Programs Center
`0.1.0.r12.g0405a2e-3` and Paint `25.12.3-9`. Control Panel remains
`0.1.0-50`, Desktop `0.2.0-29`, and Spectacle `1:6.7.4-2`. These are
component-upgraded guest results, not fresh-image acceptance of new packages.

## Optional Programs Center: cancellation, removal and recovery

1. Closed Programs Center normally, then recorded the complete package list
   and SHA-256 of the existing `~/.config/Aero7/ProgramsCenter.conf`.
2. Requested removal, confirmed the action, then clicked Cancel in the actual
   User Account Control password dialog. The UI explicitly reported that
   authorization was cancelled and no changes were made. The complete package
   list and existing configuration hash matched baseline exactly. The user
   transaction log recorded `authorization-cancelled` at 12:18:09 UTC.
3. Requested removal again and authenticated successfully. The UI changed to
   Not installed; the transaction completed at 12:20:11 UTC. The package list
   lost only Programs Center, and the existing configuration remained intact.
4. Backed up the original bundled package and its checksum in the **test VM**,
   compared both backup copies, and substituted a deliberately invalid payload
   under the expected bundle filename. The checksum file retained the expected
   hash of the valid release-3 candidate, so validation had to reject it.
5. Requested installation through the actual feature UI and authenticated.
   The helper rejected the bundle with an integrity-check error at 12:22:48 UTC.
   The error dialog offered Open Optional Features, Try Again and Cancel.
   Its technical log retained both expected and actual hashes. The complete
   package list matched the post-removal list and configuration was unchanged.
6. Left that same error dialog open, replaced the QA payload with the verified
   release-3 archive, and clicked **Try Again**. Installation completed at
   12:24:56 UTC without restarting the feature window. The recent authorization
   was reused; this replay did not display a second password prompt. The helper
   verified installation and the UI returned to Installed.
7. The complete package list returned byte-for-byte to this test's baseline.
   Programs Center reported 49 package files with zero missing; no failed
   system units were listed. The original configuration hash was unchanged.
8. Restored the VM's original release-2 bundle and checksum and compared both
   against the backups. The original archive hash is
   `6017abb575ff4551124e6e9d4a2bc5c34e1367714f6a022f14382d602e9c3381`.
   The installed program remains release 3. No damaged fixture remains selected
   in the optional-package cache. Backup copies are retained for QA recovery.

All 14 existing feature-helper source tests also passed. They include simulated
package identity, checksum, transaction, service, dependency and lock failures;
those source fixtures are not claimed as additional full graphical VM tests.

Evidence: `r10-recovery-logs/feature-recovery-*.log`, package-list snapshots,
configuration hash snapshots and transaction JSONL files;
`original-bundle-restored.log`; screenshots `65-auth-cancelled.png`,
`67-removed.png`, `72-bundle-integrity-failure.png` and
`76-try-again-auth.png` (despite its capture name, the last image shows the
completed retry, not an authentication prompt).

This verifies retention of the existing Programs Center configuration, not
every possible user's data or every optional component. No production cache,
ISO profile, firewall or host package configuration was changed.

## Offline screenshot workflow

- Actual Meta+Shift+S opened rectangular selection. Selecting and releasing
  closed the overlay without opening a Spectacle editor/main window.
- The screenshot was automatically saved under the user's XDG Pictures path
  plus `Screenshots`: `/home/aero7test/Pictures/Screenshots`.
- Actual Ctrl+V into Paint pasted image pixels, not a filename. The selected
  image was 321×241, smaller than Paint's default 400×300 canvas. Paint's
  existing Set as Image/Crop shortcut removed that extra blank canvas; the
  native PNG Save dialog then saved `offline-pasted.png`. ImageMagick
  `compare -metric AE` returned `0 (0)` and exit 0 against the original:
  no differing pixels. This crop is a verification step, not an extra step
  required by the screenshot shortcut.
- A repeat captured the actual Plasma **Screenshot saved** notification one
  second after selection, then clicked its text body. The default viewer
  opened the matching screenshot filename. The first untimed screen captures
  missed the transient notification and are not used as notification evidence.
- Both captures have distinct filenames, dimensions 321×241, and SHA-256
  `f621aa576b6e6c24d876e13797bec3d122cef998240cabcc24c83df6d934c925`.
- A further shortcut displayed the selector; Escape after confirmed readiness
  closed it. Before/after audits retained the same two filenames and hashes,
  and no Spectacle process remained. The normal Snipping Tool daemon remained
  running. This does not resolve the separately recorded early-Escape timing
  limitation before the selector is ready.

Evidence: the copied `r10-recovery-logs/screenshot-offline-*.log` audits,
`84-offline-notification.png`, `85-offline-notification-viewer.png`,
`80-offline-paint-paste.png`, `83-offline-pasted-saved.png`,
`86-offline-cancel-overlay.png` and `87-offline-cancel-closed.png`.
The original PNG and pasted PNG are retained for pixel comparison.

## Still pending

Full screenshot failure notification/Try Again replay on r10, early input
timing, broader application behavior, update preference/recovery tests and
the rest of the release acceptance matrix remain open. Paint's Image ribbon
and shared-dialog presentation are not certified by a successful save:
the captured dialog still displays a raw Linux library path. Final media must
be deliberately rebuilt with verified candidate packages and retested.
Nothing was committed, pushed or published during this pass.
