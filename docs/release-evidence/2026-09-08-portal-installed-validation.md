# Portal and Spectacle candidates — installed validation

Status: partial. Control Panel 51, Spectacle 3 and Qt 6.11.2-3.1 passed normal
offline upgrades and post-reboot baselines. The installed Qt registration
comparison and real region/clipboard-lifetime replay passed. Notification body
and thumbnail activation and actual Ctrl+V into Paint also passed. A separate
initial filename-focus defect was reproduced and fixed in Explorer 53, with
actual installed keyboard-only Save As/Open passing. Other keyboard and broader
workflow checks remain pending. No final media or signed
repository has changed; nothing was committed or published.

## Normal package upgrade and reboot

The existing disconnected r10 VM resumed after the Qt builder shut down
normally. QEMU PID 562706 uses the existing disk and firmware, verified frozen
ISO, 1920×1080 display and no NIC. No installed state was replaced with a fresh
test image.

At 21:12:53 CEST, the guarded script installed these two exact archives through
normal `pacman -U`, without dependency bypasses or network access:

- Control Panel 0.1.0-51, package SHA-256
  `820c1c5105d98fd4c009e1e2608b8344972fb45f66c2da9a16ea7585fa706580`.
- Spectacle 1:6.7.4-3, package SHA-256
  `d918e0041351a7c1b9643e15e8eee7e05547e6062b80b4bfd95cc29fb206797b`.

Both executable hashes matched their built candidates; package checks found
no missing files (Control Panel 74, Spectacle 308). Upgrade status was 0.
Pacman's existing missing sync-database warnings for core/extra/aero7 are retained;
this local-file installation does not establish online repository readiness.

Normal reboot/password login changed boot ID from
`06b9dac1-4054-4f9f-92de-f0667b20135d` to
`2a77e9ae-fe1e-43e4-81ef-4b1eb7202038`.
The 21:16:10 audit `cp51-spectacle3-audit.igN6vq` passed. It verifies versions,
executable hashes, installed files, identical hidden Action Center application
and autostart entries, one actual Action Center service and active shell/snipping
services. No system or user services were listed failed at audit time.

Actual Action Center unit:
`app-aero7\x2daction\x2dcenter@autostart.service`, PID 1013, invocation
`b0e4f204bcff486f90df9baadb089bc3`. No service name was guessed for the check.
There were no Spectacle focus-property warnings in this baseline journal, but
that is not a capture/editor test: the new full application still needs launching.

## Warnings remain visible, not waived

This baseline still uses Qt 6.11.2-3. Action Center and Snipping Tool, along
with other applications, still log duplicate host-portal registrations. That
is the separate Qt lifecycle defect targeted by the completed Qt candidate.

The journal also records missing app info for `org.kde.ksmserver`,
`org.kde.gmenudbusmenuproxy`, `org.kde.ActivityManager`, `org.kde.xembedsniproxy`
and `org.kde.org_kde_powerdevil`. UAC's helper has an unable-to-open-proc-root
warning. A KWallet portal activation exits with status 255; it is not retained
as a failed unit at the later snapshot. These are not treated as solved just
because the package/service baseline passed. The disabled-wallet policy remains
unchanged pending the user's choice. PowerDevil also reports that this virtual
hardware does not support charging thresholds; no physical battery claim is made.
Plasma also logs four missing Panel shadow-margin signals (left/top/right/bottom).
All four occur in the baseline journal before the Qt upgrade as well as after;
they are not evidence of a new Qt regression, but still need investigation.

Before/after inventories, upgrade and reboot audit logs:
[cp51-spectacle3-installed-logs](cp51-spectacle3-installed-logs/).
Screenshots 323–329 are preserved in the VM results directory.

## Installed Qt comparison

The same portal-start trace first reproduced two Snipping Tool registrations
on Qt 6.11.2-3: `snipping-portal-start.bU8yRy`, PID 2254, sender `:1.140`,
serials 34 and 38, both with `org.aero7.snippingtool`. The helper journal records
the corresponding duplicate-registration error. Bus-owner data ties that sender
to the actual installed helper. The trace restored normal services successfully.

