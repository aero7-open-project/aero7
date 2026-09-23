# Beta 2 self-hosted-repository candidate acceptance — 23 September 2026

This report records the rebuild and clean-install VM acceptance of the Aero7
Beta 2 candidate pair assembled from the new self-hosted package repository.
It is internal release evidence. Neither ISO was uploaded or published during
this pass; publication remains deferred until the release decision on Friday,
25 September 2026.

## Repository input

- public package repository: `https://aero7.org/repo/$arch`;
- repository build: `20260923T180513Z-ce604b74debf`;
- repository database SHA-256:
  `4c5b932d1998e2b2e649cb406e2e55d714abab51f8c6a02c2dd42f22739c9a9b`;
- signing-key fingerprint:
  `72C79ABBBBE96446DD3324042694BFE1090F4FD6`;
- source commit containing the restored AeroTheme integration:
  `ce604b74debf0edc4ee599895bd48bebfcff84a0`.

The repository database, detached database signature, all selected package
signatures and package identities were verified before image assembly. The ISO
source lock and installer adapter point to the same repository URL and database
identity. Supplemental Plasma, Qt, KWin, Spectacle, KWallet and optional-vault
packages remain checksum-pinned local Beta 2 inputs.

## Exact unpublished artifacts

| Variant | Filename | Exact bytes | SHA-256 |
| --- | --- | ---: | --- |
| Offline — recommended | `aero7-beta2-offline-2026.09.23-x86_64.iso` | 3,406,655,488 | `5998c42d74b4802d3da1f427b56162b813787fa515edc7c5f7517e5f65796492` |
| Online | `aero7-beta2-online-2026.09.23-x86_64.iso` | 1,615,704,064 | `52c646d3c0458fad8081d8b6d97c4ac36d787836a6ef55b2e8267e6e6e2fc14a` |

`scripts/finalize-release-artifacts.py` re-verified both exact files and wrote
the private candidate `SHA256SUMS` and `BETA2-ARTIFACTS.md` records under
`out/beta2-candidate-2026.09.23/`. The release verifier passed both images,
including the offline dependency closure, 78 selected archives and 50-entry
embedded Aero7 repository.

## Source and structural gate

- all 162 Python integration tests passed;
- Bash syntax, ShellCheck and `git diff --check` passed;
- the package-identity guard verified that the maintained
  `aero7-file-explorer` package provides the pinned shell's legacy
  `aero7-dolphin` dependency;
- the repository URL, signature fingerprint and database hash agree across the
  source lock, installer adapter and candidate input;
- both powered-off installed-system QCOW2 images passed `qemu-img check` with
  no errors.

## Online clean-install cycle

The online ISO completed a clean UEFI/Q35 installation to a new 40 GiB disk.
OOBE created a password-protected account, retained the recommended
ask-before-installing update policy, selected `Europe/Amsterdam`, applied the
public firewalld profile and reached the Aero7 desktop.

The installed system then passed these checks:

- the taskbar shortcut opened **File Explorer** with its own name and icon;
- Start search found **Turn Aero7 features on or off**, and the manager opened
  without an error with Programs Center Beta shown as not installed;
- firewalld, NetworkManager and SDDM were enabled, and firewalld was active;
- a full reboot reached the unclipped Aero7 Professional login screen and a
  password login returned to the desktop;
- the desktop diagnostic folder's 91-entry SHA-256 manifest verified in full;
- collected system and user failed-unit lists were empty and no coredumps were
  found;
- the powered-off disk image passed `qemu-img check`.

## Offline clean-install cycle

The first offline run exposed a QA-launcher problem: omitting network options
allowed QEMU to create its default NAT adapter. That run was rejected and its
disposable disk was deleted. `scripts/run-qemu.sh --no-network` now passes an
explicit `-nic none`, preventing QEMU's implicit adapter.

The exact offline ISO was then installed again from the beginning. The recorded
QEMU command line contained `-nic none`. Installation and OOBE completed from
the embedded repositories, reached the desktop, launched File Explorer, rebooted
to the Aero7 login screen and returned to the desktop after password login.
Post-shutdown evidence confirms:

- captured network inventory contains only `lo`;
- captured routes contain no external interface or default route;
- the desktop diagnostic folder's 92-entry SHA-256 manifest verified in full;
- collected system and user failed-unit lists were empty and no coredumps were
  found;
- firewalld and SDDM remained enabled;
- the powered-off disk image passed `qemu-img check`.

This establishes a genuinely disconnected installation rather than merely an
installation that happened not to download packages.

## Release boundary

The exact pair above is ready for the Friday publication decision, but is still
unpublished. No website download button, public ISO URL, tag promotion or main
branch merge is authorized by this report. A release still requires upload,
download-back hash verification and the release owner's explicit go-ahead.

The VM pass does not certify physical GPU drivers, USB/hotplug, real multi-monitor
hardware, every optional feature or universal hardware compatibility. Those
limits remain visible in the release documentation.
