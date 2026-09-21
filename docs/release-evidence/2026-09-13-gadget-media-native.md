# Media Center: native artwork, readability and control alignment

13 September 2026. Follow-up to the [provider artwork tests](2026-09-13-gadget-media-artwork.md).
No final ISO, commit, push or publication is authorized by this report.

## Installed comparison and additional failures

Private Wayland replay `gadgets17-media.F4zVQq` runs the installed release 17
and a separate MPRIS player fixture on its own session bus. The normal account
layout and autostart service are not replaced. Media Center starts at (350,250)
in its large size, with a valid existing QA image advertised before startup.
The title/status appear but the initial cover does not. A first attempted
alternate fixture path, `b.png`, does not exist and is not counted as a valid
cover test. Switching back to the verified existing `a.png` displays the image.
Changing to a coverless track then incorrectly retains that image.

With art displayed, the title/artist text becomes dim. Clicking the actual
Previous, Play/Pause and Next glyphs at (464,426), (505,426) and (546,426)
records **PlayPause, PlayPause, PlayPause**, not the three intended commands.

Normal upgrade `gadgets18-upgrade.jaPeE8` passes all 57 installed-file checks
and verifies the release-18 executable hash. Its private native replay
`gadgets18-media.PpymNr` confirms the stale-cover correction: after loading a
valid cover, switching to a coverless track removes it. Initial artwork and
dim text remain defective. Both private hosts/player fixtures were stopped.

## Additional controlled regressions and correction

Identical tests added before the next source correction reproduce six gallery
failures (65 pass): large Previous/Next hit targets send PlayPause, blank footer
clicks send commands in both sizes, and artist text loses white contrast in
both sizes. A late-subscriber test reproduces the missing initial cover
(ten media results pass, one fails).

The correction uses shared painted/hit-test rectangles for the three controls,
preserving their visual positions while excluding blank footer space. It
restores the white pen after the translucent artwork border. The provider
retains the decoded current image and replays it on later polls, allowing new
gadgets to receive it without another download. Previous request-identity and
invalid-response corrections remain intact; no icon assets change.

The full rebuilt suite passes all eight groups: 71 gallery, 74 provider and
11 media results. Candidate 19 completes normal packaging in
`work/beta2-gadgets19.EJNXDw` from archive SHA-256
`42310510be6382652ec279348b8c1e4f4295ed131a5152df72c5bb3aeef6f938`.
Its eight package-check groups pass. The archive SHA-256 is
`d227e2c2785dc44879b1553279dcf061aa5011cc4d3a34be453604b6cd822e7e`;
the executable SHA-256 is
`1923d9f24954ddf04666f306026cb39f3bc8a09312ac40974058fed40a4475a8`.
Normalized MTREE comparison changes only executable/build metadata; the same
paths, modes, symlinks, artwork and hooks are retained.

Normal upgrade `gadgets19-upgrade.WyoIEc` passes. Native fixture run
`gadgets19-media.CHERNG` now shows the initial cover with white title/artist
text. Clicking the same three visible buttons records Previous, PlayPause,
Next; an additional blank-footer click adds no command. Changing to the
coverless/paused track removes the image and displays the play glyph.

Real installed VLC 3.0.23_2-13 is exercised separately in
`gadgets19-vlc.3PXdYC` using two generated, silent five-minute WAV tracks,
private configuration/session bus, dummy audio output and metadata networking
disabled. The widget shows Track One, pauses and resumes VLC, switches to Track
Two with Next, and returns to Track One with Previous. Screenshots and MPRIS
method/property traces agree. No network or host media player is involved.
This verifies real-player command/state behavior, not audible output or remote
album-art services. Both private gadget/player runs were stopped.

Normal Start-menu logout/password login passes in `gadgets19-login.navadE`,
session 8 on boot `fde6a493-c3b9-459c-a5c9-47f8afe5cb9c`. Autostart owns PID
16445 with the exact release-19 binary. Shell/compositor/Plasma are active with
zero restarts, there are no failed system/user units, and the actual compositor
has no permission-check bypass. The ordinary account layout is byte-identical
to the release-17 snapshot; no private media/player test process remains in the
saved process list. This is a normal login audit, not a new cold-boot claim.

The next-build manifest now selects Gadgets 19 in place of 17, with KWin 7.3
unchanged. The complete project checker passes all 149 tests plus checksums,
ownership, dependencies, syntax, icon provenance, theme repeat setup and Shell
parity. Online hygiene passes for 18 archives; offline hygiene passes for 53,
including all 35 custom repository identity/hash records. There are still 16
required and two optional packages, with Programs Center Beta and Credential
Vault optional/off by default. No Shell pin changes.

Manifest SHA-256:
`e8ce103bf70f55c1a324a398076e98b5c434d122d9a24d6201f7bb5c73dd0a0f`.
See [integration output](gadget-media-native-logs/integration19.log),
[online hygiene](gadget-media-native-logs/online19.log) and
[offline hygiene](gadget-media-native-logs/offline19.log).

Frozen ISO artifacts are unchanged. Remaining player selection,
remote artwork/failure recovery, other gadget settings/providers, scaling and
broader desktop/release checks are not closed by this bounded pass.

Evidence is retained in [native-media logs](gadget-media-native-logs/), including
baseline 17 and 18 screenshots, command trace, upgrade audit and the controlled
before/after results. This is not full gadget or final-media acceptance.
