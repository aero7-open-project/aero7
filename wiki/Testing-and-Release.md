# Testing and Release

## Current publication status

Beta 2 source, release notes and handbook updates were published on
22 September 2026. GitHub contains no ISO attachments; exact online and offline
media plus checksums are distributed through the official Aero7 website.

Beta releases use four gates: source validation, image validation, a fresh
installation, and a second installed-system boot.

## Source gate

Run:

```bash
./scripts/check.sh
```

Required results include passing backend/state-machine tests, successful QML
linting, a Release CMake/Ninja build, render-smoke captures at supported design
sizes, source-lock verification, and exact package-manifest parity.

## Image gate

Run:

```bash
./scripts/verify-release.sh
sha256sum out/aero7-beta2-online-*.iso out/aero7-beta2-offline-*.iso
```

There must be exactly one current online and one current offline Beta 2 ISO in
`out/`. The verifier inspects each boot medium and its embedded live filesystem.
These local artifacts are test inputs and are not uploaded by the source push.

## Fresh-VM gate

Launch a clean disk:

```bash
./scripts/run-qemu.sh --fresh
```

Walk through language, Install now, license, custom installation, disk
confirmation, installation, restart, account, password, update, time, network,
finalization, Welcome, Preparing your desktop, and the first Plasma session.

Confirm all of the following:

- only the disposable `/dev/vda` target is offered;
- progress and restart complete without visible rendering corruption;
- the installed disk wins boot order while the DVD remains attached;
- Plymouth, OOBE, SDDM, and Plasma carry matching Aero7 branding;
- there is one Aero taskbar, a light color scheme, populated All Programs, and
  the expected application names;
- the first desktop login is automatic;
- a clean shutdown leaves the QCOW2 image healthy.

## Disk Management fixture

To test the installed Computer Management disk view without attaching host
storage, boot the existing Aero7 VM with three disposable secondary drives:

```bash
./scripts/run-qemu.sh --installed --disk-management-fixture
```

The launcher preserves the installed Aero7 system disk and adds:

- an entirely blank 8 GiB disk;
- a 24 GiB GPT disk containing 6 GiB `PROJECTS` and 4 GiB `BACKUPS`
  partitions followed by unallocated space;
- a 64 GiB GPT disk containing a 48 GiB `ARCHIVE` partition followed by
  unallocated space.

Use these disks to check rescan, volume enumeration, proportional partition
blocks, filesystem labels, properties, mount/unmount, and unallocated-space
rendering. The fixture files live under `work/qemu/disk-management-fixture/`
and are intentionally excluded from Git.

## Second-boot gate

Boot the same VM disk again. OOBE must remain disabled and SDDM must require the
created account password, proving that temporary first-login autologin was
removed.

## Beta 2 artifacts

- offline file: `aero7-beta2-offline-2026.09.22-x86_64.iso`
- offline size: `3,407,151,104` bytes
- offline SHA-256: `f44c52bf8171fd2842e2c6150909e9ca70a577f4e3ac9f6444baeea45f1676a5`
- online file: `aero7-beta2-online-2026.09.22-x86_64.iso`
- online size: `1,604,804,608` bytes
- online SHA-256: `e1744b3be9692af6252bfdc42b83a1bc4c309f33f300771dd3b26cfeacafc936`
- source release tag: `v0.2.0-beta.2`

The repository's `docs/BETA2-QA-STATUS.md` and linked evidence reports record
the automated and VM acceptance scope for this release line.

## Beta 2 release gate

The source, exact-media, fresh-install and second-boot gates are complete. See
[Beta 2 Release Notes](Beta-2-Release-Notes.md) for the tested scope and known
boundaries. Each website upload must still be downloaded again and checked
against the published byte size and SHA-256 before its button is enabled.
