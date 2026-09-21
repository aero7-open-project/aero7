# Beta 2 r5 fresh-image acceptance — 6 September 2026

Status: **r5 fresh OOBE failed; adapter and firewall-status fixes verified in a
manually repaired guest; r7 replacement media required. Not approved for release.**

## Latest checkpoint: r44 firewall authorization repair

The packaged firewalld 2.5.1 server authenticates its state-property read with
the configuration action. Calling `firewall-cmd --state` from Control Panel and
Action Center therefore caused timeouts and recurring authentication failures.
The package's server policy separately requires authentication for configuration
information such as the denied-packet logging setting. These were two distinct
causes; allowing the broad configuration action is not the solution.

Control Panel r44 queries the active systemd state and a successful default-zone
read instead of the authenticated property. Fresh installation now writes a
narrow polkit rule allowing only the three exact information actions for local,
active sessions. Configuration/all actions retain their existing authorization
requirements. Existing UFW installations and differing administrator policy
files are preserved. CLI links for Firewall and network status were also routed
to their actual Control Panel pages instead of falling back to Home.

Validation completed in the recovered r5 guest, not on final media:

- Real unprivileged information queries returned in about 0.3 seconds. Actual
  pkcheck results allowed information and required administrator authentication
  for all/config/direct/policies modifications.
- Both IPv4 and IPv6 post-reboot packet probes passed: unsolicited incoming
  traffic blocked, outgoing traffic and replies allowed.
- Authenticated offline upgrade to `linux-control-panel 0.1.0-44` passed;
  all 73 package files were present.
- Screenshot `41-r44-firewall-status.png` shows the Firewall page and On state.
  Screenshot `42-firewall-disable-confirmation.png` shows its confirmation;
  selecting No kept the service active and running.
- From 15:29 to 15:35 the restarted Action Center remained running; the journal
  contained no new firewall configuration authentication or account-lock
  failures. Evidence: `offline/results/r44-background-check.log` and
  `r44-background-journal.log`. This covers one five-minute polling interval,
  not indefinite stability.
- All 130 backend tests and all 16 Control Panel CTest groups passed. The
  read-only JavaScript policy also passed 37 local/active/action combinations.
  The local package build ran all 16 tests; its missing-host-dependency precheck
  was bypassed with `--nodeps`. It is unsigned QA output, not a clean signed
  release-builder artifact.

Final r44 package SHA-256:
`57094a6dd6ec018e383217f0440328ae2aa70b107ca93a7cdfa7096da6df61e9`.
Source archive SHA-256:
`0fe7f623c3d813437dce022aa7b005051fbc262cfdea00338d6d2021124394bf`.
Build evidence is in `work/beta2-firewall-info.LHxVb2/`.

Both r6 images completed assembly/export, but were already missing this later
firewall policy and r44 package. They are superseded QA artifacts and must not
be published or presented as accepted. Both r7 profiles completed preparation;
each reran all 130 backend tests and all three installer CTest groups. Isolated
assembly is running as `aero7-r7-builder.service`, offline then online. Its log
and outputs are under
`work/beta2-profiles.UWsuLM/builder-output/r7-firewall-status/`.
The host verification job checks the exported offline checksum and exact
embedded contents before starting a new no-NIC guest under
`/home/admin/VMs/aero7-beta2-r7-xGDR49/`. RAM and disk guards stop launch if
resources are insufficient. A queued job is not a successful build or test.
Screenshot `45-r44-network-status.png` additionally confirms the repaired
network-status command opens Network Settings in the recovered guest.
The recovered r5 guest was then shut down through Start > Shut down at 15:41:51.
Its QMP socket and QEMU process disappeared within seconds; no delayed-close
dialog was observed. This is one successful graphical shutdown, not enough to
close the earlier intermittent r4 shutdown warning. Repeat on fresh r7 media.
No commits, pushes, signing, repository promotion or ISO publication occurred.

The preceding turn made progress: Control Panel r43 passed an authenticated
offline upgrade with UFW preserved, its corrected settings link was exercised,
both profiles completed preparation, and isolated ISO assembly started. Those
upgraded-guest results do not establish fresh-image acceptance.

## Exact build and test locations

- Builder VM: `/home/admin/VMs/aero7-beta2-builder.HD2BwR/`, standalone copy of
  the stopped r4 online disk; original preserved.
