# Credential vault — uncertain lock result and two-client replay

Local release preparation only. No commit, publication or final ISO build.
This supplements the [Vault 5 lock/recovery record](2026-09-09-vault-lock-recovery.md).

## Reproduced defect and correction

The lock-completion handler combined an unavailable lock property with a
confirmed unlocked property, briefly emitting `Unlocked` in both cases.
With the normal window attached, its subsequent refresh could discover the
missing collection and lock again. That secondary correction did not make the
initial state transition valid, and the warning did not distinguish uncertainty
from a confirmed refusal.

An isolated D-Bus regression removes the collection object during Lock and
records every backend state transition before the window's refresh handler.
It fails against Vault 5 because the trace contains `Unlocked`. Vault 6 instead
clears local access immediately on a failed reply or non-boolean/missing lock
property and warns that locking **could not be verified**. The warning directs
the user to sign out before leaving; hiding credentials is not advertised as
proof that the remote vault locked. A successfully read `Locked=false` retains
the distinct refusal warning and does not claim success.

Three added tests cover the uncertain result, a confirmed refusal, and locking
two backend/window clients. Both complete CTest groups pass: 7 UI methods and
10 backend methods, plus initialization/cleanup for each (21 QtTest results).
The failure injection runs only against a separate mock process on an isolated
bus without host activation directories. It does not establish all native
service-failure timing cases.

## Package provenance and normal VM upgrade

- Candidate: `aero7-credential-vault 0.1.0-6`.
- Source SHA-256: `e910d72111cdd089f59c7aed69bd699137a14eaa4bdac51c6fcde409547f53dc`.
- Package SHA-256: `e707d78c95d098ce082bd6f6aee1932e97408ea8bd21633ff008ba3af858c1d2`.
- Installed binary SHA-256: `be2e3a8ec1b6c21edd126429051c84abdc5910ea919bc59eb160d9ab1df8b52d`.
- Full makepkg build/check/package succeeded with two jobs and no dependency
  overrides. Normal `pacman -U` upgrade from Vault 5 succeeded; all 25 files
  were present. The verified optional cache was updated to the exact package.
- Build directory: `work/beta2-vault.yiwVK1/vault6/`.

## Native two-window check

Online VM `aero7-r10-online`, Wayland 1920×1080, KWallet 6.29.0-1,
boot `5e340f25-4831-47aa-820a-5bb74cf76a5e`. Two separate application processes
(5672 and 5673) opened initially locked. The first required the original QA
vault password; the second attached to the already unlocked same-user vault.
Both listed the existing synthetic `qa-recovery.invalid` credential.

The right window opened its editor, initially masked, then explicitly revealed
the saved synthetic password. Clicking Lock in the left window closed that
editor, cleared both lists and disabled both windows' editing controls. Both
applications closed normally. A direct read of the actual collection returned
`Locked=true`; the final user-unit audit found zero failed units. No saved
credential was edited or deleted in this check.

Evidence in [the retained logs](vault-validation-logs/):
`vault6-lock-verification-before.log`, `vault6-lock-verification-after.log`,
`vault6-build.log`, `vault6-PKGBUILD`, `vault6-tests.log`,
`vault6-upgrade.Zy8yYr`, `vault6-two-clients.3RTA2t`, and the
`a7-vault6-two-{unlocked,editor,revealed,locked}.png` screenshots.
Protected-process portal registration warnings remain recorded; protection
was not weakened to suppress them.

## Remaining boundaries

The next-build local optional manifest selects Vault 6. The frozen r10 ISOs
remain unchanged. Vault 5's cold-reboot evidence remains versioned to Vault 5;
this pass does not claim a new Vault 6 reboot or final-media test.
Concurrent credential writes, simultaneous unlock prompts, account overrides,
GPG configurations, multi-user isolation and broader threat review remain open.
This closes the reproduced uncertain-state transition and one native two-client
lock scenario, not the full desktop bug pass or release gate.
