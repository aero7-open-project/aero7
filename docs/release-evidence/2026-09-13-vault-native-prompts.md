# Vault 7 — native overlapping prompts and retained content

13 September 2026. Component acceptance in the existing online Wayland guest,
not acceptance of a newly built ISO. No production package changed.

## Environment and replay

Guest `aero7-r10-online`, synthetic account `aero7test`, boot
`1e33c849-b4e7-4b4b-a09e-f79a2c99b146`; 1920×1080, two CPUs, 6 GiB RAM.
Installed `aero7-credential-vault 0.1.0-7`, executable SHA-256
`b49e4aa2e4b610021778d03120f46430a87369b90696d08db734038fed587105`;
KWallet `6.29.0-1`. The existing synthetic wallet was preserved.

[Original audit](vault-native-prompt-logs/vault-native-prompts.l2hRHy/audit.log),
[harness](vault-native-prompt-logs/vault-native-prompts.l2hRHy/harness.sh) and
[protocol trace](vault-native-prompt-logs/vault-native-prompts.l2hRHy/prompt-protocol.txt)
retain the real application replay. Monitoring was limited to Unlock, Prompt,
Dismiss and Completed; no credential-read or secret payloads were monitored.
Two installed application processes, PIDs 2205/2206, were opened normally.
Left window used sender `:1.107`, right used `:1.108`.

| Interaction | Observed native result |
| --- | --- |
| Unlock both before entering a password | Separate requests `/p0` and `/p1`, one shared KWallet password dialog; both applications wait with mutation controls disabled. |
| Cancel the shared dialog | Both requests complete with dismissed=true. Both windows return locked and can retry; the real collection remains locked. |
| Retry both with correct QA password | `/p2` and `/p3` complete successfully. Both windows show the existing entry. A duplicate daemon completion for `/p2` does not stick or reopen the UI. |
| Lock from one window | Both windows clear entries and disable editing. |
| Unlock both again, then close the left waiting application | Its destructor dismisses `/p4`; remaining `/p5` stays available. The collection remains locked and only PID 2205 remains. |
| Complete the surviving prompt | The remaining window unlocks and displays the retained entry. Late daemon signals addressed to the closed client do not obstruct it. |
| Lock and close the survivor normally | Both applications exit successfully and the real collection is locked. |

Stage evidence: [cancelled](vault-native-prompt-logs/vault-native-prompts.l2hRHy/cancelled.txt),
[both unlocked](vault-native-prompt-logs/vault-native-prompts.l2hRHy/unlocked.txt),
[one closed](vault-native-prompt-logs/vault-native-prompts.l2hRHy/one-closed.txt),
[survivor unlocked](vault-native-prompt-logs/vault-native-prompts.l2hRHy/survivor-unlocked.txt).
Screenshots retain [overlap](vault-native-prompt-logs/screenshots/a7-native-vault-overlap.png),
[both unlocked](vault-native-prompt-logs/screenshots/a7-native-vault-both-unlocked.png),
[client closure](vault-native-prompt-logs/screenshots/a7-native-vault-client-closed.png)
and [final locked UI](vault-native-prompt-logs/screenshots/a7-native-vault-final-locked.png).

Focus limitation: deliberately activating the second window could partially
cover the shared native prompt. Its visible title brought it forward and the
operation completed. The Wayland request supplies an empty parent ID; this does
not establish always-on-top or perfect prompt parenting. No focus-stealing or
security bypass was added. These are QA, not final promotional screenshots.

## Original failure and follow-up

The original harness exited **1** after the GUI interactions because it required
identical encrypted `.kwl` bytes across unlock/save/lock. The ciphertext changed
from `1121ca7e…` to `d9fa7698…`; file names, salt and attributes did not change.
That assertion stopped its later package/service checks. The original result
must not be reported as an exit-0 run.

KWallet's version-tagged [save code](https://github.com/KDE/kwallet/blob/v6.29.0/src/runtime/kwalletbackend/backendpersisthandler.cpp)
prepends/appends fresh random data before encryption. Its
[close/save path](https://github.com/KDE/kwallet/blob/v6.29.0/src/runtime/kwalletbackend/kwalletbackend.cc)
can change ciphertext without changing credentials. Inspected source copies
are retained under `vault-native-prompt-logs/upstream/`. Ciphertext equality is
not a correct content-preservation invariant across these operations.

A separate [QA probe](vault-native-prompt-logs/retention/main.cpp), compiled with
the selected production backend, performed **two real native password-prompt →
read → lock cycles**. This is an instrumented backend check, not the installed
application UI replay. Backend source SHA-256:
`f83b29a5d45669e8bde5d02a54122da6cac25add0ea52bbfa4e875d23b32c2e6`.
Probe binary SHA-256:
`5e3045705e26fad7e60cc78dcf028a22f7532e7318b31e0ac0c5c51637d10588`.

Both cycles compared the exact expected entry list and complete synthetic
username/password internally, without logging the password or calling the
backend's write/remove APIs. Both matched and locked successfully.
The [follow-up audit](vault-native-prompt-logs/vault-native-retention.04Ulj3/audit.log)
and [harness](vault-native-prompt-logs/vault-native-retention.04Ulj3/harness.sh)
record exit **0**, final collection `b true`, unchanged file names,
salt/attributes, package inventory, enabled policy and desktop-service snapshots
against the original pre-GUI baseline. Shell/Plasma/KWin remained active with
PIDs 1046/845/722 and zero restarts. Both failed-unit lists were empty at this
checkpoint; no failed state was reset.

Before the follow-up, a command was mistakenly typed into the idle lock screen
and rejected as a login attempt; it never executed. Normal password unlock
restored Terminal before the successful recorded run. This QA focus mistake is
not classified as a product authentication defect.

## Conclusion

Native overlap/cancellation is verified, including retry, client closure,
surviving-client completion and retained synthetic content. The original hash
failure is preserved with its corrected interpretation. No new production fix
was required by this replay. Other users' wallets, alternate wallet backends and
physical hardware were not tested. Final ISO acceptance is still separate.
