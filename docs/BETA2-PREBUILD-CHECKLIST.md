# Beta 2 pre-build closure checklist

Updated 22 September 2026. Internal working record, not release approval.
The goal is to finish the bug-fix pass and website-update Markdown, then request
approval to build the final online and offline images. Building, signing,
publishing or promoting packages is not authorized by a passing local test.

## Evidence already established

- The selected package manifest contains 17 required packages and two optional
  packages. The [current release notes](BETA2-RELEASE-NOTES.md) match all 19
  archive identities and optional labels. The current source gate passes all
  155 integration tests and both archive-variant checks. The earlier
  [documentation checkpoint](release-evidence/2026-09-13-vault-overlap-and-docs.md)
  records the preceding 18-package/153-test selection for history.
- [Desktop 33](release-evidence/2026-09-13-desktop-source-cleanup.md) and
  [Control Panel 55](release-evidence/2026-09-13-control-panel-source-cleanup.md)
  have cleaned source exports and passing package tests. Their reports retain
  the exact runtime/source comparison boundaries.
- The original 18 selected archives have retained build recipes whose hashes match their
  embedded BUILDINFO. The [machine-readable audit](release-evidence/selected-stack-logs/build-recipes.json)
  records the original and relocated paths. This is local traceability, not
  proof of source completeness, reproducible binaries or trusted signing.
- Component tests cover the reproduced Explorer, screenshot, display, gadget,
  optional-feature, updater and session-recovery defects. The
  [QA history](BETA2-QA-STATUS.md) retains the individual package versions and
  failure/retest evidence. Historical VM results are not final-image acceptance.

## Remaining pre-build actions

- [x] Finish the current selected-stack audit in both existing test guests,
  including normal reboot, exact running components, optional-cache identities,
  retained account data and log review. Do not turn optional features on simply
  to make the two accounts identical. Both normal-reboot audits pass in the
  [selected-stack report](release-evidence/2026-09-13-selected-stack-alignment.md).
- [x] Close the source-input traceability review: connect each selected recipe
  to its retained source/patch inputs, distinguish later test-only changes from
  runtime changes, and record any missing inputs. Recipe hashes alone do not
  close this item. The [retained-source audit](release-evidence/2026-09-13-retained-source-inputs.md)
  verifies all 95 declared inputs plus the Gadgets install hook and Qt's
  supplemental commit, with no missing inputs. Five snapshot comparisons
  classify later test changes and Desktop's older nested vault source.
- [x] Replay simultaneous native vault unlock requests and cancellation. The
  [native two-window replay](release-evidence/2026-09-13-vault-native-prompts.md)
  verifies cancellation, retry, closing a pending client and completion by the
  survivor. Two further native unlock/read/lock cycles verify the retained test
  credential. The original ciphertext-hash assertion failed because save uses
  fresh random data; the failure and prompt-parenting limits remain documented.
- [x] Triage the remaining startup diagnostics. The [resource and runtime audit](release-evidence/2026-09-13-startup-diagnostic-triage.md)
  identifies all 13 theme SVG messages in seven installed resources, with
  controlled rendering comparisons and unchanged production assets. Graphics
  fallback, optional hardware and auxiliary portal metadata limitations remain
  explicitly documented. A later scheduled update check failed in the NIC-free
  guest, correctly reporting unknown availability; its failed state is retained,
  not masked by the earlier zero-failed-unit reboot checkpoints. No warning-free
  or complete physical-hardware claim is made.
- [x] Finish the requirement-to-evidence review for the website claims and the
  requested desktop workflows. The [review](release-evidence/2026-09-13-prebuild-requirement-review.md)
  maps current evidence and historical pending statements, and identifies the
  two unfulfilled presentation requirements below. Hardware/backends and final
  filenames, screenshots, hashes and URLs remain explicitly limited or pending.
- [x] Record a safe build-space plan for the selected inputs and both final
  artifacts. The [cleanup and plan](release-evidence/2026-09-13-build-space-plan.md)
  leave 38.9 GiB host space at the recorded checkpoint, with current guests,
  selected packages and retained sources/evidence protected. Fresh capacity
  checks remain mandatory before any approved build.
- [x] Complete the requested login Ease of Access dialog, including its six
  accessibility options and bottom desktop-environment tab. The rebuilt
  [21 September candidates](release-evidence/2026-09-21-rebuilt-online-offline-acceptance.md)
  pass the lower-left dialog and Aero7/AeroThemePlasma/Plasma session selector.
- [x] Resolve the normal-session vault password-dialog ownership/branding gap.
  The
  [20 September installed-VM replay](release-evidence/2026-09-20-vault-presentation-native-vm.md)
  proves the scoped Aero7 prompt, retry, cancel, overlap and retention behavior,
  and the accepted `kwallet 6.29.0-1.1` override is now selected in the source
  manifest. The
  [22 September refreshed-candidate acceptance](release-evidence/2026-09-22-selected-kwallet-candidate-acceptance.md)
  verifies both rebuilt image variants, exact installed package selection,
  default-off Vault state, local optional cache and the native first-use/password
  presentation titled **Aero7 Credential Vault** with the retained pack icon.

Newly reproduced product defects belong in this list with a regression test and
native replay where applicable. Passing these actions is the point to notify
the user and request final-build approval, not permission to publish.

## Later gates, after explicit approval

The [website handoff launch checklist](BETA2-WEBSITE-MAKER-HANDOFF.md#launch-checks)
still requires the exact newly built online/offline images to pass fresh
installation, first-run setup, reboot/login, desktop and failure-path checks.
Then obtain final 1920×1080 promotional screenshots, artifact checksums and
website download URLs. Package signing/repository promotion and publication
require their own verified, approved actions. Old r10 images and upgraded guests
do not substitute for those final-image tests.
