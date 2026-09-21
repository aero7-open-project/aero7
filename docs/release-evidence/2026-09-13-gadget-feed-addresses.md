# Feed Manager address validation — 13 September 2026

This is a bounded follow-up to [Weather Find and feed management](2026-09-13-gadget-find-feeds.md),
not final ISO or complete gadget acceptance.

## Reproduced bug and correction

The real Add Feed dialog accepted `https://`, malformed IPv6 and an invalid
port, saving unusable catalog entries. File URLs and empty input were rejected
silently. The initial ten-row dialog regression reproduces all five failures
(seven passing Qt results, five failures including setup/cleanup).

The correction parses a complete URL strictly, requires a valid HTTP/HTTPS
scheme and nonempty host, and explains invalid input without saving or changing
the displayed catalog. It does not reinterpret malformed explicit addresses as
another host/path. Users must include `http://` or `https://`; cancelled input
does not display a new error or save anything. A successful save clears the
status and its reserved wrapped-text height. No icon, asset, dependency or hook
changes are part of this correction.

The expanded twelve-row test drives the real nested name/URL dialogs. It covers
HTTPS, HTTP with port/query, IPv6, surrounding whitespace, empty host, invalid
IPv6, invalid port, invalid percent encoding, missing scheme, file URL, empty
input and cancellation. It checks list counts, visible feedback and saved JSON
or absence of a newly written file. All eight source test groups pass, with
135 gallery, 74 provider and 11 media Qt results.

Evidence: [baseline](gadget-feed-address-logs/baseline22.log),
[corrected suite](gadget-feed-address-logs/corrected23.log).

## Candidate and remaining checks

Candidate 23 packages normally, including all eight package-check groups, from source SHA-256
`cbd8e637b7e843054b7499f22b545d24bdc0424f35997c70b811d786b5e37c4a`.
Package SHA-256 is
`f4b738faf92cd815b991ea25b71870702d4a017199b5c3c10b3f9b1f33cf5d72`;
installed executable SHA-256 is
`f7ff4a9b06943e43b54a582d7417fa984adcd3bdfbd224ba7440b20da1588d3b`.
See [package build](gadget-feed-address-logs/package23-build.log).

Normal installed upgrade `gadgets23-upgrade.8Kut38` passes, including file and
binary checks. Native private Wayland replay `gadgets23-settings.4Ij4zP` passes:

- Accepting the default incomplete `https://` address leaves three entries,
  writes no `feeds.json`, and shows the entire two-line explanation.
- A subsequent valid `https://qa.invalid/feed.atom` addition produces four
  entries, clears the error and persists the matching name/URL in JSON.
- Cancelling a further URL prompt leaves that file byte-identical. Closing and
  reopening Manage Feeds still shows the four saved entries.

The private host was stopped before normal logout/login; normal account feed
data was not edited. This private settings profile uses the default Qt palette,
not the ordinary account's full theme configuration, so these screenshots prove
dialog behavior/readability, not normal-theme parity.
See [upgrade](gadget-feed-address-logs/upgrade23.log),
[invalid input](gadget-feed-address-logs/a7-g23-invalid.png),
[successful retry](gadget-feed-address-logs/a7-g23-retry.png),
[reopened list](gadget-feed-address-logs/a7-g23-reopened.png) and
[saved catalog](gadget-feed-address-logs/native23-feeds.json).

Normal Start-menu logout/password login passes in `gadgets23-login.XKscF9`,
Wayland session 17 on the existing boot
`fde6a493-c3b9-459c-a5c9-47f8afe5cb9c`. Autostart owns PID 38087 with the exact
release-23 binary. Shell/KWin/Plasma are active with zero restarts, no failed
system/user units, no compositor permission-check bypass and no private host or
player fixture left running. Ordinary account layout is byte-identical to the
release-22 snapshot. See [login audit](gadget-feed-address-logs/login23.log).
This is a normal-login audit, not a new cold-boot check.

Gadgets 23 is selected with KWin 7.3 for the next build. Manifest SHA-256:
`c4d41e1fd61d60f79777b7cff1fa2289cdd05bf6569d39f7906fd522262e5e1a`.
All 149 integration tests and static checks pass. Archive hygiene passes for
18 online and 53 offline archives; all 35 offline repository entries match
package identities and checksums. See [integration](gadget-feed-address-logs/integration23.log),
[online](gadget-feed-address-logs/online23.log) and [offline](gadget-feed-address-logs/offline23.log).
The Shell pin,
optional defaults, frozen ISOs and publication hold are unchanged.

This does not prove the address serves a valid feed or is reachable. Live
providers, corrupt/unreadable catalog recovery, remaining gadget controls,
scaling/multi-monitor and broader desktop recovery remain separate checks.
Neither frozen ISO has changed; no final ISO build or publication is authorized.
