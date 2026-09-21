# Slideshow Options — preserve playback

Local bug-fix work only. No commit, push, publication or final ISO build.

## Reproduced failure

Gadgets 24 reloads its entire slideshow whenever Options is accepted. This
returns to the first picture and resumes a paused slideshow, including unchanged
OK and changes only to delay, shuffle or transition. Ten of twelve new real-dialog
regression cases fail; both Cancel cases pass. The
[baseline log](gadget-slideshow-options-logs/baseline24.log) records those results.

The installed release-24 Wayland replay uses a private gadget profile and two
existing QA screenshots, not the account's ordinary layout or pictures. After
Pause and Next, the [second picture is paused](gadget-slideshow-options-logs/a7-slide24-paused-second.png).
Opening Options and clicking unchanged OK
[returns to the first picture and shows Pause instead of Play](gadget-slideshow-options-logs/a7-slide24-reset-playing.png):
playback has resumed. The private host was stopped after recording the failure.

## Correction and source coverage

Only a changed effective folder reloads the slideshow. Unchanged settings keep
the picture, index, pause state and timer countdown. A changed delay updates the
existing timer without activating a paused one. Shuffle applies to subsequent
advances without resetting the current picture. Selecting no transition finishes
the current fade and discards its previous-image layer. Equivalent paths ending
in `/.` do not count as a changed folder.

Fourteen new cases cover playing and paused states for unchanged OK, delay,
shuffle, transition, active-fade cancellation, Cancel and equivalent-folder
spelling. The existing changed-folder test now uses the actual Options dialog
instead of calling the loader directly. It still clears the old fade and stops
the timer for an empty new folder. The
[targeted run](gadget-slideshow-options-logs/corrected25.log) passes 24 Qt results,
including the existing corrupt-image and pause/delay tests and setup/cleanup.
All [eight source test groups](gadget-slideshow-options-logs/full25.log) pass:
156 gallery, 74 provider and 11 media Qt results. No production icons changed.

## Candidate

Gadgets 25 builds normally in `work/beta2-gadgets25.IZ4OfN` with two jobs and
all eight package-test groups passing. The host-only dependency bypass does not
disable tests or authorize dependency bypass during installation.

- Source SHA-256: `42811249bbe50aa97c3b505ff8dcc2b743c133f168e51c7743ec38450f640125`.
- Package SHA-256: `721a513491b4c9f368144f7dbea811c6d78f5f9442e405efeaa0235f4b2db9bf`.
- Executable SHA-256: `ae36e86bcecc0ed48fdea2cf27117996c14a65adc564d06ef3decd358386da79`.

Normal [VM upgrade](gadget-slideshow-options-logs/upgrade25.log) passes dependency
checks, all 57 installed files and the executable hash. The corrected private
Wayland replay preserves the [paused second picture after unchanged OK](gadget-slideshow-options-logs/a7-slide25-unchanged-retained.png).
Changing the delay from 600 to two seconds leaves that picture
[paused](gadget-slideshow-options-logs/a7-slide25-delay-paused.png), with the saved
layout recording the accepted two-second interval. Explicit Play then
[advances at the new interval](gadget-slideshow-options-logs/a7-slide25-resumed-two-seconds.png).
The private host stops normally; ordinary account settings are not the fixture.

The [normal-login audit](gadget-slideshow-options-logs/login25/audit.log) passes
in Wayland session 23 after logout/login, on the same boot. Autostart owns PID
64823 with the exact release-25 executable hash. The actual KWin child 64523
has no permission-check bypass. Desktop services are active with zero restarts,
the failed user/system unit lists are empty at this checkpoint, and the ordinary
account layout is byte-identical to the release-24 login baseline. This is not
a new cold-boot test. The next-build manifest now selects Gadgets 25 / Control
Panel 54 / KWin 7.3. Its SHA-256 is
`8fcbc92a719570c6bc101b9e169e6766a618c43e5d34783c33f70615ee198f80`.
All [149 integration tests](gadget-slideshow-options-logs/integration25.log),
[18 online archive checks](gadget-slideshow-options-logs/online25.log), and
[53 offline archive / 35 repository-entry checks](gadget-slideshow-options-logs/offline25.log)
pass. Shell source pin and core/optional membership remain unchanged.

These tests do not
prove persistence of slideshow playback position across logout, physical-device
removal, or final-media acceptance. Frozen ISOs are unchanged.
