# Combined-stack lock, logout and power-off validation

9 September 2026. Local QA only. No new package, ISO, commit, push or publication.

## Tested installation

The existing disconnected r10 offline VM, after the
[combined package transaction](2026-09-09-aligned-stack-offline-validation.md):
Desktop 0.2.0-32, Theme release 57, Plasma Workspace 6.7.4-3.2 and UAC release 2.
Wayland, one 1920×1080 display, 6 GiB RAM, two virtual CPUs and no network device.
The vault remained uninstalled; this does not test shutdown with an unlocked vault.

## Observed results

1. **Lock and retry:** Meta+L opened the branded lock screen. One deliberately
   wrong password was rejected with “The user name or password is incorrect.”
   Clicking OK returned to the password form. The valid QA password unlocked
   the existing desktop. Branding remained fully visible in both screens.
   The journal records the expected authentication rejection, not an unexpected
   service failure.
2. **Native logout:** Start → shutdown arrow → Log Out returned to SDDM.
   A valid password opened a new graphical session in the same boot. Session ID
   changed from 2 to 5 and the old shell/authentication processes were replaced.
   Plasma stopping was recorded at 22:26:11 and stopped at 22:26:12. No stop
   timeout was recorded. The terminal was restored by the existing session
   restoration setting; no user preference was changed.
3. **Native power-off:** Start → Shut down at 22:27:37 stopped Plasma within
   that same recorded second and reached System Power Off at 22:27:38. At the
   22:27:48 host check, the original QEMU PID 151755, its QMP socket and its disk
   file handle were gone. No reset, forced kill or host power command was used.
4. **Power-on:** The existing guarded launcher verified the unchanged ISO hash
   and absence of another QEMU guest before starting the same installed disk.
   SDDM and normal password login passed. Boot ID changed from
   `6fad1672-bbcc-4e5a-ad24-fdb019554f03` to
   `a438e17d-958d-4ff3-b3fd-97a3c5162743`.
5. **Service audit:** Before testing, after logout/login and after power-on,
   Aero7 Shell, Plasma Shell and the authentication agent were active with zero
   restarts. Failed system/user unit lists were empty. Package versions remained
   unchanged. The post-power-on user journal contains no observed ReferenceError,
   binding-loop, exit-code-255 or stop-SIGTERM timeout match.

## Evidence and limits

- [Baseline services and session](session-lifecycle-logs/before.log)
- [After native logout/login](session-lifecycle-logs/after-logout.log)
- [After power-on](session-lifecycle-logs/after-poweron.log)
- [Full user journal covering lock, logout and shutdown](session-lifecycle-logs/logout-and-shutdown-user-journal.txt)
- [Wrong-password feedback, 1920×1080](session-lifecycle-logs/wrong-password.png)
- [SDDM after logout, 1920×1080](session-lifecycle-logs/logged-out.png)

Full system journals remain in
`/home/admin/VMs/aero7-beta2-r10-oTmJ9G/offline/results/session-after-poweron.e8zop2`.
Snapshots before and after logout are in siblings `session-before.6XcDpF` and
`session-after-logout.lNSaYD`. The guarded capture script is
`/home/admin/VMs/aero7-beta2-r10-oTmJ9G/inputs/audit-session-lifecycle.sh`; Bash
syntax and ShellCheck pass.

The earlier intermittent Plasma shutdown timeout **did not reproduce** in this
logout/power-off sequence. This is evidence for these exact workflows, not proof
of a universal fix. Virtual graphics/power-device and app-ID diagnostics remain;
the earlier virtual CPU clocksource warning is also preserved in the old boot.
An intentionally rejected password must not be counted as a regression.

No unsaved-document shutdown inhibitor, suspend/resume, unlocked-vault logout,
multi-user or multi-monitor lifecycle was tested here. Those limitations and
final fresh-image acceptance remain separate. These are upgraded-guest evidence
screenshots, not approved final release gallery assets.
