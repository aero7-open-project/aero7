# Startup diagnostics — identified resources and bounded impact

Status: the previously unidentified SVG warnings are now traced to exact
installed resources. Qt rendering comparisons pass in the host and existing
offline guest. Other retained diagnostics are classified below. No production
asset, package, service configuration or security policy was changed. This
closes diagnostic triage, not all desktop testing or final-image acceptance.

## Exact package and installed files

Theme `6.7.0_742.r9c2d850-57` archive SHA-256 remains
`7c6d37e69418c3a9e406a5deffedbc5e6d11b4e8a37637e721c6d23abb1e2f0a`.
The selected package manifest remains
`36d3c6a00f369ff6f86cfde5124e7b712fffebe8ad3b111ffb88dc862f543258`.

The [archive scan](svg-startup-logs/selected-theme57.json) loads all 80 packaged
SVG/SVGZ resources under both desktop themes using Qt 6.11.2: none are rejected,
seven files produce 13 messages. The
[installed scan](svg-startup-logs/startup-svg.Poy8rf/render-audit/scan.json)
loads 200 resources, including other installed themes, and finds exactly the
same 13 messages in those seven files, with none rejected. All 80 selected
package resource hashes match the installed files in the
[comparison](svg-startup-logs/package-installed-comparison.json).
The guest's selected desktop theme is `Seven-Black`.

| Resource, relative to the theme directory | Cause | Measured scope |
| --- | --- | --- |
| `Seven-Black/widgets/panel-background.svg`, its opaque/translucent variants, and `Aero7/widgets/panel-background.svg` | Empty `path8012`; nonexistent `#image` fill on duplicate `north-center-2` rectangle | Removing these nodes in memory removes both messages. Every surviving individual panel element has identical bounds, transforms and pixels. Whole-document and `layer1` rendering do change, so this is not universal pixel equivalence. |
| `Seven-Black/widgets/calendar.svg` | Unreferenced `clipPath4500` contains `rect4502`, whose stroke/filter refer to nonexistent definitions | Removing that unused definition in memory removes the gradient warning; all 16 surviving renderable IDs/full-document samples remain identical. The removed definition's child ID is explicitly recorded as lost. |
| `Seven-Black/widgets/scrollbar.svgz` | Three `<path>` elements are incorrectly nested directly inside other paths | Qt rejects those children. In-memory removal clears exactly the three parent/child warnings; all 401 surviving renderable IDs/full-document samples remain identical. |
| `Seven-Black/widgets/pager.svgz` | Empty `path1012` | In-memory removal clears the truncated-path warning; all 94 surviving renderable IDs/full-document samples remain identical. This `.svgz` is plain XML, not gzip; the probe handles both forms. |

The [packaged panel consumer](svg-startup-logs/theme57-panel-consumer.qml)
selects `west`, `north`, `east`, `south` or the default FrameSvg prefix, not
`north-center-2`. The removed test nodes have no in-document references.
No replacements or newly drawn icons were introduced. These are retained
asset/parser diagnostics without a reproduced defect in the consumed elements;
we have not silently changed out-of-frame artwork to make logs look clean.

## Rendering experiment and controls

The [effect probe](svg-startup-logs/svg-effect-probe.cpp) reads the original
asset, removes only explicitly named nodes in a DOM copy held in memory, and
compares every surviving renderable element at 64×64, 256×80 and 320×240 pixels,
plus bounds and transforms. It never writes a theme file. The seven cases
cover 1,104 surviving element/document comparisons, each at all three sizes.

Each case has a serialization-only control: parsing and serializing without
removal must preserve rendering, IDs and diagnostics. This was important:
an early QA implementation changed text spacing when serializing the DOM.
Preserving spacing-only nodes and suppressing added indentation corrected the
probe before the counted runs. A separate initial wildcard-traversal mistake
caused a missing-ID exit; it was replaced with explicit DOM traversal. Neither
QA issue was a product defect. Missing-file and missing-ID negative controls
also verify nonzero failure, rather than empty successful results.

The [host result](svg-startup-logs/host-render-audit/summary.json) and
[installed-guest result](svg-startup-logs/startup-svg.Poy8rf/render-audit/summary.json)
both pass, with identical case identities, hashes, counts and classifications.
The latter ran inside the existing Wayland session with the guest's libraries;
this is a Qt SVG raster comparison, not a complete native KSVG cache/FrameSvg
test or a hardware-accelerated rendering claim. The
[actual calendar opened from the taskbar](svg-startup-logs/calendar-native-1920x1080.png)
is also visible at 1920×1080. The screen contains QA windows and is not a final
release promotional screenshot.

