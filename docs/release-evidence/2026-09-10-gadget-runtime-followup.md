# Gadgets: normal startup, integration and further runtime corrections

10 September 2026. Local pre-release work only: no final ISO, commit, push or
publication. This report extends the [gallery/drag pass](2026-09-09-gadget-gallery.md).

## Verified startup and package integration

The next-build manifest now selects Gadgets 3.0.0-6 and KWin 6.7.4-7.1, after
their scoped installed checks. There are 18 selected archives, 16 required and
two optional. Programs Center Beta and Credential Vault remain optional/off by
default; neither was added to the required transaction. The Shell pin is unchanged.
The [complete checker](gadget-runtime-followup-logs/integration-check.log) passes
all 149 Python tests, package hashes/ownership, versioned dependencies, syntax,
icon provenance, theme repeat setup and ShellCheck. This is input integration,
not an ISO build or repository promotion.

Manifest SHA-256: `c9218383adb652bd8e4ab76e816c2a895decfd6b3435c9f6e87fc45a6e0f4cfe`.
Required list SHA-256: `8a64da0370b18ff398e276a6fcf642c7afac3fd57e194d5e5c93643312e896e8`.
Optional list remains `3ee8b94ffd671697ec11410d4e3baa4f890b4339b9414798e2e864645d2ffb71`.

Normal Start-menu logout reaches SDDM; normal password login starts session 5
on boot `dcf96047-1c04-4efa-8bbd-5317c1fe084b`. The
[00:52:44 startup audit](gadget-runtime-followup-logs/login6-audit.log) verifies
the session-bus service owner is the automatically started Gadgets process 7800,
whose running executable has release 6's exact hash. The autostart unit is
active, using the normal account environment rather than a QA config override.
The account layout remains empty. Shell/KWin/Plasma units are active with zero
restarts; system/user failed-unit lists are empty at that snapshot.

Opening the gallery through the normal launcher shows its
[normal light theme](gadget-runtime-followup-logs/a7-gadgets6-normal-gallery.png).
No manual gadget-host startup preceded the startup audit.

## Further reproduced defects

An independent empty profile `gadget-profile.kL1jRy` adds all eight first-page
gadgets via Return, then Media Center from page 2. All nine distinct IDs are in
the [saved layout](gadget-runtime-followup-logs/all9-baseline-layout.json).
They render on the [native desktop](gadget-runtime-followup-logs/a7-gadgets6-all9.png);
the ninth wraps into another column rather than covering the taskbar. This is
an add/render check, not proof that every provider and control works.

Three defects are confirmed:

1. Gallery thumbnails draw the gadget directly into 64×64 pixels, leaving
   fixed-size fonts unscaled and distorting non-square gadgets. Calendar's day
   and month overlap; other previews also clip. Four
   [baseline image regressions fail](gadget-runtime-followup-logs/preview-scale-baseline.log).
2. Offline Weather displays 0° and a sunny symbol despite an unavailable error.
   Both [waiting/offline regressions fail](gadget-runtime-followup-logs/weather-unavailable-baseline.log).
   Currency and Feed Headlines correctly show unavailable states after their
   requests fail; no successful network/provider result is claimed.
3. Calendar saves Sunday as `firstDay: 7`, but reopening Options shows Monday
   and accepting would replace it with 1. The
   [native reopened dialog](gadget-runtime-followup-logs/a7-calendar-sunday-reset.png),
   [saved Sunday layout](gadget-runtime-followup-logs/sunday-before-upgrade.json)
   and [regression failure](gadget-runtime-followup-logs/calendar-options-baseline.log)
   agree. Cancel preserves Sunday for the corrected replay.

## Installed corrections and updated selection

Previews now render the existing gadget at native size and scale the whole image
with its aspect ratio preserved. No replacement artwork or icon assets are made.
Weather without a timestamped, finite reading and valid condition code shows
`--` plus Updating/Weather unavailable, not an invented temperature or symbol.
An actual zero-degree reading remains displayable. The initial currency rate
is no longer the gallery's sample rate; sample data is assigned in the preview.
Calendar Options explicitly converts the saved numeric week-start to its label.

