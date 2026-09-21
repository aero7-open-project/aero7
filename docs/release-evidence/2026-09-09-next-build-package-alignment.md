# Next-build package alignment — 9 September 2026

Local preparation only. No final ISO was built, no repository was published,
and no commit or push was made. Frozen r10 media remains historical evidence.

## Corrected selection

The previous next-build manifest still selected several packages predating the
normally installed component fixes. The following verified archives now replace
those entries or join the required local transaction:

| Component | Previous selection | Next-build selection |
| --- | --- | --- |
| Desktop | 0.2.0-29 | 0.2.0-32 |
| File Explorer | 25.12.3-50 | 25.12.3-54 |
| Control Panel | 0.1.0-50 | 0.1.0-53 |
| AeroThemePlasma | release 46 | release 57 |
| Paint | 25.12.3-8 | 25.12.3-9 |
| Programs Center Beta, optional | release 2 | release 3 |
| Spectacle | 1:6.7.4-2 | 1:6.7.4-3 |
| Qt Base | base repository version | pinned 6.11.2-3.1 correction |
| UAC agent | repository release 1 | pinned release 2 correction |

Credential Vault remains the separately verified optional 0.1.0-6 candidate.
There are now 17 checksum-selected archives: 15 required and two optional.
Programs Center Beta and Credential Vault are the only optional entries, and
neither is added to the required transaction. No artwork or Shell pin changed.
Shell remains `cf4d1d8969dfa5ae84308c937cc60146ea59f216`.

The archive hashes were checked against the component reports and actual QA
input copies before selection. The exact inventory is retained alongside this
report. Local selection is not a public package-repository promotion.

## Verification

- All 17 selected archive checksums pass, with no overlapping package-owned
  files in the project checker. Native shared-dialog package linkage passes.
- Online archive hygiene passes for all 17 archives. Offline hygiene passes
  for those plus 35 custom dependency archives; all 35 offline repository
  identity/version/hash records match their manifest.
- The complete project checker passes all 149 Python tests, Bash/Python/QML
  syntax, ShellCheck, icon provenance, theme branding/repeat-setup checks and
  the unchanged Shell parity check. No generated-source or legacy-tree cleanup
  was needed in this pass.
- Dependency checks now retain version constraints and use pacman's `vercmp`
  semantics, including epochs, package releases and versioned providers.
  They inspect the final modeled package set after replacements, reject
  mutually conflicting packages, and check each optional feature independently.
- Negative in-memory fixtures confirm that an older embedded KWallet cannot
  satisfy `kwallet>=6.29.0`, and that one disabled optional feature cannot supply
  another optional feature's required dependency. No host packages or original
  package archives are modified by these tests.

Manifest SHA-256: `2efbdeb98a834de8a175f238583097dbb2ea5813cfb6071cda2bd84d4cd9e883`.
Required-list SHA-256: `238b0e341daae4af0240b35650d04952e1c84f48a864bda93f065355dffc58f8`.
Optional-list SHA-256: `3ee8b94ffd671697ec11410d4e3baa4f890b4339b9414798e2e864645d2ffb71`.

Evidence: [complete checker output](package-alignment-logs/check.log),
[selected archive manifest](package-alignment-logs/beta2-local-packages.sha256),
[required list](package-alignment-logs/beta2-local-package-names.txt),
[optional list](package-alignment-logs/beta2-optional-package-names.txt).

## Still required

Follow-up: the [combined offline upgrade and reboot](2026-09-09-aligned-stack-offline-validation.md)
now passes a real 15-package transaction and post-reboot checks in an existing
QA guest. The original metadata-only scope below remains historical; fresh
installer sequencing is still pending.

These are package-input and metadata checks, not a real pacman transaction,
fresh combined-stack installation, live-image runtime test or security audit.
The offline base/custom bundles remain unchanged: corrected local packages are
applied by the existing later installer transaction. That sequencing still
requires a combined-stack replay; a final dependency graph alone cannot prove
each intermediate transaction succeeds.

Remaining desktop workflow/recovery and vault security checks continue. Final
image assembly needs the user's approval, followed by end-to-end verification
of both final images. Website download names, sizes, hashes and fresh screenshots
must come from those accepted artifacts, not this package list or older r10 ISOs.
