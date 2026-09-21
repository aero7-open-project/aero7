# Time synchronization and Internet Time settings — local QA

Not release approval. r8 images remain unchanged; these changes need new
package/media verification. No commits, uploads or repository promotion.

## Reproduction and installer correction

The fresh online r8 guest had `systemd-timesyncd.service` installed by systemd
261.2-1 but disabled/inactive after OOBE and restart. `CanNTP=yes`, `NTP=no`,
`NTPSynchronized=no`, with no timesyncd journal entries. The image core-service
adapter enabled NetworkManager/SDDM/firewalld but never started the NTP client.

Source now enables and starts timesyncd during first-run image setup, checking
its enabled/active state. It does not wait for network synchronization and is
not an update/migration hook that changes existing users' clock preferences.
All 133 backend tests pass, including the expanded command sequence and injected
failure checks; existing UFW files remain untouched by that path.

In the online disposable r8 guest, the exact added service commands succeeded
at 17:36:52 CEST. The daemon contacted an Arch pool time server and recorded
initial clock synchronization. The next status probe reported
`NTP=yes` and `NTPSynchronized=yes`. No firewall changes were needed. This is
a manually applied regression check, not fresh corrected-image acceptance.

Evidence under `/home/admin/VMs/aero7-beta2-r8-pWRIgW/online/results/`:
`time-sync-inspect.log`, `time-sync-apply.log`, `time-sync-after.log`.
Backend suite: `work/beta2-updater-final.8Q4lde/time-sync-backend-tests.log`.
The offline guest, still with no network adapter, also enabled/started the
service successfully at 17:50:51 CEST without waiting for a network connection.
It correctly reports `NTP=yes`, `NTPSynchronized=no`. Evidence is its
`results/time-sync-before.log` and `results/time-sync-apply.log`. A QMP typing
race dropped the beginnings of the initial log-copy commands; they were rerun
individually. The service operation itself succeeded. Restart persistence
was then verified in the offline guest: Start-menu restart and SDDM login
succeeded; boot `249a576a5a044edc91c5a79a6d0a240e` reports the service enabled and
active, with only loopback and no failed system units. See
`offline/results/time-sync-reboot.log`. Previous-boot logs still contain
shutdown-time accessibility/DRM messages and the earlier clocksource watchdog
warning; this is not a warning-free claim. Online persistence subsequently passed
in boot `290176319b5e4616b42d9139835251f0`: enabled/active, no failed system units,
`NTPSynchronized=yes`, and synchronization with the GUI-selected Cloudflare server
at 18:04:55. See `online/results/time-sync-reboot.log`.

## Control Panel issues found during the same investigation

The editable Internet Time server was interpolated directly into elevated shell
source. Saving could start a separate NTP toggle and configuration-write action
concurrently, and Update now ignored the currently selected server.

The working correction validates one hostname/IP and passes it as a positional
argument to fixed shell source. Configuration is replaced atomically, then NTP
is enabled and the client restarted in sequence through one authorization.
Disabling uses a direct timedatectl argument list and does not overwrite the
server. Update now uses the selected server. Status guidance follows the
checkbox. Duplicate operations and ordinary Date and Time dialog dismissal
are blocked while an action is pending; failed launch/cancel/failure releases
busy state and does not call the success callback.

New tests cover invalid host data, argument separation, operation order,
short-circuiting after failure, temporary-file cleanup, selected-server GUI
wiring, duplicate-operation/close protection, cancelled authorization and
missing-command recovery. All 18 CTest groups passed (9.08 seconds), logged in
`work/beta2-updater-final.8Q4lde/control-time-tests.log`. The unsigned r48 package
built in `work/beta2-internet-time.LOWI7y` and passed all 18 package CTest groups
(9.24 seconds). Package SHA-256:
`213432bcbda0bb3a78e9477c86f7b1cdea8661ce6e0209b6b0d488df4c1b7bcb`.
Source archive SHA-256:
`efc2d910c23cfb44ec78ba41f2091d2360809603d91c54a92aa46843a14164c2`.