## Other diagnostics and actual service status

The current boot remains `8c9cd832-5bda-4ffe-b878-c9723b6ecb13`. The
[full audit](svg-startup-logs/startup-svg.Poy8rf/audit.log) retained unchanged
package lists, theme/panel config hashes and desktop service identities:
Shell PID 989, Plasma 792 and KWin service wrapper 671, each active with zero
restarts. It nevertheless **exited 1**, because its zero-failed-units assertion
found the scheduled offline update-check failure described below. It is not
reported as an entirely green audit.

| Diagnostic | Evidence and disposition |
| --- | --- |
| DRM/EGL/glamor initialization and software fallback | The actual [KWin support report](svg-startup-logs/startup-svg.Poy8rf/kwin-support.txt) reports active OpenGL compositing through Mesa llvmpipe. This non-3D virtio test VM is software-rendered. It establishes usable virtual rendering, not physical GPU-driver compatibility or performance. |
| Unknown XKB key symbols | The retained [user journal](svg-startup-logs/startup-svg.Poy8rf/user-journal.txt) explicitly says these xkbcomp errors are not fatal to the X server. Ordinary keyboard login and terminal input work; those particular extended media/privacy keys are not claimed tested. |
| No modem, battery charge threshold or kernel backlight interface | The same journal and the [boot system journal](selected-stack-logs/selected-stack-boot.H6UdCZ/system-journal.txt) identify absent ModemManager and unsupported virtual hardware. These features are unavailable in this guest; no fake hardware or settings were added. |
| Auxiliary host-portal registrations | The [entry inventory](svg-startup-logs/startup-svg.Poy8rf/portal-desktop-entries.txt) confirms missing application desktop entries for the five IDs reported by ksmserver, menu proxy, XEmbed proxy, ActivityManager and Powerdevil. Registration fails; that remains a metadata limitation, not a successful registration claim. Qt's retained registration patch logs the asynchronous error rather than aborting the process. The helpers remain visible in the process inventory. Previously verified capture/dialog behavior is not being expanded to every portal operation. |
| UAC `/proc/PID/root` registration refusal | Retained protected-process diagnostic. The [earlier actual approval/cancel replay](2026-09-09-uac-service-validation.md) established functioning authentication without weakening protection. This pass does not repeat that replay or bypass `/proc` access controls. |
| Online guest clocksource watchdog timeout | The [online boot journal](selected-stack-logs/selected-stack-boot.O6XFYN/system-journal.txt) contains a kernel remote-CPU watchdog read timeout while using kvm-clock. Reboot/login later passed; its precise host-scheduling cause is not established. Keep this as a virtual timing/performance limitation, not an Aero application fix or a physical timing guarantee. |
| Offline background update check | It ran automatically at 21:32:34, before the 21:38 SVG audit, and returned exit 1 with update availability unknown. The disconnected VM has only loopback and no route. No package was installed by the notification-only helper. This is the intentionally preserved failed-check behavior, not a desktop crash or proof that the system is up to date. |

The separate [status classification](svg-startup-logs/startup-status.R7vNIb/audit.log)
exits 0 after explicitly verifying **one failed user unit**,
`aero7-update-check.service`, no failed system units, its exit code 1 and exact
unknown-availability message, loopback-only networking, and active desktop
units with zero restarts. It does not reset, restart, hide or ignore the failure.
The installed helper hash is
`7d1e493fb26b4f051c52fa845d46bb0f86a41f6d2a8e10518c3b12357ae2bc49`,
matching maintained source and the [previous disconnected/reconnected recovery test](2026-09-08-online-update-recovery.md).
An initial classification attempt used an incorrect `/usr/bin` helper path and
stopped; [that log](svg-startup-logs/startup-status.S2IZ6D/audit.log) is retained.
The successful retry uses the installed unit's actual `/usr/lib` path.

## Remaining gate

No runtime package changes are justified by these bounded rendering results.
The known diagnostics remain visible and documented. Native overlapping vault
prompts/cancellation, requirement-to-evidence review and build-space planning
still need closure. The 153 integration tests were not rerun for this read-only
diagnostic pass. Final ISO build, fresh-image acceptance, screenshots and
publication remain separate, explicitly approved steps.

After updating this report, the QA status, pre-build checklist and website
handoff, all 139 local Markdown link targets across those four files exist.
This check does not validate remote URLs or section anchors. Both retained
shell harnesses pass `bash -n`, and `git diff --check` passes.
