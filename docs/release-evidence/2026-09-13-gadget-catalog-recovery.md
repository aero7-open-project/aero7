# Feed catalog preservation — 13 September 2026

Local bug-fix work only. No commit, push, final ISO build or publication.

## Reproduced data-loss path

Release-23 source tests open the actual Manage Feeds dialog against isolated
damaged catalogs, then use its Remove button. Five cases overwrite the original
file: truncated JSON, an object instead of an array, an invalid array member,
an incomplete entry and a malformed saved URL. Parse failures fall back to
defaults, and invalid entries in arrays are silently omitted; the next edit
saves that substitute list over the original. An oversized document also lacks
the expected error/protection. The [baseline](gadget-catalog-recovery-logs/baseline23.log)
records six failures, not six identical overwrite cases.

## Correction

Defaults now apply only when there is no saved catalog. Existing catalogs are
read with a 1 MiB bound and validated as a complete list of named HTTP/HTTPS
feeds. Invalid or unreadable files are retained without offering an editable
fallback. Manage Feeds shows an explanation, disables Add/Remove and provides
Try Again to reload after the file is repaired or restored. It does not attempt
to reconstruct lost data or silently delete the original. Successful reload
clears the error and re-enables editing. Save failure feedback uses the wrapped
status layout, and saves cannot exceed the reader's size limit.

Seven new real-dialog cases cover those six inputs plus denied read permission.
They verify byte preservation, disabled editing, visible feedback and successful
reload of a repaired file. The existing save-failure fixture now blocks the path
after successful loading, preserving its original purpose separately from the
new load-failure tests. Empty-list persistence, save retry and typed-URL retention
still pass. [Targeted results](gadget-catalog-recovery-logs/corrected24.log):
13 passed including setup/cleanup, zero failures or skips.

All [eight source test groups](gadget-catalog-recovery-logs/full24.log) pass,
including 142 gallery, 74 provider and 11 media Qt results. Only
`GadgetOptionsDialog.cpp` differs from the release-23 runtime source; the other
source change is regression coverage in `GalleryTest.cpp`.

## Candidate

Gadgets 24 builds normally under `work/beta2-gadgets24.XH1U0D` with two jobs;
all eight package-check groups pass. The host-only dependency bypass does not
disable tests and must not be used for normal VM installation.

- Source SHA-256: `8092b48838f146f09eca19fbb25a62c9c93299d38a3783016d0fe62170a134f6`.
- Archive SHA-256: `83d7b5c95d55f987320bac3b46ca8aefbca409a18a3b13153a76b162f32634d0`.
- Executable SHA-256: `1ddd25f6d8b3cc179a057f12dac275561b71a73a7fe8e06d380025edc2a9c979`.

Normal [VM upgrade](gadget-catalog-recovery-logs/upgrade24.log) passes dependency
checks and verifies the installed executable hash. The native private-host
replay uses an invalid mixed array containing one named feed and an invalid
numeric member. The [complete error](gadget-catalog-recovery-logs/a7-g24-catalog-error.png)
is visible, both edit buttons are disabled, and clicking Remove or retrying
before repair leaves the original file byte-identical to the fixture.

After repairing only that private QA file to remove the numeric member,
[Try Again](gadget-catalog-recovery-logs/a7-g24-catalog-reloaded.png) loads the
named feed, clears the error and re-enables editing. Closing and
[reopening](gadget-catalog-recovery-logs/a7-g24-catalog-reopened.png) retains the
repaired list without changing its bytes. The private host was stopped normally;
the user's ordinary gadget layout was not the corruption fixture.

The [normal-login audit](gadget-catalog-recovery-logs/login24/audit.log) passes
in Wayland session 20 on the same boot after logout/login. Autostart owns PID
58587, whose running executable matches the release-24 hash above. The actual
KWin child (58274), not only its launcher, has no permission-check bypass.
All 57 gadget files are present. Desktop services are active with zero restarts;
the failed user/system unit lists are empty at this checkpoint. The ordinary
account layout is byte-identical to the release-23 login baseline. This is a
normal-login check, not a new cold-boot test. The earlier
[attempt](gadget-catalog-recovery-logs/login24-password-timeout/audit.log)
stopped at sudo's password timeout; its nonzero result is retained.

The next-build manifest now selects Gadgets 24 with Control Panel 54 / KWin 7.3.
Manifest SHA-256: `6b62bdae37e68c4368e9c9a7127f101afa35e820d754ef2139946c64518c8a65`.
All [149 integration tests](gadget-catalog-recovery-logs/integration24.log),
[18 online archive checks](gadget-catalog-recovery-logs/online24.log), and
[53 offline archive / 35 repository-entry checks](gadget-catalog-recovery-logs/offline24.log)
pass. The source pin and optional/core package membership are unchanged.

Concurrent external edits, live provider availability and broader gadget
workflows are not proved by these catalog-load tests. Frozen ISOs are unchanged.
