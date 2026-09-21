# Media Center: track changes and stale album artwork

13 September 2026. Local pre-release source/package work; no publication,
commit, push or final ISO. The current installed/selected release remains
Gadgets 17 until the next candidate passes installed validation.

## Reproduction

The media provider lacked direct MPRIS test coverage. A new test launches a
separate Qt process exporting real MPRIS properties and methods on a private
D-Bus session with service activation disabled. Production D-Bus polling and
command routing are exercised unchanged. Artwork downloads use the existing
in-memory network fixture; no public service or host media player is contacted.
An 8×8 red PNG is a disposable test input, not new product artwork.

The release-17 RuntimeServices source is saved with SHA-256
`1aa8f0ca91e8e0e031f4f2eba674e5a5108415c95e7035759560674fbfba06d2`
and is byte-identical to the normal release-17 package source. With the expanded
tests it returns three passes and seven failures:

- Metadata, Playing/Paused status, Previous/PlayPause/Next routing and player
  disappearance pass. The unsupported Quit command is not forwarded.
- Changing from a valid cover to no cover, a missing local file, an unsupported
  scheme or a pending download fails to clear the previous image (four cases).
- A delayed download from an old track replaces the current coverless track.
- Returning to an earlier URL accepts that URL's superseded first request.
- A failed HTTP response containing decodable image bytes is accepted as art.

These are controlled provider-level failures, not yet native widget screenshots.
The initial build invocation could not see the newly added Makefile target;
rerunning CMake generated it and the subsequent build passed. The fixture
starts without artwork so constructor polling cannot consume a cover before
test spies attach. Both compared versions use the same final tests.

## Correction and controlled results

When the player or artwork URL changes, the provider clears the old cover,
including when the new URL is empty or unusable. It invalidates outstanding
artwork by request identity, not just URL, and requires a successful network
reply before decoding/publishing its image. Player disappearance also
invalidates pending artwork. No runtime interfaces, icons or dependencies change.

Corrected RuntimeServices source SHA-256:
`e3b6572a1265dd4f0a99c1f1afcb37e9d8bf1f211c577c9e5abe855217bd7656`.
Identical test source SHA-256:
`4fa16b6fa32880fb0fa98d88ea5020ccb5ed13719861ceb19e7ce49d93f57d77`.

The corrected media target passes all ten results. The complete rebuilt suite
passes all eight groups, including the existing gallery/provider tests. This
does not establish real-player, installed widget or live-download acceptance.

Candidate 18 completes normal packaging in `work/beta2-gadgets18.tUqx6r` from
source archive SHA-256
`20db3cf38b8658b0d951436f8c72cb7e35fce1452a8064be0a322fa196d51687`.
All eight normal package-check groups pass. Its archive SHA-256 is
`4f5b07c25bb6784be6375909245d0c719d9bf3b369bdf4d86b66df52d3b1e30c`;
the executable SHA-256 is
`5173f62f2c3d48f63253326a0c3401683355763c55de2fd2c86f0012875348c6`.
Normalized package MTREE comparison against release 17 changes only the
executable and build/package metadata: artwork, hooks, launchers, paths, modes
and symlinks are unchanged. Direct dependencies are unchanged. Installed
comparison, normal login and any subsequent manifest selection remain required.
Native coverage must include starting/adding Media Center while a player is
already active as well as changing artwork after startup; provider-level
subscribers alone do not prove widget initialization or click hit targets.
The selected Gadgets 17 package
does not contain this new source correction. Final-media and broader tests
remain open.

Evidence: [baseline](gadget-media-artwork-logs/baseline.log),
[corrected media tests](gadget-media-artwork-logs/corrected.log),
[full eight-group suite](gadget-media-artwork-logs/full-ctest.log),
[normal package build](gadget-media-artwork-logs/package18-build.log).
