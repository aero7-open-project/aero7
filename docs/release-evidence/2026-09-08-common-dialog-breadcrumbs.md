# Native dialog breadcrumb candidate — 8 September 2026

## Observed mismatch

The installed Explorer-50 shared dialog used a plain location field. Paint's
Open/Save dialogs exposed `~/.local/share/Aero7/Libraries/Documents` rather
than the library hierarchy used by the main Explorer window. Earlier screenshot
128 in the Snipping Tool handoff evidence records the raw-path presentation.

## Local correction

The shared dialog now has a private breadcrumb control. It uses the existing
library configuration and mounted-volume presentation policy, retaining the
real filesystem path for each destination. It does not invent drive mappings
or change library save destinations.

- Library locations display **Libraries > Documents/Pictures/etc.**, followed
  by any nested folders.
- Mounted removable locations start at the matching volume label. Nested mount
  roots use the most specific match; similarly prefixed sibling paths do not
  match incorrectly. These mappings have unit coverage, not physical-device
  acceptance in this pass.
- Crumb buttons navigate; their dropdowns enumerate real subfolders.
- Ctrl+L explicitly enters the real address. Escape abandons address editing
  and restores the breadcrumb without cancelling Open/Save.
- Existing history, filename, filtering and save-backend behavior are retained.
  The exported common-dialog class layout did not change. No new icon assets,
  theme settings, global shortcuts or persistent environment overrides were
  introduced.

## Evidence

All 20 local CTest groups passed. The disconnected r10 Wayland VM then ran
the candidate shared library using a process-local `LD_LIBRARY_PATH`, without
replacing the installed library or changing packages.

The first VM run had 50 passing rows and one failed new shortcut test. It
checked only exposure before sending Ctrl+L, not keyboard activation. The test
was corrected to require `qWaitForWindowActive`; the product binary was
unchanged between runs. The second run passed **51 rows, zero failures**, in
6.2 seconds. Both logs are retained, rather than discarding the first failure.

In the real installed Paint application with the candidate library:

- Screenshot 141 shows **Libraries > Documents**, without the internal path.
- Screenshot 142 records Ctrl+L address editing; Escape returned to breadcrumbs
  without closing the dialog.
- Screenshot 143 shows the real Libraries dropdown.
- Selecting Pictures navigated to **Libraries > Pictures**, showing its
  Screenshots folder (144).
- Cancelling Open and closing unchanged Paint returned to the terminal (145).

Candidate library SHA-256:
`29c6e426db205199cb16616ae65bb25f6d23d2f41b712bffdd4a5450a545a926`.
Settled test executable SHA-256:
`8560230dd056625852350fae21769d20a7323f12b3a5a948662d6ca0abd67022`.
Installed library baseline SHA-256:
`1c26ad73a6953bf0d5c806661432e75b7f664d0a22f45a75c2014d318c67479e`.
The same installed hash was verified again after closing Paint. Logs and
screenshots are retained in `r10-dialog-location-logs/`, including both VM
test runs and the full 20-group local CTest log.

## Remaining boundary

The release-51 package build was started from the release-50 source archive,
replacing only `aero7commondialog.cpp`, `aero7commondialogtest.cpp` and adding
the private `aero7dialoglocation.h`. Archive inventory comparison verified
that all other file contents and modes remain unchanged, with no duplicate
members. Source archive SHA-256:
`d2cbdb6c8b78179b33568ff63d988584c7dd92c3ff872d0145d20063180c112f`.
The clean package build completed with all 20 CTest groups passing during
`check()`. Package path inventories match release 50 exactly; the tests did
not add test executables to the installed package. Direct ELF dependency
comparison found 14 binaries/libraries in both packages with no changed
dependencies. Paint/shared-dialog linkage and temporary-RPATH checks passed.

- Package: `aero7-file-explorer-25.12.3-51-x86_64.pkg.tar.zst`
- Size: 8,284,451 bytes.
- SHA-256: `a4ffde82f792781ac75bd658259a90193f5365c7eb312f6e3aa00b5c0480e368`.
- Installed shared library SHA-256:
  `86b79894115b3c626f29fccfe3708a22a37b4d9230b2d885a4eed6da5dd581ab`.

The normal offline `pacman -U` transaction changed only Explorer 50 to 51.
Its file check reported 665 files, zero missing. The initial QA guard stopped
before installation because it also matched the background Explorer daemon;
the guard was narrowed to allow that exact no-document-window process while
still rejecting open Explorer/Paint windows. Both logs are retained. The daemon
was not killed during the transaction; a normal reboot check was started.

With `LD_LIBRARY_PATH` and `LD_PRELOAD` unset, `ldd` resolved the dialog tests
to `/usr/lib/libaero7commondialogs.so.1`. All 51 Wayland rows passed against the
installed release. Paint's five isolated document workflows also passed using
that installed library: same window, separate window, unsaved Cancel, Discard
and Save. The QA Paint probe was process-local and created isolated images;
it did not replace product binaries or change the real user's preferences.

The normal reboot/password login completed. The boot ID changed to
`d50e4622-7a0b-41e1-b762-a4b38f9e1d6b`; the installed hash and all 665 files
passed again. The shell, screenshot service, update-check timer and firewalld
were active. The post-login snapshot had zero failed system/user units, but
does not erase or resolve the earlier offline update-check failure. The saved
user journal retains graphics, keyboard and other startup warnings. The taskbar
Explorer shortcut opened File Explorer normally (157).

A normal post-reboot `kolourpaint` launch, without a candidate library or QA
probe override, also passed the manual Open-dialog check at 1920 x 1080.
Screenshot 160 shows Libraries > Documents; 161 shows Ctrl+L selecting the
real address; 162 shows Escape restoring breadcrumbs while keeping Open
visible. Cancel then closed Open and unchanged Paint closed normally (163).
The reboot audit, full user journal and these screenshots are copied into
`r10-dialog-location-logs/`. Paint's initial launch took longer than the first
four-second screenshot interval; no precise startup-time benchmark is claimed.

This is now a tested installed package, not a changed ISO.
Long-path/scaling, live-removal behavior and final-media checks remain.
Other dialog/Explorer parity requirements remain
open. The separate early-Escape screenshot problem is not fixed: Spectacle
creates its capture windows only after receiving the initial croppable image;
no systemwide Escape shortcut was added to work around missing keyboard focus.

Nothing was committed, pushed or published.