At 21:18:29 CEST, the guarded normal upgrade installed Qt 6.11.2-3.1 from the
verified archive. All 5,102 installed files were present and QtGui matched
`e8b4af6296f3aa591c269ad9ed4dda33a1e0b7f7eb59b1f81a55011c9887e4cf`.
No dependency bypass or online transaction was used.

Normal reboot/password login produced boot ID
`d3be2a06-2905-424b-af57-9b3aeebd985a`. The 21:22:03 audit
`qt-portal-audit.j6yyG4` passed: correct installed version/hash, the helper maps
the non-deleted QtGui library, normal shell/helper/portal are active, and no
duplicate-registration messages appear in the complete cold-login user journal.
No system/user services were listed failed at audit time. Action Center's
companion audit `cp51-spectacle3-audit.DfuBIT` also passed; its startup journal
has no portal warning. The separate missing-helper identities, UAC proc-root
and KWallet messages remain, as described above.

The identical restart trace on the candidate (`snipping-portal-start.3wzpXI`)
shows exactly one Snipping Tool registration: PID 2136, sender `:1.129`, serial
34, correct app ID. Its invocation journal has no entries. Action Center PID
1003, sender `:1.47`, registers once as `aero7-action-center` when the portal
restarts. Other already-running applications also re-register rather than
retaining the old portal's registration state. Both normal services were
restored with status 0. These two bounded traces are not exhaustive race proof.

## Actual capture and clipboard lifetime after upgrade

The installed-helper replay `snipping-clipboard-installed52.0QhXmh` uses
unchanged Theme 52 with Spectacle 3 and the new Qt. Meta+Shift+S opened the
rectangular selector. Releasing the selected rectangle closed it and returned
to the desktop, without opening the editor. One PNG was saved under the user's
Pictures/Screenshots directory:
`Screenshot 2026-09-08 21.24.15.550-20c969.png`.

- PNG SHA-256: `d040a241b845fc6e63d4dc6bd466771d0194d83670e54dbe550fb2b2e5cac893`.
- Decoded size: 361×241.
- Decoded pixel SHA-256: `9b9808d2c7ebc5c7b38e02f75de8f4983e2a07cc6dfb3f775594def35d366c75`.

The actual clipboard image matches those pixels before producer exit, after
normal producer stop and after normal-service restoration. Restoration status
is 0 and the package executable hashes remain unchanged. Global Klipper
preferences were not changed. This replay did not newly verify notification
display/clicking or a real Ctrl+V in Paint. The later desktop screenshot has no
notification visible, so it cannot establish whether a popup appeared earlier.
Keep those gates open.

The post-capture audit `cp51-spectacle3-audit.coRF71` also passed, retaining the
full user journal. No focusPolicy override, ReferenceError or TypeError appears
in that journal after the real selector launch. This is bounded log evidence,
not proof of correct keyboard navigation through every editor control.

## Notification activation and actual Paint paste

On the same disconnected VM and boot, rectangular capture again saved directly
without a Spectacle editor. The visible notification states that the screenshot
was saved and copied to the clipboard. Both routes were exercised:

- Thumbnail: trace `qt-notification-observer.lZEqLJ` records notification ID 3,
  `ActionInvoked` with action `default`. Gwenview subsequently displayed
  `Screenshot 2026-09-08 21.32.02.179-3d8094.png` (421×301).
- Body text: trace `qt-notification-observer.lvMVy0` records ID 4, action
  `default`, at epoch 1788896494.349404. The visible notification was hovered
  to prevent expiry, then clicked at screen position 1750,855. The screenshot
  taken three seconds later shows Gwenview displaying the correct
  `Screenshot 2026-09-08 21.41.02.120-663252.png` (411×261).

