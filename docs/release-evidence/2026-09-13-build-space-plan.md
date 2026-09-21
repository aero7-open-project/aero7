# Reviewed build-space cleanup and final-build plan

13 September 2026. Uses the owner's existing authorization to remove old VM
disks and ISOs on the current drive. No final image was built. No host package,
firewall, source, selected package archive or active guest disk was removed.

## Measured cleanup

The online r10 test guest was shut down normally before starting the isolated
6 GiB/two-CPU builder. Only one VM ran at a time.

The [builder inspection](build-space-logs/prebuild-space.Z3O1Yo/inspection.log)
found no active image-build service or mkarchiso/mksquashfs/makepkg process.
The builder's ext4 `/dev/vda2` had 17,566,326,784 available bytes, while the host
had about 7.02 billion bytes available. Its output directory held six old ISO
copies, occupying approximately 13.6 GiB.

The [inventory](build-space-logs/builder-image-inventory.OU9N4H/images.sha256)
records all six exact names and SHA-256 values. The
[guarded cleanup](build-space-logs/cleanup-builder-image-copies.sh) rechecked
all six hashes, regular-file identity, single link, absence of file holders and
loop mappings before any deletion. It also hashed the four retained r9/r10 host
exports and confirmed that they matched the four corresponding builder copies.
Two other copies were explicitly superseded 6 September test images.

[Cleanup exited 0](build-space-logs/builder-image-cleanup.EcCT8X/audit.log).
Only those six ISO files were deleted; no directory was recursively removed.
Guest `fstrim /` then discarded blocks already free in the guest filesystem.
Its reported 33.2 GiB discard range is **not** the host-space gain. Host available
space increased to 26,080,444,416 bytes (24.3 GiB), while the guest had
32,200,704,000 bytes (30.0 GiB) available. Guest package inventory was unchanged.

The [r9 disk preflight](build-space-logs/r9-disk-preflight.json) then examined
all nine qcow2 files under `/home/admin/VMs`. Neither of the following targets
had a dependent backing chain, file holder or loop mapping:

- `/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-r9-xTfYQR/online/disk.qcow2`

Their hashes, inode/device identities and allocated sizes are recorded. Their
combined allocated size was 15,701,606,400 bytes (14.6 GiB). Immediately before
deletion the identities, link counts, holders and loops were rechecked.
[Both exact files were removed](build-space-logs/r9-disk-cleanup.log), leaving
**41,776,095,232 available host bytes (38.9 GiB)** at 22:32 CEST. Their firmware,
logs, screenshots, results, removable-media fixture and host ISO exports remain.

Removal is permanent, not Trash. The four duplicated builder images can be
restored from the retained host exports. The two superseded image copies and
two deleted r9 guest states require another copy or rebuilding/reinstalling.
Historical logs remain evidence, but do not make those deleted guests runnable.

## Protected material

- Current r10 online/offline disks, their synthetic retained data, firmware,
  launchers, results and exact frozen ISO exports.
- The r4 online **UFW compatibility guest**, which is not interchangeable with
  the newer firewalld guests.
- The isolated builder disk; Windows 7 reference; desktop reference; wiki
  overlay. The audit verifies that the wiki overlay depends on the desktop
  reference disk, so neither was selected for removal.
- All 18 selected package archives, all 95 audited source inputs and their
  resolved symlink targets, supplemental Git objects/hooks, build recipes,
  source worktrees, pinned Shell clone, logs and documentation.
- Required/optional package membership and manifest SHA-256 remain
  `36d3c6a00f369ff6f86cfde5124e7b712fffebe8ad3b111ffb88dc862f543258`.

Host-owned protected output directories could not all be listed without sudo.
They were excluded from cleanup, not treated as empty or disposable. No host
sudo access or broad recursive deletion was used.

## Build plan — after explicit approval only

1. Revalidate the chosen manifest/source inputs and measure each newly prepared
   profile. Existing r10 profiles and media are older inputs, not final artifacts.
   Use the isolated builder, two jobs, one variant at a time, on this drive.
2. Run the existing `scripts/check-build-space.py` against the **actual** profile,
   work and export filesystems immediately before each build. It requires
   `16 GiB + 3 × profile bytes` for workspace and `4 GiB + profile bytes` for a
   separate export filesystem. Do not consume filesystem reserved blocks.
3. In addition, account for the builder's sparse qcow2 and the exports sharing
   the same physical host drive. Plan for profiles up to **3 GiB**, **25 GiB**
   of build workspace growth, **7 GiB total** for both exported ISOs and their
   small manifests/logs, and **6 GiB host reserve**: **38 GiB** before the pair.
   The measured 38.9 GiB meets that planning floor narrowly, not permanently.
   If a profile exceeds 3 GiB, exports exceed the 7 GiB combined allowance, or
   concurrent disk usage consumes the reserve, stop and revise the budget.
4. Build sequentially, retaining the first completed image while building the
   second. Count already exported bytes against the combined export allowance,
   not as newly available space. After success, verify checksums and only clean
   the build's own known temporary staging, then trim the builder's free blocks.
   Preserve failed-build logs and inspect any unexpected leftover tree first.
5. Before fresh-install tests, remeasure host capacity. Reserve **12 GiB of
   allocated growth per new test disk**, plus the 6 GiB host reserve, and run
   only one 6 GiB/two-CPU test VM at a time. These are planning allowances,
   not limits enforced by qcow2 virtual size; monitor actual allocated growth
   and stop before exhausting the host. Keep existing r10 disks protected.
6. Final hashes, screenshot assets, fresh online/offline installation acceptance,
   package signing/promotion and publication remain separate gates. No old ISO
   or upgraded guest is relabeled as the final result.

The storage planning/cleanup item is closed. This is not a guarantee about
future package growth or approval to begin image building.
The builder was subsequently shut down through its normal Start-menu action;
PID 416858 exited and its QMP socket disappeared. No QEMU VM was left running
at the final host check. The current acceptance guests remain available on disk.
