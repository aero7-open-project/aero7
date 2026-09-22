# Beta 2 build and release closure checklist

Updated 22 September 2026. Internal working record, not release approval.
The bug-fix pass, final online/offline build and exact-media VM acceptance are
complete. Signing, uploading, publishing or promoting packages is not
authorized by a passing local test.

## Evidence already established

- The selected package manifest contains 17 required packages and two optional
  packages. The [current release notes](BETA2-RELEASE-NOTES.md) match all 19
  archive identities and optional labels. The current source gate passes all
  160 integration tests and both archive-variant checks. The five additional
  tests cover fail-closed final-artifact metadata generation. The earlier
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
  checks remain mandatory before any approved build. The
  [22 September capacity refresh](release-evidence/2026-09-22-final-build-capacity-preflight.md)
  records the current 18.0 GiB state: online staging passes, offline staging
  requires 21.6 GiB, and two exact idle superseded r10 disk files form a
  sufficient approved-build cleanup set without deleting the accepted
  candidates, current builder or Windows reference VM.
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
native replay where applicable. The build approval was exercised for the local
pair below; it did not grant permission to sign, upload or publish.

## Exact-media and publication gates

- [x] Build and finalize the exact online/offline image pair. The
  [final-media report](release-evidence/2026-09-22-final-online-offline-media-acceptance.md)
  records filenames, exact byte sizes, SHA-256 values and successful artifact
  finalization.
- [x] Run a new no-network offline installation through OOBE, first login,
  optional-feature install/removal and reboot.
- [x] Run a separate new connected online installation through the same gate.
- [x] Verify first-login PolicyKit/UAC readiness and the rebooted taskbar File
  Explorer shortcut on both installed systems.
- [x] Preserve 1920×1080 login, desktop, feature-manager and File Explorer
  evidence while keeping physical GPU/hotplug and physical multi-monitor claims
  explicitly out of scope.
- [ ] Decide and verify package/release signing and repository-promotion state.
- [ ] Obtain final website download URLs, upload the exact artifacts and re-hash
  the downloaded bytes.
- [x] Obtain explicit Beta 2 publication approval from the release owner.
- [ ] Finish website layout and link checks after the exact artifacts are uploaded.

The [website handoff launch checklist](BETA2-WEBSITE-MAKER-HANDOFF.md#launch-checks)
tracks those remaining publication actions. Old r10 images and upgraded guests
are historical only; they are not being used as substitutes for the final-image
tests.
