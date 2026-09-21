# Installed screenshot recovery — release 50

Date: 8 September 2026. Status: **installed crash, cancellation, queue, save,
reboot and existing-shortcut checks passed; final-media acceptance remains open**.

This follows the rejected release-48 focus-handoff result and release-49 stale
Escape registration after a forced crash. Their failures remain documented in
[the earlier evidence](2026-09-08-snipping-early-cancel.md), including the late
PNG found after the old crash fixture had finished its bounded snapshot.

## Package identity

- Package: `aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-50-x86_64.pkg.tar.zst`
- Bytes: `5152679`
- SHA-256: `20cedc5da7bc59a1d7f4d36566f2b373045d67772004f27ffb5d2e5e24245889`
- Installed helper SHA-256: `4947eb3d33c4378d1ec4747452fbe3ac2d6320e71369bb52648158984c46f032`
- Consolidated patch SHA-256: `8ff45827c8c525bf58477ea2303d42b08c0a7a58bf30213864caf02ad7021d02`
- Restart drop-in SHA-256: `45685f807818b338fbde0c1816e376e2318c1db5d49ca2319b4d7b788210fa39`

Clean build finished at 18:28:43 CEST. All 17 CTest groups and ten isolated
greeter cases passed, as did the archive branding/repeated-setup verifier.
The prepared helper source exactly matched the maintained tree. All eleven ELF
files retained their direct library requirements relative to release 47. The
only new non-ELF payload is the narrowly scoped screenshot-service restart
drop-in; existing artwork/configuration assets are unchanged. Package metadata
and rebuilt ELF bytes differ. Upstream warnings/build-directory references are
retained, not treated as a warning-free build.

## Real installed checks

The r10 offline guest stayed on Wayland at 1920 by 1080 with `-nic none`. Normal
upgrade changed only the theme package from 49 to 50. All 1,147 package paths
were present. The running normal helper used `/usr/bin/aero7-snipping-tool`,
without a candidate executable or backend override.

The installed audit verified the drop-in at
`/usr/lib/systemd/user/app-org.aero7.snippingtool@autostart.service.d/snipping-recovery.conf`
and the live service settings `Restart=on-failure`, `RestartUSec=1s`. These were
the installed unit's settings, not properties added by a transient test unit.

### Forced crash and subsequent Escape

`theme50-crash.LdiHz3` started a real capture, then sent SIGKILL to the exact
normal capture unit at 18:31:13. No manual start occurred before checking
recovery. The service restarted automatically once, with replacement PID 7101
and `NRestarts=1`. The independent observer recorded the capture binding being
released at 18:31:14.856. It then observed all four later captures acquire and
release Escape at 50/300/650/1,250 ms. The corresponding pre-recovery frames
were clear, PNG inventories matched, and no backend child remained. The
replacement helper PID stayed unchanged throughout those four attempts.

The journal retains the deliberate SIGKILL and earlier-session messages. Those
are not unexplained production crashes or proof that the whole journal is clean.

### Queue and repeated cancellation

The normal installed helper received three closely spaced shortcut presses.
One Escape cancelled them without a queued selector reopening. A second case
pressed Escape and then started a new snip 80 ms later: the new selector stayed
visible beyond the old capture's 500 ms kill deadline, and a separate Escape
closed it. The recorded frame expectations deliberately differ for the new
active selector and the two cancelled states.

A further ten attempts repeated 50/300/650/1,250/1,800 ms twice. All ten
pre-recovery frames matched the verified idle toolbar regions. Fixture
`theme50-cancel.0RY37U` retained the same helper PID, unchanged PNG inventory
and no backend child. This is a bounded timing/queue replay, not proof of every
possible input ordering or multi-monitor behavior.

### Save, notification and clipboard preservation

The actual Meta+Shift+S workflow saved
`Screenshot 2026-09-08 18.35.18.018-557267.png` (342 by 202 pixels, SHA-256
`0662c1958b026f256e83423e97c8b870aa7c7df42d629db7ec3dc48bffc6b2bc`).
The selection overlay closed and a Screenshot saved notification appeared,
with no editor/main window. Clicking its body opened this file in the default
image viewer. A later snip was cancelled with Escape at 1,250 ms; the original
image still pasted into a fresh, empty Paint document with Ctrl+V, at the same
342 by 202 selection dimensions. This confirms actual image paste and visual
clipboard preservation for that cancellation, not a new pixel-by-pixel test.
The scratch Paint document was discarded and the saved original retained.
The saved-file audit recorded `wl-paste` as unavailable, so there is no claim of
a separate command-line clipboard hash.

### Normal reboot and shortcut collision

Normal reboot reached the greeter and a password login. A subsequent idle lock
and unlock showed the complete logo. Boot ID
`0a7d81de-d7f9-489d-b935-45a8625112f1` differs from the pre-reboot audit.
`theme50-reboot.log` verified the normal installed executable, both active
desktop/helper services, the installed recovery drop-in, and `NRestarts=0`.
Both failed-unit lists were empty. Missing offline repository databases and the
separate empty app-ID portal warning remain in the journal; they are not hidden.

Fixture `theme50-cancel.1viwlB` passed four post-reboot Escape timings at
50/300/650/1,250 ms: every pre-recovery toolbar comparison matched idle, the
saved PNG inventory stayed unchanged, the helper PID remained stable and no
backend child survived. The first host comparison used an incorrect baseline
path and did not run; the corrected comparison used the inspected post-reboot
idle frame `276-theme50-terminal.png`, with zero changed pixels in both regions.

The normally installed helper also passed the existing-Escape collision test.
The independent observer retained `aero7-escape-binding-qa/qaExistingEscape`,
recorded its actual activation and exited successfully. Escape deliberately
left the selector visible, proving the existing action won; a separate mouse
Cancel then closed it. PNG lists remained identical and the normal helper PID
was unchanged, with no backend child. `theme50-post-collision.log` confirmed
that no temporary helper or backend override remained active afterwards.

## Remaining boundaries

Logs, fixtures, input timestamps and selected unedited frames are preserved in
`snipping-installed-recovery-logs/` beside this report. The normal post-reboot
checks are separate from the later
[portal-identity source candidate](2026-09-08-snipping-portal-identity.md).

Broader desktop startup/app-ID warnings, credential-store integration, storage
and compatibility coverage, and both exact final images remain separate gates.
The frozen r10 ISOs have not been changed, signed or published by this pass.
