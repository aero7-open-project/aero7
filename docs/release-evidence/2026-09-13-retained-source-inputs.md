# Retained source inputs for the selected Beta 2 packages

13 September 2026. Local source-input traceability and snapshot comparison only.
No source was fetched, no build/package functions ran, no VM or production
package changed, and no commit, publication or final ISO build occurred.

## Declared inputs: all present

The [recipe audit](2026-09-13-selected-stack-alignment.md#recipe-traceability)
established matching retained recipes for all 18 selected archives. This pass
rechecks those archive/recipe hashes before asking `makepkg --printsrcinfo` for
the trusted recipes' declared inputs. It does not execute their prepare, build,
check or package functions.

The [final input audit](source-input-logs/final-input-audit.json) completes with
exit 0 and no missing or mismatching inputs:

| Input kind | Count | Verification |
| --- | --- | --- |
| Pinned Git sources | 10 | The exact commit or tag resolves locally; full commits are required for commit pins. Git archive SHA-256 values are recorded, and checked against the recipe where it specifies one. |
| File inputs | 82 | Every retained archive, patch, configuration and test-source file matches its declared SHA-256. |
| Signature files | 3 | Files are present and their current hashes are recorded. Signatures are **not reverified** by this audit. |

None of the ten Git sources uses an alternate object store. The report records
each input's resolved filesystem path so later cleanup can protect symlink
targets as well as the recipe-relative names. These 95 paths are retained inputs,
not disposable build output.

Two additional inputs are checked separately:

- Gadgets' install hook, which is not in its `source` array, is byte-identical
  to the selected package's actual `.INSTALL` member.
- Qt Base's supplemental icon-theming cherry-pick
  `e80e3f0cebae9c3a45a1b7ce81d6454c699d89c6` is present in the retained Git source;
  its patch hash is recorded.

The [audit script](source-input-logs/audit-source-inputs.py) and
[progress log](source-input-logs/final-input-audit.log) retain the commands'
scope. Git archive hashing follows the installed makepkg implementation. Six
[auditor tests](source-input-logs/auditor-tests-final.log) pass, checking exact,
modified and missing files, unpinned non-signature files, unsafe aliases,
unpinned Git revisions and the distinction between retaining and authenticating
a signature. These are six separate auditor tests, not an increase to the
153-test integration suite.

## Later working-tree changes: explicit comparison

The five locally snapshotted components were compared against current Git-visible
working files, including non-ignored new files. The comparison covers content,
entry type and executable bit, rather than excluding tests or companion trees
to obtain an empty diff. Archived files still on disk are also checked if their
ignore status has changed.

| Selected source snapshot | Files in snapshot | Matching files | Differences |
| --- | --- | --- | --- |
| Explorer 54 | 1,083 | 1,082 | `src/tests/aero7commondialogtest.cpp`: later concurrency tests. |
| Gadgets 25 | 52 | 52 | None. |
| Control Panel 55 | 595 | 595 | None. |
| Desktop 33 | 273 | 270 | Three files in its nested vault companion: recipe, backend and tests. |
| Vault 7 | 20 | 19 | `tests/KWalletBackendTest.cpp`: later overlap/override tests. |

The [complete comparison](source-input-logs/working-snapshot-comparison.json)
retains every differing path and both hashes; its
[script](source-input-logs/compare-working-snapshots.py) performs no extraction
or working-tree edits.

Desktop 33's nested vault copy predates the separately selected Vault 7
correction. The Desktop CMake/install rules do not build/install that companion,
and the Desktop 33 package has no vault executable or backend payload. Vault 7
has its own hash-pinned source archive and recipe, and its current backend
matches that archive. The nested differences therefore do not mean the older
vault backend is installed by Desktop 33. Any future source distribution must
retain the separate Vault 7 input; do not present Desktop 33's older nested copy
as the source of the selected Vault 7 package.

The later [Explorer concurrency tests](2026-09-13-dialog-concurrency.md) and
[Vault overlap tests](2026-09-13-vault-overlap-and-docs.md) were run against the
selected runtime builds, but are not retroactively claimed to be in those
packages' original source archives. There is no new runtime package rebuild
required by these test-only differences.

## Boundary and next work

This closes the retained-input and known later-snapshot-difference item for
manifest SHA-256
`36d3c6a00f369ff6f86cfde5124e7b712fffebe8ad3b111ffb88dc862f543258`.
It is not a comparison of every unrelated workcopy, a reproducible-build proof,
an upstream signature audit, trusted builder attestation, package-repository
promotion or fresh-image acceptance. Use the selected recipes/inputs as the
candidate's source evidence; future working-tree changes need a new review.

The [pre-build checklist](../BETA2-PREBUILD-CHECKLIST.md) still requires native
vault prompt-overlap testing, startup-diagnostic triage, the website/requirement
review and a safe build-space plan. Final ISO building remains behind explicit
approval, and final-image acceptance follows that build.
