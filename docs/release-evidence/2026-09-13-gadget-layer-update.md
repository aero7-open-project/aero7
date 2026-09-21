# Gadget layer changes: immediate surface updates

## Native failure and correction

13 September 2026. The [KWin 7.2 installed replay](2026-09-12-gadget-show-desktop.md)
fixes gadgets disappearing with Show Desktop, but exposes a separate layer-commit
delay in Gadgets 14. A one-second capture after leaving Show Desktop shows
Calendar above the restored terminal. The trace proves that the Bottom request
does not commit until the next 60-second Calendar refresh.

`GadgetWindow` now calls `update()` after setting the layer in both its Show
Desktop callback and normal layer application (including Always on top). This
uses Qt's normal repaint/commit path without direct private Wayland calls or
changing normal Bottom/explicit Top behavior. Existing icon/artwork files,
permission values and desktop-entry identities remain unchanged.

## Controlled coverage

Four new gallery cases cover Show Desktop on/off and Always on top on/off.
They stop Calendar's periodic timer, initialize its layer to the opposite
target, and require both the correct layer and a new widget update request.

The initial harness gave a false positive because the initial hover-controls
animation was still producing paints. That log is preserved as contaminated
harness evidence, not a product pass. The corrected harness stops the animation
and drains pending updates before measuring the operation.

With that isolation, the old implementation has **43 passes, four failures**;
all four new layer-update cases fail. The correction passes **47 results,
zero failures**, including setup/cleanup. These are widget-level tests, not
proof of a compositor commit; the installed timed Wayland replay remains
required. Logs are in [gadget-layer-update-logs](gadget-layer-update-logs/).

## Package and release status

Gadgets 15 builds from the maintained Desktop companion at 13:56:27 CEST,
with all seven component groups passing (47 gallery and 74 provider Qt results).
The source archive SHA-256 is
`67a6ad7d63a93f16207443cbda75fe042ba3c5b627241c1ae0b31602a6736bca`.

- Package SHA-256: `7cffb6201cc26c6011262abc4b50ce0959cdddaa91e1a16eda586d1041912680`.
- Executable SHA-256: `4a98f3575be3e188080a11803c7f4670f9575236890130ceed872ba315435e8f`.
- Normal 14→15 offline upgrade passes in `gadgets15-upgrade.KFdTGD`, with all
  57 package files and the exact executable hash verified.
- The timestamp-normalized package manifest changes only the executable and
  build/package metadata; all other installed assets, launchers, hooks and
  file modes remain unchanged.

## Installed timed replay and normal login

The private Gadgets 15 replay `gadgets15-desktop.z2TABM` passes the scoped
layer-change checks under installed KWin 7.2. The retained Wayland trace shows
Calendar committing its Top request about 4 ms after the request and its Bottom
request about 7 ms afterward, including after Show Desktop was held longer than
the old 60-second refresh interval. One-second screenshots confirm that Calendar
returns behind restored applications. Always on top on/off commits promptly and
the corresponding visible stacking and stored boolean agree.

A held Clock drag preview remains visible during actual Meta+D Show Desktop;
the trace confirms the mode is active and the preview uses the Top layer.
Release restores the expected position. Separately, the taskbar's Show Desktop
button hides/restores applications with gadgets visible; that button uses its
minimize path, not the compositor's global Show Desktop signal. These are distinct
checks, not interchangeable evidence.

After stopping the private host and using normal logout/login, the audit
`gadgets15-login.S8OlOZ` passes in session 5 on 13 September. The autostart service
owns running host PID 8090 with the exact Gadgets 15 executable hash. The actual
compositor child has no permission-check bypass; shell, compositor and Plasma
services are active with zero restarts, and no failed user/system units are
listed. The normal account's empty layout is byte-identical to its preceding
Gadgets 14 login snapshot. This does not establish that all journal warnings or
all gadget workflows are resolved.

## Remaining menu findings

Right-clicking Calendar during Meta+D Show Desktop still restores hidden
applications. At 12:05:06 UTC the trace maps `xdg_popup#74`, attaches it using
the Calendar layer surface's `get_popup`, then reports `show_desktop_changed(0)`.
This is separate from the corrected delayed commits. The
[popup desktop-membership regression](2026-09-13-gadget-popup-membership.md)
now reproduces the failure before correction and passes the full 76-result
layer-shell suite afterward. KWin 7.3 is building; normal-package and installed
acceptance remain pending, so the full Show Desktop gate remains open.

The Always on top action changes state correctly, but its checked menu capture
does not visibly show a checkmark. The indicator needs further inspection.
Screenshots, runtime trace, final private layout, upgrade and normal-login logs
are preserved in [gadget-layer-update-logs](gadget-layer-update-logs/).

The media manifest still selects Gadgets 10 and
KWin 7.1. No final ISO, commit, push or publication is authorized.
