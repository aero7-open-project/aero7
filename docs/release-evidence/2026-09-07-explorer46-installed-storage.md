# Explorer 46 installed storage and dialog validation

Local pre-release evidence; not final-media acceptance or publication approval.

## Package and unchanged consumers

Candidate directory: `work/beta2-explorer46.WVvAvZ/`.

- Package: `aero7-file-explorer-25.12.3-46-x86_64.pkg.tar.zst`, 8,250,163 bytes.
- Package SHA-256: `1eb301241e070d64408557e9b4c356e3fb4d7f8c8524998e0e6d68e9a604e2e7`.
- Source SHA-256: `0f2876ddd611dd65a53e0169647152c7fa17a984ac81bc4a8f21211037ec6eab`.
- Fresh source extraction/checksum succeeded; the incremental build source
  matches the extraction recursively. All 14 ELF dependency lists match 45.
- Normal offline VM upgrade 45 to 46 changed only Explorer. Explorer's 665
  files and Paint 8's 709 files pass package file checks. Paint preferences
  remain unchanged. See `explorer46-upgrade.log` and inventory/hash files.

The same existing offline guest remains at 1920×1080, with no network device,
boot ID `c0388ac1-1b28-4919-890f-1cd352dcda1e`. The release ISOs do not contain
this package. No GitHub commits, pushes, signing or publication occurred.

## Native USB discovery and opening

The existing, cleanly detached 96 MiB FAT fixture (UUID `F921-93DA`, label
`AERO7_QA`, serial `AERO7QA96`) was attached through QMP again. No terminal mount
command was used before this test. Explorer 46 displays the unmounted native
USB volume in its sidebar (`431-explorer46-unmounted.png`). Clicking it once
requests native setup, mounts the filesystem and opens its actual README.
The mounted label becomes `AERO7_QA (D:)` (`432-explorer46-click-setup.png`).

This closes the observed sidebar visibility/setup failure from 44 and 45.
It does not yet prove unmounted-drive discovery in Computer or common dialogs,
nor cancellation, optical media or physical hardware.

## Installed common dialogs and Paint

An updated standalone test executable was built against the shared dialog
library without a build-tree RPATH/RUNPATH, then run on the guest with normal
installed `/usr/lib/libaero7commondialogs.so.1` resolution and Wayland.
Executable SHA-256: `459292e608473d0d77abd63d667e04a87769274e6817a2a0143c2d6aab403fcc`.

`explorer46-common-dialogs.5P6c7z` records **47 passes, zero failures**, including
setup/cleanup (45 functional cases), in 4677ms. The new single-click, tree
Enter, address Enter, and unavailable Save/Open/Choose Folder cases pass.
Unavailable-location unit cases inject recorded storage identity differences;
they do not themselves perform a USB unmount.

Unchanged installed Paint 8 also passes all five instrumented Wayland workflows:
same-window open, separate-window open, unsaved cancel, discard and save.
Evidence: `paint8-readiness-workflow.52buIF`. The existing bounded-readiness
probe runs with isolated preferences; it does not replace Paint's executable.
The post-test audit confirms no Paint process remains, both package inventories
are clean and the user's saved Paint preference hash is unchanged.

See `explorer46-tests-audit.log`. Remaining live USB tests and release-wide
gates are still open; do not describe this as complete Beta 2 acceptance.

## Real unmount with Save As open

The installed standalone dialog opened with `usb46-check.png`. One click on
the mounted USB row opened its README (`435`), without accepting or closing the
dialog. Normal non-root `udisksctl unmount` succeeded at 22:22:54 while Save As
and the main Explorer USB view were open. The dialog replaced cached file rows
with an unavailable-location message, disabled Save/search and retained the
filename (`436`). New Folder was rejected with a warning (`437`). One click
on Documents restored the file area and Save button without changing the name
(`438`). The dialog was then cancelled; it did not return a saved path.

The main Explorer view handled external unmount differently from its own
Safely Remove command: it selected the nearest existing ancestor,
`/run/media/aero7test`, with a warning (`440`). That is a raw, empty runtime
mount container, **not the user's home**, despite having the same final label.
The warning truthfully describes the lost path, but the fallback destination
does not match Aero7's reduced mount presentation.

Working source now redirects this infrastructure fallback to the actual home
directory, while preserving ordinary parent-folder recovery when a folder is
deleted on a still-available drive. Nine path-policy cases cover the actual VM
input, alternate mount roots, missing containers, retained parent folders,
nonmatching usernames and root. This correction is **after the frozen 46
source archive**, not in the installed package. It needs another package/VM
check; don't silently treat it as verified from this 46 run.

The final working-source build and all 20 CTest groups pass (21.64s). The
unmount audit `storage46-audit.Rk1qtN` confirms the fixture UUID is not mounted,
no failed system units, clean package files and unchanged Paint preferences.
Save As produced an empty result log after Cancel. After QMP device/node
detachment, host inspection still shows only the original 314-byte README.
No PNG or new folder was written to the fixture; its image is retained.

Raw logs, test output and selected screenshots are retained in `usb46-logs/`.

## Remaining work

- Package and verify the later external-unmount recovery correction.
- Show/open unmounted removable drives in Computer and common dialogs, not
  only the Explorer sidebar; keep filesystem labels consistent across surfaces.
- Exercise mount cancellation, disappearance during setup, busy-device failure,
  optical eject, reconnect and physical hardware paths.
- Rebuild both final ISO variants and repeat the full fresh-install/reboot
  acceptance matrix with the final package set and release-wide checks.
- Keep website announcements/delivery information as drafts until testing and
  publication approval are complete. ISOs are destined for the website, not
  GitHub release uploads.
