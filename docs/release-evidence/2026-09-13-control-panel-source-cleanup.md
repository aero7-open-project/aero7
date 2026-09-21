# Control Panel 55 source cleanup and selected-stack login

13 September 2026. Local candidate verification only; no final ISO build,
commit, push or release approval. Raw evidence is in
[control55-source-logs](control55-source-logs/).

## Source and package

The deterministic Desktop source exporter was used for Control Panel with the
`linux-control` prefix. The new snapshot contains 595 files, is 6,772,794 bytes,
and is byte-identical to a repeated export. Compared with the complete release-54
snapshot, it excludes five generated Python bytecode files (three helpers and
two tests). The only shared source-file change is `.gitignore`, adding
`/build-*.log`; application code is unchanged. No old source or build artifact
was deleted.

- Source SHA-256: `3caf8932d340364f195b035f916c52f8625d9e0ebd525384ccb9f6fee360d7f9`
- Package: `linux-control-panel-0.1.0-55-x86_64.pkg.tar.zst`
- Package SHA-256: `c7a94908df427d0e8b12e164f536aa68ed6772a572bdffaf48690c6a79512f9d`
- Selected manifest SHA-256: `de864c2b8fb25e95d9c5f8f8c487d47da24642444853df74776e5ce01fd66ac9`

The two-job package build passed all 21 CTest groups. Both package payloads have
40 non-directory entries; 37 have identical type, mode and content. The three
rebuilt executables differ, so this is not a reproducible-binary claim.

## Upgrade and UI

`control55-upgrade.QOyCtD` passed a normal package-manager upgrade, all 74
installed-file presence checks and the new executable hash check. Desktop
service PIDs/restart counts did not change.

`control55-smoke.ZJdOmi` passed normal main-window and Optional Features
open/close checks. The large-icon view visibly has 45 applets in five columns.
The catalog has 15 entries, but only 13 are searchable optional features: the
desktop core is protected, and discontinued CardSpace is explicitly hidden.
No optional-feature checkbox was changed in this pass.

The earlier `control55-smoke.q1KJXg` failure is retained with its original
harness. It incorrectly expected all 15 catalog entries in optional search.
The harness was corrected to honor the catalog's core/visibility policy; no
production behavior was changed to make that assertion pass.

## Normal logout/login

The running offline VM has no network adapter and uses a 1920×1080 Wayland
session. Normal Start-menu Log Out returned to SDDM; password login created
session 5 on the same boot (`b4d20d4c-2122-454c-b361-fb67d20c63de`).
`stack-control55-login.LLQIA2` completed at 20:06 with exit 0:

- All 16 required core package versions and installed-file presence checks pass,
  including Desktop 33, Control Panel 55, Gadgets 25 and KWin 7.3.
- Exactly one newly autostarted Action Center (PID 14068) has the release-55
  executable hash. Gadgets PID 14066 has the release-25 hash.
- The running compositor and its actually mapped KWin library match the selected
  package. Permission checks remain enabled and the packaged capability intact.
- Shell, KWin and Plasma are active with zero restarts. Failed user/system unit
  lists are empty at the checkpoint.
- Firewalld remains active; the optional vault remains absent/disabled, with its
  offline package cached. The prior gadget layout is byte-identical.

Before logout, two fast automated idle-unlock attempts were rejected. A slower
300 ms key interval succeeded with the same password, as did subsequent SDDM
login and sudo authentication. This supports an input-timing explanation but
does not prove the exact cause. Rejections remain in the captured logs; no
authentication policy was changed.

The journals retain virtual graphics/CPU, unavailable optional hardware and
auxiliary portal-registration diagnostics. This is not a warning-free claim.
The checkpoint is a normal login on an upgraded VM, not a new boot, fresh install
or physical-hardware acceptance result.

## Integration and remaining gates

All 149 integration tests and static checks pass. The archive verifiers pass
18 online archives, 53 offline archives and 35 offline repository identities and
checksums. Source-cache cleanup is closed for this selection; broader pre-build
failure-path review remains open. Final images still require build approval and
fresh online/offline installation acceptance afterwards.
