# Aero7 vault presentation — installed VM replay

20 September 2026. **The test package passes its installed-VM presentation and
retention replay. It is not yet selected for either Beta 2 image.**

## Tested package and environment

- Package: `kwallet 6.29.0-1.1`, SHA-256
  `1079461023f7d105646675cc88ac6d4e14754cec379bee49c14046d552faf8db`.
- Guest: the existing 1920×1080 `aero7-r10-online` Wayland VM after a normal
  package upgrade and reboot/password login.
- Test data: one deliberately synthetic record only:
  `qa-recovery.invalid` / `qa-recovery-user`. The password is never written to
  the report or screenshots.
- Full passing report: [native-vm/logs/replay.log](vault-presentation-logs/native-vm/logs/replay.log).
  The harness, D-Bus prompt protocol, package/service snapshots, wallet file
  metadata and empty failed-unit reports are retained beside it.

## Visible and functional results

The real installed `ksecretd` presents the exact Aero7-scoped unlock dialog as
**Aero7 Credential Vault**, with the unchanged embedded pack icon and neutral
unlock wording. The replay verifies:

1. the initial password prompt and taskbar identity;
2. an incorrect-password retry with the Aero7 title and error text;
3. cancellation without unlocking or losing the client;
4. successful retry and display of the retained synthetic target/user while
   keeping its password out of the list;
5. explicit relocking;
6. two independently launched Credential Manager clients waiting on the shared
   native prompt and both completing after one correct unlock;
7. two additional read/lock cycles that match the complete expected synthetic
   record without calling write or remove APIs; and
8. a locked final collection, unchanged wallet filenames and non-ciphertext
   metadata, unchanged packages, unchanged desktop-service PIDs/restart counts,
   and no failed user or system units.

The encrypted `.kwl` payload receives fresh ciphertext when the wallet is saved;
its hash is therefore not used as credential-equality evidence. The retained
probe verifies the decoded synthetic record instead. Six screenshots preserve
the prompt, error, cancel, overlapping-client and successful completion states
under [native-vm/screenshots](vault-presentation-logs/native-vm/screenshots/).

## Harness correction and scope

The first full replay completed every GUI and retention action but exited 1
because its filename comparison inherited SHA-256 line order. A changed `.kwl`
ciphertext hash moved one otherwise identical filename within the snapshot. The
harness now sorts the stripped filename lists before comparing them. Rechecking
the first evidence proved the sets were identical; the complete replay was then
run again and finished with `REPLAY_EXIT=0`.

This result closes the installed unlock/retry/cancel/overlap/retention behavior
for the scoped Aero7 wallet. The source presentation suite remains the evidence
for setup, permission and password-change presentation. It does not claim that
unrelated wallet names, GPG pinentry or every upstream KWallet surface has been
rebranded. Package selection, online/offline closure and final-media testing are
still required before this can be described as shipped.
