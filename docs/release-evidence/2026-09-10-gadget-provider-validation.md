# Gadgets: provider validation, cached readings and puzzle options

10 September 2026. Local pre-release work only; no final ISO, commit, push or
publication. Extends the [runtime follow-up](2026-09-10-gadget-runtime-followup.md).

## Reproduced failures

The [provider baseline](gadget-provider-logs/gadgets-provider-baseline.log) has
15 failing cases. Actual RuntimeServices request callbacks accept null/string
temperatures, missing/fractional/unknown condition codes, invalid observation
timestamps and successful-looking bodies from failed requests. Missing forecast
values become zeroes. Invalid fresh caches suppress replacement requests;
future cache timestamps count as fresh, and failed refreshes do not report their
failure when an older reading exists. Currency similarly accepts an error body
or undated rate and trusts an invalid cached rate. Two successful-response/cache
control cases already pass, so the fixture does not simply reject all replies.

The test substitutes a private QNetworkAccessManager at construction, while
retaining the real request building, callbacks, signal emission and cache code.
Its replies use no socket or external provider. Each case owns a temporary cache;
the test runs on an isolated session bus with activation disabled. Production
still constructs the normal Qt network manager with the same timeout/redirect
policy; no runtime URL override or testing switch is added.

Picture Puzzle has a separate numeric/string round-trip defect. Both 3×3 and
5×5 [regressions fail](gadget-provider-logs/gadgets-puzzle-baseline.log), while
4×4 passes. In the installed release 8 VM, selecting 5 saves `difficulty: 5`,
but [reopening Options shows 4](gadget-provider-logs/a7-puzzle8-reset.png).
Cancel preserves the [saved layout](gadget-provider-logs/puzzle5-before-upgrade.json).

## Corrections and controlled coverage

- Current readings and cached readings require finite numeric temperatures or
  positive rates and valid observation dates/times. Invalid caches cannot stop
  replacement requests. Future cache-write times are not fresh.
