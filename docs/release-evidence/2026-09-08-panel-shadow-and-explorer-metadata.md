# Theme 53 and Explorer 54 — panel contract and metadata

Follow-up: [Theme 54](2026-09-08-detached-menu-launch.md) resolves the reproduced
menu-launch defect below and passes actual menu/reboot replay. This report
preserves the earlier observations rather than relabeling them as passes.

Status: both local candidate packages built and upgraded normally in the
disconnected r10 Wayland guest. Theme 53 passed a normal reboot/cold-login
audit. Explorer 54 passed all 59 installed common-dialog cases. These are
component checks, not final-image acceptance or publication approval.

## Panel correction and evidence

Plasma Workspace PanelView reads four shadow-margin properties and connects
their notify signals. The Aero7 Panel.qml did not provide them. The correction
derives each margin from the actual floating background rectangle, matching
the PanelView contract rather than supplying dummy zeros or filtering warnings.
It changes no icons, colors, taskbar defaults or edit-mode policy.

The regression evaluates the four bindings extracted from the actual source
Panel.qml. Five geometry cases cover docked, horizontal/vertical floating,
fractional and extending-background rectangles. It verifies all four notify
signals and updates after geometry changes. All five fail on the old source;
the corrected run reports seven passes including setup/cleanup, no failures or
skips. An intermediate test had incorrect expected arithmetic; its corrected
expectations are retained explicitly, not attributed to a product defect.
This isolated binding test does not instantiate the full desktop panel.

The fresh Theme package build completed at 22:17:40 CEST. CTest reports 20
successful statuses: 11 executed tests and nine ECM metadata checks that exit
early with “Not installed yet, skipping”. The separate ten SDDM runtime tests
passed. Do not describe the nine skipped checks as validated metadata.

- Package: `aerothemeplasma-desktop-git` `6.7.0_742.r9c2d850-53`.
- Size: 5,152,153 bytes.
- Archive SHA-256: `3ece79b3456d891a3fcaabafcf3aaec02310cec81c09f53e60b09e8f4f888b59`.
- Added patch SHA-256: `af977f13d23d513d589919ec15b77f719e49aceed84afd5bbaf72f8ac02f4381`.
- Installed Panel.qml SHA-256: `e0cf5bbf19963673d6de858a36765203f18f9d9881c7c370bf6f965f2551236a`.
- Source revision remains `9c2d850f0907cd7d33c81e8a3fcc00abae3abb9b` with the
  retained package patches; the Shell pin remains unchanged.

Normal `pacman -U` completed at 22:19:12 with all 1,147 package files present.
A normal reboot and password login produced boot ID
`fda9a4d1-0e64-43bb-becf-39b2cb926567`, different from the previous boot.
The 22:28:05 audit verifies the exact installed Panel.qml, active shell and
snipping helper, zero shell-service restarts, and absence of the four missing
shadow signals and the previously reproduced duplicate portal-registration
warning. Both failed-unit lists were empty at that instant. Other journal
warnings, including helper identities and the disabled KWallet portal, remain;
empty failed-unit lists are not a warning-free-session claim.

The actual 1920×1080 desktop, Start and taskbar context menu render after login.
The test desktop still includes its requested diagnostic-log folder. No clean
final-install desktop-icon claim is made. The broader taskbar actions are not
all accepted: the new launch-path reproduction below remains open.

## Explorer metadata correction and installed tests

Explorer 53's direct metadata check found a missing homepage URL. Explorer 54
adds the maintained project's homepage to its AppStream metadata and a required
direct `appstreamcli validate --no-net` test. `appstream` is a check dependency.
The new check validates source metadata even when ECM's install-manifest check
returns early. It does not invent developer or content-rating declarations.

The fresh build completed at 22:26:51 CEST. All 21 CTest statuses succeeded:
20 executed tests, including the new metadata validator, plus one skipped ECM
check. Direct validation succeeds with two informational findings (missing
content rating and developer information) and two pedantic findings retained
in the full output; it is not described as having no advisory messages.

- Package: `aero7-file-explorer` `25.12.3-54`.
- Size: 8,291,390 bytes.
- Archive SHA-256: `c84d91f144a99631f4459669fb2eef984b5ebb035b2b2682f9a16de3e5cdb597`.
- Source archive SHA-256: `5314daedf6058c49eac4f4961e5c481fd090a1984ea6041a39622a4344d5f816`.
- Metadata SHA-256: `ddb40ed1244700d26808e11e55ac11ca9e48cc6b3e0fd1a6ecfa82375421f9f5`.
- Installed common-dialog library SHA-256: `17457ea55f0716537bde7c2652d88e26241c85e67a179848e2068d78a6de620a`.

Normal offline upgrade at 22:28:50 preserved dependency checking and verified
all 665 installed files plus the exact validated metadata. The later Wayland
test resolves the library from `/usr/lib`, not a build-tree override, and passes
all 59 common-dialog cases with no failures or skips. Explorer 53's actual
keyboard-only Paint Save As/Open result remains historical evidence; this
entry does not relabel it as a new Explorer 54 GUI replay or cold reboot.
Both host package builds bypass only makepkg's host dependency precheck;
neither VM transaction bypasses dependencies.

## Newly reproduced taskbar launch issue — still open

Selecting taskbar Properties twice by mouse, and once using End then Enter,
closes the menu without opening Control Panel. Directly running the existing
`aero7-shell-action taskbar-properties` helper with output redirected to a file
opens the correct Taskbar and Start Menu page. No settings were applied.

A separate Qt Quick probe using the same Plasma5Support executable data engine
reproduces the difference: the plain helper reports exit code 0 but no Control
Panel window remains. Adding file redirection to that same command opens the
page, with its VDPAU diagnostic preserved in the file. The saved probe is the
redirected variant; the baseline used the same command without the redirection.
This implicates the detached child's inherited output-pipe lifetime. It does
not yet prove a specific terminating signal or constitute a launcher fix.
Do not suppress the diagnostic or count helper exit 0 as application acceptance.

The next correction must keep launched applications alive after the menu helper
finishes and retain useful diagnostics. Repeat the actual mouse/keyboard menu
actions after a normally installed correction. Taskbar Properties, other helper
launches and new-package screenshot replay remain open acceptance work.

## Retained evidence and release boundary

[Build logs, exact recipes, tests, guarded VM scripts, upgrade audits and GUI
captures](panel53-metadata54-logs/) preserve these results. The frozen r10 ISOs
are unchanged and contain neither new package. No final ISO was built, no new
disk/ISO cleanup occurred, and nothing was committed, pushed or published.
Online update recovery, existing-UFW regression, helper identities/UAC, KWallet
policy, physical/multi-monitor/storage cases and the broader final-image gates
remain open. The disconnected guest's earlier update-check failure still does
not prove a broken online updater or justify reporting unknown updates as none.
