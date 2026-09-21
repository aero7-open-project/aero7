# Qt portal registration candidate — 8 September 2026

Status: source regression verified; full Qt package and installed-VM acceptance
pending. No final ISO, package repository, commit or publication was changed.

## Reproduction and correction

The earlier [installed-helper trace](2026-09-08-snipping-portal-identity.md)
recorded two Registry.Register calls from the same Snipping Tool bus connection
715 microseconds apart during portal activation. Qt 6.11.2 only marks its shared
registration flag after receiving the asynchronous success reply, leaving both
the initial call and the portal watcher able to send while the first is pending.

The candidate patch introduces an in-flight guard, avoids empty application IDs,
clears the guard after errors, and invalidates successful/pending registration
when the portal owner departs or is replaced. Generation checks prevent a late
reply from an old owner from changing its replacement's state. Multiple watchers
share state and deduplicate the same owner-change event. This is not a warning
filter, portal disablement or timing delay.

Patch: `../../patches/qt6-base-host-portal-registration.patch`

SHA-256: `635b75094a602cf980223818925cf0eaa2c5bc0bff6effd841cb09f4865f6d0a`

## Source provenance

The candidate is based on the official Qt v6.11.2 commit
`ef55f427f2c8b410d34f8a7681020a3000cf6866` (annotated tag object
`7a59d906fb765eb85759d4d3cae45d3f295f6359`).

The official Arch qt6-base 6.11.2-3 PKGBUILD SHA-256 is
`217bd5ea50a3c721be622a8bccacc801c3091f01110c4985d142d004efcb16c5`;
it matches the cached installed package's BUILDINFO. Its three source checks
passed `makepkg --verifysource --holdver --nodeps` without changing a checksum.
The verified Git archive hash is
`c27a588094ea6d47f294539dbab00a7222d9f56e2d44ac00287bb44b5eed612a`.
An earlier manual archive hash differed because it inherited the host's Git
configuration; makepkg isolates that configuration. Repeating the archive check
with makepkg's GIT_CONFIG_GLOBAL/GIT_CONFIG_SYSTEM settings matched the recipe.
This was not evidence of a corrupt upstream source or justification to waive
integrity checks.

Primary references:

- [Qt registration source](https://github.com/qt/qtbase/blob/v6.11.2/src/gui/platform/unix/qdesktopunixservices.cpp)
- [Qt service-owner watcher](https://github.com/qt/qtbase/blob/v6.11.2/src/dbus/qdbusservicewatcher.cpp)
- [Arch package recipe](https://gitlab.archlinux.org/archlinux/packaging/packages/qt6-base/-/blob/6.11.2-3/PKGBUILD)

## Focused D-Bus regression

The retained CMake fixture extracts the actual registration functions and watcher
wiring from the supplied source tree. It compiles those against installed Qt and
runs each case on its own dbus-run-session with a delayed-reply mock portal.
The host portal is not contacted. This tests the actual extracted implementation,
not a separately rewritten state-machine model, but is not a full QtGui build.

| Scenario | Unmodified Qt | Candidate |
| --- | --- | --- |
| Two requests while registration is pending | Fails: 2 calls | Pass |
| Initial owner announcement plus initial registration | Fails: 3 calls with two watchers | Pass |
| Retry after failure, no repeat after success | Pass | Pass |
| Empty identity followed by valid identity | Fails: empty ID sent | Pass |
| Portal release and reacquisition | Fails: no new call | Pass |
| Repeated release/reacquisition by the same connection | Fails | Pass |
| Replacement while pending, followed by old success | Fails: replacement not registered | Pass |
| Replacement while pending, followed by old error | Fails: replacement not registered | Pass |

Candidate: 8/8, then 40/40 with `ctest --repeat until-fail:5`.
Unmodified baseline: 1/8, with the seven expected failures and explicit request
counts retained. Logging was routed to stderr in the test executable so Qt's
journald logging does not hide diagnostics from CTest. Production logging was
not modified. Patch application to the clean source was checked successfully.

Reproduction files and logs: [qt-portal-registration-logs](qt-portal-registration-logs/).
Configure that fixture with `-DQT_SOURCE=/absolute/path/to/the/qt/source/tree`,
build it and run CTest. Do not count the intentionally failing baseline as a
newly introduced application regression.

## Separate Action Center correction

The earlier trace also identified Action Center as a different client sending
an empty ID. Its entry point now sets `aero7-action-center` before icon/window
initialization. The matching NoDisplay desktop entry is installed in
share/applications as well as the existing autostart location: the latter alone
does not provide an application identity lookup. This adds no Start-menu item
and does not change its executable, icons or existing autostart behavior.

The source-order/packaging guard passed and the whole Control Panel build then
passed 19/19 CTest groups. The first test attempt had three Not Run results
because only the Action Center executable had been built; its log is retained,
and the complete rebuild supplied and passed those tests. Candidate executable
SHA-256: `50d15145505757a4fc90a9830aa6444d3395cafa89ae8bdf4f43dcc7d2f35eeb`.
This Action Center correction has not yet been packaged or exercised in the VM.

## Remaining acceptance gates

- Build the complete Qt package in an isolated builder, retaining Arch's build
  features, split package and existing icon-theming cherry-pick
  `e80e3f0cebae9c3a45a1b7ce81d6454c699d89c6`. The prepared regression tree has not
  yet applied those unrelated Arch preparation steps. Do not silently drop SQL
  plugins or other optional build dependencies missing on the host.
- Verify ABI/payload dependencies and actual installed-library behavior, then
  replay cold login, portal activation/replacement, screenshots and native file
  dialogs. Repeated QGuiApplication lifetimes in one process and session-bus
  reconnection are not established by this fixture.
- Package and VM-test the separate Action Center identity/desktop-entry change.
- Rebuild both final media only after package gates; repeat full online/offline
  installation and desktop acceptance. Frozen r10 images remain unchanged and
  do not contain these or the later clipboard fixes.

No host dependencies or firewall settings were changed. No additional VM disks
or ISOs were deleted in this pass.