- Weather conditions follow the provider's documented discrete code set, not
  every integer from 0 through 99. All 28 supported codes have acceptance tests;
  unassigned codes have a rejection test. Field types and timestamp expectations
  are checked against [Open-Meteo's primary documentation](https://open-meteo.com/en/docs).
- Failed or oversized replies cannot become successful observations or replace
  a valid cache. A failed refresh retains a valid previous reading, marks it
  stale and reports the failure. Genuine zero-degree readings remain valid.
- Incomplete or malformed forecast entries are omitted, not filled with zeroes
  or a made-up condition. The same filtering applies when reading the cache.
- Puzzle Options restores its numeric difficulty correctly.

Release 9 passes all five CTest groups, including 52 provider and 19 gallery
Qt results (each total includes setup/cleanup). See the
[package tests](gadget-provider-logs/package9-tests.log). These are controlled
contract tests, not claims about successful live provider connectivity.

## Release 9 package and installed checks

Final release 9 candidate source SHA-256:
`cde8c60bb9f66e2815893d82931cddde2219191079f09a3050a16f3594ba5898`.
Archive SHA-256:
`08698e9ada8526cc8b34090c4bd284db65338b846c369201e2b7ef9c62725510`,
352,881 bytes. Installed binary SHA-256:
`d3ca8502d2087ad172e42028ec6947b50e3e1c6f00667701f73c03e277f52d72`.
The [full build](gadget-provider-logs/package9-build.log) uses two jobs and normal
dependencies. The [normal offline upgrade](gadget-provider-logs/package9-upgrade.log)
passes without dependency/conflict overrides and verifies all 57 installed files.
The archive retains all 61 paths, owners, modes and symlink targets. Comparing
its normalized MTREE to release 8 changes only package/build metadata and the
host executable, not icons, gadget data, hooks or licenses.

`work/beta2-gadgets9.aM5AfY` is a preliminary build before discrete-code validation;
it was never installed or selected. The installed archive above is from
`work/beta2-gadgets9-final.tmxmoY`. Neither is selected in the next-build manifest.

The disconnected VM remains Wayland 1920×1080, boot
`dcf96047-1c04-4efa-8bbd-5317c1fe084b`, session 8. Private QA profile
`gadget-provider-profile.7muMfF` contains synthetic historical cache fixtures:
zero degrees, a rate of 1.25, two valid forecasts and one null forecast value.
These are not actual weather or financial information. The installed host
restores all nine gadgets, preserves the [5×5 selection](gadget-provider-logs/a7-puzzle9-fixed.png)
when accepting unchanged Options, and keeps the complete layout byte-identical
at that point. Real no-NIC request failures occur in the
[runtime log](gadget-provider-logs/cache9-runtime.log); both cache files remain
byte-identical to their fixtures. The [large Weather view](gadget-provider-logs/a7-weather9-forecast.png)
shows the two valid forecast entries and no invented third temperature.

## Installed presentation correction and next-build selection

The [native cached-reading replay](gadget-provider-logs/a7-gadgets9-cache.png)
exposes a clipped small Weather failure label and Currency's missing stale-data
indicator. Four real-painter
[badge regressions fail](gadget-provider-logs/gadgets-cache-label-baseline.log).
The current correction adds compact Cached/Cached rate labels in both sizes,
reserves Currency footer space, and elides condition text to its actual bounds.
Small Weather also shows the cached observation's date and time. The expanded
[gallery suite](gadget-provider-logs/gadgets10-gallery-tests.log) passes 23 Qt
results. Release 10 builds and upgrades normally with all five test groups,
52 provider results, 23 gallery results and 57 installed-file checks passing.
Its normalized MTREE retains release 8's paths/ownership/modes/symlinks and
non-executable content; no artwork or icons are changed.

Source SHA-256: `59c2f9371682bdc96719cb6f29426f112717ab322b9415f63556db2b5ab7eac0`.
Archive SHA-256: `a925fac43f1a6b6c3d76b6ee4bdafe8acf17454af44f0c2b54baf018b33ab056`,
352,809 bytes. Installed binary SHA-256:
`300fa11763fb7a9e2dc82ae5684d7b1ea6ab8436391c22c5d36e7a17cbef1597`.
Evidence: [build](gadget-provider-logs/package10-build.log),
[tests](gadget-provider-logs/package10-tests.log) and
[normal upgrade](gadget-provider-logs/package10-upgrade.log).

New isolated profile `gadget-provider-profile.UTXiOQ` runs that installed host
with the same synthetic cache fixtures. Both the
[small views](gadget-provider-logs/a7-gadgets10-cache.png) and
[large views](gadget-provider-logs/a7-gadgets10-both-large.png) show readable
Cached/Cached rate labels. Weather still displays only the two valid forecasts.
The [real disconnected failures](gadget-provider-logs/cache10-runtime.log) leave
both cached files byte-identical. An initial attempt to drag Currency through
its amount field opened the expected amount editor; Cancel preserved the value,
then its drag handle was used before resizing. This is not counted as an amount
editing or exact-position regression test.

Release 10 replaces release 8 in the next-build manifest. Manifest SHA-256:
`1b9b617fdfd5afd9ce9d08d629fcd539cf0dfa0004fbd681d018dd503be222d9`.
The required/optional lists remain unchanged: 18 selected archives, 16 required,
two optional; Vault and Programs Center remain off by default. The
[full integration checker](gadget-provider-logs/integration10-check.log) passes
all 149 tests plus its package, dependency, ownership, syntax, branding, Shell
pin and ShellCheck checks. This selects local build inputs, not public packages
or an ISO.

After stopping the private host, normal Start-menu logout reached
[SDDM](gadget-provider-logs/a7-gadgets10-sddm.png). Normal password login and the
[running-binary audit](gadget-provider-logs/login10-audit.log) pass for release 10.
The session-bus service owner is the normally autostarted host, with the exact
release 10 executable hash and no QA config/cache override. All 57 installed
files are present, the account layout remains empty, Shell/KWin/Plasma have zero
restarts, and system/user failed-unit lists are empty at the snapshot. No manual
host launch preceded the audit. This is a new normal session, not a cold boot or
fresh-install test.

## Remaining scope

Live provider success, request-identity/race handling when location or units
change, feed parsing/recovery, media integration, remaining gadget controls,
scaled/cross-monitor behavior and the broader desktop/security/recovery gates
remain open. Release 10 normal-account autostart is verified above; release
9's installed private-profile run is not a cold-boot check. No final
media has been assembled, and the public release remains on hold.
