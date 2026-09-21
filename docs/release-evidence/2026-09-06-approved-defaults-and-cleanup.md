# Owner-approved obsolete test artifact cleanup — 6 September 2026

The owner authorized deleting old VM disks and ISOs to free space on the current drive. The following exact regular files were checked with fuser (none open). All VM backing chains under /home/admin/VMs were inspected; none depend on the selected disks. Retained: both r4 disks, Windows reference VM, desktop reference VM and its wiki overlay, all logs/screenshots, source, and latest ISOs. These files are permanently deleted, not moved to Trash, to actually reclaim space. Historical acceptance evidence remains historical; these older guest disks are no longer replayable.

## Selected artifacts

- `/home/admin/VMs/aero7-beta2-acceptance-7Shb97/offline/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-acceptance-7Shb97/online/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-retest-zQPhkv/offline/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-retest-zQPhkv/online/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-fixed-mSLoUt/offline/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-fixed-mSLoUt/online/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-final-CZc2ad/offline/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-final-CZc2ad/online/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-release-check-Mnoerz/offline/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-release-check-Mnoerz/online/disk.qcow2`
- `/home/admin/Documents/Codex/Recovered-from-nvme1n1p3/Documents/scripts/aero7-physical-log-test-iso/out/aero7-beta2-offline-2026.09.04-x86_64.iso`
- `/home/admin/Documents/Codex/Recovered-from-nvme1n1p3/Documents/scripts/aero7-physical-log-test-iso/out/aero7-beta2-online-2026.09.04-x86_64.iso`
- `/home/admin/Documents/Codex/Recovered-from-nvme1n1p3/Documents/scripts/aero7-physical-log-test-iso/work/previous-images/aero7-physical-log-test-2026.09.03-x86_64.iso`

## Approved defaults

Updates must ask before installation; automatic checking can be enabled or disabled. Fresh installations may use firewalld for connection-specific network profiles; existing UFW installations must not be migrated or rewritten. No GitHub publication is authorized by these decisions.

## Verified cleanup outcome

The explicit deletion reclaimed approximately 82 GiB: available space rose from
14 GiB to 96 GiB on `/dev/nvme0n1p4`. After the new package build, 95 GiB remained.
No source, screenshots, logs, reference guests, or current r4 disks were deleted.

## Update package built and selected locally

Control Panel `0.1.0-41` includes the on/off preference dialog, notification-only
user timer and helper. Package installation remains an explicit, confirmed full
repository upgrade. A selected subset no longer runs a partial `pacman -Sy`
upgrade. Repeated clicks do not terminate a running update process. Missing
`checkupdates` reports an unavailable check instead of attempting privileged
database refreshes or falsely reporting an up-to-date system.

- All 14 Control Panel CTest groups passed in the package build.
- The new update-helper suite contains 15 cases; the native Qt dialog test covers
  saving on/off and cancelling without changing the preference.
- Installer CTest: 3/3 passed; existing backend suite: 101/101 passed.
- Dependency closure against the selected r41 package: 2/2 passed.
- `.SRCINFO` matches `makepkg --printsrcinfo`; recipe hashes updated locally.
- Runtime `pacman-contrib` and `fakeroot` archives were verified against the Arch
  keyring and added to the offline base bundle. `libnotify` was already bundled.
- Package SHA-256:
  `52e2df1d55f01f2846a668e9d9cf7d163de856db846ce72809fe4b2f636baa35`.

Evidence: `work/beta2-approved-updates.U6HL7w/control-panel-package-build.log` and
`work/beta2-approved-updates.U6HL7w/dependency-closure-r41.log`.
The local build used `makepkg --nodeps` only to skip the host dependency precheck
because the host lacks pacman-contrib and noninteractive sudo. Compile and CTest
checks ran normally. This is not signed-repository promotion or clean-builder
validation. No new package has yet been installed in the VM during this pass.

## Firewall implementation boundary

The new, not-yet-wired `backend/firewall_defaults.py` has 11 passing unit tests.
It uses an explicit fresh-install backend marker, preserves enabled AND disabled
UFW configurations, rejects the running host as an installation target, validates
the new zone before marking success, preserves custom zone files, and refuses
to start firewalld when UFW is enabled. Its restrictive initial zone opens no SSH
or file sharing and does not enable forwarding.

