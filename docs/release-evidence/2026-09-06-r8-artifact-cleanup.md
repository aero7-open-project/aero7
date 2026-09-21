# Approved r8 artifact cleanup

The owner authorized using the current drive for build files and deleting old
VM disks and ISOs. The following four obsolete regular, non-symlink files were
permanently removed on 6 September 2026:

- `/home/admin/VMs/aero7-beta2-r8-pWRIgW/offline/disk.qcow2`
- `/home/admin/VMs/aero7-beta2-r8-pWRIgW/online/disk.qcow2`
- `work/beta2-profiles.UWsuLM/builder-output/r8-updater/aero7-beta2-offline-2026.09.06-x86_64.iso`
- `work/beta2-profiles.UWsuLM/builder-output/r8-updater/aero7-beta2-online-2026.09.06-x86_64.iso`

The ISO paths above are relative to this project. All VM qcow2 backing chains
were inspected with `qemu-img info --force-share --backing-chain`. No other
listed disk depends on either removed disk. Both r8 guests had previously shut
down normally. Actual running QEMU arguments point to the separate r9 disks and
ISOs. `fuser` found no holders on the four targets immediately before removal;
the loop-device list was empty.

Free space on `/dev/nvme0n1p4` rose from approximately 21 GiB to 40 GiB, reclaiming
approximately 19 GiB. Removal was not to Trash: the guest disks cannot be
recovered through Trash, and the ISOs require rebuilding or another copy.
Historical r8 logs, screenshots, checksums and directories remain, but those
guest disks can no longer be replayed.

Retained: running r9 online/offline guests and their immutable media, the build
VM, r4 UFW compatibility guests, Windows reference VM, desktop reference and
its dependent wiki overlay, all source, packages, logs and screenshots. No host
packages or firewall configuration were changed. No commit or publication.

The current selected-package static check also completed successfully in
`/tmp/aero7-dialog-selected-package-checks3.log`, including 133 backend tests
and native-dialog package linkage validation. Existing QML lint warnings remain
in the log. This is not fresh-install acceptance of the updated packages.
