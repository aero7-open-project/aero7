# Build-space cleanup — 7 September 2026

The user authorized deleting old VM disks and ISOs on the current build drive.
Removed only this obsolete, stopped offline r4 test disk:

`/home/admin/VMs/aero7-beta2-r4-Nlm227/offline/disk.qcow2`

It occupied 7,716,265,984 bytes (about 7.2 GiB). QEMU process inspection and
`fuser` showed it was not open. Image metadata showed no backing image. All
eight remaining-before-cleanup qcow2 images under `/home/admin/VMs` were checked
for backing references; none depended on this disk. The wiki image's separate
dependency on the original desktop-test disk was preserved.

All r4 offline screenshots, exported logs, helpers and firmware files remain.
The deleted disk cannot be restored from Trash; restarting that old guest now
requires creating a new disk and reinstalling. Its launch helpers are historical
evidence, not currently runnable QA instructions.

Preserved both running r9 disks, the r4 online/UFW compatibility-test disk, the
ISO builder, Windows reference VM, original desktop-test and wiki disks. No ISO,
source archive, package archive or user source changes were deleted in this pass.