Still required: dual-backend Control Panel and Action Center, runtime packages
and offline dependency closure, installer integration and payload copy, actual
firewalld configuration validation, packet tests, per-connection profile work,
and fresh online/offline end-to-end ISO acceptance. Current selected r41 still
uses UFW; neither update scheduling nor firewalld is claimed verified on final
media. Existing r4 guest evidence must not be presented as new-media acceptance.

## Follow-up: firewalld integration and r42 package

The installer now calls the guarded fresh-target setup and copies its module
into both the live image and installed system. OOBE activates only the explicitly
selected backend. Legacy UFW files and enabled state are not rewritten.
The base package list selects firewalld. Control Panel no longer requires UFW;
both supported firewall backends are optional package dependencies, with the
fresh ISO explicitly supplying firewalld.

Control Panel and both Action Center surfaces share backend selection/status.
Firewalld failures are displayed as unavailable, not falsely off or protected.
Native controls support authenticated enable/disable, zone-scoped port/service
exceptions, firewalld-specific denied-traffic logging, and restoring one zone's
shipped defaults. Reload side effects are disclosed in the relevant dialogs.
The root helper validates all arguments, serializes changes, preserves legacy
UFW, and reports partial permanent/runtime failures. It never saves unrelated
runtime rules via runtime-to-permanent. The package supplies the restrictive
`aero7-public` zone as a restorable shipped default.

Local package `linux-control-panel-0.1.0-42-x86_64.pkg.tar.zst` built successfully
and replaced r41 in the selected local manifest. SHA-256:
`97bb89c3c921c3e51ad18c0e509b41cf264397809c93c3e56ed79cf8555b3cfd`.
This remains unsigned local QA, with the same host dependency-precheck exception
noted above. Nothing was committed, signed or published.

- Package build CTest: 16/16 passed, including 11 privileged-helper policy cases
  and 7 shared-status scenarios covering legacy UFW, stopped/failed firewalld,
  query failures, and unknown backend markers.
- Current installer/backend suite with selected r42: 113/113 passed.
- The new offline firewall dependency test recursively checks version and
  SONAME requirements, not just package-name availability.
- Seven additional Arch archives were signature-verified against the bundled
  Arch keyring and checksum-pinned: firewalld, python-firewall, python-capng,
  python-dbus, python-gobject, gobject-introspection-runtime, libgirepository.
- Firewalld 2.5.1's actual offline client validated the shipped zone, accepted
  `--set-default-zone=aero7-public`, passed `--check-config`, and returned
  `aero7-public` from `--get-default-zone`. This ran against extracted package
  files in a separate user/network namespace, without host package installation
  or host firewall changes. This is configuration validation, not packet tests.

Logs: `work/beta2-firewalld.4Dbzna/control-panel-r42-package-build.log`,
`backend-r42-selected-tests.log`, and `firewall-dependency-closure.log` in the
same directory. The checksum-checked `r42-transfer.iso` is prepared for testing
an upgrade of the existing r4 offline guest while comparing UFW files before
and after. Its temporary upgrade script is not part of release media.

Still pending: VM update-scheduler/UI acceptance, UFW-preserving upgrade proof,
fresh firewalld packet/reboot tests, per-connection Home/Work/Public integration,
and both final ISO builds and full installation/reboot regression. No final ISO
acceptance or release-readiness claim follows from these source results.

### Existing offline guest upgrade verified

The r4 offline guest (QEMU PID 9885, no NIC) installed Control Panel r42,
pacman-contrib 1.13.1-1 and fakeroot 1:1.37.2-3 from the checksum-checked transfer
CD through an authenticated sudo command. The script completed with
`R42_UPGRADE_PASSED_UFW_UNCHANGED`: `/etc/ufw/ufw.conf`, `/etc/default/ufw`,
`/etc/ufw/user.rules` and `/etc/ufw/user6.rules` had identical SHA-256 values
before/after; UFW remained active; no firewalld backend marker was created.
`pacman -Qk linux-control-panel` reported 71 total files and zero missing files.

Guest log: `/var/log/aero7-r42-upgrade.log` (not yet copied back to host).
Host visual evidence:
`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/122-r42-upgrade-result.png`.
The warnings about absent repository databases are retained; this disconnected
guest installed explicit local archives without refreshing repositories. This
proves the tested UFW-preserving package upgrade, not fresh firewalld startup,
update notifications, or final-media acceptance. The r42 transfer CD remains
mounted at `/run/aero7-r42` for further QA; no root serial shell was enabled.

