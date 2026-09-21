# Beta 2 updater error-path and legacy UFW checks

Status: installed r46 error/lifetime checks passed with harmless GUI fixtures;
r47 fixes a discovered wrapping defect and is selected locally. Final-media
acceptance remains pending.
This is not release approval.

## Connected legacy UFW guest

The stopped r4 online test guest was restarted using
`/home/admin/VMs/aero7-beta2-r4-Nlm227/start-online-r44-test.sh`.
The diagnostic input share is read-only and the writable share is restricted
to `online/r44-results/`. The host firewall and packages were not changed.

Authenticated Control Panel upgrade from r40 to r44 succeeded using exact
locally checked archives, including its three update-check dependencies.
All 20 regular files under `/etc/ufw` retained their SHA-256 values, and UFW
retained its enabled and active state. No fresh-firewalld marker or information
policy was created. Evidence: `online/r44-results/upgrade-r44.log`,
`ufw-before.sha256`, `ufw-after.sha256`, and the service-state comparisons.

The real graphical update check found one repository update. Screenshot
`38-r44-update-result.png` shows that result; `39-r44-update-approval.png`
shows the approval prompt before installation. No was selected. The actual
unprivileged checker then produced the notification captured in
`42-r44-positive-notification.png`. The package-log tail in
`43-r44-no-install-log.png` ends at the earlier authenticated r44 upgrade;
the subsequent check, notification and cancelled approval added no transaction.
This is upgraded-guest evidence, not proof
that the scheduled check or final installation image passed every path.

## Incorrect success reporting discovered and corrected

The graphical page ignored repository check exit failures and always proceeded
to the AUR check; an empty resulting list displayed up-to-date status. AUR
errors and crashes were likewise treated as an empty successful result.
The separate scheduled checker already rejected those repository errors.

Five executable Qt regression cases first failed against the old source:
repository error, repository crash, empty success output, AUR network error,
and AUR crash. They now display an explicit error instead of successful status.
The correction also leaves the last successful-check timestamp unchanged on
failure and removes stale install selections. When yay is unavailable, the
no-update result explicitly applies only to repository packages.

