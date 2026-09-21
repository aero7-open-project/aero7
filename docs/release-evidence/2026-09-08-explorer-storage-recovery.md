# Explorer 49 candidate: device-scoped removal recovery

Local candidate evidence; not final ISO acceptance or permission to publish.

## Reproduced defect

The previous implementation attached another unscoped success callback for
every removal request. A failed request could leave that callback pending.
The first subsequent recovery then disconnected every success listener,
including other requests and unrelated observers. It could therefore lose
the recovery action for the drive that actually completed removal.

Two new regression cases failed against the previous implementation:

- An unrelated success observer received one event instead of two.
- With requests for two different mount paths, completing removal did not
  return the view on the completed drive to Home.

The red run recorded two failed functional cases. Tests use temporary
directories and event dispatch; they do not mount or unmount host disks.

## Correction

The Places panel now retains the requested mount path per actual native
storage-access object. Native completion consumes that request on success
**or failure**, and successful completion carries the matching path to one
permanent main-window connection. Object destruction discards its pending
request, preventing a replacement device from inheriting stale state.

Internal removal temporarily suppresses the external-request callback. Native
completion now restores that connection, including after a failed removal.
Unique connections prevent repeated device discovery from adding duplicates.
Unrelated listeners are no longer disconnected by view recovery.

This does not force unmounts, terminate blocking applications, change polkit,
add a new icon pack, or alter update/firewall preferences.

## Source validation

- Focused run: six functional cases plus setup/cleanup, eight passes, zero
  failures or skips, 468 ms. Includes busy, denied, cancelled, independent
  observer, correct-drive recovery and destroyed-request cases.
- Full build succeeded in `build-aero7-file-explorer`.
- All 20 CTest suites passed, zero failures, in 11.90 seconds.
- `git diff --check` passed.

Logs are retained in [storage49-logs](storage49-logs/). The offscreen platform
emits expected capability/icon warnings; this is not warning-free desktop
acceptance. Model/helper regressions do not substitute for actual native
device lifecycle tests in the installed VM.

## Candidate and remaining acceptance

Source archive: `aero7-file-explorer-25.12.3-r49.tar.gz`.
SHA-256: `69a4fc4a63175773d6a85eafedcd12e4cd90cf662026e3b641054a0da3f4a62d`.
Build directory: `work/beta2-explorer49.75Yuif/`.

Package: `aero7-file-explorer-25.12.3-49-x86_64.pkg.tar.zst`, 8,267,249 bytes.
SHA-256: `2602a94c89cf14a7039ff046bc45c549ea08fe0d5dd935aa69e3585eac2ac246`.

The package was built from a freshly extracted, checksum-verified source
archive. The four changed source/test files match the tested working tree.
The local build skipped makepkg's host dependency precheck (`--nodeps`); it
did not install host dependencies or disable compiler/linker checks. All
14 packaged ELF direct-library requirements match Explorer 48. The package
retains the existing dependency declarations and compatibility launchers.

Normal offline-VM upgrade 48→49 passed. No other installed package changed;
Paint preferences remained unchanged. Installed shared dialogs passed 49
cases including setup/cleanup (47 functional), no failures/skips, in 5032 ms.
The unchanged test binary resolved the installed common-dialog library.
Paint 8 passed all five isolated-profile Wayland workflows again. Records:
`explorer49-common-dialogs.6XQBPc/`, `paint8-readiness-workflow.QSBZyf/` and
`explorer49-tests-audit.log`, retained in the linked logs directory.

### Actual removal failure and retry

The ordinary packaged Explorer, PID 43729, opened Computer and mounted the
96 MiB FAT fixture `AERO7_QA`, UUID `F921-93DA` (`512`, `513`). No observer or
replacement binary was loaded. The terminal was then deliberately placed
on that drive, while Explorer's own process had been launched from Home.

Sidebar **Safely Remove** showed the real busy-drive error and retained the
open files (`514`, `515`). After moving the terminal back to Home, the same
Explorer process offered the action again (`516`). Retrying removed the
drive and returned the open view to Home (`517`), without restarting Explorer,
force-unmounting or terminating the blocking terminal. The error banner
cleared on recovery. UDisks logged cache synchronization, START STOP UNIT
and successful power-off at 00:12:46.

The 00:13:15 restoration audit (`518`) confirms the same PID, no observer in
its maps, no mounted fixture, no temporary authorization rule, zero failed
system units, unchanged Paint preferences and zero altered package files
(Explorer 665, Desktop 75, Paint 709). Computer was restored for inspection.
QMP device deletion completed before closing the backing node. The host FAT
check still found the original 314-byte README, Photos folder and 100,442,112
bytes free. The virtual image was retained; no physical disk was used.

### Remaining findings

During the busy failure, the main breadcrumb dropped `(D:)` while the sidebar
retained it (`515`, still visible in `516`). This is a newly observed display
inconsistency, not a failed safe-removal recovery. Its cause and correction
remain pending. Missing `lsof` also still produces the native diagnostic
warning; the busy message does not name the blocking application.

The final online/offline media have not been rebuilt with this correction.
The earlier [Explorer 48 authorization report](2026-09-07-storage48-authorization.md)
remains the evidence for real UAC cancellation and busy-device behavior, not
proof of complete Explorer 49 device coverage. Its initially silent attempt
is not conclusively explained by this shorter passing replay. Simultaneous
native requests on multiple devices, external-request reconnection,
physical/optical devices and the wider final-media/reboot matrix remain open.

No commit, push, package publication or ISO release.
