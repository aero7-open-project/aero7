# Selected package set: both upgraded guests and retained build recipes

13 September 2026. Existing test-guest alignment and normal reboot checks, not
fresh final-image installation or release approval. No production package,
manifest selection, frozen ISO, Git commit or published content changed.

## Exact selection and guest changes

Manifest SHA-256:
`36d3c6a00f369ff6f86cfde5124e7b712fffebe8ad3b111ffb88dc862f543258`.
It selects 16 core packages and two optional packages, as listed in the
[current release notes](../BETA2-RELEASE-NOTES.md).

The online guest was behind in four core packages. A normal `pacman -U --needed`
transaction upgraded Desktop 33, Gadgets 25, Control Panel 55 and KWin 7.3 with
dependency, file-conflict, integrity and disk-space checks enabled. Other
selected core packages were already current. Its vault remains installed at
release 7; Programs Center remains absent. Both optional caches and sidecars
match the selected archives. Existing encrypted wallet file contents, wallet
policy and gadget layout remain unchanged.

The disconnected guest already had all 16 selected core versions and Programs
Center 3 installed. The transaction therefore skipped those current packages.
Its vault cache was updated from 6 to 7, without installing or enabling the
vault. The account still has `Enabled=false` and no wallet directory. Optional
package presence, account policy and gadget layout remain unchanged. It has no
network adapter; repository-sync database warnings are retained, and no network
refresh was performed.

Upgrade evidence, both exit 0:

- [Online selected-stack-upgrade.Kdd5sV](selected-stack-logs/selected-stack-upgrade.Kdd5sV/upgrade.log).
- [Offline selected-stack-upgrade.LlYKjN](selected-stack-logs/selected-stack-upgrade.LlYKjN/upgrade.log).

## Normal reboot and running components

Both guests restarted through the normal Start-menu Restart action and returned
through password login. Only one 6 GiB, 2-vCPU guest ran at a time, at 1920×1080.
The online guest was subsequently shut down normally before starting offline.
No QMP reset, forced process kill or permission bypass was used.

| Guest | Audit | Boot ID | Result |
| --- | --- | --- | --- |
| Online | [selected-stack-boot.O6XFYN](selected-stack-logs/selected-stack-boot.O6XFYN/audit.log) | `b2dcb551-8518-4428-85d7-7675370e921e` | Exit 0 |
| Offline, no NIC | [selected-stack-boot.H6UdCZ](selected-stack-logs/selected-stack-boot.H6UdCZ/audit.log) | `8c9cd832-5bda-4ffe-b878-c9723b6ecb13` | Exit 0 |

Each audit verifies all 16 exact installed core versions and package-file
presence, optional cache hashes, retained optional-feature presence and wallet
policy/data, unchanged gadget layout, active firewalld and Aero7Light.
It hashes the running Gadgets and Action Center executables. For KWin it checks
the wrapper and actual child compositor separately, hashes the library and
verifies that the current library inode is the one mapped by the compositor.
The packaged capability is intact, and the permission-bypass variable is absent.
The UAC service aliases share one process. Shell, Plasma and KWin are active,
with zero restarts and no failed user/system units at both checkpoints.

These are installed-version, file-presence and targeted running-file checks,
not a cryptographic comparison of every installed file. They close the
current guest-selection/cache discrepancy; they do not establish a new
installation sequence or universal desktop/hardware acceptance.

## Log review and retained limits

The complete current user/system journals and previous-boot system journals
are retained with each audit. They are not warning-free:

- Virtual graphics use software fallback, with DRM/EGL/glamor diagnostics.
- XKB reports unsupported/redefined symbols; optional modem, battery/backlight
  and related services report unavailable hardware or backends.
- Auxiliary Plasma processes report portal app-ID registration failures;
  the UAC process retains its protected `/proc` behavior.
- Plasma emits SVG parsing/property warnings, including truncated path data.
  This pass has not identified the source resource or proved their visual
  impact; the diagnostic-triage checklist stays open.
- The online log retains a virtual clocksource watchdog warning.
- An offline QA mount command lost keystrokes during automated typing. It was
  cancelled at the sudo prompt before authorization, then retried at a slower
  rate. The cancellation's PAM diagnostic and
  [terminal evidence](selected-stack-logs/a7-selected-offline-remount-fixed.png)
  are retained. No failed service was reset to make the audit pass.

## Recipe traceability

The read-only [audit script](selected-stack-logs/audit-build-recipes.py) verifies
all selected archive hashes, compares PKGINFO/BUILDINFO package identity, and
matches each retained PKGBUILD hash to the archive's recorded recipe hash.
All 18 pass. Sixteen are still at their recorded locations. Plasma Workspace
3.2's exact recipe is retained in `work/beta2-plasma-splash32.De77sn`; Qt Base's
recipe is retained in `work/beta2-qt-portal.3TA5gw`, instead of its builder-VM
`/var/tmp` location. Matching copies and BUILDINFO are retained in
[recipes](selected-stack-logs/recipes/), with the
[machine-readable result](selected-stack-logs/build-recipes.json).

The audit executes no recipe, fetches no source and extracts no package files.
It is local consistency evidence, not proof of complete source inputs,
reproducible binaries, trusted builder attestation, signed release packages or
repository promotion. Those distinctions must remain in the release review.

## Next gate

The [pre-build checklist](../BETA2-PREBUILD-CHECKLIST.md) now separates completed
guest alignment from source-input reconciliation, native vault prompt overlap,
startup diagnostic triage, requirement/website review and build-space planning.
Final image building still needs approval, followed by testing both exact new
images. No download links, filenames, checksums or promotional screenshots were
invented or published as part of this pass.
