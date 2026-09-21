# Online update recovery, approval and history corrections

Status: actual repository discovery, disconnected failure, same-window recovery,
declined approval, approved full upgrade, recheck and post-upgrade reboot/login
passed in the existing r10 online VM. Two additional presentation defects are
fixed with before/after regressions; Control Panel 52 built and upgraded normally,
and actual installed update history shows the corrected labels. No final ISO or publication is
authorized by this report.

## Preserved guest and exact component preparation

The r10 offline guest shut down normally. Its disk and NIC-free configuration
were preserved. The existing online disk/firmware were resumed, not recreated,
using the verified frozen online ISO with SHA-256
`f424e57f1d826db4946c378285a2a2c233b95fa174680543bad29e0df93caf0d`.
Only one 6 GiB/2-CPU guest ran. No host package or firewall changes were made.

Seven previously validated local candidates were hash-checked and installed in
one normal dependency-checked `pacman -U` transaction at 23:16 CEST: Desktop 30,
Explorer 54, Paint 9, Theme 54, Control Panel 51, Qt 6.11.2-3.1 and Spectacle 3.
All package files were present. Optional Programs Center was not added as part
of this update test. The hashes and before/after package lists are retained in
`online-update52-logs/current-components.X7yBIj/`.

A normal reboot/password login produced boot ID
`ffbee710-43e7-440c-9587-a58424b66c3e`. Control Panel SHA-256 was
`1a9e1e9ea26f83a700f48537e8a646673c518c45d86650aed7129d7473547eae`;
the installed update helper matched maintained source at
`7d1e493fb26b4f051c52fa845d46bb0f86a41f6d2a8e10518c3b12357ae2bc49`.
This is an upgraded guest, not an image containing those candidates.

## Real update and approval replay

The public repositories were left unchanged. The real Control Panel page was
opened through System and Security; an attempted unsupported `--page updates`
argument had opened the home page, so it is not counted as direct-page support.
All subsequent checks used the same Control Panel process, PID 1839.

| Step | Evidence and observed result |
| --- | --- |
| Connected discovery | [Two real updates](online-update52-logs/211-real-update-list.png): cryptsetup and libwacom. |
| Disconnect | QEMU link `virtio-net-pci.0` set down; guest had no default route. [GUI failure](online-update52-logs/212-disconnected-check.png) explicitly said availability could not be verified and nothing was installed. |
| Background failure | Actual `aero7-update-check.service` failed with exit 1 and “package availability is unknown”; no failure masking. |
| Reconnect/retry | Link restored, DHCP/default route returned. [The same window](online-update52-logs/213-reconnected-check.png) found both updates again. |
| Background recovery | Starting the unchanged service succeeded with exit 0 and “2 package updates; no installation performed”. No `reset-failed`, override or service repair. |
| Decline | [Install confirmation](online-update52-logs/214-install-confirmation.png) appeared; selecting No returned without a package transaction. |
| Approve | A second explicit Yes was followed by the actual [administrator password prompt](online-update52-logs/215-update-authorization.png) for `pacman --color never -Syu --noconfirm`. |
| Install | [The real transaction](online-update52-logs/216-approved-update.png) completed, including the boot-image hook. |
| Recheck | [Repository packages up to date](online-update52-logs/218-after-update-check.png), explicitly noting that AUR checking is unavailable because yay is not installed. |

Installed package lists, `/var/log/pacman.log`, and hashes of system sync
databases were byte-identical between baseline, disconnected failure and the
recovered/declined stage. Discovery and No therefore did not install packages
or refresh the system package databases. User-owned check databases are separate.

Only after explicit GUI approval and administrator authentication did pacman
perform the full system upgrade at 23:23:42. It changed exactly:

- `cryptsetup` 2.8.7-1 → 2.8.8-1.
- `libwacom` 2.19.1-1 → 2.20.0-1.

The transaction completed at 23:23:43 and the initramfs generation hook
completed successfully at 23:23:51. No ignored-package/partial-upgrade workaround,
signature weakening, fake repository, or terminal substitute for the GUI
transaction was used. The candidate Aero7 components were retained.

