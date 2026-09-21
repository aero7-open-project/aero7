# Aligned package stack — offline upgrade and reboot

9 September 2026. Local QA only; no final ISO, commit, push or publication.

## Scope and result

**PASS for the combined required-package upgrade/reinstall and observed reboot.**
The existing r10 offline QA installation received all 15 required packages from
the [aligned selection](2026-09-09-next-build-package-alignment.md) in one normal
`pacman -U --noconfirm` transaction. QEMU had no network device; only loopback
existed in the guest. No dependency, file-conflict or signature-policy bypass
was supplied. This was an already modified QA installation, not a fresh install
or a replay of each intermediate installer transaction.

All 17 archive hashes and the three selection-list hashes matched. Control Panel,
Theme, Desktop and UAC upgraded; the other 11 required packages reinstalled at
the selected versions. The transaction and its five hooks completed. Every
required package passed installed-version and missing-file checks.

Programs Center Beta release 3 was already enabled in this guest and stayed
enabled. Credential Vault remained absent. Both optional archives were cached
with matching checksums without being added to the required transaction.

## Reboot and graphical checks

- A normal reboot reached SDDM, followed by password login into Aero7 at
  1920×1080 on Wayland. No reset or forced process termination was used.
- Boot changed from `9a5dbb61-30bf-4e10-90fc-724fff44f76d` to
  `6fad1672-bbcc-4e5a-ad24-fdb019554f03`.
- Required installed versions and file checks passed again after reboot.
- Zero failed system units and zero failed user units were listed. Aero7 Shell
  was active with zero restarts. The Aero and Plasma authentication service
  names resolved to the same active unit/PID, also with zero restarts.
- Effective wallet configuration remained `Enabled=false`; the runtime KDE
  portal configuration retained `org.freedesktop.impl.portal.Secret=none`.
- Firewalld was active, the recorded firewall backend was `firewalld`, and the
  existing update preference remained `recommended`. This checks persistence,
  not packet filtering or update approval interactions.
- All 59 installed File Explorer common-dialog QtTest results passed on Wayland
  with zero failures/skips. The test and installed shared-library hashes matched
  the previously validated Explorer 54 artifacts.
- Clicking the File Explorer taskbar pin opened the branded application.
- **Turn Aero7 features on or off** displayed **Encrypted Credential Vault**
  unchecked and **Not installed**, while the previously enabled Programs Center
  remained checked. No optional feature was toggled during this replay.

## Log findings and limits

The observed shutdown stopped Plasma and the session within the recorded
22:13:39–22:13:40 interval, with no service stop timeout in those journals.
One successful shutdown does not close the earlier intermittent timeout gate.

The pre-upgrade boot contains the older KWallet portal exit-code-255 failure;
the post-upgrade boot audit does not reproduce it. Startup logs still contain
virtual graphics/software-rendering fallback diagnostics, missing optional
ModemManager and unsupported virtual power/backlight diagnostics, helper app-ID
metadata warnings, and the protected authentication agent's portal-registration
warning. Both boots also contain a virtual CPU clocksource watchdog read timeout.
These logs are not warning-free; no security setting was weakened to hide them.

Pacman reports absent repository sync databases in this disconnected guest.
Those warnings did not prevent the local archive transaction. The expected
package-not-found query for the disabled vault is retained in the audit.

Final fresh online/offline installer sequencing, broader desktop/recovery and
vault security checks remain open. Frozen r10 media was not rebuilt or changed.

## Evidence

- [Combined transaction](aligned-stack-logs/upgrade.log)
- [Post-reboot audit](aligned-stack-logs/reboot-audit.log)
- [Installed dialog suite](aligned-stack-logs/explorer-dialogs.log)
- [Optional features, 1920×1080](aligned-stack-logs/optional-features.png)
- [Taskbar Explorer launch, 1920×1080](aligned-stack-logs/taskbar-explorer.png)

Full current/previous system and user journals remain in the local QA directory
`/home/admin/VMs/aero7-beta2-r10-oTmJ9G/offline/results/aligned-stack-boot.vViepx`.
The transaction is retained in sibling `aligned-stack-upgrade.s0qIzF`, and the
dialog replay in `explorer54-dialog.z0t3e1`. Screenshots are engineering evidence
from an upgraded test guest, not final release gallery assets.