- Local build output: `work/beta2-profiles.UWsuLM/builder-output/`.
- Offline service: `aero7-isolated-builder.service` in the builder guest.
- Online service: `aero7-online-builder.service`, waits for successful offline
  build/export before replacing the guest profile and building online.
- Fresh test root: `/home/admin/VMs/aero7-beta2-r5-oz8Pm4/`.
- Test VMs will use new 64 GiB disks, 1920×1080 display, 6 GiB RAM and two vCPUs.
  Offline has no NIC; online has user-mode NAT. Test input is a read-only 9p
  share, and output is restricted to each VM's dedicated results directory.
  This instrumentation does not modify the installation ISO.

During assembly, a guest process query confirmed
`mksquashfs` alive at about 192% CPU after seven minutes; progress subsequently
advanced from 27% to 49%. This is verified running work, not a presumed hang.
The later results below supersede this build-progress checkpoint.

The host `verify-and-start-offline.sh` job is now waiting for the builder's
explicit successful-export marker. It will independently check the returned
checksum, run the exact embedded-content verifier, and only then launch the
fresh no-NIC guest. A failed builder or verifier stops that sequence. The job
does not treat an observation timeout as proof that the VM itself stopped.

The Network location screen also passed a local Qt software-render layout
inspection at 1024×768 and 800×600. All three choices and the new Public-fallback
paragraph fit without clipped text. Images and empty-error render logs are in
`work/beta2-profiles.UWsuLM/network-screen-*.png` and `network-render*.log`.
They retain the visible simulation banner and are not fresh-VM screenshots or
proof of backend behavior. No icons were replaced or generated.

## Newly observed shutdown issue to reproduce

The upgraded r4 offline guest displayed the normal session menu after an ACPI
power-button event. Choosing its shutdown control then produced a notification
that **Plasma did not close**, with a two-minute logout timeout. QEMU eventually
exited, confirmed by the absence of PID 9885. No force-kill was used.

Evidence: `offline/139-shutdown-state.png` and `offline/140-power-menu.png` under
`/home/admin/VMs/aero7-beta2-r4-Nlm227/`. This guest had undergone multiple manual
package upgrades and QA shell restarts. The cause is not yet established;
repeat on the fresh image before attributing it to a specific source change.
Do not count prompt, warning-free shutdown as passed.

## Required next evidence

- Complete both builds; independently verify returned checksums and exact
  embedded backend, manifest and package contents.
- Fresh no-NIC offline installation, nondefault regional settings, OOBE,
  firewalld Public fallback, initial desktop and normal reboot/login.
- Fresh online installation and OOBE with a per-connection network choice.
- Real IPv4/IPv6 packet filtering, persistent firewall state, Home/Work/Public
  changes, approved exceptions and existing-UFW preservation.
- Positive update notification and approval-before-install behavior, plus
  final-media on/off persistence and failure handling.
- Repeat desktop/application, Optional Features, screenshots, branding,
  recovery/multi-monitor and session-close checks on the final candidates.
- Update website handoff and final 1920×1080 screenshot inventory from actual
  accepted results. Publication/signing/promotion require separate approval.

No commit, push, signing, repository promotion, ISO upload or website
publication was performed during this continuation.

## Offline build verified and fresh guest started

The offline builder completed with exit 0 and its explicit successful-export
marker. Independent host checksum and exact embedded-content verification
passed, then the new no-NIC VM booted into the real installation UI.

- Filename: `aero7-beta2-offline-2026.09.06-x86_64.iso`
- Exact bytes: `3318059008`
- SHA-256: `b652c77920c15d6f6a33c45bebc784eb18c96a841c3395d130cd89615ce648ec`
- Location: `work/beta2-profiles.UWsuLM/builder-output/`
- Verifier log: `work/beta2-profiles.UWsuLM/verify-offline-r5.log`
- Guest: `/home/admin/VMs/aero7-beta2-r5-oz8Pm4/offline/`

The host verifier's separate package-policy loop still required UFW; this stale
rule was corrected before verification ran. The actual loop now requires
firewalld, pacman-contrib, fakeroot and libnotify and rejects UFW in the fresh
base list. A regression executes those real loops against the current list,
missing-dependency fixtures and a UFW-containing fixture; all six candidate
test cases pass. This change affects verification, not embedded ISO bytes.

The online build subsequently completed and passed exact embedded-content
verification (`work/beta2-profiles.UWsuLM/verify-online-r5.log`):

