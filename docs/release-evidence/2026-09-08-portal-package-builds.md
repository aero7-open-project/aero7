# Portal corrections: package build follow-up — 8 September 2026

This follows the [source regression report](2026-09-08-qt-portal-registration.md).
Normal upgrades, post-reboot baselines, a live portal comparison and region/
clipboard replay now pass; see the [installed validation follow-up](2026-09-08-portal-installed-validation.md).
Broader workflow and final-media acceptance remain open. No final ISO or signed
repository was updated, and nothing was committed or pushed.

## Control Panel 51: package complete, VM pending

`linux-control-panel-0.1.0-51-x86_64.pkg.tar.zst`

- Size: 9,408,447 bytes.
- SHA-256: `820c1c5105d98fd4c009e1e2608b8344972fb45f66c2da9a16ea7585fa706580`.
- Packaged Action Center binary SHA-256:
  `3242aba82c298c1973cf8a41df1bcda45c77e90b6b2b6b5cdf8f420dfda7901f`.
- Source archive SHA-256:
  `ea0bda848ae6990fe97d037f8c6192d0f249a82651e1f2466f3febeef5bf7c0c`.
- Finished at 20:19:49 CEST; all 19 package CTest groups passed.

The new archive derives from the exact package-50 source archive, adding only
the maintained Action Center identity change, application-entry installation
and source-order/packaging test. Its complete src tree matches the maintained
Control Panel src tree. All three packaged ELF direct-library requirement sets
match package 50. Apart from metadata and rebuilt binaries, the only payload
change is the added NoDisplay application entry; icons and helper scripts are
unchanged. This does not prove runtime dependency closure or desktop behavior.

The host's first makepkg attempt correctly refused its missing runtime
`pacman-contrib` dependency. The build was then run with dependency checking
explicitly skipped, without installing anything on the host. Compilation and
package tests succeeded with the installed development libraries. The package
retains its full dependency declarations; normal VM installation must check
them. Do not describe this as a clean-chroot build or runtime updater acceptance.

Logs and recipe: [action-center51-logs](action-center51-logs/).
Workspace: `work/beta2-action-center51/`. The exact archive is also staged in
the r10 QA guest's readonly inputs share, but has not been installed there.
The maintained package-repository recipe remains at 50 until live checks.

## Qt 6.11.2-3.1: full isolated build completed, VM pending

Completed at 21:06:39 CEST. The following preparation history is retained;
the terminal result and package checks are recorded below.

The r10 offline QA guest was normally powered off before starting the existing
isolated builder to limit memory pressure. The first ACPI power request did not
shut down its locked session; after unlocking, `systemctl poweroff` completed
and host PID 310781 disappeared. No forced QEMU termination was used.

Builder: `/home/admin/VMs/aero7-beta2-builder.HD2BwR`, QEMU PID 510403 at launch.
Preflight found no old builder job running, 28 GiB guest disk space available,
and Qt 6.11.2-3 installed. Only this disposable builder received dependencies
and system package updates. The host and QA guest packages remain unchanged.

The candidate recipe retains Arch's full dependency set, split package,
configuration flags and icon-theming cherry-pick. It adds the portal patch and
the eight-case regression fixture to `check()`, targeting the newly built Qt
CMake package. All six source checksums passed both on the host and in the
guest. Candidate PKGBUILD SHA-256:
`e898bb7ece909c485faca21a24697c87ec2375c732affee2bfc1f33d6bea13ed`.

First unit `aero7-qt-portal-build.service` stopped with status 15 before source
extraction/compilation: the ISO-building guest lacked debugedit and fakeroot.
That failure and package inventory are preserved. The preparation script now
includes Arch's assumed base-devel environment. After independently confirming
the failed unit and matching recipe, the guarded resume installed base-devel
and continued from the copied source; no existing artifacts were removed.

At 20:21:21 CEST, `aero7-qt-portal-resume.service` was active/running with MainPID
9713, makepkg PID 10023 and Ninja PID 15575 (`-j 2`). Actual compiler processes
were running. The 2,178-step build had subsequently passed step 120. Configuration
retained journald, GTK+, desktop OpenGL, Vulkan and the discovered SQL drivers.
This is a start/progress observation, not a completion result.

Follow-up at 20:53:29 CEST: `qt-portal-status.bBI6xG` confirms the same resume
unit is still active/running with MainPID 9713, makepkg 10023 and Ninja 15575.
The build subsequently passed step 1,512 of 2,178. The snapshot is retained in
`qt-portal-registration-logs/`. No restart or second concurrent build was used;
the QA guest remains off. This still does not establish package completion.

