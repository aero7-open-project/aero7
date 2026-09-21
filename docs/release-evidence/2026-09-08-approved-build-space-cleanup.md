# Approved build storage cleanup — 8 September 2026

The owner confirmed use of the current drive and authorized removal of old VM
disks and ISOs. This pass selects five superseded August test disks and two Beta 1
images, not the current Beta 2 acceptance guests or media.

Paths below are relative to the scripts workspace:

- `aero7-desktop-workcopies/aero7-iso-assets/work/test-vms/aero7-r34-coldboot.qcow2`
- `aero7-desktop-workcopies/aero7-iso-assets/work/test-vms/aero7-r36-r17-coldboot.qcow2`
- `aero7-desktop-workcopies/aero7-iso-assets/work/test-vms/aero7-r38-r18-final-install.qcow2`
- `aero7-desktop-workcopies/aero7-iso-assets/work/test-vms/aero7-r40-r19-final-install.qcow2`
- `aero7-desktop-workcopies/aero7-iso-assets/work/test-vms/aero7-r42-r30-final-install.qcow2`
- `aero7-iso/out/aero7-beta1-2026.08.09-x86_64.iso`
- `aero7-desktop-workcopies/aero7-iso-assets/out/aero7-beta1-2026.08.20-x86_64.iso`

Preflight: no fuser holders or loop mappings for these files; the running QEMU
uses the r10 offline guest and r10 offline ISO. QEMU backing-chain inspection
across the discovered VM locations found no dependent overlays on the selected
disks. The wiki overlay depends on the retained desktop reference disk.

Preserved: all r10 and r9 media/guests, r4 UFW compatibility guest, builder,
Windows reference, desktop reference and wiki overlay, source, packages,
screenshots and logs. No whole directory is selected for deletion. Older tests
remain historical evidence; deleted guest states will no longer be replayable.
Removal is permanent to reclaim space, not a move to Trash; recovery would
require another copy or rebuilding/reinstalling.

The approved defaults already exist in the current source: update checking has
an on/off preference, installation requires confirmation, fresh installations
select firewalld, and existing enabled or disabled UFW configurations are left
unchanged. This pass reran 22 firewall-default tests and 15 update-helper tests:
all passed. These are source regressions, not new final-media acceptance.
No host firewall changes, package installation, commit or publication.

Cleanup outcome: all seven exact files were permanently removed successfully.
Available space on `/dev/nvme0n1p4` rose from 8.8 GiB to 51 GiB, approximately
42 GiB reclaimed. No other artifact was removed in this pass.
