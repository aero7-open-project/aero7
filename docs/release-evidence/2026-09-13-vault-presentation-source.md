# Aero7 vault native-dialog presentation — source checkpoint

Updated 20 September 2026. **Source and test-package VM acceptance are complete;
release package selection and final-media acceptance remain open.**

## Change

Added a maintained downstream integration at
`aero7-desktop/integration/credential-vault/kwallet/`. It applies to the exact
wallet name `Aero7 Credentials` and changes unlock, retry, setup introduction,
new-password, access and password-change presentation. Other wallet names retain
upstream presentation. An empty caller ID is not relabelled as a trusted Aero7
request; caller text and backend error descriptions are HTML-escaped.

The native service embeds the existing optional vault's unchanged pack icon,
SHA-256 `ee4f3b564acf5559cb73997e2ad9cd3a0c322b0f9b73ed3f0aaa4331c69b5d71`.
No artwork was generated. Setup still offers both upstream encryption choices
with the same default; permission result values and cancellation remain intact.

The patch does not edit cryptographic implementations, storage format, wallet
names, service identifiers, permission keys, allow/deny persistence or Secret
Service transaction handling. The [whole-source comparison](vault-presentation-logs/source-diff.log)
finds changes only in `ksecretd.cpp`, `knewwalletdialog.cpp`, their CMake file and
the two added presentation/icon files. Diff exit 1 is the expected source
difference, not a passing test code. The later
[installed-VM replay](2026-09-20-vault-presentation-native-vm.md) verifies the
compiled change in the target environment.

## Inputs and build

- KWallet upstream 6.29.0 tarball SHA-256:
  `66a47fc170ea074cce8b916fa313f309d7c9497bd2132e0598d4b63bbad2ac88`.
- Arch reference recipe tag `6.29.0-1`, commit
  `2fa55cbc2a8a2b9b1e7ffcc201b45ccc199be7e1`.
- Work directory: `work/kwallet-presentation.GdVXLq`, with both pristine and
  prepared extractions. The source checksum matches the pinned Arch recipe;
  no upstream PGP-signature verification is claimed at this checkpoint.
- CMake/Ninja builds the actual `ksecretd` and upstream `fdo_secrets_test`
  targets with two jobs and GPG enabled. No host installation was performed.
  The [build recheck and binary hashes](vault-presentation-logs/build-check.log)
  retain the completed outputs. The initial build had warnings in unchanged
  upstream cipher, GPG, attribute and portal code; this is not warning-free.
- Local daemon SHA-256:
  `bf863c3f269a3635ec4a61a8808b1a7f4ec899276a2fc50a6780bd4de81934b9`.

## Test evidence

1. [Presentation suite](vault-presentation-logs/presentation.log): 16 Qt test
   results pass, including setup/cleanup. Compiles the real patched upstream
   setup wizard and unchanged permission dialog. Covers exact-name scope,
   anonymous/supplied callers, HTML escaping, icon availability under a missing
   theme, both cipher controls/default, rejection, and all four permission
   results. Setup has the same untranslated-placeholder warning for both the
   Aero7 and unrelated wallet cases; it comes from the upstream UI's initial
   text before the constructor replaces it. No warnings were suppressed.
2. [Preparation safety tests](vault-presentation-logs/prepare.log): five pass.
   Exact patch application/reversal, byte-identical embedded icon/header,
   repeated invocation refusal, modified-input refusal, existing-overlay
   refusal and symlinked-source refusal are covered. Refusal leaves inputs
   unchanged. ShellCheck also passes for the preparation script.
3. [Upstream Secret Service suite](vault-presentation-logs/upstream-secrets.log):
   16 results pass, including setup/cleanup. Uses upstream mock daemon methods;
   it does **not** exercise the new `internalOpen()` dialog path. It runs with
   a private D-Bus session inside a network-isolated bubblewrap namespace,
   read-only host filesystem and temporary writable test/config/data paths.
   It cannot modify the real user's wallet or use the host session bus.

## Installed-VM follow-up and remaining work

The traceable test package (`kwallet 6.29.0-1.1`, SHA-256
`1079461023f7d105646675cc88ac6d4e14754cec379bee49c14046d552faf8db`)
was upgraded normally in the 1920×1080 online Wayland VM and rebooted. The
[native replay](2026-09-20-vault-presentation-native-vm.md) exits 0 after the
real Aero7 unlock prompt, wrong-password retry, cancel, relock, two overlapping
clients and two complete synthetic read/lock retention cycles. Packages,
desktop-service state, wallet filenames/non-ciphertext metadata and final lock
state are preserved; no user or system unit is failed at the checkpoint.

The runtime replay closes the scoped existing-vault password-dialog gap. The
source suite remains the coverage for setup, permission and password-change
presentation. Global first-run UI, unrelated wallet names and GPG pinentry are
outside the exact `Aero7 Credentials` scope and must not be advertised as a
complete wallet-UI replacement.

Before final media, select a release-built package and reconcile online/offline
dependency closure, source evidence and release documentation.

The selected 18-archive manifest is still unchanged, SHA-256
`36d3c6a00f369ff6f86cfde5124e7b712fffebe8ad3b111ffb88dc862f543258`.
The KWallet override is not yet selected. The login Ease of Access gate remains
open, and the vault gate remains open only for release-package selection and
image integration. No final ISO was built and nothing was committed or
published.
