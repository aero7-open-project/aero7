# Native dialog USB removal and recovery — 8 September 2026

This is candidate-library QA in the modified r10 offline VM, not final ISO
acceptance. It extends the [overflow/scaling pass](2026-09-08-dialog-overflow-scaling.md).

## Test configuration

The existing guest shut down normally with `systemctl poweroff`; QEMU PID
188806 exited and the disk had no holder. The guarded resume launcher was
updated to include a USB controller, then verified the unchanged r10 offline
ISO checksum and relaunched the same disk as QEMU PID 310781. Password login
completed. The VM remains disconnected (`-nic none`), 1920×1080, with 6 GiB RAM.
The QA input/result shares were mounted for this boot only.

Only the separate 96 MiB FAT QA image was attached. Its serial is `AERO7QA96`,
label `AERO7_QA`, UUID `F921-93DA`. The original r9 fixture was not modified.
Before and after the entire replay, its copied image SHA-256 was identical:
`bb0bbc822a5215a82b150ef12b80d98efa9d28d6ed1acf3f825a5c48087c73a0`.

The native `aero7-file-dialog` Save As executable used the corrected library
through process-local `LD_LIBRARY_PATH`. Explorer 51 remained installed and
unchanged; the candidate library hash is
`38281ed02c6ca759163e1139b3bd90e1e1eb4a10c85f3f1fdf86f0158038b799`.
The normal user profile was used with a separate QA dialog-state identifier.

## Observed sequence

1. The unmounted USB appeared under Computer (179). Clicking it mounted it
   through native device setup and displayed README.txt and Photos. The
   breadcrumb and sidebar displayed `AERO7_QA (D:)` (180).
2. The breadcrumb dropdown listed the actual Photos folder (181). Selecting
   it showed `AERO7_QA (D:) > Photos` and its Trips folder (182). The filename
   remained `keep-usb-name.png`. Clicking the drive crumb returned to its root.
3. A guarded non-root `udisksctl unmount` verified the fixture identity and
   unmounted `/dev/sda`. The dialog replaced cached rows with an unavailable
   message and disabled Save, preserving the filename (183). Clicking the
   stale drive crumb did not restore saving. New Folder displayed an explicit
   unavailable-location warning and did not create a folder (184).
4. QMP detached the already-unmounted USB; `info usb` showed none. The sidebar
   removed its device row while Save remained disabled (185). Reattaching the
   same fixture restored an unmounted device row, not phantom files (186).
5. Keyboard navigation selected that device (187). Enter performed native
   setup, restored README.txt/Photos and the drive breadcrumb, and enabled Save
   without accepting or losing the filename (188).
6. Cancel closed Save As. The normal helper unmounted the fixture, after which
   QMP detached the USB and released the backing node. No forced unmount or
   unplug during writes was used. The complete image hash stayed identical;
   host FAT inspection found only the original README and Photos/Trips tree.

The final guest audit found 665 Explorer files, none missing, and the unchanged
installed library hash. It found zero failed system/user units at that instant;
the saved session journal still contains startup warnings. This does not erase
older disconnected-update failures or prove the full desktop warning-free.
The device popup took focus during the first launch attempt; the helper had
not run, so terminal focus was restored before typing it again. No duplicate
dialog process was started.

Raw logs and screenshots are retained in `dialog-usb-logs/`.

## Package and release boundary

Explorer 52 was built separately from Explorer 51's source archive with
only the reviewed private breadcrumb header and its regression tests replaced.
Archive comparison found exactly those two changed paths, no other content,
mode, type or link-target change, and no duplicate members. Its source archive
SHA-256 is `5306e819178015cf1ee00ebb677b2abbd80e5a43c5973a4c1e8f19b91a87de09`.
Build location: `work/beta2-explorer52.Ov78Uo/`.

The build completed at 16:33:46 with all 20 CTest groups passing (23.77 seconds),
the host dependency precheck skipped (`--nodeps`), and no host packages installed.
Warnings are retained in the package log. Packaged paths, dependency/provides/
conflict/replaces fields and all 14 ELF direct-library dependency lists match
Explorer 51. Native Paint/dialog linkage, SONAME and temporary-RPATH checks pass.

- Package: `aero7-file-explorer-25.12.3-52-x86_64.pkg.tar.zst`
- Size: 8,291,930 bytes.
- SHA-256: `cea711ac30b79eb42158b6f90cf269494b1dd095caadd098ee69aa56ede6c8da`.
- Packaged stripped dialog-library SHA-256:
  `160e5fd8c2e49074c933d81a2b8fe4b4e03563bb67123beb6d693e51e8f9fbd4`.

The normal offline upgrade changed only Explorer 51 to 52. All 665 package
files were present and the installed hash matched. With library overrides
unset, the dialog test executable resolved `/usr/lib/libaero7commondialogs.so.1`
and passed all 54 Wayland rows in 5734 ms. Paint's five isolated workflows
passed again: same-window, separate-window, unsaved Cancel, Discard and Save.
The QA probe was process-local and did not replace Paint or user documents.

The VM's idle lock intercepted the first typed upgrade command before its
helper ran. The lock-screen authentication error is retained as QA input
evidence, not an installer/package failure. Normal password unlock succeeded;
the actual upgrade log starts at 16:36:49.

The normal reboot and password login subsequently passed. The audit at
16:44:25 checked a changed boot ID, Explorer 52's installed version and exact
library hash, all 665 package files, and active screenshot, update-check timer,
firewalld and shell services. System and user failed-unit snapshots were empty.
The taskbar Explorer shortcut opened the normal home view after login (200).
The guest remained disconnected with only loopback throughout.

This is not a clean-journal claim: the full retained user journal still includes
portal application-registration errors, the disabled-wallet Secret portal exit,
QTerminal variable-width-font warnings and virtual graphics/hardware warnings.
The audit marker records the explicit checks above, not complete desktop health.
Evidence: `dialog-usb-logs/explorer52-reboot-audit.log`,
`explorer52-user-journal.log`, `explorer52-boot-before.txt` and screenshots
197–200 in the same evidence directory.
No ISO, repository manifest, GitHub commit or publication changed in this pass.

Physical USB/optical hardware, simultaneous devices and broader failure paths
remain separate acceptance requirements. So do the other Beta 2 release gates,
including the early-Escape screenshot problem and final online/offline media.
