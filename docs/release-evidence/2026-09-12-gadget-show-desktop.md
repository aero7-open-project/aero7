# Gadgets: Show Desktop permission regression

## Scope and release gate

12 September 2026. Local bug-fix work only; no commit, push, publication or final
ISO is authorized. The next-build manifest still selects Gadgets 10. Installed
Gadgets 13 fixed the permission defect but still failed native Show Desktop
visibility. A separate compositor correction is under test, not selected for media.

## Reproduction and cause

Normal-account Gadgets 11 and 12 disappear when Meta+D activates Show Desktop.
The installed 12 private Wayland trace also has no window-management global or
Show Desktop events. Its layer surface starts on the bottom layer.

KWin 6.7.4's `src/utils/serviceutils.h` resolves the executable against application
desktop entries and reads `X-KDE-Wayland-Interfaces` as a KService QStringList.
The VM's read-only KService probe finds both installed Host and Gallery entries,
with matching absolute executable paths. However, version 12 parses the value as
`org_kde_plasma_window_management;`, including the semicolon. This fails KWin's
exact permission membership check. Static text matching had incorrectly accepted
that malformed value; it was not proof of compositor authorization.

## Correction and regression coverage

All three launchers now use the exact single permission without a trailing
semicolon. Absolute executable paths are retained. No fake-input, screen capture
or permission-check bypass is added. No icon or artwork is changed.

The new KService-based permission regression fails against all three version 12
source entries and passes against the corrected source. KService is a test/build
dependency only; the runtime dependencies remain unchanged. The build runs seven
CTest groups, including 74 provider and 34 gallery Qt results (these counts
include test setup/cleanup). All pass.

## Package identity and installed evidence

- Source archive SHA-256: `57826e91c180b28f3b4bd82490522ba093eba59b14894ee863bb671f3189139d`
- Package: `aero7-gadgets-3.0.0-13-x86_64.pkg.tar.zst`
- Package SHA-256: `c0631b554ba3c2ad1e527fb294313c43d53c317fe96487b78472275f1ebcce4f`
- Installed executable SHA-256: `8da69f2c9e4a96a6daba7a5fc52a19736872a4734fb74f3e2ed4d97ff67bad86`
- Build completed 18:49:43 CEST, exit zero.
- Normal offline VM upgrade 12 to 13 passes with all 57 package paths present.
- After upgrade, the same native KService probe reads the exact permission from
  both application entries, with no trailing semicolon.

Evidence is retained in [gadget-show-desktop-logs](gadget-show-desktop-logs/):
the failing semantic regression, full package build/tests, upgrade audit and
before/after installed service lookup.

## Fresh-login result and second cause

Normal logout and password login pass with the exact Gadgets 13 executable
running through the normal autostart. No failed system/user units or shell,
Plasma or KWin restart counts appear in that audit. KWin permission checks are
not disabled. Clock and Calendar are added through the native gallery, but both
still disappear during Meta+D. They return when Show Desktop is toggled off.
Both QA gadgets are then removed; the account layout is byte-identical to the
empty pre-test layout. The later private trace host is stopped too.

The installed 13 private Wayland trace now proves that the window-management
global is advertised and bound, `show_desktop_changed(1)` arrives, the gadget
sends `set_layer(2)`, and its surface commits. Missing permission or a missing
layer commit no longer explains this failure.

KWin's `Workspace::breaksShowingDesktop()` hides windows unless they are desktop
components (or other explicit exempt types). A layer surface with the custom
gadget scope is classified as an ordinary window; changing its layer does not
clear `hiddenByShowDesktop`.

The proposed [compositor patch](../../patches/kwin-desktop-gadgets-visibility.patch)
overrides desktop membership for the exact gadget and transparent drag-preview
scopes only. It does not turn gadgets into wallpaper focus targets or docks,
change their keyboard interactivity, or exempt unrelated layer clients. It adds
native compositor regressions for both exact scopes, a normal layer client and
a similar-but-not-matching scope, including repeated Show Desktop transitions
and unchanged switcher/type/layer expectations. Patch application dry-run passes
with zero fuzz against the existing KWin 7.1 source.

## Controlled compositor result

The integration target builds in `work/beta2-kwin-gadgets.AAlvVC` with two jobs.
The first test-harness run fails at initialization because the workspace-derived
Wayland socket path exceeds the Unix socket length limit. That run is not a
product regression result. The runner now uses a private short runtime directory,
private config/cache/data and a private D-Bus session without desktop activation.

The valid targeted baseline has four passes and two failures: only the gadget
and drag-preview membership expectations fail. The full baseline has 70 passes
and those same two failures. After applying the candidate, the full layer-shell
suite passes **72 results, zero failures**, including setup/cleanup. Gadget and
drag-preview scopes retain visibility across repeated Show Desktop transitions;
the ordinary and similar-name scopes are still hidden. Existing output, anchor,
margin, layer, focus, activation, stacking, edge and protocol-error checks pass.
The client protocol error printed by `testUnconfiguredBuffer` is intentional
coverage of a rejected invalid client, not a failed test.

