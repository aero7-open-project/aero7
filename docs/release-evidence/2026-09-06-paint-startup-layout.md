# Paint startup layout and colour swatch regressions

6 September 2026. Local work only; no release approval or publication.

## Reproduced defects and corrections

The fresh r9 online Paint screenshot (`online/39-pasted-image.png`) showed
the ribbon together with the legacy menu, main toolbar and colour dock.
Startup now calls the existing mode-change slot after XMLGUI restores its saved
layout, matching the mode selected by the user. The ribbon's otherwise blank
application button now has a translated File label and retains its original menu.

During installed r5 validation, selecting red in the palette produced a red
stroke while the foreground swatch remained black. SARibbon's pixmap cache did
not distinguish different icon identities. Its cache now includes the icon key
and device-pixel ratio, in addition to size and state. No icon assets were created
or replaced. DPI handling is covered by the implementation, not a multi-monitor
acceptance claim.

## Source and package evidence

Evidence directory: `work/beta2-paint-layout.BtokV4/`.

- `layout-before.log`: real application observation failed because menu and
  toolbar remained visible in ribbon mode. The corrected default/classic fresh
  launch, reopening and both mode transitions pass.
- `file-button-before.log`: adding the File-menu assertion failed before the
  label change; `file-button-after.log` passes all four scenarios afterward.
- `colour-cache-before.log`: direct black-to-red icon update rendered stale
  pixels. `colour-cache-after.log` passes black/red/green/blue changes and cache
  reuse without pointer movement or QAction events.
- `paint-r6-package.log`: successful makepkg build, including the existing
  normal-close lifetime test, colour-cache test and four startup-layout cases.
  This used `--noextract --nodeps` and the prepared source/build trees; it is not
  a clean signed-builder result. No host packages were installed.
- All packaging patches applied to fresh exports of their exact pinned Git
  commits in `work/beta2-patch-check.ruwDDP/`. The resulting two Paint translation
  units and SARibbon toolbutton translation unit match the prepared build inputs.
  This is a forward patch/content check, not a fresh compilation.
- Canonical `.SRCINFO` matches `makepkg --printsrcinfo`.

Package: `aero7-kolourpaint-25.12.3-6-x86_64.pkg.tar.zst`, 6,614,751 bytes.
SHA-256: `edf360265dd709ae7500e35dd7e8a1c5ab8ed573c5140bac77c77376ef3fd2ce`.
Selected in the local ISO manifest only. r3/r4/r5 archives are retained.

## Modified offline VM checks

Guest evidence root: `/home/admin/VMs/aero7-beta2-r9-xTfYQR/`.
The original fresh/reboot r9 evidence remains unchanged: these are subsequent
local package upgrades, not proof that the existing ISO includes the fixes.

The offline guest was upgraded r3 → r5 → r6 with normal `pacman -U`, without
dependency bypass or forced overwrite. Both upgrade logs report 709 files and
zero altered files. Before/after package inventories change only Paint.
Logs: `offline/results/paint5-install.log`, `paint6-install.log`.
The r6 helper initially had an ineffective negated-command errexit guard;
Paint was independently observed closed before the actual upgrade. The helper
was corrected after completion and passes ShellCheck. No running script was edited.

- `offline/59-paint5-installed.png`: normal desktop settings, visible tool icons,
  single ribbon and visible File label. Earlier isolated-config previews had
  missing icons; they were not accepted as package evidence.
- `60-paint5-file-menu.png`: original populated File menu opens.
- `63-paint5-saved.png`, `64-paint5-reopened.png`: black and red strokes saved
  as PNG and retained after normal close/reopen. Exported file is
  `offline/results/paint5-lines.png`, 400×300 RGBA, SHA-256
  `5eef2db4c425058e18323d5e1ff9a4823d26b35b7a0e162a234e10eca6a92abb`.
- `68-paint6-red-swatch.png`: installed r6 displays the red swatch and matching
  red stroke without hovering over the swatch. This reproduces the same gesture
  that left r5's swatch black.
- `69-paint6-saved.png`, `70-paint6-reopened.png`: switching again to green
  updates the swatch correctly; the red/green drawing survives PNG save and
  normal close/reopen in the installed r6 package.

After selecting r6 locally, `scripts/check.sh` completed with `Static checks
passed` (`work/beta2-paint-layout.BtokV4/selected-r6-checks.log`). Existing QML
lint warnings remain recorded. The pinned Shell worktree is still clean.

The first Colours-tab capture briefly showed clipped labels; later settled
captures reflowed them correctly. Startup/tab layout timing needs further review.
Common save dialogs still expose KDE-style controls and raw volume labels:
`62-paint5-save-dialog.png`. Do not advertise full Windows common-dialog parity.
Final-image inclusion and full application/failure/scaling checks remain open.
