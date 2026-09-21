# Weather Find and feed-management failure paths

13 September 2026. Source regression checkpoint following the
[release-20 settings pass](2026-09-13-gadget-settings.md). No final ISO, commit,
push or publication is authorized by this report.

## Weather lookup

A test-only injectable network manager exercises the actual Find button and
reply handler without contacting a provider. Before the correction, 99 gallery
results pass and eleven new cases fail. The handler accepts an HTTP-error body
as a successful lookup, converts missing/string coordinates to zero, clamps
out-of-range values instead of rejecting them, permits an empty place name,
accepts an oversized reply's valid JSON prefix, gives no visible feedback for
empty/invalid responses, and overwrites location/coordinate edits made during
the request. An edit changed away and back is also overwritten.
See [the Weather baseline](gadget-find-feeds-logs/find-baseline20.log).

The correction validates request success, response size, JSON structure, a
non-empty place name, numeric/finite coordinates and their geographic ranges
before changing any field. An edit revision guards the entire location result,
including changes away and back. Failed, invalid, unmatched and superseded
requests show plain-text feedback and re-enable Find. Manual coordinate entry
remains available. Retry clears the earlier error; real zero coordinates and
both valid boundaries are accepted. Closing the dialog disconnects its reply
handler so a later response cannot access destroyed fields.

Seventeen new Weather rows cover the eleven failures, four successful
timeout/retry combinations (zero, southern coordinates, lower and upper bounds),
an empty query making no request, and a reply after dialog destruction. These
are controlled provider tests, not claims of live Internet/API availability.

## Feed catalog

Three additional baseline failures reproduce in the actual Manage Feeds dialog:
removing all three defaults writes an empty array but reopening restores all
three; a failed save removes a row from the UI despite not persisting it; and
opening/closing the manager discards a URL typed in the parent Options combo.
See [the feed baseline](gadget-find-feeds-logs/feeds-baseline20.log). This baseline
already includes the Weather correction; it is not an unmodified release-20
binary comparison.

A valid saved empty catalog is now retained. Save completion includes both the
full write and atomic commit; the in-memory list changes only after success.
Failure shows an inline message and leaves the previous list intact. A retry
after removing a deliberately created write obstruction succeeds, clears the
message, and persists exactly one removal. Rebuilding the chooser retains a
typed HTTP(S) URL. Tests isolate all catalog writes inside temporary profiles;
no ordinary account's feeds are removed. Removing a catalog entry does not
delete an existing gadget or silently replace its configured custom URL.

## Current verification boundary

All eight rebuilt source groups pass: **120 gallery, 74 provider and 11 media
results**. The [complete output](gadget-find-feeds-logs/corrected21.log) includes
the previous settings, media, opacity and menu regressions. The feed retry row
adds recovery coverage beyond the three original failures.

Normal candidate packaging completes in `work/beta2-gadgets21.WbYcha` with all
eight package-check groups passing. See [the build log](gadget-find-feeds-logs/package21-build.log).
Source archive SHA-256:
`a3c14e809c826a5f231cc3c0f20726af4be359e73fe37d81204647caa23c8792`.
Package `aero7-gadgets-3.0.0-21-x86_64.pkg.tar.zst` SHA-256:
`afbd7ba4c8620cf1e70ac9253e7d021d7537a5048e423e90f60409d00f78c558`.
Executable SHA-256:
`8d416847cc20249180c427a652d0c39fc54967d03e0cb6181cb222d2a6a0d83a`.
Normalized MTREE comparison changes only the executable and package/build
metadata, preserving paths, modes, symlinks, assets, hooks and launchers.
The next-build manifest still selects Gadgets 20 with KWin 7.3. No existing ISO
contains these new fixes. The following native checks supersede the earlier
pending-install status of release 21.

## Installed release 21 and message clipping

Normal upgrade `gadgets21-upgrade.pmhM2i` passes the package/file/hash checks.
Private no-NIC Wayland replay `gadgets21-settings.ds3JBi` confirms that Weather
Find returns to an enabled button and retains the original city/coordinates
after an offline failure, but its explanatory label is visibly clipped. This
prevents accepting release 21 as the final correction.

