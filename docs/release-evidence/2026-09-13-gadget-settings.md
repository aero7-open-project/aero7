# Gadget Options: live refresh intervals and puzzle preservation

13 September 2026. Scoped bug-fix evidence; not final ISO acceptance or
authorization to commit, publish, or build final images.

## Reproduction and correction

The release-19 source baseline passes 83 gallery results and fails three new
regressions: Weather and Feed Headlines save a 60-minute refresh interval but
leave their running timers at 30 minutes; Picture Puzzle reshuffles when OK is
clicked without changing any settings. Cancelling passes. The baseline is
retained in [baseline19.log](gadget-settings-logs/baseline19.log).

The correction configures the network timer both on startup and after accepted
options. Weather is bounded to 15–360 minutes and Feeds to 5–1440 minutes before
conversion to milliseconds, including values loaded from an edited settings
file. Currency retains its six-hour interval. Cancel leaves the active timer
and saved settings unchanged.

Picture Puzzle now distinguishes the explicit New puzzle button from ordinary
OK. Unchanged options preserve the board, image and move count; changed
difficulty or the selected image starts a new game. Changing the custom image
path only resets the game when the custom image is selected. Adding missing
default fields on the first Options visit does not reset progress.

All eight source groups pass: 99 gallery results, 74 provider results and 11
media results. New coverage includes all nine gadgets' settings serialization,
accepted/cancelled refresh changes, bounded stored intervals, unchanged puzzle
OK/Cancel, keyboard Enter, explicit New puzzle, changed difficulty/built-in or
custom image, cancellation of changed settings, and missing default fields.
Reset checks validate the move counter and tile permutation instead of relying
on a random shuffle differing from a previous one. CPU Meter's row only checks
serialization; it does not imply that CPU Meter has an Options UI.
See [corrected20.log](gadget-settings-logs/corrected20.log).

## Package and installed VM

Normal package build `work/beta2-gadgets20.LPI7zM` completes with all eight
package-check groups passing. The source archive SHA-256 is
`8087a268bedc8b90dfc6a85a39a853f04a0e08802e238eff282d222d5109411e`.
Package `aero7-gadgets-3.0.0-20-x86_64.pkg.tar.zst` SHA-256 is
`4ecf649454a610094ea2e5891eb0d1a4ff5d26b4546389915c3466e80447c842`;
the installed executable SHA-256 is
`10e530ae96f4404b84470a8e9fef47fe95b32a48255f891743a401b2ff4256ab`.
No artwork, icons, dependencies or session launchers were changed for this fix.

Normal VM upgrade `gadgets20-upgrade.SQj6fN` verifies the package identity,
executable hash and all 57 installed paths. The no-NIC Wayland guest retains
KWin 7.3. Private profiles and session buses isolate the settings replay from
the ordinary account layout. These profiles use their own default Options
palette; the screenshots do not establish normal-account theme parity.

Before the upgrade, `gadgets19-settings.znEgPC` reproduces the puzzle reset
through the actual context menu and OK button. After the upgrade,
`gadgets20-settings.EjG8bR` preserves the puzzle: the 250×250 board crop at
(350,250) is pixel-identical before/after OK. Explicit New puzzle then changes
the board. Weather and Feeds both save 60 minutes and show 60 when reopened;
editing each to 90 and cancelling leaves both saved values at 60. Their live
timer intervals are verified by the controlled tests, not by claiming a full
hour elapsed in this native replay. No online provider success is claimed.
Both private replay hosts were stopped normally.

See the [package build](gadget-settings-logs/package20-build.log),
[upgrade audit](gadget-settings-logs/upgrade20.log),
[saved private layout](gadget-settings-logs/native20-layout.json), and screenshots
in [gadget-settings-logs](gadget-settings-logs/).

Normal Start-menu logout/password login passes in `gadgets20-login.xskiot`,
Wayland session 11 on the existing boot
`fde6a493-c3b9-459c-a5c9-47f8afe5cb9c`. Autostart owns PID 23811 with the exact
release-20 executable hash. Shell, KWin and Plasma are active with zero restarts
and no failed system/user units. Compositor permission checks remain enabled,
no private settings/player host remains, and the account layout is byte-identical
to the release-19 login snapshot. This is a normal-login check, not a cold boot.
See [login20.log](gadget-settings-logs/login20.log).

Normalized package MTREE comparison changes only the executable and package
build metadata; installed paths, modes, symlinks, assets and hooks are unchanged.
The next-build manifest now selects Gadgets 20 with KWin 7.3. Its SHA-256 is
`1f912e309234937c4d30776f0285cb4f122ead21d5d1f5480ad3c11ee3f4d233`.
All 149 project integration tests and the remaining static checks pass. Archive
hygiene passes for all 18 online and 53 offline candidate/custom dependency
archives, including the 35 offline repository identity/hash records. See the
[integration check](gadget-settings-logs/integration20.log),
[online check](gadget-settings-logs/online20.log) and
[offline check](gadget-settings-logs/offline20.log).
The Shell pin, optional-feature defaults and frozen ISOs are unchanged.

Broader gadget controls, feed management, Weather Find error paths,
live providers, scaling/multi-monitor, recovery and final-image tests remain
open. This pass does not establish complete puzzle-game persistence across
application restarts, full gadget parity, or release readiness.
