# Screenshot helper portal identity — 8 September 2026

Status: source candidate and installed package 51 verified for capture, crash
recovery and post-reboot cancellation. A distinct cold-login portal warning
remains under investigation. This is not final-media acceptance or publication.

## Cause and correction

The normal installed release-50 helper repeatedly logged an empty application
ID at login: `Could not register app ID: App info not found for ''`.
Its entry point set the executable/application name but not its desktop-file ID.

Qt's [desktopFileName documentation](https://doc.qt.io/qt-6/qguiapplication.html#desktopFileName-prop)
requires the base name of the matching desktop entry, without path or extension.
The [Qt portal implementation](https://github.com/qt/qtbase/blob/v6.10.2/src/gui/platform/unix/qdesktopunixservices.cpp)
passes that property to the host portal registry. The helper now sets
`org.aero7.snippingtool` before window-icon, window or clipboard initialization.
This matches its shipped application desktop file. No portal is disabled, no
warning filter is installed, and no icon artwork or launcher name is changed.

## Source and runtime evidence

- Candidate executable SHA-256:
  `9b375c7d74f24e2f53bf6924621653a4020828878d5aee5215b6b58fe91004ff`.
- Six focused CTest groups passed. The new source-order/desktop-entry guard is
  deliberately not represented as a runtime portal test.
- The existing VM fixture temporarily ran the candidate as an unprivileged
  user service with debug logging enabled for Qt's services category.
- Fixture `snipping-focus.2BwRBu`, invocation
  `4b2a1b17f58d4c1bb08698cd4af99c68`, recorded the positive result:
  `Successfully registered with host portal as "org.aero7.snippingtool"`.
- Actual Meta+Shift+S capture saved three 342 by 202 PNGs. The saved notification
  and closed overlay were inspected. A timely notification-body click opened
  `Screenshot 2026-09-08 18.55.18.329-2d5915.png` in the default image viewer.
  Its SHA-256 is `99c27351e7d2257ecf4e8e984870b7e402cf9014fe0ec9d79a04a8f1e3d83d1f`.
- An earlier click produced no viewer: the notification had expired before the
  manual action. That attempt is not counted as a successful opening. The
  later timed replay records the actual viewer and launch in the journal.
- Escape at 1,250 ms closed a subsequent capture. The fixture restored the
  normal installed helper with status 0 and left both installed binary hashes
  unchanged. Its blank Enter is labelled `timeout` by the old fixture formatter;
  this is not evidence that the four-minute timeout fired.

The saved-image inventory contains the three deliberate new captures, not a
claim that this save-mode fixture kept the complete inventory unchanged.
This candidate has not yet had a separate clipboard pixel-comparison replay.
An additional check after the fixture stopped the candidate and restored the
normal helper found that a newly opened Paint document could not paste the
image (frames 286–288). The PNGs remained saved. Clipboard persistence across
helper termination is therefore an open lifecycle issue; this does not negate
the earlier live-helper cancellation/paste proof, nor establish its cause yet.
Paint was also not ready at the first 3.5-second observation but was visible at
the later observation; exact startup timing and the cause still need tracing.
Spectacle's inherited QML `focusPolicy` shadow warnings remain and are preserved.

Package inputs: `work/beta2-theme51.JZf9zv`, with the release-50 recovery patch
unchanged and an additional portal-identity patch SHA-256
`5ce5528a2bd56c5e8795a8481a2d0afd1163b0a5b754cc0182846bd647003d4c`.
## Package and normal-install follow-up

Package 51 finished at 19:02:50 CEST, with 18/18 CTest groups and 10/10 isolated
greeter checks passing. Branding/repeated-setup verification passed. All 11 ELF
direct-library requirement sets matched release 50; all non-ELF payload assets
were unchanged (package metadata and rebuilt ELF bytes differ). The prepared
Snipping Tool source exactly matched the maintained source tree. Build warnings
and embedded build-directory references are retained.

- Package bytes: `5152449`.
- Package SHA-256: `0e05d85e1ce6b2cc008693478e89f659ba69500f4751f95ff6e353396bc08d41`.
- Installed helper SHA-256: `b8773ea8ae4a830ecd1703dd4d7a71b461bf182bdd660f7437ecdf147cc886bc`.

The normal offline upgrade changed only theme 50 to 51. All 1,147 paths were
present. A normal-service SIGKILL at 19:05:18 automatically restarted the helper
once to PID 7962; Escape ownership became free at 19:05:19.960. Four subsequent
timing checks passed with matched PNG inventories, stable replacement PID,
no backend child and observed acquisition/release of the internal Escape action.

Normal reboot/login reached boot `0b42e8f7-bbe3-4d7b-a101-b6cc95d0caa3` with both
services active, the installed drop-in in use and `NRestarts=0`. Four further
50/300/650/1,250 ms timing checks passed without changing PNGs or leaving a child.
The real post-reboot capture saved a 342 by 202 PNG and showed a saved notification;
its body opened `Screenshot 2026-09-08 19.10.54.414-0e42af.png` in the default viewer.
Actual Ctrl+V then pasted this screenshot as a 342 by 202 image into a fresh,
empty Paint document (frame 298). The scratch document was discarded, leaving
the original PNG saved. This is a live-helper image-paste check, not a new
pixel-by-pixel comparison or proof of persistence after helper termination.

The initial empty-ID error is absent from this boot, but the normal login log
contains `Connection already associated with an application ID`. This is a
different registration-lifecycle issue, not proof of a warning-free startup.
Qt 6.11.2's registration function sets its shared success flag only after an
asynchronous reply and has both a queued registration and a service-registration
watcher; overlapping calls are a hypothesis to trace, not yet an established
cause. The successful source-candidate registration used an already-running
portal and does not prove the cold-login path. Do not suppress the warning or
declare all portal failures resolved.

The local package recipe and `.SRCINFO` now match the tested release-51 inputs.
No commit, signed-repository promotion, final ISO selection or publication.

## Portal-activation trace follow-up

Controlled portal activation at 19:33:03 reproduced the duplicate warning with
the normally installed release-51 helper, PID 7771, invocation
`4bf792e7c48e4fa190ac65f83b42ef35`. Fixture `snipping-portal-start.zQvkFO`
stopped only the screenshot helper and frontend portal in the idle QA guest,
monitored Registry calls/portal ownership changes, and restarted the helper.
It restored both normal services active, status 0, with no configuration changes.

The same client `:1.697` sent two Register calls for `org.aero7.snippingtool`:
serial 34 at `1788888783.393685`, serial 38 at `1788888783.394400` (715 microseconds
apart). The captured bus-owner list maps that client to PID 7771. The helper
journal then recorded `Connection already associated with an application ID`.
This establishes duplicate client registration during portal activation, not an
invalid Aero7 desktop ID. The trace deliberately did not record unrelated D-Bus
method-return payloads. A precise Qt in-flight guard and portal-restart lifecycle
test remain to be implemented; no warning is hidden. A different client with an
empty ID was identified as the Action Center, PID 999, and needs its own audit.
