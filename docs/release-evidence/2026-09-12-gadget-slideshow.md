# Slide Show: damaged-file playback regression

12 September 2026. **Scoped source/package/native playback and normal-login checks pass.**
This is separate from the compositor Show Desktop investigation. Gadgets 14
remains installed in the QA VM; the next-build manifest remains at Gadgets 10.

## Native reproduction

The offline 1920×1080 VM runs an isolated Gadgets 13 profile with two large Slide
Show instances. Both use the same two existing QA screenshots as pictures, with
a two-second delay, no transition and shuffle disabled. The left folder contains
only the two valid PNGs; the right folder also has a deliberately invalid PNG
alphabetically between them. No product icon or artwork is created or changed.

Seven captured frames show the left slideshow changing between the two pictures,
while the right remains on the first. Picture-region hashes confirm that the
control changes repeatedly and the damaged-folder image remains byte-identical.
The private runtime is then stopped with Ctrl+C; the normal account's layout
was not changed. One initial launch attempt reached the idle lock screen instead
of the terminal; it did not start a QA profile. The replay below was performed
after unlocking and confirming terminal focus.

- Runtime profile: `slides13-profile.RY0mMg` in the offline VM results.
- Installed package: `aero7-gadgets 3.0.0-13`.
- Executable SHA-256: `8da69f2c9e4a96a6daba7a5fc52a19736872a4734fb74f3e2ed4d97ff67bad86`.
- [Evidence directory](gadget-slideshow-logs/): seven screenshots, copied runtime
  log/layout and picture-region hash sequence. Regions are `(60,210)-(300,380)`
  for the control and `(360,210)-(600,380)` for the damaged-folder instance.

## Source cause and proposed correction

The previous code selected only the immediate next index. If that image failed
to decode, it returned without advancing, so every following timer tick retried
the same damaged file. Initial loading likewise did not skip a bad first file.

The local correction tries at most one complete file-list cycle in the requested
direction. It re-reads files at selection time, including files removed after
the initial folder scan, and retains the last displayed image if none can be
read. Initial loading skips unreadable pictures. Folder changes clear the old
transition state, and a folder with no readable pictures uses the existing
placeholder without an idle slideshow timer. Delays are clamped to the same
2–3600-second bounds as the settings UI, including resuming playback.

Nine new gallery test rows cover corrupt first/next/previous pictures, removal
after scanning, removal of all pictures, folder changes during a transition,
delay bounds and pause/resume. They are prepared in the source and in a separate
regression work directory (`work/gadgets14-regression.ycOop2`) using Gadgets 13
runtime source for a before-fix baseline. The full gallery baseline reproduces
six failures and 37 passes: corrupt first/next/previous pictures, removal after
scanning, stale transition state after a folder change, and delay overflow fail.
After the correction, the complete gallery executable passes **43 results,
zero failures**, including setup/cleanup. Logs are retained alongside the native
baseline evidence. The normal Gadgets 14 package uses the source
archive SHA-256 is `d8c4c929206493abe848cb06066f7ebcedc4ce1f89a43991d405ae335a4a7e68`.

## Installed corrected replay

Gadgets 14 finishes its normal package build at 19:26:38 CEST. All seven CTest
groups pass, including 43 gallery and 74 provider Qt results. The normal VM
upgrade from 13 to 14 passes with all 57 package paths and the expected binary.
The normalized package file manifest differs from 13 only in build/package
metadata and the host executable: icons, artwork, launchers, hooks and file
modes remain unchanged.

- Package SHA-256: `31673af6e422ac6c80dc85d44b07a2cc73a84f47e62eada5e3af0c918c2b2aa3`.
- Installed executable SHA-256: `ad042dd2e5815b627cd10403b5f99e131accd182746c7b6a06d6d82b11dd480a`.
- Upgrade report: `gadgets14-upgrade.IlzwAy`.
- Isolated native replay: `slides14-profile.jWfeBF`.

With the exact same folders and settings used for the failing baseline, both
instances now alternate between the two pictures. Seven screenshot-region
hashes show the damaged-folder instance advancing in step with the valid-only
control, rather than freezing on its first image.

On the damaged-folder instance, the native pause button changes to Play.
Previous skips the damaged file and shows the other valid picture; that picture
remains unchanged after five seconds while still paused. Next skips the damaged
file in the forward direction and returns to the other picture without resuming
the timer. Pressing Play resumes automatic changes. Screenshots and image-region
hashes are retained in the evidence directory. The control-image hash regions
exclude the overlaid buttons: `(360,210)-(600,350)`.

The private runtime is stopped before a normal logout/login. The 19:35:23 CEST
audit (`gadgets14-login.K11VEw`, session 14) verifies the normal autostart PID
24658 running the exact installed executable, with no failed user/system units
and zero shell/KWin/Plasma restart counts. KWin remains 7.1 and its permission
checks are not bypassed. The account's empty gadget layout is byte-identical
to its pre-test layout. This verifies the reproduced playback/control failure, not every
slideshow option, every image format, every gadget or the final ISO. The Show
Desktop compositor gate and broader release gates remain open; the build
manifest still selects Gadgets 10.
