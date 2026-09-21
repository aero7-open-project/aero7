# Plasma splash lifecycle — candidate 3.2 scoped VM pass

This follows the confirmed caller trace and Desktop 28 live-layout correction
in [the preceding report](2026-09-07-desktop-live-layout-repair.md).
No commit, push, signing for distribution, new ISO, or release publication.

## Correction under test

The local Plasma Workspace checkout now sends desktop-readiness progress without
requesting D-Bus service activation. A bounded passive registration watcher still
allows the normal session splash to register slightly later. A one-shot guard
and in-flight request guard prevent repeated readiness calls or a registration
race from delivering duplicate progress. QObject ownership cancels the pending
registration wait when its shell context is destroyed. Already-sent bus messages
cannot be recalled; the destruction test explicitly accounts for that boundary.

The splash itself is not disabled, its errors are not masked, and no arbitrary
startup delay is inserted. The notifier is owned by ShellCorona.

## Source and recipe provenance

- Upstream Plasma tag `v6.7.4`: `fd05f4c88ab093aee23ce137bf6f2412437c9bba`.
- Exact Arch packaging tag `6.7.4-3`, commit
  `3aeb231d7dd8214e46155f922c7d04ecbadc19cd`.
- Original recipe SHA-256:
  `372cb7dda8d4055e60febf279252bf0489b06a6cb63bc51742a158477f01c678`.
- KDE source archive SHA-256:
  `21ec3c002929eb65377a1ae0eb105b9ab6f608049dac5493e188f51bd50398d5`.
- Detached signature validates with signing subkey
  `B3CB366552540BE06EE9AD9711968C44928CAEFC`, primary fingerprint
  `0AAC775BB6437A8D9AF7A3ACFE0784117FBCE11D`, allowed by the original recipe.
  Verification uses an isolated keyring; the host keyring is unchanged.
- Local patch SHA-256:
  `05bbf5e48b92bdde06b170e8860accc8c84d8e2c31fa3575a61277cf5b4119c6`.
- Standalone package test CMake fixture SHA-256:
  `b3c2c56f8596be593dd6f4aee939ff8e95cd0d282ff40129dfed39fdeea8b08f`.

The local recipe keeps the complete workspace and X11-session split packages
and runtime dependencies, with unpublished candidate release `3.1`. It does not
replace a loose system binary. Debug package generation is disabled to limit
build storage. The full build uses two jobs and the normal Arch CMake options.
Host dependency prechecking is skipped with `makepkg --nodeps`; source checksum
and signature verification and compilation run normally. No host packages were
installed. Normal dependency checking remains required for the VM upgrade.

## Isolated regression evidence

The test executable starts its own private D-Bus daemon, service directory and
activation probe; it does not inspect or mutate the host session bus.
Six functional cases cover absent service, existing service, delayed registration,
expired wait, registration during an in-flight call, and context destruction.

- Final fixture with auto-start restored: **4 pass, 4 fail**, including test
  initialization and cleanup. This demonstrates that the fixture detects the bug.
- Corrected implementation: **8 pass, 0 fail** (6 functional cases plus setup
  and cleanup), 931 ms.
- Ten consecutive corrected executions: **all 10 passed**, each reporting
  8 pass and 0 fail.
- Repository whitespace check passes; the immutable Shell checkout stays clean.

Evidence directory: `work/beta2-plasma-splash.HlnTDU/`.
Logs: `splash-final-fixture-red.log`, `splash-green.log`,
`splash-repeat-green.log`, `source-signature-verification.log` and
`plasma-splash-package.log`.

## Pending acceptance

The offline r9 VM preflight completed without installing anything. Its baseline
`plasma-workspace 6.7.4-3` reports **6,785 files, zero altered files**. The shell,
splash executable and D-Bus service file are owned by that package. Desktop 28
and Theme 46 remain installed. The guest's missing remote sync-database warnings
were recorded without refreshing repositories in this disconnected test guest.
Completed regression, signature and guest-preflight logs are also copied into
`plasma-splash-logs/` beside this report.

Prepared VM-only helpers under the r9 QA `inputs/` directory:

- `install-plasma-splash.sh`: verifies both candidate and rollback identities
  and checksums, checks baseline integrity, saves the rollback archive inside
  the guest, then uses a normal dependency-checked local package transaction.
  It compares all installed package versions and Paint preferences afterwards.
- `audit-plasma-splash-login.sh`: verifies the installed candidate, cold-login
  health beyond 80 seconds, splash service result, and absence of late activation
  failures or unnecessary shell restarts. It exports the remaining warnings.