The actual default PNG handler is `org.kde.gwenview.desktop`, confirmed by
`xdg-mime`; the process inventory includes both exact saved paths. This does
not newly establish Aero7 branding of that viewer. An earlier untraced click
was inconclusive because expiry/timing was not captured, and is not counted
as either a successful action or a confirmed defect. The 120-second observer
timeout is the expected collection boundary, not a pass criterion.

Paint 25.12.3-9 was launched normally. Actual Ctrl+V pasted the screenshot,
then Ctrl+S and the native Aero7 Save dialog wrote `qt-paint-pasted.png` in the
QA results share. All 411×261 screenshot pixels match the saved Paint image's
top-left region exactly (decoded 8-bit RGBA SHA-256
`7c8017d610754786e92a76bcf33a5906cb6125890a7ed611ecd150596fbb72fe`).
Paint retains the larger initial canvas height: its 411×300 output has 39
remaining rows verified opaque white. This is not a scaled or damaged paste.
The screenshot file hash is
`32bfe2edc2eddc96d6963644bda3454e3f46ca0638a34ee2f33a109eb1b0863a`;
the Paint output file hash is
`e489d11c36c7b4a471f7f23ee993f249446a86370881b0378dfed8ae94d7b494`.

The host Python environment lacks Pillow; that attempted decoder did not run.
The retained ImageMagick verification completed with explicit size, pixel-hash
and blank-canvas assertions. `wl-paste` is absent in the guest, so that audit
does not claim a newly exported clipboard PNG; actual application paste is
the evidence here, alongside the earlier dedicated Qt clipboard-lifetime test.

Save As initially ignored typing until the filename field was clicked. A
second Ctrl+Shift+S replay reproduced this without saving another file. Source
tests identify the initial focus as the breadcrumb QScrollArea, not the filename.
Five regression cases fail before the fix and pass after setting the initial
focus once in the dialog constructor; all 59 common-dialog checks pass. The
[Explorer 53 package build and installed replay](2026-09-08-dialog-initial-focus.md)
subsequently passed normal upgrade and actual keyboard-only Save As/Open.
The new Paint process maps the verified non-deleted candidate library. This
does not establish all keyboard workflows or a new final-image reboot test.

Traces, screenshots and pixel verification:
[notification-paint-logs](notification-paint-logs/).

## Panel warning investigation, not yet fixed

The local Plasma 6.7.4 `shell/panelview.cpp` connects four shadow-margin change
signals and reads those values when selecting borders and updating shadows.
The AeroThemePlasma `contents/views/Panel.qml` exposes none of those properties.
The installed stock Plasma panel instead binds them to the actual floating
panel rectangle (negative top/left offset and remaining right/bottom space).
This identifies a concrete shell-view contract mismatch. No warnings were
filtered, no zero-valued compatibility signals were added, and the Aero panel
has not yet been changed or visually retested for this issue.

The 21:53:31 read-only installed identity inventory (`helper-identities.mbRB9z`)
confirms the five missing `/usr/share/applications/<ID>.desktop` entries rather
than assuming that all portal messages have the same cause. GMenu/XEmbed and
PowerDevil have separately named autostart entries. The stock PolicyKit desktop
entry *does* exist and is owned by `polkit-kde-agent` 6.7.4-1, while Aero7 UAC
has its own differently named application entry. UAC's retained error is an
inability to open `/proc/844/root`, not a missing-file message. No process
security, authentication settings, desktop entries or services were changed by
the inventory. In particular, do not weaken process protections merely to
eliminate that warning. The inventory is retained with the notification logs.

Qt upgrade, cold-login, bus trace and clipboard records are in
[qt-portal-package-logs](qt-portal-package-logs/); Control Panel/Spectacle records
are in [cp51-spectacle3-installed-logs](cp51-spectacle3-installed-logs/).
Screenshots 330–334 remain in the VM results directory.

Next: native dialogs, notification/viewer, real application paste, keyboard,
cancellation and further service recovery on this exact package combination.
Missing helper identities need their own investigation, not suppression of
portal logging. Final online and offline image rebuilds/acceptance remain open.
