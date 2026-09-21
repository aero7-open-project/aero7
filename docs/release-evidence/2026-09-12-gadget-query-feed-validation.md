# Gadget request identity and feed validation — 12 September 2026

Status: source regressions, package build, normal upgrade, native query/feed
checks and normal-login autostart pass. A further Show Desktop defect is
reproduced below. This does not approve final ISO assembly or publication.

## Reproduced failures

The pre-fix real-service fixture run produced 54 passing and 14 failing Qt
results. The focused real-window run produced two passing and six failing
results. These totals include setup/cleanup; they are test cases, not a count
of distinct bugs. An additional click-handler regression failed in both gadget
sizes (two passing setup/cleanup results and two failing cases).

- Out-of-order weather, currency and feed responses could replace newer data
  and caches, including when the superseded request failed.
- Weather windows matched only the displayed city name, allowing different
  coordinates or temperature units to receive one another's readings.
- Changing units, currency pairs or feed URLs left the previous query's data
  visible under the new settings while the new request was pending.
- The default feed request URL and reply filter used different defaults.
- Failed requests, incomplete XML and trailing malformed XML could supply
  headlines. Invalid caches could suppress a refresh; an empty valid feed was
  not cached. Failed refreshes with saved headlines were not reported.
- Atom enclosure/self links could replace the article link; relative links
  were not resolved against their document/base URL.
- Clicking the header, footer or outside the feed body could open an article
  that was not the visible row being clicked.

## Changes under test

Each network category tracks the latest in-flight reply per logical query.
Superseded replies cannot publish or write caches. Independent queries remain
independent. Weather publishes its coordinates/unit key as well as its display
label, so windows sharing coordinates under different labels remain supported.
Query changes clear old values before requesting new data; refreshing the same
query retains its valid cached data.

Feed caches require paired, typed title/link arrays. Only HTTP(S) article links
are retained. Parsing checks the complete bounded XML document, stores at most
30 headlines, rejects DTDs/excessive nesting, and distinguishes a valid empty
feed from an error. Failed refreshes keep the valid saved cache and report the
failure. Cached headlines are labelled in both sizes; successful empty feeds
say “No headlines,” and missing data does not claim saved headlines exist.

Atom article selection follows the alternate-link default and scoped
`xml:base` rules in [RFC 4287](https://www.rfc-editor.org/rfc/rfc4287.html).
This is not a claim of complete Atom/RSS schema conformance.

Feed click handling now excludes the header, footer, outside-body coordinates
and rows that are not drawn. The “open links” preference is still respected.
No artwork, icons, metadata, dependencies or normal clean-profile defaults
were intentionally changed.

## Verification

The final source build passes:

- 74 provider Qt results, including controlled success/failure/cache tests,
  six out-of-order cases, independent weather queries, document size flags,
  malformed XML after the 30-item limit, local/script-link exclusion, Atom
  inherited base URLs/default relation and valid empty feeds;
- 34 gallery Qt results, including independent weather instances, shared-query
  aliases, settings-change clearing, default-feed delivery, both-size cached
  and empty-feed labels, and both-size click-target checks;
- all five CTest groups, including the icon-independence/policy checks;
- `git diff --check` in the Desktop worktree.

Tests use injected network replies and an isolated D-Bus session. They do not
prove live provider availability, native compositor behaviour, installed
package upgrades, normal-login restoration or final-media acceptance.

Logs are retained in `gadget-query-feed-logs/`. Baseline logs are preserved
alongside final results; the test fixtures were not relaxed to obtain a pass.

Candidate source archive: `work/beta2-gadgets11.2T4sLV/aero7-gadgets-3.0.0.tar.gz`.
SHA-256: `0893da1e712b697fe0eeb8be391e72bd477159a651d33ff5a3eba6844e7a11e4`.
Candidate package `aero7-gadgets-3.0.0-11-x86_64.pkg.tar.zst` is 365328 bytes;
SHA-256 `405a70916b832785eae927ef680194973996532cd7852eff44ed4fba35b9495b`.
Installed executable SHA-256:
`c0f271dfd5dcef4a29d1d01cbd3ba7ee86e0a87cae7ab1549f9d480efa9e5ddf`.
`makepkg` finishes successfully at 18:08:04 CEST with all five CTests passing.
Normalized package metadata differs from release 10 only in package/build
metadata and the host executable; file ownership, modes, symlinks, icons, data,
licenses and install hooks are unchanged.

## Installed VM evidence

The existing offline QA disk boots without a NIC at 1920×1080. Boot ID:
`ec6e18a8-16f7-4d91-9633-0f047c32acb3`.

- Normal `pacman -U` upgrades 10 to 11 with no overwrite/dependency bypass.
  `gadgets11-upgrade.5cLA0W` records exit 0, all 57 installed paths present and
  the expected executable hash. Missing sync-database warnings are preserved;
  this local offline transaction does not fetch repository databases.
- Private profile `gadget-query-profile.cM3wmF` uses explicitly synthetic
  saved cache fixtures. The [native screenshot](gadget-query-feed-logs/a7-gadgets11-query-visible.png)
  shows both sizes of cached, empty and unavailable feeds (top to bottom), plus
  independent 0-degree Celsius and 32-degree Fahrenheit readings under the same
  display label. Real no-network refresh failures are logged; the four seeded
  cache files remain byte-identical. The private bus intentionally cannot
  activate the host portal; its warning is retained, not treated as a normal
  session portal failure. The fresh empty-feed fixture is time-bounded to this
  run and must be refreshed for a later replay.
- After stopping the private host and normal Start-menu logout/password login,
  `gadgets11-login.Za0YHE` records session 5, normal autostart PID 3556 beginning
  at 18:16:42, and the exact `/proc/3556/exe` hash. No QA config/cache override
  is present. All 57 package paths remain present, failed-unit lists are empty,
  and Shell/KWin/Plasma report zero restarts. The normal saved gadget layout is
  empty before the additional Show Desktop probe.

### Additional native finding: Show Desktop

Meta+D hid all private-profile gadgets. To exclude private-D-Bus isolation as
the cause, the normal autostart host was tested separately: a Clock was added
through the real Gallery, Meta+D hid it, and Meta+D again restored it. See
[hidden](gadget-query-feed-logs/a7-gadgets11-normal-showdesktop.png) and
[restored](gadget-query-feed-logs/a7-gadgets11-normal-restored.png).
The current `showingDesktopChanged`/layer-switch code therefore does not prove
the intended native behaviour. This is a reproducible remaining parity defect,
not a reason to undo the provider/feed fixes. The test Clock was removed after
the probe; the normal empty layout is retained.

The manifest still selects Gadgets 10 pending the follow-up and integration
selection. Frozen r10 ISOs are unchanged.

## Remaining gates

Fix and retest native Show Desktop behaviour, then update/check the candidate
selection. Other gadget settings/media/slideshow/scaling, full desktop recovery, vault security
and final online/offline image gates remain tracked in the QA status document.
Do not turn these scoped passing tests into a “Beta 2 fully tested” claim.
