# Combined selected-stack reboot — 13 September 2026

Local acceptance evidence only. No commit, publication or final ISO build.

## Scope and result

The existing r10 offline test installation was upgraded with the selected
corrections, then restarted through the normal Start-menu Restart action.
It returned through [SDDM](stack-20260913-logs/a7-stack-cold-sddm.png), password
login and the [desktop](stack-20260913-logs/a7-stack-cold-desktop.png).
This is a normal reboot of an upgraded VM, not a power-off/cold-start or a fresh
installation of a newly built image. The guest has no network adapter.

The [audit](stack-20260913-logs/reboot/audit.log) exits zero at 19:22 CEST.
Boot ID `b4d20d4c-2122-454c-b361-fb67d20c63de` differs from the previous
`fde6a493-c3b9-459c-a5c9-47f8afe5cb9c`; the active Wayland session is 2.

- All [16 required package versions](stack-20260913-logs/stack-20260913-required-versions.txt)
  match and their installed-file checks report no missing files.
- Running Gadgets PID 1012 matches the selected release-25 executable hash.
- KWin wrapper 675, actual compositor 679 and its mapped `libkwin` match
  release 7.3. The mapped inode matches the installed library; no deleted old
  library is used. Permission checks remain enabled and capabilities unchanged.
- Shell 999, Plasma 796 and KWin are active with zero service restarts.
  Both authentication-agent unit names resolve to the same PID 835.
- Failed user/system unit lists are empty at this checkpoint.
- Firewalld is active and remains the selected backend. Update preference is
  `recommended`; the audit does not initiate or approve an update.
- Credential Vault is absent, KWallet is disabled and the Secret portal remains
  disabled by the session policy. Cached optional Programs Center and Vault
  archives match their expected hashes. Programs Center remains installed from
  the earlier optional-feature test; this is not a fresh-default assertion.
- Aero7Light is selected. The gadget account layout is byte-identical to the
  prior release-25 logout/login baseline (`gadgets25-login.r5VFGm`).

## Journal findings

The full [current system journal](stack-20260913-logs/reboot/system-journal.txt),
[user journal](stack-20260913-logs/reboot/user-journal.txt) and
[previous system journal](stack-20260913-logs/reboot/previous-system-journal.txt)
are retained. The prior boot reaches reboot and journal shutdown at 19:16:11;
the next kernel starts at 19:16:19. No compositor/shell crash or service restart
is reported in this new-boot audit. This does **not** mean warning-free logs.

Remaining messages include virtual graphics/EGL software fallback, XKB symbol
warnings, unavailable optional ModemManager/systemd-homed, and unsupported
virtual battery/backlight controls. Auxiliary KDE helpers report missing portal
app-ID metadata; the protected authentication agent reports inability to open
its process root. These match categories already recorded in the
[earlier combined-stack audit](2026-09-09-aligned-stack-offline-validation.md).
No process protection or portal permission checks were weakened to hide them.
The virtual CPU also reports a feature dependency warning and a clocksource
watchdog read timeout. Physical CPU/GPU behavior is not proven by this VM.

Pacman warns that repository sync databases are absent in this disconnected
test guest. Exact installed versions, file presence and cached archive hashes
are nevertheless checked locally. The vault package-not-found message is the
expected negative assertion, not an installation failure.

## Boundaries

This closes the combined normal-reboot check for the selected 16-package stack,
not final-media acceptance, physical hotplug/driver testing, or every possible
failure path. The existing online/offline ISOs are unchanged. Current package
selection remains Gadgets 25 / Control Panel 54 / KWin 7.3, with manifest SHA-256
`8fcbc92a719570c6bc101b9e169e6766a618c43e5d34783c33f70615ee198f80`.
The [guarded audit script](stack-20260913-logs/audit-stack-20260913-boot.sh),
package inventory, output state and process maps are retained with the logs.