The following normal reboot/password login produced boot ID
`d6401675-6853-46a9-bdc5-6c15a0047a97`. Both updated packages passed `pacman -Qk`;
the shell was active with zero restarts and both failed-unit lists were empty
at the audit instant. The previous journal records a reboot request at 23:27:49
and completed shutdown at 23:27:50, without the delayed Plasma-close warning.
That is one observed shutdown, not universal reliability. Virtual CPU/graphics
warnings, missing helper portal identities and disabled-KWallet warnings remain.

## Two defects exposed by the replay

1. Immediately after a successful install, the page said “Your system is up to
   date” although it had not checked AUR and had not performed a new availability
   check. Completion now says the selected updates are complete and asks the
   user to check again for further updates. It preserves the distinct message
   when known unselected updates remain. Three repository/AUR completion cases
   fail before this change and pass after; process-close protection remains tested.
2. [Installed Updates](online-update52-logs/219-update-history-click.png) labeled
   locally installed Aero7 packages “AUR” / “Arch User Repository” solely because
   they were absent from current sync catalogs. The fallback now reads
   “Local or unavailable repository” with publisher “Unknown”. It does not
   invent an origin for local/private packages or for missing databases.
   Three such cases fail before and pass after. Latest-upgrade selection,
   known-repository grouping, version/date and ignoring non-upgrade log entries
   are also checked. Repository-derived labels remain catalog information,
   not proof of a historical package's signed provenance.

The extracted history parser is the production parser, used by the page's
existing asynchronous gatherer. Tests do not mutate `/var/log/pacman.log` or
run real package commands. The update helper's 15 policy tests pass; the page
suite passes 20 cases and history suite six, including setup/cleanup. The
three selected CTest suites all pass. Host-only offscreen/icon warnings are
retained in the log and are not claimed to be a warning-free graphical session.

Control Panel 52 source archive SHA-256:
`48599ab3a65bf74b86849035cb56924fea51960c10f4ada091cec4875b118125`.
The full package build completed at 23:34:38 CEST with all 20 CTest suites
passing. The prepared changed source files match the maintained worktree.
Host makepkg dependency prechecking alone was bypassed; installed dependency
checks and signature policy were not weakened. Archive identity, SHA-256,
unsafe-path and VCS-metadata checks passed.

- Package: `linux-control-panel` `0.1.0-52`.
- Size: 9,429,807 bytes.
- Archive SHA-256: `bc9d79115090f150e2c0c3854b6024de3be1822dd30a18ac76d06a9784c9d206`.
- Installed `/usr/bin/control` SHA-256: `170845c671eb21bba72cf330137cb44393c2eda9b1606a537828ca657b5b52e9`.

Normal `pacman -U` completed with all 74 package files present and the exact
binary hash verified. A new instance opened through `--page installed-updates`
shows [the corrected history](online-update52-logs/225-cp52-history.png), retaining
the real cryptsetup/libwacom upgrades and labeling the local Desktop/Explorer
entries “Local or unavailable repository” / “Unknown”. The source update helper
is unchanged. The successful full repository transaction above ran on Control
Panel 51; it is not relabeled as a second real update on 52. The new completion
wording is verified by the production-page regression tests.

The package-built page tests also ran in the installed Wayland session after
the upgrade: 20 update-settings cases and six history cases passed with no
failures or skips. These intentionally use isolated fake package commands and
must not be counted as a second real package installation. Installed package
lists before/after those tests were identical. Full logs are retained in
`online-update52-logs/cp52-wayland-tests.CqFvr7/`.

## Scope and evidence

[Evidence directory](online-update52-logs/) retains the normal component upgrade,
each update-state audit, package logs, before/after regression output, scripts
and 1920×1080 screenshots. Background-service recovery was deliberately
triggered without changing its schedule; timer scheduling across a whole day
was not tested. No AUR package installation was tested in this guest.
Earlier on/off persistence and manual checks while disabled are recorded in
[the update-preferences report](2026-09-08-update-preferences.md).

The public repository does not yet provide all local candidate versions.
Signing/promotion, remaining startup and workflow fixes, final image rebuilds,
fresh-image acceptance, website artifact URLs and publication approval remain
separate. No commits, pushes, wiki publication or final ISO build were made.
