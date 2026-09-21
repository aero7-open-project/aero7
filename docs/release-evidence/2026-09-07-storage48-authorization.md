# Explorer 48: actual authorization cancellation and busy-drive checks

Installed offline r9 VM, Explorer `25.12.3-48`, Desktop `0.2.0-29`, Wayland,
1920×1080, no network adapter. This continues the
[Explorer 48/Desktop 29 evidence](2026-09-07-explorer48-desktop29.md), not final
ISO acceptance. No production code or package was changed in this pass.

## Scope and restoration

Only the existing disposable 96 MiB FAT virtual USB fixture was used: label
`AERO7_QA`, UUID `F921-93DA`, serial `AERO7QA96`. A temporary polkit rule required
administrator authentication only for this UUID, `/dev/sda`, the `aero7test`
account and filesystem-mount actions. Other devices/actions were unaffected.
The rule used the documented [UDisks authorization variables](https://storaged.org/doc/udisks2-api/latest/udisks-polkit-actions.html).

Installation was guarded by guest hostname, KVM, account, exact device size,
USB transport, UUID, label and unmounted state. The rule was removed after
comparison with its exact source, at 23:34:26. It was not included in a package.
The final audit rechecks absence. No host policy or physical disk was changed.

## Real authorization sequence

- **Computer cancellation and retry:** opening the unmounted tile raised the
  actual User Account Control prompt (`479`). Cancel left the drive unmounted
  and showed an open-drive failure (`480`). Retrying and approving mounted the
  drive and opened its original files (`481`).
- **Navigate away while authorization is pending:** a repeated, short sequence
  opened authorization from Computer, selected Documents, and then approved
  the still-pending mount. Screenshot `488` shows Documents behind the real
  prompt; `489` shows the drive mounted while Explorer remains in Documents.
  No delayed navigation replaced the user's newer destination.
- **Save As authorization cancellation:** the installed `/usr/bin/aero7-file-dialog`
  retained `storage48-unsaved.png`, its original directory and open state after
  cancellation (`491`, `492`). It did not return a selected path.
- **Close the owning Save As dialog during another pending mount:** Cancel
  closed the dialog and authorization prompt. The process returned its normal
  cancellation code, with empty selected-path output (`493`). Polkit recorded
  the disconnected request failing at 23:33:08.

The Save As harness used an isolated empty configuration directory to preserve
the user's saved settings. Its dark/default-looking controls are not a normal
desktop-appearance acceptance result. It loaded the installed dialog binary and
library; no preview executable or substituted dialog implementation was used.
No PNG was written. The result is `storage48-save.iMHGnT/`.

The first navigation-away attempt included a misplaced drag which moved the
Explorer window instead of the authorization window. That long sequence is
not used to prove cancellation timing. The short repeat (`488`, `489`) is the
acceptance evidence. Original screenshots are retained.

## Busy-device failure and recovery

A terminal was deliberately left with its working directory on the fixture.
A normal `udisksctl unmount` confirmed the actual `DeviceBusy` refusal (`497`).
Nothing was force-unmounted and no blocking process was killed.

The first sidebar Safely Remove attempt showed no visible explanation (`496`).
That attempt remains inconclusive: no observer captured its request/signals.
Do not call the initial absence fixed merely because later runs passed.

A read-only Qt observer was then loaded into one newly launched installed
Explorer process. It issued no device operations and logged the actual Solid
and KFilePlacesModel signals. Busy teardown returned error 2, a valid model
index and a user-facing error. Computer and Documents both displayed the red
busy-drive banner (`500`, `501`). The trace also records that `lsof` is absent,
so the native fallback message does not name the blocking application. This
missing optional diagnostic capability remains a packaging follow-up.

After closing that observed process, a normal uninstrumented Explorer launch
also displayed the busy-drive banner (`502`). A retry remained busy because
Explorer had itself inherited the USB working directory from the terminal.
After releasing the terminal directory and closing that Explorer instance,
another ordinary launch from home successfully removed the drive (`504`).

At 23:47:32–33, UDisks logs record unmount cleanup, SCSI cache synchronization,
START STOP UNIT and successful power-off. The fixture disappears from both
Computer and its sidebar. This verifies recovery after releasing the blockers,
not forced removal or automatic closure of unrelated applications.

## Final audit and artifact state

`storage48-policy.log` ends with the 23:47:54 audit: clean Explorer/Desktop
package checks (665/75 files), unchanged Paint preferences, no failed system
units, no mounted fixture and normal Explorer PID 37627 without the observer
in its process maps. The temporary polkit rule is absent.

QMP device removal completed before closing the backing node. A subsequent
host FAT directory check found the same 314-byte README and test Photos folder,
with 100,442,112 bytes free. The fixture remains available for future tests.

Raw logs, guarded QA helpers and screenshots are in
[storage48-authorization-logs](storage48-authorization-logs/). The observer's
binary SHA-256 was `969d94b3da0527d57a55893399c9ac3bc205c1c6e011bcf78fec91ba559f55b4`;
it is a local QA tool, not release content. No commit, push or publication.

## Still open

The initially silent attempt needs a longer mounted-device lifecycle replay;
application-name reporting lacks `lsof`. Multiple drives, physical/optical
devices, explicit policy denial distinct from user cancellation, common-dialog
address presentation and current-stack reboot/final ISO matrices remain open.
These checks do not establish complete USB support or an entirely bug-free DE.
