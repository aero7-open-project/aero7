# Vault request overlap and release-document consistency

13 September 2026. Additional tests and documentation corrections only. No
runtime behavior, selected package, final image or published content changed.

## Five backend cases

The isolated mock now holds unlock replies until explicitly released. The new
cases verify:

1. Two clients both finish when their replies arrive in reverse order.
2. Destroying the first client while it waits does not prevent the second from
   finishing its own unlock request.
3. Repeated Unlock on one opening client submits only one service request.
4. Collection deletion invalidates a pending operation; its later success reply
   does not unlock the client again.
5. A fresh process with explicit `Enabled=false` stays locked, reports the
   override, submits zero Unlock calls and leaves its configuration unchanged.

The full host suite passes 9 UI and 22 backend results, with no failures or skips.
Native Wayland replay `vault-overlap.1jjLsy` passes all 22 backend results and
exits 0. The real QA wallet stays locked; its effective policy and the desktop
service PIDs/restart counts are unchanged. The private test bus has no service
activation directories and uses only a mock wallet and temporary configuration.
This replay does not access real credential values.

Test executable SHA-256:
`31f890ce6714e21a45e23dc640b9d9e1364fe0606ae62be2112914c975f4a384`.
The runtime backend source remains byte-identical to Vault 7's source archive:
`f83b29a5d45669e8bde5d02a54122da6cac25add0ea52bbfa4e875d23b32c2e6`.
Vault 7 remains selected; these additional test cases were added after that
package was built and are not claimed to be inside its retained source snapshot.

This covers overlapping asynchronous protocol replies, not simultaneous native
password-prompt windows, all service scheduling, concurrent writes, GPG or
multi-user isolation. Those broader boundaries remain explicit.

## Documentation mismatch corrected

The standalone release notes still listed Desktop 27, Explorer 35, Control Panel
43 and other superseded candidates, alongside historical blockers described as
current. They now match all 18 selected package metadata records and distinguish
local checks, frozen-media results, final-build approval and release acceptance.
The old text is retained in the clearly marked
[historical snapshot](2026-09-13-superseded-release-notes.md).

The notes now include the approved update-approval toggle, fresh-firewalld /
existing-UFW policy, optional vault, recommended offline media and website-only
ISO distribution. The Optional Features wiki source now explains the previously
missing vault, all 15 catalog entries, 13 searchable optional features, retained
data, account overrides, locking uncertainty and offline-cache limits.

The candidate archive verifier now checks the release-notes version table against
actual package metadata and its optional labels against the package policy.
Four new unit methods reject stale/missing/extra versions, duplicate/missing
tables and incorrect optional labels. Both archive variants execute the check.
This prevents the observed version-table drift; it is not a verifier for every
prose claim or a substitute for editorial review.

## Verification and next gates

- All 153 integration tests and static checks pass.
- Online: 18 archives pass; release notes match all 18 selected versions/policy.
- Offline: 53 archives and 35 repository entries pass, plus the same notes check.
- Local-link inspection of the changed notes, handoff, QA record, historical
  snapshot and Optional Features guide found 117 targets and no missing files
  at that checkpoint; extensionless wiki links resolve to their Markdown files.
- Diff whitespace checks and the VM harness shell check pass.

Evidence is retained in [vault-overlap-logs](vault-overlap-logs/). This is progress
toward pre-build completion, not approval to publish or build final ISOs. Current
remaining work includes the supported-workflow/failure-path review and source /
package provenance reconciliation; exact final media are built and tested only
after the requested approval gate.