- Patch SHA-256: `5c1d6b0e39dd4e3babb5cc6d2228a2b6077898591e04dfbb3d0d7d9c74621cd0`.
- Candidate test executable SHA-256: `fc5b28e486e0c01e4173457652e4b45503f3d0e70ed50ffaf0a879a18c2a84be`.
- Candidate test-build libkwin SHA-256: `028d44a63965106c65b963b5b6326559f44fdc8ec283a41b199822c7a586d482`.
- Baseline and corrected full logs are retained in `gadget-show-desktop-logs`.

## Normal package and VM upgrade

The normal release-7.2 package completes at 20:04:29 CEST, exit zero. Its prepared
source tree exactly matches the passing compositor test tree. The normal recipe
retains the previous distro compiler/hardening flags; this is not the separate
test-build library repackaged as a release.

- Archive SHA-256: `cd0b3c39be0585445d0470960ea28385b48c79dc0927c83db0a7d91d344729d6`.
- Packaged executable SHA-256: `588162b57709d6a2976edab399e26bec9c4423216bf22fcc8a13f63a4714e7c4`.
- Packaged libkwin SHA-256: `c5c771f041902fe1d0e6d83dc3d5320eb12f4b204c1e4d6b4aa56b879ad5bf85`.

Extracted 7.1/7.2 package comparisons have identical 2,256 paths, file modes and
symlink targets. All 63 ELF files retain their direct dependencies, GNU stack
flags and RELRO presence. Package metadata other than version/build date/size
is unchanged. Full build/comparison results are in `gadget-show-desktop-logs`.

The normal offline 7.1→7.2 VM upgrade passes in
`kwin72-upgrade.fARjIR`, with 2,256 files present, exact executable/library hashes
and `cap_sys_nice=ep` retained. Restart is selected through the native Start
menu. Post-reboot running-library and visible desktop behavior are still pending;
the next-build manifest is not changed by this upgrade.

## 13 September running-process verification

The first post-reboot audit stopped at a hash mismatch because it compared the
systemd unit's MainPID with the compositor executable. The unit's MainPID is
actually `kwin_wayland_wrapper`; its observed SHA-256 exactly matches the packaged
wrapper (`a6b23e6a6ad26fe4a421a20b8b2d7eefe6be61dc38d49d4b9d60706045b53887`).
This was a test-process identification error, not evidence of a stale compositor.
The failed result is preserved, not relabelled as a pass.

The corrected audit verifies the packaged wrapper, finds its one live child
whose executable is `/usr/bin/kwin_wayland`, verifies that child's executable
hash, and compares the mapped library inode with the exact-hash installed
library. It also rejects any permission-check override in the actual compositor
environment and fails if the protected-process read itself fails.

After the stopped test VM is cold-started on 13 September, the audit passes at
13:44:28 CEST in `kwin72-boot.3duk1b`: boot
`ea74a7cd-07ed-4203-a051-f6d850afb410`, session 2, wrapper PID 679,
compositor PID 683, library inode 1365388. The actual compositor and library
match the package hashes above. File capability remains intact, no permission
override is present, all three desktop services are active with zero restarts,
and failed system/user unit lists are empty. The strengthened Gadgets 14
normal-login audit also passes (`gadgets14-login.izGZIs`).

These checks do not imply an error-free journal: the VM records software-rendering
fallback and auxiliary application's portal-registration warnings. Nor does this
cold-start check retroactively establish a clean shutdown for an interrupted run.
Evidence is in [gadget-show-desktop72-logs](gadget-show-desktop72-logs/).

The first native replay now keeps all three test gadgets visible during Show
Desktop while hiding ordinary applications. However, the tightly timed follow-up
finds a remaining gadget-side commit delay. The first late screenshot missed
the transient; it must not be treated as immediate-restoration evidence.

In the repeat, Show Desktop turns on at 11:47:30.425007 UTC. Calendar requests
the Top layer, but commits only at its periodic refresh, 11:48:04.009821.
Show Desktop turns off at 11:48:58.632399; Calendar requests Bottom but does not
commit until 11:49:04.009440. The screenshot taken one second after toggle-off
shows Calendar incorrectly above the restored terminal. This establishes a real
visible delay, not just delayed logging. This private native host is then stopped.

The compositor visibility correction is therefore a scoped pass, but full native
Show Desktop acceptance stayed open at this checkpoint. The subsequent
[Gadgets 15 timed replay](2026-09-13-gadget-layer-update.md) verifies immediate
surface updates and normal login, but identifies a separate popup issue.
The [popup follow-up](2026-09-13-gadget-popup-membership.md) records its
controlled correction and remaining package/VM gate. No new package is selected
for media yet.
