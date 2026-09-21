# Unsaved-work logout: reproduced hazard and candidate correction

9–10 September 2026. **Scoped native logout and power-off checks pass; package integration remains pending.**
No package promotion, final ISO, commit, push or publication.

## Reproduction on the combined-stack guest

The disconnected Wayland QA VM has KWin 6.7.4-7, Paint 25.12.3-9,
Desktop 0.2.0-32 and Plasma Workspace 6.7.4-3.2. After creating an unsaved
400×300 drawing in Paint, Start → shutdown arrow → Log Out produced a native
Save/Discard/Cancel prompt. Separately, the compositor displayed a persistent
notification listing Paint and Command Prompt, with a two-minute forced-logout
countdown and separate cancel/override actions.

Clicking **Cancel in Paint** kept the drawing open but **did not cancel the
logout countdown**. Clicking **Cancel Logout in the notification** then cancelled
the outstanding session operation. The drawing was saved through the native
PNG dialog and Paint closed normally. Its SHA-256 is
`1140f7aaba1e94babd175c89a62eec4e10f05056e384f51f82a00d5a90623c1e`.
The same boot/session and active shell remained afterwards. A later scheduled
update check failed in this intentionally disconnected guest at 22:40:21 and
appears in the failed-unit list; the baseline is not a zero-failed-units result.
Its journal reports that package availability is unknown. This baseline
deliberately avoided letting the countdown destroy
the test document: actual data loss was not induced.