- `check-plasma-splash-appearance.sh`: tests real dark/light backend changes and
  the resulting shell reload, observing each for another 80 seconds while
  checking that the recovered shell PID remains stable. Failure restores the
  original light scheme; success requires an explicit restore pass afterwards.

All three helpers pass Bash syntax and ShellCheck, and reject execution on the
host with exit status 2. The rollback archive in the QA share matches the pinned
baseline SHA-256. The upgrade helper has since executed, as recorded below;
the other helpers remain preparation checks, not graphical acceptance results.
The candidate is not selected in the ISO
manifest yet. The existing packaging path can install a declared local workspace
candidate after its base package; exact final-media content still needs checking.

The full package build completed successfully on 7 September 2026 at 20:10:05
CEST. Its check stage compiled the test against the exact prepared package
source and passed the lifecycle CTest (0.94 seconds).

| Unpublished local artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| plasma-workspace-6.7.4-3.1-x86_64.pkg.tar.zst | 25605576 | d2ce1203ec57026ae19210859f2da3e9404fa32a9fa2619245e2bde6854fb2d0 |
| plasma-x11-session-6.7.4-3.1-x86_64.pkg.tar.zst | 13625 | 0a6822d179b6c523a8ace05084ed4e8245ff1b72477550473f2065ea56c722f1 |

The workspace archive's sorted file list exactly matches the original Arch
6.7.4-3 package. Normalized package metadata also matches after excluding only
version, build date, packager and size; dependency declarations are unchanged.
The archive verifier confirmed its checksum and identity and found no forbidden
VCS or unsafe archive paths. The completed build log is preserved with the other
evidence. The workspace package is copied to the local package directory and
VM QA share, but not selected in the ISO manifest yet. The optional X11 split
package was built but is not selected for this Wayland VM upgrade.

## Candidate 3.1: normal upgrade passed, graphical acceptance failed

The guarded upgrade completed normally, with only plasma-workspace changing.
All five checked packages reported zero altered files and Paint settings were
unchanged. Evidence: `plasma-splash-logs/plasma-splash-upgrade.LI1qOl/`.

After reboot and password login, the apps area disappeared and the taskbar
collapsed to approximately 300 pixels. The guest journal identified both failed
QML imports: Seven Tasks and Notifications could not load because
`libflatpak.so.0` was absent. Configuration/process-only health still reported
valid; that is not a substitute for applet-rendering acceptance.
Evidence: `plasma-splash-logs/plasma-candidate-diagnostic.BBlwMY/`.

Comparing direct ELF requirements for **all 152 ELF files** against the original
Arch archive finds one changed file: `libnotificationmanager.so.6.7.4` acquired
dependencies on libflatpak, libglib and libgobject. The original build metadata
does not contain Flatpak. Upstream CMake auto-detects the host's Flatpak SDK;
the unchanged runtime package declarations therefore missed the new dependency.
Identical package file lists and metadata did not catch this contamination.

The VM was rolled back with normal package dependency checks using the retained,
checksum-verified 6.7.4-3 package. Only that package changed, all five integrity
checks passed and Paint settings remained unchanged. After reboot and password
login, the full-width taskbar and pinned application buttons returned.
Evidence: `plasma-splash-logs/plasma-splash-rollback.WLzDeC/`.
Screenshots 366 and 367 under the r9 offline QA directory record login and desktop.

## Candidate 3.2: explicit baseline build configuration

The source now has a default-on `BUILD_FLATPAK_INTEGRATION` build option. The
local Arch-compatible recipe explicitly switches it off to match the original
package. This controls optional discovery of notification settings inside
Flatpak installations; it does not remove Flatpak applications, ordinary
notifications, or any feature previously enabled in the baseline package.
No host or guest Flatpak package is added to hide the dependency problem.

Additional patch SHA-256:
`e7617fdda7d16104113dffe08c5ead3d6c6f4dbd5b0e45f454901c14309ff463`.
Recipe and evidence: `work/beta2-plasma-splash32.De77sn/`.
All source checksums and the KDE signature verify. The corrected configuration
generates `HAVE_FLATPAK 0`. The incremental build reuses the prepared 3.1 source
and build directory after applying exactly this extra patch; its original
recipe, archives and logs are preserved, and 3.2 artifacts go to a separate
directory. A fresh build can use the complete 3.2 recipe and verified sources.

