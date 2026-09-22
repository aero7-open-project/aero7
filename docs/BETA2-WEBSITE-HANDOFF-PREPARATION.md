# Beta 2 website handoff — preparation only

> **Superseded 22 September 2026.** Beta 2 publication is approved. Use the
> [approved website release handoff](BETA2-WEBSITE-MAKER-HANDOFF.md) for current
> copy, exact artifacts and launch checks.

Status: **Historical preparation brief; not a release announcement.**
Use the expanded [website-maker handoff](BETA2-WEBSITE-MAKER-HANDOFF.md)
for current draft copy and the
[corrected-candidate report](release-evidence/2026-09-05-fixed-candidate-acceptance.md)
for newer 1920×1080 VM results. Final refreshed-image acceptance remains pending.

The original state recorded below concerns the 4 September test images, which
failed the 5 September acceptance pass. See
[QA findings](release-evidence/2026-09-05-online-offline-iso-acceptance.md).
This brief lets the website team prepare layouts without announcing a release.

## Distribution and download page

- Host Beta 2 ISO downloads on the project's website, **not GitHub Releases**.
  GitHub remains the source/documentation/issue destination.
- Prepare two download cards: **Offline ISO — recommended** and **Online ISO**.
- Offline explanation: larger initial download; includes installation packages;
  avoids package-download delays during setup and supports installation without
  internet. Do not advertise optional-feature offline support until retested.
- Online explanation: smaller ISO; requires reliable internet throughout the
  package phase; download speed and mirror availability affect installation.
- Both installations keep the normal signed package repositories for later
  updates when connected to the internet.
- Final filenames, version/date, sizes, SHA-256 values, and direct website
  download URLs must come from the **new passing artifacts**, not this QA report.
- Prepare verification instructions and a visible beta/backup warning. Do not
  enable download buttons or label Beta 2 available before release approval.
- Preserve the existing release/download status until the replacement is approved.

## Product pages to prepare

1. **Desktop:** Aero7 Wayland session, glass/taskbar/Start design, factory pins,
   Recycle Bin, login/lock branding, and fallback session. Explain the KDE/Linux
   foundations; do not imply this is Microsoft Windows.
2. **File Explorer:** maintained Dolphin-based implementation, Explorer-style
   navigation, Libraries, Computer, familiar disk labels, and integrated dialogs.
3. **Control Panel:** Windows-inspired applet layout with real Linux settings.
   Separate implemented controls from unavailable hardware/optional backends.
4. **Desktop Gadgets:** gallery and included gadgets, configuration, and the
   internet requirement for live data such as Weather. Use the established icon
   pack and actual application assets; no replacement invented icons.
5. **Optional features:** Start/Control Panel entry, what each feature does,
   requirements, install/remove behavior, retained data, and Programs Center Beta
   being optional. Link the final verified Optional Features guide.
6. **Installer and support:** online/offline choice, disk safety, first-run
   setup, updates, known limitations, and how to collect/share diagnostic logs.
   Explain that diagnostic bundles can contain machine/user identifiers and
   should be reviewed before sharing; never invite public password submission.

## Claims and screenshots requiring the final QA gate

The following restriction described the failed 4 September images, not newer
manually upgraded guests or the subsequent corrected candidates:

Do not present screenshot capture, searchable optional features, normal-session
persistence, or offline optional-feature cycling as passing today. These fail
or remain untested on the current images. Do not claim “everything works,”
universal hardware support, or a fixed installation-time improvement.

After the corrected images pass, capture fresh **1920×1080** screenshots from
those installed VMs: desktop, Start, Computer/Libraries, Control Panel, Screen
Resolution, Features, Gadgets, SDDM accessibility/session selection, lock screen,
and screenshot notification. Use a clean demonstration account and exclude
passwords, private paths, test terminals, and transient errors. Current QA
screenshots are 1024×768 failure evidence, not final promotional assets.

## Final handoff checklist (not completed)

- Approved release announcement draft after both installation/desktop gates pass.
- Exact tested hashes, byte sizes, filenames, and website URLs.
- Verified feature list, known issues, requirements and installation limitations.
- 1920×1080 screenshot set with captions and useful alt text.
- Updated handbook/wiki links and package-update guidance.
- Website download checks, checksum-download checks, and explicit publication approval.

No website edits, uploads, or publication were performed as part of this brief.