The AUR empty-result handling was checked against
[yay's upstream implementation](https://github.com/Jguer/yay/blob/next/print.go):
its empty-result path returns an empty error. The frontend therefore accepts
normal exit 1 only with empty output and diagnostics; nonempty error diagnostics
and crashes remain failures. Unreadable successful output is also rejected.

The expanded Qt test covers eleven failure/success result combinations,
including both empty-result exit conventions, real-format repository/AUR
update lines, and missing yay. All 16 Control Panel CTest groups pass.
Logs are in `work/beta2-firewall-info.LHxVb2/update-error-*.log`.
Packaging work is in `work/beta2-update-errors.GqIwJU/`.
The unsigned r45 package completed at 16:00:38 with all 16 CTest groups passing.
As for the preceding local QA package, `--nodeps` bypassed the host dependency
precheck only; tests were not skipped. This is not a clean signed release build.
Package SHA-256:
`8d119fd855cf6862ef6af3c34db93ada6836de795baab4417247cbe2cbf9d7f1`.
Source archive SHA-256:
`5442687e489833048d2bc0b60cfbe2c94a8f53573d97f67a4ca0dae160ffcb4d`.

## Update transaction lifetime follow-up

The page-owned QProcess was vulnerable to destruction when Control Panel replaced
the update page. The source now retains that page while a repository/AUR install
is active, ignores ordinary window-close requests until completion, and explains
why the user needs to wait. Back/forward, search and page navigation are guarded.
A failed command start releases the guard and displays an explicit error instead
of leaving the page permanently busy. Process crashes cannot count as success.
Merged package output is retained for failure diagnostics.

Four executable fixtures pass: standalone repository page, nested repository
page, nested AUR page, and missing privileged command. The fixtures use a private
PATH and harmless `/bin/sleep`, never real package operations. All 16 CTest
groups pass after compiling the complete Control Panel. Logs:
`work/beta2-update-errors.GqIwJU/transaction-{build,tests}.log`.
The initial `close-before.log` used an incorrect QMessageBox test response and
does not establish a valid before-fix regression; do not cite it as proof.
The corrected fixtures click the actual Yes button and assert an active install.

The r46 source archive hash is
`60333e823c9551231e9be74b29264bf1777859932090d19cd2532a2e5925eca8`.
Its unsigned local QA build completed at 16:16:48, with all 16 CTest groups
passing, in `work/beta2-update-lifetime.0VTg5d/`. Package SHA-256:
`1f4c4ff67e74d234b99f379c3bd86ba09558178f651d8a83f08ae5df53986d3a`.
Real MainWindow navigation and repository-failure checks subsequently passed in
the installed r46 guest, as detailed below.
This ordinary-close guard is not proof of protection against forced termination,
power loss, session shutdown, or every package-manager failure.

## Remaining checks

- Finish the final-media application matrix with r47 selected.
- Repeat disconnected/error, notification, settings persistence, approval and
  cancellation checks on final media.
- Repeat the tested close/navigation and update-error paths on final media;
  do not deliberately interrupt a real package operation.
- The completed r7 images contain r44, not these later corrections.
  They can test the fresh firewall/OOBE repair, but are not final release media.
- No commits, pushes, signing, repository promotion or publication occurred.

## Intermediate offline r7 image

Assembly and exact embedded-content verification succeeded; a new no-NIC VM
started at 15:57 under `/home/admin/VMs/aero7-beta2-r7-xGDR49/offline/`.
It completed installation and first-run setup and reached the desktop at about
16:13 without a NIC or a manual backend/service repair. Account creation used
`aero7test` / hostname `aero7-r7-offline`, recommended notification-only update
checks, Europe/Amsterdam and Public network defaults. The no-connected-network
notice was displayed correctly. A first-login sudo authentication succeeded.
The first-boot audit passed package integrity, no-NIC validation, active/enabled
firewalld and real IPv4/IPv6 Public packet probes (inbound blocked, outbound
allowed with verified replies). No failed system services or current-boot crash
dumps were found. Europe/Amsterdam is applied correctly. The normal-user
Control Panel shows firewall On without an authentication dialog, captured in
`22-firewall.png`. OOBE logs retain the pinned Shell's package-origin and
Plymouth-visible-hold warnings; this is not a warning-free install.
Results are in the VM's `offline/results/`, including `installed-audit.log`,
`oobe.log` and `first-boot-journal.log`. The normal-user policy probe also passed:
three read-information actions are allowed, configuration actions still require
administrator authorization, queries take about 0.29 seconds, and faillock has
no entries. No failed user services were listed. The update-check timer is
enabled and waiting after selecting recommended checks in OOBE. Evidence:
`a7-user-policy.log`, `a7-user-failed.log`, `a7-update-timer.log`.
Start-menu Restart was selected at 16:18:58. SDDM returned, the password login
succeeded, and the desktop was reached again by 16:19. Screenshots
`24-power-menu.png`, `26-login.png` and `28-reboot-desktop.png` preserve this
ordinary reboot/login pass. The SDDM branding is fully visible at 1920x1080.
Post-reboot system service/package checks and IPv4/IPv6 packet probes also
passed (`post-reboot-audit.log`), with no current-boot coredumps. The captured
post-reboot journal has no matching authentication failure, faillock or
failed-service-start errors. Broader shutdown repetition remains pending;
a single successful reboot does not clear intermittent shutdown bugs.

## Installed r46/r47 graphical updater acceptance

The r4 online/UFW guest was upgraded from r44 to r46 and then r47. Both package
checks passed with 73 files and zero missing, all 20 UFW file hashes stayed the
same, and UFW remained active/enabled. No fresh-firewalld marker was created.
Logs are in `online/r44-results/r46/` beneath the r4 guest directory.

The installed `/usr/bin/control` was launched as its normal desktop user with
an isolated configuration and a temporary command PATH. Fake `checkupdates`
provided a known failure or one update; fake `pkexec` only waited for a release
marker and never invoked privilege escalation or a package manager.

- Screenshot `49-error-result.png`: repository failure displays an explicit
  error and leaves the successful-check timestamp at Never.
- `51-approval.png`: installation approval is requested before the fixture runs.
- `52-update-guard.png`: attempted close, Home, Back and search leave the active
  operation running on the update page.
- `53-fixture-completed.png`: releasing the same running mock operation produces
  its completion marker and a successful UI result.
- `54-navigation-restored.png`: Home works again after completion; normal window
  close then succeeds. Captured pacman logs show no real transaction between
  the r46 upgrade and these mock checks.
- r46's waiting guidance was clipped. Added word wrapping plus a regression
  assertion; all 16 CTest groups passed. The unsigned r47 package built at
  16:28:02. In the installed r47 guest, `59-r47-wrapped.png` shows the whole
  message across two lines. The mock operation again completed normally.

r47 package SHA-256:
`2a1f21b512ef6eefb07a34d537aecaba1cbeda0f4b317f4e70dfe6f2f3046ebb`.
Source SHA-256:
`c4eb74d54aa0d93aa48c2873f80b5c6d10c3f471abb5220d87a15f6042a69365`.
Local recipe, .SRCINFO and ISO candidate manifest now select r47; no remote
repository promotion or publication occurred. These deliberately mocked GUI
checks are not a successful full-system package upgrade or final ISO acceptance.

## r8 media rebuild

Both online/offline profiles were prepared with r47. Each preparation passed
130 backend tests, three installer CTest groups and candidate/package checks.
Prepared inputs and logs are in `work/beta2-updater-final.8Q4lde/`.
The local candidate manifest SHA-256 is
`ba0233b31855ec7056b3cd4133a3ab13fbc67bead5954649c8282fec57f014ce`.
The existing isolated builder started `aero7-r8-builder.service`; output is
`work/beta2-profiles.UWsuLM/builder-output/r8-updater/`.
No new VM was started from r8 media yet. Build success and final-media
acceptance must be checked separately; do not infer them from preparation.

The website handoff's long, superseded QA preamble was consolidated into one
current hold/checklist while preserving all product copy and announcement
sections. The pre-cleanup document is preserved locally as
`work/beta2-updater-final.8Q4lde/website-handoff-before-cleanup.md`.
English UI, Dutch regional formatting and the US keyboard were selected. The
exact new standalone 64 GiB qcow2 was confirmed through QMP before approving
installation to guest `/dev/vda`; no host disk or existing guest was selected.

- File: `aero7-beta2-offline-2026.09.06-x86_64.iso`
- Bytes: `3318009856`
- SHA-256: `cd23d0dad4d86fbee3fee0c9a6b1e6396a97acb6aa41cc14c3d62b9d12a83084`
- Location: `work/beta2-profiles.UWsuLM/builder-output/r7-firewall-status/`
- Verifier: `work/beta2-firewall-info.LHxVb2/verify-offline-r7.log`

The online build also completed and exported successfully (`R7_BUILDER_EXIT=0`)
but has not yet been freshly installed. Do not use these intermediate
filenames/checksums in public download cards.

## Build-drive cleanup

After confirming no process held the files, the superseded r5 and r6 online and
offline ISO exports were removed (four files, about 9 GiB). Their build logs and
checksums remain. Current r7 images and all VM disks were retained. Available
space increased from approximately 18 to 27 GiB. Removed exports require a
rebuild or a retained builder copy to recover; they were not put in Trash.