Candidate 3.2 packaging completed at 20:32:51 CEST on 7 September. Its lifecycle
CTest passed in 0.95 seconds. Fresh extraction and `prepare()` from the separate
recipe produced an identical source tree (comparison does not dereference the
upstream intentionally recursive symlink test fixture).

| Unpublished local artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| plasma-workspace-6.7.4-3.2-x86_64.pkg.tar.zst | 25603571 | d586c6f0a3e9ccdd1dde50628621ddc163ece25371286bed5dc9be74ad2f2e09 |
| plasma-x11-session-6.7.4-3.2-x86_64.pkg.tar.zst | 13620 | 3f0b6d6d0347e699a7be85389097166fbfd70c5488db2664a3feb9938b830ab6 |

Direct ELF requirements in the **final extracted 3.2 archive** match the
baseline for all 152 binaries, with no changed entries. Normalized package
metadata also matches. The new readelf-based checker has seven passing unit
tests; it rejects the actual 3.1 archive's library change and passes the baseline
self-comparison. All **142 ISO Python tests pass**. These checks do not prove
ABI compatibility or complete runtime dependency closure by themselves.

The 3.2 VM upgrade completed with normal dependency checks and no unrelated
package changes. All five package integrity checks pass, Paint settings are
unchanged, and guest linkage checks of plasmashell, notificationmanager and
both affected applet plugins find no missing runtime libraries. Evidence:
`plasma-splash-logs/plasma-splash-upgrade.CmwCIw/`.

## Candidate 3.2 cold login

Boot ID: `19454a89-aebf-42a1-9ea6-24dbee866a0b`. Password login produced the
complete full-width taskbar and pinned app buttons. The initial splash starts
at 20:36:25 and finishes normally at 20:36:28; its service reports success and
exit status 0. Plasmashell PID 797 starts once, and the audit beyond 80 seconds
passes without late splash activation failures or failed user units. The
notification service owns its bus name, and neither affected applet reports a
load or missing-library failure. Evidence:
`plasma-splash-logs/plasma-splash-login.DqW4Os/`, screenshots 372–378 in r9 QA.

This is a scoped startup pass, not a warning-free desktop claim. The retained
warning log still has 85 lines, including task-model QML bindings, portal
registration warnings and virtual-GPU/audio limitations; they need separate
triage. Health configuration alone did not catch candidate 3.1's broken applets.

### Appearance harness correction

The first dark-mode pass changed PID 797 to 2087 and retained that PID through
80 seconds, but the harness exited 1 when `journalctl -g` found **no** splash
messages. Its saved activation log contains only `-- No entries --`; no shell
log was collected because `set -e` stopped execution at that command. The
failure trap restored Aero7Light. This result is not counted as a completed
appearance acceptance pass. Evidence: guest results `plasma-splash-dark.6uXGyn/`.

The VM-only harness now collects the complete user journal first, preserving
journal read errors, then permits only grep's no-match status when filtering
splash messages. It also records failure line/status and exports logs on both
success and failure when noninteractive authorization is available. ShellCheck
passes. The corrected dark/light sequence is being rerun.

The corrected dark run completed successfully: recovered PID 3151 stayed
unchanged through 80 seconds, no splash activation messages were recorded,
the notifications service remained available and applets had no load failures.
The selected settings were BreezeDark and KvDark, with valid appearance/layout
health. Exit status 0; evidence: `plasma-splash-logs/plasma-splash-dark.x4AGzf/`.
The original Aero7Light restore is being checked separately.

The light restore also completed successfully: PID 3797 stayed unchanged for
80 seconds, the selected scheme returned to Aero7Light and Kvantum to
Windows7Aero, and both appearance and layout health were valid. There were no
late splash activations or applet load failures, and the notification service
remained available. Exit status 0; evidence:
`plasma-splash-logs/plasma-splash-restore.vQEQT7/`.

After restoring light mode, clicking the pinned Explorer icon opened the
branded File Explorer window (screenshot 382). A `notify-send` test displayed a
visible Aero-style notification at bottom right (screenshot 384). These are
scoped runtime smoke checks, not another full Explorer/screenshot acceptance
matrix. The opened Explorer window was closed normally; no user files changed.

The original late-splash regression now has source, package, cold-login and
real dark/light reload evidence in this modified offline VM. Remaining work
includes warning triage, pending Explorer storage fixes, broader recovery and
display tests, and both final ISO rebuilds/fresh-install acceptance. Candidate
3.1 must not be promoted. Neither candidate has been committed, published or
selected in the ISO manifest. The active VM retains 3.2 with Aero7Light restored
and a checksum-verified baseline rollback archive inside the guest.