Both disposable r8 guests were manually upgraded to r48. The offline package
integrity check reports 73 files, zero altered files; its expected unsynchronized
repository-database warnings remain. These are modified guests, not fresh r48
media installations.

Installed online GUI checks:

- Invalid server text displays a validation warning without authentication
  (`29-invalid-time-server.png`).
- Selecting `time.cloudflare.com` and pressing Update now opens one administrator
  prompt. Cancelling returns to usable settings with the previous server still
  shown in the parent dialog (`30-time-authorization.png`,
  `31-time-auth-cancelled.png`). Retrying opens a fresh prompt.
- After approval, the configuration is a root-owned 0644 file containing exactly
  `[Time]` and `NTP=time.cloudflare.com`. The service contacts that server and
  synchronizes at 17:59:09; the status probe reports `NTPSynchronized=yes`.
  See `online/results/time-sync-control-applied.log`.

Installed offline GUI checks: switching synchronization off disables its server
controls, requests administrator approval on save, and updates the parent status
to not configured for automatic synchronization (`55-time-disable-option.png`,
`56-time-disable-auth.png`, `57-time-disabled.png`). Re-enabling also completed
after approval and the parent status refreshed (`58-time-enable-auth.png`,
`59-time-reenabled.png`), still with no NIC. The collected
`offline/results/time-sync-control-reenabled.log` records stop at 18:01:27,
restart at 18:03:14, enabled/active state and `NTPSynchronized=no`, as expected
without a network adapter.

The online reboot attempt correctly asked before closing the QA terminal's
interactive root shell. The terminal was idle with evidence already saved;
its close confirmation was accepted. This user-response delay is not an NTP
startup timeout (`online/35-time-reboot.png`).

## Additional malformed-address regression — r48 superseded

A final edge-case test found that QHostAddress accepts arbitrary text after an
IPv6 scope separator, including a newline followed by a second NTP setting.
The failing source regression is recorded in
`work/beta2-internet-time.LOWI7y/scoped-address-newline-before.log`.
This would write an unintended configuration entry after administrator approval;
it is not evidence of a shell-command execution or authentication bypass.

The validator now restricts characters before address parsing, rejecting scope
suffixes and control characters while keeping hostnames, IPv4 and ordinary IPv6.
All 18 source test groups pass in `scoped-address-fixed-tests.log` (9.02 seconds).
The unsigned r49 package built successfully and passed all 18 package tests
(9.02 seconds), then installed in both guests. Each reports version 0.1.0-49
and 73 files with zero altered files. The local recipe, .SRCINFO and candidate
manifest select r49. Full ISO static checks passed with the existing QML
unqualified-access warnings; `.SRCINFO` matches generated metadata.

r49 package SHA-256:
`45ea2224eff8db789a98eac17e408d45fc329c63fe0246544d9430b05331ad88`.
Source archive SHA-256:
`0a343754eda3c34a891edbd28fcc8259e9f639702c35ae9368d462b1d6b88505`.
Build/evidence: `work/beta2-internet-time.LOWI7y/build-r49.log`,
`iso-static-r49-check.log` and both guests' `results/control-r49-upgrade.log`
and `results/control-r49-integrity.log`.

Installed r49 was opened normally as the desktop user. Entering a scoped IPv6
address and pressing Update now produced the expected validation warning before
authentication (`online/40-r49-scoped-address-rejected.png`). Cancelling the
settings editor discarded the test input. The newline regression was tested
in the source/package suites, not entered into the live guest configuration.

**Do not use r48 for new images.** Its ordinary GUI evidence above remains
useful but does not prove fresh r49 media. No new ISOs have been built with
these time changes yet, and no signing, promotion or publication has occurred.

## Lock-screen negative-path check

In the offline r8 guest, a deliberately incorrect password produced the expected
error, followed by successful unlock with the correct password. Screenshots
`46-lock-result.png`, `47-retry-form.png` and `48-unlock-result.png` record this
single failed-login/recovery sequence. This does not substitute for repeated
session shutdown or hardware acceptance.
