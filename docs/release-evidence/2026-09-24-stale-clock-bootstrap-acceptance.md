# Beta 2 stale-clock bootstrap acceptance — 24 September 2026

This report records the fix and clean-install VM acceptance prompted by a
physical Aero7 installation whose firmware clock made the Aero7 and Arch HTTPS
certificates appear not yet valid. The rebuilt images remain unpublished. They
are candidates for the planned Friday release decision, not authorization to
enable downloads or merge `testing` into `main`.

## Reproduced failure

The physical system reached `pacman -Syu`, but failed to retrieve `aero7.db`,
`core.db` and `extra.db` with OpenSSL result 9: the certificate was not yet
valid or the system clock was incorrect. The repository itself was available.
At the time of the report, the affected certificate validity periods began in
September 2026, so a firmware date before that month made every HTTPS mirror
look untrusted.

The old first-run order could also write that stale system time back to the RTC
before starting network time synchronization. That made the problem survive an
offline installation and reboot.

## Implemented safeguard

Each image now embeds its validated UTC build epoch at
`/usr/share/aero7/build-epoch`. A one-shot
`aero7-clock-bootstrap.service` runs before networking, package initialization,
the installer and OOBE. It advances a clock only when it is older than the
installation-media build time. It never moves a newer clock backwards, and
normal network time synchronization remains responsible for exact time.

The same service and build epoch are copied into the installed system and
enabled at `sysinit.target`. OOBE applies the same floor before saving the
system time to the hardware clock. Missing, malformed and implausible build
epochs stop safely instead of setting an arbitrary date.

The QEMU launcher now accepts `--rtc-base YYYY-MM-DDTHH:MM:SS`, allowing this
failure class to be reproduced deliberately rather than waiting for a machine
with a flat RTC battery.

## Source and image gate

- all 164 Python integration tests passed;
- all 3 C++/Qt tests passed;
- Python syntax, Bash syntax, QML syntax, ShellCheck, package closure, source
  policy and static release checks passed;
- unit coverage proves a stale clock advances, a newer clock remains unchanged,
  and missing, malformed or out-of-range media metadata is rejected;
- both exact images passed `scripts/verify-release.sh`, including the embedded
  epoch, service contents, enablement link and offline package closure.

## Exact unpublished candidates

Both images use signed self-hosted repository build
`20260923T180513Z-ce604b74debf` and signing-key fingerprint
`72C79ABBBBE96446DD3324042694BFE1090F4FD6`.

| Variant | Filename | Exact bytes | SHA-256 |
| --- | --- | ---: | --- |
| Offline — recommended | `aero7-beta2-offline-2026.09.24-x86_64.iso` | 3,406,675,968 | `653c1d891e79823eecddd185501ba943ef97e18a789a990d18f75259dc5d0e5a` |
| Online | `aero7-beta2-online-2026.09.24-x86_64.iso` | 1,615,720,448 | `7e93cfc862d9018668003dfcc877a44125d4fada05f6de2838df6dbe7e841cd2` |

## Offline clean-install cycle

The exact offline candidate booted with its emulated firmware clock fixed at
`2026-08-01T00:00:00Z`, before the repository certificates were valid. In the
live environment, the clock advanced to 24 September, the bootstrap service
was active and Arch database synchronization completed over HTTPS.

The graphical installer then completed a clean UEFI installation to a new
40 GiB disk. OOBE created a password-protected user, retained the recommended
ask-before-installing update policy, selected `Europe/Amsterdam`, displayed the
correct 24 September date and reached the desktop. In the installed system:

- the bootstrap service was enabled and active;
- the UTC date remained valid;
- `pacman -Syy` synchronized `core`, `extra` and `aero7` successfully;
- a second reboot reached the Aero7 login screen and the service remained
  active with a valid date.

## Online clean-install cycle

The exact online candidate repeated the same test from a fresh disk and the
same deliberately stale `2026-08-01T00:00:00Z` firmware clock. Before disk
changes, the live bootstrap service advanced the date and `pacman -Syy`
downloaded `core` and `extra` over HTTPS.

The installer then downloaded 1.66 GB of packages, completed package hooks,
bootloader and system configuration, and rebooted into OOBE. OOBE selected the
recommended update policy, `Europe/Amsterdam` and the public network profile,
showed the correct date and reached the desktop. In the installed system:

- the bootstrap service was enabled and active;
- `pacman -Syy` synchronized `core`, `extra` and the self-hosted `aero7`
  database successfully;
- the second reboot reached the Aero7 login screen;
- after that reboot the UTC date remained valid and the bootstrap service was
  active.

## Scope and release boundary

This closes the reproduced stale-firmware-clock/TLS failure for both exact
candidates. QEMU's hardware-clock read timed out once with its deliberately
fixed `clock=vm` test mode, so this report does not claim a physical RTC battery
or motherboard clock certification. The boot-time floor, OOBE ordering, HTTPS
database refresh and two-boot installed-system behavior were all demonstrated.

Neither ISO was uploaded or published during this pass. Publication still
requires final upload, download-back checksum verification and the release
owner's explicit approval.
