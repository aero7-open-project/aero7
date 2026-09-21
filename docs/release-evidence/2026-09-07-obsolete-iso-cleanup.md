# Approved obsolete ISO cleanup — 7 September 2026

The owner approved using the current drive for build files and deleting old VM
disks and ISOs. This pass selects only the following three superseded regular,
non-symlink files under this project's `out/` directory:

| File | Bytes | SHA-256 before removal |
| --- | ---: | --- |
| aero7-beta2-offline-2026.09.05-x86_64.iso | 3314876416 | e414e4d4e98c07763be7368283a77f0a11087858c48e5461954e798925cae507 |
| aero7-beta2-online-2026.09.05-x86_64.iso | 1458135040 | e1af2fa2afef38a1cac8a5ad53ec2280693716a22b1c096c81b50e4d32f723aa |
| aero7-beta2-online-2026.09.06-x86_64.iso | 1458139136 | 81ceb52824608c76cdf5c02fd1915e6088ab5561aad20cbcc378f0c8c5c76a74 |

These are **not** the retained r9 media with a similar date in their filenames.
The immutable online and offline r9 images remain under
`work/beta2-profiles.UWsuLM/builder-output/r9-time-final/`.

Read-only checks found no file holders (`fuser`), no loop-device mappings, and
no running QEMU arguments referencing the selected files. The active VM uses
its installed r9 offline disk, without installation media. No VM disk is selected:
the stopped r9 online guest, builder, UFW compatibility guest, Windows reference,
and desktop reference plus its dependent wiki overlay remain useful for testing.

Source, packages, historical checksum manifests, screenshots, logs and the
ongoing Plasma package build are preserved. Removal is permanent, not to Trash,
so these images would require a rebuild or another copy to recover.

Status: all three targets permanently removed after a second file-type and
file-holder check. This reclaimed 6,231,150,592 apparent bytes (about 5.8 GiB).
`df -h .` now reports 46 GiB available on `/dev/nvme0n1p4`, up from 40 GiB.
The concurrent package build continues, so available capacity will change.

The approved product defaults remain unchanged: automatic update **checking**
can be enabled or disabled, installation requires confirmation, fresh installs
use firewalld, and existing UFW configurations are preserved. This cleanup does
not alter the host firewall or install host packages. No commit or publication.
