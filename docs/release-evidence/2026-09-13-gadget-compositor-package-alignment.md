# Gadgets 17 / KWin 7.3 next-build alignment

13 September 2026. Local preparation only: no commit, push, publication or
final ISO build. The frozen r10 images are unchanged.

Later on 13 September, the [native media follow-up](2026-09-13-gadget-media-native.md)
replaces Gadgets 17 with 19 after further reproduced fixes, native/VLC/login
checks and a fresh full project-checker pass. The selection below is retained
as the earlier checkpoint, not the latest manifest.

## Selected packages

The local checksum manifest now replaces Gadgets 3.0.0-10 with 3.0.0-17 and
KWin 6.7.4-7.1 with 6.7.4-7.3. These are the exact normal-build archives used
in the [installed gadget checks](2026-09-13-gadget-opacity.md) and
[compositor upgrade/reboot/popup checks](2026-09-13-gadget-popup-membership.md).
The source fixes retain the earlier corrections; no test-only compositor
library is packaged. Existing archives are retained rather than overwritten.

- Gadgets archive SHA-256:
  `906a802bc78979ad046ab96cce7d472f57ad96229e1bc04eb8aaa6d24e6c443b`.
- KWin archive SHA-256:
  `32fdebc384498639412bbfd10822c47ae7139c4c041de4e8a93ba58dcd35ca75`.
- Selection manifest SHA-256:
  `2955de9ad5e6abdf240bdec9ab25352e3b6a67527b346363affda20fe8921bf7`.
- Required-list SHA-256, unchanged:
  `8a64da0370b18ff398e276a6fcf642c7afac3fd57e194d5e5c93643312e896e8`.
- Optional-list SHA-256, unchanged:
  `3ee8b94ffd671697ec11410d4e3baa4f890b4339b9414798e2e864645d2ffb71`.

There are still 18 selected archives, 16 required and two optional. Programs
Center Beta and Credential Vault remain optional/off by default. No icons,
firewall policy, required/optional boundaries or Shell pin change. Shell remains
`cf4d1d8969dfa5ae84308c937cc60146ea59f216`.

## Verification

The complete project checker exits 0: all 149 Python tests pass, together with
selected checksums, file ownership, versioned dependency checks, native dialog
package linkage, syntax, ShellCheck, original-icon provenance, repeatable theme
setup and Shell parity. Online archive hygiene passes for all 18 archives.
Offline hygiene passes for 53 archives (18 local plus 35 custom dependencies),
and all 35 offline repository identity/version/hash records match their manifest.

The normal Gadgets 17 logout/login audit passes in session 5 with its exact
autostarted running binary, an unchanged ordinary-account layout, active desktop
services with zero restarts and no failed units. This extends, but does not
replace, the preceding installed native checks and compositor reboot audit.

Evidence: [full checker](gadget-compositor-alignment-logs/check.log),
[online hygiene](gadget-compositor-alignment-logs/online-hygiene.log),
[offline hygiene](gadget-compositor-alignment-logs/offline-hygiene.log),
[selected manifest](gadget-compositor-alignment-logs/beta2-local-packages.sha256).

## Still open

Package-input validation is not a new installation or proof that every gadget
works. Remaining media/provider, gadget-settings, scaling/multi-monitor,
optional-vault, desktop recovery and broader release checks remain required.
Final online/offline images require the user's build approval and then exact
artifact end-to-end testing. Do not publish downloads or final checksums from
this report. No host packages or firewall settings were changed.
