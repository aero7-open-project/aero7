# Desktop 28 — live layout repair and splash caller trace

Local release-candidate work. No commit, push, signing, publication or new ISO.
Final media and broader acceptance remain pending.

## Confirmed cause and scope

The normally installed Desktop 27 health service sends every layout or
appearance repair to `aero7-session-setup --reconcile-only`. That path always
restarts Plasma. This includes a layout/output correction during login, after
the initial splash has already completed successfully.

A scoped 20-second D-Bus trace in the disconnected r9 VM identifies the late
caller, rather than merely correlating timestamps. Following a controlled shell
restart, the owner of `org.kde.plasmashell` was `:1.163`, PID 2329, also reported
as the systemd service's MainPID. The captured call from that exact bus name was
`org.kde.KSplash.setStage("desktop")` at 19:12:02 CEST. The trace filtered only
that method/destination; the monitor's own name-acquired/lost signals are also
present. It did not capture general user-session traffic.

The first tracing attempt used an incorrect D-Bus object path for the identity
query. The corrected trace uses `/org/freedesktop/DBus` and completed normally.
The guest had been stopped by the host between sessions; it was resumed from
its existing disk without reinstalling or replacing the disk.

## Correction

- Added `--reconcile-layout-only`, applying the real layout script and wallpaper
  live, without rewriting appearance or restarting Plasma.
- The health service selects this mode only when appearance is already valid.
  Invalid appearance still uses the existing reload and post-reload layout path.
- Initial login continues to apply visual defaults without restarting the shell.
- Extra command-line arguments are rejected before changing state.

This removes an unnecessary restart path. It does **not** fix Plasma's late
splash activation after every possible legitimate restart: dark/light global
theme recovery may still need a reload, and the installed `plasma-workspace`
caller does not suppress D-Bus auto-start. That remaining lifecycle fix must not
be replaced by disabling the splash or masking its failure.

## Regression and package evidence

The actual setup script executes under isolated command doubles with redirected
absolute resource paths. Before correction, live-layout and extra-argument tests
failed; the existing initial-login and appearance-reload cases passed. New health
helper tests also failed before the new interface existed. After correction,
all four execution tests and ten health tests pass, including a supervisor
decision matrix for layout-only, appearance-only, combined and healthy state.

All seven source CTest groups passed (13.98 seconds); all seven frozen-package
groups passed again (14.89 seconds), including the new execution suite.
Shell syntax and repository whitespace checks pass. ShellCheck still reports
the pre-existing unused `attempt` loop-variable warning; no claim of an entirely
warning-free source tree is made.

Frozen local build: `work/beta2-desktop28.iLyM8b`.

- Package: `aero7-desktop-0.2.0-28-x86_64.pkg.tar.zst`, 1,984,580 bytes.
- Package SHA-256: `3833ddbc7ccc7a4998e6b8310cbac6314999c32d4690602423b5ff1b7dcae63f`.
- Source archive SHA-256: `4d245d663befa60b0700bd9cfb5dc715607470879bede25a243548bf961c7e3e`.
- Completed: 7 September 2026, 19:13:58 CEST.

The local snapshot uses current tracked and nonignored new source files, excluding
deleted/ignored build products. The recipe preserves the earlier local package's
dependency and File Explorer ownership boundary. No remote source commit or
repository pin was invented; the published repository recipe remains separate
until source publishing is approved. The immutable Shell checkout is unchanged.

## Installed VM status

Normal dependency-checked upgrade from Desktop 27 to 28 passed in the offline
guest. Only the Desktop package changed. Integrity checks show zero altered files
for Desktop (73), Theme (1,143), Explorer (665) and Paint (709). The existing
Paint settings checksum is unchanged. Three successive real live-layout repairs
retained Plasma PID 2329, with valid layout/appearance reported afterwards.

The VM then rebooted normally. Boot IDs differ:
`982cea9d-2ff0-492f-aa1d-6dba28c945de` before,
`dd750f37-8d7d-4179-9b84-b8140786fdf8` after.
The new session started Plasma once (PID 794), with no subsequent stop/restart
in its journal. The splash finished successfully at 19:17:39 after 3.208 seconds.
The audit ran more than 80 seconds after shell activation, beyond the previous
timeout window: no late KSplash activation failure, valid health, and zero altered
files in all four audited packages. The failed-user-unit list was empty at that
point; this does not prove absence of all journal warnings.

Screenshots `323-desktop28-reboot-login.png`,
`324-desktop28-new-boot-desktop.png` and `328-desktop28-reboot-audit.png` are in
`/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`. The exact report/logs are copied
to `desktop-live-layout-logs/`, including `desktop28-reboot.rRtdmy/` and the scoped
trace `splash46-trace.AQTGKb/`.

The next-image manifest now selects Desktop 28. ISO static checks pass, including
135 backend tests and the theme branding gate. All 13 selected online candidate
archives pass identity/hash and unsafe-path checks. Neither ISO has been rebuilt
with this package yet. Appearance-recovery checks are recorded separately below.

## Appearance regression

The installed VM applied `BreezeDark` through `plasma-apply-colorscheme`, the
same backend used by the Control Panel Personalization page. Health recovery
reloaded Plasma from PID 794 to 2384 and selected `KvDark`. Returning to the
saved original `Aero7Light` setting reloaded it to PID 2719 and restored
`Windows7Aero`. Both checks waited for the actual target scheme, active shell
and valid layout/appearance; they did not count merely issuing the command as
success. Screenshots 330 and 331 show the surviving desktop and test output.
These are backend/recovery checks, not complete application-color parity tests.

The normal-boot audit was captured before these intentional reloads. Its clean
splash result must not be generalized to the post-theme-change journal, exported
separately as `desktop28-post-appearance.log`. This preserves the remaining late
caller defect instead of resetting failed units or suppressing journal evidence.
That journal confirms activation at 19:21:23 and failure at 19:22:24 after the
dark-mode reload. The desktop remains healthy and restored to Aero7Light; the
underlying Plasma splash call still needs correction. All 48 offline candidate
and dependency archives also passed validation, with all 35 offline repository
entries matching their package identities and hashes.