The same installed replay verifies the feed fixes. A temporary directory at the
private profile's `feeds.json` path deliberately blocks saving; Remove leaves
all three entries visible and shows the complete save-error message. Removing
only that empty test obstruction and retrying persists one removal and clears
the message. Removing the other two entries then reopening the manager leaves
the list empty. The URL typed before opening the manager is preserved as
`https://qa.invalid/new.xml` in the saved gadget settings. The ordinary account
profile is untouched, and the private host is stopped after the replay.
See [upgrade21.log](gadget-find-feeds-logs/upgrade21.log),
[native layout](gadget-find-feeds-logs/native21-layout.json),
[empty catalog](gadget-find-feeds-logs/native21-feeds.json), and the native
screenshots in [gadget-find-feeds-logs](gadget-find-feeds-logs/).

Three additional message-layout regressions reproduce the clipping with 12,
16 and 24-pixel fonts: allocated label heights are 24/29/40 pixels versus
51/88/297 required by their actual widths. See
[message-baseline21.log](gadget-find-feeds-logs/message-baseline21.log).
The correction gives the message a full-width form row and lays out its actual
width before reserving sufficient wrapped-text height and resizing the dialog.
Retry clears that minimum height. All eight rebuilt source groups pass, now
with 123 gallery, 74 provider and 11 media results. Candidate 22 packaging
completes with all eight package-check groups passing in
`work/beta2-gadgets22.qUgBEq` from source SHA-256
`3d2ed92175412d009f718d76b1da7bcbe6539325eeb0179336d5c2957f72899a`.
Package SHA-256 is
`a05a0b562bd19b1de3ff353a1346cf030fe3388f220b04b1529f129164856236`;
executable SHA-256 is
`f7cc58567f7ddd2ae3f1fe3e5fdb93abd8bb4c81255000c0bee9e0082f98473f`.
See [source tests](gadget-find-feeds-logs/message-corrected22.log) and
[package build](gadget-find-feeds-logs/package22-build.log).

Normal upgrade `gadgets22-upgrade.jFqSzS` passes. Private native replay
`gadgets22-settings.5KiHnU` shows the entire offline-error message, with no
overlap or clipping, while retaining the original city and coordinates. Find
can be retried, and manual latitude/longitude (-12,34) save normally after the
failure. The private host is stopped. See
[the corrected message](gadget-find-feeds-logs/a7-g22-weather-error.png),
[upgrade audit](gadget-find-feeds-logs/upgrade22.log) and
[saved private settings](gadget-find-feeds-logs/native22-layout.json).
This checks offline failure feedback/manual recovery, not native online lookup
success or the entire Settings UI under every theme/scale.

Normal Start-menu logout/password login then passes in
`gadgets22-login.bKRQCV`, Wayland session 14 on the existing boot
`fde6a493-c3b9-459c-a5c9-47f8afe5cb9c`. Autostart owns PID 32510 with the exact
release-22 binary. Shell/KWin/Plasma are active with zero restarts, no failed
system/user units, no compositor permission-check bypass, and no private
settings/player host remaining. The account layout is byte-identical to the
release-20 login snapshot. See [login22.log](gadget-find-feeds-logs/login22.log).
This is a normal-login audit, not a new cold-boot claim.

Gadgets 22 is now selected with KWin 7.3 for the next build. Manifest SHA-256:
`701b97b495b5c9f333e8121492a1444f65c2fc185c72ee03fa674e58989c8f54`.
All 149 integration tests pass, with static checks complete. Archive hygiene
passes for 18 online and 53 offline archives; all 35 offline repository entries
match package identities and checksums. See [integration](gadget-find-feeds-logs/integration22.log),
[online](gadget-find-feeds-logs/online22.log) and [offline](gadget-find-feeds-logs/offline22.log).
The Shell pin,
optional-feature defaults, existing ISO files and publication hold are unchanged.

Broader live-provider success, feed URL validation/corrupt-catalog recovery,
remaining gadget controls, scaling/multi-monitor, desktop recovery and final
image tests remain open. This report does not establish release readiness.
