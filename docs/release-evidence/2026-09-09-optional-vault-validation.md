# Optional encrypted vault — candidate validation

Local preparation only. No commit, push, publication, or final ISO build is
authorized by this record. The frozen September 8 test images are unchanged.

Follow-up: the [external-lock and recovery pass](2026-09-09-vault-lock-recovery.md)
found two defects outside this initial lifecycle test and supersedes Vault 3
with Vault 5. Keep the historical results below tied to their tested versions.

## Requested policy and implementation

Encrypted Credential Vault is a separate, off-by-default package, enabled in
**Turn Aero7 features on or off**. Credential Manager opens the companion only
when installed. Enabling or disabling requires administrator authorization and
sign-out. Removal retains encrypted vault files and account settings; shared
KWallet dependencies are not removed. Explicit per-user overrides are preserved.

The Qt Widgets companion uses the established icon pack and native KWallet
encryption/password prompts. It manages only its dedicated **Aero7 Credentials**
collection and **Generic Credentials** folder. Passwords are masked unless
explicitly revealed in the editor. No custom cryptography, browser import,
autofill, Windows domain integration, password recovery, or plaintext export is
provided. The native setup/password dialogs still have KWallet branding.

## Package candidates

| Package | SHA-256 |
| --- | --- |
| linux-control-panel 0.1.0-53 | `f86749fe4ce5a8bcfaa165a389784326870c20de1b85fec9dd204bf7ea424bcc` |
| aero7-desktop 0.2.0-32 | `edc3b7ed82677854640cbb567faf928d177b5f347986ca3d27dee7e15f54be06` |
| aero7-credential-vault 0.1.0-3 | `090fc0e388805210056efe5cb156ade3682d09c368a84591a10cc98673d50da7` |

Vault 3 source archive: `5d0f23e337fcf705d677266026f9f557c83a2d1b48a64d0b067fc409f2747e6a`.
Desktop 32 source archive: `664510f9871b3e257f20bbd8d494f5f5921a54c034e800f5dae9846a7b3b0622`.
Candidate archives/recipes/build logs are retained under
`work/beta2-vault.yiwVK1/`; reviewed logs are copied into
[vault-validation-logs](vault-validation-logs/).

Normal pacman upgrades enforce dependencies in the VM. Desktop/Control Panel
build-host `makepkg --nodeps` only avoids installing VM-only runtime dependencies
on the host; it does not waive installation dependencies or skip build tests.
The host's fakeroot emitted a payload warning on package creation; package
creation exited successfully, ownership was inspected, and normal VM file checks
reported zero missing files. This is not a claim of reproducible-build acceptance.

## Automated checks

- Control Panel: all 20 CTest groups pass, including optional catalog and applet
  routing assertions.
- Desktop 32: all 9 CTest groups pass. Its portal-policy group contains 9 Python
  cases, including explicit user overrides and startplasma's KDE identity.
- Vault 3: the UI CTest passes (7 test methods plus initialization/cleanup).
  These use a fake backend, not proof of native encryption or D-Bus behavior.
- Installer: all 85 disk-plan tests pass, including an optional vault fixture
  that is cached with a checksum but not installed as a core package.

## Native VM evidence so far

Online test VM `aero7-r10-online`, user `aero7test`, Wayland 1920×1080,
KWallet 6.29.0-1. Only synthetic credentials are used.

- Vault 3 normal upgrade and reboot passed. Boot
  `dbfa7dbb-dba6-4a2d-9bcd-09a9e42db885` had zero failed user units and enabled
  wallet policy. Installed file checks: Desktop 81, Control Panel 74, Vault 25,
  all present.
- Native creation cancellation returned to a retryable locked UI. Immediate
  retry reopened the native wizard without restarting the app or backend.
- Created a native password-protected test wallet using a non-empty password.
  Added a synthetic credential, reopened it masked, explicitly revealed it,
  changed the username/password, and saved.
