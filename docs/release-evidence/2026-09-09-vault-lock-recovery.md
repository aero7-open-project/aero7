# Credential vault — external lock and backend recovery

Local Beta 2 preparation; no commit, publication or final ISO build. This
follow-up supplements the [initial vault lifecycle record](2026-09-09-optional-vault-validation.md).
The initial happy-path tests passed but did not establish external-lock or
backend-loss behavior. This pass reproduced and corrected two native defects.

Follow-up: [Vault 6 lock-verification testing](2026-09-09-vault-lock-verification.md)
supersedes the local candidate selection. Results below remain specific to
Vault 5, including its cold-login check.

## Reproductions

1. **External lock left the editor visible.** On Vault 3, a separate D-Bus
   client locked only `Aero7 Credentials`. The service returned `Locked=true`,
   but the Aero7 editor still displayed a revealed, unsaved synthetic password.
   Evidence: `vault-failure.tQsGLq`, `a7-vault-external-lock-before.png` and
   `a7-vault-external-lock-after.png` in [the retained logs](vault-validation-logs/).
2. **Unlock could not reactivate a stopped backend.** After stopping only the
   verified QA user's `ksecretd` process with SIGTERM, the UI correctly locked,
   but both reopening the app and retrying Unlock failed. The installed bus
   reported the generic `org.freedesktop.secrets` name was not activatable.
   `org.kde.secretservicecompat` was activatable and pointed to `/usr/bin/ksecretd`.
   Evidence: `vault-activation.4v1YYC`, `vault-failure.0anDtC` and
   `a7-vault4-unlock-retry.png`. No reboot or manual backend restart was used
   to hide this failure before testing the correction.

## Corrections

- Listen to service-level `CollectionChanged` and `CollectionDeleted` as well
  as collection property changes. A matching change rechecks the actual lock
  property asynchronously; a locked, missing or unqueryable collection clears
  the UI and dismisses the editor. Changes to unrelated collections are ignored.
- Address KWallet's activatable `org.kde.secretservicecompat` name for the
  Secret Service interface. This also avoids depending on whichever provider
  happens to own the generic name. Normal bus activation restarts the backend
  when the user clicks Unlock; no shell command, automatic password entry or
  weakened process protection is introduced.

This matches the installed behavior and upstream KWallet 6.29's
[collection-change implementation](https://raw.githubusercontent.com/KDE/kwallet/v6.29.0/src/runtime/ksecretd/kwalletfreedesktopservice.cpp)
and [compatibility bridge service selection](https://raw.githubusercontent.com/KDE/kwallet/v6.29.0/src/runtime/kwalletd/secretserviceclient.cpp).

## Package and automated evidence

Current local candidate: `aero7-credential-vault 0.1.0-5`.

- Source archive SHA-256: `be74d32bd01df5b9f5a8dc972a61a3c084913a4f76bb11003d4b89bd687683d3`.
- Package SHA-256: `0f148be8594ef7eab1f25b6607577981cfdd7a3ec07b4e5cf6bcbf11f2e40cdf`.
- Installed binary SHA-256: `31fe1e4f3b7e8148ae73edeee125cee07b8e1cbb2f96e48b139f3a223e6632f2`.
- Full makepkg build/check/package passed with two build jobs and no dependency
  override. Two CTest groups pass: 7 UI test methods and 7 backend test methods,
  each also recording initialization and cleanup (18 QtTest results total).
- The backend tests use an isolated bus and a separate mock service process,
  without host activation directories. They cover the real D-Bus signal path,
  editor dismissal, unrelated/unlocked changes, collection disappearance,
  service loss and operation without the generic service alias.
- External-lock and deletion regression cases failed before the signal fix.
  The missing-generic-alias case failed before the service-name fix. The final
  package's complete suites pass. Fake services do not prove native encryption.

Build provenance: `work/beta2-vault.yiwVK1/vault5/`; copied evidence includes
`vault5-build.log`, `vault5-PKGBUILD`, `vault5-tests.log` and the earlier
`vault4-regression-before.log`/`vault4-regression-after.log`.

## Native installed-VM replay

Online VM `aero7-r10-online`, Wayland 1920×1080, KWallet 6.29.0-1,
Desktop 32 and Control Panel 53. Boot `75afc4e8-aa06-4884-a93d-6ac696dd9891`.
Only synthetic QA credentials were used.

- Normal upgrade passed without dependency/file-conflict overrides; all 25
  installed package files were present. Evidence: `vault5-upgrade.mobISu`.
- From the previously stopped-backend state, Unlock activated KWallet and
  displayed its password prompt. Correct authentication reopened the vault.
- With an unsaved, revealed password in the editor, another client locked the
  actual collection. The editor disappeared and all editing controls disabled.
  Reauthentication reopened an empty list: the unsaved entry was not written.
- Saved `qa-recovery.invalid`, then edited its password without saving and
  deliberately revealed that draft. SIGTERM to the verified QA-user backend
  closed the editor and cleared the list.
- Unlock in the **same app process and desktop session** reactivated the
  backend and required the original vault password. The saved record returned
  masked. Explicit Show password confirmed the exact original synthetic value,
  `Saved-RecoveryQA-42`, not the unsaved draft `Unsaved-LostQA-99`.
- The journal confirms backend PID 11070 stopped and PID 14008 started through
  normal D-Bus activation. Final user-unit audit showed zero failed units.
  Evidence: `vault-failure.NG7M3A`, `a7-vault5-lock-before.png`,
  `a7-vault5-lock-after.png`, `a7-vault5-no-unsaved-record.png`,
  `a7-vault5-loss-before.png`, `a7-vault5-loss-after.png`,
  `a7-vault5-loss-recovery-prompt.png` and `a7-vault5-recovered-value.png`.

## Post-upgrade cold login

A normal reboot and login passed on boot
`5e340f25-4831-47aa-820a-5bb74cf76a5e`. The installed package audit found
all Desktop 32, Control Panel 53 and Vault 5 files present, normal session
configuration paths, the explicitly enabled wallet policy, and zero failed
user units. The vault initially opened locked and required its original
password. The saved test record returned; its editor initially masked the
password, and explicit Show confirmed `Saved-RecoveryQA-42` after reboot.
The editor was cancelled without changes, then Lock cleared the list and
disabled editing before the application was closed.

Evidence: `vault5-boot.avgMRu`, `a7-vault5-cold-current.png` (password prompt),
`a7-vault5-cold-unlocked.png`, `a7-vault5-cold-editor.png` (masked),
`a7-vault5-cold-value.png` and `a7-vault5-cold-locked.png` in the retained logs.

## Integration and remaining gates

The local optional-package checksum manifest now selects Vault 5; the earlier
Vault 3 archive remains only as historical local material. No core package
dependency enables the vault by default. Existing frozen ISOs remain unchanged.

Post-upgrade cold-login verification passed. Broader concurrent-client stress,
GPG/account-override combinations, multi-user behavior and credential
threat review remain open. The retained protected-process portal warning is
not suppressed. Full candidate-stack promotion, final-media and physical-device
acceptance remain separate release gates; these results do not complete the
whole desktop bug pass.