## Follow-up: update preference runtime and r43 network profiles

The upgraded disconnected guest persisted `Enabled=false` after reopening the
native Change settings dialog. The user timer remained active intentionally:
the helper printed `Automatic update checks are off` and returned without a
query. Re-enabling saved `Enabled=true`; the helper reported a failed check and
unknown package availability, never a false up-to-date result. The original
enabled preference was restored. Evidence: screenshots 128, 130 and 131 under
`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/`. Positive update-available
notifications and approved installation still need final-image runtime tests.

This exposed a misleading grey Change settings link: an obsolete target lookup
marked a directly handled native action unavailable. r43 excludes that action
and Check for updates from the legacy resolver. r43 also adds per-connection
Public/Home/Work controls and validates active physical NetworkManager UUIDs
before authenticated profile changes. OOBE selects only an unambiguous physical
connection; Public stays the default for disconnected/ambiguous cases. Home
permits mDNS discovery only, not automatic sharing or remote access. All three
zone definitions passed firewalld's actual offline validator. Packet/reboot
acceptance and the r43 graphical recheck are not yet complete.

Control Panel `0.1.0-43` built locally with all 16 CTest groups passing, including
13 helper policy cases. The same host `--nodeps` precheck exception applies;
this is not a clean signed-repository build. Selected archive SHA-256:
`bf0f77836f8aa04574f7bce2526313dbd2f4a72f1696e9d72a1b6dddc4b8a8f4`.
Recipe/source hashes and `.SRCINFO` were refreshed locally. No commit or push.

Offline preparation found and fixed three integration defects:

- Offline pacstrap installs every base archive. The obsolete UFW archive would
  therefore defeat the fresh firewalld default even after editing the package
  list. It was moved, not deleted, to
  `work/beta2-profiles.UWsuLM/legacy-base-packages/ufw-0.36.2-7-any.pkg.tar.zst`;
  its manifest entry was removed and dependency tests now reject it in the fresh
  base bundle. Existing guest UFW was not removed or changed.
- The pinned Shell parity check still required UFW. Its explicit approved
  replacement is now firewalld; every other parity check and the pinned Shell
  source remain unchanged.
- The installer manifest parser rejected Spectacle's valid colon-containing
  versioned filename. It now accepts colons while regression tests still reject
  absolute, nested and traversal paths, and parse the exact candidate manifest.

Offline prepare-only now succeeds: 124 backend tests, 3 installer CTest groups
and all embedded bundle checks pass. Logs are in
`work/beta2-profiles.UWsuLM/offline-prepare-fixed.log`, with the earlier failed
preparation preserved alongside it. This is profile preparation, not ISO or
fresh-install acceptance.

The stopped r4 online disk was copied into a standalone builder disk under
`/home/admin/VMs/aero7-beta2-builder.HD2BwR/`; the original disk is unchanged.
The isolated builder has 6 GiB RAM, two vCPUs, read-only project/Shell shares,
and one writable share restricted to
`work/beta2-profiles.UWsuLM/builder-output`. No host packages or firewall
settings were changed. Host free space after cloning was 85 GiB. Building both
final variants, exact checksums, fresh installs and final desktop acceptance
remain required before publication.

### r43 guest check and build progress

The same disconnected r4 guest subsequently installed the exact r43 archive
from `r43-transfer.iso`. The checksum check passed, UFW's four files were
unchanged, its service stayed active, no backend marker appeared, and the
package check reported 73 files with zero missing. Screenshot 135 records
`R43_UPGRADE_PASSED_UFW_UNCHANGED`; screenshots 136–137 show the corrected,
non-grey Change settings link and its working native preference dialog.
Screenshot 138 shows the retained UFW backend reporting On and explaining its
single rule set, without exposing firewalld-only location controls. No firewall
settings were changed by that read-only page check. The guest log is
`/var/log/aero7-r43-upgrade.log`, not yet copied to the host.

The isolated builder successfully installed its build prerequisites and reached
offline SquashFS compression. Its active compressor was verified at about
192% CPU using the two assigned vCPUs, rather than assuming a slow progress
bar meant a hang. The full build has not yet been accepted. Host online
prepare-only also completed successfully (`online-prepare.log` in the r43 QA
directory); a separate guest job waits for offline build/export success before
copying the online profile and building it. Output/logs are restricted to the
dedicated builder-output share. Neither build job publishes artifacts.