The expanded real-widget/painter suite passes 16 Qt results including setup and
cleanup. Candidate release 7 builds and upgrades normally, and restores all nine
gadgets. Its [native replay](gadget-runtime-followup-logs/a7-gadgets7-restored.png)
shows unavailable Weather without a false temperature/symbol and properly scaled
thumbnails. [Calendar Options](gadget-runtime-followup-logs/a7-calendar-sunday-fixed.png)
now displays Sunday; accepting without changes leaves the layout byte-identical.
Archive SHA-256 `0abb8a1abb28f4267f06a60fbcbc57f83ec3f1e79f848a1f3e0bb34cb50221b4`,
351,920 bytes; installed binary SHA-256
`4b63620ef6abb7c99519783852c65058bb35f425db30571a100c6b3c773e95a0`.
[Build](gadget-runtime-followup-logs/package7-build.log) and
[upgrade](gadget-runtime-followup-logs/package7-upgrade.log) exit 0; the archive
has the same 61 root-owned paths/modes, with icons/data/hooks unchanged.

The native preview replay exposed uneven label baselines when thumbnails retain
different outer dimensions. Release 8 adds a fixed transparent thumbnail canvas
around the aspect-preserving scaled image. The expanded suite still passes
16 Qt results. The [installed release 8 gallery](gadget-runtime-followup-logs/a7-gadgets8-gallery.png)
now has aligned row labels and complete aspect-preserving thumbnails. All nine
saved instances restore. Weather remains unavailable without an invented reading.
[Calendar Options](gadget-runtime-followup-logs/a7-calendar8.png) still shows Sunday;
accepting leaves the entire saved layout byte-identical to the pre-upgrade copy.
No icon assets were replaced. The private profile's original metadata still
identifies release 6; release 8's installed identity is independently recorded
by the normal upgrade audit rather than inferred from that stale profile metadata.

Release 8 archive SHA-256:
`77f494f5c250ab93d12db0581aa105c7c83ec8f51ff4d201a0d21016dd7f0d74`,
351,876 bytes. Installed binary SHA-256:
`f09a685f9d0687a99c341f53b65042449c795a4577494789f7322a1d6baf3a0a`.
The [build](gadget-runtime-followup-logs/package8-build.log) passes all four CTest
groups; the [normal upgrade](gadget-runtime-followup-logs/package8-upgrade.log)
passes all 57 installed-file checks without dependency or conflict overrides.
The archive retains the same 61 root-owned paths and modes.

Release 8 now replaces 6 in the local next-build manifest; KWin 7.1 remains
selected. The updated manifest SHA-256 is
`e9f5da8bcf3f1ae96032e64d4fe7bddbe3b0974988c3fcff6f2daf3a3d65bc14`.
The required/optional lists and 18/16/2 counts above are unchanged. The complete
[integration checker](gadget-runtime-followup-logs/integration8-check.log) passes
all 149 tests and its package, dependency, ownership, syntax, branding and Shell
checks. No ISO has been built from this selection.

### Release 8 normal-account startup

The private host was stopped after the unchanged-layout check. Normal Start-menu
logout reached [SDDM](gadget-runtime-followup-logs/a7-sddm8.png); password login
created session 8 on the same boot. The
[01:23:24 audit](gadget-runtime-followup-logs/login8-audit.log) verifies the normal
session-bus owner is autostarted process 16005, started at 01:22:28, with release
8's exact running executable hash. All 57 installed files are present. The
GadgetHost autostart unit and Shell/KWin/Plasma units are active; the latter have
zero restarts, and system/user failed-unit lists are empty at that snapshot.
The ordinary account's saved layout remains empty, separate from the nine-item
QA profile. Opening the [normal gallery](gadget-runtime-followup-logs/a7-gadgets8-normal.png)
after the audit confirms readable light-theme labels and aligned previews.

The first attempted audit keystrokes coincided with a restored blank Paint
window taking focus and did not create an audit report. The terminal was
explicitly focused and its input cleared before the successful retry. No
manual gadget-host launch preceded that audit. This pass is normal logout/login,
not a new cold-boot or fresh-install claim for release 8.

## Scope still open

Complete provider success/failure/cache validation, remaining gadget settings and
controls, scaled/cross-monitor dragging and broader desktop/security/recovery
checks remain separate. Final ISO assembly still requires the user's approval,
then exact online/offline installation testing. Current r10 media is unchanged.