- **Lock vault** cleared the list and disabled editing. Unlock required the
  native password prompt; an intentionally wrong password was rejected. The
  correct password restored the edited entry and exact edited test value.
- Cleared the feature checkbox, confirmed removal, approved the normal Aero
  administrator prompt, and observed successful removal/sign-out guidance.
- After removal and reboot, the package/executable were absent, wallet policy
  was false, and all three saved wallet files had exactly the same hashes as
  before removal. Files were mode 0600.
- Re-enabled through the feature checkbox, reviewed the plan, and approved
  administrator authentication. Installation from the checksum-verified local
  optional cache succeeded (`vault-reenable.kmgUO4`).
- Reboot `75afc4e8-aa06-4884-a93d-6ac696dd9891` with Desktop 32/Control Panel 53/
  Vault 3 passed: enabled wallet policy, normal XDG config directories and zero
  failed user units. The original vault password restored the saved entry and
  exact edited synthetic password after removal/reinstall/reboot. Evidence:
  `vault3-boot.Wf6kmi` and `a7-vault-retained-value.png`.
- Native **Remove** confirmation passed both branches: **No** retained the
  selected synthetic entry; **Yes** deleted it and left an empty list with
  Edit/Remove disabled. Only the QA-created credential was deleted.
  The vault was then locked and the app closed; final metadata/journal audit:
  `vault-state.kZaozf`.

The app log still records Qt's host-portal app-ID registration warning because
the portal cannot open the protected process's `/proc/<pid>/root`. Native vault
operations above work despite that warning. Process protection was not weakened
to suppress it; this is not a claim of warning-free application logs.

The Vault 3 archive is now in the local ISO preparation package directory and
checksum manifest; all 15 manifest hashes pass. It is listed as optional, not
core. This is preparation for a future build, not verification of availability
on older installations or in the frozen images.

## Reproduced issues and corrections

Vault 1's asynchronous KWallet open never completed after setup cancellation.
Vault 2 used a reply-bearing open call, but the native service sent the wrong
result variant on a dismissed collection-creation prompt. The libsecret bridge
then hung. Vault 3 handles Secret Service prompts directly, treats dismissal as
cancellation regardless of the unused result payload, and verifies the actual
collection before obtaining a compatibility handle. The native Cancel/retry
replay above now passes. Actual locking uses Secret Service collection locking,
not merely closing the compatibility handle.

Desktop 31's disabled-wallet policy wrote only `aero7-portals.conf`. Boot
`f7c9d095-6c81-4ab8-8e2a-62173d3e4ed9` exposed that startplasma changes
`XDG_CURRENT_DESKTOP` to `KDE`; the portal ignored the Aero7-named file and still
started the disabled wallet portal, which exited 255. Zero failed units in a
later snapshot did not mean a clean startup. The journal caught the failure.
Desktop 32 writes both Aero7 and KDE runtime policies. A regression test fails
before and passes after this correction. Full build and normal VM upgrade pass.
Corrected boot `58e23d95-108e-49db-bb6a-86d6c6dabb2e` passes the disabled-state
replay: package/executable absent, effective wallet policy false, KDE runtime
Secret provider set to `none`, zero failed user units, and no KWallet/ksecretd
startup or exit-255 lines in the complete user journal. Saved vault files remain
byte-identical. Evidence: `vault-off-boot.CqdXvl`, not the earlier failed
Desktop 31 replay `vault-off-boot.qTnWHE`.

## Remaining acceptance

- External-lock editor dismissal, backend failure and concurrent-client stress
  beyond fake-backend coverage.
- GPG-backed setup, multi-user migration and broader credential threat review.
- Reviewed candidate source/recipe promotion and complete core-package manifest
  alignment remain pending. The vault archive alone is staged; current frozen
  media do not contain this feature or these fixes.
- Full Beta 2 release gates remain open; these bounded tests are not final ISO,
  physical-hardware, or whole-desktop acceptance.
