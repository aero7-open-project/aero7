# Automatic output repair — 13 September 2026

The installed Desktop 32 supervisor and session-setup helper pass automatic
layout repair in an isolated three-output virtual compositor. No package or
final ISO was rebuilt for this test, and publication remains on hold.

## Isolation

The first attempt [refused to proceed](display-auto-logs/guard-refusal/run.log):
although D-Bus was private, `systemctl --user` could still reach the ordinary
VM user's service manager through its shared runtime directory. This was
caught before launching the test compositor or supervisor.

The corrected harness uses private runtime, configuration, state, data and
cache directories plus a private D-Bus instance. Its service-manager probe
now [fails to connect](display-auto-logs/corrected-isolation/private-systemctl.txt).
The ordinary session's service manager is deliberately unavailable in this
test. The actual installed supervisor executable and session-setup helper run
unchanged; appearance is initialized from the normal account's configuration.
Initial health confirms the expected Aero appearance and valid layout, avoiding
the appearance-restart branch. The private activity manager, Plasma, KWin and
supervisor are stopped by their recorded PIDs on exit.

## Result

[Run log](display-auto-logs/corrected-isolation/run.log): exit 0.
The compositor exposes three 1280×960 outputs at 100%, 125% and 150% scale.
After initial layout setup, the harness never calls layout repair again.

- Disabling output 2 is followed by automatic repair to two Aero taskbars.
- Re-enabling it is followed by automatic repair to three Aero taskbars.
- Each active screen has exactly one Aero panel with the expected five widgets
  in order. Private KWin, Plasma and the supervisor remain alive throughout.
- The actual [supervisor session log](display-auto-logs/corrected-isolation/supervisor-state/session.log)
  records layout/output reconciliation at 16:26:50 and 16:26:56 UTC.
- The [ordinary-session audit](display-auto-logs/ordinary-session-after/audit.log)
  confirms its Shell, Plasma and KWin service PIDs remain 50786, 50704 and
  37773, respectively, with zero restarts. This test did not replace them.

Reproduction: [outer harness](display-auto-logs/display-auto32.sh) and
[inner harness](display-auto-logs/display-auto32-inner.sh), using the previously
recorded isolated bus configuration. All timeouts and the guard refusal are
preserved as evidence rather than counted as product failures or passes.

## Scope

This establishes the installed supervisor's automatic decision/repair path
with real virtual outputs and real Plasma state. It does not establish
physical connector hotplug, DRM-driver behavior, normal systemd service-manager
interaction during multi-output changes, mixed-DPI visual legibility or
multi-output screenshot/input behavior. The separate normal-session recovery
test covers service-owned shell restart, not those physical cases.
