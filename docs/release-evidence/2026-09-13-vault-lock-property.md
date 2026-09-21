# Optional vault: reject malformed lock-state values

13 September 2026. Source fix, package build, isolated backend verification and
native package-upgrade/locking checks. The optional manifest now selects Vault 7.
No final ISO or published package changed; broader acceptance remains open.

## Reproduction

The backend already required a real boolean for lock-completion verification
and service-level collection-change handling, but `collectionLocked()` and
`PropertiesChanged` handling coerced other variant types with `toBool()`.
A mock collection returning the string `"false"` therefore left the UI unlocked
before initial unlock completion, before listing entries and after a malformed
property-change notification.

The new isolated tests reproduce all three failures against the original
backend. The existing strict service-change path and the valid boolean-false
control pass. Baseline: 14 backend results pass, 3 fail. This is a protocol
failure-injection finding, not evidence of real credentials being disclosed or
of the normal KWallet service emitting malformed values.

## Correction and checks

Both remaining paths now require `QMetaType::Bool` before accepting an unlocked
state. Unknown types drop local access through the existing disconnect path;
valid `false` notifications still preserve access. This does not claim that
losing local access proves the underlying service has encrypted/locked its data.

- Fixed host build: 9 UI and 17 backend results pass, with no failures/skips.
- Native VM replay: 17 backend results pass in
  `vault-lock-type.Th9BWK`, exit 0, on Wayland.
- The replay uses a private D-Bus with no service activation directories, a mock
  wallet and temporary test account configuration. The real optional vault stays
  absent/disabled. Desktop service PIDs and restart counts are unchanged.
- Test executable SHA-256:
  `fcf25798d3da697eadddf230f8f25fa7a47d83cd7ce12727223dc7aa95871be2`.

Evidence, the original backend, test source and replay script are retained in
[vault-lock-type-logs](vault-lock-type-logs/). The initial harness build missed
the explicit `QDBusReply` include; its compiler error and corrected build are
retained separately from the actual product regression baseline.

## Package and remaining work

The local release-7 package build completed with both CTest groups passing.
The 20-file source inventory comes from the companion's Git-visible files and
excludes its generated build tree. An initial tar invocation placed `-C` too
late and failed; the retained empty failed archive was not used by makepkg.
The corrected archive was listed, hashed and pinned before building.

- Source SHA-256:
  `e916697d6c16d8efdcf14fb0350aeae5c66c42ef14e112727ad067f4f829d9d2`.
- Package: `aero7-credential-vault-0.1.0-7-x86_64.pkg.tar.zst`.
- Package SHA-256:
  `55cae7104828152b935e3b72315dd588a898c48b12072a05039708e5aaa0e50e`.

## Installed application and optional cache

The existing online QA VM was started after the offline guest shut down normally;
only one 6 GiB guest ran at a time. Boot ID:
`e0eaef5a-b3e2-43a1-af01-f8beaad758c0`. This guest has KWallet 6.29.0-1 and the
existing synthetic `qa-recovery.invalid` credential. It is not the same core
package selection as the more recently updated offline guest.

`vault7-upgrade.uymw7J` passed normal dependency-enforcing `pacman -U` from 6 to 7,
all 25 installed-file checks and executable hash verification. The saved encrypted
wallet files remained byte-identical across upgrade. Desktop service PIDs and
restart counts were unchanged. Installed executable SHA-256:
`b49e4aa2e4b610021778d03120f46430a87369b90696d08db734038fed587105`.

Two release-7 processes (2968/2969) opened locked. The first required the original
QA wallet password; the second attached to the unlocked same-user wallet. Both
listed the retained credential. The right window's editor initially masked its
password; explicit Show password revealed it. Lock in the left window closed
that editor, cleared both lists and disabled editing in both windows. Neither
credential contents nor the wallet password were changed. An accidentally opened
empty Add dialog was cancelled without saving. Both application processes exited
normally. `vault7-final.bXVrFG` independently confirmed the actual collection
property `Locked=true` and the 25 installed files, with exit 0.

The replay's first harness, `vault7-two-clients.9QcZM5`, failed to read a protected
process executable as an ordinary user. The corrected replay uses privileged
read-only hash verification; the application's process protection was not changed.
`vault7-two-clients.x4MGme` passed its hashes, normal exits, collection lock and
unchanged-service checks, but exited 1 on the final zero-failed-user-units assertion.
Do not describe that whole script as a green run.

The retained final diagnostics identify the single failed unit as
`app-sudo@88b23808afd646ef82b8756e939086e1.service`: the QA mount command reached
the desktop launcher before Terminal opened at 20:21:16, and sudo correctly
refused authentication without a terminal. This predates the vault upgrade and
replay. Its exact command, exit status and journal are retained; it was not
reset merely to make the audit green. Vault logs retain the known protected-proc
portal-registration warning. Shell, Plasma and KWin stayed active with unchanged
PIDs and zero restarts during the replay.

`vault7-cache.DRKJCj` verifies the exact release-7 package and digest sidecar in
the online guest's optional cache. The next-build manifest selects that package;
the offline guest's existing cache remains at 6 until refreshed. Nothing enables
the vault by default in future installs. Current manifest SHA-256:
`36d3c6a00f369ff6f86cfde5124e7b712fffebe8ad3b111ffb88dc862f543258`.

All 149 integration tests, static checks, 18 online archive checks, 53 offline
archive checks and 35 offline repository identity/checksum checks pass again.
Broader vault failure-path review and final-image acceptance remain open. This
pass does not claim a release-7 cold reboot, fresh install, all multi-client
interleavings or alternative KWallet configuration acceptance.