Authoritative output directory:
`work/beta2-profiles.UWsuLM/builder-output/qt6-base-6.11.2-3.1/`

- `build.log`: terminal initial failure, retained.
- `resume.log`: current build output; inspect this and the live unit together.
- `packages-before.txt`, `packages-after.txt`, `packages-after-base-devel.txt`:
  exact guest package inventories.
- Future success requires `QT_PORTAL_RESUME_EXIT=0`, exported archives with
  verified checksums, package tests and a terminal-success unit. An active unit's
  `Result=success` field is not evidence of completed work.

Guest build path: `/var/tmp/aero7-qt-6.11.2-3.1`.
Recipes, guarded preparation/resume and status scripts:
`work/beta2-qt-portal.3TA5gw/`.
The status script writes a new `qt-portal-status.XXXXXX` snapshot to builder-output
each time; it does not overwrite previous observations. Preserve the active job
across continuations and never start another build solely because an observation
times out.

After the complete package build: verify feature/payload/ELF parity, install the
exact candidates into the QA guest, inspect both applications' portal identities
at cold login, replay portal restart plus screenshot/native-dialog workflows,
and only then select packages for rebuilt online and offline final media.

## Package-comparison preparation

The frozen baseline `qt6-base-6.11.2-3-x86_64.pkg.tar.zst` passed its manifest
SHA-256 (`257c5ef6180119d5b4365bdfe2a2ad051694b5dff390eac8e736dd78b8107b21`)
and the archive identity/path checks before extraction into
`work/beta2-qt-portal.3TA5gw/package-parity.X9qW6U/baseline/`.

The read-only `compare-exports.py` records versioned dynamic symbol names,
binding, visibility, type and exported data sizes without executing libraries.
Its six real compiled-library fixtures pass, including rejection of removed
functions/libraries and changed data sizes. A baseline self-comparison covers
67 shared libraries. This only validates the checker: it is not a comparison
against a completed Qt candidate. Full C++ ABI and runtime compatibility are
not established by symbol-table equality. Scripts and fixture results are
retained in `qt-portal-registration-logs/`.

## Completed package and static comparison

All 2,178 build steps completed. All eight portal regression scenarios passed
against the newly built Qt (6.48 seconds). Package assembly/export completed
with `QT_PORTAL_RESUME_EXIT=0`. At 21:07:23 CEST the same resume unit was
inactive/dead, MainPID 0, Result success, ExecMainStatus 0; the original failed
preparation unit remains separate historical evidence.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| qt6-base-6.11.2-3.1-x86_64.pkg.tar.zst | 21,620,819 | eb0dd4e417acc1f75a29c0ac134acafb90aaf061a7b2198ffd5531272fa3c690 |
| qt6-xcb-private-headers-6.11.2-3.1-x86_64.pkg.tar.zst | 35,202 | 01c8fa728292022b365f105c80f62b98e75c14dedbb2a8ee6036b0f7ab4088a1 |
| qt6-base-debug-6.11.2-3.1-x86_64.pkg.tar.zst | 408,701,789 | c55784b50d2d7d8f8123c9fd0292dda80444aaf3816145138cbd090be3524953 |

All three exported checksums verified. Main and private-header archive
identity/path checks pass. Comparing the extracted main package with the frozen
Arch baseline finds all 67 shared libraries' exported symbol records unchanged,
all 88 ELF direct-library requirements unchanged, and byte-identical complete
`usr/include` and `usr/share` trees. Dependency declarations are unchanged.
Only version, build date, packager and installed-size fields change in PKGINFO.
The larger compressed archive does not reflect a larger installed payload:
installed size changes from 69,756,985 to 69,748,798 bytes. The unsigned test
package still identifies its builder as Unknown Packager; this is not a signed
repository release.

Packaged QtGui SHA-256:
`e8b4af6296f3aa591c269ad9ed4dda33a1e0b7f7eb59b1f81a55011c9887e4cf`.
These static comparisons are not full C++ ABI or installed runtime acceptance.

Logs, package inventory, configuration, recipe, checksums, terminal unit snapshot
and comparison JSON: [qt-portal-package-logs](qt-portal-package-logs/).
The main archive and guarded normal-upgrade script are staged in the r10 QA
inputs share. After terminal-success verification the builder shut down normally
and PID 510403 disappeared. The existing offline QA guest resumed as PID 562706
with its ISO checksum verified and no network adapter; candidates are not yet
installed. Frozen images and package-repository selection remain unchanged.
