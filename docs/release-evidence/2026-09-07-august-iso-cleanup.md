# Approved August test ISO cleanup

Under the owner's permission to free space on the current build drive, removed
only this obsolete test image on 7 September 2026:

`/home/admin/Documents/Codex/Recovered-from-nvme1n1p3/Documents/scripts/aero7-beta2-test-iso/out/aero7-beta2-test-2026.08.24-x86_64.iso`

- Regular, non-symlink file with one link; size 1,424,932,864 bytes (1.33 GiB).
- SHA-256 before deletion:
  `9970ed106b8e42e0371046bfaaf1115c2387f6284a8b3dbb455719b93caa25c5`.
- No open holder reported by `fuser`; no loop devices or ISO filesystem mounts.
  Running QEMU uses the separate r9 offline disk, not this image.
- Rechecked the exact target and size immediately before permanent removal.
- Available space on `/dev/nvme0n1p4` rose from 43 GiB to 44 GiB.

This is not a Trash operation: recovery requires a rebuild or another copy.
No VM disk was deleted in this pass. Retained current r9 online/offline guests
and media, the builder, the r4 UFW compatibility guest, Windows reference,
desktop reference and its dependent wiki overlay, source, logs and screenshots.

The approved defaults remain implemented: update checking has an on/off
preference, package installation requires confirmation, fresh installations
use firewalld, and existing UFW setups are not migrated. A fresh local rerun
passed 22 firewall-default tests and 15 update-check tests. These are regression
checks, not acceptance of rebuilt final media. No host firewall or packages
changed, and no GitHub commit or push occurred.
