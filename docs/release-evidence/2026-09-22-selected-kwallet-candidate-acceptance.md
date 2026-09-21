# Refreshed online/offline candidate acceptance with selected KWallet

## Scope

On 22 September 2026 the online and offline test profiles were rebuilt after
selecting the accepted `kwallet 6.29.0-1.1` Aero7 presentation package. These
are internal test candidates. They are not the final Beta 2 downloads and this
record does not authorize signing, uploading, website publication or promotion
of packages.

The configured filenames retain the 21 September build label even though the
artifacts in this record were rebuilt and verified on 22 September:

| Variant | Bytes | SHA-256 |
|---|---:|---|
| `aero7-beta2-online-2026.09.21-x86_64.iso` | 1,604,804,608 | `473af71c81bb3686fdcf43250aee67dc23172a2840a50fa30e584fcf1b3bf6c1` |
| `aero7-beta2-offline-2026.09.21-x86_64.iso` | 3,407,151,104 | `44e687a2edcc8fcad9faf0300d3080ccbceed16f6b973e51d65fb5650ad215f8` |

The builder completed both exports with exit status 0. The source gate passed
155 integration tests. Release verification passed bootability and embedded
source checks for both images, including 19 selected online archives and the
offline set of 84 dependency archives plus 65 repository entries. The selected
KWallet archive digest is
`1079461023f7d105646675cc88ac6d4e14754cec379bee49c14046d552faf8db`.

## Offline candidate

A new 40 GiB VM completed the installer, first-run setup, update-policy choice,
Europe/Amsterdam time zone, public firewalld profile and reboot into the
installed desktop. The installed package audit reports:

- `kwallet 6.29.0-1.1`
- `aero7-desktop 0.2.0-33`
- `aero7-file-explorer 25.12.3-55`
- `linux-control-panel 0.1.0-55`
- no installed `aero7-credential-vault` before the optional feature is enabled

Both optional packages are retained in `/var/cache/aero7/optional-packages`.
The cached Vault 7 archive reports the expected package identity and digest
`55cae7104828152b935e3b72315dd588a898c48b12072a05039708e5aaa0e50e`.
The installer log records the offline base transaction entirely from embedded
`/usr/share/aero7/offline-packages/base` archives. Host release verification
also closes the complete dependency set. This VM had a virtual NIC available,
so this particular replay is not described as a new physically disconnected
installation.

The Optional Features helper installed Vault 7 from the verified local cache
and logged a successful transaction. The native first-use path then displayed
the KWallet wizard and password dialog as **Aero7 Credential Vault**, with the
existing bundled icon and Aero7-specific text. No stock KDE Wallet title was
visible. The feature remained off by default before that deliberate test.

The previous normal boot has no coredumps. Its error-priority entries are the
known virtual-QXL/software-rendering output fallback and shutdown-time network
dispatcher diagnostics. The periodic test-log collector completed normally
after login; a second collection happened to be running when QA requested
poweroff and was terminated by shutdown. That shutdown-only result is retained
rather than presented as a warning-free log.

Screenshots:

- [installed SDDM](selected-kwallet-candidate-images/offline-sddm.png)
- [installed desktop](selected-kwallet-candidate-images/offline-desktop.png)
- [native Aero7 vault password dialog](selected-kwallet-candidate-images/offline-vault-password.png)

## Online candidate

A separate new 40 GiB VM completed the online installer and booted from the
installed disk. OOBE created the account, accepted the recommended daily check
with approval required before installation, selected Europe/Amsterdam and
applied the public firewalld zone. Finalization reached the installed desktop.

The installed audit reports the same selected Desktop 33, Explorer 55, Control
Panel 55 and `kwallet 6.29.0-1.1` packages. Vault 7 is absent by default, while
its cached archive and checksum match the offline candidate. SDDM,
NetworkManager and firewalld are enabled; OOBE is disabled after completion.
The graphical boot has no error-priority journal entries, no failed-unit result
and no coredumps.

The OOBE log retains two known shell-validator warnings: the image-mode package
origin is not a signed-repository installation record, and the historical
Plymouth five-second-hold check is not satisfied. Both were already recorded by
earlier candidate evidence; neither is hidden or reclassified as a clean log.

- [installed online desktop](selected-kwallet-candidate-images/online-desktop.png)

## Selected KWin logout guard recheck

The selected KWin `6.7.4-7.3` prepared source was rechecked after the candidate
acceptance so the launch checklist would not rely on a stale historical status.
The structural policy guard passes and confirms that the unconditional logout
deadline remains removed, cancellation fails closed, and logout despite pending
windows still requires the explicit **Log Out Anyway** action. The controlled
production-method harness passes all 11 notification-enabled results and all six
notification-disabled results. This is the exact source used for the selected
KWin archive, not the older `7.1` checkpoint.

The native installed-VM evidence remains the runtime authority: the
[unsaved-work logout report](2026-09-09-unsaved-work-logout.md) records survival
past the former deadline, document preservation, Cancel Logout, notification
dismissal, explicit override, ordinary logout, normal power-off and cold start.
It also records the retained unrelated teardown warnings and does not claim a
universally warning-free shutdown.

## Result and remaining boundary

The refreshed candidate cycle closes the selected-package and native Vault
presentation item on the pre-build checklist. The source/package bug-test pass
is ready for owner review. Final online/offline media still require explicit
build approval, new public filenames, exact final-artifact verification and the
publication/website gates. Physical GPU, hotplug and multi-monitor hardware are
outside this VM acceptance pass.
