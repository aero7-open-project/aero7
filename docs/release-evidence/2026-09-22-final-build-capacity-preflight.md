# Final-build capacity preflight

22 September 2026. Read-only preparation for the owner-approved final build;
no image was built, removed, signed or published during this check.

## Current result

The repository capacity guard was run against the retained prepared profiles on
the build filesystem. The online profile is 0.18 GiB and passes with 18.0 GiB
available. The offline profile is 1.87 GiB and stops before cleanup because its
conservative workspace floor is 21.6 GiB. This is a storage preflight failure,
not an ISO or installer test failure.

## Reviewed cleanup boundary

The two superseded r10 guest disks are the smallest sufficient reviewed cleanup
set:

| Disposable file after final-build approval | Bytes |
| --- | ---: |
| `/home/admin/VMs/aero7-beta2-r10-oTmJ9G/online/disk.qcow2` | 9,210,494,976 |
| `/home/admin/VMs/aero7-beta2-r10-oTmJ9G/offline/disk.qcow2` | 7,711,948,800 |
| **Total** | **16,922,443,776** |

No QEMU process is active and neither disk has an open file handle. Their r10
test results and exported logs remain in the repository evidence. Delete only
these two exact disk files immediately before an explicitly approved build;
retain their containing directories and non-disk evidence.

That cleanup would raise the available workspace above the offline guard while
preserving all of the following:

- the refreshed online/offline acceptance guests;
- the current builder VM and its inputs;
- both accepted 21 September internal candidate ISOs;
- the Windows 7 reference VM;
- selected packages, retained build sources, screenshots and release evidence.

The accepted candidate ISOs are also idle and have recorded hashes, but they are
not required in the first cleanup set and should remain until the new final
images pass exact-artifact verification. No broad VM directory, glob, repository
work tree or reference disk is an approved deletion target.

## Artifact-metadata finalizer follow-up

The final build now has a fail-closed local metadata step in
`scripts/finalize-release-artifacts.py`. It requires one regular, non-symlink
online image and one offline image with matching final-date filenames. It runs
the full release verifier on the recommended offline image first and the online
image second, then writes an offline-first `SHA256SUMS` and a Markdown artifact
table. Existing metadata is not overwritten, and a verifier failure leaves no
metadata behind.

Five focused tests cover the accepted pair, mismatched dates, wrong variants,
symlinks, verifier failure and overwrite refusal. The complete project suite now
passes all 160 tests. An end-to-end dry run against the two accepted 21 September
internal candidates reran both full release verifiers and reproduced their
recorded sizes and SHA-256 values in temporary metadata. Those dry-run files
were not retained as final artifacts and do not authorize signing, upload or
publication.

## Build boundary

After explicit approval, recheck open handles and free space, remove only the
two paths above, prepare the current `testing` source again, and run the online
and offline build paths with the current date. The resulting images still need
embedded-content verification, fresh install/OOBE/reboot acceptance, exact
sizes and SHA-256 values before they can be called final or handed to the
website owner.