- Filename: `aero7-beta2-online-2026.09.06-x86_64.iso`
- Exact bytes: `1547751424`
- SHA-256: `dc70764e2a7372ccbfa707586e8d1274ca12cb7d8479ee7af944c134657f0dad`

These hashes identify superseded QA artifacts, not an approved release.

## Fresh offline first-run failure and isolated recovery

The real no-NIC installation completed and rebooted into OOBE. English UI,
Dutch regional formats and a US keyboard were selected. First-run setup stopped
at 62% in the pinned Shell's `40-plasma-wayland` stage. The actual command was
`systemctl enable ufw.service`; its error was `Unit ufw.service does not exist`.
Fresh firewalld preparation had already succeeded; the remaining UFW assumption
was in the pinned Shell service helper.

Evidence under `/home/admin/VMs/aero7-beta2-r5-oz8Pm4/offline/`:

- `16-oobe-finishing.png`: actual 62% setup failure.
- `results/live-installer.log`: successful base installation.
- `results/oobe-failed.log` and `results/shell-failed.log`: original failure.
- `results/backend-before-core-fix`: preserved original embedded backend.
- `results/retry-core-fix.log`: diagnostic OOBE retry completed to 100%.
- `results/installed-audit-core-fix.log`: selected package versions, Public
  runtime/permanent zones, enabled update timer, Dutch defaults, US keyboard,
  no NIC, no failed system services or current-boot coredumps at this checkpoint.
  All checked package files exist. IPv4 and IPv6 packet probes both verified
  blocked unsolicited inbound traffic and permitted outbound/reply traffic.

The ISO backend now owns the core-service step and skips only its pinned
UFW-specific counterpart. It calls the pinned package-policy function, enables
and validates NetworkManager and SDDM, activates only the explicitly selected
firewalld backend, and verifies it is enabled and active. Existing UFW setups
are not changed. No pinned Shell files were edited. All 128 backend tests and
three installer CTest groups pass; static checks pass with existing QML warnings.
Injected command failures stop the adapter instead of bypassing validation.

Only the failed disposable guest received a replacement backend. Its retry was
invoked through the backend with the same QA account and choices, not through
a fresh GUI flow. Home was chosen with no NIC, and the backend correctly retained
Public defaults. This proves recovery and packet behavior, **not acceptance of
unchanged installation media**. Both images must be rebuilt and retested fresh.
The replacement backend SHA-256 is
`5a125dfced6f89704e6b0d1d55e486e67c07ba158816fb88b5deda5afecfa09f`.

## Recovery reboot and new status-query issue

The recovered guest rebooted and reached its desktop. The login/lock branding
was complete, and the taskbar showed Dutch date/time formatting. Evidence:
`20-recovered-reboot.png`, `21-recovered-desktop.png` and
`22-recovered-terminal.png`. This remains a manually repaired guest.

Opening Control Panel > System and Security > Windows Firewall reported
**Unavailable**, with a DBus reply timeout also reproduced by the user's
`firewall-cmd --state`. Evidence: `26-firewalld-status.png` and
`28-firewall-query-result.png`. Do not infer that filtering stopped or that it
remained working after reboot; the post-reboot root/packet audit is pending.
An unprivileged systemd query subsequently confirmed `ActiveState=active` and
`SubState=running` (`32-firewalld-systemd-state.png`). This establishes the
service is running, not that every runtime rule passed the post-reboot probe.

Read-only inspection of the actual firewalld archive found its policy symlink
selects `org.fedoraproject.FirewallD1.server.policy.choice`. Configuration-info
queries require administrator authentication under that policy; the supplied
desktop policy allows information queries while retaining authentication for
changes. The Control Panel invokes several such queries with a 2.5-second
timeout. The QA account's read-only `faillock` output also showed three polkit
failures, so additional authentication attempts were stopped. Investigate and
test the read-only information policy and query path; do not broadly authorize
firewall changes or treat a longer timeout as a verified fix.

The r6 backend-only replacement builds are running in the isolated builder,
with output restricted to `work/beta2-profiles.UWsuLM/builder-output/r6-core-services/`.
The initial build attempt stopped before assembly because the pinned read-only
Shell share was not remounted after the builder reboot. Its failure log is
preserved as `builder-missing-shell-mount.log`; the guarded retry remounted it
and reached offline SquashFS compression. Online is sequenced after successful
offline export. These builds do not resolve the new status-query issue and
must not be promoted based only on successful assembly.