The matching [upstream KWin 6.7.4 session source](https://raw.githubusercontent.com/KDE/kwin/v6.7.4/src/sm.cpp)
contains the unconditional timeout path: after two minutes it replies with
permission to continue even when windows remain. Cancelling an application's
own close dialog does not communicate cancellation through this compositor path.
This is a separate issue from the earlier delayed Plasma service-stop warning.

Evidence: [save prompt](kwin-logout-logs/baseline-save-prompt.png),
[countdown still present after Paint Cancel](kwin-logout-logs/baseline-countdown-after-cancel.png),
[baseline audit](kwin-logout-logs/vm-baseline.log),
[user journal](kwin-logout-logs/vm-baseline-user-journal.txt).
Both screenshots are 1920×1080 upgraded-guest QA evidence, not release assets.

## Candidate correction

The [local KWin patch](../../patches/kwin-explicit-logout-choice.patch) removes
the unconditional force timer and its member/cleanup call. It preserves:

- Normal completion when all pending windows close.
- The existing delayed persistent notification naming pending applications.
- Explicit **Cancel Logout**, and cancellation when the notification is closed.
- Explicit **Log Out Anyway**, with text warning about unsaved-work loss.
- Refusal when another operation is already in progress, and cancellation in
  builds without notification support.

Elapsed time alone will no longer authorize abandoning pending applications.
The patch does not claim that Paint's Cancel button immediately cancels the
whole session request: users can close/save the app or use Cancel Logout.

The source guard [fails on the pristine source](kwin-logout-logs/baseline-policy.log)
and [passes after the patch](kwin-logout-logs/patched-policy.log). It checks the
timer's removal, text, explicit actions, successful-reply sites and cancellation
fallback. This is a structural source check, **not a runtime or semantic C++
proof**; the real deadline and actions still need testing in the installed VM.

## Controlled-timer and cleanup follow-up

The [control-flow harness](../../tests/kwin_logout_harness.cpp) compiles the actual
two session-method bodies extracted from the selected KWin source. Timer time,
Wayland windows, D-Bus reply delivery and notification transport are controlled
test collaborators; Qt signal connections and guard lifetimes execute normally.
It does not start a real compositor or prove installed transport/ABI behavior.

The original source [fails the old-deadline test](kwin-logout-logs/baseline-flow.log):
advancing controlled time permits logout despite a pending window. The initial
timer-only patch passes that case, but a subsequent
[late-window-close test fails](kwin-logout-logs/patched-flow-late-close.log) because
programmatically closing the notification can synchronously invoke the cancel
callback before the successful completion reply. That yields two replies.
The supported reentrant close path is consistent with
[KNotifications close/deref handling](https://raw.githubusercontent.com/KDE/knotifications/v6.29.0/src/knotification.cpp)
and its [manager/plugin cleanup](https://raw.githubusercontent.com/KDE/knotifications/v6.29.0/src/knotificationmanager.cpp).
This second case is a controlled regression, not yet a reproduced VM failure.

The revised patch disconnects the cancellation guard before programmatic
notification cleanup. The [expanded enabled suite](kwin-logout-logs/corrected-flow-full.log)
passes 11 Qt results (including init/cleanup), covering deadline survival,
cancel, explicit override, notification dismissal, early/late completion,
empty sessions, a new request after cancellation and concurrent-request refusal.
The [no-notification build](kwin-logout-logs/corrected-flow-no-notifications.log)
passes six Qt results, including safe cancellation and retry without UI support.
The [revised structural guard](kwin-logout-logs/corrected-source-policy.log) also
checks cleanup ordering.

The initial package build was deliberately interrupted with SIGINT to its
verified isolated build process group before updating the prepared source and
checksum. It was not a spontaneous failure. No VM was interrupted. Applying
the revised patch to pristine source produces byte-identical `sm.cpp`/`sm.h`
to the prepared build tree. Source checksum/signature checks
[pass again](kwin-logout-logs/verify-resumed-source.log). The normal package build
has resumed using the existing object files with two jobs.

## Package provenance and build

Candidate recipe: `kwin 6.7.4-7.1`, based on the exact Arch `6.7.4-7` tag,
commit `6b8447cb35fa06d80604e59ffa601adeb9dc43c7`.
The [original recipe](kwin-logout-logs/PKGBUILD.upstream) hashes to
`854a215b99879801b8acf5c69f4fddfb3ad3575c9e397b23cee3ef06a88bc95a`,
matching the installed package's `.BUILDINFO` record.
The [candidate recipe](kwin-logout-logs/PKGBUILD.candidate) retains dependencies,
the existing upstream backport and package capabilities, adding the local patch,
release suffix and a two-job build limit. No host package was installed/changed.

All source checksums pass. The release archive signature was verified using an
isolated build keyring, with signing subkey
`B3CB366552540BE06EE9AD9711968C44928CAEFC` under the recipe-approved primary
`0AAC775BB6437A8D9AF7A3ACFE0784117FBCE11D`.
See [signature evidence](kwin-logout-logs/upstream-signature.log).
Revised patch SHA-256: `cb7aa8a798eea18c00b57b6415740e7edd72177bbe7119fc3d3c0c7f51343cd0`.

Build directory: `work/beta2-kwin-logout.vNSROm`. The resumed normal package build
completed successfully at 23:27:19 CEST with exit 0;
[full build log](kwin-logout-logs/full-package-build.log). `build.log` retains the
deliberately interrupted first attempt, not a spontaneous failure.

- Main archive: `kwin-6.7.4-7.1-x86_64.pkg.tar.zst`, 12,989,858 bytes.
- Archive SHA-256: `b5cd822104cd37e638da15e57df9d283f575b8ecb97d15b006f922ba67afb151`.
- Extracted `kwin_wayland` SHA-256: `cbccf07000527cf968d3de63339c3e94387ac8aeeaaac4a7f356f6850ee6930f`.
- The [ELF comparison](kwin-logout-logs/elf-needed-comparison.json) finds the same
  63 ELF paths and identical direct `DT_NEEDED` lists. Package dependencies are
  unchanged. This does not by itself prove runtime ABI compatibility.
- Archive metadata preserves root ownership, mode 0755 and byte-identical
  `security.capability` attributes on `kwin_wayland` relative to the original
  package. The subsequent normal guest install also reports `cap_sys_nice=ep`.
- The generated debug archive is not selected for installation.

The verified main archive was installed from the guest's read-only QA share
through normal `pacman -U`, without dependency/conflict overrides or a network
adapter. The [upgrade log](kwin-logout-logs/normal-upgrade.log) records exit 0,
all 2,256 files present, the exact candidate binary hash and the retained
scheduling capability. The before/after package lists differ only in KWin's
release. Evidence: `kwin-logout-upgrade.BA7LA4`, original boot
`a438e17d-958d-4ff3-b3fd-97a3c5162743`.
Normal `systemctl reboot` and password login succeeded. The
[post-reboot audit](kwin-logout-logs/candidate-boot.log) verifies boot
`cc7d27f6-4916-43db-b210-e88a1081ea43`, Wayland session 2, and the exact running
`/proc/683/exe` hash against the candidate archive. Shell PID 1000 and the KWin
and Plasma units are active with zero restarts; system/user failed-unit lists
are empty at the audit snapshot. The [new user journal](kwin-logout-logs/candidate-boot-user-journal.txt)
is retained, along with full current/previous system journals in
`kwin-candidate-boot.MB3lTc`. Previous shutdown records include DRM teardown
warnings; this is not a claim that every journal warning has disappeared.

The initial QA mount-command input landed in a restored Paint window before
the terminal was explicitly refocused; it did not execute in the terminal.
The command was re-entered after checking focus, and authentication was supplied
only at the observed sudo prompt. Shares mounted and the boot audit completed.
This input interruption is not counted as a passed application workflow.

The native deadline and cancellation checks below now pass. The current
17-archive next-build selection remains unchanged pending the remaining actions.

## Native deadline and cancellation replay, 9–10 September

On the verified candidate compositor, an unsaved 400×300 black V was drawn in
Paint. Start → shutdown arrow → Log Out showed the native save prompt; Cancel
kept the drawing open. The pending-app notification had no countdown, retained
its explicit actions, and listed Paint. The read-only observer recorded the
same boot, Wayland session 2, and process IDs/kernel start times before logout,
after document cancellation, and **219.24 real seconds after the cancel marker**:
shell `1000/5967`, compositor `683/5597`, Paint `1071/6021`.
Evidence directory: `kwin-logout-deadline.fJgsKU` on the offline QA result share.

The [before capture](kwin-logout-logs/a7-deadline-before-no-cursor.png) and
[past-deadline capture](kwin-logout-logs/a7-deadline-after-timeout.png) contain
identical image pixels at `(704,500)` with width 400 and height 300. After an
idle lock/unlock, **Cancel Logout** removed the pending notification. Paint
remained open, and its native PNG Save dialog saved
[preserved-drawing.png](kwin-logout-logs/preserved-drawing.png). All **120,000
RGB pixels** match the original screenshot region (3,862 dark pixels). File
SHA-256: `6d74d6c0b0c80f227b55a7f00208456efbb5e7d17b5a4ddb6d8f419645fc579a`.
The [saved state](kwin-logout-logs/a7-deadline-saved.png) has no unsaved marker.
`kwin-actions-cancel-saved.bxI8hY` confirms the same session and active shell,
KWin and Plasma units with zero restarts and no failed units at 23:58:57 CEST.

A further QA-only horizontal stroke made the drawing unsaved again. A second
Start-menu logout request produced a fresh save prompt and notification.
After cancelling Paint's prompt, closing the notification with **×** removed
the request without ending the session. `kwin-actions-notification-dismissed.UHlqbt`
at 00:01:21 CEST on 10 September confirms the same boot/session/unit identities
and no failed units. A third logout request worked, demonstrating that neither
cancellation route left the operation stuck in progress.

For late completion, the third request was left pending until its notification
appeared. After cancelling the document prompt, the native Save As dialog wrote
[late-completion.png](kwin-logout-logs/late-completion.png) without replacing the
first proof image. All 120,000 pixels match the modified drawing capture;
SHA-256 `96ee216cb6df593a3ff2c1224d8b1ea2db4463861f78de4a6a92a8ff06a2dd50`.
The [saved app and pending notification](kwin-logout-logs/a7-late-saved-pending.png)
remained visible together. Closing Paint, the last pending app, then completed
logout and returned to [SDDM](kwin-logout-logs/a7-late-logout-result.png).
Password login opened session 5 in the same boot. The
[audit](kwin-logout-logs/late-completion-login.log) records new shell/KWin/Plasma
identities, active units with zero restarts, and no failed units. The
[journal](kwin-logout-logs/native-actions-user-journal.txt) shows normal Plasma
and compositor stops at 00:03:20 without a stop timeout in this transition.
It still contains unrelated startup/asset warnings; this is not a globally
warning-free journal claim.

## Explicit override, 10 September

In session 5, a new unnamed, disposable QA drawing was made. Start-menu logout
produced the expected prompt; Cancel left the drawing open alongside the
[pending notification](kwin-logout-logs/a7-override-before-action.png). Clicking
**Log Out Anyway**, and not simply waiting, ended that session and returned to
[SDDM](kwin-logout-logs/a7-override-result.png). Only this unsaved test stroke was
discarded. Both earlier saved PNGs retain their verified hashes.

Password login opened session 8 in the same boot. The
[post-override audit](kwin-logout-logs/override-login.log) has active shell/KWin/
Plasma units, zero restarts and no failed units at the new-session snapshot.
The [full journal](kwin-logout-logs/native-override-user-journal.txt) explicitly
records the previous Paint process losing its Wayland connection and exiting
with status 1 when the compositor stopped. That is part of this requested
unsaved-app abandonment, not a clean app save/close result, and is not hidden
by the new session's clean failed-unit list. Plasma and KWin themselves stopped
normally at 00:07:32–33 with no stop timeout in this transition.

## Required follow-up

- Preserve the completed build/metadata evidence and verify the installed runtime.
- Use the verified post-upgrade/reboot compositor for the following native checks.
- Deadline survival, Cancel Logout, notification dismissal and repeated requests
  pass with the real Paint document; retain the pixel and identity evidence.
- Native late-completion/override and their post-login logs now pass within
  their stated scope; repeat normal power-off/relaunch before integration.
- Recheck normal logout/power-off and update package selection only after passing.

The prepared [guest deadline observer](../../scripts/audit-kwin-logout-deadline.sh)
records boot/session IDs and the process IDs plus kernel start times of KWin,
the Aero7 shell and Paint. It requires the candidate package, the disconnected
QA hostname and Wayland. Record `begin` before logout, `mark-after-cancel` after
the native document Cancel action, and `finish` at least 150 real seconds later.
It compares all identities and captures unit states and journals; it neither
starts logout nor treats process survival as proof of preserved document pixels.
The native drawing must still be inspected, saved and checked independently.
The observer passes Bash syntax and ShellCheck and its native execution passes.
Its process ownership check reads the real UID in `/proc/PID/status`, rather than
the proc-directory owner, because protected user processes can have root-owned
proc directories. No process protection was changed.
The full ISO source checker also passes with the new observer present: all 149
Python tests, selected-package identities/hashes, QML/Bash checks, approved
branding, Shell pin and ShellCheck. The run is retained in
`work/beta2-kwin-logout.vNSROm/iso-check-deadline-observer.log`. These checks do
not themselves execute the guest observer or validate the native logout flow.
After the real replay and UID-observer correction, the full checker passes
again, including all 149 Python tests, package identities/hashes, static/QML
checks and ShellCheck. The new run is
`work/beta2-kwin-logout.vNSROm/iso-check-native-actions.log` (exit 0).

The matching prepared Plasma Workspace 6.7.4 source sets the KWin session call's
D-Bus timeout to `INT32_MAX`; a false or invalid reply calls `resetLogout()` and
`logoutCancelled()`. This source inspection supports testing a prolonged wait
without changing the caller, but is not a substitute for the real session test.
The later offline update-check failure remains visible in the baseline: the
notification-only checker deliberately returns failure when repository
availability is unknown, rather than reporting zero updates. No service status
was reset and no offline result was relabelled as up to date.

The older ordinary lifecycle pass remains valid for its stated scope. It never
tested this unsaved-work interaction and must not be used to close this hold.

## Normal power-off and cold start, 10 September

After the native logout checks, Start → Shut Down powered off the guest without
QMP force-off or killing QEMU. The old QEMU process exited and the disk had no
open owner before the existing-disk launcher was used for a cold start. The
previous system journal records Plasma/KWin stopped at 00:24:43 CEST and
System Power Off completed at 00:24:44. No stop timeout appears in this shutdown.
Power-profile QML warnings during service teardown remain in the retained
[system journal](kwin-logout-logs/poweroff-system-journal.txt).

Normal SDDM password login produces boot
`dcf96047-1c04-4efa-8bbd-5317c1fe084b`, session 2. At 00:29:16,
`kwin-candidate-boot.zN5g8t` verifies compositor PID 684 against the exact candidate
binary hash, the retained capability, all 2,256 package paths, active desktop
units, zero restarts and zero failed units in that snapshot. The
[cold-boot audit](kwin-logout-logs/coldboot-after-poweroff.log) exits successfully.
The pre-shutdown snapshot preserves the intentionally disconnected update-check
failure; this was not reset or relabelled as a successful update check.

This completes the scoped power-off/relaunch check for this KWin candidate.
It does not establish final-image acceptance, multi-monitor/suspend coverage or
a universal fix for the older intermittent service-stop issue. Next-build
package integration is still pending; no ISO or publication was produced.
