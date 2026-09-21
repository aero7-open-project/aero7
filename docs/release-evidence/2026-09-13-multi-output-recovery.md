# Three virtual outputs and shell recovery — 13 September 2026

Local QA only, against installed Desktop 32, Control Panel 54, Gadgets 23,
KWin 7.3 and Plasma Workspace 3.2 in the offline Wayland VM. This does not
authorize publication or building the final ISOs.

## Isolation and harness findings

The three-output test uses the installed compositor and Plasma executables,
a unique Wayland socket, private configuration/state/cache/data directories,
and a private D-Bus session without service activation directories. An activity
manager is started explicitly on that private bus. Only the recorded test
processes are stopped during cleanup. The ordinary VM session is not replaced.
The outer harness has a 180-second limit with a bounded termination grace.

The [first attempt](display-multi-recovery-logs/initial-harness-failure/run.log)
could not validate the layout because the guest has no `jq` and the isolated
bus did not start an activity manager. Plasma explicitly reported aborting
its shell load for that missing daemon. The harness now preflights the tools,
uses the existing Python JSON parser, and starts the private activity manager.
This was a harness failure, not evidence of a normal-session desktop bug.

The next [windowed attempt](display-multi-recovery-logs/windowed-scale-limitation/run.log)
had the correct three taskbars, but all output scales remained 1. Inspection
of the selected KWin 7.3 source, `src/backends/wayland/wayland_output.cpp`,
`WaylandOutput::applyChanges`, establishes that this backend intentionally
ignores requested scale changes because the parent fractional-scale protocol
controls them. A successful command exit was therefore insufficient proof.

## Virtual-framebuffer result

The corrected test uses KWin's `--virtual` backend with three 1280×960 outputs.
[Run log](display-multi-recovery-logs/virtual-three-output/run.log): exit 0.

- Initial state has three Aero panels, one on each screen, each containing
  Seven Start, tasks, tray, clock and Show Desktop in that order. All desktop
  containments use the Aero type.
- Backend JSON confirms three separate scale values of 1, 1.25 and 1.5, with
  the exact panel/widget layout retained:
  [mixed-scale outputs](display-multi-recovery-logs/virtual-three-output/mixed-scale-outputs.json),
  [layout](display-multi-recovery-logs/virtual-three-output/mixed-scale-layout.json).
- Disabling one output and explicitly running the installed layout script
  restores one Aero panel per remaining screen. Enabling it and running the
  same script restores three panels.
- Stopping and restarting the private Plasma process preserves three panels
  without an additional explicit layout-script invocation after restart.

The [outer](display-multi-recovery-logs/display-multi54.sh) and
[inner](display-multi-recovery-logs/display-multi54-inner.sh) harnesses and
[isolated bus configuration](display-multi-recovery-logs/gadget-isolated-session.conf)
are preserved. This is live backend/layout evidence, not visual legibility or
physical mixed-DPI acceptance. The output-change steps explicitly reconcile
layout; they do not prove automatic production-supervisor hotplug handling.

## Normal-session recovery

A separate guarded test targets only the normal VM user's service-owned
`plasmashell` PID after checking its owner, executable, singleton process and
Aero shell identity. One injected crash is followed by an explicit
`aero7-recovery restart-shell` check. The [run](display-multi-recovery-logs/normal-recovery/run.log)
passes with exit 0, including 30 subsequent checks at two-second intervals.
The final layout/wallpaper JSON is byte-identical to the pre-crash snapshot.

The [journal](display-multi-recovery-logs/normal-recovery/journal.log) confirms
that systemd automatically restarted the killed Plasma process, PID 37875,
as PID 50571. Do not attribute that restart specifically to the health-service
poller. The explicit recovery command then starts Plasma PID 50704 and the
health service PID 50786. KWin's wrapper and actual compositor retain PIDs
37773 and 37778; Paint and Terminal also retain their original PIDs. All three
desktop services remain active during the 60-second follow-up. The intentional
SIGKILL failure/restart is preserved in the journal, not erased from the result.

The [guarded harness](display-multi-recovery-logs/recovery54.sh), before/after
processes, backend outputs and layouts are retained alongside the
[visible follow-up](display-multi-recovery-logs/a7-recovery54-followup.png).
This checks one recoverable crash and one explicit restart, not a repeated
crash loop, sustained compositor failure or every recovery-UI action.

## Remaining boundaries

Physical connector hotplug, actual graphics drivers, multi-output input/capture
behavior, automatic output repair under the production supervisor, repeated
crash-loop behavior and exact final-image acceptance remain separate gates.
These tests neither rebuilt media nor changed the selected package manifest.
